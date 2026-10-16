"""Build index.html (installable app) from src/hub.html.
Usage: python3 tools/build.py src/hub.html index.html
"""
import re,sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src).read()
s=s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
s=re.sub(r'<title>.*?</title>\n?','',s,count=1)
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>MBA Platform</title>
<meta name="description" content="MBA Platform by Mohamed Elsayed: AI-built study companion for Finance for Non-Financial Managers, with lecture issues, bilingual flashcards, a scenario quiz and a formula sheet.">
<meta name="theme-color" content="#0f2440">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="MBA Platform">
<meta property="og:title" content="MBA Platform">
<meta property="og:description" content="Lecture issues, flashcards, a scenario quiz and a formula sheet for Finance for Non-Financial Managers.">
<meta property="og:image" content="icon-512.png">
'''
extra_css='''
<style>
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0}img{max-width:100%}[hidden]{display:none!important}
body::before{background:var(--mast)}
.install{display:inline-flex;align-items:center;gap:8px}
.install svg{width:16px;height:16px}
.sheet{position:fixed;inset:0;z-index:50;background:rgba(5,12,22,.55);display:flex;align-items:flex-end;justify-content:center;padding:16px;padding-bottom:max(16px,env(safe-area-inset-bottom,0px))}
.sheet .card{background:var(--surface);color:var(--ink);border-radius:16px;max-width:460px;width:100%;padding:22px;display:flex;flex-direction:column;gap:14px;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.sheet h3{font-family:var(--f-brand);font-stretch:105%;font-size:21px;font-weight:700}
.sheet ol{margin:0;padding-right:20px;display:flex;flex-direction:column;gap:8px}
.sheet .approw{display:flex;gap:12px;align-items:center}
.sheet .approw img{width:52px;height:52px;border-radius:12px}
.sheet .approw b{font-family:var(--f-brand);font-size:17px;display:block}
@media (display-mode: standalone){.install{display:none!important}}
</style>
</head>
<body>
'''
i=s.index('</style>')+len('</style>')
s=head+s[:i]+extra_css+s[i:]
# install button in byline area
s=s.replace('<div class="byline"><span>Curated by','<div><button class="btn brass install" id="install-btn" type="button"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1v9m0 0l-3.5-3.5M8 10l3.5-3.5M2 12v2h12v-2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Install the app</button></div>\n      <div class="byline"><span>Curated by',1)
sheet='''
<div class="sheet" id="sheet" hidden role="dialog" aria-modal="true" aria-labelledby="sheet-title">
  <div class="card">
    <div class="approw"><img src="icon-192.png" alt=""><div><b>MBA Platform</b><span class="note">Opens full screen and works offline</span></div></div>
    <h3 id="sheet-title" class="ar">ثبّت التطبيق على موبايلك</h3>
    <div id="sheet-ios" class="ar" hidden><ol><li>افتح اللينك من <b>Safari</b>.</li><li>دوس على زرار المشاركة (المربع اللي طالع منه سهم) تحت الشاشة.</li><li>اختار <b>Add to Home Screen</b>، وبعدين <b>Add</b>.</li></ol></div>
    <div id="sheet-other" class="ar" hidden><ol><li>افتح اللينك من <b>Chrome</b>.</li><li>دوس على النقط التلاتة فوق على اليمين.</li><li>اختار <b>Install app</b> أو <b>Add to Home screen</b>.</li></ol></div>
    <button class="btn primary" id="sheet-close" type="button">Got it</button>
  </div>
</div>
<script>
(function(){
  var deferred=null, btn=document.getElementById('install-btn'), sheet=document.getElementById('sheet');
  var standalone=window.matchMedia('(display-mode: standalone)').matches||window.navigator.standalone===true;
  if(standalone&&btn)btn.hidden=true;
  window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();deferred=e;});
  window.addEventListener('appinstalled',function(){if(btn)btn.hidden=true;sheet.hidden=true;});
  var ios=/iphone|ipad|ipod/i.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  if(btn)btn.addEventListener('click',function(){
    if(deferred){deferred.prompt();deferred.userChoice.then(function(){deferred=null;});return;}
    document.getElementById('sheet-ios').hidden=!ios;
    document.getElementById('sheet-other').hidden=ios;
    sheet.hidden=false;
  });
  document.getElementById('sheet-close').addEventListener('click',function(){sheet.hidden=true;});
  sheet.addEventListener('click',function(e){if(e.target===sheet)sheet.hidden=true;});
  if('serviceWorker' in navigator){window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});}
})();
</script>
'''
s=s+sheet+'</body>\n</html>\n'
open(dst,'w').write(s)
