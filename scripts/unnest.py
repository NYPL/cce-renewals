#!/usr/bin/env python3

import argparse
from enum import Enum
import re
import uuid


class State(Enum):
    header = 0
    prologue = 1
    prologue_blank = 2
    start = 3
    entry = 4
    continuing = 5
    blank = 6
    unhandled = 7


NS = uuid.UUID('569a2de5-d88e-410c-9bec-83887e0d4ee6')


def hardleft():
    return r'^(\s{0})(\S.+)$'


def moredent(x):
    return r'^(\s{%d})(\S.+)$' % (x+2,)


def nodent(x):
    return r'^(\s{%d})(\S.+)$' % x


def undent(x):
    return r'^(\s{%d})(\S.+)$' % (x-2,)


def doubleundent(x):
    return r'^(\s{%d})(\S.+)$' % (x-4,)


def tripleundent(x):
    return r'^(\s{%d})(\S.+)$' % (x-6,)


def add(data, entry):
    return (entry[0] + ' ' + data,) + entry[1:]


def push(data, entry):
    return (data,) + entry


def error_out(s):
    return {**s, **{'state': State.unhandled}}


def change_state(c, s):
    return {'state': s, 'previous_state': c['state']}


def entry_type(d, s):
    return {True: 'CF',
            False: s}[bool(re.search(r'\bSEE\b', d))]


def level(c):
    """Calculate entry level from indentation."""

    if len(c[1]) % 2:
        raise Exception("Number of spaces is not a multiple of 2.")

    return int(len(c[1])/2)


def is_page_number(func):
    def wrapper(*args, **kwargs):
        status = args[0]
        data = args[1]

        # If this line is just a page number, update the page number
        # in the buffer and continue

        page = re.match(r"^<pb id='(\d+)\.(?:.+n=.+\/(\d+))?", data)
        if page:
            if page[2]:
                return {**status,
                        **{'page': int(page[2])}}

            return status

        # Otherwise just execute the function
        return func(status, data)
    return wrapper


def is_prologue(s):
    return re.match(r'^RENEWALS?', s)


def is_prologue_7(s):
    return re.match(r'^(\[\*|material. Information)', s)


def row_id(s):
    """Create a UUID v5 from the full text of the entry."""
    return uuid.uuid5(NS, s)


def full_text(status):
    return '|'.join(tuple(reversed(status['entry'])))


def is_cf(entry):
    return bool(sum(
        [len(re.findall(r'\bSEE(?: ALSO)?\b(?! [A-Z]{2,})',
                        e)) for e in entry]))


def output(status, depth):
    if not is_cf(status['entry']):
        print('\t'.join((str(row_id(full_text(status))),
                         str(status['volume']),
                         status['part'],
                         str(status['number']),
                         str(status['page']),
                         '|'.join(tuple(reversed(status['entry']))))))

    return status['entry'][-depth:]


def state_unhandled(status, data):
    raise Exception('UNHANDLED STATE')


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


@is_page_number
def state_prologue(status, data):
    if not data:
        return {**status,
                **change_state(status, State.prologue_blank)}

    return status


@is_page_number
def state_prologue_blank(status, data):
    if not data:
        return {**status,
                **change_state(status, State.start)}

    return {**status,
            **change_state(status, State.prologue)}


@is_page_number
def state_start(status, data):
    if not data:
        raise StopIteration()

    if re.match(r'\*\*\* END', data):
        raise StopIteration()

    contents = re.match(hardleft(), data)
    if contents:
        return {**status,
                **change_state(status, State.entry),
                **{'indent': len(contents[1]),
                   'part_indent': len(contents[1]),
                   'entry': (contents[2],),
                   'entry_type': entry_type(data, status['entry_type'])}}

    return error_out(status)


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


TRANSITIONS = {State.header: state_header,
               State.prologue: state_prologue,
               State.prologue_blank: state_prologue_blank,
               State.start: state_start,
               State.entry: state_entry,
               State.blank: state_blank,
               State.continuing: state_continuing,
               State.unhandled: state_unhandled}


TRANSITIONS2 = {State.header: state_header_7,
                State.prologue: state_prologue,
                State.prologue_blank: state_prologue_blank,
                State.start: state_start,
                State.entry: state_entry,
                State.blank: state_blank,
                State.continuing: state_continuing2,
                State.unhandled: state_unhandled}


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
