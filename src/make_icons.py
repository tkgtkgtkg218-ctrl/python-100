"""PWA用アイコンを生成する（フォント不要。青い角丸の四角に、白い ">_"（ターミナルのプロンプト）を描く）。"""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "public", "icons")
BLUE = (43, 109, 224, 255)
WHITE = (255, 255, 255, 255)


def draw_icon(size, maskable=False):
    s = size * 4  # 4倍で描いて縮小（アンチエイリアス）
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        d.rectangle([0, 0, s, s], fill=BLUE)  # マスクされる前提で全面塗り
        scale = 0.56  # セーフゾーン（中央80%の円）に収める
    else:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=BLUE)
        scale = 0.68
    g = s * scale  # グリフ全体の幅
    ox = (s - g) / 2
    oy = (s - g) / 2
    w = int(g * 0.13)  # 線の太さ
    # ">" （山括弧）
    pts = [(ox + g * 0.08, oy + g * 0.18), (ox + g * 0.46, oy + g * 0.50), (ox + g * 0.08, oy + g * 0.82)]
    d.line(pts, fill=WHITE, width=w, joint="curve")
    for p in (pts[0], pts[2]):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=WHITE)
    # "_" （アンダースコア）
    y = oy + g * 0.82
    d.line([(ox + g * 0.56, y), (ox + g * 0.94, y)], fill=WHITE, width=w)
    for x in (ox + g * 0.56, ox + g * 0.94):
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=WHITE)
    return img.resize((size, size), Image.LANCZOS)


SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="113" fill="#2b6de0"/>
  <g fill="none" stroke="#fff" stroke-width="45" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="140,150 245,256 140,362"/>
    <line x1="287" y1="362" x2="372" y2="362"/>
  </g>
</svg>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    draw_icon(192).save(os.path.join(OUT, "icon-192.png"))
    draw_icon(512).save(os.path.join(OUT, "icon-512.png"))
    draw_icon(512, maskable=True).save(os.path.join(OUT, "icon-maskable-512.png"))
    # iOS はホーム画面アイコンの透過を黒く塗るため、不透明の正方形にする
    base = draw_icon(180, maskable=True)
    base.convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
    with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(SVG)
    print("icons written to", OUT)


if __name__ == "__main__":
    main()
