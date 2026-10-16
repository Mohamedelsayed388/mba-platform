from PIL import Image, ImageDraw
NAVY=(15,36,64); BRASS=(214,160,64); WHITE=(238,243,249)
def make(size, maskable=False, out=None):
    S=size*4
    im=Image.new('RGBA',(S,S),NAVY+(255,) if maskable else (0,0,0,0))
    d=ImageDraw.Draw(im)
    if not maskable:
        d.rounded_rectangle([0,0,S-1,S-1],radius=int(S*0.22),fill=NAVY)
    # content box (safe zone)
    pad = 0.24 if maskable else 0.17
    x0=S*pad; w=S*(1-2*pad)
    u=w/24.0
    def X(v): return x0+v*u
    def Y(v): return x0+v*u
    # outline frame (non maskable only)
    if not maskable:
        d.rounded_rectangle([X(-1.2),Y(-1.2),X(25.2),Y(25.2)],radius=int(u*4.5),outline=BRASS,width=max(2,int(u*0.9)))
    bw=4.2
    bars=[(2.5,15,WHITE),(10,10,WHITE),(17.5,4.5,BRASS)]
    for bx,top,col in bars:
        d.rounded_rectangle([X(bx),Y(top),X(bx+bw),Y(22)],radius=int(u*0.8),fill=col)
    pts=[(X(4.6),Y(11)),(X(12.1),Y(6)),(X(19.6),Y(1.2))]
    d.line(pts,fill=BRASS,width=max(2,int(u*1.1)))
    for p in pts[:2]:
        r=u*1.5; d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],fill=BRASS)
    im=im.resize((size,size),Image.LANCZOS)
    if out.endswith('apple-touch-icon.png'):
        bg=Image.new('RGB',(size,size),NAVY); bg.paste(im,(0,0),im); im=bg
    im.save(out)
make(192,out='icon-192.png'); make(512,out='icon-512.png')
make(512,maskable=True,out='icon-maskable-512.png')
make(180,maskable=True,out='apple-touch-icon.png')
make(48,out='favicon.png')
