---
title: Tableau de bord des vélos en libre-service
date: 2025-01
category: personal
thumbnail: images/thumbnails/bike-dashboard.svg
thumbnail_alt: Plan de ville stylisé avec un trajet reliant trois stations
tags: [Python, Streamlit, Open data, API]
summary: Une petite application Streamlit qui affiche les vélos disponibles à Rennes et prédit les stations qui seront vides dans l'heure.
featured: true
links:
  repo: https://github.com/example/bike-dashboard
  demo: https://example.com/bike-dashboard
---
Réalisé en quelques week-ends à partir de l'API open data publique.

- Collecte de l'état des stations toutes les cinq minutes, stocké dans SQLite.
- Modèle logistique simple pour prédire « vide dans l'heure » (précision 0,81).
- Déployé gratuitement ; environ 40 visites par semaine d'amis et de camarades.
