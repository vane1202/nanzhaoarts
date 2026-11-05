#!/usr/bin/env python3
"""Generate the Phase-1 SEO pages from index.html.

Run from the repo root:  python3 tools/build_seo_pages.py
Needs: pip install opencc-python-reimplemented

Outputs (all committed, served by Cloudflare Pages as clean URLs):
  master.html team.html stores.html contact.html   -> /master /team /stores /contact
  a/a1.html .. a/a4.html                           -> /a/a1 .. /a/a4 (copies of index.html,
                                                      noindex,follow + canonical /team)
Re-run whenever index.html changes, otherwise /a/* will drift from the homepage.
"""
import re, pathlib, html
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

def page_head(title, desc, path):
    url = f"{BASE}{path}"
    return f"""<!doctype html>
<html lang="zh-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta name="description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{BASE}/img/og-cover.jpg"><meta property="og:url" content="{url}">
{ICONS}
{STYLES}
<link rel="stylesheet" href="/round1/fixes.css"><link rel="stylesheet" href="/round2/design.css?v=hero-a-wide-20261103"><link rel="stylesheet" href="/seo.css?v=1">
</head>
"""

NAV_ITEMS = [("/#story", "品牌緣起", None), ("/#culture", "玉雕文化", None), ("/master", "楊樹明老師", "/master"),
             ("/team", "南詔團隊", "/team"), ("/#gallery", "作品展示", None), ("/stores", "門店", "/stores"), ("/contact", "聯繫我們", "/contact")]

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
<p class="fnav"><a href="/">首頁</a> · <a href="/master">楊樹明老師</a> · <a href="/team">南詔團隊</a> · <a href="/stores">門店</a> · <a href="/contact">聯繫我們</a></p>
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
    dict(n="張圓", r="「南詔工匠」董事長", img="/img/team-a2.webp?v=3", wa="8615394805302",
         fb="https://www.facebook.com/profile.php?id=61550201366795", reel="https://www.facebook.com/reel/4002130003429958"),
    dict(n="張清雪", r="「南詔工匠」品牌店店長", img="/img/team-a3.webp", wa="8613238791871",
         fb="https://www.facebook.com/profile.php?id=100092552777975", reel="https://www.facebook.com/reel/1684487290062592"),
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
           '<div class="cta"><a class="btn fill" href="/contact">咨询大师定制</a><a class="btn" href="/team">认识南诏团队</a></div>', f, flags=re.S)
assert 'href="/contact"' in f and "<details" not in f and "<h1" in f
f = tw(f)
master_body = f"""<main id="main">
{f}
</main>
"""
write("master.html",
      page_head("楊樹明老師｜騰衝翡翠玉雕大師 | 南詔工匠 Nanzhao Arts",
                "楊樹明，雲南騰衝玉雕師、省級非遺代表性傳承人，南詔工匠品牌創始人。了解他的師承、代表作《風雪夜歸人》、榮譽與從藝年表。", "/master")
      + nav("/master") + master_body + FOOT)

# ---------- /team ----------
def card(p):
    return f"""<div class="card"><img loading="lazy" src="{p['img']}" alt="{p['n']}｜{p['r']}" width="600" height="600" style="aspect-ratio:1;object-fit:cover;width:100%"><div class="body"><h2 class="seo-h3">{p['n']}</h2><p class="role">{p['r']}</p>
<div class="tbtns"><a class="btn fill" target="_blank" rel="noopener" href="{p['fb']}">在 Facebook 關注</a><a class="btn jade" target="_blank" rel="noopener" href="https://wa.me/{p['wa']}">WhatsApp 聯繫</a><a class="btn jade" target="_blank" rel="noopener" href="{p['reel']}">觀看精選影片</a></div></div></div>"""

team_body = f"""<main id="main"><section class="mint team"><div class="wrap">
<p class="eyebrow">南詔團隊</p><h1 class="seo-h1">南詔團隊｜陪您讀懂一塊玉</h1>
<p class="lead culead" style="margin-bottom:26px">南詔團隊通過影片分享南詔工匠的品牌故事、玉雕文化與翡翠入門知識，並一對一陪您溝通定製需求。</p>
<div class="grid">
{''.join(card(p) for p in TEAM)}
</div>
<div class="cta"><a class="btn fill" href="/contact">聯繫我們</a><a class="btn" href="/master">認識楊樹明老師</a><a class="btn" href="/stores">查看門店</a></div>
</div></section></main>
"""
write("team.html",
      page_head("南詔團隊｜張偉、張圓、張清雪、文強 | 南詔工匠 Nanzhao Arts",
                "認識南詔工匠團隊：創始人張偉、董事長張圓、品牌店店長張清雪、供應鏈負責人文強，陪您了解翡翠與玉雕，並一對一溝通定製需求。", "/team")
      + nav("/team") + team_body + FOOT)

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
<div class="cta"><a class="btn fill" href="/contact">聯繫我們</a><a class="btn" href="/team">認識南詔團隊</a></div>
</div></section></main>
"""
write("stores.html",
      page_head("門店與工作室｜騰衝・瑞麗・香港 | 南詔工匠 Nanzhao Arts",
                "南詔工匠門店與工作室地址：騰衝市百寶街、瑞麗多寶之城35棟、香港旺角花園街好景商業中心，附地圖導航連結。", "/stores")
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
<div class="cgrid">{''.join(pcontact(p) for p in TEAM)}</div>
<p class="seo-note">門店地址與地圖導航請見<a href="/stores">門店頁</a>；團隊介紹請見<a href="/team">南詔團隊</a>。本站為品牌展示網站，不提供線上交易。</p>
</div></section></main>
"""
write("contact.html",
      page_head("聯繫南詔工匠｜定製雕刻、看料賞玉諮詢 | 南詔工匠 Nanzhao Arts",
                "聯繫南詔工匠：品牌電子郵件，以及團隊成員張偉、張圓、張清雪、文強的 WhatsApp 與 Facebook，洽詢定製雕刻、看料賞玉與到店。", "/contact")
      + nav("/contact") + contact_body + FOOT)

# ---------- /a/a1..a4 : homepage experience, noindex + canonical /team ----------
canon = '<link rel="canonical" href="https://nanzhaoarts.com/">'
assert canon in idx
for i in range(1, 5):
    t = idx.replace(canon, f'<link rel="canonical" href="{BASE}/team"><meta name="robots" content="noindex,follow">', 1)
    t = t.replace('<meta property="og:url" content="https://nanzhaoarts.com/">', f'<meta property="og:url" content="{BASE}/team">', 1)
    assert 'noindex,follow' in t
    write(f"a/a{i}.html", t)
