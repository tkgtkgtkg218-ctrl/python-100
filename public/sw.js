/* Service Worker（PWA）。下の VERSION は、ビルド時に index.html 等の内容ハッシュへ置き換わる。
 *  - アプリ本体（index.html・manifest・アイコン）: インストール時に事前キャッシュし、オフラインでも起動できる。
 *    内容が変わるとバージョンが変わるため、新しい Service Worker が入り、古いキャッシュは破棄される。
 *  - Pyodide（コード採点用の Python 実行環境）: jsDelivr からの取得を初回に自動でキャッシュし、以降はオフラインで使える。
 *  - 学習の進捗は localStorage にあり、更新しても消えない。 */
const VERSION = "0aeeb65ced";
const SHELL_CACHE = "pypath-shell-" + VERSION;
const PYODIDE_PREFIX = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
const PYODIDE_CACHE = "pypath-pyodide-v0.26.4"; // バージョン固定なので、アプリ更新では消さない
const SHELL_FILES = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png", "icons/apple-touch-icon.png", "icons/favicon.svg"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(SHELL_CACHE).then((c) => c.addAll(SHELL_FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== SHELL_CACHE && k !== PYODIDE_CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.href.startsWith(PYODIDE_PREFIX)) {
    event.respondWith(cacheFirst(req, PYODIDE_CACHE));
    return;
  }
  if (url.origin === self.location.origin) {
    // ページ移動（HTML）は、オフラインでも index.html を返す。URLの ?query は無視して照合する
    if (req.mode === "navigate") {
      event.respondWith(caches.match("index.html", { cacheName: SHELL_CACHE }).then((r) => r || fetch(req)));
      return;
    }
    event.respondWith(caches.match(req, { cacheName: SHELL_CACHE, ignoreSearch: true }).then((r) => r || fetch(req)));
  }
  // それ以外の外部リクエストには関与しない
});

async function cacheFirst(req, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  // importScripts は no-cors で取得するため opaque 応答になる。それも保存する（中身は読めなくても再利用できる）
  if (res && (res.ok || res.type === "opaque")) cache.put(req, res.clone()).catch(() => {});
  return res;
}
