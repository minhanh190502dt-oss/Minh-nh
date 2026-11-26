import numpy as np, wave
SR=48000
def save(n,x):
    x=x/ (np.max(np.abs(x))+1e-9)*0.9
    st=np.stack([x,x],1); d=(st*32767).astype(np.int16)
    w=wave.open(f"/home/user/work/sfx/{n}.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes()); w.close()
t=lambda d: np.arange(int(SR*d))/SR
rng=np.random.default_rng(1)
# whoosh: noise through moving resonant bandpass (via FFT segments)
d=0.55; n=int(SR*d); noise=rng.standard_normal(n); out=np.zeros(n); win=2048; hop=512
for i in range(0,n-win,hop):
    frac=i/n; fc=300+3500*np.sin(np.pi*frac)**1.5; seg=noise[i:i+win]*np.hanning(win)
    F=np.fft.rfft(seg); f=np.fft.rfftfreq(win,1/SR); F*=np.exp(-((f-fc)/(fc*0.6))**2); out[i:i+win]+=np.fft.irfft(F)
env=np.sin(np.pi*np.linspace(0,1,n))**2; save("whoosh",out*env)
# pop: fast pitch drop sine
tt=t(0.09); f=900*np.exp(-tt*30)+300; ph=2*np.pi*np.cumsum(f)/SR; save("pop",np.sin(ph)*np.exp(-tt*45))
# ding: bell
tt=t(1.2); x=sum(a*np.sin(2*np.pi*fr*tt) for fr,a in [(1568,1),(3136,.4),(4704,.15),(2093,.3)]); save("ding",x*np.exp(-tt*4))
# boom: sub drop + noise burst
tt=t(1.0); f=120*np.exp(-tt*3)+40; ph=2*np.pi*np.cumsum(f)/SR; x=np.sin(ph)*np.exp(-tt*3.5)+0.3*rng.standard_normal(len(tt))*np.exp(-tt*25); save("boom",x)
# riser: rising noise+tone 1.2s
tt=t(1.2); f=200+1800*(tt/1.2)**2; x=0.5*np.sin(2*np.pi*np.cumsum(f)/SR)+0.5*rng.standard_normal(len(tt)); save("riser",x*(tt/1.2)**2)
# click/shutter
tt=t(0.12); x=rng.standard_normal(len(tt))*(np.exp(-tt*120)+0.6*np.exp(-np.maximum(tt-0.05,0)*150)*(tt>0.05)); save("shutter",x)
# sparkle: series of high blips
tt=t(0.7); x=np.zeros(len(tt))
for k,fr in enumerate([2637,3136,3520,4186,4699]):
    s=int(k*0.08*SR); seg=t(0.3); x[s:s+len(seg)]+=np.sin(2*np.pi*fr*seg)*np.exp(-seg*14)
save("sparkle",x)
# boing: wobble pitch
tt=t(0.45); f=330+120*np.sin(2*np.pi*14*tt)*np.exp(-tt*5); x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*6); save("boing",x)
# slurp: modulated bandpassed noise
d=0.6; n=int(SR*d); nz=rng.standard_normal(n); out=np.zeros(n); win=1024; hop=256
for i in range(0,n-win,hop):
    fr=i/n; fc=500+900*fr; seg=nz[i:i+win]*np.hanning(win); F=np.fft.rfft(seg); f=np.fft.rfftfreq(win,1/SR)
    F*=np.exp(-((f-fc)/180)**2); out[i:i+win]+=np.fft.irfft(F)
am=0.5+0.5*np.sign(np.sin(2*np.pi*11*np.arange(n)/SR)); save("slurp",out*am*np.sin(np.pi*np.linspace(0,1,n)))
# click (buckle/plug): two sharp clicks
x=np.zeros(int(SR*0.25))
for off in (0,0.09):
    s=int(off*SR); seg=t(0.03); x[s:s+len(seg)]+=rng.standard_normal(len(seg))*np.exp(-seg*300)+np.sin(2*np.pi*2500*seg)*np.exp(-seg*200)
save("click",x)
# zap: electric buzz
tt=t(0.35); x=np.sign(np.sin(2*np.pi*120*tt))*0.4+0.6*rng.standard_normal(len(tt)); x*=np.exp(-tt*8); save("zap",x)
# tada: bright arpeggio chord
tt=t(1.0); x=np.zeros(len(tt))
for k,fr in enumerate([523,659,784,1047]):
    s=int(k*0.06*SR); seg=t(1.0-k*0.06); x[s:s+len(seg)]+=(np.sin(2*np.pi*fr*seg)+0.3*np.sin(4*np.pi*fr*seg))*np.exp(-seg*3)
save("tada",x)
# swish: short light whoosh
d=0.25; n=int(SR*d); nz=rng.standard_normal(n); F=np.fft.rfft(nz); f=np.fft.rfftfreq(n,1/SR); F*=np.exp(-((f-2500)/1500)**2); x=np.fft.irfft(F,n)*np.sin(np.pi*np.linspace(0,1,n))**2; save("swish",x)
