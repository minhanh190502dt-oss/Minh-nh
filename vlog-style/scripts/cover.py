import sys,os,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import refstyle as RS
src,out=sys.argv[1],sys.argv[2]
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
"""+RS.HEADER_STYLES+"""
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
E=[]
def add(l,st,tx): E.append(f"Dialogue: {l},0:00:00.00,0:00:05.00,{st},,0,0,0,,{tx}")
add(6,"Serif",r"{\blur4\an5\pos(540,1035)\fs96}lên Sài Gòn để")
add(6,"Head",r"{\blur3\an5\pos(540,1185)\fs215\fsp6}GIẢI NGỐ")
add(6,"Head",r"{\blur3\an5\pos(540,1330)\fs66\1c"+RS.PINK+r"}& BÀI HỌC EM NHẬN RA")
for l,a,b,st,tx in RS.pill(540,1460,"cuối clip bật mí em học gì","Y",0,5,fs=50):
    tx=tx.replace(RS.POPT,"")
    add(l,st,tx)
for x,y,s in [(150,1120,60),(940,1150,44),(880,1010,30),(200,1290,34),(980,1300,26),(120,980,24)]:
    add(4,"Spark",rf"{{\an5\pos({x},{y})\fs{s}}}✦")
open("/home/user/work/cover/cover.ass","w").write(hdr+"\n".join(E)+"\n")
vf=("scale=1080:1920,eq=saturation=1.08:brightness=0.02:contrast=1.03,"
    "drawbox=x=0:y=900:w=1080:h=1020:color=black@0.0:t=fill,"
    "geq=lum='lum(X,Y)*(1-0.35*clip((Y-880)/500,0,1)*clip((1700-Y)/250+1,0,1))':cb='cb(X,Y)':cr='cr(X,Y)',"
    "ass=/home/user/work/cover/cover.ass")
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vf",vf,"-frames:v","1",out],check=True)
print("ok",out)
