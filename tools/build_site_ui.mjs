// Post-process generated SEO pages without new dependencies. Run after build_seo_pages.py.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const write=(p,s)=>fs.writeFileSync(path.join(root,p),s);
const idx=read('index.html');
const re=()=>/<(p|dt|dd|span|b|h3|h2|h1|a)\b((?:"[^"]*"|'[^']*'|[^'">])*)>([\s\S]*?)<\/\1>/g;
const decode=s=>s.replaceAll('&amp;','&').replaceAll('&quot;','"');
const attr=s=>s.replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
const dictionary=new Map();
const add=(tw,cn,en)=>dictionary.set(tw,[cn,tw,en]);
for(const row of [
 ['品牌緣起','品牌缘起','Our story'],['玉雕文化','玉雕文化','Jade carving culture'],['楊樹明老師','杨树明老师','Master Yang Shuming'],['南詔團隊','南诏团队','Our team'],['作品展示','作品展示','Our works'],['門店','门店','Stores'],['聯繫我們','联系我们','Contact'],['首頁','首页','Home'],['跳至正文','跳至正文','Skip to content'],
 ['聯繫南詔工匠','联系南诏工匠','Contact Nanzhao Arts'],['定製雕刻、作品欣賞或到店諮詢，請透過下方渠道聯繫我們。','定制雕刻、作品欣赏或到店咨询，请通过下方渠道联系我们。','For custom carving, viewing works or planning a visit, contact us using the channels below.'],
 ['品牌聯繫','品牌联系','Brand enquiries'],['電子郵件','电子邮件','Email'],['團隊成員個人聯繫','团队成员个人联系','Contact a team member'],['WhatsApp 聯繫','WhatsApp 联系','Chat on WhatsApp'],
 ['張偉','张伟','Zhang Wei'],['張圓','张圆','Zhang Yuan'],['張清雪','张清雪','Zhang Qingxue'],['文強','文强','Wen Qiang'],
 ['「南詔工匠」珠寶品牌創始人','「南诏工匠」珠宝品牌创始人','Founder, Nanzhao Arts Jewelry'],['「南詔工匠」董事長','「南诏工匠」董事长','Chairman, Nanzhao Arts'],['「南詔工匠」品牌店店長','「南诏工匠」品牌店店长','Store Manager, Nanzhao Arts Brand Store'],['「南詔工匠」供應鏈負責人','「南诏工匠」供应链负责人','Head of Supply Chain, Nanzhao Arts'],
 ['門店與工作室','门店与工作室','Stores and studios'],['門店與工作室｜騰衝、瑞麗、香港','门店与工作室｜腾冲、瑞丽、香港','Stores and studios | Tengchong, Ruili, Hong Kong'],
 ['南詔工匠在騰衝、瑞麗與香港設有門店與工作室。如需到店看料、賞玉，歡迎先透過聯繫頁與我們溝通。','南诏工匠在腾冲、瑞丽与香港设有门店与工作室。如需到店看料、赏玉，欢迎先通过联系页与我们沟通。','Nanzhao Arts has stores and studios in Tengchong, Ruili and Hong Kong. Please contact us before visiting to view stones or jade.'],
 ['騰衝','腾冲','Tengchong'],['瑞麗','瑞丽','Ruili'],['香港','香港','Hong Kong'],['總部 · 騰衝市百寶街樹明玉雕3樓','总部 · 腾冲市百宝街树明玉雕3楼','Headquarters · 3F Shuming Jade Carving, Baibao Street, Tengchong'],['瑞麗多寶之城35棟','瑞丽多宝之城35栋','Building 35, Duobao City, Ruili'],
 ['香港旺角花園街2-16號好景商業中心23樓2304室','香港旺角花园街2-16号好景商业中心23楼2304室','Flat 2304, 23/F, Ho King Commercial Centre, 2–16 Fa Yuen Street, Mong Kok, Hong Kong'],
 ['2025年10月15日，「南詔工匠·楊樹明大師工作站」在瑞麗啟動。','2025年10月15日，「南诏工匠·杨树明大师工作站」在瑞丽启动。','The Nanzhao Arts · Yang Shuming Master Workstation opened in Ruili on 15 October 2025.'],
 ['高德地圖','高德地图','Amap'],['Google 地圖','Google 地图','Google Maps'],['Apple 地圖','Apple 地图','Apple Maps'],['認識南詔團隊','认识南诏团队','Meet our team'],['諮詢大師定製','咨询大师定制','Ask about a master commission'],
 ['楊樹明老師｜騰衝翡翠玉雕','杨树明老师｜腾冲翡翠玉雕','Master Yang Shuming | Jade carving in Tengchong'],
 ['© 2026 南詔工匠 · 騰衝南詔珠寶有限公司 · nanzhaoarts.com · 品牌展示網站，不提供線上交易','© 2026 南诏工匠 · 腾冲南诏珠宝有限公司 · nanzhaoarts.com · 品牌展示网站，不提供在线交易','© 2026 Nanzhao Arts · Tengchong Nanzhao Jewelry Co., Ltd. · nanzhaoarts.com · Brand showcase site; no online sales.'],
 ['門店地址與地圖導航請見<a href="/stores">門店頁</a>；團隊介紹請見<a href="/team">南詔團隊</a>。本站為品牌展示網站，不提供線上交易。','门店地址与地图导航请见<a href="/stores">门店页</a>；团队介绍请见<a href="/team">南诏团队</a>。本站为品牌展示网站，不提供在线交易。','For addresses and directions, see <a href="/stores">stores</a>; meet <a href="/team">our team</a>. This is a brand showcase website; no online sales.']
]) add(...row);
// Preserve the already published English biography and every existing fact verbatim.
const source=[...idx.match(/<section id="founder"[\s\S]*?<\/section>/)[0].matchAll(re())];
const master=read('master.html');
const target=[...master.match(/<section[^>]*id="founder-bio"[\s\S]*?<\/section>/)[0].matchAll(re())];
if(source.length!==target.length) throw Error('Biography structure changed; review translation alignment.');
for(let i=0;i<source.length-2;i++){
 const s=source[i],t=target[i];
 if(s[1]!==t[1]&&!(s[1]==='h2'&&t[1]==='h1'))throw Error('Biography tag mismatch');
 const en=s[2].match(/data-en="([^"]*)"/)?.[1];
 if(en&&s[1]!=='h2')add(decode(t[3]),decode(s[3]),decode(en));
}
const inject=s=>{
 s=s.replace('data-en="Worried " master="" work"="" is="" just="" a="" label?"=""','data-en="Worried &quot;master work&quot; is just a label?"');
 if(!s.includes('href="/site-ui.css'))s=s.replace('</head>','<link rel="stylesheet" href="/site-ui.css?v=20261110"></head>');
 if(!s.includes('src="/site-ui.js'))s=s.replace('</body>','<script src="/site-ui.js?v=20261110" defer></script></body>');
 return s;
};
for(const p of ['master.html','stores.html','contact.html']){
 let s=read(p).replace(/\sdata-ui-(?:cn|tw|en)="[^"]*"/g,'');
 const decorate=text=>text.replace(re(),(all,tag,attrs,html)=>{
  const row=dictionary.get(decode(html));
  return row?`<${tag}${attrs} data-ui-cn="${attr(row[0])}" data-ui-tw="${attr(row[1])}" data-ui-en="${attr(row[2])}">${html}</${tag}>`:`<${tag}${attrs}>${decorate(html)}</${tag}>`;
 });
 s=decorate(s);
 // Keep the same shared visual stylesheet as the homepage.
 s=s.replace(/\/round2\/design.css\?[^" ]+/g,idx.match(/\/round2\/design.css\?[^" ]+/)[0]);
 if(!s.includes('class="lang"'))s=s.replace('<button class="burger"','<div class="lang" aria-label="Language"><button type="button" data-l="zh-TW">繁中</button><button type="button" data-l="zh-CN">简中</button><button type="button" data-l="en">EN</button></div><button class="burger"');
 write(p,inject(s));
}
write('index.html',inject(idx));
write('team.html',inject(read('team.html')));
for(let i=1;i<=4;i++)write(`a/a${i}.html`,inject(read(`a/a${i}.html`)));
console.log('Updated 9 page shells and biography translations.');
