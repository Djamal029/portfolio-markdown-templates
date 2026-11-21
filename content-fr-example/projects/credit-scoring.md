---
title: Scoring du défaut de crédit
date: 2025-03
category: academic
thumbnail: images/thumbnails/credit-scoring.svg
thumbnail_alt: Diagramme en barres croissant vers un seuil de décision en pointillés
tags: [Python, LightGBM, SHAP, Données déséquilibrées]
summary: Prédire le défaut de paiement sur 300 000 demandes de prêt, avec un modèle interprétable qu'un analyste crédit peut discuter.
featured: true
links:
  repo: https://github.com/example/credit-scoring
  report: files/cv-alex-martin.pdf
---
## Contexte

Projet en équipe (4 élèves) pour le cours de *Machine Learning*. Le jeu de données contient 300 000 demandes de prêt anonymisées, avec 8 % de défauts.

## Ma contribution

- Construction du pipeline de variables (valeurs manquantes, target encoding, découpage temporel).
- Comparaison régression logistique, forêt aléatoire et LightGBM en validation croisée stratifiée.
- Explication des décisions individuelles avec les valeurs SHAP pour la soutenance.

## Résultats

| Modèle | AUC | Rappel à 10 % de faux positifs |
|---|---|---|
| Régression logistique | 0,74 | 0,41 |
| LightGBM | **0,79** | **0,52** |

Le modèle final a été classé 2e sur 18 équipes.
