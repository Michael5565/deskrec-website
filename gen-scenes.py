#!/usr/bin/env python3
"""Generate a set of styled dark-UI 'app scene' images for the DeskRec website,
all consistent with the Home mockup palette. Each is a mini app-window showing a
concept scene. Writes PNGs to img/."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

BG=(11,13,19); SURFACE=(19,23,34); SURF2=(26,32,48); EDGE=(42,48,66)
ACCENT=(108,92,231); ACCENT_HI=(143,123,255); TEXT=(238,240,247)
DIM=(162,169,188); FAINT=(107,114,133); DANGER=(255,92,92); OK=(53,196,107)

DEF_W_DEF_H = (960, 600)   # 16:10

def font(sz,bold=False):
    p=f"C:/Windows/Fonts/{'arialbd.ttf' if bold else 'arial.ttf'}"
    return ImageFont.truetype(p,sz) if os.path.exists(p) else ImageFont.load_default()

def scene_window(base, d, w, h, title):
    """Draw a window-frame top bar on an existing image."""
    # subtle bg
    glow=Image.new("RGBA",(w,h),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse([-80,-60,w+80,h*0.45],fill=(ACCENT+(16,)))
    base=Image.alpha_composite(base,glow); d=ImageDraw.Draw(base)
    # window frame
    d.rounded_rectangle([0,0,w-1,h-1],radius=14,fill=(14,17,25,255),outline=EDGE,width=1)
    x0,y0=18,18
    for i,c in enumerate([(255,95,87),(254,188,46),(39,201,63)]):
        d.ellipse([x0+i*16,y0,x0+i*16+10,y0+10],fill=c)
    d.text((x0+62,y0-2),title,font=font(13),fill=DIM)
    return base,d

def mini_tile(d,x,y,w,h,label,sub,sel=False):
    d.rounded_rectangle([x,y,x+w,y+h],radius=10,
        fill=(ACCENT+(10,)) if sel else (SURFACE+(255,)),
        outline=(ACCENT[:3]+(200,) if sel else EDGE),width=1)
    d.rounded_rectangle([x+10,y+8,x+34,y+32],radius=6,
        fill=(ACCENT+(45,) if sel else SURF2+(255,)))
    d.text((x+16,y+9),"■",font=font(14),fill=(255,255,255) if sel else DIM)
    d.text((x+42,y+9),label,font=font(12,True),fill=TEXT)
    d.text((x+42,y+26),sub,font=font(9),fill=DIM)

def render(name, w, h, draw_fn, title):
    base=Image.new("RGBA",(w,h),BG)
    d=ImageDraw.Draw(base)
    base,d=scene_window(base,d,w,h,title)
    draw_fn(w,h,d)
    base.convert("RGB").save(f"img/{name}.png","PNG")
    print("  wrote img/"+name+".png")

def inner(w,h,d):
    """Return content area rect."""
    return (18,18+22, w-18, h-18)

# ---------------- Showcase (16:9) ----------------
def scene_demo(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=14
    # two panels: big preview + small clips
    d.text((x0,y0),"Feature demos",font=font(15,True),fill=TEXT)
    d.text((x0,y0+22),"Auto-zoom keeps the action centered as you narrate.",font=font(11),fill=DIM)
    d.rounded_rectangle([x0,y0+44,x1-30,y1-14],radius=12,fill=SURFACE2_ish(),outline=EDGE)
    # a "zoomed" center box simulating the auto-zoom
    zx,zys,zw,zh = x0+70,y0+84,220,150
    d.rounded_rectangle([zx,zys,zx+zw,zys+zh],radius=8,fill=SURF2,outline=ACCENT,width=2)
    d.text((zx+zw//2-80,zys+zh//2-10),"cursor here",font=font(12),fill=DIM)
    # accent dot for clicked zoom target
    d.ellipse([zx+zw//2-4,zys+zh//2-4,zx+zw//2+4,zys+zh//2+4],fill=ACCENT_HI)
    mini_tile(d,x1-190,y0+50,160,30,"Clip 1","example",False)
    mini_tile(d,x1-190,y0+88,160,30,"Clip 2","example",False)
    d.text((x0,zys+zh+22),"● 00:24",font=font(11,True),fill=DANGER)

def SURFACE2_ish(): return (SURFACE+(255,))
def selected_p(): return False

def scene_bug(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=14
    d.text((x0,y0),"Bug report",font=font(15,True),fill=TEXT)
    d.text((x0,y0+22),"Record the exact steps to paste into your tracker.",font=font(11),fill=DIM)
    # code-ish panel
    d.rounded_rectangle([x0,y0+44,x1-20,y1-14],radius=12,fill=(11,14,22,255),outline=EDGE)
    for i in range(6):
        d.text((x0+20,(y0+60)+i*22),("def "+" "*i)+"handle_click  ...",font=font(11),fill=(DIM if i%2==0 else TEXT))
    d.text((x0+20,y1-44),"← reproduced · steps 1-3",font=font(10),fill=OK)

def scene_tutorial(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=14
    d.text((x0,y0),"Tutorial",font=font(15,True),fill=TEXT)
    d.text((x0,y0+22),"Clean frames with a webcam bubble.",font=font(11),fill=DIM)
    d.rounded_rectangle([x0,y0+44,x1-20,y1-14],radius=12,fill=SURFACE,outline=EDGE)
    d.rounded_rectangle([x0+160,y0+70,x1-200,y1-70],radius=10,fill=SURF2,outline=EDGE,width=2)
    d.text((x0+220,y1//2-6),"✓ distraction-free frame",font=font(11),fill=DIM)
    # webcam bubble corner
    d.rounded_rectangle([x1-120,y0+58,x1-40,y0+128],radius=8,fill=SURF2,outline=ACCENT)
    d.text((x1-100,y0+86),"cam",font=font(10),fill=DIM)

# ---------------- Features (16:10) ----------------
def feature_bg(w,h,d,x0,y0,x1,y1):
    d.text((x0,y0),"Auto-zoom",font=font(16,True),fill=TEXT)
    d.rounded_rectangle([x0,y0+34,x1-20,y1],radius=12,fill=SURFACE,outline=EDGE)

def scene_zoom(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=10
    feature_bg(w,h,d,x0,y0,x1,y1)
    d.rounded_rectangle([x0+60,y0+60,x1-140,y1-30],radius=10,fill=SURF2,outline=ACCENT,width=2)
    d.text((x0+150,y1//2),"Zooms to the click",font=font(12),fill=DIM)

def scene_cursor(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=10
    feature_bg(w,h,d,x0,y0,x1,y1)
    # marker line
    for i in range(8):
        d.line([x0+80+i*12,y0+80,x0+80+i*12,y1-40],fill=(ACCENT_HI+(120,)),width=2)
    d.ellipse([x0+120,y0+110,x0+132,y0+122],fill=DANGER)
    d.text((x0+140,y0+106),"Cursor smoothing + markers",font=font(12),fill=DIM)

def scene_sources(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=10
    feature_bg(w,h,d,x0,y0,x1,y1)
    mini_tile(d,x0+30,y0+54,340,44,"🖥 Monitor 1","1920×1080 · 60 Hz",True)
    mini_tile(d,x0+30,y0+106,340,40,"Chrome window","1920×1020")
    d.text((x0+410,y0+70),"Or draw a custom region",font=font(11),fill=DIM)

def scene_audio(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=10
    feature_bg(w,h,d,x0,y0,x1,y1)
    items=[("System audio","ON",True),("Microphone","ON",True),("Webcam (PiP)","OFF",False)]
    yy=y0+54
    for name,st,on in items:
        d.rounded_rectangle([x0+30,yy,x0+360,yy+36],radius=8,fill=SURF2,outline=EDGE)
        d.ellipse([x0+44,yy+12,x0+54,yy+22],fill=ACCENT if on else SURF2)
        d.ellipse([x0+46 if on else x0+40,yy+14,x0+52 if on else x0+46,yy+20],fill=(255,255,255) if on else FAINT)
        d.text((x0+66,yy+11),name,font=font(12),fill=TEXT)
        d.text((x0+250,yy+11),st,font=font(10,True),fill=(OK if on else FAINT))
        yy+=44

def scene_editor(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=10
    feature_bg(w,h,d,x0,y0,x1,y1)
    # timeline bar
    d.rounded_rectangle([x0+30,y1-60,x1-30,y1-18],radius=8,fill=SURF2,outline=EDGE)
    d.line([x0+40,y1-40,x1-40,y1-40],fill=ACCENT_HI,width=3)
    d.ellipse([x0+180,y1-44,x0+192,y1-32],fill=ACCENT)
    d.text((x0+40,y0+54),"Built-in editor · trim & export",font=font(12),fill=DIM)

def scene_speed(w,h,d):
    x0,y0,x1,y1=inner(w,h,d); y0+=10
    feature_bg(w,h,d,x0,y0,x1,y1)
    for i in range(3):
        d.rounded_rectangle([x0+30+i*130,y0+70,x0+30+i*130+110,y0+110],radius=8,fill=SURF2,outline=EDGE)
    d.text((x0+30,y0+120),"Distraction-free · countdown · full-res preview",font=font(11),fill=DIM)

scenes = {
  # showcase (16:9 -> 960x540)
  "showcase-demo":    (960,540,scene_demo,"Feature demos"),
  "showcase-bug":     (960,540,scene_bug,"Bug reports"),
  "showcase-tutorial":(960,540,scene_tutorial,"Tutorials"),
  # features (16:10 -> 960x600)
  "feature-zoom":     (960,600,scene_zoom,"Auto-zoom"),
  "feature-cursor":   (960,600,scene_cursor,"Cursor & annotations"),
  "feature-sources":  (960,600,scene_sources,"Capture sources"),
  "feature-audio":    (960,600,scene_audio,"Audio & webcam"),
  "feature-editor":   (960,600,scene_editor,"Built-in editor"),
  "feature-speed":    (960,600,scene_speed,"Power user"),
}
def main():
    for name,(w,h,fn,title) in scenes.items():
        render(name,w,h,fn,title)
    print("done")
if __name__=="__main__":
    main()
