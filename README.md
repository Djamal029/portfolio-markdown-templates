# Portfolio Markdown : huit modèles prêts à l'emploi

Créez votre site portfolio **sans écrire de HTML**. Vous remplissez quelques fichiers texte (Markdown), un script fabrique le site, et GitHub Pages le publie gratuitement.

Trois modèles visuels sont fournis, avec **le même contenu** : vous passez de l'un à l'autre en changeant une seule ligne. Couleurs, polices, langue (français ou anglais) et sections se règlent dans un seul fichier.

> Une version mise en page de ce guide, avec sommaire, est disponible dans **README.html** (ouvrez-le dans votre navigateur).

---

## Sommaire

1. [Les huit modèles](#1-les-huit-modèles)
2. [Démarrage rapide (5 minutes)](#2-démarrage-rapide-5-minutes)
3. [Ce qu'il faut modifier](#3-ce-quil-faut-modifier)
4. [Référence des fichiers, champ par champ](#4-référence-des-fichiers-champ-par-champ)
5. [Couleurs et polices](#5-couleurs-et-polices)
6. [Tâches courantes](#6-tâches-courantes)
7. [Voir le site sur son ordinateur](#7-voir-le-site-sur-son-ordinateur)
8. [Publier sur GitHub Pages](#8-publier-sur-github-pages)
9. [FAQ](#9-faq)

---

## 1. Les huit modèles

**Voir les huit modèles en ligne, avec une courte animation explicative :** https://djamal029.github.io/portfolio-markdown-templates/ . Le bouton « Choisir ce modèle » compte combien de personnes ont choisi chaque modèle et mène au dépôt GitHub.

| | Modèle A « Editorial » | Modèle B « Cards » | Modèle C « Sidebar » | Modèle D « Bento » | Modèle E « Spotlight » | Modèle F « Terminal » | Modèle G « Resume » | Modèle H « Horizon » |
|---|---|---|---|---|---|---|---|---|
| Organisation | une seule longue page, menu de sections collé en haut | plusieurs pages (Accueil, À propos, Expériences, Projets, Contact) | profil fixe dans une colonne à gauche, contenu à droite | une seule page en tuiles, menu flottant en forme de pilule | une seule page centrée, frise d'expériences alternée | une page façon terminal, fenêtres avec barre de titre | un CV en ligne : feuille avec colonne de contact et compétences | une page grand format, projets en défilement horizontal |
| Style | titres à empattements, ambiance magazine | grille de cartes, police sans empattements | sobre et technique, détails en police à chasse fixe | tuiles lumineuses, chiffres clés, projet vedette en double largeur | grand titre éclairé, photo cerclée de couleur, projets en grandes rangées | commandes et police à chasse fixe | sobre et élégant, imprimable | nom géant, chiffres clés, expériences numérotées |
| Palette par défaut | `teal` | `indigo` | `graphite` | `indigo` | `sunset` | `graphite` | `teal` | `indigo` |
| Idéal pour | un profil à lire d'une traite | beaucoup de projets | un profil technique, data ou dev | un profil moderne qui veut tout montrer d'un coup d'œil | un profil qui veut marquer les esprits | un profil développeur ou data | un profil qui veut un CV en ligne | un profil qui veut un effet « waouh » |

**Modèle A, ordinateur et téléphone**

![Modèle A sur ordinateur](docs-assets/template-a-desktop.webp)

<img src="docs-assets/template-a-mobile.webp" alt="Modèle A sur téléphone" width="300">

**Modèle B, ordinateur et téléphone**

![Modèle B sur ordinateur](docs-assets/template-b-desktop.webp)

<img src="docs-assets/template-b-mobile.webp" alt="Modèle B sur téléphone" width="300">

**Modèle C, ordinateur et téléphone**

![Modèle C sur ordinateur](docs-assets/template-c-desktop.webp)

<img src="docs-assets/template-c-mobile.webp" alt="Modèle C sur téléphone" width="300">

**Modèle D, ordinateur et téléphone**

![Modèle D sur ordinateur](docs-assets/template-d-desktop.webp)

<img src="docs-assets/template-d-mobile.webp" alt="Modèle D sur téléphone" width="300">

**Modèle E, ordinateur et téléphone**

![Modèle E sur ordinateur](docs-assets/template-e-desktop.webp)

<img src="docs-assets/template-e-mobile.webp" alt="Modèle E sur téléphone" width="300">

**Modèle F, ordinateur et téléphone**

![Modèle F sur ordinateur](docs-assets/template-f-desktop.webp)

<img src="docs-assets/template-f-mobile.webp" alt="Modèle F sur téléphone" width="300">

**Modèle G, ordinateur et téléphone**

![Modèle G sur ordinateur](docs-assets/template-g-desktop.webp)

<img src="docs-assets/template-g-mobile.webp" alt="Modèle G sur téléphone" width="300">

**Modèle H, ordinateur et téléphone**

![Modèle H sur ordinateur](docs-assets/template-h-desktop.webp)

<img src="docs-assets/template-h-mobile.webp" alt="Modèle H sur téléphone" width="300">

**Mode sombre** : chaque modèle a un bouton lune/soleil, et suit automatiquement le réglage de l'ordinateur du visiteur.

![Modèle C en mode sombre](docs-assets/template-c-dark.webp)

![Modèle D en mode sombre](docs-assets/template-d-dark.webp)

![Modèle E en mode sombre](docs-assets/template-e-dark.webp)

![Modèle F en mode sombre](docs-assets/template-f-dark.webp)

Les huit modèles s'adaptent au téléphone, se parcourent au clavier, respectent le réglage « réduire les animations » et fonctionnent hors ligne (seules les polices Google Fonts sont chargées en ligne, et c'est désactivable).

### Comparer les modèles chez vous

Une commande génère les huit modèles avec l'exemple, en anglais et en français, et ouvre une page de choix :

```
uv run build.py --preview-all
```

(ou `install.ps1 preview-all` sous Windows, `sh install.sh preview-all` sous Linux et macOS). La page s'ouvre sur `http://localhost:8000` ; elle est aussi lisible sans serveur en double-cliquant sur `previews/index.html`. Arrêtez le serveur avec Ctrl+C.

![Page de choix des modèles](docs-assets/preview-chooser.webp)

---

## 2. Démarrage rapide (5 minutes)

1. **Téléchargez** ce dossier (bouton vert **Code > Download ZIP** sur GitHub), puis décompressez-le.
2. **Lancez l'installateur**, qui installe ce qu'il faut (l'outil `uv`) si besoin, génère le site et l'ouvre :
   - **Windows** : double-cliquez sur `install.cmd`. Ou, dans PowerShell ouvert dans le dossier : `powershell -ExecutionPolicy Bypass -File install.ps1`
   - **macOS** : ouvrez le Terminal, tapez `cd ` (avec un espace), glissez le dossier dans la fenêtre, Entrée, puis `sh install.sh`
   - **Linux** : dans un terminal ouvert dans le dossier : `sh install.sh`
3. **Modifiez** les fichiers du dossier `content/` (voir plus bas), puis relancez l'installateur (ou `uv run build.py`) pour voir le résultat.
4. **Publiez** sur GitHub Pages (section 8).

![Sortie de l'installateur sous Windows](docs-assets/installer-windows.webp)

L'installateur peut être relancé autant de fois que vous voulez : si `uv` est déjà là, il ne réinstalle rien. Options :

| Commande | Effet |
|---|---|
| `install.ps1` / `sh install.sh` | installe uv si besoin, génère `docs/`, ouvre `docs/index.html` |
| `install.ps1 preview` / `sh install.sh preview` | idem, puis sert le site sur `http://localhost:8000` (Ctrl+C pour arrêter) |
| `install.ps1 preview-all` / `sh install.sh preview-all` | les huit modèles côte à côte (voir section 1) |
| `-Port 8080` / `--port 8080` | utiliser un autre port |
| `-NoOpen` / `--no-open` | ne pas ouvrir le navigateur |

---

## 3. Ce qu'il faut modifier

```
portfolio/
  content/              <- LE SEUL DOSSIER À MODIFIER
    site.yml            réglages : langue, modèle, couleurs, polices, sections
    profile.md          nom, titre, photo, liens, CV, courte présentation
    about.md            texte libre « À propos »
    skills.md           compétences, rangées par groupes
    education.md        formations
    experiences/        un fichier .md par expérience
    projects/           un fichier .md par projet
    images/             photo, logos, vignettes de projets
    files/              CV en PDF, rapports
  content-fr-example/   le même exemple, rédigé en français (à consulter)
  templates/a … h/      les modèles (inutile d'y toucher)
  build.py              le script qui fabrique le site
  install.ps1, install.sh, install.cmd   installateurs
  docs/                 le site généré (ne pas modifier à la main)
  docs-assets/          images de ce guide
  outils/               regénère README.html à partir de README.md (uv run outils/readme_html.py)
```

Le dossier `content/` contient un exemple complet en anglais (Alex Martin, étudiant fictif). `content-fr-example/` contient le même exemple en français. **Remplacez le contenu d'Alex par le vôtre**, fichier par fichier. Si vous préférez partir de la version française : supprimez `content/` puis renommez `content-fr-example/` en `content/`.

Un éditeur de texte suffit (Bloc-notes, TextEdit en mode texte brut, ou mieux [VS Code](https://code.visualstudio.com/)). Voici le dossier ouvert dans un éditeur :

![Le dossier content dans un éditeur](docs-assets/editor-content.webp)

### Comment lire un fichier .md

Chaque fichier a deux parties :

```markdown
---
title: Data Science Intern        <- en-tête : des lignes « clé: valeur »
start: 2025-06
---
- Texte libre en Markdown          <- corps : votre texte
- **gras**, *italique*, [lien](https://exemple.com)
```

Règles qui évitent 90 % des erreurs :

- l'en-tête commence et finit par une ligne `---` ;
- après les deux-points, **mettez un espace** : `title: Mon titre` ;
- si une valeur contient `:` ou `#`, mettez-la entre guillemets : `title: "Stage : data science"` ;
- les couleurs commencent par `#` : **mettez-les toujours entre guillemets** (`"#0f766e"`), sinon elles sont lues comme un commentaire ;
- indentez avec des **espaces**, jamais des tabulations ;
- les dates s'écrivent `AAAA-MM` (exemple `2024-09`), ou `present` pour un poste en cours ;
- les chemins d'images sont relatifs au dossier `content/` : `images/photo.jpg`.

---

## 4. Référence des fichiers, champ par champ

### `content/site.yml`

| Champ | Obligatoire | Rôle |
|---|---|---|
| `language` | non (défaut `en`) | langue de l'interface : `en` ou `fr` (menus, titres de sections, mois, « Aujourd'hui »...) |
| `template` | non (défaut `a`) | `a` (Editorial), `b` (Cards), `c` (Sidebar), `d` (Bento), `e` (Spotlight), `f` (Terminal), `g` (Resume) ou `h` (Horizon) |
| `title` | non | titre de l'onglet du navigateur |
| `description` | non | phrase affichée par Google et LinkedIn |
| `base_url` | non | adresse finale du site, par exemple `https://pseudo.github.io/portfolio/` |
| `palette` | non | `teal`, `indigo`, `forest`, `sunset` ou `graphite` (voir section 5) |
| `colors` | non | couleurs personnalisées du mode clair (voir section 5) |
| `dark_colors` | non | couleurs personnalisées du mode sombre |
| `dark_mode` | non (défaut `true`) | `false` pour supprimer le mode sombre et son bouton |
| `fonts` | non | polices des titres (`heading`) et du texte (`body`) |
| `google_fonts` | non (défaut `true`) | `false` pour n'utiliser que les polices de l'ordinateur |
| `sections` | non | `true`/`false` pour chaque section : `about`, `experiences`, `projects`, `skills`, `education`, `contact` |

```yaml
language: fr
template: c
title: "Camille Durand, élève ingénieure à l'ENSAI"
description: "Portfolio de Camille Durand, statistique et data science."
base_url: "https://camille-durand.github.io/portfolio/"
palette: "forest"
dark_mode: true
fonts:
  heading: "lora"
  body: ""
sections:
  about: true
  experiences: true
  projects: true
  skills: true
  education: true
  contact: true
```

Une section sans contenu (par exemple aucun projet) est **cachée automatiquement**, même si elle vaut `true`.

### `content/profile.md`

| Champ | Obligatoire | Rôle |
|---|---|---|
| `name` | **oui** | prénom et nom |
| `headline` | **oui** | votre titre en une ligne |
| `location` | non | ville, pays |
| `availability` | non | phrase courte affichée dans un badge vert en haut de la page (ex. « Disponible dès avril 2027 pour un stage de 6 mois ») |
| `email` | non | si renseigné, un bouton « Envoyer un e-mail » apparaît. Sinon, aucune adresse n'est affichée |
| `phone` | non | numéro de téléphone |
| `show_phone` | non (défaut `false`) | le numéro n'est **jamais affiché** tant que ce champ ne vaut pas `true` |
| `photo` | non | chemin de la photo, par exemple `images/photo.jpg` (carrée de préférence) |
| `photo_alt` | non | description de la photo pour les lecteurs d'écran (défaut : « Portrait de ... ») |
| `cv_pdf` | non | chemin du CV, par exemple `files/cv.pdf` : ajoute un bouton « Télécharger le CV » |
| `linkedin`, `github`, `website` | non | adresses complètes, commençant par `https://` |

Le corps du fichier est votre présentation courte (2 ou 3 phrases), affichée en haut du site.

```markdown
---
name: Camille Durand
headline: Élève ingénieure en data science
location: Rennes, France
availability: "Available from April 2027 for a 6-month internship"
email: camille.durand@example.com
phone: "+33 6 00 00 00 00"
show_phone: false
photo: images/photo.jpg
cv_pdf: files/cv-camille-durand.pdf
linkedin: https://www.linkedin.com/in/camille-durand
github: https://github.com/camille-durand
website: ""
---
Élève ingénieure en deuxième année à l'**ENSAI**. Je recherche un stage de 6 mois en data science.
```

### `content/about.md`

Texte libre en Markdown, sans en-tête obligatoire. Paragraphes, listes, gras, liens : tout est permis. Laissez le fichier vide pour cacher la section.

```markdown
J'ai découvert la statistique grâce à un projet de lycée...

En dehors des cours :

- je fais partie de l'association de théâtre ;
- je cours un semi-marathon par an.
```

### `content/skills.md`

Une liste de groupes. Chaque compétence s'écrit soit simplement, soit avec un niveau de 1 à 5 (affiché sous forme de points, de barre ou de carrés selon le modèle).

```markdown
---
groups:
  - name: Programmation
    items:
      - name: Python
        level: 5
      - name: R
        level: 4
  - name: Outils
    items: [pandas, scikit-learn, Power BI]
  - name: Langues
    items: [Français (natif), Anglais (C1)]
---
```

Le corps du fichier (sous le second `---`) est facultatif : une phrase d'introduction affichée au-dessus des compétences.

### `content/education.md`

```markdown
---
entries:
  - school: ENSAI
    degree: Diplôme d'ingénieur, statistique et science des données
    location: Bruz, France
    start: 2023-09
    end: present
    details: Modélisation statistique, machine learning, sondages.
  - school: Lycée Exemple
    degree: CPGE MP
    location: Nantes, France
    start: 2021-09
    end: 2023-06
---
```

`school` et `degree` sont obligatoires ; `location`, `start`, `end` et `details` sont facultatifs. Les formations sont triées automatiquement, la plus récente en premier.

### `content/experiences/*.md` (un fichier par expérience)

| Champ | Obligatoire | Rôle |
|---|---|---|
| `title` | **oui** | intitulé du poste |
| `organisation` | **oui** | entreprise ou association |
| `location` | non | lieu |
| `start` | **oui** | date de début `AAAA-MM` |
| `end` | **oui** | date de fin `AAAA-MM`, ou `present` |
| `type` | **oui** | `internship` (stage), `job` (emploi), `apprenticeship` (alternance) ou `volunteering` (bénévolat) |
| `logo` | non | chemin du logo, par exemple `images/logos/entreprise.png` (sinon, les initiales sont affichées) |
| `logo_alt` | non | description du logo (défaut : « Logo de ... ») |
| `tags` | non | mots-clés : `[Python, SQL]` |

Le corps contient vos réalisations, idéalement une liste à puces avec des résultats chiffrés.

```markdown
---
title: Stagiaire data scientist
organisation: Banque Exemple
location: Paris, France
start: 2025-06
end: 2025-08
type: internship
logo: images/logos/banque-exemple.png
tags: [Python, Scoring, SQL]
---
- Construit un modèle de scoring qui a amélioré l'AUC de 0,71 à 0,78.
- Automatisé le reporting mensuel (deux jours gagnés par mois).
```

Les expériences sont triées automatiquement par date, la plus récente en premier.

### `content/projects/*.md` (un fichier par projet)

| Champ | Obligatoire | Rôle |
|---|---|---|
| `title` | **oui** | nom du projet |
| `date` | **oui** | `AAAA-MM` |
| `category` | **oui** | `academic` (académique) ou `personal` (personnel) : sert aux filtres |
| `summary` | **oui** | une ou deux phrases, affichées sur la carte |
| `thumbnail` | non | vignette, format paysage 16:9 conseillé (par exemple 1200 x 675 pixels) |
| `thumbnail_alt` | non | description de la vignette (défaut : « Illustration du projet ... ») |
| `tags` | non | mots-clés |
| `links` | non | `repo` (code), `demo` (démo en ligne), `report` (rapport : adresse web ou fichier `files/rapport.pdf`) |
| `featured` | non (défaut `false`) | `true` pour mettre le projet à la une |

Le corps est la page détaillée du projet (contexte, ce que vous avez fait, résultats, tableaux, images). **Si le corps est vide**, le projet n'a pas de page détaillée : seule la carte est affichée.

```markdown
---
title: Scoring du défaut de crédit
date: 2025-03
category: academic
thumbnail: images/thumbnails/credit.png
thumbnail_alt: Courbe ROC des trois modèles comparés
tags: [Python, LightGBM]
summary: Prédire le défaut de paiement sur 300 000 demandes de prêt.
featured: true
links:
  repo: https://github.com/camille-durand/credit-scoring
  report: files/rapport-credit.pdf
---
## Contexte

Projet en équipe de 4 pour le cours de Machine Learning...
```

---

## 5. Couleurs et polices

Tout se règle dans `content/site.yml`.

### Palettes toutes prêtes

Écrivez simplement `palette: "sunset"` (ou `teal`, `indigo`, `forest`, `graphite`). Chaque palette a une version claire et une version sombre, déjà vérifiées pour la lisibilité.

![Les cinq palettes, en clair et en sombre](docs-assets/palettes.webp)

![La ligne palette dans site.yml](docs-assets/editor-site-yml.webp)

**Avant / après** : le modèle B avec sa palette par défaut, puis avec `palette: "sunset"` et `heading: "lora"`.

![Avant : palette indigo](docs-assets/colors-before.webp)

![Après : palette sunset et titres en Lora](docs-assets/colors-after.webp)

### Couleurs personnalisées

Pour aller plus loin, remplacez une ou plusieurs couleurs de la palette (toujours **entre guillemets**) :

```yaml
palette: "teal"
colors:
  primary: "#9d174d"      # boutons et liens
  secondary: "#0369a1"    # petits détails : étiquettes, « À la une »
  background: "#fffaf5"   # fond de la page
  surface: "#ffffff"      # fond des cartes
  text: "#1f1720"         # texte
dark_colors:
  primary: ""             # vide = calculé automatiquement à partir du mode clair
dark_mode: true           # false = pas de mode sombre ni de bouton lune/soleil
```

Le script **vérifie la lisibilité** (contraste suffisant pour les normes d'accessibilité). Si une couleur est trop claire ou trop proche du fond, il l'ajuste automatiquement et vous prévient, par exemple :

```
Avertissement (couleurs) : mode clair : la couleur principale #f5d90a contraste trop peu avec le fond ; le site utilise #86750b pour les liens et les boutons.
```

Pour trouver un code couleur : [htmlcolorcodes.com](https://htmlcolorcodes.com/fr/).

### Polices

```yaml
fonts:
  heading: "fraunces"   # titres
  body: "inter"         # texte
```

Choix possibles : `inter`, `plus-jakarta-sans`, `space-grotesk`, `ibm-plex-sans` (sans empattements), `fraunces`, `lora`, `source-serif-4` (avec empattements), `jetbrains-mono` (chasse fixe), `system` (police de l'ordinateur, aucun téléchargement). Laissez vide pour garder la police du modèle. Avec `google_fonts: false`, aucune police n'est téléchargée et le site utilise les polices de l'ordinateur.

---

## 6. Tâches courantes

### Ajouter une expérience ou un projet

1. Dans `content/experiences/` (ou `content/projects/`), **copiez un fichier existant** et renommez la copie, par exemple `stage-banque.md`. Utilisez des minuscules, des tirets et pas d'accents dans le nom du fichier : il sert d'adresse à la page du projet.
2. Modifiez l'en-tête et le texte.
3. Relancez `uv run build.py` (ou l'installateur).

Pour supprimer un élément, supprimez son fichier. Pour le mettre de côté sans le supprimer, ajoutez un tiret bas au début du nom (`_brouillon.md`) : les fichiers qui commencent par `_` sont ignorés.

### Ajouter une photo, un logo ou une vignette

1. Copiez l'image dans `content/images/` (ou un sous-dossier comme `images/thumbnails/`).
2. Indiquez son chemin dans le fichier concerné : `thumbnail: images/thumbnails/mon-projet.png`.
3. Formats acceptés : `.jpg`, `.png`, `.webp`, `.svg`. Pensez à alléger les photos (moins de 500 Ko).
4. Remplissez `thumbnail_alt` (ou `photo_alt`, `logo_alt`) avec une courte description de l'image : c'est ce que lisent les personnes malvoyantes.

Les images fournies (silhouette, logos à initiales, vignettes abstraites) sont des exemples neutres à remplacer.

### Changer de langue

Dans `content/site.yml`, mettez `language: fr` ou `language: en`. Cela traduit l'interface (menus, titres, mois, « Aujourd'hui »). **Votre texte n'est pas traduit** : rédigez-le dans la langue choisie.

### Changer de modèle

Dans `content/site.yml`, mettez `template: a`, `b`, `c`, `d`, `e`, `f`, `g` ou `h`, puis relancez le script. Aucun autre changement n'est nécessaire. Pour essayer sans modifier le fichier : `uv run build.py --template c`.

---

## 7. Voir le site sur son ordinateur

Le plus simple est l'installateur (section 2). Si vous préférez les commandes :

### Installer uv (une seule fois)

`uv` est un petit outil qui installe Python et les bibliothèques nécessaires à votre place.

- **Windows** (PowerShell) : `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **macOS et Linux** : `curl -LsSf https://astral.sh/uv/install.sh | sh`

Fermez puis rouvrez le terminal.

### Générer et ouvrir le site

Ouvrez un terminal **dans le dossier du portfolio** (sous Windows : clic droit dans le dossier, « Ouvrir dans le terminal »), puis :

```
uv run build.py
```

Ouvrez ensuite `docs/index.html` en double-cliquant dessus. Après chaque modification, relancez la commande et rafraîchissez la page (F5).

### Si quelque chose ne va pas

Si le contenu contient une erreur, le site n'est pas généré et le script indique **le fichier, le champ et la correction attendue** :

![Exemple de message d'erreur](docs-assets/error-message.webp)

Ici, deux corrections : mettre le titre entre guillemets (`title: "Data Science Intern: churn"`) et écrire la date `2024-12`.

**Sans uv** : `python -m pip install markdown pyyaml jinja2` puis `python build.py` (Python 3.11 ou plus récent).

Options utiles :

```
uv run build.py --template b                                    # essayer un autre modèle
uv run build.py --language fr                                   # essayer l'autre langue d'interface
uv run build.py --content content-fr-example --out apercu-fr    # générer l'exemple français ailleurs
uv run build.py --preview-all                                   # les huit modèles côte à côte
uv run build.py --serve                                         # génère puis sert docs/ sur http://localhost:8000
```

---

## 8. Publier sur GitHub Pages

### Étape 1 : créer votre dépôt

1. Créez un compte sur [github.com](https://github.com) si besoin.
2. Le plus simple : sur la page de ce projet, cliquez sur **Use this template > Create a new repository** (ou **Fork**), nommez-le par exemple `portfolio`, laissez-le **Public**.
3. Sinon, créez un dépôt vide (**New repository**) et envoyez-y le dossier :
   - sans ligne de commande : sur la page du dépôt, **uploading an existing file**, glissez-déposez le contenu du dossier (y compris le dossier `.github` ; s'il n'apparaît pas, affichez les fichiers cachés) ;
   - avec Git :
     ```
     git init
     git add .
     git commit -m "Mon portfolio"
     git branch -M main
     git remote add origin https://github.com/VOTRE-PSEUDO/portfolio.git
     git push -u origin main
     ```

### Étape 2 : activer la publication

Dans votre dépôt, ouvrez l'onglet **Settings** (roue dentée, en haut à droite), puis dans le menu de gauche la rubrique **Pages** (section « Code and automation »). L'écran affiche un titre « GitHub Pages » et un bloc **Build and deployment** avec une liste déroulante **Source**. Deux choix, prenez-en **un** :

- **GitHub Actions (recommandé)** : choisissez `GitHub Actions` dans la liste **Source**. Rien d'autre à régler : à chaque modification envoyée sur la branche `main`, le site est régénéré et publié tout seul. Suivez l'avancement dans l'onglet **Actions** (rond orange pendant la publication, coche verte quand c'est fini). Vous pouvez même modifier vos fichiers `content/` directement sur le site de GitHub (icône crayon).
- **Deploy from a branch (simple)** : choisissez `Deploy from a branch`, puis dans les deux listes qui apparaissent, la branche `main` et le dossier `/docs`, et cliquez sur **Save**. GitHub publie alors le dossier `docs/` tel quel : pensez à lancer `uv run build.py` sur votre ordinateur **avant** chaque envoi.

Après une ou deux minutes, un bandeau en haut de cette page indique « Your site is live at ... » avec l'adresse, du type `https://VOTRE-PSEUDO.github.io/portfolio/`. Reportez-la dans `base_url` de `site.yml`.

---

## 9. FAQ

**Le site affiche toujours Alex Martin.**
Relancez `uv run build.py` après vos modifications, puis rafraîchissez la page (Ctrl+F5). Sur GitHub, vérifiez que l'onglet **Actions** est vert.

**Mon image ne s'affiche pas.**
Le script signale les images introuvables. Vérifiez le chemin (relatif à `content/`), les majuscules (`Photo.JPG` n'est pas `photo.jpg` sur GitHub) et l'extension.

**Ma couleur n'est pas prise en compte.**
Elle n'est sans doute pas entre guillemets : `primary: "#9d174d"`. Sans guillemets, tout ce qui suit `#` est un commentaire.

**Je ne veux pas montrer mon e-mail.**
Laissez `email:` vide : aucun bouton ni adresse n'apparaît. Le téléphone, lui, n'est jamais affiché sans `show_phone: true`.

**Comment cacher une section ?**
Dans `site.yml`, passez-la à `false` (par exemple `skills: false`). Une section vide est de toute façon cachée.

**Je veux un projet sans page détaillée.**
Laissez le corps du fichier vide (rien sous le second `---`) : seule la carte s'affiche, avec ses liens.

**Windows refuse de lancer install.ps1.**
Utilisez `install.cmd` (double-clic), ou la commande complète `powershell -ExecutionPolicy Bypass -File install.ps1`, qui autorise ce script seulement, une fois.

**Le port 8000 est déjà utilisé.**
Pas de souci : l'aperçu essaie automatiquement les ports suivants (8001, 8002...) et affiche l'adresse retenue. Vous pouvez aussi choisir le port : `-Port 8080` (Windows) ou `--port 8080` (Linux, macOS).

**Le site doit-il être en ligne pour fonctionner ?**
Non. Le dossier `docs/` fonctionne aussi hors ligne. Pour n'utiliser aucune ressource externe, mettez `google_fonts: false`.

**Puis-je modifier la mise en page plus finement ?**
Oui, dans `templates/<a…h>/static/style.css`. Ce n'est pas nécessaire pour un usage normal.

**Que sont les dossiers `previews/` et `_qa/` ?**
`previews/` est créé par `--preview-all` ; `_qa/` contient des essais de vérification. Les deux sont ignorés par Git et peuvent être supprimés.

---

Licence MIT. Les images d'exemple sont des créations neutres libres de droits, à remplacer par les vôtres.

---

## Licence

Projet libre sous [licence MIT](LICENSE) : vous pouvez l'utiliser, le modifier et le partager gratuitement, y compris pour votre portfolio personnel. Seule condition : garder la mention de copyright du fichier `LICENSE` dans les copies du code. Si le projet vous aide, une étoile sur le dépôt et un abonnement à [Djamal029](https://github.com/Djamal029) font plaisir.
