import yaml,re,collections,sys
t=open(sys.argv[1]).read()
yaml.safe_load(re.sub(r'(?m)^(\s*[\w.]+:) =$',r'\1 "="',t))
names=re.findall(r'(?m)^\s*- ([A-Za-z0-9_ ]+):\s*$',t)
print('controls',len(names),'dups',[n for n,c in collections.Counter(names).items() if c>1])
lines=t.split('\n'); i=0; dupk=0
while i<len(lines):
    if lines[i].strip()=='Properties:':
        ind=len(lines[i])-len(lines[i].lstrip())+2; j=i+1; keys=[]
        while j<len(lines) and (lines[j].strip()=='' or len(lines[j])-len(lines[j].lstrip())>=ind):
            if len(lines[j])-len(lines[j].lstrip())==ind and re.match(r'\s*[\w.]+:',lines[j]): keys.append(lines[j].strip().split(':')[0])
            j+=1
        c=[k for k,v in collections.Counter(keys).items() if v>1]
        if c: dupk+=1; print('dupkey',lines[i-2].strip(),c)
        i=j
    else: i+=1
print('dupkeys',dupk)
bad=0; i=0
while i<len(lines):
    m=re.match(r'^(\s+)([\w.]+): \|[-+]?$',lines[i])
    if m:
        ind=len(m.group(1)); j=i+1; blk=[]
        while j<len(lines) and (lines[j].strip()=='' or len(lines[j])-len(lines[j].lstrip())>ind):
            blk.append(lines[j]); j+=1
        s=re.sub(r'//[^\n]*','','\n'.join(blk)); s=re.sub(r'/\*.*?\*/','',s,flags=re.S); s=re.sub(r'"[^"]*"','',s)
        for a,b in ('()','{}','[]'):
            if s.count(a)!=s.count(b): bad+=1; print('unbal',m.group(2),a,s.count(a),s.count(b))
        i=j
    else: i+=1
print('unbalanced',bad)
