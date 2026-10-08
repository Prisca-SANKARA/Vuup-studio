# Vuup Studio · Soyez vu, passez devant.

Site vitrine de **Vuup**, studio de création de sites web basé à Casablanca, pour les commerçants, indépendants et PME au Maroc, en Afrique et en Europe.

🌐 **En ligne :** [vuupstudio.com](https://vuupstudio.com)

![Aperçu de Vuup](og-image.png)

## Points forts

- **Identité sur mesure** : le logo est dessiné en SVG, et les deux « u » forment des yeux dont les pupilles suivent la souris.
- **Démo animée dans le hero** : une recherche Google se tape toute seule, et le site du client monte de la 4ᵉ à la 1ʳᵉ place, sur un fond « aurora » animé en Canvas.
- **Simulateur de prix** : pack + options + pages supplémentaires, avec un récapitulatif envoyé sur WhatsApp en un clic.
- **Convertisseur de devises** : DH, €, $ et FCFA, avec détection automatique selon le fuseau horaire du visiteur.
- **Bilingue FR / EN** : la version anglaise est générée automatiquement à partir de la version française.
- **Mode clair et sombre**, responsive, et respect de `prefers-reduced-motion`.
- **SEO** : balises Open Graph, données structurées JSON-LD (ProfessionalService), `hreflang`, `sitemap.xml` et `robots.txt`.
- **Sans framework ni dépendance** : HTML, CSS et JavaScript natifs, en un seul fichier par page.

## Structure

| Fichier | Rôle |
|---|---|
| `index.html` | Page principale (français), la source de vérité |
| `build-en.py` | Génère `en.html` à partir d'une table de traduction FR → EN. S'arrête si un texte français a changé sans traduction. |
| `build-site.py` | Construit `dist/` : ajoute le `<head>` complet (SEO, Open Graph, favicon), copie les fichiers, écrit `robots.txt` et `sitemap.xml` |
| `legal.html` | Mentions légales, politique de confidentialité, conditions de vente |
| `assets-src/` | Sources HTML de l'image de partage et de l'icône (rendues en PNG avec Edge en mode headless) |

## Construire en local

```bash
python build-site.py
```

Le site prêt à publier est généré dans `dist/`.

## Déploiement

Le site est hébergé sur **Cloudflare Pages**, relié à ce dépôt GitHub. Chaque `git push` sur `main` lance automatiquement le build (`python build-site.py`, dossier de sortie `dist`) et met le site en ligne.

---

© Vuup Studio · Casablanca
