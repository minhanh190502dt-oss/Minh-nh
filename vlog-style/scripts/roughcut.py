import subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from segments import SEGS
RAW="/home/user/work/raw/raw.mp4"; OUT="/home/user/work/cut"
lst=[]; t=0; marks=[]
for i,(sec,s,e,sp) in enumerate(SEGS):
    f=f"{OUT}/seg_{i:03d}.mp4"; d=(e-s)/sp
    vf=f"setpts=PTS/{sp},fps=30,scale=1080:1920:flags=lanczos,eq=saturation=1.1:contrast=1.04,format=yuv420p"
    af=f"atempo={sp}" if sp!=1 else "anull"
    if not os.path.exists(f):
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(s),"-t",str(e-s),"-i",RAW,"-vf",vf,"-af",af+",aresample=48000",
          "-ac","2","-c:v","libx264","-preset","fast","-crf","18","-c:a","aac","-b:a","192k","-t",f"{d:.3f}",f],check=True)
    lst.append(f"file '{f}'"); marks.append((sec,round(t,2),round(d,2),s,e)); t+=d
open(f"{OUT}/list.txt","w").write("\n".join(lst))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{OUT}/list.txt","-c","copy",f"{OUT}/roughcut.mp4"],check=True)
cur=None
for sec,t0,d,s,e in marks:
    if sec!=cur: print(f"\n{sec} @ {t0:.1f}s", end=": "); cur=sec
    print(f"[{s}-{e}]",end=" ")
print(f"\nTOTAL {t:.1f}s")
