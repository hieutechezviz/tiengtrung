# Tạo nhạc nền nhẹ nhàng (tự tổng hợp, không bản quyền) + tiếng "ting" lúc mở khoá
import numpy as np, wave
SR=44100; DUR=39.0; N=int(SR*DUR); t=np.arange(N)/SR
out=np.zeros(N)
def note(f,start,length,amp,kind='pluck'):
    s=int(start*SR); n=int(length*SR); n=min(n,N-s)
    if n<=0: return
    tt=np.arange(n)/SR
    if kind=='pluck':
        env=np.exp(-tt*5)*np.minimum(1,tt*200)
        w=np.sin(2*np.pi*f*tt)+.3*np.sin(4*np.pi*f*tt)+.1*np.sin(6*np.pi*f*tt)
    elif kind=='pad':
        env=np.minimum(1,tt/0.6)*np.minimum(1,(length-tt)/0.6)
        w=sum(np.sin(2*np.pi*f*d*tt) for d in (1,1.004,0.996))/3
    elif kind=='bass':
        env=np.exp(-tt*2.5)*np.minimum(1,tt*100)
        w=np.sin(2*np.pi*f*tt)
    elif kind=='chime':
        env=np.exp(-tt*4)*np.minimum(1,tt*400)
        w=np.sin(2*np.pi*f*tt)+.5*np.sin(2*np.pi*f*2.01*tt)
    out[s:s+n]+=amp*env*w
mid=lambda m:440*2**((m-69)/12)
BPM=100; beat=60/BPM; bar=4*beat
chords=[[60,64,67,71],[55,59,62,66],[57,60,64,67],[53,57,60,64]]  # Cmaj7 G Am F
bass=[48,43,45,41]
arp=[0,1,2,3,2,1,2,3]
b=0; tm=0.0
while tm<DUR:
    c=chords[b%4]
    note(None or mid(c[0]),tm,bar,.05,'pad'); note(mid(c[1]),tm,bar,.04,'pad'); note(mid(c[2]),tm,bar,.04,'pad')
    note(mid(bass[b%4]),tm,beat*2,.16,'bass'); note(mid(bass[b%4]),tm+beat*2,beat*2,.12,'bass')
    if tm>=1.0:
        for i,a in enumerate(arp): note(mid(c[a]+12),tm+i*beat/2,0.6,.07 if i%2==0 else .05,'pluck')
    # hi-hat nhẹ
    for i in range(8):
        s=int((tm+i*beat/2+beat/4)*SR); n=int(.05*SR)
        if s+n<N and tm>=4: out[s:s+n]+=np.random.randn(n)*np.exp(-np.arange(n)/SR*90)*.012
    tm+=bar; b+=1
for ct in [2.95]+[9.1+1.2+2*i for i in range(6)]:
    note(mid(84),ct,1.0,.12,'chime'); note(mid(91),ct+.08,1.0,.10,'chime')
for ct in [4.0,7.5,9.1,21.1,24.6,31.4,34.9]:  # whoosh chuyển cảnh
    s=int((ct-.3)*SR); n=int(.5*SR); tt=np.arange(n)/SR
    nz=np.convolve(np.random.randn(n),np.ones(30)/30,'same')
    out[s:s+n]+=nz*np.sin(np.pi*tt/.5)**2*.10
fade=np.ones(N); fi=int(.5*SR); fo=int(1.5*SR)
fade[:fi]=np.linspace(0,1,fi); fade[-fo:]=np.linspace(1,0,fo)
out*=fade; out=out/np.max(np.abs(out))*0.7
st=np.stack([out,out],1)
with wave.open('nhac_nen.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok')
