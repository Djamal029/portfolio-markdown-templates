---
title: Prévision de la consommation électrique régionale
date: 2024-12
category: academic
thumbnail: images/thumbnails/energy-forecast.svg
thumbnail_alt: Courbe d'une série temporelle saisonnière prolongée par une prévision en pointillés
tags: [R, SARIMA, Prophet, Séries temporelles]
summary: Prévisions à J+1 de la consommation d'électricité avec des modèles saisonniers, comparées à une référence naïve.
featured: true
links:
  repo: https://github.com/example/energy-forecast
---
Projet du cours de *Séries temporelles*, sur cinq ans de données publiques de consommation à la demi-heure.

- Décomposition de la série (saisonnalités journalière, hebdomadaire et annuelle).
- Ajustement de modèles SARIMA et Prophet avec la température comme variable externe.
- Erreur absolue moyenne en pourcentage ramenée de 6,1 % (naïf) à 2,8 %.
