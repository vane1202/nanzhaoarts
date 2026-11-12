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
 ,['翡翠訂製','翡翠订制','Custom Jadeite'],['楊樹明老師團隊・一對一翡翠訂製','杨树明老师团队・一对一翡翠订制',"Master Yang Shuming's team · one-to-one custom jadeite"],['聯繫專屬顧問','联系专属顾问','Contact your consultant'],
 ['可訂製品類','可订制品类','What we can make'],['可以訂製什麼','可以订制什么','What can be commissioned'],['以下為規劃中的訂製品類；各品類說明與實拍圖將於資料齊備後更新。','以下为规划中的订制品类；各品类说明与实拍图将于资料齐备后更新。','These are the categories planned for this service. Descriptions and photographs will be added when the copy is ready.'],
 ['待補實拍圖','待补实拍图','Photo to be supplied'],
 ['手鐲','手镯','Bangles'],['吊墜','吊坠','Pendants'],['戒面鑲嵌','戒面镶嵌','Cabochons and setting'],['雕件擺件','雕件摆件','Carvings and ornaments'],['對牌／禮贈','对牌／礼赠','Pair plaques and gifts'],['翡翠收藏','翡翠收藏','Jadeite rough collection'],
 ['<span class="todo">【待補：手鐲訂製的一句說明】</span>','<span class="todo">【待补：手镯订制的一句说明】</span>','<span class="todo">[To be supplied: one-line description of custom bangles]</span>'],
 ['<span class="todo">【待補：吊墜訂製的一句說明】</span>','<span class="todo">【待补：吊坠订制的一句说明】</span>','<span class="todo">[To be supplied: one-line description of custom pendants]</span>'],
 ['<span class="todo">【待補：戒面與鑲嵌的一句說明】</span>','<span class="todo">【待补：戒面与镶嵌的一句说明】</span>','<span class="todo">[To be supplied: one-line description of cabochons and setting]</span>'],
 ['<span class="todo">【待補：雕件擺件的一句說明】</span>','<span class="todo">【待补：雕件摆件的一句说明】</span>','<span class="todo">[To be supplied: one-line description of carvings and ornaments]</span>'],
 ['<span class="todo">【待補：對牌或禮贈的一句說明】</span>','<span class="todo">【待补：对牌或礼赠的一句说明】</span>','<span class="todo">[To be supplied: one-line description of pair plaques or gifts]</span>'],
 ['精選翡翠原石，開窗見種色，可藏可訂製','精选翡翠原石，开窗见种色，可藏可订制',"Selected jadeite rough, windowed to show color. Collect or carve to order."],
 ['從溝通到交付','从沟通到交付','From first conversation to delivery'],['訂製流程','订制流程','The commissioning process'],
 ['溝通需求','沟通需求','Share your needs'],['選料','选料','Choose the stone'],['確認設計','确认设计','Approve the design'],['報價與定金','报价与定金','Quotation and deposit'],['製作與交付','制作与交付','Making and delivery'],
 ['與專屬顧問說明用途、預算區間，以及喜歡的種水與顏色。預算起點：<span class="todo">【待補：起訂預算區間】</span>。','与专属顾问说明用途、预算区间，以及喜欢的种水与颜色。预算起点：<span class="todo">【待补：起订预算区间】</span>。','Tell your consultant the intended use, budget range, and the texture and colour you prefer. Starting budget: <span class="todo">[To be supplied: starting budget range]</span>.'],
 ['可透過影片或到店看料，確認原石或成品料。','可通过视频或到店看料，确认原石或成品料。','View stones by video or in store, and confirm the rough or finished material.'],
 ['由老師或團隊提供手稿或效果圖建議，確認後再進入製作。','由老师或团队提供手稿或效果图建议，确认后再进入制作。','The master or the team shares a sketch or visual proposal; making begins after you approve it.'],
 ['報價組成：<span class="todo">【待補：報價組成，例如料價、工費、鑲嵌】</span>。確認後支付定金再開始製作。','报价组成：<span class="todo">【待补：报价组成，例如料价、工费、镶嵌】</span>。确认后支付定金再开始制作。','The quotation includes: <span class="todo">[To be supplied: what the quote covers, e.g. stone, carving, setting]</span>. Making starts after the deposit is paid.'],
 ['製作期間會回報進度，完工後以影片確認，再寄出或到店取件。周期：<span class="todo">【待補：製作周期】</span>。','制作期间会回报进度，完工后以视频确认，再寄出或到店取件。周期：<span class="todo">【待补：制作周期】</span>。','You receive progress updates during making, then a completion video before shipment or collection. Timeline: <span class="todo">[To be supplied: production time]</span>.'],
 ['交付與保障','交付与保障','Quality and delivery'],['品質保障','品质保障','Our assurances'],['作者署名','作者署名','Attribution'],['證書','证书','Certificate'],['交付','交付','Delivery'],['售後','售后','After-sales'],
 ['完成後會註明作者為楊樹明老師或團隊成員。','完成后会注明作者为杨树明老师或团队成员。','Finished work is attributed to Master Yang Shuming or a member of the team.'],
 ['檢測機構：<span class="todo">【待補：檢測機構】</span>','检测机构：<span class="todo">【待补：检测机构】</span>','Testing laboratory: <span class="todo">[To be supplied: testing laboratory]</span>'],
 ['<span class="todo">【待補：寄送地區與方式】</span>','<span class="todo">【待补：寄送地区与方式】</span>','<span class="todo">[To be supplied: shipping regions and method]</span>'],
 ['<span class="todo">【待補：修改、保養、退換規則】</span>','<span class="todo">【待补：修改、保养、退换规则】</span>','<span class="todo">[To be supplied: revision, care, and return policy]</span>'],
 ['常見問題','常见问题','Frequently asked questions'],
 ['最低預算多少？','最低预算多少？','What is the starting budget?'],
 ['多久完成？','多久完成？','How long does it take?'],
 ['可以用自己的料嗎？','可以用自己的料吗？','Can I bring my own stone?'],
 ['海外怎麼收貨？','海外怎么收货？','How does international delivery work?'],
 ['證書是哪家？','证书是哪家？','Which laboratory issues the certificate?'],
 ['不滿意怎麼辦？','不满意怎么办？','What if I am not satisfied?'],
 ['起訂預算見<span class="todo">【待補：起訂預算區間】</span>。歡迎先告訴顧問用途與偏好，再一起看適配的料與方案。','起订预算见<span class="todo">【待补：起订预算区间】</span>。欢迎先告诉顾问用途与偏好，再一起看适配的料与方案。','The starting budget is <span class="todo">[To be supplied: starting budget range]</span>. Share the intended use and your preferences, and a consultant will help you review suitable stones and options.'],
 ['製作周期見<span class="todo">【待補：製作周期】</span>。確認設計與定金後開始計算，顧問會同步進度。','制作周期见<span class="todo">【待补：制作周期】</span>。确认设计与定金后开始计算，顾问会同步进度。','The production time is <span class="todo">[To be supplied: production time]</span>. It is counted after the design and deposit are confirmed, and your consultant will share progress updates.'],
 ['<span class="todo">【待補：是否接受客戶自帶料，以及注意事項】</span>','<span class="todo">【待补：是否接受客户自带料，以及注意事项】</span>','<span class="todo">[To be supplied: whether clients may bring their own stone, and any notes]</span>'],
 ['<span class="todo">【待補：可寄送的國家或地區與方式】</span>','<span class="todo">【待补：可寄送的国家或地区与方式】</span>','<span class="todo">[To be supplied: countries or regions served, and the shipping method]</span>'],
 ['<span class="todo">【待補：檢測機構】</span>','<span class="todo">【待补：检测机构】</span>','<span class="todo">[To be supplied: testing laboratory]</span>'],
 ['開始諮詢','开始咨询','Start a conversation'],['與我們談談您的想法','与我们谈谈您的想法','Tell us about your piece'],
 ['認識楊樹明老師','认识杨树明老师','Meet Master Yang'],['查看門店','查看门店','Our stores']

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
for(const p of ['master.html','stores.html','contact.html','custom.html']){
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
console.log('Updated 10 page shells and biography translations.');
