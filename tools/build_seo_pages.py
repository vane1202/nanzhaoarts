#!/usr/bin/env python3
"""Generate the Phase-1 SEO pages from index.html.

Run from the repo root:  python3 tools/build_seo_pages.py
Needs: pip install opencc-python-reimplemented

Outputs (all committed, served by Cloudflare Pages as clean URLs):
  master.html team.html stores.html contact.html   -> /master /team /stores /contact
  custom.html                                      -> /custom (index,follow)
  custom/<slug>.html                               -> /custom/<slug> (noindex,follow; not in sitemap yet)
  a/a1.html .. a/a4.html                           -> /a/a1 .. /a/a4 (copies of index.html,
                                                      noindex,follow + canonical /team)
Re-run whenever index.html changes, otherwise /a/* will drift from the homepage.

/custom is a public page: index,follow, listed in sitemap.xml, the shared nav
and footer, and linked from the homepage, /master, /team and /stores.
Do not invent after-sales, returns, or own-material policies; omit those items.
"""
import re, pathlib, html, json
from opencc import OpenCC

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://nanzhaoarts.com"
cc = OpenCC("s2tw")  # char-level only; phrase mode (s2twp) mangles 项目/高级/局部
_FIX = {"聯系": "聯繫", "瞭解": "了解", "舞臺": "舞台"}
def tw(s):
    s = cc.convert(s)
    for a, b in _FIX.items():
        s = s.replace(a, b)
    return s
idx = (ROOT / "index.html").read_text(encoding="utf-8")

# ---------- shared head / nav / footer ----------
head_end = idx.find("<body")
HEAD = idx[:head_end]
STYLES = "".join(re.findall(r"<style>.*?</style>", HEAD, re.S))
ICONS = re.search(r'<meta name="theme-color".*?apple-touch-icon" href="[^"]+">', HEAD, re.S).group(0)

def jsonld_tag(data):
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{payload}</script>'

def page_head(title, desc, path, robots="index,follow", og_image=None, jsonld=None):
    url = f"{BASE}{path}"
    img = og_image or f"{BASE}/img/og-cover.jpg"
    ld = ("\n" + jsonld_tag(jsonld)) if jsonld else ""
    return f"""<!doctype html>
<html lang="zh-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{img}"><meta property="og:url" content="{url}">
{ICONS}
{STYLES}
<link rel="stylesheet" href="/css/site.css">{ld}
</head>
"""

NAV_ITEMS = [("/#story", "品牌緣起", None), ("/#culture", "玉雕文化", None), ("/master", "楊樹明老師", "/master"),
             ("/team", "南詔團隊", "/team"), ("/#gallery", "作品展示", None), ("/custom", "翡翠訂製", "/custom"),
             ("/stores", "門店", "/stores"), ("/contact", "聯繫我們", "/contact")]

def nav(current):
    li = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if cur and cur == current else ""}>{t}</a></li>'
        for h, t, cur in NAV_ITEMS)
    return f"""<body><a class="r1-skip" href="#main">跳至正文</a>
<nav class="nav"><div class="wrap">
<a class="brand" href="/" aria-label="南詔工匠 Nanzhao Arts"><picture><source srcset="/img/logo-white.webp" type="image/webp"><img src="/img/logo-white.png" width="961" height="465" alt="南詔工匠 Nanzhao Arts"></picture></a>
<ul class="menu" id="menu">{li}</ul>
<button class="burger" aria-label="選單" aria-controls="menu" aria-expanded="false">☰</button>
</div></nav>
"""

FOOT = """<footer><picture><source srcset="/img/logo-white.webp" type="image/webp"><img class="flogo" loading="lazy" src="/img/logo-white.png" width="961" height="465" alt="南詔工匠 Nanzhao Arts"></picture>
<p class="fnav"><a href="/">首頁</a> · <a href="/master">楊樹明老師</a> · <a href="/team">南詔團隊</a> · <a href="/custom">翡翠訂製</a> · <a href="/stores">門店</a> · <a href="/contact">聯繫我們</a></p>
<p>© 2026 南詔工匠 · 騰衝南詔珠寶有限公司 · nanzhaoarts.com · 品牌展示網站，不提供線上交易</p></footer>
<script>(function(){var b=document.querySelector('.burger'),m=document.getElementById('menu');b.onclick=function(){b.setAttribute('aria-expanded',m.classList.toggle('open'))};m.onclick=function(e){if(e.target.tagName==='A')m.classList.remove('open')}})()</script>
</body></html>
"""

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", path, len(text))

def esc(s): return html.escape(s, quote=True)

# ---------- team data (taken from index.html TEAM; titles per site) ----------
TEAM = [
    dict(n="張偉", r="「南詔工匠」珠寶品牌創始人", img="/img/team-a1.webp", wa="8617587115637",
         fb="https://www.facebook.com/profile.php?id=61552356396891", reel="https://www.facebook.com/reel/1633329301766649"),
    dict(n="張圓", r="「南詔工匠」董事長", img="/img/team-a2-20261126.webp", wa="8615394805302",
         fb="https://www.facebook.com/profile.php?id=61550201366795", reel="https://www.facebook.com/reel/4002130003429958"),
    # 張清雪 remains on the team data in index.html as a profile, but has no public contact card.
    dict(n="文強", r="「南詔工匠」供應鏈負責人", img="/img/team-a4.webp", wa="8613320456149",
         fb="https://www.facebook.com/profile.php?id=100095150474571", reel="https://www.facebook.com/reel/1734231688266352"),
]
# keep the data in sync with index.html: fail loudly if a number/URL drifted
for p in TEAM:
    for k in ("wa", "fb", "reel"):
        val = p[k]
        assert val in idx, f"{p['n']} {k} not found in index.html: {val}"

# ---------- /master ----------
m = re.search(r'<section id="founder" class="founder">.*?</section>', idx, re.S)
f = m.group(0)
f = re.sub(r'\sdata-en="[^"]*"', "", f)
f = f.replace('<section id="founder" class="founder">', '<section class="founder" id="founder-bio">')
f = re.sub(r'<h2>杨树明 老师</h2>', '<h1 class="seo-h1">楊樹明老師｜騰衝翡翠玉雕</h1>', f)
f = re.sub(r'<details class="r2-biography"><summary>.*?</summary>', '<div class="r2-biography r2-open">', f, flags=re.S)
f = f.replace('</details>', '</div>')
f = f.replace('<a class="r2-link" href="#gallery">欣赏老师的作品 ↗</a>', '<a class="r2-link" href="/#gallery">欣赏老师的作品 ↗</a>')
f = re.sub(r'<div class="cta">.*?</div>',
           '<div class="cta"><a class="btn fill" href="/contact">咨询大师定制</a><a class="btn" href="/team">认识南诏团队</a><br><a class="seo-more" href="/custom">了解翡翠订制 ↗</a></div>', f, flags=re.S)
assert 'href="/contact"' in f and "<details" not in f and "<h1" in f
f = tw(f)
master_body = f"""<main id="main">
{f}
</main>
"""
master_ld = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "楊樹明",
    "alternateName": ["杨树明", "Yang Shuming"],
    "jobTitle": "玉雕師・省級非遺代表性傳承人",
    "url": f"{BASE}/master",
    "image": f"{BASE}/img/master-yang2.webp",
    "worksFor": {"@type": "Organization", "name": "南詔工匠 Nanzhao Arts", "url": f"{BASE}/"},
}
write("master.html",
      page_head("楊樹明老師｜騰衝翡翠玉雕大師 | 南詔工匠 Nanzhao Arts",
                "楊樹明，雲南騰衝玉雕師、省級非遺代表性傳承人，南詔工匠品牌創始人。了解他的師承、代表作《風雪夜歸人》、榮譽與從藝年表。", "/master", jsonld=master_ld)
      + nav("/master") + master_body + FOOT)

# ---------- /team ----------
# /team reuses the homepage chrome (nav, #team section markup, footer, modal, scripts, CSS)
# so it looks and behaves exactly like the homepage team section. Only the <head> SEO tags
# differ, and the other homepage sections are dropped from <main>.
def build_team_page():
    t = idx
    # head: title / canonical / robots / description / og
    title = "南詔團隊｜張偉、張圓與品牌影片 | 南詔工匠 Nanzhao Arts"
    desc = "認識南詔工匠創始人張偉與董事長張圓，了解翡翠與玉雕，並一對一溝通定製需求；公司橫版宣傳影片專區預留中。"
    url = f"{BASE}/team"
    t = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", t, count=1, flags=re.S)
    t = t.replace('<link rel="canonical" href="https://nanzhaoarts.com/">',
                  f'<link rel="canonical" href="{url}"><meta name="robots" content="index,follow">', 1)
    t = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', t, count=1)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', t, count=1)
    t = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', t, count=1)
    t = t.replace('<meta property="og:url" content="https://nanzhaoarts.com/">', f'<meta property="og:url" content="{url}">', 1)
    assert 'content="index,follow"' in t and url in t
    # nav: anchors -> homepage anchors, brand -> /
    t = t.replace('<a class="brand" href="#top"', '<a class="brand" href="/"', 1)
    nav_s = t.index('<nav class="nav">'); nav_e = t.index('</nav>', nav_s)
    nv = t[nav_s:nav_e]
    nv = re.sub(r'href="#(story|culture|gallery)"', r'href="/#\1"', nv)
    nv = nv.replace('<li><a href="/team"', '<li><a href="/team" aria-current="page"', 1)
    t = t[:nav_s] + nv + t[nav_e:]
    # main: keep only the #team section
    ms = t.index('<main id="main">'); me = t.index('</main>')
    main = t[ms:me]
    ts = main.index('<section id="team" class="mint team">')
    te = main.index('</section>', ts) + len('</section>')
    team = main[ts:te]
    team = team.replace('<p class="eyebrow"', '<h1 class="sr" data-en="Our Team · Zhang Wei, Zhang Yuan & Company Films">南诏团队 · 张伟、张圆与品牌影片</h1><p class="eyebrow"', 1)
    team = re.sub(r'<p class="seo-more-c">.*?</p>',
                  '<div class="cta cta-trio"><a class="btn" href="/contact" data-en="Contact us">联系我们</a> <a class="btn" href="/master" data-en="Meet Master Yang">认识杨树明老师</a> <a class="btn" href="/stores" data-en="Our stores">查看门店</a></div><p class="seo-more-c"><a class="seo-more" href="/custom" data-en="Learn more about custom jadeite ↗">了解翡翠订制 ↗</a></p>',
                  team, count=1, flags=re.S)
    assert 'id="teamGrid"' in team and 'href="/contact"' in team
    # the homepage script touches elements of sections we dropped: provide inert stubs
    stub_ids = ["cgrid", "gal", "galTabs", "heroCta",
                "contact", "mtoast", "pcard", "persona", "voiceGrid", "voices", "tvlb"]
    # the map-picker sheet is wired by shared scripts at load time, so keep the real (hidden) markup
    _i = idx.index('id="msheet"'); _i = idx.rfind('<div', 0, _i); _j = idx.index('<div class="mtoast"', _i)
    msheet = idx[_i:_j]
    stubs = msheet + '<div hidden aria-hidden="true" style="display:none">' + "".join(f'<div id="{i}"></div>' for i in stub_ids) + '</div>'
    # clear top padding so the fixed nav does not cover the first heading
    t = t[:ms] + '<main id="main" class="seo-team">' + team + stubs + t[me:]
    # the homepage script rewrites document.title on every render; keep the /team title instead
    old_t = "document.title=z?'南诏工匠 Nanzhao Arts | 腾冲翡翠 · 大师玉雕':'Nanzhao Arts 南诏工匠 | Master Jadeite Carving from Tengchong';"
    assert old_t in t
    t = t.replace(old_t, "document.title=z?'南诏团队｜张伟、张圆与品牌影片 | 南诏工匠 Nanzhao Arts':'Our Team | Nanzhao Arts 南诏工匠';", 1)
    # round2/design.js only restyles sections that are not on this page (selected works, culture, biography)
    t = t.replace('<script src="/round2/design.js" defer></script>', '')
    return t

write("team.html", build_team_page())

# ---------- /stores ----------
STORES = [
    ("騰衝", "總部 · 騰衝市百寶街樹明玉雕3樓", "25.033753,98.488371", "樹明玉雕", "騰衝市百寶街樹明玉雕", None),
    ("瑞麗", "瑞麗多寶之城35棟", "23.993632,97.868467", "南詔工匠", "瑞麗多寶之城35棟",
     "2025年10月15日，「南詔工匠·楊樹明大師工作站」在瑞麗啟動。"),
    ("香港", "香港旺角花園街2-16號好景商業中心23樓2304室", "22.313217,114.176892", "南詔工匠 好景商業中心",
     "Ho King Commercial Centre, 2-16 Fa Yuen Street, Mong Kok, Hong Kong", None),
]
def store_card(city, addr, ll, name, gq, note):
    la, lo = ll.split(",")
    from urllib.parse import quote
    amap = f"https://uri.amap.com/marker?position={lo},{la}&name={quote(name)}&coordinate=gaode&src=nanzhaoarts&callnative=1"
    goog = f"https://www.google.com/maps/dir/?api=1&destination={la},{lo}"
    appl = f"https://maps.apple.com/?ll={la},{lo}&q={quote(name)}"
    return f"""<div class="mc seo-store"><div class="mt"><h2 class="seo-h3">{city}</h2><p class="maddr">{addr}</p>{f'<p class="maddr">{note}</p>' if note else ''}
<div class="mapbtns"><a class="btn jade" target="_blank" rel="noopener" href="{amap}">高德地圖</a><a class="btn jade" target="_blank" rel="noopener" href="{goog}">Google 地圖</a><a class="btn jade" target="_blank" rel="noopener" href="{appl}">Apple 地圖</a></div></div></div>"""

stores_body = f"""<main id="main"><section class="loc"><div class="wrap">
<p class="eyebrow">門店與工作室</p><h1 class="seo-h1">門店與工作室｜騰衝、瑞麗、香港</h1>
<p class="lead" style="margin-bottom:26px">南詔工匠在騰衝、瑞麗與香港設有門店與工作室。如需到店看料、賞玉，歡迎先透過聯繫頁與我們溝通。</p>
<div class="grid mgrid">
{''.join(store_card(*s) for s in STORES)}
</div>
<div class="cta"><a class="btn fill" href="/contact">聯繫我們</a><a class="btn" href="/team">認識南詔團隊</a><br><a class="seo-more" href="/custom">了解翡翠訂製 ↗</a></div>
</div></section></main>
"""
stores_ld = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "南詔工匠門店與工作室",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "JewelryStore",
                "name": f"南詔工匠 · {city}",
                "address": {"@type": "PostalAddress", "streetAddress": addr},
                "geo": {"@type": "GeoCoordinates", "latitude": float(ll.split(",")[0]), "longitude": float(ll.split(",")[1])},
                "url": f"{BASE}/stores",
            },
        }
        for i, (city, addr, ll, _name, _gq, _note) in enumerate(STORES, 1)
    ],
}
write("stores.html",
      page_head("門店與工作室｜騰衝・瑞麗・香港 | 南詔工匠 Nanzhao Arts",
                "南詔工匠門店與工作室地址：騰衝市百寶街、瑞麗多寶之城35棟、香港旺角花園街好景商業中心，附地圖導航連結。", "/stores", jsonld=stores_ld)
      + nav("/stores") + stores_body + FOOT)

# ---------- /contact ----------
def pcontact(p):
    return f"""<div class="cbox"><h2 class="seo-h3">{p['n']}</h2><p class="role" style="margin-bottom:12px">{p['r']}</p><a class="btn fill" target="_blank" rel="noopener" href="https://wa.me/{p['wa']}">WhatsApp 聯繫</a><a class="btn" target="_blank" rel="noopener" href="{p['fb']}">Facebook</a></div>"""

contact_body = f"""<main id="main">
<section class="contact seo-contact"><div class="wrap">
<p class="eyebrow">聯繫我們</p><h1 class="seo-h1">聯繫南詔工匠</h1>
<p class="lead" style="margin:auto">定製雕刻、作品欣賞或到店諮詢，請透過下方渠道聯繫我們。</p>
<h2 class="seo-h3 seo-sub">品牌聯繫</h2>
<div class="cgrid"><div class="cbox"><h3>電子郵件</h3><p><a href="mailto:hello@nanzhaoarts.com">hello@nanzhaoarts.com</a></p></div></div>
<h2 class="seo-h3 seo-sub">團隊成員個人聯繫</h2>
<div class="cgrid cgrid-team">{''.join(pcontact(p) for p in TEAM)}</div>
<p class="seo-note">門店地址與地圖導航請見<a href="/stores">門店頁</a>；團隊介紹請見<a href="/team">南詔團隊</a>。本站為品牌展示網站，不提供線上交易。</p>
</div></section></main>
"""
contact_ld = {
    "@context": "https://schema.org",
    "@type": "ContactPage",
    "name": "聯繫南詔工匠",
    "url": f"{BASE}/contact",
    "mainEntity": {
        "@type": "Organization",
        "name": "南詔工匠 Nanzhao Arts",
        "url": f"{BASE}/",
        "email": "hello@nanzhaoarts.com",
    },
}
write("contact.html",
      page_head("聯繫南詔工匠｜定製雕刻、看料賞玉諮詢 | 南詔工匠 Nanzhao Arts",
                "聯繫南詔工匠：品牌電子郵件，以及團隊成員張偉、張圓、文強的 WhatsApp 與 Facebook，洽詢定製雕刻、看料賞玉與到店。", "/contact", jsonld=contact_ld)
      + nav("/contact") + contact_body + FOOT)

# ---------- /custom ----------
# Remaining unpublished until supplied: after-sales / rework / returns, and own-material FAQ.
# Do not invent prices, policies, revision counts, insurance coverage, or unstated guarantees.
# Category data is the single source for /custom cards and /custom/<slug> pages.
# To add photos later: put WebP files in /img/ and append entries to works (max 5)
# and/or scenes (max 3). Fields:
#   works[]  = dict(src, alt, caption="", w=None, h=None)
#   scenes[] = dict(src, alt, title, caption, w=None, h=None)
#   faqs[]   = (question, answer)  — the FAQ block is omitted while this is empty
#   lead_time = e.g. "7–12 個工作日", or None to hide 訂製要點 when no other points exist
#   points[] = extra already-published fact strings for that category only; do not invent copy
# Do not add these slugs to sitemap.xml until the pages are ready to be indexed.
CATS = [
    dict(slug="bangles", name="手鐲", desc="按手圍選料，圈口與條型可訂製",
         img="/img/custom-bangle.webp", alt="翡翠手鐲 / Jadeite bangles", w=1600, h=1200,
         lead_time="7–12 個工作日", points=[], works=[], scenes=[], faqs=[]),
    dict(slug="pendants", name="吊墜", desc="依寓意設計，楊老師團隊親手雕琢",
         img="/img/custom-pendant-v2.webp", alt="翡翠吊墜 / Jadeite pendant", w=1332, h=999,
         lead_time="7–12 個工作日", points=[], works=[], scenes=[], faqs=[]),
    dict(slug="rings", name="戒面鑲嵌", desc="精選戒面，按需設計鑲嵌款式",
         img="/img/custom-ring-v3.webp", alt="翡翠戒指 / Jadeite ring", w=1600, h=1200,
         lead_time="7–10 個工作日", points=[], works=[], scenes=[], faqs=[]),
    dict(slug="carvings", name="雕件擺件", desc="因料施藝，雕琢獨一無二的擺件",
         img="/img/custom-carving-v2.webp", alt="翡翠擺件 / Jadeite carving", w=1600, h=1200,
         lead_time="15–30 個工作日", points=[], works=[], scenes=[], faqs=[]),
    dict(slug="pairs", name="對牌／禮贈", desc="成對雕刻，適合情侶與禮贈",
         img="/img/custom-pair.webp", alt="翡翠對牌 / Jadeite pair plaques", w=1600, h=1200,
         lead_time="7–15 個工作日", points=[], works=[], scenes=[], faqs=[]),
    dict(slug="rough", name="翡翠收藏", desc="精選翡翠原石，開窗見種色，可藏可訂製",
         img="/img/custom-rough.webp", alt="翡翠原石收藏 / Jadeite rough stone", w=1080, h=810,
         lead_time=None, points=[], works=[], scenes=[], faqs=[]),
]
def cat_card(c):
    title, desc, img, alt, w, h = c["name"], c["desc"], c.get("img"), c.get("alt"), c.get("w"), c.get("h")
    if img:
        media = (
            f'<div class="seo-ph seo-ph-img"><img loading="lazy" src="{img}" width="{w}" height="{h}" alt="{esc(alt)}"></div>'
        )
    else:
        media = '<div class="seo-ph"><span>待補實拍圖</span></div>'
    desc_html = f'<span class="todo">{desc}</span>' if '【待補' in desc else desc
    href = f'/custom/{c["slug"]}'
    return (
        f'<article class="card">'
        f'<a class="seo-card-link" href="{href}">'
        f'{media}'
        f'<div class="body"><h3>{title}</h3><p>{desc_html}</p>'
        f'<span class="seo-card-more">查看更多 →</span></div></a></article>'
    )

STEPS = [
    ("01", "溝通需求",
     "南詔工匠位於緬甸翡翠源頭市場，自有一定規模的原石、成品貨盤優勢。與專屬顧問說明用途、預算區間，以及喜歡的種水與顏色。"),
    ("02", "選料",
     "可透過影片或到店看料，確認原石或成品料。"),
    ("03", "確認設計",
     "初稿和定稿一般以手稿或電子稿形式呈現；在材料特性的基礎上，盡量滿足客戶的需求。"),
    ("04", "報價與定金",
     "報價透明，訂製過程中的每一項環節都單獨註明。定金比例與支付方式詳情請諮詢客服。"),
    ("05", "製作與交付",
     "各品類製作周期大致為：手鐲 7–12 個工作日，吊墜 7–12 個工作日，戒面鑲嵌 7–10 個工作日，雕件擺件 15–30 個工作日，對牌 7–15 個工作日。會根據製作工序酌情記錄相關照片和影片。寄送與到店取貨方式見下方品質保障。"),
]
def step_item(num, title, desc):
    return f'<li><span class="n" aria-hidden="true">{num}</span><h3>{title}</h3><p>{desc}</p></li>'

TRUST = [
    ("作者署名", "雕工標準和檔次由客戶自行選擇，根據實際負責人署名。"),
    ("證書", "證書由 NGTC 或 HSNGTC 出具。"),
    ("寄送", "我們與順豐國際快遞合作，業務範圍覆蓋全球 200 多個國家及地區；實際可否寄達請諮詢客服。預設順豐國際快遞，保價服務可諮詢客服。"),
    ("到店取貨", "目前僅支持騰衝、瑞麗和香港門店到店取貨。"),
]
def trust_card(title, desc):
    return f'<article class="card"><h3>{title}</h3><p>{desc}</p></article>'

FAQS = [
    ("最低預算多少？", "各件訂製方案與預算請諮詢客服。最低100元即可體驗緬甸天然A貨翡翠，這不是訂製報價。"),
    ("多久完成？", "各品類製作周期大致為：手鐲 7–12 個工作日，吊墜 7–12 個工作日，戒面鑲嵌 7–10 個工作日，雕件擺件 15–30 個工作日，對牌 7–15 個工作日。"),
    ("海外客戶怎麼收貨、怎麼付款？", "我們與順豐國際快遞合作，業務範圍覆蓋全球 200 多個國家及地區；實際可否寄達請諮詢客服。預設順豐國際快遞，保價服務可諮詢客服。定金比例與支付方式詳情請諮詢客服。"),
    ("證書是哪家？", "證書由 NGTC 或 HSNGTC 出具。"),
]
def faq_item(q, a):
    return f'<details><summary><span>{q}</span></summary><p>{a}</p></details>'

def faq_jsonld(faqs):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{payload}</script>'

custom_body = f"""<main id="main">
<!-- /custom is a public page (index,follow); keep unpublished after-sales and own-material items omitted. -->
<header class="hero seo-custom-hero">
<picture><source srcset="/img/master-yang3.webp" type="image/webp"><img src="/img/master-yang3.jpg" width="1500" height="1000" fetchpriority="high" alt="玉雕大師楊樹明雕琢翡翠 / Master Yang Shuming carving jadeite"></picture>
<div class="htxt">
<h1>翡翠訂製</h1>
<p class="sub">楊樹明老師團隊・一對一翡翠訂製</p>
<div class="btns"><a class="btn fill" href="/contact">聯繫專屬顧問</a></div>
</div></header>
<section class="seo-custom-cats" id="categories">
<div class="wrap">
<p class="eyebrow">可訂製品類</p>
<h2>可以訂製什麼</h2>
<p class="lead">翡翠訂製包括手鐲、吊墜、戒面鑲嵌、雕件擺件與對牌，亦可選購翡翠原石收藏。</p>
<div class="grid">
{''.join(cat_card(c) for c in CATS)}
</div>
</div></section>
<section class="mint seo-custom-flow" id="process">
<div class="wrap">
<p class="eyebrow">從溝通到交付</p>
<h2>訂製流程</h2>
<ol class="seo-steps">
{''.join(step_item(*s) for s in STEPS)}
</ol>
</div></section>
<section class="trust seo-custom-trust" id="assurance">
<div class="wrap">
<p class="eyebrow">交付與保障</p>
<h2>品質保障</h2>
<div class="grid">
{''.join(trust_card(*t) for t in TRUST)}
</div>
</div></section>
<section class="mint seo-custom-faq" id="faq">
<div class="wrap">
<p class="eyebrow">常見問題</p>
<h2>常見問題</h2>
{faq_jsonld(FAQS)}
<div class="seo-faq">
{''.join(faq_item(*f) for f in FAQS)}
</div>
</div></section>
<section class="contact seo-custom-cta" id="custom-cta">
<div class="wrap">
<p class="eyebrow">開始諮詢</p>
<h2>與我們談談您的想法</h2>
<div class="cta cta-trio"><a class="btn" href="/contact">聯繫我們</a> <a class="btn" href="/master">認識楊樹明老師</a> <a class="btn" href="/stores">查看門店</a></div>
</div></section>
</main>
"""
write("custom.html",
      page_head("翡翠訂製｜南詔工匠 楊樹明老師團隊 | Nanzhao Arts",
                "楊樹明老師團隊提供一對一翡翠訂製。了解可訂製品類、訂製流程與聯繫方式，由專屬顧問協助溝通需求。",
                "/custom")
      + nav("/custom") + custom_body + FOOT)


def ph_slot(kind="image"):
    # kind=image -> gallery placeholder; kind=scene -> scene card placeholder (no invented captions).
    label = "圖片待補充" if kind == "image" else "場景待補充"
    cap = "" if kind == "image" else "<h3>場景待補充</h3><p>說明待補充</p>"
    return f'<div class="seo-slot seo-slot-ph"><div class="seo-ph"><span>{label}</span></div>{cap}</div>'

def work_slot(item):
    src, alt = item["src"], esc(item.get("alt") or "")
    cap = item.get("caption") or ""
    wh = f' width="{item["w"]}" height="{item["h"]}"' if item.get("w") and item.get("h") else ""
    cap_attr = f' data-caption="{esc(cap)}"' if cap else ""
    cap_html = f'<p class="seo-slot-cap">{esc(cap)}</p>' if cap else ""
    return (
        f'<a class="seo-slot seo-slot-img" href="{esc(src)}" data-lightbox="works"{cap_attr}>'
        f'<div class="seo-ph seo-ph-img"><img loading="lazy" src="{esc(src)}"{wh} alt="{alt}"></div>'
        f'{cap_html}</a>'
    )

def scene_slot(item):
    src, alt = item["src"], esc(item.get("alt") or item.get("title") or "")
    title, cap = item.get("title") or "", item.get("caption") or ""
    wh = f' width="{item["w"]}" height="{item["h"]}"' if item.get("w") and item.get("h") else ""
    cap_attr = f' data-caption="{esc((title + " — " + cap).strip(" —"))}"' if (title or cap) else ""
    return (
        f'<a class="seo-slot seo-slot-scene" href="{esc(src)}" data-lightbox="scenes"{cap_attr}>'
        f'<div class="seo-ph seo-ph-img"><img loading="lazy" src="{esc(src)}"{wh} alt="{alt}"></div>'
        f'<h3>{esc(title)}</h3><p>{esc(cap)}</p></a>'
    )

def breadcrumb_jsonld(page):
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "翡翠訂製", "item": f"{BASE}/custom"},
            {"@type": "ListItem", "position": 2, "name": page["name"], "item": f"{BASE}/custom/{page['slug']}"},
        ],
    }
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{payload}</script>'

def category_body(page, cats):
    works = list(page.get("works") or [])[:5]
    scenes = list(page.get("scenes") or [])[:3]
    faqs = list(page.get("faqs") or [])
    points = list(page.get("points") or [])
    if page.get("lead_time"):
        points = [f'製作周期大致為 {page["lead_time"]}。'] + points

    if works:
        gallery = "".join(work_slot(it) for it in works)
    else:
        gallery = "".join(ph_slot("image") for _ in range(5))
    gallery_sec = (
        '<section class="seo-cat-gallery" id="works">\n'
        '<div class="wrap">\n'
        '<p class="eyebrow">作品圖庫</p>\n'
        ' <h2>作品圖庫</h2>\n'
        f'<div class="seo-slots seo-slots-5">{gallery}</div>\n'
        '</div></section>\n'
    )

    if scenes:
        scene_html = "".join(scene_slot(it) for it in scenes)
    else:
        scene_html = "".join(ph_slot("scene") for _ in range(3))
    scene_sec = (
        '<section class="mint seo-cat-scenes" id="scenes">\n'
        '<div class="wrap">\n'
        '<p class="eyebrow">應用場景</p>\n'
        '<h2>應用場景</h2>\n'
        f'<div class="seo-slots seo-slots-3">{scene_html}</div>\n'
        '</div></section>\n'
    )

    if points:
        items = "".join(f'<li>{esc(pt)}</li>' for pt in points)
        points_sec = (
            '<section class="seo-cat-points" id="notes">\n'
            '<div class="wrap">\n'
            '<p class="eyebrow">訂製要點</p>\n'
            '<h2>訂製要點</h2>\n'
            f'<ul class="seo-cat-facts">{items}</ul>\n'
            '</div></section>\n'
        )
    else:
        points_sec = ""

    process_sec = (
        '<section class="mint seo-cat-process" id="process">\n'
        '<div class="wrap">\n'
        '<p class="eyebrow">訂製流程</p>\n'
        '<h2>訂製流程</h2>\n'
        '<p class="seo-cat-strip">溝通需求 · 選料 · 確認設計 · 報價與定金 · 製作與交付</p>\n'
        '<p class="seo-more-c"><a class="seo-more" href="/custom#process">了解完整訂製流程 ↗</a></p>\n'
        '</div></section>\n'
    )

    if faqs:
        faq_sec = (
            '<section class="mint seo-custom-faq" id="faq">\n'
            '<div class="wrap">\n'
            '<p class="eyebrow">常見問題</p>\n'
            ' <h2>常見問題</h2>\n'
            f'{faq_jsonld(faqs)}\n'
            '<div class="seo-faq">\n'
            f'{"".join(faq_item(*f) for f in faqs)}\n'
            '</div>\n'
            '</div></section>\n'
        )
    else:
        faq_sec = ""

    others = [c for c in cats if c["slug"] != page["slug"]]
    other_links = "".join(
        f'<li><a href="/custom/{c["slug"]}">{c["name"]}</a></li>' for c in others
    )
    bottom_sec = (
        '<section class="contact seo-custom-cta seo-cat-more" id="more">\n'
        '<div class="wrap">\n'
        '<p class="eyebrow">其他品類</p>\n'
        '<h2>其他品類</h2>\n'
        f'<ul class="seo-cat-others">{other_links}</ul>\n'
        '<div class="cta cta-trio"><a class="btn fill" href="/contact">諮詢訂製</a></div>\n'
        '</div></section>\n'
    )

    img, alt, w, h = page["img"], esc(page["alt"]), page["w"], page["h"]
    return (
        f'<main id="main" class="seo-cat">\n'
        f'{breadcrumb_jsonld(page)}\n'
        f'<header class="seo-cat-hero">\n'
        f'<div class="wrap">\n'
        f'<nav class="seo-bc" aria-label="breadcrumb"><a href="/custom">翡翠訂製</a>'
        f'<span aria-hidden="true"> › </span><span>{page["name"]}</span></nav>\n'
        f'<h1>{page["name"]}</h1>\n'
        f'<p class="sub">{page["desc"]}</p>\n'
        f'<div class="seo-ph seo-ph-img seo-cat-hero-img">'
        f'<img src="{img}" width="{w}" height="{h}" fetchpriority="high" alt="{alt}"></div>\n'
        f'<div class="btns"><a class="btn fill" href="/contact">諮詢訂製</a></div>\n'
        f'</div></header>\n'
        f'{gallery_sec}{scene_sec}{points_sec}{process_sec}{faq_sec}{bottom_sec}'
        f'</main>\n'
    )

def write_category_pages(cats):
    for page in cats:
        title = f'{page["name"]}｜翡翠訂製｜南詔工匠 Nanzhao Arts'
        desc = f'{page["desc"]}楊樹明老師團隊提供一對一翡翠訂製。'
        path = f'/custom/{page["slug"]}'
        write(f'custom/{page["slug"]}.html',
              page_head(title, desc, path, robots="noindex,follow")
              + nav("/custom") + category_body(page, cats) + FOOT)


write_category_pages(CATS)

# ---------- /works/<slug> : dedicated artwork detail pages from index.html WORKS ----------
def extract_works():
    m = re.search(r"const WORKS=\[(.*?)\];", idx, re.S)
    assert m, "WORKS array not found in index.html"
    items = []
    pat = re.compile(
        r"\{cat:'finished',src:'([^']+)',full:'(/img/works/([a-z0-9-]+)-full\.webp)',"
        r"artist:\{zh:'([^']+)',en:'([^']+)'\},\s*"
        r"zh:\{t:'([^']+)',d:'([^']+)',long:'([^']+)'\},\s*"
        r"en:\{t:'([^']+)',d:'([^']+)',long:'([^']+)'\}\}",
        re.S,
    )
    for g in pat.finditer(m.group(1)):
        items.append(dict(
            card=g.group(1), full=g.group(2), slug=g.group(3),
            artist_cn=g.group(4), artist_en=g.group(5),
            t_cn=g.group(6), d_cn=g.group(7), long_cn=g.group(8),
            t_en=g.group(9), d_en=g.group(10), long_en=g.group(11),
        ))
    assert len(items) == 6, f"Expected 6 finished works with full images, found {len(items)}"
    return items

WORK_DIMS = {
    "fengxue": (2000, 948), "zizai": (2000, 924), "yulong": (2000, 952),
    "shuangchi": (2000, 952), "chushou": (2000, 952), "yingwu": (2000, 1000),
}
WORKS_LIST = extract_works()
for wi, w in enumerate(WORKS_LIST):
    t_tw, d_tw, long_tw, artist_tw = tw(w["t_cn"]), tw(w["d_cn"]), tw(w["long_cn"]), tw(w["artist_cn"])
    prev_w = WORKS_LIST[(wi - 1) % len(WORKS_LIST)]
    next_w = WORKS_LIST[(wi + 1) % len(WORKS_LIST)]
    iw, ih = WORK_DIMS[w["slug"]]
    work_ld = {
        "@context": "https://schema.org",
        "@type": "VisualArtwork",
        "name": t_tw,
        "alternateName": w["t_en"],
        "creator": {"@type": "Person", "name": artist_tw, "url": f"{BASE}/master"},
        "artMedium": "翡翠 / Burmese Jadeite",
        "artform": "玉雕 / Jade Carving",
        "image": f"{BASE}{w['full']}",
        "description": long_tw,
        "url": f"{BASE}/works/{w['slug']}",
    }
    work_body = f"""<main id="main"><section class="work-page"><div class="wrap">
<nav class="work-crumb" aria-label="Breadcrumb"><a href="/#gallery" data-ui-cn="作品展示" data-ui-tw="作品展示" data-ui-en="Our works">作品展示</a><span aria-hidden="true">/</span><strong data-ui-cn="{esc(w['t_cn'])}" data-ui-tw="{esc(t_tw)}" data-ui-en="{esc(w['t_en'])}">{esc(t_tw)}</strong></nav>
<p class="eyebrow" data-ui-cn="品牌作品" data-ui-tw="品牌作品" data-ui-en="Signature Work">品牌作品</p>
<h1 class="seo-h1" data-ui-cn="{esc(w['t_cn'])}" data-ui-tw="{esc(t_tw)}" data-ui-en="{esc(w['t_en'])}">{esc(t_tw)}</h1>
<div class="work-meta">
<span><span data-ui-cn="作者：" data-ui-tw="作者：" data-ui-en="Artist: ">作者：</span><a href="/master" data-ui-cn="{esc(w['artist_cn'])}" data-ui-tw="{esc(artist_tw)}" data-ui-en="{esc(w['artist_en'])}">{esc(artist_tw)}</a></span>
<span data-ui-cn="翡翠成品" data-ui-tw="翡翠成品" data-ui-en="Finished Jadeite">翡翠成品</span>
</div>
<figure class="work-stage"><img src="{w['full']}" width="{iw}" height="{ih}" fetchpriority="high" alt="{esc(t_tw)} — {esc(artist_tw)}"></figure>
<p class="work-essay" data-ui-cn="{esc(w['long_cn'])}" data-ui-tw="{esc(long_tw)}" data-ui-en="{esc(w['long_en'])}">{esc(long_tw)}</p>
<div class="cta"><a class="btn fill" href="/contact" data-ui-cn="交流这件作品" data-ui-tw="交流這件作品" data-ui-en="Ask about this work">交流這件作品</a><a class="btn" href="/master" data-ui-cn="认识杨树明老师" data-ui-tw="認識楊樹明老師" data-ui-en="Meet Master Yang">認識楊樹明老師</a><a class="seo-more" href="/custom" data-ui-cn="了解翡翠订制 ↗" data-ui-tw="了解翡翠訂製 ↗" data-ui-en="Learn more about custom jadeite ↗">了解翡翠訂製 ↗</a></div>
<nav class="work-pager" aria-label="More works">
<a href="/works/{prev_w['slug']}"><small data-ui-cn="← 上一件作品" data-ui-tw="← 上一件作品" data-ui-en="← Previous work">← 上一件作品</small><strong data-ui-cn="{esc(prev_w['t_cn'])}" data-ui-tw="{esc(tw(prev_w['t_cn']))}" data-ui-en="{esc(prev_w['t_en'])}">{esc(tw(prev_w['t_cn']))}</strong></a>
<a class="next" href="/works/{next_w['slug']}"><small data-ui-cn="下一件作品 →" data-ui-tw="下一件作品 →" data-ui-en="Next work →">下一件作品 →</small><strong data-ui-cn="{esc(next_w['t_cn'])}" data-ui-tw="{esc(tw(next_w['t_cn']))}" data-ui-en="{esc(next_w['t_en'])}">{esc(tw(next_w['t_cn']))}</strong></a>
</nav>
</div></section></main>
"""
    write(f"works/{w['slug']}.html",
          page_head(f"{t_tw}｜{artist_tw}翡翠玉雕作品 | 南詔工匠 Nanzhao Arts",
                    d_tw, f"/works/{w['slug']}", og_image=f"{BASE}{w['full']}", jsonld=work_ld)
          + nav("/#gallery") + work_body + FOOT)

# ---------- /a/a1..a4 : homepage experience, noindex + canonical /team ----------
canon = '<link rel="canonical" href="https://nanzhaoarts.com/">'
assert canon in idx
for i in range(1, 5):
    t = idx.replace(canon, f'<link rel="canonical" href="{BASE}/team"><meta name="robots" content="noindex,follow">', 1)
    t = t.replace('<meta property="og:url" content="https://nanzhaoarts.com/">', f'<meta property="og:url" content="{BASE}/team">', 1)
    assert 'noindex,follow' in t
    write(f"a/a{i}.html", t)

# Shared languages, consultation routing and accessible video controls.
# Keep this post-process last so regenerated SEO pages retain the common UI.
import subprocess
subprocess.run(["node", str(ROOT / "tools" / "build_site_ui.mjs")], cwd=ROOT, check=True)
