import unnest
import parse


def split_in(s):
    return iter([line.rstrip() for line in s.split('\n')])

    
def join_out(s):
    return '\t'.join(s) + '\n'


def test_basic_entry(capsys):
    inp = '''\
ACTUAL BUSINESS ENGLISH, by P. H. Deffendall.
  © 1Aug22, A681161. R60449,
  5Apr50, P. H. Deffendall (A)

\
'''

    l = split_in(inp)

    expected = join_out((
        '7a3120c6-1d31-5715-942e-b38216e86c13', '1', '1',
        '1', '1',
        'ACTUAL BUSINESS ENGLISH, by P. H. Deffendall. © 1Aug22, A681161. ' + \
        'R60449, 5Apr50, P. H. Deffendall (A)'))

    s = {'state': unnest.State.start,
         'indent': 0,
         'page': 1,
         'entry_type': 'ENTRY',
         'volume': 1,
         'part': '1',
         'number': 1
    }

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
  
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.start

    out, err = capsys.readouterr()
    assert out == expected

    assert s['indent'] == 0
    assert s['entry'] is None


def test_multiple_cf():
    inp = '''\
A la recherche du temps perdu. SEE

  Le côté de Guermantes. R61350.

  Du côté de chez Swann. R61348.

\
'''

    l = split_in(inp)

    s = {'state': unnest.State.start,
         'indent': 0,
         'page': 1,
         'entry_type': 'ENTRY',
         'volume': 1,
         'part': '1',
         'number': 1
    }


    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 2
    assert len(s['entry']) == 2
    first_entry_head = s['entry'][-1]
    first_entry_body = s['entry'][0]
  
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 2
    assert len(s['entry']) == 2
    first_entry_head == s['entry'][-1]
    first_entry_body != s['entry'][0]

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.start


def test_two_sub_entries(capsys):
    inp = '''\
AN ADVANCED COURSE OF INSTRUCTION IN
  CHEMICAL PRINCIPLES, by Arthur A.
  Noyes and Miles S. Sherrill. Complete
  ed.

  © 16May22, A674144. R59672, 20Mar50,
    Clement Gould Noyes (NK)

  © 16May22, A674144. R61614, 27Apr50,
    Clement Gould Noyes (NK) & Miles S.
    Sherrill (A)

\
'''

    l = split_in(inp)

    entry1 = join_out((
        '16712954-673e-5adf-86e4-cea090dfd8c4', '1', '1', '1', '1',
        'AN ADVANCED COURSE OF INSTRUCTION IN CHEMICAL PRINCIPLES, ' + \
        'by Arthur A. Noyes and Miles S. Sherrill. Complete ed.|© ' + \
        '16May22, A674144. R59672, 20Mar50, Clement Gould Noyes (NK)'))

    entry2 = join_out((
        '12006c18-6111-520c-9b14-fd2c2b8347f5', '1', '1', '1', '1',
        'AN ADVANCED COURSE OF INSTRUCTION IN CHEMICAL PRINCIPLES, by ' + \
        'Arthur A. Noyes and Miles S. Sherrill. Complete ed.|© 16May22, ' + \
        'A674144. R61614, 27Apr50, Clement Gould Noyes (NK) & Miles S. ' + \
        'Sherrill (A)'))

    s = {'state': unnest.State.start,
         'indent': 0,
         'page': 1,
         'entry_type': 'ENTRY',
         'volume': 1,
         'part': '1',
         'number': 1
    }

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    # TODO: Make this 0 so it is the indentation of the entry part
    assert s['indent'] == 2 
    assert len(s['entry']) == 1

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    # First subentry
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 2 
    assert len(s['entry']) == 2

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    # TODO: Don't update indent when continuing
    assert s['indent'] == 4
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    # Second subentry
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 2
    assert len(s['entry']) == 2

    out, err = capsys.readouterr()
    assert out == entry1
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    assert s['indent'] == 4
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.start
    
    out, err = capsys.readouterr()
    assert out == entry2


def test_4_levels(capsys):
    inp = '''\
LOUISIANA. COURTS OF APPEAL.

  Advance reports. Edited and
    annotated by J. B. Herold.
    © West Pub. Co. (PWH)

    v. 7, no.

      20. Dec27. © 6Jan28; A1018985.
        4Apr55; R148080.

      21. Feb28. © 17Feb28;
        A1018986. 4Apr55; R148081.

  Reports. Vol. 6. Edited by
    J. B. Herold. © 10Nov27;
    A1010903. West Pub. Co. (PWH);
    5Jan55; R142306.

\
'''

    l = split_in(inp)

    s = {'state': unnest.State.start,
         'indent': 0,
         'page': 1,
         'entry_type': 'ENTRY',
         'volume': 1,
         'part': '1',
         'number': 1
    }

    entry1 = join_out((
        'e06e556d-3db4-51c7-9892-7ff4d44c737b', '1', '1', '1', '1',
        'LOUISIANA. COURTS OF APPEAL.|Advance reports. Edited and ' + \
        'annotated by J. B. Herold. © West Pub. Co. (PWH)|v. 7, no.|20. ' + \
        'Dec27. © 6Jan28; A1018985. 4Apr55; R148080.'))

    entry2 = join_out((
        '5edb4308-303f-5953-a106-d2cdb3ad9590', '1', '1', '1', '1',
        'LOUISIANA. COURTS OF APPEAL.|Advance reports. Edited and ' + \
        'annotated by J. B. Herold. © West Pub. Co. (PWH)|v. 7, no.|' + \
        '21. Feb28. © 17Feb28; A1018986. 4Apr55; R148081.'))

    entry3 = join_out((
        'ac07fa17-ee6b-59a0-92ce-787132801166', '1', '1', '1', '1',
        'LOUISIANA. COURTS OF APPEAL.|' + \
        'Reports. Vol. 6. Edited by J. B. Herold. © ' + \
        '10Nov27; A1010903. West Pub. Co. (PWH); 5Jan55; R142306.'))

    
    # 1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    # 1.1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 2
    assert len(s['entry']) == 2

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank
    assert s['entry'][1] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][0] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'

    # 1.1.1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 4
    assert len(s['entry']) == 3

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank
    assert s['entry'][2] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][1] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    assert s['entry'][0] == 'v. 7, no.'

    # 1.1.1.1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank
    assert s['entry'][3] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][2] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    assert s['entry'][1] == 'v. 7, no.'
    assert s['entry'][0] == '20. Dec27. © 6Jan28; A1018985. 4Apr55; R148080.'

    # 1.1.1.2
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry

    out, err = capsys.readouterr()
    assert out == entry1

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank
    assert s['entry'][3] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][2] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    assert s['entry'][1] == 'v. 7, no.'
    assert s['entry'][0] == '21. Feb28. © 17Feb28; A1018986. 4Apr55; R148081.'

    # 1.2
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 2
    assert len(s['entry']) == 2
    assert s['entry'][1] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][0] == 'Reports. Vol. 6. Edited by'

    out, err = capsys.readouterr()
    assert out == entry2

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank
    assert s['entry'][1] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][0] == 'Reports. Vol. 6. Edited by J. B. Herold. © 10Nov27; A1010903. West Pub. Co. (PWH); 5Jan55; R142306.'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.start

    out, err = capsys.readouterr()
    assert out == entry3
    
