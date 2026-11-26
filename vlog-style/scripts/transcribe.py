from faster_whisper import WhisperModel
import json,sys
m=WhisperModel(sys.argv[2],device="cpu",compute_type="int8",cpu_threads=4)
import wave,numpy as np
wf=wave.open(sys.argv[1]);a=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(np.float32)/32768
segs,info=m.transcribe(a,language="vi",word_timestamps=True,vad_filter=True,beam_size=5)
out=[]
for s in segs:
    out.append({"s":s.start,"e":s.end,"t":s.text.strip(),"w":[(w.start,w.end,w.word) for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}",flush=True)
json.dump(out,open(sys.argv[3],"w"),ensure_ascii=False)
