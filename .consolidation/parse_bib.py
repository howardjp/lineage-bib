from __future__ import annotations
import re, json, sys
from dataclasses import dataclass
from pathlib import Path

ENTRY_START_RE = re.compile(r'@([A-Za-z]+)\s*([({])', re.M)
FIELD_START_RE = re.compile(r'([A-Za-z][A-Za-z0-9_.-]*)\s*=', re.M)

@dataclass
class Entry:
    type: str
    key: str
    fields: list[tuple[str,str]]
    start_line: int
    raw: str

    def field_dict(self):
        d={}
        for k,v in self.fields:
            if k.lower() not in d:
                d[k.lower()] = v
        return d


def strip_outer(v:str)->str:
    v=v.strip().rstrip(',').strip()
    changed=True
    while changed and len(v)>=2:
        changed=False
        if v[0]=='{' and v[-1]=='}':
            depth=0; inq=False; esc=False; ok=True
            for i,ch in enumerate(v):
                if esc: esc=False; continue
                if ch=='\\': esc=True; continue
                if ch=='"' and depth==0: inq=not inq; continue
                if inq: continue
                if ch=='{': depth+=1
                elif ch=='}':
                    depth-=1
                    if depth==0 and i != len(v)-1:
                        ok=False; break
            if ok and depth==0:
                v=v[1:-1].strip(); changed=True
        elif v[0]=='"' and v[-1]=='"':
            v=v[1:-1].strip(); changed=True
    return v


def split_top(text, delim=','):
    out=[]; start=0; b=0; p=0; q=False; esc=False
    for i,ch in enumerate(text):
        if esc: esc=False; continue
        if ch=='\\': esc=True; continue
        if ch=='"' and b==0: q=not q; continue
        if q: continue
        if ch=='{': b+=1
        elif ch=='}': b-=1
        elif ch=='(': p+=1
        elif ch==')': p-=1
        elif ch==delim and b==0 and p==0:
            out.append(text[start:i]); start=i+1
    out.append(text[start:])
    return out


def parse_fields(body):
    fields=[]
    for part in split_top(body):
        part=part.strip()
        if not part: continue
        m=FIELD_START_RE.match(part)
        if not m:
            fields.append(("__raw__",part))
            continue
        fields.append((m.group(1), strip_outer(part[m.end():])))
    return fields


def parse(text):
    entries=[]; pos=0; errs=[]
    while True:
        m=ENTRY_START_RE.search(text,pos)
        if not m: break
        typ=m.group(1).lower(); op=m.group(2); cl='}' if op=='{' else ')'
        depth=1; q=False; esc=False; i=m.end()
        while i<len(text) and depth:
            ch=text[i]
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch=='"' and depth==1: q=not q
            elif not q:
                if ch==op: depth+=1
                elif ch==cl: depth-=1
            i+=1
        line=text.count('\n',0,m.start())+1
        if depth:
            errs.append((line,'unterminated')); break
        content=text[m.end():i-1]
        parts=split_top(content)
        if not parts:
            errs.append((line,'no parts')); pos=i; continue
        key=parts[0].strip()
        body=content[len(parts[0])+1:] if len(parts)>1 else ''
        fields=parse_fields(body)
        entries.append(Entry(typ,key,fields,line,text[m.start():i]))
        pos=i
    return entries,errs

if __name__=='__main__':
    p=Path(sys.argv[1]); text=p.read_text(encoding='utf-8')
    entries,errs=parse(text)
    print('entries',len(entries),'errors',errs)
    for e in entries[:3]:
        print(e.type,e.key,e.start_line,e.field_dict())
