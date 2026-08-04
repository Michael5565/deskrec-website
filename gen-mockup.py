#!/usr/bin/env python3
"""Hand-build a clean, realistic DeskRec 'New recording' screen mockup, matching
the app's actual dark palette, rendered inside a window frame. Output PNG."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL import Image as _I
import os

# Palette (from App.css)
BG      = (11, 13, 19)
SURFACE = (19, 23, 34)
SURF2   = (26, 32, 48)
EDGE    = (42, 48, 66)
ACCENT  = (108, 92, 231)
ACCENT_HI = (143, 123, 255)
TEXT    = (238, 240, 247)
DIM     = (162, 169, 188)
FAINT   = (107, 114, 133)
DANGER  = (255, 92, 92)

W, H = 1280, 820          # mockup render size
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "home-mockup.png")

def f(sz, bold=False):
    fam = "arial.ttf" if not bold else "arialbd.ttf"
    p = f"C:/Windows/Fonts/{fam}"
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.load_default()

def rounded(img, r):
    m = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0,0,img.size[0]-1,img.size[1]-1], radius=r, fill=255)
    img.putalpha(m)
    return img

def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ------- subtle background glow -------
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-200,-150,W+200,H*0.5], fill=(108,92,231,18))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)

    # ------- window frame (a big rounded panel with a subtle chrome edge) -------
    frame_margin = 28
    frame = [frame_margin, frame_margin, W-frame_margin, H-frame_margin]
    d.rounded_rectangle(frame, radius=18, fill=(14,17,25,255), outline=EDGE, width=1)

    # window titlebar dots
    cx0, cy = frame[0]+24, frame[1]+26
    for i,(col) in enumerate([(255,95,87),(254,188,46),(39,201,63)]):
        d.ellipse([cx0+i*18, cy-6, cx0+i*18+11, cy+5], fill=col)
    d.text((frame[0]+120, cy-13), "DeskRec — New recording", font=f(14), fill=DIM)

    # header: logo + title
    lx, ly = frame[0]+52, frame[1]+70
    logo = Image.new("RGBA", (44,44), (0,0,0,0))
    ld = ImageDraw.Draw(logo)
    ld.rounded_rectangle([0,0,43,43], radius=12, fill=ACCENT)
    ld.text((13,5), "D", font=f(24, True), fill=(255,255,255))
    img.paste(logo, (lx, ly), logo)
    d.text((lx+60, ly), "New recording", font=f(24, True), fill=TEXT)
    d.text((lx+60, ly+32), "Pick a screen or window. DeskRec auto-zooms and polishes as you record.",
           font=f(14), fill=DIM)

    # ------- sources section -------
    sx, sy = frame[0]+52, ly+86
    d.text((sx, sy), "CAPTURE SOURCE", font=f(11), fill=FAINT)
    tile_y = sy + 24
    tile_w = (frame[2]-sx-16) // 2
    tile_h = 62
    tiles = [
        (True,  "Monitor 1", "1920×1080 · 60 Hz · primary"),
        (False, "Google Chrome", "1920×1020 · Window"),
    ]
    for i,(sel,name,meta) in enumerate(tiles):
        tx = sx + i*(tile_w+16)
        fillc = (ACCENT+(9,) ) if sel else (SURFACE+(255,))
        d.rounded_rectangle([tx, tile_y, tx+tile_w, tile_y+tile_h], radius=12,
                            fill=fillc, outline=(ACCENT[:3]+(200,) if sel else EDGE), width=1 if sel else 1)
        # icon chip
        d.rounded_rectangle([tx+14, tile_y+16, tx+50, tile_y+52], radius=8, fill=(ACCENT+(40,) if sel else SURF2+(255,)))
        d.text((tx+24, tile_y+18), "🖥" if name.startswith("Monitor") else "🪟", font=f(20))
        d.text((tx+64, tile_y+16), name, font=f(14,True), fill=TEXT)
        d.text((tx+64, tile_y+36), meta, font=f(12), fill=DIM)
        if sel:
            d.rounded_rectangle([tx+tile_w-88, tile_y+20, tx+tile_w-12, tile_y+42], radius=11, fill=ACCENT)
            d.text((tx+tile_w-82, tile_y+22), "Selected", font=f(11,True), fill=(255,255,255))

    # ------- options panel -------
    oy = tile_y + tile_h + 26
    d.rounded_rectangle([sx, oy, frame[2]-52, oy+118], radius=14, fill=SURFACE, outline=EDGE)
    d.text((sx+22, oy+16), "OPTIONS", font=f(11), fill=FAINT)
    # toggles (system audio on, mic on, webcam off)
    toggles = [("System audio", True, "🎧"), ("Microphone", True, "🎙"), ("Webcam (PiP)", False, "📷")]
    ty = oy + 44
    for i,(label,on,emo) in enumerate(toggles):
        txx = sx + 24 + i*170
        d.ellipse([txx, ty+4, txx+13, ty+17], fill=ACCENT if on else SURF2)
        d.ellipse([txx+((10 if on else 0)), ty+6, txx+((10 if on else 0)+9), ty+15],
                  fill=(255,255,255) if on else (FAINT))
        d.text((txx+20, ty), f"{emo} {label}", font=f(13), fill=TEXT)
    # frame rate 60 pill + record button
    d.text((sx+24, oy+84), "FRAME RATE", font=f(10), fill=FAINT)
    d.rounded_rectangle([sx+110, oy+78, sx+156, oy+100], radius=8, fill=SURF2, outline=EDGE)
    d.text((sx+121, oy+79), "60", font=f(13,True), fill=TEXT)
    # record button
    bw, bh = 200, 46
    d.rounded_rectangle([frame[2]-52-bw, oy+118-56, frame[2]-52, oy+118-10], radius=12, fill=ACCENT)
    d.ellipse([frame[2]-52-bw+24, oy+118-56+16, frame[2]-52-bw+38, oy+118-56+30], fill=(255,255,255))
    d.text((frame[2]-52-bw+56, oy+118-50), "Record", font=f(15,True), fill=(255,255,255))

    # ------- bottom hint / brand -------
    d.text((frame[1] and sx, H-64), "Auto-zoom · Cursor smoothing · Built-in editor", font=f(12), fill=FAINT)

    img.convert("RGB").save(OUT, "PNG")
    print("wrote", OUT, img.size)

if __name__ == "__main__":
    main()
