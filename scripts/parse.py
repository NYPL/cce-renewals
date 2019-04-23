#!/usr/bin/env python3 -u

import argparse
import csv
import dateutil.parser
import re
import sys

DATE_RE = r'\d{1,2}[A-z]{3}\d{1,2}'
ONE_DATE = re.compile(DATE_RE)

REGNUM_RE = r'(?:A(?:(?:A|F|I\-|5\-|6\-|O-))?|B(?:5\-)?|DP|I(?:U)?|[CDFGJKL]|Label |Print )\d+(?:\-\d+)?'
ONE_REGNUM = re.compile(REGNUM_RE)


RID_RE = r'R(?:\d+)'
CLAIMS_RE = r'.+\((?!See).+?\)'
DATE_REG_PAIR_RE = r'%s, %s' % (DATE_RE, REGNUM_RE)
PUB_ABROAD_RE = r'\(pub\. abroad.+?\)[,;]'
NEW_MATTER_RE = r'(?:on (?:.+?);)?'

shift_re = lambda r: re.compile(r'^(%s)(.*)$' % r)

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

RID_OR_RANGE = re.compile(r'(R\d+(?:(?:\-|, )\d+)?)')
RID_PARSE = re.compile(r'(?:R?(\d+)(?:(?:\-|, )(\d+))?)')
MIXED_RIDS_RE = r'((?:(?:R\d+(?:\-\d+)?)(?:,? )?)+)'
MIXED_RIDS = re.compile(MIXED_RIDS_RE)

REG_PARSE = re.compile(r'(A(?:(?:A|F|I\-|5\-|6\-|O\-))?|B(?:5\-)?|DP|I(?:U)?|[CDFGJKL]|Label |Print )(\d+)(?:\-(\d+))?')

CODE_SPLIT = re.compile(r'(?:\(([^\(]+)\))')

ONE_AI_REGNUM = r'(A(?:I|F)-\d+)'
ONE_AI = re.compile(ONE_AI_REGNUM)

AUTH_TITLE = re.compile(r'^(.*)([,;] by )((?:[^\(;](?!Pub. ))+)(.*)$')
AUTH_TITLE_F3 = re.compile(r'^(.+[\.\)])( By )((?:[^\(])+)(.*)$')

def record(**kwargs):
    return {**{'author': None, 'title': None, 'oreg': None,
               'odat': None, 'id': None, 'rdat': None,
               'claimants': None, 'previous': None, 'new_matter': None,
               'notes': None, 'see_also_ren': None,
               'see_also_reg': None}, **kwargs}


def shift_field(s, r, op=lambda x, y: (x, y)):
    m = r.match(s)
    return op(*(m[2].lstrip(';., '), [m[1]]))


shift_dates = lambda s: shift_field(s, SHIFT_DATES, extract_dates)

shift_one_date = lambda s: shift_field(s, SHIFT_ONE_DATE, extract_dates)

shift_regnums = lambda s: shift_field(s, SHIFT_REGNUMS, extract_regnums)

shift_date_reg = lambda s, op=lambda x, y: (x, y): shift_field(s, SHIFT_DATE_REG_PAIR, op)

shift_rids = lambda s: shift_field(s, SHIFT_RIDS, extract_rids)

shift_pub_abroad = lambda s: shift_field(s, SHIFT_PUB_ABROAD, extract_interim)

shift_new_matter = lambda s: shift_field(s, SHIFT_NEW_MATTER,
                                         extract_new_matter)

shift_see_also = lambda s: shift_field(s, SHIFT_SEE_ALSO, extract_see_also)

def shift_claims(s):
    m = SHIFT_CLAIMS.match(s)
    return (m[2].lstrip(';., '),
            '||'.join(format_claims(split_on_codes(CODE_SPLIT.split(m[1])))))


def parse_date(d):
    try:
        dt = dateutil.parser.parse(d)
        if dt.year > 2000:
            return (dt - dateutil.relativedelta.relativedelta(years=100)).strftime('%Y-%m-%d')
    
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        # Not all the dates are valid
        return None
    

def extract_dates(reg, dates):
    return (reg, [parse_date(d) for d in ONE_DATE.findall(dates[0])])


def extract_regnums(reg, regnums):
    return (reg, unroll_regnums(ONE_REGNUM.findall(regnums[0])))


def extract_date_reg_pairs(reg, pairs):
    return (reg,
            [parse_date(d) for d in ONE_DATE.findall(pairs[0])],
            ONE_REGNUM.findall(pairs[0]))


def extract_rids(reg, rids):
    m = EXTRACT_RIDS.findall(rids[0])
    return (reg, unroll_rids(EXTRACT_RIDS.findall(rids[0])))


def unroll_rids(rids):
    """Recursively unroll rid id ranges into individual rids."""
    if not rids:
        return []

    m = rids[0]
    if m[1]:
        return ['R%d' % r for r in range(int(m[0]), int(m[1])+1)] + unroll_rids(rids[1:])
    return ['R%s' % m[0]] + unroll_rids(rids[1:])

    return []


def extract_interim(reg, r):
    m = re.search(r'\((pub\. abroad) (.+?)\)', r[0])
    return (reg, '||'.join(interim_pairs(m[1], m[2])))


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


def join_title_parts(p1, p2):
    if p2:
        if p2[1] == ' ':
            return p1.strip() + p2.strip()
        return p1.strip() + ' ' + p2.strip()
    return p1.strip()


def find_numbered_eds(author, title):
    m = re.match(r'^(.+)( [0-9]+(?:[nr]?d|th).+ed\.(?:, rev\.)?)$', author)
    if m:
        return (m[1], title + ', ' + m[2].strip())
    return (author, title)



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


def get_f3_new_matter(book):
    m = re.match(r'^(.+)(?:NM: )(.+)$', book)
    if m:
        return (m[1].strip(), m[2].strip())
    return (book, None)


def find_post_author(author, title):
    m = re.match(r'^(.+)(Prev\. pub\. .+)$', author)
    if m:
        return (m[1].strip(), title + ' ' + m[2].strip())
    return (author, title)
    

def get_f3_author_title(book):
    m = AUTH_TITLE_F3.match(book)
    if m:
        title = join_title_parts(m[1], m[4]).strip()
        author, title = find_numbered_eds(m[3].strip(), title)
        author, title = find_post_author(author, title)
        return (author, title)
    return (None, book)

    
def interim_pairs(s, p):
    dates = [parse_date(d) for d in ONE_DATE.findall(p)]
    numbers = ONE_AI.findall(p)

    if len(dates) == len(numbers):
        return [one_ai(s, p) for p in zip(dates, numbers)]

    # Its okay if there is only one date and no number
    if len(dates) == 1 and len(numbers) == 0:
        return [one_ai(s, (dates[0], ''))]

    raise Exception('Cannot parse interim registrations %s' % p)


def one_ai(s, p):
    return '|'.join([s, p[0], p[1]])
                  

def split_on_codes(c):
    """
    Pad out the list if the code is missing, otherwise trim the last
    empty item.

    """
    return (len(c) == 1 and (c[0], '')) or c[0:-1]


def format_claims(c):
    return (c and ('|'.join(cleanup_claim(c[0:2])),) + \
            format_claims(c[2:])) or ()


def cleanup_claim(c):
    """Remove leading punctuation and whitespace from claimant strings."""
    return (c[0].lstrip(',.& ').strip(), c[1])


def unroll_regnums(regs):
    """Recursively unroll rid id ranges into individual rids."""
    if not regs:
        return []

    m = REG_PARSE.match(regs[0])
    if m:
        if m[3]:
            return ['%s%d' % (m[1], r) for r in range(int(m[2]), int(m[3])+1)] + unroll_regnums(regs[1:])

        return [regs[0]] + unroll_regnums(regs[1:])

    return []


def all_singles(regdates, regnums, rids, rendates, interims):
    return len(regdates) == len(regnums) == len(rids) == \
        len(rendates) == 1 and (interims is None or len(interims) == 1)


def all_singles_but_interims(regdates, regnums, rids, rendates):
    return len(regdates) == len(regnums) == len(rids) == \
        len(rendates) == 1


def all_multiples(regdates, regnums, rids, rendates, interims):
    """All these are lists of the same length, except for interims which
       either has the same length as the others or is None."""

    return len(regdates) == len(regnums) == len(rids) == \
        len(rendates) and (interims is None or len(interims) == len(regdates))


def most_multiples(regdates, regnums, rids, rendates, interims):
    """All these are lists of the same length, except for interims which
       either has the same length as the others or is None."""

    max_len = max([len(l) for l in (regdates, regnums, rids, rendates)])
    return n_or_1(max_len, regdates) and \
        n_or_1(max_len, regnums) and \
        n_or_1(max_len, rids) and \
        n_or_1(max_len, rendates) and \
        n_1_or_none(max_len, interims)


def n_or_1(n, l):
    return len(l) in (1, n)


def n_1_or_none(n, l):
    return l is None or n_or_1(n, l)


def dehyphen(r):
    m = re.match(r'^AI\-(\d+)$', r)
    if m:
        return 'AI{}'.format(m[1])

    return r
    

def format_record(author=None, title=None, regdates=None, regnums=None,
                  rids=None, rendates=None, claims=None, notes=None,
                  previous=None, new_matter=None, see_also_ren=None,
                  see_also_reg=None):

    regnums = [dehyphen(r) for r in regnums]
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


def pad_and_unroll_records(author=None, title=None, regdates=None, regnums=None,
                           rids=None, rendates=None, claims=None, notes=None,
                           previous=None, new_matter=None, see_also_ren=None,
                           see_also_reg=None):
    max_len = max([len(l) for l in (regdates, regnums, rids, rendates)])
    return [record(**dict(zip(('author', 'title', 'odat', 'oreg', 'id', 'rdat',
                               'claimants', 'new_matter', 'previous'),
                              r))) for r in \
            zip([author] * max_len,
                [title] * max_len,
                unroll_to(max_len, regdates),
                unroll_to(max_len, regnums),
                unroll_to(max_len, rids),
                unroll_to(max_len, rendates),
                [claims] * max_len, [new_matter] * max_len,
                [previous] * max_len,
                [notes] * max_len)]


def unroll_to(n, l):
    return (len(l) == n and l) or \
        len(l) == 1 and l * n or \
        False


def add_metadata(p, r):
    return {**p,
            **{'full_text': ' '.join(r[-1].split('|'))},
            **dict(zip(('entry_id', 'volume', 'part', 'number', 'page'), r[0:5]))}


def format1(v):
    """Does the volume number correspond to format 1?"""
    return v in ('4', '5', '6', '7')


def format2(v, p):
    """Does the volume number correspond to format 2?"""
    return v in ('8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                 '18', '19', '20', '21', '22', '23', '24', '25', '26') \
                 or (v == '27' and p == '1')


def format3(v, p):
    """Does the volume number correspond to format 2?"""
    return (v == '27' and p == '2') or v in ('28', '29', '30', '31')


def cc_split(e):
    """Split on ©-symbol."""
    return [s.strip() for s in e.split('©')]


def parse(v, p, e):
    """Dispatch to proper parsing function based on expected format."""
    return format1(v) and f1_parse(e) or \
        format2(v, p) and f2_parse(e) or \
        format3(v, p) and f3_parse(e) or \
        [record()]


def f1_parse(e):
    """Dispatch to proper f1 parsing function based on number of parts."""
    p = e.split('|')
    if len(p) == 1:
        return f1_one_part(*p) or f1_date_reg_pairs(*p) or False

    if len(p) == 2:
        return f1_two_parts(*p) or False

    if len(p) == 3:
        return f1_three_parts(*p) or False

    return False
    

def f1_one_part(e):
    """Simplest version of f1 format."""
    try:
    #if 1:
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
            try:
                reg, prev = shift_pub_abroad(reg)
                reg, regnums = shift_regnums(reg)
            except:
                return False

        reg, rids = shift_rids(reg)
        reg, rendates = shift_dates(reg)
        reg, claims = shift_claims(reg)

        note = reg if len(reg) else None
            #raise Exception('Remaining string: %s' % reg)

        return format_record(author=author, title=title, regdates=dates,
                             regnums=regnums, rids=rids, rendates=rendates,
                             claims=claims, new_matter=newmatter, previous=prev,
                             notes=note)
    except TypeError:
        return False

    except ValueError:
        # Possible no ©
        return False


def f1_date_reg_pairs(e):
    """F1 format with date/regnum pairs."""
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

    
def f1_two_parts(p1, p2):
    if '©' in p2:
        if '©' not in p1:
            return f1_parse(f1_f2_rearrange_two_parts(p1, p2))

        return f1_rearrange_chiastic(p1, p2)

    return False


def f1_f2_rearrange_two_parts(p1, p2):
    pre, post = cc_split(p2)
    
    return (p1.strip() + ' ' + pre.strip()).strip() + ' © ' + post.strip()


def f1_rearrange_chiastic(p1, p2):
    try:
        p1a, p1b = cc_split(p1)
        p2a, p2b = cc_split(p2)

        return f1_parse(p1a + ' ' + p2a + ' © ' + p2b + ' ' + p1b)
    except ValueError:
        # Maybe too many ©'s because multiple entries have been run together
        return False
    


def f1_three_parts(p1, p2, p3):
    if '©' in p2 and '©' in p3:
        return f1_rearrange_three_parts(p1, p2, p3)
        
    return False

def f1_rearrange_three_parts(p1, p2, p3):
    p2a, p2b = cc_split(p2)
    p3a, p3b = cc_split(p3)

    return f1_parse(p1 + ' ' + p2a + ' ' + p3a + ' © ' + p3b + ' ' + p2b)

"""
Parse Format 2 (vols 8-)
"""

def f2_parse(e):
    """Dispatch to proper f2 parsing function based on number of parts."""
    p = e.split('|')
    if len(p) == 1:
        return f2_one_part(*p) or False #f2_date_reg_pairs(*p) or False

    if len(p) == 2:
        return f2_two_parts(*p) or False

    if len(p) == 3:
        return f2_three_parts(*p) or False

    return False


def f2_one_part(e, author=None):
    """Simplest version of format 2."""

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
            except:
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
            #raise Exception('Remaining string: %s' % reg)

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


def f2_date_reg_pairs(e, author=None):
    #if 1:
    try:
        book, reg = cc_split(e)
        prev = note = None
        reg, newmatter = shift_new_matter(reg)
        reg, dates, regnums = shift_date_reg(reg, extract_date_reg_pairs)
        reg, claims = shift_claims(reg)
        reg, rendates = shift_dates(reg)
        reg, rids = shift_rids(reg)

        if len(reg):
            return False
            #raise Exception('Remaining string: %s' % reg)

        return format_record(author=author, title=book, regdates=dates,
                             regnums=regnums, rids=rids, rendates=rendates,
                             claims=claims, new_matter=newmatter, previous=prev,
                             notes=note)

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
            #return False
            # raise Exception('Remaining string: %s' % reg)

        return format_record(author=author, title=title, regdates=dates,
                             regnums=regnums, rids=rids, rendates=rendates,
                             claims=claims, new_matter=newmatter, previous=prev,
                             notes=note)
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
        ('[*Blank page*]' not in e) and\
        ('[*Blank Page*]' not in e)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Load CCE xml into database')
    parser.add_argument('-f', '--file', metavar='FILE', type=str,
                    help='TSV file to process')
    args = parser.parse_args()

    fields = ('entry_id', 'volume', 'part','number', 'page', 'author',
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
