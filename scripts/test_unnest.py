import unnest
import parse


def split_in(s):
    return [line.rstrip() for line in s.split('\n')]

    
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

  s = unnest.transition(unnest.TRANSITIONS, s, l[0])
  assert s['state'] == unnest.State.entry

  s = unnest.transition(unnest.TRANSITIONS, s, l[1])
  assert s['state'] == unnest.State.continuing

  s = unnest.transition(unnest.TRANSITIONS, s, l[2])
  assert s['state'] == unnest.State.continuing
  
  s = unnest.transition(unnest.TRANSITIONS, s, l[3])
  assert s['state'] == unnest.State.blank

  s = unnest.transition(unnest.TRANSITIONS, s, l[4])
  assert s['state'] == unnest.State.start

  out, err = capsys.readouterr()
  assert out == expected

  assert s['indent'] == 0
  assert s['entry'] is None
