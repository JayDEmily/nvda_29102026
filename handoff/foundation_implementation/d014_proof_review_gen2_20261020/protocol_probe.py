"""Independent finite protocol model, not extracted authored/production code."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Page:
    items:tuple
    cursor:str|None

seed=object()
finite=(seed,)
# Documentary reproduction of the protocol mismatch: a fabricated next-page
# offset into a one-record native sequence has no first member.
assert finite[1:101]==()
try:
    finite[1:101][0]
except IndexError:
    print('OLD_PROTOCOL_PRECONDITION: offset1 has no item; IndexError independently reproduced')
else:
    raise AssertionError('expected empty native offset')

def adversary(mode,cursor):
    if mode=='malformed':
        return Page((seed,),'bad')
    if mode=='repeat':
        return Page((seed,),'1')
    if mode=='empty':
        return Page((),'1')
    return Page((seed,),str(1 if cursor is None else int(cursor)+1))

# Authority-derived bounded consumer validates protocol after each response;
# deliberately independent of project classes, helpers and implementation.
for mode,expected,calls_expected in [('malformed','malformed',1),('repeat','repeated',2),('empty','empty-nonterminal',1),('cap','cap',1000)]:
    cursor=None
    seen=set()
    count=0
    reason=None
    for _ in range(1000):
        response=adversary(mode,cursor)
        count+=1
        cursor=response.cursor
        if not re.fullmatch('[1-9][0-9]*',cursor):
            reason='malformed'
            break
        if cursor in seen:
            reason='repeated'
            break
        if not response.items:
            reason='empty-nonterminal'
            break
        seen.add(cursor)
    else:
        reason='cap'
    assert reason==expected and count==calls_expected
    print('INDEPENDENT_MODEL',mode,reason,count,'no native-offset delegation')
print('DOCUMENTARY_ONLY; no authored/project module import/execution; not actual product GREEN')
