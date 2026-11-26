import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plan import SECS, SPEED, V0, VEND
from callouts import CALL
W="/home/user/work/final"; SFX="/home/user/work/sfx"
OFF=float(os.environ.get('HOOK_OFF','0'))
T=lambda v:OFF+(v-V0)/SPEED
def ts(x):
    x=max(0,x); h=int(x//3600); m=int(x%3600//60); s=x%60
    return f"{h}:{m:02d}:{s:05.2f}"
YEL="&H0000E6FF&"
REF=os.environ.get("STYLE")=="ref"
import refstyle as RS, refcontent as RC
def D(e):
    l,a,b,st,tx=e
    if st in ("Head","Serif","Small") and tx.startswith("{"): tx="{\\blur4"+tx[1:]
    return f"Dialogue: {l},{ts(a)},{ts(b)},{st},,0,0,0,,{tx}"
hdr=r"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter SemiBold,56,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,2,2,90,90,540,1
Style: Title,Baloo 2 ExtraBold,320,&H00FFFFFF,&H00FFFFFF,&H008B4FFF,&H96000000,0,0,0,0,100,100,2,0,1,16,9,5,40,40,0,1
Style: Script,Pacifico,205,&H00FFFFFF,&H00FFFFFF,&H00401A2E,&H96000000,0,0,0,0,100,100,0,0,1,7,5,5,40,40,0,1
Style: Hook,Inter Black,104,&H0000E6FF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,9,5,8,60,60,330,1
Style: Big,Baloo 2 ExtraBold,110,&H0000E6FF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,5,8,60,60,360,1
Style: Tag,Baloo 2 ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H007F3DFF,&H007F3DFF,0,0,0,0,100,100,0,0,3,14,0,8,70,70,360,1
Style: Loc,Inter ExtraBold,50,&H00FFFFFF,&H00FFFFFF,&H00202020,&H00202020,0,0,0,0,100,100,0,0,3,12,0,8,70,70,470,1
"""+(RS.HEADER_STYLES.replace("Style: Cap,","Style: CapR,") if REF else "")+r"""
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[]
POP=r"{\fscx30\fscy30\t(0,110,\fscx115\fscy115)\t(110,190,\fscx100\fscy100)\fad(0,160)}"
sfx=[]
if REF:
    for v,d,num,sm,ti,sub in RC.CHAPTERS:
        ev.extend(D(e) for e in RS.chapter(T(v),T(v+d),num,sm,ti,sub)); sfx.append(("sparkle",T(v)+0.1,0.3))
    for v,d,tx,k in RC.CHIPS:
        ev.extend(D(e) for e in RS.pill(540,1225,tx,k,T(v),T(v+d))); sfx.append(("pop",T(v),0.3))
    for v,d,sm,big in RC.SERIF:
        ev.extend(D(e) for e in RS.serif_big(T(v),T(v+d),sm,big)); sfx.append(("ding" if big in("bật mí","clip sau") else "pop",T(v)+0.1,0.4))
for v,d,txt,sty,s in ([] if REF else CALL):
    a=T(v); b=T(v+d)
    pre = POP if sty!="Loc" else r"{\fad(120,160)\move(-400,470,540,470,0,220)}"
    if sty=="Loc": txt="VỊ TRÍ: "+txt
    ev.append(f"Dialogue: 2,{ts(a)},{ts(b)},{sty},,0,0,0,,{pre}{txt}")
    if s=="riser_end": sfx.append(("riser",a-1.1,0.35))
    elif s and sty in ("Hook","Big"): sfx.append((s,a,{"boom":0.8,"pop":0.45,"sparkle":0.35,"shutter":0.7,"ding":0.45}[s]))
# running captions
caps=json.load(open(f"{W}/captions.json")); capev=[]
import re
from emphasis import KEY, RED, ZOOM
def emph(txt):
    marks=[]
    for ph,col,sc in [(k,("&H00A8F1FF&" if REF else "&H0000E6FF&"),(100 if REF else 108)) for k in sorted(KEY,key=len,reverse=True)]+[(r,("&H009A7BF2&" if REF else "&H003C3CFF&"),125) for r in RED]:
        for m in re.finditer(r"(?<![\w])"+re.escape(ph)+r"(?![\w])",txt,re.I|re.U):
            if not any(m.start()<e and s_<m.end() for s_,e,_,_ in marks): marks.append((m.start(),m.end(),col,sc))
    for s_,e,col,sc in sorted(marks,reverse=True):
        txt=txt[:s_]+"{\\c"+col+"\\fscx"+str(sc)+"\\fscy"+str(sc)+"}"+txt[s_:e]+"{\\c&H00FFFFFF&\\fscx100\\fscy100}"+txt[e:]
    return txt
for c in caps:
    words=c["words"]  # list of [v_s, v_e, word]
    # chunk to <=4 words / <=22 chars
    chunks=[]; cur=[]
    for w in words:
        cur.append(w)
        if len(cur)>=6 or len(" ".join(x[2] for x in cur))>26 or w[2].endswith((",",".","?","!")):
            chunks.append(cur); cur=[]
    if cur: chunks.append(cur)
    if len(chunks)>1 and len(chunks[-1])==1: x_=chunks.pop(); chunks[-1]+=x_
    for k,ch in enumerate(chunks):
        a=T(ch[0][0]); b=T(chunks[k+1][0][0]) if k+1<len(chunks) else T(ch[-1][1])+0.25
        capev.append([a,b,emph(" ".join(x[2].strip() for x in ch))])
capev.sort()
for k in range(len(capev)):
    if k+1<len(capev): capev[k][1]=min(capev[k][1],capev[k+1][0])
    if capev[k][1]>capev[k][0]+0.01: ev.append(f"Dialogue: 1,{ts(capev[k][0])},{ts(capev[k][1])},{'CapR' if REF else 'Cap'},,0,0,0,,{chr(123)+chr(92)+'blur3'+chr(125) if REF else ''}{capev[k][2]}")
open(f"{W}/subs.ass","w").write(hdr+"\n".join(ev)+"\n")
d1=T(152.0); d2=T(153.0)
if REF:
    SH=r'\t(0,60,\frz-6)\t(60,120,\frz6)\t(120,180,\frz-4)\t(180,240,\frz0)'
    ev.append(D((6,d1,d2,'Serif',f'{{\\an5\\pos(540,560)\\fs220\\1c{RS.PINKD}'+RS.POPT+SH+'}dở')))
    ev.append(D((6,d2,T(153.55),'Serif','{\\an5\\pos(540,470)\\fs170\\1c'+RS.PINKD+'\\s1\\alpha&H50&}dở')))
    ev.extend(D(e) for e in RS.serif_big(d2+0.15,T(153.55),'',"hết dở!",y=770,fs=150))
else:
    SH=r"\t(0,60,\frz-6)\t(60,120,\frz6)\t(120,180,\frz-4)\t(180,240,\frz0)"
    ev.append(f"Dialogue: 4,{ts(d1)},{ts(d2)},Big,,0,0,0,,{{\\an5\\pos(540,620)\\fs190\\1c&H003C3CFF&\\3c&H00FFFFFF&\\fscx40\\fscy40\\t(0,120,\\fscx110\\fscy110)\\t(120,200,\\fscx100\\fscy100){SH}}}DỞ")
    ev.append(f"Dialogue: 4,{ts(d2)},{ts(T(153.55))},Big,,0,0,0,,{{\\an5\\pos(540,560)\\fs150\\1c&H003C3CFF&\\3c&H00FFFFFF&\\s1\\alpha&H40&}}DỞ")
    ev.append(f"Dialogue: 4,{ts(d2+0.15)},{ts(T(153.55))},Big,,0,0,0,,{{\\an5\\pos(540,760)\\fs165\\frz-4\\fscx30\\fscy30\\t(0,140,\\fscx118\\fscy118)\\t(140,240,\\fscx100\\fscy100)\\fad(0,200)}}HẾT DỞ!")
sfx += [("boom",d1,0.45),("ding",d2+0.12,0.5),("sparkle",d2+0.2,0.4)]
# whooshes at section starts
for si,(name,v0,*_) in enumerate(SECS):
    if si>0: sfx.append(("whoosh",T(v0)-0.22,0.5))
from actions import ACTIONS
jobs=json.load(open(f"{W}/jobs.json"))
def raw2final(r):
    if OFF>0 and r<OFF: return r
    for j in jobs:
        s0,e0,sp,TT=j["s"],j["e"],j["sp"],j["T"]
        if sp=="freeze": used=min(e0-s0,TT*0.45 if j["sec"]!="outro" else e0-s0); eff=1
        else:
            L=(e0-s0)/sp; eff=sp if L>=TT else sp*L/TT; used=TT*eff
        if s0<=r<s0+used: return OFF+j["start"]+(r-s0)/eff
for r,n,vol in ACTIONS:
    f=raw2final(r)
    if f is None: print("skip action",r,n)
    else: sfx.append((n,f,vol))
TOTAL=T(VEND)+1.5
if OFF>0 and REF:
    ev.extend(D(e) for e in RS.hook(OFF)); sfx += [("pop",0.1,0.5),("sparkle",0.55,0.35),("swish",2.80,0.4),("boing",2.88,0.65)]
    open(f"{W}/subs.ass","w").write(hdr+"\n".join(ev)+"\n")
elif OFF>0:
    B1=r"{\an5\pos(390,600)\frz7\fscx0\fscy0\t(80,260,\fscx118\fscy118)\t(260,380,\fscx100\fscy100)\fad(0,200)}BYE"
    B2=r"{\an5\pos(700,800)\frz-5\1c&H004DE1FF&\fscx0\fscy0\t(380,560,\fscx118\fscy118)\t(560,680,\fscx100\fscy100)\fad(0,200)}BYE~"
    B3=r"{\an5\pos(560,1010)\frz-3\alpha&HFF&\t(750,1050,\alpha&H00&)\move(560,1060,560,1010,750,1050)\fad(0,200)}em đi đây"
    ev.insert(0,f"Dialogue: 3,{ts(0.0)},{ts(OFF)},Title,,0,0,0,,{B1}")
    ev.insert(0,f"Dialogue: 3,{ts(0.0)},{ts(OFF)},Title,,0,0,0,,{B2}")
    ev.insert(0,f"Dialogue: 3,{ts(0.0)},{ts(OFF)},Script,,0,0,0,,{B3}")
    sfx += [("pop",0.1,0.55),("pop",0.4,0.55),("sparkle",0.78,0.35)]
    open(f"{W}/subs.ass","w").write(hdr+"\n".join(ev)+"\n")
inputs=["-i",f"{W}/base_full.mov","-i","/home/user/work/final/voice_clean.wav"]
fc=[f"[1:a]aresample=48000,aformat=channel_layouts=stereo[vn]",f"anullsrc=r=48000:cl=stereo,atrim=0:{OFF:.3f}[sil]",f"[sil][vn]concat=n=2:v=0:a=1,apad,atrim=0:{TOTAL:.3f},asplit=2[vo][vk]",
    f"[0:a]volume='if(lt(t,{OFF}),1.5,0.4)':eval=frame[or]","[or][vk]sidechaincompress=threshold=0.01:ratio=14:attack=15:release=350:makeup=1[ord]"]
mixin=["[vo]","[ord]"]
for k,(n,t,vol) in enumerate(sfx):
    inputs+=["-i",f"{SFX}/{n}.wav"]; idx=k+2; ms=int(max(0,t)*1000)
    fc.append(f"[{idx}:a]volume={vol},adelay={ms}|{ms}[s{k}]"); mixin.append(f"[s{k}]")
fc.append(f"{''.join(mixin)}amix=inputs={len(mixin)}:normalize=0:duration=first,alimiter=limit=0.95[aout]")
TT="(in/30)"
def ramp(a0,b0,z,r=0.3): return f"(({z-1:.3f})*min(1\\,max(0\\,min(({TT}-{a0:.3f})/{r}\\,({b0:.3f}-{TT})/{r}))))"
ZC="+".join(ramp(T(a0),T(b0),z,0.35) for a0,b0,z in ZOOM)
ZF="0"
ZX=f"if(lt({TT}\\,4.0)*gt({ZF}\\,0)\\,590\\,540)"; ZY=f"if(lt({TT}\\,4.0)*gt({ZF}\\,0)\\,370\\,960)"
VZ=(f"zoompan=z='1+{ZC}+{ZF}':x='max(0\\,min({ZX}-iw/zoom/2\\,iw-iw/zoom))':y='max(0\\,min({ZY}-ih/zoom/2\\,ih-ih/zoom))':d=1:s=1080x1920:fps=30,")
BHZ="if(lt(in/30\\,0.15)\\,1+0.95*in/30/0.15\\,if(lt(in/30\\,0.25)\\,1.95-0.15*(in/30-0.15)/0.1\\,if(lt(in/30\\,0.78)\\,1.8\\,max(1\\,1.8-0.8*(in/30-0.78)/0.12))))"
BX="600-40*(t-3.0)-280"; BY="380-80*(t-3.0)-300"
if REF and OFF>0:
    inputs+=["-loop","1","-t","1.2","-i",f"{W}/headmask.png"]; mi=len([x for x in inputs if x=="-i"])-1
    inputs+=["-ss","2.85","-t","0.95","-i",f"{W}/base_full.mov"]; fi=mi+1
    fc.append(f"[{fi}:v]setpts=PTS-STARTPTS+2.85/TB,crop=560:600:x='{BX}':y='{BY}',setpts=PTS-STARTPTS,zoompan=z='{BHZ}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=560x600:fps=30,format=rgba[bfz]")
    fc.append(f"[{mi}:v]format=gray,trim=0:1,setpts=PTS-STARTPTS[bmk]")
    fc.append(f"[bfz][bmk]alphamerge,setpts=PTS+2.85/TB[bfa]")
    fc.append(f"[0:v][bfa]overlay=x='{BX}':y='{BY}':enable='between(t,2.85,3.8)':eof_action=pass[v0]")
    V0L="[v0]"
else: V0L="[0:v]"
fc.append(f"{V0L}{VZ}null[vout]") if os.environ.get("NO_TEXT") else fc.append(f"{V0L}{VZ}ass={W}/subs.ass,drawbox=x=0:y=0:w='iw*t/{TOTAL:.2f}':h=12:color={'0xF4A7C0@0.95' if REF else '0xFFE600@0.95'}:t=fill[vout]")
out=sys.argv[1] if len(sys.argv)>1 else f"{W}/final.mp4"
cmd=["ffmpeg","-v","error","-y",*inputs,"-filter_complex",";".join(fc),"-map","[vout]","-map","[aout]",
     "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart","-t",os.environ.get("TEST_T",f"{TOTAL:.3f}"),out]
if os.environ.get('SUBS_ONLY'): sys.exit(0)
r=subprocess.run(cmd); print("rc",r.returncode); r.check_returncode(); print("done",out,TOTAL)
