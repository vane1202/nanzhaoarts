/* Focused repairs layered on the archived production application, without replacing its data. */
(()=>{'use strict';
 const text=(cn,en,tw)=>L==='en'?en:L==='zh-TW'?(tw||twc(cn)):cn;
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const pending=s=>/【|待[補补]|to be supplied|coming soon/i.test(s||'');
 const realWa=n=>/^\d{6,15}$/.test(n||'')&&!/^0+$/.test(n);
 const originalVid=vid;
 vid=(v,z)=>(v&&(v.yt||v.fb))?originalVid(v,z):'';
 extras=(p,z,brief)=>`${!brief&&p.languages&&!pending(z?p.languages.zh:p.languages.en)?`<p class="langs">${z?'服务语言：':'Languages: '}${esc(z?p.languages.zh:p.languages.en)}</p>`:''}${vid(p.video,z)}`;
 pbtn=(href,label,z,fill)=>href?`<a class="btn ${fill?'fill':'jade'}" href="${esc(href)}" target="_blank" rel="noopener">${esc(label)}</a>`:'';
 chan=(c,z)=>[
  realWa(c.whatsapp)?`<div class="cbox"><h3>WhatsApp</h3><a class="btn fill" target="_blank" rel="noopener" href="https://wa.me/${c.whatsapp}">${z?'WhatsApp 聊天':'Chat on WhatsApp'}</a></div>`:'',
  isUrl(c.line)?`<div class="cbox"><h3>LINE</h3><a class="btn" target="_blank" rel="noopener" href="${esc(c.line)}">${z?'添加 LINE':'Add LINE'}</a>${c.lineQR?`<img class="qr" loading="lazy" src="${esc(c.lineQR)}" alt="LINE QR">`:''}${c.lineId?`<p>LINE ID: ${esc(c.lineId)}</p>`:''}</div>`:'',
  c.wechatQR||c.wechatId?`<div class="cbox"><h3>${z?'微信':'WeChat'}</h3>${c.wechatQR?`<img class="qr" src="${esc(c.wechatQR)}" alt="WeChat QR">`:''}${c.wechatId?`<p>${esc(c.wechatId)}</p>`:''}</div>`:''
 ].join('');

 function removePlaceholders(root){
  for(const node of root.querySelectorAll('.todo,.vid.ph,.btn.off'))node.remove();
  for(const node of root.querySelectorAll('p,small,.langs'))if(!node.children.length&&pending(node.textContent))node.remove();
 }
 function cleanContacts(){
  const footer=document.getElementById('contact');removePlaceholders(footer);
  const lead=footer.querySelector('.lead');if(lead)lead.textContent=text('定制雕刻、作品欣赏或到店咨询，请通过下方渠道联系我们。','For custom carving, viewing a work or arranging a visit, use the contact details below.','定製雕刻、作品欣賞或到店諮詢，請通過下方渠道聯繫我們。');
  document.querySelectorAll('#teamGrid .card').forEach(card=>{
   removePlaceholders(card);
   for(const anchor of card.querySelectorAll('a[data-open]')){anchor.href='#contact';anchor.removeAttribute('data-open');anchor.removeAttribute('target');anchor.textContent=text('联系品牌','Contact the brand','聯繫品牌');anchor.classList.add('r1-contact-fallback');}
  });
  for(const a of document.querySelectorAll('.js-wa'))if(!realWa(CO.whatsapp)){a.textContent=text('联系咨询','Contact us','聯繫諮詢');a.removeAttribute('target');a.href='#contact';}
  const choices={fWa:realWa(CO.whatsapp),fLine:isUrl(CO.line),fWx:!!(CO.wechatQR||CO.wechatId),fEm:!!CO.email};
  for(const [id,available] of Object.entries(choices)){const a=document.getElementById(id);if(a)a.hidden=!available;}
  removePlaceholders(document.getElementById('tmbody'));
 }
 const originalRender=render;render=function(){originalRender();cleanContacts();};
 const originalTeamShow=tmShow;tmShow=function(i){originalTeamShow(i);const root=document.getElementById('tmbody');removePlaceholders(root);if(!root.querySelector('.btns2 a[href^="https://wa.me/"]')){const a=document.createElement('a');a.href='#contact';a.className='r1-profile-contact';a.textContent=text('联系品牌咨询','Contact the brand','聯繫品牌諮詢');a.addEventListener('click',()=>tmClose());root.append(a);}};
 // Repair current data-dependent contact UI once, then keep it correct after all three language switches.
 render();if(L==='zh-TW')twApply(true);

 const menu=document.getElementById('menu'),burger=document.querySelector('.burger');
 function closeMenu(){menu.classList.remove('open');burger.setAttribute('aria-expanded','false');}
 burger.onclick=()=>{const on=menu.classList.toggle('open');burger.setAttribute('aria-expanded',String(on));};
 menu.onclick=event=>{if(event.target.closest('a'))closeMenu();};
 document.querySelectorAll('.lang button').forEach(b=>b.setAttribute('aria-pressed',String(b.classList.contains('on'))));
 const originalSetLang=setLang;setLang=function(...args){originalSetLang(...args);document.querySelectorAll('.lang button').forEach(b=>b.setAttribute('aria-pressed',String(b.classList.contains('on'))));if(lb.classList.contains('open'))showWork();};

 const lb=document.getElementById('lb');lb.classList.add('r1-work');lb.setAttribute('aria-labelledby','r1WorkTitle');
 lb.innerHTML='<div class="r1-work-panel" tabindex="-1"><div class="r1-work-toolbar"><span id="r1WorkLabel"></span><button class="r1-close" type="button">×</button></div><div class="r1-work-image"><img alt=""><p class="r1-image-status" role="status"></p><button class="r1-retry" type="button" hidden></button></div><div class="r1-work-copy"><h2 id="r1WorkTitle"></h2><p class="r1-work-by"></p><p class="r1-work-spec" hidden></p><p class="r1-work-description"></p><div class="r1-work-actions"><button id="r1Prev" type="button"></button><button id="r1Next" type="button"></button><a class="btn" href="#contact" id="r1WorkContact"></a></div></div></div>';
 let workIndex=0,workTrigger=null;
 const image=lb.querySelector('img'),status=lb.querySelector('.r1-image-status'),retry=lb.querySelector('.r1-retry');
 function imageReady(){status.textContent='';retry.hidden=true;}
 image.addEventListener('load',imageReady);image.addEventListener('error',()=>{status.textContent=text('图片暂时无法加载，请重试。','The image could not load. Please retry.','圖片暫時無法載入，請重試。');retry.hidden=false;});
 retry.onclick=()=>{status.textContent=text('图片加载中…','Loading image…','圖片載入中…');retry.hidden=true;image.src=WORKS[workIndex].full||WORKS[workIndex].src;};
 function indices(){return [...document.querySelectorAll('#gal figure[data-i]')].map(n=>Number(n.dataset.i));}
 function showWork(){
  const work=WORKS[workIndex],x=L==='en'?work.en:work.zh,content=s=>L==='zh-TW'?twc(s):s;
  lb.querySelector('#r1WorkLabel').textContent=text('作品详情','Work details','作品詳情');
  lb.querySelector('.r1-close').setAttribute('aria-label',text('关闭作品','Close work','關閉作品'));
  retry.textContent=text('重新加载','Retry image','重新載入');
  lb.querySelector('h2').textContent=content(x.t);lb.querySelector('.r1-work-by').textContent=text('作者：','By ','作者：')+content(L==='en'?work.artist.en:work.artist.zh);
  lb.querySelector('.r1-work-description').textContent=content(x.long||x.d||'');
  const spec=L==='en'?x.d.match(/^.*?\b(?:cm|mm)\./i):x.d.match(/^.*?(?:cm|mm|厘米|毫米)[^。]*。?/i);
  const specNode=lb.querySelector('.r1-work-spec');specNode.hidden=!spec;specNode.textContent=spec?content(spec[0]):'';
  const current=indices(),position=current.indexOf(workIndex);lb.querySelector('#r1Prev').disabled=position<=0;lb.querySelector('#r1Next').disabled=position>=current.length-1;
  lb.querySelector('#r1Prev').textContent=text('上一件','Previous','上一件');lb.querySelector('#r1Next').textContent=text('下一件','Next','下一件');lb.querySelector('#r1WorkContact').textContent=text('交流这件作品','Ask about this work','交流這件作品');
  status.textContent=text('图片加载中…','Loading image…','圖片載入中…');retry.hidden=true;image.alt=content(x.t);image.src=work.full||work.src;
  if(image.complete&&image.naturalWidth)imageReady();
 }
 function closeWork(){lb.classList.remove('open');syncDialog();if(workTrigger?.isConnected)workTrigger.focus({preventScroll:true});}
 function changeWork(delta){const current=indices(),next=current[current.indexOf(workIndex)+delta];if(next===undefined)return;workIndex=next;showWork();}
 openWork=function(figure){workIndex=Number(figure.dataset.i);workTrigger=figure;showWork();lb.classList.add('open');syncDialog();};
 lb.onclick=event=>{if(event.target===lb||event.target.closest('.r1-close'))closeWork();};
 lb.querySelector('#r1Prev').onclick=()=>changeWork(-1);lb.querySelector('#r1Next').onclick=()=>changeWork(1);lb.querySelector('#r1WorkContact').onclick=()=>closeWork();
 // A dialog may live within main (map picker), so inert only siblings along its ancestor path.
 const teamDialog=document.getElementById('tm'),mapSheet=document.getElementById('msheet');
 teamDialog.setAttribute('aria-label',text('团队介绍','Team profile','團隊介紹'));mapSheet.querySelector('[role="dialog"]').setAttribute('aria-labelledby','mname');
 let active=null,returnFocus=null;const savedInert=new Map();
 const focusable=root=>[...root.querySelectorAll('a[href],button:not(:disabled),input,textarea,select,[tabindex]:not([tabindex="-1"])')].filter(n=>!n.hidden&&n.getClientRects().length&&!n.closest('[hidden],[inert]'));
 function restoreInert(){for(const [node,state] of savedInert)node.inert=state;savedInert.clear();}
 function syncDialog(){
  const next=!mapSheet.hidden?mapSheet:teamDialog.classList.contains('open')?teamDialog:lb.classList.contains('open')?lb:null;
  if(next===active)return;restoreInert();
  if(!next){document.body.classList.remove('r1-modal-open');const previous=returnFocus;active=null;returnFocus=null;if(previous?.isConnected)previous.focus({preventScroll:true});return;}
  if(!active)returnFocus=document.activeElement;active=next;document.body.classList.add('r1-modal-open');closeMenu();
  for(let node=next;node.parentElement&&node!==document.body;node=node.parentElement){for(const sibling of node.parentElement.children)if(sibling!==node&&!/^(SCRIPT|STYLE|LINK)$/.test(sibling.tagName)){if(!savedInert.has(sibling))savedInert.set(sibling,sibling.inert);sibling.inert=true;}}
  const target=next.querySelector('.r1-close,.tmx')||focusable(next)[0]||next;target.setAttribute('tabindex',target.getAttribute('tabindex')||'0');target.focus({preventScroll:true});
 }
 const observer=new MutationObserver(syncDialog);for(const node of [lb,teamDialog,mapSheet])observer.observe(node,{attributes:true,attributeFilter:['class','hidden']});
 document.onkeydown=null;
 document.addEventListener('keydown',event=>{
  if(!active){if(event.key==='Escape'&&menu.classList.contains('open')){closeMenu();burger.focus();}return;}
  if(event.key==='Escape'){event.preventDefault();event.stopImmediatePropagation();if(active===lb)closeWork();else if(active===teamDialog){tmClose();syncDialog();}else{mapSheet.hidden=true;syncDialog();}return;}
  if(active===lb&&['ArrowLeft','ArrowRight'].includes(event.key)){event.preventDefault();changeWork(event.key==='ArrowLeft'?-1:1);return;}
  if(event.key==='Tab'){const items=focusable(active);if(!items.length){event.preventDefault();return;}const i=items.indexOf(document.activeElement);if(event.shiftKey&&(i<=0)){event.preventDefault();items.at(-1).focus();}else if(!event.shiftKey&&(i===items.length-1||i<0)){event.preventDefault();items[0].focus();}}
 },true);
 // Hide the floating contact launcher wherever an existing action area needs the space.
 if('IntersectionObserver'in window){const visible=new Map();const observer=new IntersectionObserver(entries=>{for(const entry of entries)visible.set(entry.target,entry.isIntersecting);document.getElementById('fabw').dataset.r1Suppressed=String([...visible.values()].some(Boolean));});for(const selector of ['#top','#contact','.loc']){const node=document.querySelector(selector);if(node)observer.observe(node);}}
})();
