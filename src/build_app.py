"""3つのJSONと app/ の CSS・JS から、次の2つを作る。
  - app/index.html : ダブルクリックで開ける単一HTML（PWA機能なし）
  - public/        : PWA 一式（GitHub に置いて Vercel などの静的ホスティングで公開する）
                     index.html / manifest.webmanifest / sw.js / icons/*
"""
import hashlib
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APP = os.path.join(ROOT, "app")
PUBLIC = os.path.join(ROOT, "public")

PWA_HEAD = """<meta name="description" content="短い教科書を読んで、すぐ問題を解く。Python 初心者向けの10ステージ・全100問。">
<meta name="theme-color" content="#2b6de0">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Python100問">
<meta name="apple-mobile-web-app-status-bar-style" content="default">"""


def read(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def render_html(pwa):
    data = {n: json.load(open(os.path.join(ROOT, n + ".json"), encoding="utf-8")) for n in ["curriculum", "lessons", "questions"]}
    # </script> で早期終了しないよう "</" をエスケープ（JSONとしては同値）
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = read(APP, "template.html")
    html = html.replace("<!--PWA_HEAD-->", PWA_HEAD if pwa else "")
    html = html.replace("/*STYLE*/", read(APP, "style.css"))
    html = html.replace("/*PYWORKER*/", read(APP, "pyworker.js"))
    html = html.replace("/*GRADER*/", read(APP, "grader.js"))
    html = html.replace("/*PYRUNNER*/", read(APP, "pyrunner.js"))
    html = html.replace("/*PWA*/", read(APP, "pwa.js") if pwa else "")
    html = html.replace("/*APP*/", read(APP, "app.js"))
    html = html.replace("/*DATA*/", payload)
    return html


def main():
    # 1) 単一HTML
    out = os.path.join(APP, "index.html")
    write(out, render_html(pwa=False))
    print("wrote", out, "%d KB" % (os.path.getsize(out) // 1024))

    # 2) PWA（public/）
    html = render_html(pwa=True)
    write(os.path.join(PUBLIC, "index.html"), html)
    shutil.copyfile(os.path.join(APP, "manifest.webmanifest"), os.path.join(PUBLIC, "manifest.webmanifest"))
    # キャッシュのバージョン = アプリ本体・manifest・Service Worker・アイコンの内容ハッシュ
    h = hashlib.sha256()
    h.update(html.encode("utf-8"))
    h.update(read(APP, "manifest.webmanifest").encode("utf-8"))
    h.update(read(APP, "sw.js").encode("utf-8"))
    icons = os.path.join(PUBLIC, "icons")
    for name in sorted(os.listdir(icons)):
        h.update(open(os.path.join(icons, name), "rb").read())
    version = h.hexdigest()[:10]
    write(os.path.join(PUBLIC, "sw.js"), read(APP, "sw.js").replace("__VERSION__", version))
    print("wrote public/ (cache version %s, index.html %d KB)" % (version, os.path.getsize(os.path.join(PUBLIC, "index.html")) // 1024))


if __name__ == "__main__":
    main()
