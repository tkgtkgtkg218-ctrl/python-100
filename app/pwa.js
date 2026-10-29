/* PWA: Service Worker の登録、インストール案内、更新の通知（https または localhost でのみ有効） */
(function () {
  "use strict";
  const pwa = (window.__pwa = {
    installEvent: null,
    standalone: (window.matchMedia && matchMedia("(display-mode: standalone)").matches) || navigator.standalone === true,
  });
  const notify = () => window.dispatchEvent(new Event("pwa-installable"));
  window.addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); pwa.installEvent = e; notify(); });
  window.addEventListener("appinstalled", () => { pwa.installEvent = null; pwa.standalone = true; notify(); });

  if (!("serviceWorker" in navigator) || !/^https?:$/.test(location.protocol)) return; // file:// などでは登録しない
  const hadController = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    // 初回インストール（それまで管理するSWがなかった）では通知しない。更新時のみ「更新する」を出す
    if (!hadController) return;
    const b = document.getElementById("update-banner");
    if (b) b.hidden = false;
  });
  const reload = document.getElementById("update-reload");
  if (reload) reload.addEventListener("click", () => location.reload());
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js").catch((e) => console.warn("Service Worker の登録に失敗しました", e));
  });
})();
