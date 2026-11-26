import json, subprocess
W="/home/user/work/final"; FPS=30
jobs=json.load(open(f"{W}/jobs.json")); files=json.load(open(f"{W}/files2.json"))
HOOK=3.7
items=[(f"{W}/hook2.mov",HOOK,True)]+[(f,j["frames"]/FPS,j["first"]) for f,j in zip(files,jobs)]
SEC_TR=["smoothleft","smoothup","smoothright","smoothdown"]
inputs=[]; fc=[]; t=0; prevv="0:v"; preva="0:a"; sc=0
for k,(f,dur,first) in enumerate(items):
    inputs+=["-i",f]
for k in range(1,len(items)):
    # transition between k-1 and k at cut time t+dur(k-1)
    t+=items[k-1][1]
    first=items[k][2]
    if first: tr=SEC_TR[sc%4]; d=0.45; sc+=1
    else: tr="fade"; d=0.3
    # trim previous audio to its length+d (cut point aligned)
    la=f"a{k}"; lv=f"v{k}"
    fc.append(f"[{k}:a]anull[ain{k}]")
    fc.append(f"[{prevv}][{k}:v]xfade=transition={tr}:duration={d}:offset={t:.4f}[{lv}]")
    prevA_len = t + d  # desired length of accumulated audio before crossfade
    fc.append(f"[{preva}]atrim=0:{prevA_len:.4f}[pa{k}]")
    fc.append(f"[pa{k}][ain{k}]acrossfade=d={d}:c1=tri:c2=tri[{la}]")
    prevv=lv; preva=la
total=t+items[-1][1]
fc.append(f"[{prevv}]trim=0:{total:.4f},setpts=PTS-STARTPTS[vout]")
fc.append(f"[{preva}]atrim=0:{total:.4f}[aout]")
open(f"{W}/xfade_graph.txt","w").write(";\n".join(fc))
subprocess.run(["ffmpeg","-v","error","-y",*inputs,"-filter_complex_script",f"{W}/xfade_graph.txt","-map","[vout]","-map","[aout]",
  "-c:v","libx264","-preset","fast","-crf","17","-pix_fmt","yuv420p","-c:a","pcm_s16le",f"{W}/base_full.mov"],check=True)
print("total",total)
