---
title: Bike-sharing Live Dashboard
date: 2025-01
category: personal
thumbnail: images/thumbnails/bike-dashboard.svg
thumbnail_alt: Stylised city map grid with a route linking three stations
tags: [Python, Streamlit, Open data, API]
summary: A small Streamlit app that shows bike availability in Rennes and predicts which stations will be empty within the hour.
featured: true
links:
  repo: https://github.com/example/bike-dashboard
  demo: https://example.com/bike-dashboard
---
Built over a few weekends using the public open-data API.

- Collects station status every five minutes and stores it in SQLite.
- Simple logistic model to predict "empty within one hour" (precision 0.81).
- Deployed for free; around 40 visits a week from friends and classmates.
