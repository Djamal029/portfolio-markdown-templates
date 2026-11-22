#!/usr/bin/env sh
# Installe ce qu'il faut et affiche le portfolio (Linux, macOS, Git Bash sous Windows).
#
# Utilisation (dans le dossier du portfolio) :
#   sh install.sh               installe uv si besoin, génère le site, l'ouvre
#   sh install.sh preview       idem, puis sert docs/ sur http://localhost:8000
#   sh install.sh preview-all   tous les modèles côte à côte sur http://localhost:8000
#
# Options : --port 8080 (autre port), --no-open (ne pas ouvrir le navigateur), --no-serve (pas de serveur local).
# Le script peut être relancé autant de fois que nécessaire : il ne réinstalle rien d'inutile.

set -u

ACTION="build"
PORT=8000
NO_OPEN=0
NO_SERVE=0

while [ $# -gt 0 ]; do
  case "$1" in
    build|preview|preview-all) ACTION="$1" ;;
    --port) shift; PORT="${1:-8000}" ;;
    --no-open) NO_OPEN=1 ;;
    --no-serve) NO_SERVE=1 ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    *) printf 'Option inconnue : %s (voir : sh install.sh --help)\n' "$1"; exit 1 ;;
  esac
  shift
done

if [ -t 1 ]; then C_STEP='\033[36m'; C_OK='\033[32m'; C_ERR='\033[31m'; C_END='\033[0m'
else C_STEP=''; C_OK=''; C_ERR=''; C_END=''; fi
step() { printf "${C_STEP}==> %s${C_END}\n" "$1"; }
ok() { printf "${C_OK}    %s${C_END}\n" "$1"; }
fail() { printf "\n${C_ERR}Erreur : %s${C_END}\n" "$1"; exit 1; }

cd "$(dirname "$0")" || fail "impossible d'ouvrir le dossier du script."
[ -f build.py ] || fail "build.py est introuvable. Lancez ce script depuis le dossier du portfolio."

find_uv() {
  if command -v uv >/dev/null 2>&1; then command -v uv; return 0; fi
  for candidate in "$HOME/.local/bin/uv" "$HOME/.cargo/bin/uv" "$HOME/.local/bin/uv.exe" "$HOME/.cargo/bin/uv.exe"; do
    if [ -x "$candidate" ]; then printf '%s\n' "$candidate"; return 0; fi
  done
  return 1
}

open_target() {
  [ "$NO_OPEN" -eq 1 ] && return 0
  if command -v open >/dev/null 2>&1 && [ "$(uname -s)" = "Darwin" ]; then open "$1"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$1" >/dev/null 2>&1 &
  elif command -v cmd.exe >/dev/null 2>&1; then cmd.exe /c start "" "$1" >/dev/null 2>&1
  else printf '    Ouvrez vous-même : %s\n' "$1"
  fi
}

printf '\nPortfolio Markdown : installation et aperçu\n\n'

# 1. uv
step "Recherche de uv (gestionnaire Python)"
if UV="$(find_uv)"; then
  ok "uv est déjà installé : $UV"
else
  step "uv absent : installation avec l'installateur officiel (astral.sh)"
  if command -v curl >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh || fail "l'installation de uv a échoué. Vérifiez la connexion Internet ou voir https://docs.astral.sh/uv/"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- https://astral.sh/uv/install.sh | sh || fail "l'installation de uv a échoué. Vérifiez la connexion Internet ou voir https://docs.astral.sh/uv/"
  else
    fail "ni curl ni wget ne sont disponibles pour télécharger uv. Installez curl puis relancez."
  fi
  PATH="$HOME/.local/bin:$PATH"; export PATH
  UV="$(find_uv)" || fail "uv semble installé mais reste introuvable. Ouvrez un nouveau terminal et relancez ce script."
  ok "uv installé : $UV"
fi
ok "Version : $("$UV" --version)"

# 2. Aperçu de tous les modèles
if [ "$ACTION" = "preview-all" ]; then
  step "Génération de tous les modèles dans previews/"
  set -- --preview-all --port "$PORT"
  [ "$NO_OPEN" -eq 1 ] && set -- "$@" --no-open
  [ "$NO_SERVE" -eq 1 ] && set -- "$@" --no-serve
  "$UV" run build.py "$@" || fail "la génération des aperçus a échoué (voir les messages ci-dessus)."
  exit 0
fi

# 3. Génération du site
step "Génération du site (content/ vers docs/)"
"$UV" run build.py || fail "le site n'a pas été généré. Corrigez les points indiqués ci-dessus puis relancez le script."
INDEX="$(pwd)/docs/index.html"
ok "Site prêt : $INDEX"

# 4. Ouverture
if [ "$ACTION" = "build" ]; then
  step "Ouverture dans le navigateur"
  open_target "$INDEX"
  printf '\nTerminé. Après chaque modification de content/, relancez ce script (ou : uv run build.py).\n'
  exit 0
fi

[ "$NO_SERVE" -eq 1 ] && exit 0
step "Aperçu local (serveur http.server de Python, Ctrl+C pour arrêter)"
# build.py choisit le port suivant si $PORT est déjà pris par un autre programme.
set -- --serve --port "$PORT"
[ "$NO_OPEN" -eq 1 ] && set -- "$@" --no-open
"$UV" run build.py "$@" \
  || fail "le serveur local n'a pas pu démarrer (port $PORT déjà utilisé ?). Essayez : sh install.sh preview --port 8080"
