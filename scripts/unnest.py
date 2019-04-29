#!/usr/bin/env python3

# Convert Project Gutenberg transcriptions of Catalog of Copyright
# Entries renewals to tab delimited files.
#
# See https://onlinebooks.library.upenn.edu/cce/
#
# This will read a plain text transcription of CCE renewals and
# "unnest" the entries. That is it will take text blocks with
# heirarchical indentation like this:
#
#   A
#     B1
#       C1
#       C2
#
#     B2
#       C3
#
# and generate flattened rows of output:
#
#   A|B1|C1
#   A|B1|C2
#   A|B2|C3
#
# The hierchical levels are indicated with pipe characters (|) in the
# output as shown
#
# In addition, the script adds metadata fields for page (parsed from
# the text file) and volume, part, and number (with values supplied by
# command-line parameters).

import argparse
from enum import Enum
import re
import uuid


# This script uses a state machine pattern, keeping track of blank
# lines and indentation to know where entries begin and end.
#
# All the possible states:
class State(Enum):
    header = 0
    prologue = 1
    prologue_blank = 2
    start = 3
    entry = 4
    continuing = 5
    blank = 6
    unhandled = 7


# Namespace for UUID. A version-5 UUID is calculated for each row
# using the text of the entry as the name and this as the namespace
NS = uuid.UUID('569a2de5-d88e-410c-9bec-83887e0d4ee6')

# Match a line with no indentation
HARDLEFT = r'^(\s{0})(\S.+)$'


# Match a line with more indentation than the current level
def moredent(x):
    return r'^(\s{%d})(\S.+)$' % (x+2,)


# Match a line with the same indentation as the current level
def nodent(x):
    return r'^(\s{%d})(\S.+)$' % x


# Match a line with one fewer indents
def undent(x):
    return r'^(\s{%d})(\S.+)$' % (x-2,)


# Match a line with two fewer indents
def doubleundent(x):
    return r'^(\s{%d})(\S.+)$' % (x-4,)


# Match a line with three fewer indents
def tripleundent(x):
    return r'^(\s{%d})(\S.+)$' % (x-6,)


# Add a line of text to the current (bottom-most) level of the entry
def add(data, entry):
    return (entry[0] + ' ' + data,) + entry[1:]


# Add a hierarchical level to the entry stack
def push(data, entry):
    return (data,) + entry


# Switch to unhandled state
def error_out(s):
    return {**s, **{'state': State.unhandled}}


# Switch to new state (s) and store the previous state
def change_state(c, s):
    return {'state': s, 'previous_state': c['state']}


# Check whether the entry is a cross reference
def entry_type(d, s):
    return {True: 'CF',
            False: s}[bool(re.search(r'\bSEE\b', d))]


# Calculate entry level from indentation.
#
# The level is the number of spaces of indentation divided by
# two. Raise an error if the indentation is not a multiple of two
def level(c):
    if len(c[1]) % 2:
        raise Exception("Number of spaces is not a multiple of 2.")

    return int(len(c[1])/2)


# Decorator for handling page numbers
#
# If the current line is a page number element, parse it for a page
# number and update the state if necessary, and carry on with the
# transition. If the current line is not a page number element, just
# hand off to the transition.
#
# Page number elements come in two forms. One that indicates a page
# break, where the page number is the last part of the 'n' attribute:
#
#     <pb id='016.png' n='1950_h1/A/0006' />
#
# And one with no 'n' attribute that indicates a column break. These
# are ignored:
#
#     <pb id='017.png' />
def is_page_number(func):
    def wrapper(*args, **kwargs):
        status = args[0]
        data = args[1]

        # If this line is just a page number, update the page number
        # in the state and continue

        page = re.match(r"^<pb id='(\d+)\.(?:.+n=.+\/(\d+))?", data)
        if page:
            if page[2]:
                return {**status,
                        **{'page': int(page[2])}}

            return status

        # Otherwise just execute the function
        return func(status, data)
    return wrapper


# Check whether we have reached the "prologue." That is the part after
# the Project Gutenberg file header, but before the first actual
# renewal entry.
def is_prologue(s):
    return re.match(r'^RENEWALS?', s)


# Check whether we have reached the prologue in files in the format
# used in 1973 and after
def is_prologue_7(s):
    return re.match(r'^(\[\*|material. Information)', s)


# Create a UUID v5 from the full text of the entry.
def row_id(s):
    return uuid.uuid5(NS, s)


# Format the full text of the entry. Hierachical levels join by pipes (|)
def full_text(status):
    return '|'.join(tuple(reversed(status['entry'])))


# Check whether the entry is a cross reference (look for 'SEE' or 'SEE
# ALSO' in the text)
def is_cf(entry):
    return bool(sum(
        [len(re.findall(r'\bSEE(?: ALSO)?\b(?! [A-Z]{2,})',
                        e)) for e in entry]))


# Output a tab-delimted line with metadata and clear the necessary
# levels of the entry (depth).
def output(status, depth):
    if not is_cf(status['entry']):
        print('\t'.join((str(row_id(full_text(status))),
                         str(status['volume']),
                         status['part'],
                         str(status['number']),
                         str(status['page']),
                         '|'.join(tuple(reversed(status['entry']))))))

    # Since the levels of the entry are stored in reverse order, for
    # example [C, B, A], and if the depth is 2, we want the 2 righmost
    # levels of the entry, that is [B, A]. Since presumable we have a
    # new entry starting with another 'C' level
    return status['entry'][-depth:]


# Handle the unhandled state. Which we do by throwing an error.
def state_unhandled(status, data):
    raise Exception('UNHANDLED STATE')


# Header state. We are in the Project Gutenberg file header and are
# looking for the start of the transcription prologue
@is_page_number
def state_header(status, data):
    if not data:
        return status

    if data:
        if is_prologue(data):
            return {**status,
                    **change_state(status, State.prologue)}
        return status

    return error_out(status)


# Header state for 1973- files
@is_page_number
def state_header_7(status, data):
    if not data:
        return status

    if data:
        if is_prologue_7(data):
            return {**status,
                    **change_state(status, State.prologue)}
        return status

    return error_out(status)


# Prologue state. We are in the prologue of the transcription (the
# little bit of text that precedes the entries in the printed volume)
# and looking for its end, indicated by two blank lines
@is_page_number
def state_prologue(status, data):
    if not data:
        return {**status,
                **change_state(status, State.prologue_blank)}

    return status


# Blank line in the prologue. When a second blank line is encountered,
# switch the the Start state and game on.
@is_page_number
def state_prologue_blank(status, data):
    if not data:
        return {**status,
                **change_state(status, State.start)}

    return {**status,
            **change_state(status, State.prologue)}


# Start state. We are expecting a new entry
@is_page_number
def state_start(status, data):
    # Reasons to stop reading the file
    if not data:
        raise StopIteration()

    if re.match(r'\*\*\* END', data):
        raise StopIteration()

    # Expect text with NO indentation
    contents = re.match(HARDLEFT, data)
    if contents:
        return {**status,
                **change_state(status, State.entry),
                **{'indent': len(contents[1]),
                   'part_indent': len(contents[1]),
                   'entry': (contents[2],),
                   'entry_type': entry_type(data, status['entry_type'])}}

    return error_out(status)


# Entry state. We are reading an entry, looking either for the
# continuation of the current level or a blank line.
@is_page_number
def state_entry(status, data):
    if not data:
        return {**status,
                **change_state(status, State.blank)}

    contents = re.match(moredent(status['indent']), data)
    if contents:
        return {**status,
                **change_state(status, State.continuing),
                **{'indent': len(contents[1]),
                   'entry': add(contents[2], status['entry']),
                   'entry_type': entry_type(data, status['entry_type'])}}

    return error_out(status)


# Continuing state. We are reading an entry and expecting more of the
# same (with the same indentation) or the start of a new level with
# more indentation
@is_page_number
def state_continuing(status, data):
    if not data:
        return {**status,
                **change_state(status, State.blank)}

    contents = re.match(nodent(status['indent']), data)
    if contents:
        return {**status,
                **change_state(status, State.continuing),
                **{'indent': len(contents[1]),
                   'entry': add(contents[2], status['entry']),
                   'entry_type': entry_type(data, status['entry_type'])}}

    contents = re.match(moredent(status['indent']), data)
    if contents:
        return {**status,
                **change_state(status, State.continuing),
                **{'indent': len(contents[1]),
                   'entry': add(contents[2], status['entry']),
                   'entry_type': entry_type(data, status['entry_type'])}}
    return error_out(status)


# Continuing state for 1973- files
@is_page_number
def state_continuing2(status, data):
    if not data:
        return {**status,
                **change_state(status, State.blank)}

    contents = data.strip()
    if contents:
        return {**status,
                **change_state(status, State.continuing),
                **{'indent': None,
                   'entry': add(contents, status['entry']),
                   'entry_type': 'ENTRY'}}

    return error_out(status)


# Blank state. We got a blank line. Another blank line will indicate
# the end of the current entry. Otherwise we expect a new part of the
# entry which may change the indentation level
@is_page_number
def state_blank(status, data):
    # Second blank line, output previous entry, clear status
    if not data:
        output(status, 0)
        return {**status,
                **change_state(status, State.start),
                **{'indent': 0,
                   'entry': [],
                   'entry_type': 'ENTRY'}}

    # Same indent level...
    contents = re.match(nodent(status['indent']), data)
    if contents:
        if status['previous_state'] == State.continuing:
            # ... as previous continuation. Start a new subentry
            return {**status,
                    **change_state(status, State.entry),
                    **{'indent': len(contents[1]),
                       'part_indent': len(contents[1]),
                       'entry': push(contents[2], status['entry']),
                       'entry_type': entry_type(data, status['entry_type'])}}

        if status['previous_state'] == State.entry:
            # ... as previous (sub-)entry start. Output previous entry
            # and start a new sub-entry of parent
            return {**status,
                    **change_state(status, State.entry),
                    **{'indent': len(contents[1]),
                       'part_indent': len(contents[1]),
                       'entry': push(contents[2],
                                     output(status, level(contents))),
                       'entry_type': entry_type(data, status['entry_type'])}}

    # Indent level increased. Start a new subentry
    contents = re.match(moredent(status['indent']), data)
    if contents:
        if status['previous_state'] == State.entry:
            return {**status,
                    **change_state(status, State.entry),
                    **{'indent': len(contents[1]),
                       'part_indent': len(contents[1]),
                       'entry': push(contents[2], status['entry']),
                       'entry_type': entry_type(data, status['entry_type'])}}

    # Indent level decreased after blank, output previous entry, start
    # new subentry of parent
    contents = re.match(undent(status['indent']), data)
    if contents:
        if status['previous_state'] in (State.continuing, State.entry):
            return {**status,
                    **change_state(status, State.entry),
                    **{'indent': len(contents[1]),
                       'part_indent': len(contents[1]),
                       'entry': push(contents[2],
                                     output(status, level(contents))),
                       'entry_type': entry_type(data, status['entry_type'])}}

    contents = re.match(doubleundent(status['indent']), data)
    if contents:
        return {**status,
                **change_state(status, State.entry),
                **{'indent': len(contents[1]),
                   'part_indent': len(contents[1]),
                   'entry': push(contents[2], output(status, level(contents))),
                   'entry_type': entry_type(data, status['entry_type'])}}

    contents = re.match(tripleundent(status['indent']), data)
    if contents:
        return {**status,
                **change_state(status, State.entry),
                **{'indent': len(contents[1]),
                   'part_indent': len(contents[1]),
                   'entry': push(contents[2], output(status, level(contents))),
                   'entry_type': entry_type(data, status['entry_type'])}}

    return error_out(status)


# State and their handlers
TRANSITIONS = {State.header: state_header,
               State.prologue: state_prologue,
               State.prologue_blank: state_prologue_blank,
               State.start: state_start,
               State.entry: state_entry,
               State.blank: state_blank,
               State.continuing: state_continuing,
               State.unhandled: state_unhandled}


# States and handlers for 1973- files
TRANSITIONS2 = {State.header: state_header_7,
                State.prologue: state_prologue,
                State.prologue_blank: state_prologue_blank,
                State.start: state_start,
                State.entry: state_entry,
                State.blank: state_blank,
                State.continuing: state_continuing2,
                State.unhandled: state_unhandled}


# Take the current state, apply the proper handler, get back and
# return a new state
def transition(transitions, status, l):
    return transitions[status['state']](status, l)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load CCE xml into database')
    parser.add_argument('-f', '--file', metavar='FILE', type=str,
                        help='File to process')
    parser.add_argument('-e', '--encoding', metavar='ENCODING', type=str,
                        default='utf-8', help='Encoding for file')
    parser.add_argument('-v', '--volume', metavar='VOLUME', type=int,
                        required=True, help='Source volume')
    parser.add_argument('-p', '--part', metavar='PART', type=str,
                        required=True, help='Source volume part')
    parser.add_argument('-n', '--number', metavar='NUMBER', type=int,
                        required=True, help='Source volume number')
    parser.add_argument('-7', '--post-1973', action='store_true',
                        help='Volume is 1973 pt. 2 or later format')
    args = parser.parse_args()

    if args.post_1973:
        transitions = TRANSITIONS2
    else:
        transitions = TRANSITIONS

    line_no = 0

    status = {'state': State.header,
              'indent': 0,
              'page': 1,
              'entry_type': 'ENTRY',
              'volume': args.volume,
              'part': args.part,
              'number': args.number}

    with open(args.file, encoding=args.encoding) as f:
        try:
            for line in f:
                line_no += 1

                line = line.rstrip()

                status = transition(transitions, status, line)

        except StopIteration:
            pass

        if 'entry' in status:
            output(status, 0)
