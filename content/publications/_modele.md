---
# Modèle de publication, pour les modèles « chercheur » (ra à rj).
# Ce fichier est ignoré parce que son nom commence par « _ ».
# Copiez-le, renommez-le (par exemple 2026-joint-models.md) et remplacez les valeurs.
title: "Titre exact de l'article"
authors: [Prénom Nom, Co-autrice Une, Co-auteur Deux]   # votre nom sera mis en gras
year: 2026
venue: "Nom de la revue ou de la conférence"
type: journal        # journal, conference, preprint, workshop, thesis, book, chapter, report, talk, poster
status: ""           # facultatif, par exemple "Under review" ou "Accepté"
award: ""            # facultatif, par exemple "Best paper award"
summary: "Une phrase simple qui dit ce que l'article apporte."
featured: true       # mis en avant
doi: 10.xxxx/xxxxx   # facultatif : crée un bouton DOI
links:
  paper: https://...           # page de l'article
  pdf: files/mon-article.pdf   # PDF local (dans content/files/) ou adresse https://
  code: https://github.com/...
  slides: ""
  # aussi possibles : arxiv, hal, data, poster, video
bibtex: |
  @article{nom2026,
    title = {Titre exact de l'article},
    author = {Nom, Prénom and Une, Co-autrice},
    journal = {Nom de la revue},
    year = {2026}
  }
---
Le résumé (abstract) de l'article, en quelques phrases. Il s'affiche dans un encadré
qu'on déplie avec le bouton « Résumé ».
