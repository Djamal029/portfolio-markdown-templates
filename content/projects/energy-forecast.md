---
title: Forecasting Regional Electricity Demand
date: 2024-12
category: academic
thumbnail: images/thumbnails/energy-forecast.svg
thumbnail_alt: Line chart of a seasonal time series with a dashed forecast
tags: [R, SARIMA, Prophet, Time series]
summary: Day-ahead forecasts of electricity demand with seasonal models, compared against a naive benchmark.
featured: true
links:
  repo: https://github.com/example/energy-forecast
---
Project for the *Time Series* course, using five years of half-hourly public consumption data.

- Decomposed the series (daily, weekly and yearly seasonality).
- Fitted SARIMA and Prophet models with temperature as an external regressor.
- Reduced the mean absolute percentage error from 6.1% (naive) to 2.8%.
