from faster_whisper import WhisperModel
import sys,wave,json,numpy as np
m=WhisperModel("large-v3",device="cpu",compute_type="int8",cpu_threads=4)
wf=wave.open(sys.argv[1]);a=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(np.float32)/32768
P="Vlog đi Sài Gòn. Hello mọi người, giải ngố, cuối clip bật mí, mái ngố, Hiền Hồ, cắt tóc, bà chị, mắc cỡ, bằng lái, tài xế, trạm dừng chân Đồng Tháp, não cá vàng, xe khách, Haidilao, tài trợ, đồng nghiệp cũ, tư vấn viên, thẩm mỹ viện, livestream, thói quen, cày tiếp, clip sau."
segs,_=m.transcribe(a,language="vi",beam_size=5,word_timestamps=True,vad_filter=True,initial_prompt=P,condition_on_previous_text=False)
W=[]
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text.strip()}",flush=True)
    W.append({"s":s.start,"e":s.end,"t":s.text.strip(),"w":[(w.start,w.end,w.word) for w in s.words]})
json.dump(W,open(sys.argv[2],"w"),ensure_ascii=False)
