#!/usr/bin/env python3 -u

# Take tab delimited-files produced by unnest.py and parse and
# "unroll" the entries. "Unrolling" means to take a row that really
# representes multiple renewals and convert to as many rows as
# necessary, keeping all the numbers and dates corrdinated.
#
# Parsing might be done to one of two levels. If the author, title,
# claimants, etc. can be determined, these are all broken out into
# individual fields.
#
# If the individual fields can't be determined but we can try to
# extract at least the id numbers and dates while leaving the rest of
# the fields blank.
#
# If neither of the above is possible, just output the metadata fields
# and full text already in the unnested file, with the other fields
# blank.

import argparse
import csv
import dateutil.parser
import re
import sys

# Let a hundred regexes bloom...
# These handle all the patterns we are looking to to parse the entries

DATE_RE = r'\d{1,2}[A-z]{3}\d{1,2}'
ONE_DATE = re.compile(DATE_RE)

REGNUM_RE = r'(?:A(?:(?:A|F|I\-|5\-|6\-|O-))?|B(?:5\-)?|DP|I(?:U)?|' + \
            r'[CDFGJKL]|Label |Print )\d+(?:\-\d+)?'
ONE_REGNUM = re.compile(REGNUM_RE)


RID_RE = r'R(?:\d+)'
HAS_RID = re.compile(RID_RE)
DATE_REG_PAIR_RE = r'%s, %s' % (DATE_RE, REGNUM_RE)

CLAIMS_RE = r'.+\((?!See).+?\)'

PUB_ABROAD_RE = r'\(pub\. abroad.+?\)[,;]'
NEW_MATTER_RE = r'(?:on (?:.+?);)?'


# We have a number of regexes that look to extract certain kinds of
# info. This is a generic way to create a regex for each that just
# looks for it at the beginning if a line, User by the various
# shift_X() functions
def shift_re(r):
    return re.compile(r'^(%s)(.*)$' % r)


SHIFT_DATES = shift_re(r'(?:%s(?:[;,\.]) )+' % DATE_RE)
SHIFT_ONE_DATE = shift_re(DATE_RE)
SHIFT_REGNUMS = shift_re(r'(?:%s(?:,|\.) )+' % REGNUM_RE)
SHIFT_RIDS = shift_re(r'(?:(?:R?\d+(?:\-R?\d+)?(?:(?:, |\.|\b)))+)')

SHIFT_CLAIMS = shift_re(CLAIMS_RE)
SHIFT_DATE_REG_PAIR = shift_re(r'(?:%s(?:;|\.) )+' % DATE_REG_PAIR_RE)
SHIFT_PUB_ABROAD = shift_re(PUB_ABROAD_RE)
SHIFT_NEW_MATTER = shift_re(NEW_MATTER_RE)
EXTRACT_RIDS = re.compile(r'(?:(\d+)(?:\-R?(\d+))?)')
SHIFT_SEE_ALSO = shift_re(r'\(See also .+\)')
SEE_ALSO_NUMS = re.compile(r'\(See also (.+)\)')


RID_OR_RANGE_RE = r'(R\d+(?:(?:\-|, )\d+)?)'
RID_OR_RANGE = re.compile(RID_OR_RANGE_RE)
RID_PARSE = re.compile(r'(?:R?(\d+)(?:(?:\-|, )(\d+))?)')
MIXED_RIDS_RE = r'((?:(?:R\d+(?:\-\d+)?)(?:,? )?)+)'
MIXED_RIDS = re.compile(MIXED_RIDS_RE)

REG_PARSE = re.compile(r'(A(?:(?:A|F|I\-|5\-|6\-|O\-))?|B(?:5\-)?' +
                       r'|DP|I(?:U)?|[CDFGJKL]|Label |Print )' +
                       r'(\d+)(?:\-(\d+))?')

CODE_SPLIT = re.compile(r'(?:\(([^\(]+)\))')

ONE_AI_REGNUM = r'(A(?:I|F)-\d+)'
ONE_AI = re.compile(ONE_AI_REGNUM)

DATE_REG_PAIR2_RE = r'%s[,;] %s' % (DATE_RE, REGNUM_RE)
RID_DATE_PAIR_RE = r'{}, {}'.format(RID_OR_RANGE_RE, DATE_RE)
DATE_RID_PAIR_RE = r'{}; {}'.format(DATE_RE, RID_RE)


AUTH_TITLE = re.compile(r'^(.*)([,;] by )((?:[^\(;](?!Pub. ))+)(.*)$')
AUTH_TITLE_F3 = re.compile(r'^(.+[\.\)])( By )((?:[^\(])+)(.*)$')


# Return a record that is blank except for the fields supplied
def record(**kwargs):
    return {**{'author': None, 'title': None, 'oreg': None,
               'odat': None, 'id': None, 'rdat': None,
               'claimants': None, 'previous': None, 'new_matter': None,
               'notes': None, 'see_also_ren': None,
               'see_also_reg': None}, **kwargs}


# Extract info from the beginning of a string. Pattern for the info is
# in the passed in regex. by default return the extract info and the
# remainder of the string, but if a function is supplied, run that
# function with the extracted info and remainder and return the result
def shift_field(s, r, op=lambda x, y: (x, y)):
    m = r.match(s)
    return op(*(m[2].lstrip(';., '), [m[1]]))


# Various functions to extract particular info from the beginning of a string
def shift_dates(s):
    return shift_field(s, SHIFT_DATES, extract_dates)


def shift_one_date(s):
    return shift_field(s, SHIFT_ONE_DATE, extract_dates)


def shift_regnums(s):
    return shift_field(s, SHIFT_REGNUMS, extract_regnums)


def shift_date_reg(s, op=lambda x, y: (x, y)):
    return shift_field(s, SHIFT_DATE_REG_PAIR, op)


def shift_rids(s):
    return shift_field(s, SHIFT_RIDS, extract_rids)


def shift_pub_abroad(s):
    return shift_field(s, SHIFT_PUB_ABROAD, extract_interim)


def shift_new_matter(s):
    return shift_field(s, SHIFT_NEW_MATTER, extract_new_matter)


def shift_see_also(s):
    return shift_field(s, SHIFT_SEE_ALSO, extract_see_also)


def shift_claims(s):
    m = SHIFT_CLAIMS.match(s)
    return (m[2].lstrip(';., '),
            '||'.join(format_claims(split_on_codes(CODE_SPLIT.split(m[1])))))


# Convert dates to ISO-8601 format. Since dates in the renewals have
# only two digit years, the result may need to have 100 years
# subtracted.
#
# Return None if the date is invalid
def parse_date(d):
    try:
        dt = dateutil.parser.parse(d)
        if dt.year > 2000:
            minus100 = dateutil.relativedelta.relativedelta(years=100)
            return (dt - minus100).strftime('%Y-%m-%d')

        return dt.strftime('%Y-%m-%d')
    except ValueError:
        # Not all the dates are valid
        return None


# Various functions to extract info from strigs
def extract_dates(reg, dates):
    return (reg, [parse_date(d) for d in ONE_DATE.findall(dates[0])])


def extract_regnums(reg, regnums):
    return (reg, unroll_regnums(ONE_REGNUM.findall(regnums[0])))


def extract_date_reg_pairs(reg, pairs):
    return (reg,
            [parse_date(d) for d in ONE_DATE.findall(pairs[0])],
            ONE_REGNUM.findall(pairs[0]))


def extract_rids(reg, rids):
    return (reg, unroll_rids(EXTRACT_RIDS.findall(rids[0])))


def extract_interim(reg, r):
    m = re.search(r'\((pub\. abroad) (.+?)\)', r[0])
    return (reg, interim_pairs(m[1], m[2]), r[0])
    # return (reg, '||'.join(interim_pairs(m[1], m[2])))


def extract_new_matter(reg, r):
    try:
        m = re.search(r'on (.+)(?:;)', r[0])
        return (reg, m[1].strip())
    except TypeError:
        return (reg, None)


def extract_see_also(reg, r):
    m = SEE_ALSO_NUMS.match(r[0])
    try:
        rids = '|'.join(shift_rids(m[1])[1])
    except TypeError:
        rids = None
    try:
        regnums = '|'.join(shift_regnums(m[1]+', ')[1])
    except TypeError:
        regnums = None

    return (reg, rids, regnums)


# Turn a text list of renewal ids into a Python list of renewal IDs
# and extrapolate ranges if necessary
def unroll_rids(rids):
    """Recursively unroll rid id ranges into individual rids."""
    if not rids:
        return []

    m = rids[0]
    if m[1]:
        return ['R%d' % r for r in range(int(m[0]),
                                         int(m[1])+1)] + unroll_rids(rids[1:])
    return ['R%s' % m[0]] + unroll_rids(rids[1:])

    return []


# Join two parts of a title with proper spacing
def join_title_parts(p1, p2):
    if p2:
        if p2[1] == ' ':
            return p1.strip() + p2.strip()
        return p1.strip() + ' ' + p2.strip()
    return p1.strip()


# Look for '1st ed', '3rd ed., rev.', etc.
def find_numbered_eds(author, title):
    m = re.match(r'^(.+)( [0-9]+(?:[nr]?d|th).+ed\.(?:, rev\.)?)$', author)
    if m:
        return (m[1], title + ', ' + m[2].strip())
    return (author, title)


# Try to extract the author and title from an entry
def get_author_title(book):
    m = AUTH_TITLE.match(book)

    if m:
        if '[' in m[3] or '[' in m[1]:
            return (None, book)
        title = join_title_parts(m[1], m[4]).strip()
        author, title = find_numbered_eds(m[3].strip(), title)
        if re.search(r'[0-9]', author):
            return (None, book)
        return (author, title)

    return (None, book)


# Try to extract 'new matter' notice (format 3)
def get_f3_new_matter(book):
    m = re.match(r'^(.+)(?:NM: )(.+)$', book)
    if m:
        return (m[1].strip(), m[2].strip())
    return (book, None)


# Look for information that sometimes comes after the author
def find_post_author(author, title):
    m = re.match(r'^(.+)(Prev\. pub\. .+)$', author)
    if m:
        return (m[1].strip(), title + ' ' + m[2].strip())
    return (author, title)


# Try to extract the author and title from an entry (format 3)
def get_f3_author_title(book):
    m = AUTH_TITLE_F3.match(book)
    if m:
        title = join_title_parts(m[1], m[4]).strip()
        author, title = find_numbered_eds(m[3].strip(), title)
        author, title = find_post_author(author, title)
        return (author, title)
    return (None, book)


# Look for pairs of interim registration ids and dates
def interim_pairs(s, p):
    dates = [parse_date(d) for d in ONE_DATE.findall(p)]
    numbers = ONE_AI.findall(p)

    if len(dates) == len(numbers):
        return [one_ai(s, p) for p in zip(dates, numbers)]

    # Its okay if there is only one date and no number
    if len(dates) == 1 and len(numbers) == 0:
        return [one_ai(s, (dates[0], ''))]

    raise Exception('Cannot parse interim registrations %s' % p)


# Format one interim registration for output
def one_ai(s, p):
    #return '|'.join([s, p[0], p[1]])
    return [p[0], p[1]]



# Pad out the list if the code is missing, otherwise trim the last
# empty item.
def split_on_codes(c):
    return (len(c) == 1 and (c[0], '')) or c[0:-1]


# Format claimants and code for output
def format_claims(c):
    return (c and ('|'.join(cleanup_claim(c[0:2])),) +
            format_claims(c[2:])) or ()


# Remove leading punctuation and whitespace from claimant strings
def cleanup_claim(c):
    return (c[0].lstrip(',.& ').strip(), c[1])


# Recursively unroll rid id ranges into individual rids.
def unroll_regnums(regs):
    if not regs:
        return []

    unroll_re = r'((?:[A-Z]+|(?:AI|AIO|AF|AO|A5|B5)\-)(?:\-)?)' + \
                r'(\d{2,})(?:\-\1?(\d+))?'
    m = re.match(unroll_re, regs[0])

    if m:
        if m[3]:
            return ['%s%d' % (m[1], r) for r in
                    range(int(m[2]), int(m[3])+1)] + unroll_regnums(regs[1:])

        return [regs[0]] + unroll_regnums(regs[1:])

    return []


# Test whether the dates and ids are all single items
def all_singles(regdates, regnums, rids, rendates, interims):
    return len(regdates) == len(regnums) == len(rids) == \
        len(rendates) == 1 and (interims is None or len(interims) == 1)


# Test whether all the dates and ids are single items except for the
# interim registrations
def all_singles_but_interims(regdates, regnums, rids, rendates):
    return len(regdates) == len(regnums) == len(rids) == \
        len(rendates) == 1


# Test whether all these are lists of the same length, except for
# interims which must either have the same length as the others or be
# None.
def all_multiples(regdates, regnums, rids, rendates, interims):
    return len(regdates) == len(regnums) == len(rids) == \
        len(rendates) and (interims is None or len(interims) == len(regdates))


# Test wheter all these lists are as long as the longest or only have
# 1 item, except for interim registrations which might also be None
def most_multiples(regdates, regnums, rids, rendates, interims):
    max_len = max([len(l) for l in (regdates, regnums, rids, rendates)])
    return n_or_1(max_len, regdates) and \
        n_or_1(max_len, regnums) and \
        n_or_1(max_len, rids) and \
        n_or_1(max_len, rendates) and \
        n_1_or_none(max_len, interims)


# The length of list is either n or 1
def n_or_1(n, l):
    return len(l) in (1, n)


# The lenght of list l is n, 1, or None
def n_1_or_none(n, l):
    return l is None or n_or_1(n, l)


# Remove hyphens from class AI regnums
def dehyphen(r):
    m = re.match(r'^AI\-(\d+)$', r)
    if m:
        return 'AI{}'.format(m[1])

    return r


# Format a record for output
def format_record(author=None, title=None, regdates=None, regnums=None,
                  rids=None, rendates=None, claims=None, notes=None,
                  previous=None, new_matter=None, see_also_ren=None,
                  see_also_reg=None):

    regnums = [dehyphen(r) for r in regnums]
    notes = None if notes == '' else notes
    if all_singles(regdates, regnums, rids, rendates, previous):
        return [record(author=author, title=title, odat=regdates[0],
                       oreg=regnums[0], id=rids[0], rdat=rendates[0],
                       claimants=claims, new_matter=new_matter,
                       previous=previous, notes=notes,
                       see_also_ren=see_also_ren, see_also_reg=see_also_reg)]

    if all_singles_but_interims(regdates, regnums, rids, rendates):
        return [record(author=author, title=title, odat=regdates[0],
                       oreg=regnums[0], id=rids[0], rdat=rendates[0],
                       claimants=claims, new_matter=new_matter,
                       previous=previous, notes=notes,
                       see_also_ren=see_also_ren, see_also_reg=see_also_reg)]

    if all_multiples(regdates, regnums, rids, rendates, previous):
        return pad_and_unroll_records(author=author, title=title,
                                      regdates=regdates, regnums=regnums,
                                      rids=rids, rendates=rendates,
                                      claims=claims, new_matter=new_matter,
                                      previous=previous, notes=notes,
                                      see_also_ren=see_also_ren,
                                      see_also_reg=see_also_reg)

    if most_multiples(regdates, regnums, rids, rendates, previous):
        return pad_and_unroll_records(author=author, title=title,
                                      regdates=regdates, regnums=regnums,
                                      rids=rids, rendates=rendates,
                                      claims=claims, new_matter=new_matter,
                                      previous=previous, notes=notes,
                                      see_also_ren=see_also_ren,
                                      see_also_reg=see_also_reg)

    return False


# Our record may in fact be multiple records if the list of regnums,
# etc. has more than 1 item. Pad multiply one item lists to the length
# of the multiple item lists and return as many records as necessary
def pad_and_unroll_records(author=None, title=None, regdates=None,
                           regnums=None, rids=None, rendates=None,
                           claims=None, notes=None, previous=None,
                           new_matter=None, see_also_ren=None,
                           see_also_reg=None):
    max_len = max([len(l) for l in (regdates, regnums, rids, rendates)])
    return [record(**dict(zip(('author', 'title', 'odat', 'oreg', 'id', 'rdat',
                               'claimants', 'new_matter', 'previous', 'notes'),
                              r))) for r in
            zip([author] * max_len,
                [title] * max_len,
                unroll_to(max_len, regdates),
                unroll_to(max_len, regnums),
                unroll_to(max_len, rids),
                unroll_to(max_len, rendates),
                [claims] * max_len, [new_matter] * max_len,
                [previous] * max_len,
                [notes] * max_len)]


# Given a list l and a length n make sure that l has length n, or if l
# has length 1, multiply it to match length n.
#
# Return False if l has any length either than 1 or n.
def unroll_to(n, l):
    return (len(l) == n and l) or \
        len(l) == 1 and l * n or \
        False


# Add metadata fields to the record.
def add_metadata(p, r):
    return {**p,
            **{'full_text': ' '.join(r[-1].split('|'))},
            **dict(zip(('entry_id', 'volume', 'part', 'number', 'page'),
                       r[0:5]))}


# The format of the CCE renewals changed over time. Check the volume
# and number of the entry to determine if we should use format 1, 2, or 3

# Does the volume number correspond to format 1?
def format1(v):
    return v in ('4', '5', '6', '7')


# Does the volume number correspond to format 2?
def format2(v, p):
    return v in ('8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                 '18', '19', '20', '21', '22', '23', '24', '25', '26') \
        or (v == '27' and p == '1')


# Does the volume number correspond to format 3?
def format3(v, p):
    return (v == '27' and p == '2') or v in ('28', '29', '30', '31')


# Split on ©-symbol.
def cc_split(e):
    return [s.strip() for s in e.split('©')]


# Last ditch, just extract the numbers (format 1)
def f1_just_numbers(e):
    reg_date = re.findall(DATE_REG_PAIR_RE, e)
    if len(reg_date):
        rid_date = re.findall(
            r'(?:R\d+(?:(?:\-|, )\d+)?), \d{1,2}[A-z]{3}\d{1,2}', e)
        if len(rid_date):
            regdates = [parse_date(r.split(', ')[0]) for r in reg_date]
            regnums = [r.split(', ')[1] for r in reg_date]
            rid, rendate = rid_date[0].split(', ')
            rids = unroll_rids(EXTRACT_RIDS.findall(rid))
            return format_record(regdates=regdates,
                                 regnums=regnums, rids=rids,
                                 rendates=[parse_date(rendate)])
    return False


# Last ditch, just extract the numbers (format 2)
def f2_just_numbers(e):
    reg_date = re.findall(DATE_REG_PAIR2_RE, e)
    if len(reg_date):
        rid_date = re.findall(
            r'\d{1,2}[A-z]{3}\d{1,2}; (?:R\d+(?:(?:\-|, )\d+)*)', e)
        if len(rid_date):
            rendate, rid = rid_date[0].split('; ')
            regdates = [parse_date(re.split(r'[;,] ', r)[0]) for r in reg_date]
            regnums = unroll_regnums(
                [re.split(r'[;,] ', r)[1] for r in reg_date])
            rids = unroll_rids(EXTRACT_RIDS.findall(rid))

            if len(rids) > 200:
                # Handle typos like R312280-512281 (that is R312280-312281)
                return False

            return format_record(regdates=regdates,
                                 regnums=regnums, rids=rids,
                                 rendates=[parse_date(rendate)])
    return False


# Figure out which format we are dealing with and dispatch to the
# proper handler.
def parse(v, p, e):
    """Dispatch to proper parsing function based on expected format."""
    return format1(v) and f1_parse(e) or \
        format2(v, p) and f2_parse(e) or \
        format3(v, p) and f3_parse(e) or \
        [record()]


# Try several ways of parsing a format 1 entry
def f1_parse(e):
    """Dispatch to proper f1 parsing function based on number of parts."""
    p = e.split('|')

    if len(p) == 1:
        return f1_one_part(*p) or f1_date_reg_pairs(*p) or f1_just_numbers(e)

    if len(p) == 2:
        return f1_two_parts(*p) or f1_just_numbers(e)

    if len(p) == 3:
        return f1_three_parts(*p) or f1_just_numbers(e)

    return False


# Simplest version of f1 format.
def f1_one_part(e):
    note = []
    if 1:
    #try:
        book, reg = cc_split(e)
        author, title = get_author_title(book)
        reg, newmatter = shift_new_matter(reg)
        try:
            reg, dates = shift_dates(reg)
        except TypeError:
            reg, dates = shift_one_date(reg)

        try:
            reg, regnums = shift_regnums(reg)
            prev = None
        except TypeError:
            if 1:
            #try:
                reg, prev, prev_note = shift_pub_abroad(reg)
                print(prev)
                reg, regnums = shift_regnums(reg)
                dates += [r[0] for r in prev]
                regnums += [r[1] for r in prev]
                note += [prev_note.strip(' (),')]
            # except Exception:
            #    return False

        reg, rids = shift_rids(reg)
        reg, rendates = shift_dates(reg)
        reg, claims = shift_claims(reg)

        note += [reg] if len(reg) else []

        print(note)

        return format_record(author=author, title=title,
                             regdates=dates, regnums=regnums,
                             rids=rids, rendates=rendates,
                             claims=claims, new_matter=newmatter,
                             notes='|'.join(note))
    # except TypeError:
    #    return False

    #except ValueError:
        # Possible no ©
    #    return False


# F1 format with date/regnum pairs.
def f1_date_reg_pairs(e):
    try:
        book, reg = cc_split(e)
        author, title = get_author_title(book)
        reg, dates, regnums = shift_date_reg(reg, extract_date_reg_pairs)
        reg, rids = shift_rids(reg)
        reg, rendates = shift_dates(reg)
        reg, claims = shift_claims(reg)

        if len(reg):
            return False

        return format_record(author=author, title=title, regdates=dates,
                             regnums=regnums, rids=rids, rendates=rendates,
                             claims=claims)
    except TypeError:
        return False

    except ValueError:
        # Possible no ©
        return False


# F1 in two parts. depending on which parts contain a ©-symbol,
# rearrange the parts into something that can be parsed by another
# handler
def f1_two_parts(p1, p2):
    if '©' in p2:
        if '©' not in p1:
            return f1_parse(f1_f2_rearrange_two_parts(p1, p2))

        return f1_rearrange_chiastic(p1, p2)

    return False


# Rearrange the parts into a 1-part format
def f1_f2_rearrange_two_parts(p1, p2):
    pre, post = cc_split(p2)

    return (p1.strip() + ' ' + pre.strip()).strip() + ' © ' + post.strip()


# Take an 'A B B A' format and rearrange it to be more simple
def f1_rearrange_chiastic(p1, p2):
    try:
        p1a, p1b = cc_split(p1)
        p2a, p2b = cc_split(p2)

        return f1_parse(p1a + ' ' + p2a + ' © ' + p2b + ' ' + p1b)
    except ValueError:
        # Maybe too many ©'s because multiple entries have been run together
        return False


# Handle a three part entry by rearranging it into a one-part entry
def f1_three_parts(p1, p2, p3):
    if '©' in p2 and '©' in p3:
        return f1_rearrange_three_parts(p1, p2, p3)

    return False


def f1_rearrange_three_parts(p1, p2, p3):
    p2a, p2b = cc_split(p2)
    p3a, p3b = cc_split(p3)

    return f1_parse(p1 + ' ' + p2a + ' ' + p3a + ' © ' + p3b + ' ' + p2b)


#
# Parse Format 2 (vols 8-)
#

# Dispatch to proper f2 parsing function based on number of parts."""
def f2_parse(e):
    p = e.split('|')
    if len(p) == 1:
        return f2_one_part(*p) or f2_just_numbers(e)

    if len(p) == 2:
        return f2_two_parts(*p) or f2_just_numbers(e)

    if len(p) == 3:
        return f2_three_parts(*p) or f2_just_numbers(e)

    return False


# Simplest version of format 2.
def f2_one_part(e, author=None):
    try:
        title, reg = cc_split(e)

        newmatter2 = None
        if author is None:
            title, newmatter2 = get_f3_new_matter(title)
            author, title = get_f3_author_title(title)

        reg, newmatter = shift_new_matter(reg)
        note = None
        reg, dates = shift_dates(reg)
        try:
            reg, regnums = shift_regnums(reg)
            prev = None
        except TypeError:
            try:
                reg, prev = shift_pub_abroad(reg)
                reg, regnums = shift_regnums(reg)
            except Exception:
                return False

        reg, claims = shift_claims(reg)
        reg, rendates = shift_dates(reg)
        reg, rids = shift_rids(reg)
        try:
            reg, see_also_ren, see_also_reg = shift_see_also(reg)
        except TypeError:
            see_also_ren = see_also_reg = None

        if len(reg):
            return False

    except TypeError:
        return False

    return format_record(author=author, title=title, regdates=dates,
                         regnums=regnums, rids=rids, rendates=rendates,
                         claims=claims,
                         new_matter=(newmatter or newmatter2),
                         previous=prev, notes=note,
                         see_also_ren=see_also_ren, see_also_reg=see_also_reg)


def f2_two_parts(p1, p2):
    try:
        if '©' in p2:
            if '©' in p1:
                return f2_parse_two_cc(p1, p2)
                return False

            return f2_one_part(p2, author=p1) or \
                f2_date_reg_pairs(p2, author=p1) or \
                False
        return False
    except ValueError:
        # Too many ccs?
        return f2_rearrange_two_ccs(p1, *cc_split(p2))


def regnums_are_hyphenated(regnums):
    hy = [re.search(r'(?<!^[A-Z]\d)\-', r) is not None for r in regnums]
    return len([h for h in hy if h])


def f2_date_reg_pairs(e, author=None):

    try:
        book, reg = cc_split(e)
        prev = note = None
        reg, newmatter = shift_new_matter(reg)
        reg, dates, regnums = shift_date_reg(reg, extract_date_reg_pairs)

        # We might actualy have pairse of ranges, so bail
        if regnums_are_hyphenated(regnums):
            return False

        reg, claims = shift_claims(reg)
        reg, rendates = shift_dates(reg)
        reg, rids = shift_rids(reg)

        if len(reg):
            return False

        return format_record(author=author, title=book,
                             regdates=dates, regnums=regnums,
                             rids=rids, rendates=rendates,
                             claims=claims, new_matter=newmatter,
                             previous=prev, notes=note)

    except TypeError:
        return False


def f2_parse_two_cc(p1, p2, author=None):
    p1a, p1b = cc_split(p1)
    p2a, p2b = cc_split(p2)

    title = p1a + ' ' + p2a

    try:
        prev = note = None
        reg, newmatter = shift_new_matter(p2b)
        reg, dates = shift_dates(reg)
        reg, regnums = shift_regnums(reg)
        reg, rendates = shift_dates(reg)
        reg, rids = shift_rids(reg)
        reg, claims = shift_claims(p1b)

        if len(reg):
            title = p1a + ' ' + reg + ' ' + p2a

        return format_record(author=author, title=title,
                             regdates=dates, regnums=regnums,
                             rids=rids, rendates=rendates,
                             claims=claims, new_matter=newmatter,
                             previous=prev, notes=note)
    except TypeError:
        return False


def f2_three_parts(p1, p2, p3):
    if '©' in p2:
        if '©' in p3:
            p2a, p2b = cc_split(p2)
            p3a, p3b = cc_split(p3)
            return f2_parse_two_cc(p2a + ' © ' + p2b, p3, author=p1)

    return False


def f2_rearrange_two_ccs(author, title, p3, p4):
    prev = note = None
    try:
        reg, dates = shift_dates(p3)
        reg, regnums = shift_regnums(reg + ' ')

        if len(reg):
            return False

        reg, newmatter = shift_new_matter(p4)
        reg, claims = shift_claims(reg)
        reg, rendates = shift_dates(reg)
        reg, rids = shift_rids(reg)

        if len(reg):
            return False

        return format_record(author=author, title=title,
                             regdates=dates, regnums=regnums, rids=rids,
                             rendates=rendates, claims=claims,
                             new_matter=newmatter, previous=prev, notes=note)

    except TypeError:
        return False


def f3_parse(e):
    """Just dispose of the initial renewal id and treat as format 2."""
    return f2_parse(shift_rids(e)[0])


def do_parse(e):
    return ('non-renewal entr' not in e) and \
        ('[*Blank page*]' not in e) and \
        ('[*Blank Page*]' not in e) and \
        HAS_RID.search(e) is not None


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Load CCE xml into database')
    parser.add_argument('-f', '--file', metavar='FILE', type=str,
                        help='TSV file to process')
    args = parser.parse_args()

    fields = ('entry_id', 'volume', 'part', 'number', 'page', 'author',
              'title', 'oreg', 'odat', 'id', 'rdat',
              'claimants', 'previous', 'new_matter', 'see_also_ren',
              'see_also_reg', 'notes', 'full_text')

    writer = csv.DictWriter(sys.stdout, fieldnames=fields, delimiter='\t')
    writer.writeheader()
    with open(args.file) as tsv:
        reader = csv.reader(tsv, delimiter='\t')
        for row in reader:
            if do_parse(row[-1]):
                parsed = parse(row[1], row[3], row[-1])

                for p in parsed:
                    writer.writerow(add_metadata(p, row))
