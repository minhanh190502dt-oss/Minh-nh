import subprocess, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from plan import SECS, SPEED, V0
RAW="/home/user/work/raw/raw.mp4"; OUT="/home/user/work/final/clips2"; FPS=30; EXT=14  # extra frames for crossfade (~0.45s)
TAIL=1.5
jobs=[]; tl=[]; frame_cursor=0
for si,(name,v0,v1,clips,fx) in enumerate(SECS):
    sec_start=(v0-V0)/SPEED; sec_end=(v1-V0)/SPEED + (TAIL if name=="outro" else 0)
    f0=round(sec_start*FPS); f1=round(sec_end*FPS); F=f1-f0
    nat=[(e-s)/(sp if isinstance(sp,(int,float)) else 1) for s,e,sp in clips]
    N=sum(nat); 
    # frames per clip, cumulative rounding
    acc=0; cuts=[]
    for i,L in enumerate(nat):
        a=round(acc/N*F); acc+=L; b=round(acc/N*F); cuts.append(b-a)
    for ci,((s,e,sp),L,nf) in enumerate(zip(clips,nat,cuts)):
        T=nf/FPS
        jobs.append(dict(i=len(jobs),sec=name,si=si,ci=ci,s=s,e=e,sp=sp,frames=nf,T=T,first=(ci==0),start=(f0+sum(cuts[:ci]))/FPS))
json.dump(jobs,open("/home/user/work/final/jobs.json","w"),indent=1)
def run(j):
    key=f"c{j['i']:03d}_{j['s']}_{j['e']}_{j['sp']}_{j['frames']}_{int(j['first'] and j['si']>0)}"
    f=f"{OUT}/{key}.mp4"
    if os.path.exists(f.replace(".mp4",".mov")) and "--force" not in sys.argv: return f.replace(".mp4",".mov")
    s,e,sp,T,nf=j['s'],j['e'],j['sp'],j['T'],j['frames']
    if j['i']<len(jobs)-1: nf=nf+EXT; T=nf/FPS
    dirn=1 if j['i']%2==0 else -1
    if sp=="freeze":
        play=min(e-s, T*0.45 if j['sec']!="outro" else e-s)
        src=play; vt=f"setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={T}"
        at=f"apad"
    else:
        L=(e-s)/sp
        if L>=T: k=1.0; src=T*sp; eff=sp
        else: eff=sp*L/T; src=e-s
        vt=f"setpts=(PTS-STARTPTS)/{eff:.5f}"
        # atempo chain
        a=eff; chain=[]
        while a<0.5: chain.append("atempo=0.5"); a/=0.5
        while a>2: chain.append("atempo=2"); a/=2
        chain.append(f"atempo={a:.5f}"); at=",".join(chain)+",apad"
    Z="1"
    vf=(f"{vt},fps={FPS},scale=w='trunc(1188*{Z}/2)*2':h='trunc(2112*{Z}/2)*2':eval=frame:flags=bicubic,"
        f"crop=1080:1920:x='(iw-1080)/2*(1+{0.6*dirn}*(t/{T:.3f}-0.5))':y='(ih-1920)/2*(1+{0.4*dirn}*(t/{T:.3f}-0.5))',"
        f"eq=saturation=1.12:contrast=1.04:brightness=0.01,format=yuv420p")
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{s}","-t",f"{src+0.1:.3f}","-i",RAW,"-vf",vf,
        "-af",f"{at},aresample=48000,atrim=0:{T:.4f}","-ac","2","-frames:v",str(nf),
        "-c:v","libx264","-preset","fast","-crf","18","-c:a","pcm_s16le","-t",f"{T:.4f}",f.replace(".mp4",".mov")],check=True)
    os.rename(f.replace(".mp4",".mov"),f) if False else None
    return f.replace(".mp4",".mov")
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(3) as ex: files=list(ex.map(run,jobs))
open("/home/user/work/final/list2.txt","w").write("\n".join(f"file '{f}'" for f in files))
json.dump(files,open("/home/user/work/final/files2.json","w"))
print(len(jobs),"clips; total",sum(j['frames'] for j in jobs)/FPS)
