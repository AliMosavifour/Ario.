/* Ario service worker: offline-first shell, always-fresh version.json, APK never cached */
const V='ario-v6',CORE=['./','index.html','privacy.html','manifest.webmanifest','assets/icon.webp','assets/icon-192.png','assets/icon-512.png','assets/favicon.png','assets/qr.js','app/fonts/Vazirmatn.woff2','assets/shots/d-account.webp','assets/shots/d-kk.webp','assets/shots/d-stats.webp','assets/shots/d-today.webp','assets/shots/d-week.webp','assets/shots/l-account.webp','assets/shots/l-kk.webp','assets/shots/l-stats.webp','assets/shots/l-today.webp','assets/shots/l-week.webp','assets/chars/bg-black-bunny.webp','assets/chars/bg-cow.webp','assets/chars/bg-masked.webp','assets/chars/bg-pink-bear.webp','assets/chars/black-bunny-b.webp','assets/chars/black-bunny-f.webp','assets/chars/cow-b.webp','assets/chars/cow-f.webp','assets/chars/masked-b.webp','assets/chars/masked-f.webp','assets/chars/pink-bear-b.webp','assets/chars/pink-bear-f.webp'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>Promise.all(CORE.map(u=>c.add(u).catch(()=>{})))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET'||u.origin!==location.origin||u.pathname.endsWith('.apk')||r.headers.has('range'))return;
  if((u.pathname.endsWith('version.json')||u.pathname.endsWith('changelog.json'))){
    e.respondWith(fetch(r).then(x=>{const c=x.clone();caches.open(V).then(h=>h.put(r,c));return x}).catch(()=>caches.match(r)));return;
  }
  /* stale-while-revalidate: instant from cache, refreshed in background */
  e.respondWith(caches.open(V).then(async c=>{
    const hit=await c.match(r,{ignoreSearch:true});
    const net=fetch(r).then(x=>{if(x&&x.ok)c.put(r,x.clone());return x}).catch(()=>null);
    if(hit){e.waitUntil(net);return hit}
    const x=await net;
    return x||(r.mode==='navigate'?c.match('index.html'):Response.error());
  }));
});
