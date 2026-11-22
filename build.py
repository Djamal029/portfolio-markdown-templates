# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "markdown>=3.5",
#   "pyyaml>=6.0",
#   "jinja2>=3.1",
# ]
# ///
"""Générateur de portfolio statique à partir du dossier content/.

Utilisation :
    uv run build.py                      # lit content/, écrit docs/
    uv run build.py --template b         # force le modèle B
    uv run build.py --content content-fr-example --out _qa/build-fr

Le script lit les fichiers Markdown du dossier de contenu, vérifie chaque
champ, puis produit un site HTML complet (sans dépendance externe) dans le
dossier de sortie. Les messages d'erreur indiquent le fichier et le champ
à corriger.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

try:
    import jinja2
    import markdown
    import yaml
except ImportError as exc:  # pragma: no cover
    print(
        "Il manque une bibliothèque Python (" + str(exc.name) + ").\n"
        "Lancez plutôt :  uv run build.py\n"
        "ou installez-les :  python -m pip install markdown pyyaml jinja2",
        file=sys.stderr,
    )
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
BUILD_MARKER = ".portfolio-build"

# ---------------------------------------------------------------------------
# Textes d'interface (anglais / francais)
# ---------------------------------------------------------------------------

I18N: dict[str, dict[str, Any]] = {
    "en": {
        "nav_home": "Home",
        "nav_about": "About",
        "nav_experiences": "Experience",
        "nav_projects": "Projects",
        "nav_skills": "Skills",
        "nav_education": "Education",
        "nav_contact": "Contact",
        "section_about": "About me",
        "section_experiences": "Experience",
        "section_projects": "Projects",
        "section_skills": "Skills",
        "section_education": "Education",
        "section_contact": "Contact",
        "featured_projects": "Selected projects",
        "latest_experience": "Recent experience",
        "see_all_projects": "See all projects",
        "see_all_experiences": "See all experience",
        "more_about": "More about me",
        "present": "Present",
        "view_project": "View project",
        "back_to_projects": "Back to projects",
        "filter_label": "Filter projects",
        "filter_all": "All",
        "academic": "Academic",
        "personal": "Personal",
        "featured": "Featured",
        "download_cv": "Download CV",
        "contact_me": "Contact me",
        "email_me": "Send an email",
        "email": "Email",
        "phone": "Phone",
        "location": "Location",
        "availability": "Availability",
        "at_a_glance": "At a glance",
        "n_projects": "projects",
        "n_experiences": "experiences",
        "linkedin": "LinkedIn",
        "github": "GitHub",
        "website": "Website",
        "repo": "Code",
        "demo": "Demo",
        "report": "Report",
        "contact_title": "Let's talk",
        "contact_text": "Open to internships, apprenticeships and collaborations. The quickest way to reach me is below.",
        "type_internship": "Internship",
        "type_job": "Job",
        "type_apprenticeship": "Apprenticeship",
        "type_volunteering": "Volunteering",
        "level": "Level {n} of 5",
        "skip_link": "Skip to content",
        "theme_toggle": "Switch between light and dark theme",
        "menu": "Menu",
        "main_nav": "Main navigation",
        "photo_alt": "Portrait of {name}",
        "thumbnail_alt": "Illustration for the project {title}",
        "logo_alt": "Logo of {org}",
        "footer_built": "Built from Markdown files.",
        "updated": "Last updated {date}",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "no_projects": "No project in this category yet.",
        "tags": "Keywords",
    },
    "fr": {
        "nav_home": "Accueil",
        "nav_about": "À propos",
        "nav_experiences": "Expériences",
        "nav_projects": "Projets",
        "nav_skills": "Compétences",
        "nav_education": "Formation",
        "nav_contact": "Contact",
        "section_about": "À propos",
        "section_experiences": "Expériences",
        "section_projects": "Projets",
        "section_skills": "Compétences",
        "section_education": "Formation",
        "section_contact": "Contact",
        "featured_projects": "Projets à la une",
        "latest_experience": "Expériences récentes",
        "see_all_projects": "Voir tous les projets",
        "see_all_experiences": "Voir toutes les expériences",
        "more_about": "En savoir plus",
        "present": "Aujourd'hui",
        "view_project": "Voir le projet",
        "back_to_projects": "Retour aux projets",
        "filter_label": "Filtrer les projets",
        "filter_all": "Tous",
        "academic": "Académique",
        "personal": "Personnel",
        "featured": "À la une",
        "download_cv": "Télécharger le CV",
        "contact_me": "Me contacter",
        "email_me": "Envoyer un e-mail",
        "email": "E-mail",
        "phone": "Téléphone",
        "location": "Localisation",
        "availability": "Disponibilité",
        "at_a_glance": "En bref",
        "n_projects": "projets",
        "n_experiences": "expériences",
        "linkedin": "LinkedIn",
        "github": "GitHub",
        "website": "Site web",
        "repo": "Code",
        "demo": "Démo",
        "report": "Rapport",
        "contact_title": "Discutons",
        "contact_text": "Ouvert aux stages, alternances et collaborations. Le plus simple pour me joindre est ci-dessous.",
        "type_internship": "Stage",
        "type_job": "Emploi",
        "type_apprenticeship": "Alternance",
        "type_volunteering": "Bénévolat",
        "level": "Niveau {n} sur 5",
        "skip_link": "Aller au contenu",
        "theme_toggle": "Basculer entre thème clair et sombre",
        "menu": "Menu",
        "main_nav": "Navigation principale",
        "photo_alt": "Portrait de {name}",
        "thumbnail_alt": "Illustration du projet {title}",
        "logo_alt": "Logo de {org}",
        "footer_built": "Site généré à partir de fichiers Markdown.",
        "updated": "Mis à jour en {date}",
        "months": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
        "no_projects": "Aucun projet dans cette catégorie pour le moment.",
        "tags": "Mots-clés",
    },
}

SECTION_ORDER = ["about", "experiences", "projects", "skills", "education", "contact"]
EXPERIENCE_TYPES = ["internship", "job", "apprenticeship", "volunteering"]
PROJECT_CATEGORIES = ["academic", "personal"]
PRESENT_WORDS = {"present", "présent", "present.", "aujourd'hui", "en cours", "now", "current"}

# ---------------------------------------------------------------------------
# Gestion des erreurs
# ---------------------------------------------------------------------------


@dataclass
class Report:
    content_dir: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def _where(self, path: Path, key: str | None) -> str:
        try:
            shown = path.relative_to(self.content_dir.parent).as_posix()
        except ValueError:
            shown = path.as_posix()
        return f"{shown} (champ « {key} »)" if key else shown

    def error(self, path: Path, key: str | None, message: str) -> None:
        self.errors.append(f"{self._where(path, key)} : {message}")

    def warn(self, path: Path, key: str | None, message: str) -> None:
        self.warnings.append(f"{self._where(path, key)} : {message}")


# ---------------------------------------------------------------------------
# Lecture des fichiers
# ---------------------------------------------------------------------------

# smart_dashes désactivé : « -- » et « --- » restent tels quels (pas de tirets longs générés).
MD = markdown.Markdown(
    extensions=["extra", "sane_lists", "smarty"],
    extension_configs={"smarty": {"smart_dashes": False}},
    output_format="html",
)


def md_to_html(text: str) -> str:
    MD.reset()
    return MD.convert(text or "").strip()


def md_inline(text: str) -> str:
    html = md_to_html(text)
    if html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        html = html[3:-4]
    return html


def read_text(path: Path, report: Report) -> str | None:
    try:
        return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    except UnicodeDecodeError:
        report.error(path, None, "le fichier n'est pas encodé en UTF-8. Ré-enregistrez-le en UTF-8 dans votre éditeur.")
    except OSError as exc:
        report.error(path, None, f"lecture impossible ({exc.strerror}).")
    return None


INVALID = object()


def parse_yaml(text: str, path: Path, report: Report, line_offset: int = 0) -> Any:
    """Lit du YAML ; renvoie INVALID (et enregistre une erreur claire) si la syntaxe est fausse."""
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        problem = getattr(exc, "problem", None) or "syntaxe invalide"
        where = f" vers la ligne {mark.line + 1 + line_offset}" if mark is not None else ""
        report.error(
            path,
            None,
            f"en-tête YAML invalide{where} ({problem}). Vérifiez les deux-points « clé: valeur », "
            "l'indentation (espaces, pas de tabulation) et mettez entre guillemets les textes qui contiennent « : » ou « # ».",
        )
        return INVALID


def read_markdown(path: Path, report: Report, frontmatter_required: bool = True) -> tuple[dict | None, str]:
    """Renvoie (frontmatter, corps). frontmatter vaut None en cas d'erreur."""
    text = read_text(path, report)
    if text is None:
        return None, ""
    if not text.startswith("---\n") and text.strip() != "---":
        if frontmatter_required:
            report.error(
                path,
                None,
                "le fichier doit commencer par une ligne « --- », suivie des champs, puis d'une autre ligne « --- ».",
            )
            return None, ""
        return {}, text
    match = re.search(r"^---[ \t]*$", text[4:], re.M)
    if not match:
        report.error(path, None, "la ligne « --- » qui ferme l'en-tête est introuvable.")
        return None, ""
    data = parse_yaml(text[4 : 4 + match.start()], path, report, line_offset=1)
    if data is INVALID:
        return None, ""
    if data is None:
        data = {}
    if not isinstance(data, dict):
        report.error(path, None, "l'en-tête doit contenir des lignes « clé: valeur ».")
        return None, ""
    return data, text[4 + match.end() :].lstrip("\n")


# ---------------------------------------------------------------------------
# Champs et validation
# ---------------------------------------------------------------------------


class Fields:
    """Accesseurs typés qui enregistrent des erreurs lisibles."""

    def __init__(self, data: dict, path: Path, report: Report, content_dir: Path, assets: set[str]):
        self.data = data
        self.path = path
        self.report = report
        self.content_dir = content_dir
        self.assets = assets

    def text(self, key: str, required: bool = False, default: str = "") -> str:
        value = self.data.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            if required:
                self.report.error(self.path, key, "champ obligatoire manquant ou vide.")
            return default
        if isinstance(value, (dict, list)):
            self.report.error(self.path, key, "doit être un texte simple, pas une liste.")
            return default
        return str(value).strip()

    def boolean(self, key: str, default: bool = False) -> bool:
        value = self.data.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str) and value.strip().lower() in {"true", "oui", "yes", "vrai"}:
            return True
        if isinstance(value, str) and value.strip().lower() in {"false", "non", "no", "faux"}:
            return False
        if value is None:
            return default
        self.report.error(self.path, key, "doit valoir true ou false.")
        return default

    def text_list(self, key: str) -> list[str]:
        value = self.data.get(key)
        if value in (None, ""):
            return []
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        if isinstance(value, list) and all(isinstance(v, (str, int, float)) for v in value):
            return [str(v).strip() for v in value if str(v).strip()]
        self.report.error(self.path, key, "doit être une liste, par exemple [Python, SQL] ou des lignes « - Python ».")
        return []

    def choice(self, key: str, choices: list[str], required: bool = True) -> str:
        value = self.text(key, required=required).lower()
        if value and value not in choices:
            self.report.error(self.path, key, f"valeur « {value} » inconnue. Valeurs possibles : {', '.join(choices)}.")
            return choices[0]
        return value

    def url(self, key: str, value: str | None = None) -> str:
        value = self.text(key) if value is None else value
        if not value:
            return ""
        if re.match(r"^https?://", value):
            return value
        if re.match(r"^(www\.)?[\w-]+\.[a-z]{2,}", value, re.I):
            self.report.error(self.path, key, f"ajoutez « https:// » au début de l'adresse ({value}).")
            return ""
        return self.local_file(key, value)

    def local_file(self, key: str, value: str, kind: str = "fichier") -> str:
        """Vérifie qu'un chemin relatif au dossier de contenu existe."""
        rel = value.replace("\\", "/").lstrip("./")
        if re.match(r"^https?://", value):
            return value
        if ".." in Path(rel).parts:
            self.report.error(self.path, key, "le chemin ne doit pas contenir « .. ». Placez le fichier dans le dossier images/ ou files/.")
            return ""
        if not (self.content_dir / rel).is_file():
            self.report.error(
                self.path,
                key,
                f"{kind} introuvable : « {value} ». Le chemin est relatif au dossier "
                f"{self.content_dir.name}/ (exemple : images/photo.jpg). Vérifiez l'orthographe et l'extension.",
            )
            return ""
        self.assets.add(rel)
        return rel

    def image(self, key: str) -> str:
        value = self.text(key)
        if not value:
            return ""
        if not re.search(r"\.(png|jpe?g|webp|gif|svg|avif)$", value, re.I) and not value.startswith("http"):
            self.report.error(self.path, key, "format d'image non reconnu. Utilisez .jpg, .png, .webp ou .svg.")
            return ""
        return self.local_file(key, value, kind="image")

    def date(self, key: str, required: bool = True, allow_present: bool = False) -> dict | None:
        value = self.data.get(key)
        if value is None or value == "":
            if required:
                self.report.error(self.path, key, "date manquante. Format attendu : AAAA-MM (exemple : 2024-09).")
            return None
        if isinstance(value, dt.datetime):
            value = value.date()
        if isinstance(value, dt.date):
            return {"y": value.year, "m": value.month, "d": value.day}
        text = str(value).strip()
        if allow_present and text.lower() in PRESENT_WORDS:
            return {"present": True, "y": 9999, "m": 12, "d": 31}
        match = re.fullmatch(r"(\d{4})(?:[-/](\d{1,2}))?(?:[-/](\d{1,2}))?", text)
        if not match or (match.group(2) and not 1 <= int(match.group(2)) <= 12):
            hint = " ou « present »" if allow_present else ""
            self.report.error(self.path, key, f"date « {text} » illisible. Format attendu : AAAA-MM (exemple : 2024-09){hint}.")
            return None
        return {"y": int(match.group(1)), "m": int(match.group(2) or 0), "d": int(match.group(3) or 0)}


def date_key(d: dict | None) -> tuple[int, int, int]:
    if not d:
        return (0, 0, 0)
    return (d["y"], d["m"], d["d"])


def format_date(d: dict | None, t: dict) -> str:
    if not d:
        return ""
    if d.get("present"):
        return t["present"]
    if d["m"]:
        return f"{t['months'][d['m'] - 1]} {d['y']}"
    return str(d["y"])


def format_range(start: dict | None, end: dict | None, t: dict) -> str:
    a, b = format_date(start, t), format_date(end, t)
    if a and b and a != b:
        return f"{a} – {b}"
    return a or b


def iso_date(d: dict | None) -> str:
    if not d or d.get("present"):
        return ""
    if d["m"]:
        return f"{d['y']:04d}-{d['m']:02d}"
    return f"{d['y']:04d}"


def slugify(text: str) -> str:
    import unicodedata

    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "projet"


# ---------------------------------------------------------------------------
# Thème : palettes, couleurs personnalisées, polices
# ---------------------------------------------------------------------------

COLOR_KEYS = ["primary", "secondary", "background", "surface", "text"]

PALETTES: dict[str, dict[str, dict[str, str]]] = {
    "teal": {
        "light": {"primary": "#0f766e", "secondary": "#b45309", "background": "#fbfaf7", "surface": "#ffffff", "text": "#1c1917"},
        "dark": {"primary": "#5fc4b8", "secondary": "#f0b65a", "background": "#131211", "surface": "#1c1b19", "text": "#ede9e3"},
    },
    "indigo": {
        "light": {"primary": "#4f46e5", "secondary": "#be185d", "background": "#f5f6fa", "surface": "#ffffff", "text": "#151826"},
        "dark": {"primary": "#a5a0ff", "secondary": "#f9a8d4", "background": "#0f1117", "surface": "#171a23", "text": "#eceef5"},
    },
    "forest": {
        "light": {"primary": "#2f6b3a", "secondary": "#9a5b06", "background": "#f6f7f2", "surface": "#ffffff", "text": "#1a2119"},
        "dark": {"primary": "#8fcf96", "secondary": "#e8c06a", "background": "#10140f", "surface": "#182017", "text": "#e6ece3"},
    },
    "sunset": {
        "light": {"primary": "#c2410c", "secondary": "#6d28d9", "background": "#fdf8f4", "surface": "#ffffff", "text": "#23160f"},
        "dark": {"primary": "#fb9a6c", "secondary": "#c4b5fd", "background": "#171110", "surface": "#221a17", "text": "#f3e9e3"},
    },
    "graphite": {
        "light": {"primary": "#1e293b", "secondary": "#0e7490", "background": "#f4f5f7", "surface": "#ffffff", "text": "#0f172a"},
        "dark": {"primary": "#e2e8f0", "secondary": "#5fd4ea", "background": "#0c0e12", "surface": "#151922", "text": "#e5e9f0"},
    },
}

FONTS: dict[str, tuple[str, str, str]] = {
    # clé: (nom Google Fonts, graisses, famille de secours)
    "inter": ("Inter", "wght@400;500;600;700", "sans"),
    "plus-jakarta-sans": ("Plus Jakarta Sans", "wght@400;500;600;700;800", "sans"),
    "space-grotesk": ("Space Grotesk", "wght@400;500;600;700", "sans"),
    "ibm-plex-sans": ("IBM Plex Sans", "wght@400;500;600;700", "sans"),
    "fraunces": ("Fraunces", "opsz,wght@9..144,500;9..144,600;9..144,700", "serif"),
    "lora": ("Lora", "wght@400;500;600;700", "serif"),
    "source-serif-4": ("Source Serif 4", "opsz,wght@8..60,400;8..60,600;8..60,700", "serif"),
    "jetbrains-mono": ("JetBrains Mono", "wght@400;500;700", "mono"),
    "system": ("", "", "sans"),
}
FALLBACKS = {
    "sans": 'system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif',
    "serif": '"Iowan Old Style", "Palatino Linotype", Georgia, serif',
    "mono": 'ui-monospace, "Cascadia Code", Consolas, "Liberation Mono", monospace',
}

TEMPLATES = {
    "a": {"name": "Editorial", "palette": "teal", "heading": "fraunces", "body": "inter", "mono": "system"},
    "b": {"name": "Cards", "palette": "indigo", "heading": "plus-jakarta-sans", "body": "plus-jakarta-sans", "mono": "system"},
    "c": {"name": "Sidebar", "palette": "graphite", "heading": "space-grotesk", "body": "ibm-plex-sans", "mono": "jetbrains-mono"},
    "d": {"name": "Bento", "palette": "indigo", "heading": "space-grotesk", "body": "inter", "mono": "system"},
    "e": {"name": "Spotlight", "palette": "sunset", "heading": "source-serif-4", "body": "inter", "mono": "system"},
    "f": {"name": "Terminal", "palette": "graphite", "heading": "jetbrains-mono", "body": "ibm-plex-sans", "mono": "jetbrains-mono"},
    "g": {"name": "Resume", "palette": "teal", "heading": "lora", "body": "inter", "mono": "system"},
    "h": {"name": "Horizon", "palette": "indigo", "heading": "plus-jakarta-sans", "body": "plus-jakarta-sans", "mono": "system"},
    "i": {"name": "Aurora", "palette": "indigo", "heading": "plus-jakarta-sans", "body": "inter", "mono": "system"},
    "j": {"name": "Studio", "palette": "forest", "heading": "fraunces", "body": "inter", "mono": "system"},
}

WHITE = (255, 255, 255)
INK = (15, 15, 17)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def luminance(rgb: tuple[int, int, int]) -> float:
    def chan(c: int) -> float:
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(rgb: tuple[int, int, int], other: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(round(c + (o - c) * ratio) for c, o in zip(rgb, other))  # type: ignore[return-value]


def to_hex(rgb: tuple[int, int, int]) -> str:
    return "#" + "".join(f"{c:02x}" for c in rgb)


def ensure_contrast(fg: tuple[int, int, int], bg: tuple[int, int, int], target: float, toward: tuple[int, int, int]) -> tuple[int, int, int]:
    """Rapproche fg de « toward » jusqu'à atteindre le contraste voulu avec bg."""
    steps = 0
    while contrast(fg, bg) < target and steps < 40:
        fg = mix(fg, toward, 0.08)
        steps += 1
    return fg


def is_hex(value: str) -> bool:
    return bool(re.fullmatch(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value))


def read_colors(data: Any, path: Path, report: Report, key: str) -> dict[str, str]:
    if data in (None, ""):
        return {}
    if not isinstance(data, dict):
        report.error(path, key, "doit contenir des lignes comme « primary: \"#0f766e\" ».")
        return {}
    out = {}
    for name, value in data.items():
        if name not in COLOR_KEYS:
            report.error(path, f"{key}.{name}", f"couleur inconnue. Couleurs possibles : {', '.join(COLOR_KEYS)}.")
            continue
        if value in (None, ""):
            continue
        value = str(value).strip()
        if not is_hex(value):
            report.error(path, f"{key}.{name}", f"« {value} » n'est pas une couleur hexadécimale. Écrivez-la entre guillemets, par exemple \"#0f766e\".")
            continue
        out[name] = value if value.startswith("#") else "#" + value
    return out


def resolve_mode(base: dict[str, str], custom: dict[str, str], mode: str, warnings: list[str]) -> dict[str, str]:
    """Calcule les variables CSS d'un mode (clair ou sombre) en corrigeant les contrastes insuffisants."""
    label = "mode clair" if mode == "light" else "mode sombre"
    c = {k: hex_to_rgb(custom.get(k) or base[k]) for k in COLOR_KEYS}
    bg, surface = c["background"], c["surface"]
    away = INK if luminance(bg) > 0.4 else WHITE

    text = c["text"]
    fixed = ensure_contrast(ensure_contrast(text, bg, 7, away), surface, 7, away)
    if fixed != text and set(custom) & {"text", "background", "surface"}:
        warnings.append(f"{label} : le texte {to_hex(text)} est peu lisible sur ce fond ; le site utilise {to_hex(fixed)}.")
    text = fixed

    primary = c["primary"]
    fixed = ensure_contrast(ensure_contrast(primary, bg, 4.5, away), surface, 4.5, away)
    if fixed != primary and "primary" in custom:
        warnings.append(
            f"{label} : la couleur principale {to_hex(primary)} contraste trop peu avec le fond ; "
            f"le site utilise {to_hex(fixed)} pour les liens et les boutons."
        )
    primary = fixed
    on_primary = WHITE if contrast(WHITE, primary) >= contrast(INK, primary) else INK

    secondary = c["secondary"]
    fixed = ensure_contrast(ensure_contrast(secondary, bg, 4.5, away), surface, 4.5, away)
    if fixed != secondary and "secondary" in custom:
        warnings.append(
            f"{label} : la couleur secondaire {to_hex(secondary)} contraste trop peu avec le fond ; le site utilise {to_hex(fixed)}."
        )
    secondary = fixed

    muted = ensure_contrast(mix(text, bg, 0.38), bg, 4.8, text)
    muted = ensure_contrast(muted, surface, 4.6, text)
    dark = mode == "dark"
    return {
        "--bg": to_hex(bg),
        "--surface": to_hex(surface),
        "--surface-2": to_hex(mix(surface, text, 0.07 if dark else 0.045)),
        "--text": to_hex(text),
        "--muted": to_hex(muted),
        "--line": to_hex(mix(bg, text, 0.16 if dark else 0.12)),
        "--accent": to_hex(primary),
        "--accent-rgb": ", ".join(map(str, primary)),
        "--on-accent": to_hex(on_primary),
        "--accent2": to_hex(secondary),
        "--accent2-rgb": ", ".join(map(str, secondary)),
        "--shadow": "0 1px 2px rgba(0,0,0,.3), 0 8px 24px rgba(0,0,0,.28)" if dark
        else "0 1px 2px rgba(20,20,30,.05), 0 8px 24px rgba(20,20,30,.07)",
        "--shadow-lift": "0 2px 4px rgba(0,0,0,.3), 0 16px 36px rgba(0,0,0,.4)" if dark
        else "0 2px 4px rgba(20,20,30,.05), 0 16px 36px rgba(20,20,30,.11)",
        "color-scheme": "dark" if dark else "light",
    }


def font_stack(key: str) -> str:
    family, _, kind = FONTS[key]
    return (f'"{family}", ' if family else "") + FALLBACKS[kind]


def build_theme(site: dict, warnings: list[str]) -> dict:
    tpl = TEMPLATES[site["template"]]
    palette = PALETTES[site["palette"] or tpl["palette"]]
    custom_light = dict(site["colors"])
    custom_dark = dict(site["dark_colors"])
    # Couleur personnalisée en mode clair sans équivalent sombre : on dérive une version plus claire.
    for key in ("primary", "secondary"):
        if key in custom_light and key not in custom_dark:
            rgb = hex_to_rgb(custom_light[key])
            dark_bg = hex_to_rgb(custom_dark.get("background") or palette["dark"]["background"])
            custom_dark[key] = to_hex(ensure_contrast(rgb, dark_bg, 6.5, WHITE))
    light = resolve_mode(palette["light"], custom_light, "light", warnings)
    dark = resolve_mode(palette["dark"], custom_dark, "dark", warnings) if site["dark_mode"] else light

    heading = site["fonts"].get("heading") or tpl["heading"]
    body = site["fonts"].get("body") or tpl["body"]
    mono = tpl["mono"]
    font_vars = {"--font-heading": font_stack(heading), "--font-body": font_stack(body), "--font-mono": font_stack(mono)}
    fonts_url = ""
    if site["google_fonts"]:
        families = []
        for key in dict.fromkeys([heading, body, mono]):
            family, axes, _ = FONTS[key]
            if family:
                families.append("family=" + family.replace(" ", "+") + ":" + axes)
        if families:
            fonts_url = "https://fonts.googleapis.com/css2?" + "&".join(families) + "&display=swap"

    def block(values: dict[str, str]) -> str:
        return ";".join(f"{k}:{v}" for k, v in values.items())

    css = ":root{" + block({**light, **font_vars}) + "}"
    if site["dark_mode"]:
        css += '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){' + block(dark) + "}}"
        css += ':root[data-theme="dark"]{' + block(dark) + "}"
    return {"css": css, "fonts_url": fonts_url, "accent": light["--accent"], "dark_mode": site["dark_mode"]}


# ---------------------------------------------------------------------------
# Chargement du contenu
# ---------------------------------------------------------------------------


def load_site(content_dir: Path, report: Report, assets: set[str]) -> dict:
    path = content_dir / "site.yml"
    if not path.is_file():
        report.error(path, None, "fichier de configuration introuvable.")
        return {}
    text = read_text(path, report)
    if text is None:
        return {}
    data = parse_yaml(text, path, report)
    if data is INVALID:
        return {}
    data = data or {}
    if not isinstance(data, dict):
        report.error(path, None, "le fichier doit contenir des lignes « clé: valeur ».")
        return {}
    f = Fields(data, path, report, content_dir, assets)
    site = {
        "language": f.choice("language", list(I18N), required=False) or "en",
        "template": f.choice("template", list(TEMPLATES), required=False) or "a",
        "title": f.text("title"),
        "description": f.text("description"),
        "base_url": f.text("base_url"),
        "google_fonts": f.boolean("google_fonts", default=True),
        "dark_mode": f.boolean("dark_mode", default=True),
        "palette": f.choice("palette", list(PALETTES), required=False),
        "colors": read_colors(data.get("colors"), path, report, "colors"),
        "dark_colors": read_colors(data.get("dark_colors"), path, report, "dark_colors"),
        "fonts": {},
    }
    # Ancien réglage « accent » : équivalent de colors.primary.
    legacy = f.text("accent")
    if legacy:
        if is_hex(legacy):
            site["colors"].setdefault("primary", legacy if legacy.startswith("#") else "#" + legacy)
        else:
            report.error(path, "accent", f"« {legacy} » n'est pas une couleur hexadécimale (exemple : \"#0f766e\", avec les guillemets).")
    fonts_raw = data.get("fonts") or {}
    if isinstance(fonts_raw, dict):
        for slot, value in fonts_raw.items():
            if slot not in ("heading", "body"):
                report.error(path, f"fonts.{slot}", "réglage inconnu. Réglages possibles : heading (titres), body (texte).")
            elif value not in (None, ""):
                value = str(value).strip().lower().replace(" ", "-")
                if value not in FONTS:
                    report.error(path, f"fonts.{slot}", f"police « {value} » inconnue. Polices possibles : {', '.join(FONTS)}.")
                else:
                    site["fonts"][slot] = value
    else:
        report.error(path, "fonts", "doit contenir « heading: ... » et/ou « body: ... ».")
    if site["base_url"] and not re.match(r"^https?://", site["base_url"]):
        report.error(path, "base_url", "doit commencer par https:// (exemple : https://pseudo.github.io/portfolio/).")
        site["base_url"] = ""
    if site["base_url"] and not site["base_url"].endswith("/"):
        site["base_url"] += "/"

    sections_raw = data.get("sections", {})
    sections = {name: True for name in SECTION_ORDER}
    if isinstance(sections_raw, dict):
        for name, value in sections_raw.items():
            if name not in sections:
                report.error(path, f"sections.{name}", f"section inconnue. Sections possibles : {', '.join(SECTION_ORDER)}.")
            elif not isinstance(value, bool):
                report.error(path, f"sections.{name}", "doit valoir true ou false.")
            else:
                sections[name] = value
    elif sections_raw not in (None, ""):
        report.error(path, "sections", "doit contenir une ligne par section, par exemple « about: true ».")
    site["sections"] = sections
    return site


def load_profile(content_dir: Path, report: Report, assets: set[str], t: dict) -> dict:
    path = content_dir / "profile.md"
    if not path.is_file():
        report.error(path, None, "fichier obligatoire introuvable.")
        return {}
    data, body = read_markdown(path, report)
    if data is None:
        return {}
    f = Fields(data, path, report, content_dir, assets)
    name = f.text("name", required=True)
    email = f.text("email")
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        report.error(path, "email", f"adresse e-mail invalide : « {email} ».")
        email = ""
    phone = f.text("phone")
    show_phone = f.boolean("show_phone", default=False)
    if show_phone and not phone:
        report.warn(path, "show_phone", "vaut true mais aucun numéro n'est renseigné dans « phone ».")
    profile = {
        "name": name,
        "headline": f.text("headline", required=True),
        "location": f.text("location"),
        "availability": f.text("availability"),
        "email": email,
        "phone": phone if show_phone else "",
        "phone_link": re.sub(r"[^\d+]", "", phone) if show_phone else "",
        "photo": f.image("photo"),
        "photo_alt": f.text("photo_alt") or t["photo_alt"].format(name=name),
        "cv_pdf": f.local_file("cv_pdf", f.text("cv_pdf"), kind="fichier PDF") if f.text("cv_pdf") else "",
        "linkedin": f.url("linkedin"),
        "github": f.url("github"),
        "website": f.url("website"),
        "pitch_html": md_to_html(body),
        "initials": "".join(part[0] for part in name.split()[:2]).upper() if name else "?",
    }
    return profile


def load_about(content_dir: Path, report: Report) -> str:
    path = content_dir / "about.md"
    if not path.is_file():
        return ""
    data, body = read_markdown(path, report, frontmatter_required=False)
    return md_to_html(body) if data is not None else ""


def load_skills(content_dir: Path, report: Report, assets: set[str]) -> dict:
    path = content_dir / "skills.md"
    if not path.is_file():
        return {"groups": [], "intro_html": ""}
    data, body = read_markdown(path, report)
    if data is None:
        return {"groups": [], "intro_html": ""}
    groups_raw = data.get("groups") or []
    groups = []
    if not isinstance(groups_raw, list):
        report.error(path, "groups", "doit être une liste de groupes (chaque groupe commence par « - name: »).")
        groups_raw = []
    for i, raw in enumerate(groups_raw, start=1):
        key = f"groups[{i}]"
        if not isinstance(raw, dict):
            report.error(path, key, "chaque groupe doit avoir « name: » et « items: ».")
            continue
        gname = str(raw.get("name") or "").strip()
        if not gname:
            report.error(path, f"{key}.name", "nom du groupe manquant.")
        items_raw = raw.get("items") or []
        if isinstance(items_raw, str):
            items_raw = [s.strip() for s in items_raw.split(",") if s.strip()]
        if not isinstance(items_raw, list):
            report.error(path, f"{key}.items", "doit être une liste de compétences.")
            continue
        items = []
        for j, item in enumerate(items_raw, start=1):
            if isinstance(item, (str, int, float)):
                items.append({"name": str(item).strip(), "level": 0})
            elif isinstance(item, dict) and item.get("name"):
                level = item.get("level", 0) or 0
                if not isinstance(level, int) or not 0 <= level <= 5:
                    report.error(path, f"{key}.items[{j}].level", "le niveau doit être un nombre entier de 1 à 5.")
                    level = 0
                items.append({"name": str(item["name"]).strip(), "level": level})
            else:
                report.error(path, f"{key}.items[{j}]", "écrivez soit « - Python », soit « - name: Python » puis « level: 4 ».")
        if gname and items:
            groups.append({"name": gname, "entries": items, "has_levels": any(i["level"] for i in items)})
    return {"groups": groups, "intro_html": md_to_html(body)}


def load_education(content_dir: Path, report: Report, assets: set[str], t: dict) -> list[dict]:
    path = content_dir / "education.md"
    if not path.is_file():
        return []
    data, _ = read_markdown(path, report)
    if data is None:
        return []
    entries_raw = data.get("entries") or []
    if not isinstance(entries_raw, list):
        report.error(path, "entries", "doit être une liste (chaque formation commence par « - school: »).")
        return []
    entries = []
    for i, raw in enumerate(entries_raw, start=1):
        if not isinstance(raw, dict):
            report.error(path, f"entries[{i}]", "chaque formation doit contenir « school: », « degree: »...")
            continue
        sub = Report(report.content_dir)
        f = Fields(raw, path, sub, content_dir, assets)
        start = f.date("start", required=False)
        end = f.date("end", required=False, allow_present=True)
        entry = {
            "school": f.text("school", required=True),
            "degree": f.text("degree", required=True),
            "location": f.text("location"),
            "logo": f.image("logo"),
            "start": start,
            "end": end,
            "dates": format_range(start, end, t),
            "details_html": md_to_html(f.text("details")),
            "sort": date_key(end or start),
        }
        for message in sub.errors:
            report.errors.append(message.replace("(champ « ", f"(formation n°{i}, champ « ", 1))
        entry["logo_alt"] = t["logo_alt"].format(org=entry["school"])
        entries.append(entry)
    entries.sort(key=lambda e: e["sort"], reverse=True)
    return entries


def md_files(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.glob("*.md") if not p.name.startswith(("_", ".")))


def load_experiences(content_dir: Path, report: Report, assets: set[str], t: dict) -> list[dict]:
    items = []
    for path in md_files(content_dir / "experiences"):
        data, body = read_markdown(path, report)
        if data is None:
            continue
        f = Fields(data, path, report, content_dir, assets)
        start = f.date("start")
        end = f.date("end", allow_present=True)
        if start and end and not end.get("present") and date_key(end) < date_key(start):
            report.error(path, "end", "la date de fin est antérieure à la date de début.")
        etype = f.choice("type", EXPERIENCE_TYPES)
        org = f.text("organisation", required=True)
        items.append(
            {
                "title": f.text("title", required=True),
                "organisation": org,
                "location": f.text("location"),
                "start": start,
                "end": end,
                "dates": format_range(start, end, t),
                "start_iso": iso_date(start),
                "is_current": bool(end and end.get("present")),
                "type": etype,
                "type_label": t.get(f"type_{etype}", etype),
                "logo": f.image("logo"),
                "logo_alt": f.text("logo_alt") or t["logo_alt"].format(org=org),
                "org_initials": "".join(w[0] for w in org.split()[:2]).upper() if org else "",
                "tags": f.text_list("tags"),
                "body_html": md_to_html(body),
                "sort": (date_key(end), date_key(start)),
            }
        )
    items.sort(key=lambda e: e["sort"], reverse=True)
    return items


def load_projects(content_dir: Path, report: Report, assets: set[str], t: dict) -> list[dict]:
    items = []
    seen: set[str] = set()
    for path in md_files(content_dir / "projects"):
        data, body = read_markdown(path, report)
        if data is None:
            continue
        f = Fields(data, path, report, content_dir, assets)
        title = f.text("title", required=True)
        date = f.date("date")
        links_raw = data.get("links") or {}
        links = []
        if isinstance(links_raw, dict):
            for key, value in links_raw.items():
                if key not in ("repo", "demo", "report"):
                    report.error(path, f"links.{key}", "lien inconnu. Liens possibles : repo, demo, report.")
                    continue
                if value:
                    href = f.url(f"links.{key}", str(value).strip())
                    if href:
                        links.append({"kind": key, "label": t[key], "href": href, "external": href.startswith("http")})
        else:
            report.error(path, "links", "doit contenir des lignes « repo: https://... », « demo: ... », « report: ... ».")
        slug = slugify(path.stem)
        if slug in seen:
            report.error(path, None, f"deux projets donnent la même adresse « {slug} ». Renommez l'un des fichiers.")
        seen.add(slug)
        body_html = md_to_html(body)
        items.append(
            {
                "slug": slug,
                "title": title,
                "date": date,
                "date_label": format_date(date, t),
                "date_iso": iso_date(date),
                "category": f.choice("category", PROJECT_CATEGORIES),
                "thumbnail": f.image("thumbnail"),
                "thumbnail_alt": f.text("thumbnail_alt") or t["thumbnail_alt"].format(title=title),
                "tags": f.text_list("tags"),
                "links": links,
                "summary": f.text("summary", required=True),
                "featured": f.boolean("featured"),
                "body_html": body_html,
                "has_page": bool(body.strip()),
                "sort": date_key(date),
            }
        )
    for p in items:
        p["category_label"] = t.get(p["category"], p["category"])
    items.sort(key=lambda p: p["sort"], reverse=True)
    return items


def check_unknown_dirs(content_dir: Path, report: Report) -> None:
    for path in sorted(content_dir.glob("*.md")):
        if path.name not in {"profile.md", "about.md", "skills.md", "education.md"} and not path.name.startswith(("_", ".")):
            report.warn(path, None, "fichier ignoré (seuls profile.md, about.md, skills.md et education.md sont lus à la racine).")


# ---------------------------------------------------------------------------
# Rendu
# ---------------------------------------------------------------------------


def relink(html: str, prefix: str) -> str:
    """Préfixe les liens relatifs du Markdown pour les pages placées dans un sous-dossier."""
    if not prefix:
        return html
    return re.sub(r'(src|href)="(?!https?:|mailto:|tel:|#|/|data:)([^"]+)"', rf'\1="{prefix}\2"', html)


def favicon_svg(initials: str, accent: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        f'<rect width="64" height="64" rx="14" fill="{accent}"/>'
        '<text x="32" y="41" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="26" font-weight="700" fill="#ffffff">{initials}</text></svg>'
    )


def build_pages(template: str, visible: dict[str, bool]) -> list[dict]:
    """Liste des pages HTML à générer pour chaque modèle."""
    if template != "b":
        return [{"file": "index.html", "template": "index.html", "key": "home"}]
    pages = [{"file": "index.html", "template": "index.html", "key": "home"}]
    if visible["about"] or visible["skills"] or visible["education"]:
        pages.append({"file": "about.html", "template": "about.html", "key": "about"})
    if visible["experiences"]:
        pages.append({"file": "experience.html", "template": "experience.html", "key": "experiences"})
    if visible["projects"]:
        pages.append({"file": "projects.html", "template": "projects.html", "key": "projects"})
    if visible["contact"]:
        pages.append({"file": "contact.html", "template": "contact.html", "key": "contact"})
    return pages


def build_nav(template: str, visible: dict[str, bool], pages: list[dict], t: dict) -> list[dict]:
    if template != "b":
        return [
            {"key": s, "label": t[f"nav_{s}"], "href": f"index.html#{s}"}
            for s in SECTION_ORDER
            if visible[s]
        ]
    return [{"key": p["key"], "label": t[f"nav_{p['key']}"], "href": p["file"]} for p in pages]


def safe_clean(out_dir: Path) -> None:
    """Vide le dossier de sortie seulement s'il a été créé par ce script."""
    if out_dir.exists():
        if not (out_dir / BUILD_MARKER).exists() and any(out_dir.iterdir()):
            print(
                f"Erreur : le dossier de sortie {out_dir} existe déjà et n'a pas été créé par build.py.\n"
                "Par sécurité il n'est pas effacé. Choisissez un autre dossier avec --out ou supprimez-le vous-même.",
                file=sys.stderr,
            )
            sys.exit(1)
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    (out_dir / BUILD_MARKER).write_text("Dossier généré par build.py, ne pas modifier à la main.\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Aperçu de tous les modèles côte à côte (--preview-all)
# ---------------------------------------------------------------------------

# Liens du projet d'origine, affichés sur la page galerie (--preview-all).
PROJECT_REPO = "https://github.com/Djamal029/portfolio-markdown-templates"
PROJECT_OWNER = "https://github.com/Djamal029"
# Compteurs publics « combien de personnes ont choisi ce modèle » (service gratuit Abacus, aucune donnée personnelle).
COUNTER_NAMESPACE = "djamal029-portfolio-markdown-templates"
# Modèles mis en avant en tête de la galerie.
GALLERY_FIRST = ["i", "j"]

PREVIEW_TEXT = {
    "a": "Une seule longue page, menu de sections collé en haut, titres à empattements.",
    "b": "Plusieurs pages (accueil, à propos, expériences, projets, contact), grille de cartes.",
    "c": "Profil fixe dans une colonne à gauche, contenu à droite, détails en police à chasse fixe.",
    "d": "Une seule page en tuiles (bento) : grandes cartes lumineuses, projet vedette en double largeur, menu flottant.",
    "e": "Une seule page centrée façon vitrine : grand titre éclairé, frise alternée, projets en grandes rangées.",
    "f": "Une page façon terminal de développeur : fenêtres avec barre de titre, commandes, police à chasse fixe.",
    "g": "Un CV en ligne élégant : une feuille posée sur la page, colonne de contact et de compétences à gauche.",
    "h": "Une page grand format : nom géant, projets qui défilent à l'horizontale, expériences numérotées.",
    "i": "Le plus lumineux : aurores de couleur en fond, cartes en verre dépoli, photo cerclée de lumière, apparitions douces au défilement.",
    "j": "Un portfolio façon magazine : grande photo en ouverture, sommaire numéroté, titres de section qui restent en marge pendant la lecture.",
}


def serve_folder(out: Path, port: int, open_browser: bool) -> int:
    """Sert un dossier sur http://localhost:<port> (module http.server de Python) et ouvre le navigateur."""
    index = out / "index.html"
    import functools
    import http.server
    import socketserver
    import webbrowser

    import socket

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args: Any) -> None:  # pas de journal à chaque requête
            pass

    def port_in_use(number: int) -> bool:
        # Un autre logiciel (serveur web local...) peut déjà écouter sur ce port, en IPv4 ou IPv6.
        for family, host in ((socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")):
            try:
                with socket.socket(family, socket.SOCK_STREAM) as probe:
                    probe.settimeout(0.3)
                    if probe.connect_ex((host, number)) == 0:
                        return True
            except OSError:
                continue
        return False

    handler = functools.partial(QuietHandler, directory=str(out))
    httpd = None
    for candidate in range(port, port + 10):
        if port_in_use(candidate):
            print(f"Port {candidate} déjà utilisé par un autre programme, essai du suivant.", flush=True)
            continue
        try:
            httpd = socketserver.ThreadingTCPServer(("127.0.0.1", candidate), handler)
            break
        except OSError:
            continue
    if httpd is None:
        print(f"Aucun port libre entre {port} et {port + 9}. Ouvrez directement {index}.")
        return 1
    url = f"http://localhost:{candidate}/"
    print(f"Aperçu disponible sur {url}  (Ctrl+C pour arrêter)", flush=True)
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServeur arrêté.")
    finally:
        httpd.server_close()
    return 0


def preview_all(serve: bool, port: int, open_browser: bool = True) -> int:
    out = ROOT / "previews"
    safe_clean(out)
    jobs = [(tpl, lang, folder) for tpl in TEMPLATES for lang, folder in (("en", "content"), ("fr", "content-fr-example"))]
    # Un profil d'exemple différent par modèle (outils/exemples.py), construit dans un dossier temporaire.
    sys.path.insert(0, str(ROOT / "outils"))
    try:
        import exemples
    except ImportError:
        exemples = None
    tmp = Path(tempfile.mkdtemp(prefix="portfolio-exemples-"))
    for tpl, lang, folder in jobs:
        if not (ROOT / folder).is_dir():
            print(f"Dossier {folder}/ absent : aperçu {tpl.upper()} {lang} ignoré.")
            continue
        source = folder
        if exemples is not None and tpl in exemples.PERSONAS:
            source = str(exemples.make_content(tpl, lang, ROOT / folder, tmp / tpl / lang))
        code = main(["--content", source, "--template", tpl, "--language", lang, "--out", f"previews/{tpl}/{lang}", "--quiet"])
        if code:
            return code
        (out / tpl / BUILD_MARKER).write_text("", encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    thumbs = out / "thumbs"
    thumbs.mkdir(exist_ok=True)
    cards, minis = [], []
    order = GALLERY_FIRST + [t for t in TEMPLATES if t not in GALLERY_FIRST]
    for tpl in order:
        info = TEMPLATES[tpl]
        shot = ROOT / "docs-assets" / f"template-{tpl}-desktop.webp"
        img = ""
        if shot.is_file():
            shutil.copy2(shot, thumbs / shot.name)
            img = f'<div class="shot"><img src="thumbs/{shot.name}" alt="Capture du modèle {tpl.upper()}" loading="lazy"></div>'
            minis.append(f'<img src="thumbs/{shot.name}" alt="" style="animation-delay:{0.25 + 0.12 * len(minis):.2f}s">')
        label = f"{tpl.upper()} « {info['name']} »"
        cards.append(
            f'<li class="card{" is-new" if tpl in GALLERY_FIRST else ""}">{img}<div class="body"><h3><span class="letter">{tpl.upper()}</span>{info["name"]}'
            f'{"<span class=\"new\">Nouveau</span>" if tpl in GALLERY_FIRST else ""}</h3>'
            f'<p>{PREVIEW_TEXT[tpl]}</p>'
            f'<p class="count" data-count="template-{tpl}" hidden><span></span></p>'
            f'<div class="links"><a href="{tpl}/en/index.html">Voir · EN</a>'
            f'<a href="{tpl}/fr/index.html">Voir · FR</a>'
            f'<button type="button" class="choose" data-choose="{tpl}" data-label="{label}">Choisir ce modèle</button></div></div></li>'
        )
    page = (ROOT / "outils" / "galerie.html").read_text(encoding="utf-8")
    for key, value in {"%CARDS%": "\n".join(cards), "%MINIS%": "".join(minis), "%COUNT%": str(len(TEMPLATES)),
                       "%REPO%": PROJECT_REPO, "%OWNER%": PROJECT_OWNER, "%COUNTER_NS%": COUNTER_NAMESPACE}.items():
        page = page.replace(key, value)
    index = out / "index.html"
    index.write_text(page, encoding="utf-8")
    print(f"Aperçus générés. Page de choix : {index}")
    if not serve:
        return 0

    return serve_folder(out, port, open_browser)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Génère le portfolio à partir du dossier content/.")
    parser.add_argument("--content", default="content", help="dossier de contenu (défaut : content)")
    parser.add_argument("--out", default="docs", help="dossier de sortie (défaut : docs)")
    parser.add_argument("--template", choices=list(TEMPLATES), help="force le modèle (sinon : valeur de site.yml)")
    parser.add_argument("--language", choices=list(I18N), help="force la langue de l'interface (sinon : site.yml)")
    parser.add_argument("--preview-all", action="store_true", help="génère tous les modèles (anglais et français) et la page galerie dans previews/, puis les ouvre")
    parser.add_argument("--no-serve", action="store_true", help="avec --preview-all : génère sans lancer le serveur local")
    parser.add_argument("--serve", action="store_true", help="après la génération, sert le site sur http://localhost:8000")
    parser.add_argument("--no-open", action="store_true", help="avec --preview-all ou --serve : ne pas ouvrir le navigateur")
    parser.add_argument("--port", type=int, default=8000, help="port du serveur local (défaut : 8000)")
    parser.add_argument("--quiet", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.preview_all:
        return preview_all(serve=not args.no_serve, port=args.port, open_browser=not args.no_open)

    content_dir = (ROOT / args.content).resolve() if not Path(args.content).is_absolute() else Path(args.content)
    out_dir = (ROOT / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
    if not content_dir.is_dir():
        print(f"Erreur : le dossier de contenu « {args.content} » est introuvable.", file=sys.stderr)
        return 1

    report = Report(content_dir)
    assets: set[str] = set()
    site = load_site(content_dir, report, assets)
    if args.template:
        site["template"] = args.template
    if args.language:
        site["language"] = args.language
    site.setdefault("language", "en")
    site.setdefault("template", "a")
    site.setdefault("sections", {s: True for s in SECTION_ORDER})
    for key, default in (("palette", ""), ("colors", {}), ("dark_colors", {}), ("fonts", {}), ("google_fonts", True), ("dark_mode", True)):
        site.setdefault(key, default)
    t = I18N[site["language"]]

    profile = load_profile(content_dir, report, assets, t)
    about_html = load_about(content_dir, report)
    skills = load_skills(content_dir, report, assets)
    education = load_education(content_dir, report, assets, t)
    experiences = load_experiences(content_dir, report, assets, t)
    projects = load_projects(content_dir, report, assets, t)
    check_unknown_dirs(content_dir, report)

    for message in report.warnings:
        print(f"Avertissement : {message}")
    if report.errors:
        print(f"\nLe site n'a pas été généré : {len(report.errors)} erreur(s) à corriger.\n", file=sys.stderr)
        for message in report.errors:
            print(f"  - {message}", file=sys.stderr)
        print("\nCorrigez ces points puis relancez :  uv run build.py", file=sys.stderr)
        return 1

    has_contact = bool(profile["email"] or profile["phone"] or profile["linkedin"] or profile["github"] or profile["website"])
    wanted = site["sections"]
    visible = {
        "about": wanted["about"] and bool(about_html),
        "experiences": wanted["experiences"] and bool(experiences),
        "projects": wanted["projects"] and bool(projects),
        "skills": wanted["skills"] and bool(skills["groups"]),
        "education": wanted["education"] and bool(education),
        "contact": wanted["contact"] and has_contact,
    }

    template_dir = ROOT / "templates" / site["template"]
    if not template_dir.is_dir():
        print(f"Erreur : le modèle « {site['template']} » est introuvable dans templates/.", file=sys.stderr)
        return 1

    theme_warnings: list[str] = []
    theme = build_theme(site, theme_warnings)
    for message in theme_warnings:
        print(f"Avertissement (couleurs) : {message}")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(["html"]),
        undefined=jinja2.StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    pages = build_pages(site["template"], visible)
    nav = build_nav(site["template"], visible, pages, t)
    today = dt.date.today()
    title = site["title"] or (f"{profile['name']}, {profile['headline']}")
    description = site["description"] or f"{profile['name']}: {profile['headline']}"

    safe_clean(out_dir)
    base_ctx = {
        "site": site,
        "title": title,
        "description": description,
        "profile": profile,
        "about_html": about_html,
        "skills": skills,
        "education": education,
        "experiences": experiences,
        "projects": projects,
        "featured": [p for p in projects if p["featured"]] or projects[:3],
        "visible": visible,
        "t": t,
        "lang": site["language"],
        "nav": nav,
        "theme": theme,
        "updated": t["updated"].format(date=format_date({"y": today.year, "m": today.month, "d": 0}, t)),
        "year": today.year,
        "has_academic": any(p["category"] == "academic" for p in projects),
        "has_personal": any(p["category"] == "personal" for p in projects),
    }

    def render(template_name: str, target: str, **extra: Any) -> None:
        depth = target.count("/")
        root = "../" * depth
        ctx = dict(base_ctx, root=root, **extra)
        html = env.get_template(template_name).render(**ctx)
        dest = out_dir / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")

    for page in pages:
        render(page["template"], page["file"], page=page)
    projects_page = "projects.html" if site["template"] == "b" else "index.html#projects"
    for project in projects:
        if project["has_page"]:
            render(
                "project.html",
                f"projects/{project['slug']}.html",
                page={"key": "projects", "file": f"projects/{project['slug']}.html"},
                project=project,
                project_body=relink(project["body_html"], "../"),
                projects_page=projects_page,
            )

    # Fichiers statiques du modèle et fichiers du contenu
    shutil.copytree(template_dir / "static", out_dir / "assets")
    for folder in ("images", "files"):
        if (content_dir / folder).is_dir():
            shutil.copytree(content_dir / folder, out_dir / folder, dirs_exist_ok=True)
    for rel in assets:
        if rel.startswith("http"):
            continue
        dest = out_dir / rel
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(content_dir / rel, dest)
    (out_dir / "favicon.svg").write_text(favicon_svg(profile["initials"], theme["accent"]), encoding="utf-8")
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    count = len(pages) + sum(1 for p in projects if p["has_page"])
    shown = ", ".join(s for s in SECTION_ORDER if visible[s]) or "aucune"
    try:
        out_display = out_dir.relative_to(ROOT).as_posix()
    except ValueError:
        out_display = str(out_dir)
    if args.quiet:
        print(f"Site généré : {out_display}/ (modèle {site['template'].upper()}, langue {site['language']}).")
        return 0
    print(
        f"Site généré : {count} page(s) dans {out_display}/ "
        f"(modèle {site['template'].upper()}, langue {site['language']}, sections : {shown}).\n"
        f"Ouvrez {out_display}/index.html dans votre navigateur pour le voir."
    )
    if args.serve:
        return serve_folder(out_dir, args.port, open_browser=not args.no_open)
    return 0


if __name__ == "__main__":
    sys.exit(main())
