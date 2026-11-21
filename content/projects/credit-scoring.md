---
title: Credit Default Scoring
date: 2025-03
category: academic
thumbnail: images/thumbnails/credit-scoring.svg
thumbnail_alt: Bar chart rising towards a dashed decision threshold
tags: [Python, LightGBM, SHAP, Imbalanced data]
summary: Predicting loan default on 300,000 applications, with an interpretable model a credit analyst can challenge.
featured: true
links:
  repo: https://github.com/example/credit-scoring
  report: files/cv-alex-martin.pdf
---
## Context

Team project (4 students) for the *Machine Learning* course. The dataset contains 300,000 anonymised loan applications with an 8% default rate.

## What I did

- Built the feature pipeline (missing values, target encoding, time-based split).
- Compared logistic regression, random forest and LightGBM with stratified cross-validation.
- Explained individual decisions with SHAP values for the final presentation.

## Results

| Model | AUC | Recall at 10% FPR |
|---|---|---|
| Logistic regression | 0.74 | 0.41 |
| LightGBM | **0.79** | **0.52** |

The final model was ranked 2nd out of 18 teams.
