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
    assert s['entry'][0] == 'LOUISIANA. COURTS OF APPEAL.'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank
    assert s['entry'][0] == 'LOUISIANA. COURTS OF APPEAL.'

    # 1.1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 2
    assert s['entry'][1] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][0] == 'Advance reports. Edited and'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    assert s['entry'][1] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][0] == 'Advance reports. Edited and annotated by J. B. Herold.'
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    assert s['entry'][1] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][0] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank
    assert s['entry'][1] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][0] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'

    # 1.1.1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 4
    assert len(s['entry']) == 3
    assert s['entry'][2] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][1] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    assert s['entry'][0] == 'v. 7, no.'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank
    assert s['entry'][2] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][1] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    assert s['entry'][0] == 'v. 7, no.'

    # 1.1.1.1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['entry'][3] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][2] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    assert s['entry'][1] == 'v. 7, no.'
    assert s['entry'][0] == '20. Dec27. © 6Jan28; A1018985.'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    assert s['entry'][3] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][2] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    assert s['entry'][1] == 'v. 7, no.'
    assert s['entry'][0] == '20. Dec27. © 6Jan28; A1018985. 4Apr55; R148080.'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank


    # 1.1.1.2
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry

    out, err = capsys.readouterr()
    assert out == entry1

    assert s['entry'][3] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][2] == 'Advance reports. Edited and annotated by J. B. Herold. © West Pub. Co. (PWH)'
    assert s['entry'][1] == 'v. 7, no.'
    assert s['entry'][0] == '21. Feb28. © 17Feb28;'

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

    out, err = capsys.readouterr()
    assert out == entry2

    assert s['indent'] == 2
    assert len(s['entry']) == 2
    assert s['entry'][1] == 'LOUISIANA. COURTS OF APPEAL.'
    assert s['entry'][0] == 'Reports. Vol. 6. Edited by'

    
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
    

def test_single_line_continuations(capsys):
    inp = '''\
DISNEY (WALT) PRODUCTIONS.

  Little Hiawatha. By Walt Disney.
    (In Philadelphia inquirer) © Walt
    Disney Productions (PWH)

    © 10Nov40; A5-115958. 25Jan68;
      R427684.

    © 25May41; A5-119480. 26Jun68; R438012.

  The Los Angeles County Museum
    presents a retrospective exhibition
    of the Walt Disney medium.
    © 29Nov40; A154044. Walt Disney
    Productions (PWH); 25Jan68; R427864.

\
'''

    l = split_in(inp)

    entry1 = join_out((
        '00a2ad53-92ff-5e01-915b-1604a6dc3c52', '1', '1', '1', '1',
        'DISNEY (WALT) PRODUCTIONS.|' + \
        'Little Hiawatha. By Walt Disney. (In Philadelphia inquirer) ' + \
        '© Walt Disney Productions (PWH)|' + \
        '© 10Nov40; A5-115958. 25Jan68; R427684.'))

    entry2 = join_out((
        '6c390bc9-0b3e-59ee-b6ab-a3f95436acda', '1', '1', '1', '1',
	    'DISNEY (WALT) PRODUCTIONS.|' + \
        'Little Hiawatha. By Walt Disney. (In Philadelphia inquirer) ' + \
        '© Walt Disney Productions (PWH)|' + \
        '© 25May41; A5-119480. 26Jun68; R438012.'))

    entry3 = join_out((
        '3b663723-e643-57fc-8ba7-9ee189269c09', '1', '1', '1', '1',
        'DISNEY (WALT) PRODUCTIONS.|The Los Angeles County Museum ' + \
        'presents a retrospective exhibition of the Walt Disney medium. ' + \
        '© 29Nov40; A154044. Walt Disney Productions (PWH); 25Jan68; ' + \
        'R427864.'))

    s = {'state': unnest.State.start,
         'indent': 0,
         'page': 1,
         'entry_type': 'ENTRY',
         'volume': 1,
         'part': '1',
         'number': 1
    }

    # 1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 0
    assert s['part_indent'] == 0
    assert s['entry'][0] == 'DISNEY (WALT) PRODUCTIONS.'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    # 1.1
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 2
    assert s['part_indent'] == 2
    assert s['entry'][1] == 'DISNEY (WALT) PRODUCTIONS.'
    assert s['entry'][0] == 'Little Hiawatha. By Walt Disney.'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    assert s['indent'] == 4 # TODO: Keep this at 2
    assert s['part_indent'] == 2
    assert s['entry'][1] == 'DISNEY (WALT) PRODUCTIONS.'
    assert s['entry'][0] == 'Little Hiawatha. By Walt Disney. (In Philadelphia inquirer) © Walt'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    assert s['indent'] == 4 # TODO: Keep this at 2
    assert s['part_indent'] == 2
    assert s['entry'][1] == 'DISNEY (WALT) PRODUCTIONS.'
    assert s['entry'][0] == 'Little Hiawatha. By Walt Disney. (In Philadelphia inquirer) © Walt Disney Productions (PWH)'
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank


    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 4
    assert s['part_indent'] == 4
    assert s['entry'][2] == 'DISNEY (WALT) PRODUCTIONS.'
    assert s['entry'][1] == 'Little Hiawatha. By Walt Disney. (In Philadelphia inquirer) © Walt Disney Productions (PWH)'
    assert s['entry'][0] == '© 10Nov40; A5-115958. 25Jan68;'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing
    assert s['indent'] == 6
    assert s['part_indent'] == 4
    assert s['entry'][2] == 'DISNEY (WALT) PRODUCTIONS.'
    assert s['entry'][1] == 'Little Hiawatha. By Walt Disney. (In Philadelphia inquirer) © Walt Disney Productions (PWH)'
    assert s['entry'][0] == '© 10Nov40; A5-115958. 25Jan68; R427684.'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry
    assert s['indent'] == 4
    assert s['part_indent'] == 4
    assert s['entry'][2] == 'DISNEY (WALT) PRODUCTIONS.'
    assert s['entry'][1] == 'Little Hiawatha. By Walt Disney. (In Philadelphia inquirer) © Walt Disney Productions (PWH)'
    assert s['entry'][0] == '© 25May41; A5-119480. 26Jun68; R438012.'

    out, err = capsys.readouterr()
    assert out == entry1
    
    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.entry

    out, err = capsys.readouterr()
    assert out == entry2

    assert s['indent'] == 2
    assert s['part_indent'] == 2
    assert s['entry'][1] == 'DISNEY (WALT) PRODUCTIONS.'
    assert s['entry'][0] == 'The Los Angeles County Museum'

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.continuing

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.blank

    s = unnest.transition(unnest.TRANSITIONS, s, next(l))
    assert s['state'] == unnest.State.start
    
    out, err = capsys.readouterr()
    assert out == entry3
    
