import json,sys,os,difflib,unicodedata,re
sys.path.insert(0, os.path.dirname(__file__))
from lines import LINES
t1=json.load(open(sys.argv[1])); t2=json.load(open(sys.argv[2]))
W=[(a,b,w.strip()) for s in t1 for a,b,w in s["w"] if a<29.9]+[(a,b,w.strip()) for s in t2 for a,b,w in s["w"] if a>=29.9]
def norm(w):
    w=unicodedata.normalize("NFD",w.lower()); w="".join(c for c in w if unicodedata.category(c)!="Mn")
    return re.sub(r"[^a-z0-9đ]","",w)
mine=[]  # (line_idx, word)
for li,(s,e,t) in enumerate(LINES):
    for w in t.split(): mine.append([li,w,None,None])
A=[norm(m[1]) for m in mine]; B=[norm(w[2]) for w in W]
sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        m=mine[blk.a+k]; w=W[blk.b+k]; m[2],m[3]=w[0],w[1]
matched=sum(1 for m in mine if m[2] is not None); print("matched",matched,"/",len(mine))
# interpolate gaps, bounded by line start/end
n=len(mine)
for i in range(n):
    if mine[i][2] is None:
        j=i
        while j<n and mine[j][2] is None: j+=1
        li=mine[i][0]
        left = mine[i-1][3] if i>0 and mine[i-1][3] is not None else LINES[li][0]
        right= mine[j][2] if j<n else LINES[-1][1]
        if mine[i-1][0]!=li if i>0 else True: left=max(left,LINES[li][0])
        cnt=j-i
        for k in range(cnt):
            mine[i+k][2]=left+(right-left)*k/cnt; mine[i+k][3]=left+(right-left)*(k+1)/cnt
out=[]
for li,(s,e,t) in enumerate(LINES):
    ws=[[m[2],m[3],m[1]] for m in mine if m[0]==li]
    out.append({"s":s,"e":e,"words":ws})
json.dump(out,open("/home/user/work/final/captions.json","w"),ensure_ascii=False)
for o in out[:3]+out[18:21]: print(round(o["words"][0][0],2),round(o["words"][-1][1],2)," ".join(w[2] for w in o["words"])[:50])
