/* Shared UI for the existing static site. No persistent adviser attribution. */
(()=>{
 'use strict';
 const q=(s,r=document)=>r.querySelector(s),all=(s,r=document)=>[...r.querySelectorAll(s)];
 const valid=['zh-TW','zh-CN','en'];
 const app=typeof setLang==='function';
 let language=document.documentElement.lang;
 const choose=(cn,tw,en)=>language==='en'?en:language==='zh-CN'?cn:tw;
 const adviserData=[
  ['a1','张伟','張偉','Zhang Wei','8617587115637'],
  ['a2','张圆','張圓','Zhang Yuan','8615394805302'],
  ['a4','文强','文強','Wen Qiang','8613320456149']
 ];
 const ref=new URLSearchParams(location.search).get('ref')||location.pathname.match(/^\/a\/(a[1-4])(?:\.html)?\/?$/)?.[1];
 const adviser=adviserData.find(a=>a[0]===ref);
 const name=()=>adviser&&choose(...adviser.slice(1,4));
 const contactURL=()=>'/contact'+(adviser?'?ref='+adviser[0]:'');
 const translations=all('[data-ui-en]').map(node=>({node,cn:node.dataset.uiCn,tw:node.dataset.uiTw,en:node.dataset.uiEn}));
 function propagate(){
  for(const a of all('a[href]')){
   if(a.id==='fab'||a.closest('.msheet'))continue;
   const raw=a.getAttribute('href');
   if(!raw||raw.startsWith('javascript:'))continue;
   let u;try{u=new URL(raw,location.href);}catch{continue;}
   if(u.origin!==location.origin||!/^https?:$/.test(u.protocol))continue;
   if(u.hash==='#contact'){
    u=new URL(contactURL(),location.origin);
    a.removeAttribute('target');
   }
   // Only propagate context through real site pages, never media or email.
   if(!/^\/(?:index\.html|team(?:\.html)?|master(?:\.html)?|stores(?:\.html)?|contact(?:\.html)?|custom(?:\.html)?|custom\/[a-z0-9-]+(?:\.html)?|works\/[a-z0-9-]+(?:\.html)?|a\/a[1-4](?:\.html)?)?\/?$/.test(u.pathname))continue;
   if(adviser)u.searchParams.set('ref',adviser[0]);
   a.setAttribute('href',u.pathname+u.search+u.hash);
  }
 }
 function consultation(){
  const host=q('#contact .wrap');
  if(host){
   let row=q('.ui-consult',host);
   if(!row){row=document.createElement('div');row.className='ui-consult';const lead=q('.lead',host);lead?.after(row);}
   row.replaceChildren();
   const a=document.createElement('a');a.className='btn fill';
   if(adviser){a.href='https://wa.me/'+adviser[4];a.target='_blank';a.rel='noopener';a.textContent=choose('联系顾问：','聯繫顧問：','Contact your consultant: ')+name()+' · WhatsApp';}
   else{a.href=contactURL();a.textContent=choose('选择顾问 · WhatsApp 咨询','選擇顧問 · WhatsApp 諮詢','Choose a consultant · WhatsApp');}
   row.append(a);
  }
  const fm=q('.fabm');
  if(fm){let a=q('.ui-adviser-link',fm);if(!a){a=document.createElement('a');a.className='ui-adviser-link';fm.prepend(a);}a.href=contactURL();a.textContent=choose('选择顾问','選擇顧問','Choose a consultant');}
  // Keep the brand mailbox available, with personal contact channels grouped first.
  const contact=q('.seo-contact .wrap');
  if(contact){
   const headings=all('h2.seo-sub',contact);
   if(headings.length===2){const brand=headings.find(h=>h.nextElementSibling?.querySelector('a[href^="mailto:"]'));const team=headings.find(h=>h!==brand);if(brand&&team){const grid=team.nextElementSibling;brand.before(team,grid);}}
   for(const card of all('.cbox',contact)){
    const wa=q('a[href^="https://wa.me/"]',card);if(!wa)continue;
    const match=adviser&&wa.href==='https://wa.me/'+adviser[4];
    card.classList.toggle('ui-referral',!!match);
    let badge=q('.ui-badge',card);
    if(match){if(!badge){badge=document.createElement('p');badge.className='ui-badge';card.prepend(badge);}badge.textContent=choose('来自您访问的社交账号','來自您造訪的社交帳號','From the social profile you visited');card.parentElement.prepend(card);}
   }
  }
 }
 function videos(){
  for(const v of all('.vid[data-yt],.vid[data-fb]')){
   v.setAttribute('role','button');v.tabIndex=0;
   const card=v.closest('.card');
   const who=q('.team-heading h3',card||v.parentElement)?.textContent||'';
   v.setAttribute('aria-label',choose('播放视频','播放影片','Play video')+(who?' · '+who:''));
   if(!v.dataset.uiSource){
    let source=v.dataset.yt?'https://www.youtube.com/watch?v='+encodeURIComponent(v.dataset.yt):decodeURIComponent(v.dataset.fb);
    if(!/^https:\/\/(?:www\.)?(?:youtube\.com|facebook\.com)\//.test(source))continue;
    v.dataset.uiSource=source;
    const a=document.createElement('a');a.className='ui-source';a.href=source;a.target='_blank';a.rel='noopener';
    // A sibling keeps the fallback usable after the poster becomes an iframe.
    v.after(a);
   }
  }
  for(const a of all('.ui-source'))a.textContent=choose('无法播放？打开原视频 ↗','無法播放？開啟原影片 ↗','Video unavailable? Open original ↗');
 }
 function profiles(){
  for(const card of all('#teamGrid > .card')){
   const heading=q('.team-heading',card);if(!heading)continue;
   let b=q('.ui-profile',heading);
   if(!b){b=document.createElement('button');b.type='button';b.className='ui-profile';heading.append(b);b.addEventListener('click',e=>{e.stopPropagation();card.click();});}
   b.textContent=choose('查看个人介绍 ↗','查看個人介紹 ↗','View profile ↗');
   b.setAttribute('aria-label',choose('查看','查看','View profile of ')+(q('h3',heading)?.textContent||''));
  }
 }
 function refresh(){
  language=document.documentElement.lang;
  consultation();videos();profiles();propagate();
  all('.lang button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.l===language)));
 }
 if(app){
  const original=setLang;
  setLang=function(...args){const result=original.apply(this,args);refresh();return result;};
  const originalRender=render;
  render=function(...args){const result=originalRender.apply(this,args);queueMicrotask(refresh);return result;};
 }else{
  function change(l,save){
   if(!valid.includes(l))l='zh-TW';
   language=l;document.documentElement.lang=l;
   for(const t of translations)if(t.node.isConnected)t.node.innerHTML=choose(t.cn,t.tw,t.en);
   for(const b of all('.lang button'))b.classList.toggle('on',b.dataset.l===l);
   const h=q('h1');if(h)document.title=h.textContent+' | Nanzhao Arts';
   const burger=q('.burger');if(burger)burger.setAttribute('aria-label',choose('菜单','選單','Menu'));
   if(save)try{localStorage.setItem('lang2',l);}catch{}
   refresh();
  }
  all('.lang button').forEach(b=>b.addEventListener('click',()=>change(b.dataset.l,true)));
  let saved='zh-TW';try{saved=localStorage.getItem('lang2')||saved;}catch{}
  change(saved,false);
  const burger=q('.burger'),menu=q('#menu');
  if(burger&&menu){
   const close=()=>{menu.classList.remove('open');burger.setAttribute('aria-expanded','false');};
   menu.addEventListener('click',e=>{if(e.target.closest('a'))close();});
   document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.classList.contains('open')){close();burger.focus();}});
  }
 }

 function galleryLightbox(){
  const items=all('a[data-lightbox]');
  if(!items.length)return;
  let box=q('#seo-lb');
  if(!box){
   box=document.createElement('div');
   box.id='seo-lb';
   box.className='seo-lb';
   box.setAttribute('role','dialog');
   box.setAttribute('aria-modal','true');
   box.innerHTML='<button type="button" class="seo-lb-x" aria-label="Close">×</button><img alt=""><p class="seo-lb-cap"></p>';
   document.body.append(box);
   const close=()=>{box.classList.remove('open');box.setAttribute('aria-hidden','true');document.body.style.overflow='';};
   box.addEventListener('click',e=>{if(e.target===box||e.target.closest('.seo-lb-x'))close();});
   document.addEventListener('keydown',e=>{if(e.key==='Escape'&&box.classList.contains('open'))close();});
   box._close=close;
  }
  if(box.dataset.bound==='1')return;
  box.dataset.bound='1';
  items.forEach(a=>{
   a.addEventListener('click',e=>{
    e.preventDefault();
    const img=q('img',box),cap=q('.seo-lb-cap',box);
    img.src=a.getAttribute('href');
    img.alt=a.querySelector('img')?.alt||'';
    cap.textContent=a.dataset.caption||'';
    cap.style.display=cap.textContent?'block':'none';
    box.classList.add('open');
    box.setAttribute('aria-hidden','false');
    document.body.style.overflow='hidden';
    q('.seo-lb-x',box)?.focus();
   });
  });
 }
 // Keyboard activation reuses the existing player handler; an activated iframe is
 // no longer a button. Fallback links never bubble into the promo-block handler.
 document.addEventListener('keydown',e=>{const v=e.target.closest('.vid[role="button"]');if(v&&e.target===v&&['Enter',' '].includes(e.key)){e.preventDefault();v.click();}});
 document.addEventListener('click',e=>{
  if(e.target.closest('.ui-source')){e.stopPropagation();return;}
  // Profile and work dialogs are populated by the existing click handlers.
  queueMicrotask(()=>{videos();propagate();});
  const v=e.target.closest('.vid')||e.target.closest('.promo-film-block')?.querySelector('.vid');
  if(!v)return;
  const label=v.getAttribute('aria-label');
  queueMicrotask(()=>{const f=q('iframe',v);if(!f)return;v.removeAttribute('role');v.removeAttribute('tabindex');v.removeAttribute('aria-label');f.title=label||choose('品牌视频','品牌影片','Brand video');if(e.target===v)f.focus();});
 },true);
 galleryLightbox();
 refresh();
})();
