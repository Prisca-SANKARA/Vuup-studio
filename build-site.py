"""Construit la version prête à mettre en ligne dans le dossier dist/.

    python build-site.py

Étapes :
1. régénère en.html depuis index.html (build-en.py) ;
2. entoure index.html et en.html d'un document HTML complet avec un vrai <head> :
   description Google, aperçu de lien (Open Graph), favicon, langues, données structurées ;
3. copie la page légale et les images ;
4. écrit robots.txt et sitemap.xml pour Google.

Changez SITE_URL quand le nom de domaine définitif est réservé.
"""
import json
import runpy
import shutil
from pathlib import Path

SITE_URL = "https://vuupstudio.com"  # domaine acheté le 2026-10-08 chez Cloudflare
PHONE = "+212775767001"

# Mesure d'audience : laisser vide pour désactiver. Ces identifiants sont publics (visibles dans le code des pages).
GA4_ID = "G-76N589CXJ0"       # Google Analytics 4, ex. "G-ABC123XYZ"
CLARITY_ID = "yunskkfrkh"   # Microsoft Clarity, ex. "abcd1234ef"

# Profils officiels (Instagram, TikTok…) : Google les relie au site. À remplir quand les comptes existent.
SOCIAL_PROFILES = [
    "https://www.instagram.com/vuupstudio",
    "https://www.tiktok.com/@vuupstudio",
    "https://www.youtube.com/@VuupStudio",
]

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

PAGES = {
    "index.html": {
        "lang": "fr",
        "path": "/",
        "title": "Vuup Studio · Création de sites web sur mesure, maquette offerte",
        "description": "Sites web professionnels pour commerçants, indépendants et PME, au Maroc et partout ailleurs. "
                       "Hébergement, domaine, maintenance et référencement Google inclus. Devis gratuit sur WhatsApp.",
        "og_title": "Vuup Studio · Soyez vu, passez devant.",
        "og_description": "Sites web sur mesure, maquette offerte en 48h. Hébergement, domaine et maintenance inclus.",
        "locale": "fr_FR",
    },
    "en.html": {
        "lang": "en",
        "path": "/en",
        "title": "Vuup Studio · Custom websites, free mockup in 48h",
        "description": "Professional websites for shops, freelancers and small businesses, in Morocco and worldwide. "
                       "Hosting, domain, maintenance and Google SEO included. Free quote on WhatsApp.",
        "og_title": "Vuup Studio · Get seen, get ahead.",
        "og_description": "Custom websites, free mockup in 48h. Hosting, domain and maintenance included.",
        "locale": "en_US",
    },
}

# Reprend le petit reset que la plateforme d'aperçu ajoute automatiquement
BASE_STYLE = """<style>
  :root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
  body{margin:0;font:14px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#f6f5f2}
  img{max-width:100%}
  [hidden]{display:none!important}
</style>"""


def head(meta):
    url = SITE_URL + meta["path"]
    ld = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Vuup Studio",
        "alternateName": "Vuup",
        "url": SITE_URL + "/",
        "image": SITE_URL + "/og-image.png",
        "logo": SITE_URL + "/icon-512.png",
        "telephone": PHONE,
        "priceRange": "1500 - 6500 MAD",
        "areaServed": "Worldwide",
        "address": {"@type": "PostalAddress", "addressLocality": "Casablanca", "addressCountry": "MA"},
        "description": meta["description"],
    }
    if SOCIAL_PROFILES:
        ld["sameAs"] = SOCIAL_PROFILES
    # Indique à Google le nom à afficher pour le site dans les résultats
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "Vuup Studio",
               "alternateName": ["Vuup", "vuupstudio.com"], "url": SITE_URL + "/"}
    alt = "".join(
        f'<link rel="alternate" hreflang="{p["lang"]}" href="{SITE_URL}{p["path"]}">\n' for p in PAGES.values()
    )
    return f"""<!doctype html>
<html lang="{meta['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['description']}">
<link rel="canonical" href="{url}">
{alt}<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-512.png">
<meta name="theme-color" content="#ff5a36">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Vuup Studio">
<meta property="og:title" content="{meta['og_title']}">
<meta property="og:description" content="{meta['og_description']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{meta['locale']}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(site_ld, ensure_ascii=False)}</script>
{BASE_STYLE}
</head>
<body>
"""


def clean_links(html):
    """En ligne, Cloudflare sert les pages sans « .html » (/en, /legal) : on écrit directement ces adresses."""
    return (html.replace('href="index.html"', 'href="/"')
                .replace('href="en.html"', 'href="/en"')
                .replace('href="legal.html', 'href="/legal'))


def wrap(name, meta):
    src = (ROOT / name).read_text(encoding="utf-8")
    # le fichier source commence par son propre <title> : on le retire, le <head> en fournit un
    if src.startswith("<title>"):
        src = src[src.index("</title>") + len("</title>"):].lstrip("\n")
    (DIST / name).write_text(clean_links(head(meta) + src + "\n</body>\n</html>\n"), encoding="utf-8")


def main():
    runpy.run_path(str(ROOT / "build-en.py"), run_name="__main__")
    DIST.mkdir(exist_ok=True)
    for name, meta in PAGES.items():
        wrap(name, meta)
    for page in ("legal.html", "404.html"):  # 404.html : servie par Cloudflare Pages pour toute adresse inconnue
        (DIST / page).write_text(clean_links((ROOT / page).read_text(encoding="utf-8")), encoding="utf-8")
    for f in ("favicon.svg", "icon-512.png", "og-image.png"):
        shutil.copy2(ROOT / f, DIST / f)
    if GA4_ID or CLARITY_ID:
        # bandeau cookies : les outils de mesure ne se chargent qu'après l'accord du visiteur
        consent = ((ROOT / "assets-src" / "consent.html").read_text(encoding="utf-8")
                   .replace("{{GA4_ID}}", GA4_ID).replace("{{CLARITY_ID}}", CLARITY_ID))
        for page in ("index.html", "en.html", "legal.html", "404.html"):
            html = (DIST / page).read_text(encoding="utf-8")
            cut = html.rindex("</body>")
            (DIST / page).write_text(html[:cut] + consent + "\n" + html[cut:], encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    urls = "".join(
        f"  <url><loc>{SITE_URL}{p['path']}</loc>"
        + "".join(f'<xhtml:link rel="alternate" hreflang="{q["lang"]}" href="{SITE_URL}{q["path"]}"/>' for q in PAGES.values())
        + "</url>\n"
        for p in PAGES.values()
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + urls + "</urlset>\n",
        encoding="utf-8",
    )
    print("dist/ prêt :", ", ".join(sorted(p.name for p in DIST.iterdir())))


if __name__ == "__main__":
    main()
