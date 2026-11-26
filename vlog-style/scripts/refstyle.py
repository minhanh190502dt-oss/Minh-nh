# Pastel "reference" style: chapter titles, pills, italic-serif accents, sparkles
from PIL import ImageFont
F={"SB":("/root/.fonts/MontSB.ttf",1.219),"XB":("/root/.fonts/MontXB.ttf",1.219),"IT":("/root/.fonts/PlayIt.ttf",1.333)}
def tw(text,font,fs,spacing=0):
    path,r=F[font]; f=ImageFont.truetype(path,max(1,int(fs/r)))
    return f.getlength(text)+spacing*len(text)
BLUE="&H00F5DCB4&"; PINK="&H00C0A7F4&"; PINKD="&H00A882EE&"; CREAM="&H00C0EBF7&"; DARK="&H00302B2B&"
CHIPC={"W":("&H00FFFFFF&",None),"Y":("&H00A0F0FF&",DARK),"B":("&H00FAE8CD&",DARK),"P":("&H00E0D3F9&",DARK)}
HEADER_STYLES = r"""Style: Cap,Mont SB,56,&H00FFFFFF,&H00FFFFFF,&H90000000,&H80000000,0,0,0,0,100,100,0,0,1,2.5,0,2,90,90,560,1
Style: Draw,Mont SB,40,&H00FFFFFF,&H00FFFFFF,&H00302B2B,&H80000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Chip,Mont SB,44,&H00302B2B,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Head,Mont XB,128,&H00F5DCB4,&H00FFFFFF,&H80000000,&H60000000,0,0,0,0,100,100,3,0,1,3,3,5,0,0,0,1
Style: Serif,Play It,84,&H00C0EBF7,&H00FFFFFF,&H80000000,&H70000000,0,0,0,0,100,100,0,0,1,3,2,5,0,0,0,1
Style: Small,Mont SB,46,&H00FFFFFF,&H00FFFFFF,&H90000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1
Style: Spark,DejaVu Sans,40,&H00C0EBF7,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
"""
def rrect(w,h,r):
    return (f"m {r} 0 l {w-r} 0 b {w} 0 {w} 0 {w} {r} l {w} {h-r} b {w} {h} {w} {h} {w-r} {h} "
            f"l {r} {h} b 0 {h} 0 {h} 0 {h-r} l 0 {r} b 0 0 0 0 {r} 0")
POPT=r"\fscx40\fscy40\t(0,140,\fscx108\fscy108)\t(140,220,\fscx100\fscy100)\fad(0,180)"
def ev(layer,a,b,style,text): return (layer,a,b,style,text)
def pill(x,y,text,kind,a,b,fs=50,layer=5):
    fill,border=CHIPC[kind]; w=int(tw(text,"SB",fs)+56); h=int(fs*1.32); r=h//2
    bord=r"\bord2.5\3c"+border if border else r"\bord0\shad3\4c&H50000000&\blur2"
    out=[ev(layer,a,b,"Draw",f"{{\\an5\\pos({x},{y})\\p1\\1c{fill}{bord}{POPT}}}{rrect(w,h,r)}"),
         ev(layer+1,a,b,"Chip",f"{{\\an5\\pos({x},{y+1})\\fs{fs}{POPT}}}{text}")]
    return out
def sparkles(pts,a,b,layer=4):
    out=[]
    for i,(x,y,s) in enumerate(pts):
        d=i*90
        out.append(ev(layer,a,b,"Spark",f"{{\\an5\\pos({x},{y})\\fs{s}\\alpha&HFF&\\t({d},{d+200},\\alpha&H00&)\\t({d+500},{d+800},\\alpha&H90&)\\t({d+900},{d+1200},\\alpha&H00&)\\fad(0,200)}}✦"))
    return out
def chapter(a,b,num,small,title,sub=None,y=420):
    out=[]
    # line 1: badge + italic word
    sw=tw(small,"IT",84); bw=100; gap=16; total=bw+gap+sw; x0=540-total/2
    bx=x0+bw/2; sx=x0+bw+gap+sw/2; y1=y-125
    out.append(ev(5,a,b,"Draw",f"{{\\an5\\pos({bx:.0f},{y1})\\p1\\1c{PINK}\\bord0{POPT}}}{rrect(bw,76,18)}"))
    out.append(ev(6,a,b,"Chip",f"{{\\an5\\pos({bx:.0f},{y1+1})\\fnMont XB\\fs52\\1c&H00FFFFFF&{POPT}}}{num}"))
    out.append(ev(6,a,b,"Serif",f"{{\\an5\\pos({sx:.0f},{y1-4})\\fad(150,180)\\move({sx:.0f},{y1+16},{sx:.0f},{y1-4},0,250)}}{small}"))
    fs=128 if len(title)<=12 else int(128*12/len(title))
    out.append(ev(6,a+0.08,b,"Head",f"{{\\an5\\pos(540,{y})\\fs{fs}{POPT}}}{title}"))
    if sub: out.append(ev(6,a+0.25,b,"Head",f"{{\\an5\\pos(540,{y+108})\\fs66\\1c{PINK}\\fad(200,180)\\move(540,{y+128},540,{y+108},0,250)}}{sub}"))
    tw_=tw(title,"XB",fs,3)/2
    out+=sparkles([(540-tw_-40,y-40,34),(540+tw_+36,y+10,26),(540+tw_+10,y-120,22),(540-tw_+20,y+60,20)],a,b)
    return out
def serif_big(a,b,small,big,y=440,col=CREAM,fs=150):
    out=[]
    if small: out.append(ev(6,a,b,"Small",f"{{\\an5\\pos(540,{y-95})\\fad(150,180)\\move(540,{y-75},540,{y-95},0,220)}}{small}"))
    out.append(ev(6,a+0.1,b,"Serif",f"{{\\an5\\pos(540,{y})\\fs{fs}\\1c{col}{POPT}}}{big}"))
    w=tw(big,"IT",fs)/2
    out+=sparkles([(540-w-36,y-30,30),(540+w+34,y+20,24)],a,b)
    return out
def hook(OFF):
    out=[]
    out.append(ev(6,0.08,OFF,"Head",f"{{\\an5\\pos(540,1000)\\fs225\\fsp6{POPT}}}BYE BYE"))
    out.append(ev(6,0.55,OFF,"Serif",f"{{\\an5\\pos(560,1160)\\fs150\\alpha&HFF&\\t(0,300,\\alpha&H00&)\\move(560,1200,560,1160,0,300)\\fad(0,180)}}em đi đây"))
    out+=sparkles([(130,910,44),(960,940,34),(900,1100,26),(170,1140,28),(560,850,22)],0.1,OFF)
    return out
