// Render clean review screenshots (teal stars + review text, white, Inter, 1370px wide) in the style of
// Dropbox "[01] Clients/The Tallowed Truth/Testimonial Text". Usage:
//   NODE_PATH=$(npm root -g) node tools/review_cards.js <reviews.json> <out_dir>
// reviews.json: [{"file": "Name - Hook.png", "rating": 5, "text": "verbatim review"}]
const {chromium}=require('playwright');const fs=require('fs');
const [,,json,outdir]=process.argv;const items=JSON.parse(fs.readFileSync(json,'utf8'));
const star='<svg viewBox="0 0 24 24" width="27" height="27"><path fill="#3c8274" d="M12 2.2l2.95 6.3 6.85.8-5.08 4.68 1.37 6.77L12 17.4l-6.09 3.35 1.37-6.77L2.2 9.3l6.85-.8z" stroke="#3c8274" stroke-width="1.2" stroke-linejoin="round"/></svg>';
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:685,height:400},deviceScaleFactor:2});
for(const it of items){
 const html=`<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=block" rel="stylesheet"><style>
 html,body{margin:0;background:#fff}#c{padding:18px 30px 26px 20px;width:635px;font-family:Inter,sans-serif;font-size:16.5px;line-height:1.62;color:#333}
 .s{display:flex;gap:4px;margin:0 0 22px}.t{margin:0}</style></head><body><div id="c"><div class="s">${star.repeat(it.rating)}</div><p class="t">${esc(it.text)}</p></div></body></html>`;
 await p.setContent(html,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
 const ok=await p.evaluate(()=>document.fonts.check('16px Inter'));
 await (await p.$('#c')).screenshot({path:outdir+'/'+it.file});console.log(it.file,'inter',ok);}
await b.close();})();
