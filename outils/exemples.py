# -*- coding: utf-8 -*-
"""Profils d'exemple de la galerie (--preview-all) : un profil fictif différent par modèle.

Ces profils servent uniquement à montrer les modèles en ligne. Votre propre site
n'utilise que le dossier content/ : vous n'avez pas besoin de toucher à ce fichier.
"""
from __future__ import annotations

import math
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Projets d'exemple (en plus des 5 projets du dossier content/)
# kind : dessin de la miniature (bars, line, km, network, grid, chat, dots, wave)
# ---------------------------------------------------------------------------
PROJECTS = {
    "survival-oncology": dict(kind="km", c=("#1e3a5f", "#2563eb"), date="2025-04", cat="academic", featured=True,
        tags=["R", "survival", "Cox model", "Kaplan-Meier"],
        en=("Survival Analysis of a Cancer Trial", "Kaplan-Meier curves and Cox models on a public oncology trial, with a clear check of the proportional hazards assumption.",
            ["Cleaned 1,200 patient records and handled censored follow-up.", "Fitted Cox models and tested proportional hazards with Schoenfeld residuals.", "Wrote a two-page summary a clinician can read in five minutes."]),
        fr=("Analyse de survie d'un essai en oncologie", "Courbes de Kaplan-Meier et modèles de Cox sur un essai public en oncologie, avec une vérification claire de l'hypothèse des risques proportionnels.",
            ["Nettoyé 1 200 dossiers patients et traité les suivis censurés.", "Ajusté des modèles de Cox et testé les risques proportionnels (résidus de Schoenfeld).", "Rédigé une synthèse de deux pages lisible en cinq minutes par un clinicien."])),
    "longitudinal-mixed": dict(kind="line", c=("#3b0764", "#7c3aed"), date="2024-12", cat="academic", featured=False,
        tags=["R", "lme4", "Mixed models"],
        en=("Growth Curves with Mixed Models", "Repeated measurements of children's growth modelled with random effects per child.",
            ["Compared random intercept and random slope models.", "Visualised individual trajectories against the population curve."]),
        fr=("Courbes de croissance et modèles mixtes", "Mesures répétées de la croissance d'enfants, modélisées avec des effets aléatoires par enfant.",
            ["Comparé modèles à intercept aléatoire et à pente aléatoire.", "Visualisé les trajectoires individuelles face à la courbe moyenne."])),
    "sample-size-app": dict(kind="bars", c=("#134e4a", "#0d9488"), date="2025-02", cat="personal", featured=False,
        tags=["R Shiny", "Power analysis"],
        en=("Sample Size Calculator for Trials", "A small Shiny app that computes the number of patients needed for common trial designs.",
            ["Implemented power formulas for means, proportions and survival endpoints.", "Checked every formula against published examples."]),
        fr=("Calculateur de taille d'échantillon", "Une petite application Shiny qui calcule le nombre de patients nécessaire pour les plans d'essai courants.",
            ["Implémenté les formules de puissance pour moyennes, proportions et survie.", "Vérifié chaque formule sur des exemples publiés."])),
    "churn-mlops": dict(kind="bars", c=("#7c2d12", "#ea580c"), date="2025-05", cat="personal", featured=True,
        tags=["Python", "MLflow", "Docker", "FastAPI"],
        en=("Churn Model, from Notebook to API", "A churn model packaged with MLflow and served behind a FastAPI endpoint, with automated tests.",
            ["Tracked every experiment and model version with MLflow.", "Served predictions through a Docker image and a FastAPI endpoint.", "Added a GitHub Actions pipeline that retrains and tests the model."]),
        fr=("Modèle de churn, du notebook à l'API", "Un modèle de churn suivi avec MLflow et servi derrière une API FastAPI, avec des tests automatiques.",
            ["Suivi de chaque expérience et version du modèle avec MLflow.", "Prédictions servies par une image Docker et une API FastAPI.", "Pipeline GitHub Actions qui réentraîne et teste le modèle."])),
    "image-defects": dict(kind="grid", c=("#0c4a6e", "#0284c7"), date="2025-03", cat="academic", featured=True,
        tags=["PyTorch", "CNN", "Transfer learning"],
        en=("Detecting Defects on Factory Images", "A convolutional network that flags faulty parts on production line photos.",
            ["Fine-tuned a pretrained ResNet on 6,000 labelled images.", "Used Grad-CAM to show which area of the image drives each decision."]),
        fr=("Détection de défauts sur images d'usine", "Un réseau convolutif qui repère les pièces défectueuses sur les photos d'une ligne de production.",
            ["Affiné un ResNet préentraîné sur 6 000 images annotées.", "Utilisé Grad-CAM pour montrer la zone de l'image qui guide chaque décision."])),
    "satellite-segmentation": dict(kind="grid", c=("#14532d", "#16a34a"), date="2024-11", cat="personal", featured=False,
        tags=["PyTorch", "U-Net", "Remote sensing"],
        en=("Mapping Fields from Satellite Images", "A U-Net that segments crop fields on open Sentinel-2 images.",
            ["Built tiles and masks from open data.", "Reached 0.81 IoU on held-out regions."]),
        fr=("Cartographier les champs par satellite", "Un U-Net qui segmente les parcelles agricoles sur des images Sentinel-2 ouvertes.",
            ["Construit les tuiles et les masques à partir de données ouvertes.", "Atteint un IoU de 0,81 sur des régions jamais vues."])),
    "model-compression": dict(kind="bars", c=("#312e81", "#4f46e5"), date="2025-01", cat="academic", featured=False,
        tags=["PyTorch", "Quantisation", "Edge AI"],
        en=("Making a Vision Model Fit on a Phone", "Pruning and quantisation of an image classifier, measured on accuracy and latency.",
            ["Cut model size by 4 with less than 1 point of accuracy lost.", "Benchmarked latency on a mid-range phone."]),
        fr=("Faire tenir un modèle de vision sur un téléphone", "Élagage et quantification d'un classifieur d'images, mesurés en précision et en latence.",
            ["Divisé la taille du modèle par 4 en perdant moins d'un point de précision.", "Mesuré la latence sur un téléphone milieu de gamme."])),
    "rag-assistant": dict(kind="chat", c=("#1e1b4b", "#6d28d9"), date="2025-04", cat="personal", featured=True,
        tags=["Python", "LLM", "RAG", "Embeddings"],
        en=("A Course Assistant with Retrieval", "A question-answering assistant that cites the course notes it uses, built with embeddings and an open LLM.",
            ["Indexed 400 pages of course notes with sentence embeddings.", "Measured answer faithfulness on 100 hand-written questions.", "Every answer links to the exact paragraph it comes from."]),
        fr=("Un assistant de cours avec recherche documentaire", "Un assistant de questions-réponses qui cite les notes de cours utilisées, construit avec des embeddings et un LLM ouvert.",
            ["Indexé 400 pages de notes de cours avec des embeddings de phrases.", "Mesuré la fidélité des réponses sur 100 questions rédigées à la main.", "Chaque réponse renvoie au paragraphe exact d'où elle vient."])),
    "llm-eval": dict(kind="bars", c=("#4a044e", "#c026d3"), date="2025-02", cat="academic", featured=False,
        tags=["LLM", "Evaluation", "Statistics"],
        en=("How Reliable Are LLM Judges?", "Comparing human and LLM ratings of summaries, with confidence intervals instead of single scores.",
            ["Collected 600 human ratings on 200 summaries.", "Estimated agreement with bootstrap confidence intervals."]),
        fr=("Les LLM juges sont-ils fiables ?", "Comparaison des notes humaines et des notes de LLM sur des résumés, avec des intervalles de confiance plutôt qu'un score unique.",
            ["Recueilli 600 notes humaines sur 200 résumés.", "Estimé l'accord avec des intervalles de confiance bootstrap."])),
    "speech-fr": dict(kind="wave", c=("#083344", "#0891b2"), date="2024-10", cat="personal", featured=False,
        tags=["Whisper", "Audio", "Python"],
        en=("Transcribing Lectures in French", "Speech-to-text for recorded lectures, with automatic chapters and keywords.",
            ["Compared three open speech models on 5 hours of lectures.", "Added chapter detection from the transcript."]),
        fr=("Transcrire des cours en français", "Transcription automatique de cours enregistrés, avec chapitres et mots-clés automatiques.",
            ["Comparé trois modèles de reconnaissance vocale sur 5 heures de cours.", "Ajouté un découpage en chapitres à partir de la transcription."])),
    "ab-testing": dict(kind="bars", c=("#7f1d1d", "#dc2626"), date="2025-03", cat="academic", featured=True,
        tags=["Python", "Bayesian", "A/B testing"],
        en=("Bayesian A/B Testing for a Shop", "Deciding between two page designs with a Bayesian model and an explicit decision rule.",
            ["Modelled conversion with Beta-Binomial posteriors.", "Simulated how long the test must run before deciding."]),
        fr=("Tests A/B bayésiens pour une boutique", "Choisir entre deux versions de page avec un modèle bayésien et une règle de décision explicite.",
            ["Modélisé la conversion avec des lois a posteriori Bêta-Binomiale.", "Simulé la durée nécessaire avant de décider."])),
    "customer-segmentation": dict(kind="dots", c=("#3f1d38", "#be185d"), date="2024-12", cat="personal", featured=False,
        tags=["Python", "Clustering", "RFM"],
        en=("Customer Segments that Marketing Can Use", "Clustering customers on purchase behaviour, then naming each segment with the marketing team.",
            ["Built RFM features from two years of orders.", "Chose the number of segments with stability checks, not only the elbow plot."]),
        fr=("Des segments clients utiles au marketing", "Regrouper les clients selon leurs achats, puis nommer chaque segment avec l'équipe marketing.",
            ["Construit des variables RFM sur deux ans de commandes.", "Choisi le nombre de segments par des tests de stabilité, pas seulement le coude."])),
    "airflow-pipeline": dict(kind="network", c=("#1c1917", "#57534e"), date="2025-04", cat="personal", featured=True,
        tags=["Airflow", "PostgreSQL", "dbt", "Docker"],
        en=("An Open Data Pipeline that Runs Itself", "Daily ingestion of public transport data with Airflow, tested with dbt and stored in PostgreSQL.",
            ["Scheduled extraction, cleaning and loading as one Airflow DAG.", "Added dbt tests that fail loudly when the source changes."]),
        fr=("Un pipeline de données ouvertes automatique", "Ingestion quotidienne de données de transport public avec Airflow, testée avec dbt et stockée dans PostgreSQL.",
            ["Planifié extraction, nettoyage et chargement dans un seul DAG Airflow.", "Ajouté des tests dbt qui alertent dès que la source change."])),
    "malaria-incidence": dict(kind="line", c=("#713f12", "#d97706"), date="2025-01", cat="academic", featured=True,
        tags=["R", "Count models", "Public health"],
        en=("Malaria Incidence after a Prevention Campaign", "Negative binomial models comparing villages with and without a prevention campaign.",
            ["Modelled weekly case counts with village random effects.", "Reported the incidence ratio with its uncertainty, all else being equal."]),
        fr=("Incidence du paludisme après une campagne de prévention", "Modèles binomiaux négatifs comparant des villages avec et sans campagne de prévention.",
            ["Modélisé les cas hebdomadaires avec des effets aléatoires par village.", "Présenté le rapport d'incidence avec son incertitude, toutes choses égales par ailleurs."])),
    "vaccination-dashboard": dict(kind="bars", c=("#064e3b", "#059669"), date="2024-11", cat="personal", featured=False,
        tags=["R Shiny", "Open data", "Maps"],
        en=("Vaccination Coverage Dashboard", "A Shiny dashboard of vaccination coverage by region, built on open health data.",
            ["Automated the monthly data refresh.", "Designed maps that stay readable in black and white."]),
        fr=("Tableau de bord de couverture vaccinale", "Un tableau de bord Shiny de la couverture vaccinale par région, construit sur des données de santé ouvertes.",
            ["Automatisé la mise à jour mensuelle des données.", "Conçu des cartes lisibles même en noir et blanc."])),
    "sentiment-reviews": dict(kind="chat", c=("#164e63", "#0e7490"), date="2025-02", cat="academic", featured=True,
        tags=["Python", "Transformers", "NLP"],
        en=("What Do Reviews Really Say?", "Aspect-based sentiment analysis of 50,000 French product reviews with a fine-tuned CamemBERT.",
            ["Annotated 2,000 reviews to fine-tune and evaluate the model.", "Showed which product aspects drive negative reviews."]),
        fr=("Que disent vraiment les avis clients ?", "Analyse de sentiment par aspect sur 50 000 avis produits en français, avec un CamemBERT affiné.",
            ["Annoté 2 000 avis pour affiner et évaluer le modèle.", "Montré quels aspects des produits expliquent les avis négatifs."])),
    "topic-press": dict(kind="dots", c=("#422006", "#a16207"), date="2024-10", cat="personal", featured=False,
        tags=["Python", "BERTopic", "Text mining"],
        en=("Twenty Years of Press Topics", "Topic modelling of 80,000 newspaper articles to see how subjects rise and fade.",
            ["Compared LDA and BERTopic on topic coherence.", "Plotted topic trends over time with clear labels."]),
        fr=("Vingt ans de sujets dans la presse", "Modélisation thématique de 80 000 articles de presse pour voir les sujets monter et disparaître.",
            ["Comparé LDA et BERTopic sur la cohérence des thèmes.", "Tracé l'évolution des thèmes dans le temps avec des libellés clairs."])),
}

# ---------------------------------------------------------------------------
# Les huit profils (un par modèle)
# ---------------------------------------------------------------------------
def _exp(title_en, title_fr, org, loc, start, end, etype, tags, en, fr):
    return dict(title=(title_en, title_fr), org=org, loc=loc, start=start, end=end, type=etype, tags=tags, en=en, fr=fr)


PERSONAS = {
    "a": dict(name="Léa Moreau", city="Lyon, France", colors=("#0f766e", "#b45309"),
        headline=("Biostatistics Student, Clinical Trials and Survival Analysis", "Étudiante en biostatistique, essais cliniques et analyse de survie"),
        pitch=("Biostatistics student, I turn clinical data into results that doctors can trust. I am looking for a **6-month internship in biostatistics**.",
               "Étudiante en biostatistique, je transforme des données cliniques en résultats fiables pour les médecins. Je cherche un **stage de 6 mois en biostatistique**."),
        avail=("Available from April 2027 for a 6-month internship", "Disponible dès avril 2027 pour un stage de 6 mois"),
        about=(["A summer job in a hospital lab made me curious about one question: does this treatment really work?",
                "I now focus on **survival analysis**, **mixed models** and trial design, and I care about explaining results to clinicians."],
               ["Un job d'été dans un laboratoire hospitalier m'a rendue curieuse d'une question : ce traitement marche-t-il vraiment ?",
                "Je me concentre aujourd'hui sur l'**analyse de survie**, les **modèles mixtes** et la conception d'essais, en tenant à expliquer les résultats aux cliniciens."]),
        skills=[("Programming", "Programmation", [("R", 5), ("SAS", 3), ("Python", 4), ("SQL", 3)]),
                ("Biostatistics", "Biostatistique", ["Survival analysis", "Mixed models", "Trial design", "Missing data"]),
                ("Languages", "Langues", ["French (native)", "English (C1)"])],
        exps=[_exp("Biostatistics Intern", "Stagiaire en biostatistique", "Clinova Research", "Lyon, France", "2025-06", "2025-09", "internship", ["R", "SAS", "Clinical trials"],
                   ["Wrote the statistical analysis plan section on missing data.", "Programmed safety tables for a phase II trial."],
                   ["Rédigé la partie données manquantes du plan d'analyse statistique.", "Programmé les tableaux de tolérance d'un essai de phase II."]),
              _exp("Teaching Assistant in Statistics", "Monitrice en statistique", "Université Lyon 1", "Lyon, France", "2024-09", "", "job", ["Teaching", "R"],
                   ["Run weekly R practicals for 30 first-year students."], ["J'anime chaque semaine des TP de R pour 30 étudiants de première année."])],
        projects=["survival-oncology", "longitudinal-mixed", "sample-size-app", "survey-sampling"]),
    "b": dict(name="Yanis Benali", city="Paris, France", colors=("#4f46e5", "#be185d"),
        headline=("Machine Learning Student, from Notebooks to Production", "Étudiant en machine learning, du notebook à la production"),
        pitch=("I build machine learning models and the code around them: tests, APIs, monitoring. I am looking for a **machine learning engineering internship**.",
               "Je construis des modèles de machine learning et le code autour : tests, API, suivi. Je cherche un **stage d'ingénieur machine learning**."),
        avail=("Available from February 2027", "Disponible dès février 2027"),
        about=(["I started with Kaggle competitions and quickly realised that a model is only useful once someone can call it.",
                "Since then I enjoy the whole path: **feature engineering**, **model evaluation**, then packaging and deployment."],
               ["J'ai commencé par des compétitions Kaggle et compris vite qu'un modèle n'est utile que si quelqu'un peut l'appeler.",
                "Depuis, j'aime tout le chemin : **préparation des variables**, **évaluation des modèles**, puis mise en production."]),
        skills=[("Programming", "Programmation", [("Python", 5), ("SQL", 4), ("Git", 4), ("Docker", 3)]),
                ("Machine learning", "Machine learning", ["Gradient boosting", "Deep learning", "MLflow", "FastAPI"]),
                ("Languages", "Langues", ["French (native)", "Arabic (native)", "English (C1)"])],
        exps=[_exp("Machine Learning Intern", "Stagiaire machine learning", "Northwind Analytics", "Paris, France", "2025-06", "2025-08", "internship", ["Python", "MLflow", "Docker"],
                   ["Moved a churn model from a notebook to a tested API.", "Cut the retraining time from a day to 40 minutes."],
                   ["Passé un modèle de churn d'un notebook à une API testée.", "Réduit le temps de réentraînement d'une journée à 40 minutes."]),
              _exp("Data Analyst (part-time)", "Analyste de données (temps partiel)", "Cityflow Mobility", "Paris, France", "2024-10", "", "job", ["SQL", "Dashboards"],
                   ["Maintain weekly dashboards used by three city operators."], ["Je maintiens des tableaux de bord hebdomadaires utilisés par trois opérateurs."])],
        projects=["churn-mlops", "credit-scoring", "image-defects", "recipe-recommender", "bike-dashboard"]),
    "c": dict(name="Hugo Lambert", city="Nantes, France", colors=("#1e293b", "#0e7490"),
        headline=("Data Engineering Student, Pipelines and Dashboards", "Étudiant en data engineering, pipelines et tableaux de bord"),
        pitch=("I make data arrive on time, clean and documented. I am looking for a **data engineering apprenticeship**.",
               "Je fais en sorte que les données arrivent à l'heure, propres et documentées. Je cherche une **alternance en data engineering**."),
        avail=("Apprenticeship from September 2026", "Alternance dès septembre 2026"),
        about=(["I like systems that run quietly every night without anyone noticing.",
                "My favourite tools are **SQL**, **Airflow** and **dbt**, and I write tests before I trust any table."],
               ["J'aime les systèmes qui tournent chaque nuit sans que personne ne s'en rende compte.",
                "Mes outils préférés sont **SQL**, **Airflow** et **dbt**, et j'écris des tests avant de faire confiance à une table."]),
        skills=[("Programming", "Programmation", [("SQL", 5), ("Python", 4), ("Bash", 3), ("Git", 4)]),
                ("Data engineering", "Data engineering", ["Airflow", "dbt", "PostgreSQL", "Docker"]),
                ("Languages", "Langues", ["French (native)", "English (B2)"])],
        exps=[_exp("Data Engineer Intern", "Stagiaire data engineer", "Cityflow Mobility", "Nantes, France", "2025-05", "2025-08", "internship", ["Airflow", "PostgreSQL"],
                   ["Rebuilt the nightly ingestion of 40 data sources.", "Added data quality alerts that caught three silent failures."],
                   ["Reconstruit l'ingestion nocturne de 40 sources de données.", "Ajouté des alertes qualité qui ont repéré trois pannes silencieuses."]),
              _exp("Volunteer, Open Data Club", "Bénévole, club open data", "Data For Good Nantes", "Nantes, France", "2024-01", "", "volunteering", ["Open data"],
                   ["Help associations publish clean open datasets."], ["J'aide des associations à publier des jeux de données ouverts propres."])],
        projects=["airflow-pipeline", "bike-dashboard", "energy-forecast", "vaccination-dashboard"]),
    "d": dict(name="Karim Diallo", city="Toulouse, France", colors=("#4f46e5", "#be185d"),
        headline=("AI Student, Language Models and Retrieval", "Étudiant en IA, modèles de langage et recherche documentaire"),
        pitch=("I build assistants based on language models, and I measure when they are wrong. I am looking for an **internship in applied AI**.",
               "Je construis des assistants à base de modèles de langage, et je mesure quand ils se trompent. Je cherche un **stage en IA appliquée**."),
        avail=("Available from April 2027 for 6 months", "Disponible dès avril 2027 pour 6 mois"),
        about=(["Language models fascinate me, and so do their mistakes.",
                "I work on **retrieval-augmented generation**, **evaluation** and speech, always with a statistician's eye on uncertainty."],
               ["Les modèles de langage me passionnent, et leurs erreurs aussi.",
                "Je travaille sur la **génération augmentée par recherche**, l'**évaluation** et la parole, avec un regard de statisticien sur l'incertitude."]),
        skills=[("Programming", "Programmation", [("Python", 5), ("PyTorch", 4), ("SQL", 3), ("Git", 4)]),
                ("AI", "IA", ["LLM", "RAG", "Embeddings", "Speech recognition", "Evaluation"]),
                ("Languages", "Langues", ["French (native)", "English (C1)", "Wolof (native)"])],
        exps=[_exp("AI Research Intern", "Stagiaire en recherche IA", "Lumen AI Lab", "Toulouse, France", "2025-06", "2025-09", "internship", ["LLM", "Python"],
                   ["Built an evaluation set of 500 questions for a legal assistant.", "Reduced hallucinated citations by 35%."],
                   ["Construit un jeu d'évaluation de 500 questions pour un assistant juridique.", "Réduit de 35 % les citations inventées."]),
              _exp("Mentor, AI Student Club", "Mentor, club étudiant d'IA", "ENSEEIHT AI Club", "Toulouse, France", "2024-09", "", "volunteering", ["Teaching"],
                   ["Run monthly workshops on language models."], ["J'anime chaque mois des ateliers sur les modèles de langage."])],
        projects=["rag-assistant", "llm-eval", "speech-fr", "sentiment-reviews", "topic-press"]),
    "e": dict(name="Camille Laurent", city="Bordeaux, France", colors=("#c2410c", "#7c3aed"),
        headline=("Data Science Student, Recommendation and Experimentation", "Étudiante en data science, recommandation et expérimentation"),
        pitch=("I help products make better decisions with data: recommendations, A/B tests and clear dashboards. I am looking for a **data science internship**.",
               "J'aide les produits à mieux décider grâce aux données : recommandations, tests A/B et tableaux de bord clairs. Je cherche un **stage en data science**."),
        avail=("Available from April 2027", "Disponible dès avril 2027"),
        about=(["I came to data science through marketing, wondering why some customers come back and others never do.",
                "I enjoy **recommender systems**, **Bayesian A/B testing** and turning results into decisions."],
               ["Je suis arrivée à la data science par le marketing, en me demandant pourquoi certains clients reviennent et d'autres jamais.",
                "J'aime les **systèmes de recommandation**, les **tests A/B bayésiens** et transformer les résultats en décisions."]),
        skills=[("Programming", "Programmation", [("Python", 5), ("SQL", 4), ("R", 3), ("Git", 3)]),
                ("Data science", "Data science", ["Recommender systems", "A/B testing", "Clustering", "Bayesian statistics"]),
                ("Languages", "Langues", ["French (native)", "English (C1)", "Italian (B2)"])],
        exps=[_exp("Data Science Intern", "Stagiaire data science", "Maison Verte", "Bordeaux, France", "2025-06", "2025-08", "internship", ["Python", "A/B testing"],
                   ["Designed and analysed four A/B tests on the online shop.", "Built a product recommendation model now used in emails."],
                   ["Conçu et analysé quatre tests A/B sur la boutique en ligne.", "Construit un modèle de recommandation utilisé dans les e-mails."]),
              _exp("Marketing Assistant", "Assistante marketing", "Studio Lumière", "Bordeaux, France", "2023-07", "2023-12", "job", ["Excel", "Surveys"],
                   ["Ran customer surveys and summarised them for the team."], ["Mené des enquêtes clients et synthétisé les résultats pour l'équipe."])],
        projects=["recipe-recommender", "ab-testing", "customer-segmentation", "survey-sampling", "credit-scoring"]),
    "f": dict(name="Thomas Petit", city="Grenoble, France", colors=("#1e293b", "#0e7490"),
        headline=("Machine Learning Student, Computer Vision", "Étudiant en machine learning, vision par ordinateur"),
        pitch=("I teach computers to see: detection, segmentation and models small enough for real devices. I am looking for a **computer vision internship**.",
               "J'apprends aux ordinateurs à voir : détection, segmentation et modèles assez légers pour de vrais appareils. Je cherche un **stage en vision par ordinateur**."),
        avail=("Available from March 2027", "Disponible dès mars 2027"),
        about=(["I built my first image classifier to sort my holiday photos, and never stopped.",
                "I work with **PyTorch** on **detection**, **segmentation** and **model compression**."],
               ["J'ai construit mon premier classifieur d'images pour trier mes photos de vacances, et je n'ai jamais arrêté.",
                "Je travaille avec **PyTorch** sur la **détection**, la **segmentation** et la **compression de modèles**."]),
        skills=[("Programming", "Programmation", [("Python", 5), ("PyTorch", 5), ("C++", 3), ("Linux", 4)]),
                ("Computer vision", "Vision par ordinateur", ["CNN", "U-Net", "Object detection", "Quantisation"]),
                ("Languages", "Langues", ["French (native)", "English (C1)", "German (B1)"])],
        exps=[_exp("Computer Vision Intern", "Stagiaire en vision par ordinateur", "Optiq Industries", "Grenoble, France", "2025-06", "2025-09", "internship", ["PyTorch", "Edge AI"],
                   ["Deployed a defect detector on an embedded camera.", "Halved inference time with quantisation."],
                   ["Déployé un détecteur de défauts sur une caméra embarquée.", "Divisé par deux le temps d'inférence par quantification."]),
              _exp("Robotics Club Lead", "Responsable du club robotique", "Grenoble INP Robotics", "Grenoble, France", "2024-09", "", "volunteering", ["ROS", "Teamwork"],
                   ["Lead a team of 12 students building a vision-guided robot."], ["J'encadre 12 étudiants qui construisent un robot guidé par la vision."])],
        projects=["image-defects", "satellite-segmentation", "model-compression", "energy-forecast"]),
    "g": dict(name="Aïcha Traoré", city="Rennes, France", colors=("#0f766e", "#b45309"),
        headline=("Public Health Data Analyst, Epidemiology and Surveys", "Analyste de données en santé publique, épidémiologie et enquêtes"),
        pitch=("I analyse health data to help programmes reach the people who need them. I am looking for a **position in epidemiology or public health statistics**.",
               "J'analyse des données de santé pour aider les programmes à atteindre ceux qui en ont besoin. Je cherche un **poste en épidémiologie ou statistique de santé publique**."),
        avail=("Available from September 2027", "Disponible dès septembre 2027"),
        about=(["I grew up close to a health centre and saw how much good data can change a vaccination campaign.",
                "I specialise in **count models**, **survey sampling** and **survival analysis** applied to public health."],
               ["J'ai grandi près d'un centre de santé et j'ai vu à quel point de bonnes données changent une campagne de vaccination.",
                "Je me spécialise dans les **modèles de comptage**, les **sondages** et l'**analyse de survie** appliqués à la santé publique."]),
        skills=[("Programming", "Programmation", [("R", 5), ("Stata", 4), ("Python", 3), ("SQL", 3)]),
                ("Epidemiology", "Épidémiologie", ["Count models", "Survey sampling", "Survival analysis", "Mixed models"]),
                ("Languages", "Langues", ["French (native)", "English (C1)", "Bambara (native)"])],
        exps=[_exp("Epidemiology Intern", "Stagiaire en épidémiologie", "Institut de Santé Ouest", "Rennes, France", "2025-06", "2025-09", "internship", ["R", "Public health"],
                   ["Evaluated a malaria prevention campaign with count models.", "Presented results to the programme team and its funders."],
                   ["Évalué une campagne de prévention du paludisme avec des modèles de comptage.", "Présenté les résultats à l'équipe du programme et à ses financeurs."]),
              _exp("Survey Interviewer", "Enquêtrice", "Observatoire Régional de Santé", "Rennes, France", "2024-06", "2024-08", "job", ["Surveys"],
                   ["Conducted 150 face-to-face health interviews."], ["Mené 150 entretiens de santé en face à face."])],
        projects=["malaria-incidence", "survey-sampling", "vaccination-dashboard", "survival-oncology"]),
    "h": dict(name="Inès Roussel", city="Lille, France", colors=("#4f46e5", "#be185d"),
        headline=("Data Science Student, Natural Language Processing", "Étudiante en data science, traitement automatique du langage"),
        pitch=("I make sense of large amounts of text: reviews, articles, conversations. I am looking for an **NLP internship**.",
               "Je donne du sens à de grandes quantités de texte : avis, articles, conversations. Je cherche un **stage en traitement du langage**."),
        avail=("Available from April 2027", "Disponible dès avril 2027"),
        about=(["Literature first, statistics second: I love words, and I love counting them even more.",
                "I work on **sentiment analysis**, **topic modelling** and **language models**, in French and English."],
               ["La littérature d'abord, la statistique ensuite : j'aime les mots, et encore plus les compter.",
                "Je travaille sur l'**analyse de sentiment**, la **modélisation thématique** et les **modèles de langage**, en français et en anglais."]),
        skills=[("Programming", "Programmation", [("Python", 5), ("SQL", 3), ("R", 3), ("Git", 4)]),
                ("NLP", "Traitement du langage", ["Transformers", "Topic modelling", "Sentiment analysis", "LLM"]),
                ("Languages", "Langues", ["French (native)", "English (C1)", "Spanish (B2)"])],
        exps=[_exp("NLP Intern", "Stagiaire en traitement du langage", "Verbatim Analytics", "Lille, France", "2025-06", "2025-09", "internship", ["Transformers", "Python"],
                   ["Classified 200,000 customer messages by topic and urgency.", "Built a monitoring dashboard for the support team."],
                   ["Classé 200 000 messages clients par thème et urgence.", "Construit un tableau de bord de suivi pour le service client."]),
              _exp("Editor, Student Newspaper", "Rédactrice, journal étudiant", "La Plume ENSAI", "Bruz, France", "2023-09", "", "volunteering", ["Writing"],
                   ["Write a monthly column explaining statistics in the news."], ["J'écris une chronique mensuelle qui explique les statistiques de l'actualité."])],
        projects=["sentiment-reviews", "topic-press", "rag-assistant", "llm-eval"]),
}


# ---------------------------------------------------------------------------
# Dessins (miniatures de projets et avatars)
# ---------------------------------------------------------------------------
def _thumb(kind: str, c1: str, c2: str, seed: int) -> str:
    W, H = 1200, 675
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>',
           f'<rect width="{W}" height="{H}" fill="url(#g)"/>']
    ink, gold = "rgba(255,255,255,.85)", "#fde68a"
    if kind == "bars":
        for k in range(10):
            h = 120 + 34 * k + 40 * math.sin(k * 1.3 + seed)
            out.append(f'<rect x="{180 + k * 85}" y="{560 - h:.0f}" width="56" height="{h:.0f}" rx="6" fill="{ink}" opacity="{0.45 + 0.05 * k:.2f}"/>')
        out.append(f'<line x1="150" y1="330" x2="1050" y2="330" stroke="{gold}" stroke-width="5" stroke-dasharray="16 12"/>')
    elif kind in ("line", "wave"):
        pts = " ".join(f"{100 + x * 10},{337 + (90 if kind == 'line' else 150) * math.sin(x / (9 if kind == 'line' else 3.2) + seed) * (0.6 + 0.4 * math.cos(x / 23)) - (x * 1.2 if kind == 'line' else 0):.0f}" for x in range(101))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{gold}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>')
        out.append(f'<line x1="100" y1="560" x2="1100" y2="560" stroke="{ink}" stroke-width="3" opacity=".5"/>')
    elif kind == "km":
        for arm, (col, rate) in enumerate([(gold, 0.018), (ink, 0.03)]):
            y, x, d = 140.0, 120, f"M120 140"
            while x < 1080:
                x += 40 + (arm * 13 + x) % 50
                d += f" H{x} V{y:.0f}"
                y += (560 - y) * rate * 6
            out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="7"/>')
        out.append(f'<line x1="120" y1="600" x2="1100" y2="600" stroke="{ink}" stroke-width="3" opacity=".5"/>')
    elif kind == "network":
        import random
        r = random.Random(seed)
        nodes = [(r.randint(160, 1040), r.randint(120, 560)) for _ in range(11)]
        for i, (x, y) in enumerate(nodes):
            for j in range(i + 1, len(nodes)):
                if (i * 7 + j * 3) % 4 == 0:
                    out.append(f'<line x1="{x}" y1="{y}" x2="{nodes[j][0]}" y2="{nodes[j][1]}" stroke="{ink}" stroke-width="3" opacity=".55"/>')
        for i, (x, y) in enumerate(nodes):
            out.append(f'<circle cx="{x}" cy="{y}" r="{16 if i % 3 else 22}" fill="{gold if i % 3 == 0 else "#fff"}"/>')
    elif kind == "grid":
        for i in range(4):
            for j in range(3):
                on = (i + j + seed) % 3 == 0
                out.append(f'<rect x="{230 + i * 190}" y="{110 + j * 160}" width="160" height="130" rx="12" fill="{ink}" opacity="{0.9 if on else 0.35}"/>')
                if on:
                    out.append(f'<rect x="{226 + i * 190}" y="{106 + j * 160}" width="168" height="138" rx="14" fill="none" stroke="{gold}" stroke-width="6"/>')
    elif kind == "chat":
        for k, (x, w, right) in enumerate([(200, 520, False), (480, 520, True), (200, 600, False), (560, 440, True)]):
            y = 110 + k * 125
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="90" rx="40" fill="{gold if right else ink}" opacity="{0.95 if right else 0.8}"/>')
            for m in range(3):
                out.append(f'<rect x="{x + 40}" y="{y + 26 + m * 16}" width="{w - 80 - m * 90}" height="8" rx="4" fill="{c1}" opacity=".45"/>')
    else:  # dots
        for i in range(24):
            for j in range(10):
                on = math.sin(i * 0.7 + seed) * math.cos(j * 0.9) > 0.35
                out.append(f'<circle cx="{170 + i * 37}" cy="{170 + j * 37}" r="{9 if on else 6}" fill="{gold if on else ink}" opacity="{1 if on else 0.5}"/>')
    out.append("</svg>")
    return "\n".join(out)


def _avatar(name: str, c1: str, c2: str) -> str:
    initials = "".join(p[0] for p in name.split()[:2]).upper()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">'
            f'<defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            f'<rect width="400" height="400" fill="url(#a)"/>'
            f'<circle cx="200" cy="160" r="70" fill="rgba(255,255,255,.28)"/><path d="M70 400c10-90 70-140 130-140s120 50 130 140z" fill="rgba(255,255,255,.28)"/>'
            f'<text x="200" y="372" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="56" font-weight="700" fill="#fff" opacity=".9">{initials}</text></svg>')


def _q(text: str) -> str:
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ---------------------------------------------------------------------------
# Construction d'un dossier de contenu pour un modèle et une langue
# ---------------------------------------------------------------------------
def make_content(template: str, lang: str, base: Path, dest: Path) -> Path:
    """Copie le contenu de base puis le remplace par le profil d'exemple du modèle."""
    p = PERSONAS[template]
    k = 0 if lang == "en" else 1
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(base, dest)
    slug_name = p["name"].lower().replace(" ", ".").replace("ï", "i").replace("é", "e").replace("è", "e")
    (dest / "images" / "persona.svg").write_text(_avatar(p["name"], *p["colors"]), encoding="utf-8")
    profile = (dest / "profile.md").read_text(encoding="utf-8")
    head, _, _ = profile.partition("\n---\n")
    lines = []
    for line in head.splitlines():
        key = line.split(":", 1)[0].strip()
        if key == "name": line = f"name: {_q(p['name'])}"
        elif key == "headline": line = f"headline: {_q(p['headline'][k])}"
        elif key == "location": line = f"location: {_q(p['city'])}"
        elif key == "availability": line = f"availability: {_q(p['avail'][k])}"
        elif key == "email": line = f"email: {slug_name}@example.com"
        elif key == "photo": line = "photo: images/persona.svg"
        elif key == "photo_alt": line = f"photo_alt: {_q(('Illustrated portrait of ' if k == 0 else 'Portrait illustré de ') + p['name'])}"
        lines.append(line)
    (dest / "profile.md").write_text("\n".join(lines) + "\n---\n" + p["pitch"][k] + "\n", encoding="utf-8")
    about = p["about"][k]
    extra = ("Outside the classroom, I share what I learn through talks and student projects." if k == 0
             else "En dehors des cours, je partage ce que j'apprends dans des présentations et des projets étudiants.")
    (dest / "about.md").write_text("\n\n".join(about + [extra]) + "\n", encoding="utf-8")
    sk = ["---", "groups:"]
    for g_en, g_fr, items in p["skills"]:
        sk.append(f"  - name: {_q(g_en if k == 0 else g_fr)}")
        if items and isinstance(items[0], tuple):
            sk.append("    items:")
            for name, level in items:
                sk += [f"      - name: {_q(name)}", f"        level: {level}"]
        else:
            sk.append("    items: [" + ", ".join(_q(i) for i in items) + "]")
    sk.append("---")
    (dest / "skills.md").write_text("\n".join(sk) + "\n", encoding="utf-8")
    # experiences
    exp_dir = dest / "experiences"
    shutil.rmtree(exp_dir)
    exp_dir.mkdir()
    for n, e in enumerate(p["exps"]):
        body = "\n".join("- " + b for b in (e["en"] if k == 0 else e["fr"]))
        fm = [f"title: {_q(e['title'][k])}", f"organisation: {_q(e['org'])}", f"location: {_q(e['loc'])}",
              f"start: {e['start']}", f"end: {e['end'] or 'present'}", f"type: {e['type']}", "tags: [" + ", ".join(_q(t) for t in e["tags"]) + "]"]
        (exp_dir / f"exp-{n + 1}.md").write_text("---\n" + "\n".join(fm) + "\n---\n" + body + "\n", encoding="utf-8")
    # projects: keep the chosen base projects, add the chosen pool projects
    proj_dir = dest / "projects"
    for f in proj_dir.glob("*.md"):
        if f.stem not in p["projects"]:
            f.unlink()
    thumbs = dest / "images" / "thumbnails"
    for n, slug in enumerate(p["projects"]):
        if slug not in PROJECTS:
            continue
        d = PROJECTS[slug]
        title, summary, bullets = d["en"] if k == 0 else d["fr"]
        (thumbs / f"{slug}.svg").write_text(_thumb(d["kind"], *d["c"], seed=n + len(slug)), encoding="utf-8")
        what = "## What I did" if k == 0 else "## Ce que j'ai fait"
        fm = [f"title: {_q(title)}", f"date: {d['date']}", f"category: {d['cat']}", f"thumbnail: images/thumbnails/{slug}.svg",
              f"thumbnail_alt: {_q(title)}", "tags: [" + ", ".join(_q(t) for t in d["tags"]) + "]", f"summary: {_q(summary)}",
              f"featured: {'true' if d['featured'] else 'false'}", "links:", f"  repo: https://github.com/example/{slug}"]
        (proj_dir / f"{slug}.md").write_text("---\n" + "\n".join(fm) + "\n---\n" + what + "\n\n" + "\n".join("- " + b for b in bullets) + "\n", encoding="utf-8")
    return dest


# Profils des modeles I et J (fichier separe pour rester lisible)
try:
    import exemples_ij  # noqa: F401
except ImportError:
    pass

try:
    import exemples_ko  # noqa: F401
except ImportError:
    pass

try:
    import exemples_py  # noqa: F401
except ImportError:
    pass

try:
    import exemples_zad  # noqa: F401
except ImportError:
    pass
