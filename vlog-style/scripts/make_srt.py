import re
def parse(path, layer):
    ev=[]
    for l in open(path).read().splitlines():
        if l.startswith(f"Dialogue: {layer},"):
            p=l.split(",",9)
            def sec(x): h,m,s=x.split(":"); return int(h)*3600+int(m)*60+float(s)
            txt=re.sub(r"\{[^}]*\}","",p[9]).replace("\\N"," ").strip()
            ev.append((sec(p[1]),sec(p[2]),txt))
    return sorted(ev)
def fmt(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000))%1000:03d}"
def write(ev,out):
    with open(out,"w") as f:
        for i,(a,b,t) in enumerate(ev,1): f.write(f"{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n")
A="/home/user/work/final/subs.ass"; O="/tmp/claude-0/-home-user-Minh-nh/3dbb16d0-1bc5-58cc-8994-67b181dcc473/scratchpad"
write(parse(A,1),f"{O}/phu_de_loi_thoai.srt")
write(parse(A,2)+parse(A,3),f"{O}/chu_nhan_manh.srt")
print("ok")
