// Export each lecture (notes, cards, formulas, quiz) as a plain page for the NotebookLM study assistant.
// Usage: serve the repo on :8769 (python3 -m http.server 8769), then: node tools/notebook_sources.mjs
import { chromium } from 'playwright';
import fs from 'fs';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--headless=new']});
const p = await (await b.newContext({viewport:{width:1100,height:900}})).newPage();
await p.goto('http://localhost:8769/',{waitUntil:'load'}); await p.waitForTimeout(800);
const data = await p.evaluate(()=>{
  const out={};
  document.querySelectorAll('[data-issue-body]').forEach(a=>{ a.hidden=false; out['lecture'+a.dataset.issueBody]=a.innerText; });
  return out;
});
const src = fs.readFileSync('src/hub.html','utf8');
const grab=n=>{const i=src.indexOf('var '+n+'=[');let d=0,j=i+('var '+n+'=').length;for(;j<src.length;j++){if(src[j]=='[')d++;else if(src[j]==']'){d--;if(!d)break;}}return eval(src.slice(i+('var '+n+'=').length,j+1));};
const C=grab('CARDS'),Q=grab('QUIZ'),F=grab('FORMULAS'),I=grab('ISSUES');
for (const L of I){
  let t=`MBA Platform · Finance for Non-Financial Managers\nLecture ${String(L.n).padStart(2,'0')}: ${L.title}\n(Independent study companion by Mohamed Elsayed. Not an official Academy publication.)\n\n=== LECTURE NOTES ===\n\n`+data['lecture'+L.n].replace(/\n{3,}/g,'\n\n');
  t+=`\n\n=== KEY TERMS (flashcards) ===\n`;
  for(const c of C.filter(c=>c.i===L.n)) t+=`\n• ${c.t}${c.full?' ('+c.full+')':''} — ${c.tAr||''}\n  ${c.en}${c.f?'\n  Formula: '+c.f:''}\n  شرح: ${c.ar}\n`;
  t+=`\n=== FORMULAS ===\n`;
  for(const f of F.filter(f=>f.i===L.n)) t+=`• ${f.t} (${f.tAr||''}): ${f.f}. ${f.r}\n`;
  t+=`\n=== PRACTICE QUESTIONS WITH SOLUTIONS ===\n`;
  Q.filter(q=>q.i===L.n).forEach((q,k)=>{ t+=`\nQ${k+1}. ${q.s}\n`; q.o.forEach(o=>{ t+=`  - ${o[0]}${o[2]?'  ✔ correct':''}: ${o[1]}\n`;}); t+=`  Working:\n  ${q.st.replace(/\n/g,'\n  ')}\n  شرح: ${q.ar}\n`; });
  const clean=t.split('\n').map(l=>l.trim()).filter((l,i,a)=>l||a[i-1]).join('\n').trim();
  const esc=x=>x.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const body=clean.split('\n').map(l=>l?'<p>'+esc(l)+'</p>':'').join('\n');
  fs.writeFileSync(`notebook/lecture-${String(L.n).padStart(2,'0')}.html`, `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${esc(clean.split('\n')[1])} · MBA Platform study source</title></head><body>\n${body}\n</body></html>\n`);
}
await b.close();
