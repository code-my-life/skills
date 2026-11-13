---
name: factory-onboard
description: "Préparer un repo pour la factory : clone Linux, projet Hermès lié au board, hermes verify, AGENTS.md, vérification des CLI, graphe Graphify, blocage si un outil ou une clé manque. Rend la factory agnostique à la stack."
version: 0.1.0
author: code-my-life + Hermès Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [factory, onboarding, tooling, graphify]
    category: software-development
---


# factory-onboard

Carte d'onboarding d'un repo `OWNER/REPO`. Résultat : le repo est prêt à recevoir des cartes d'implémentation. Une fois par repo, puis à chaque fois que `hermes verify` échoue ou que la stack change.

1. `kanban_show()` : `repo`, `path` souhaité (défaut `~/perso/<nom>`), `project_slug`.
2. Clone Linux (jamais `/mnt/c`) : `gh repo clone OWNER/REPO <path>` ou `git -C <path> pull --ff-only` si présent. `git remote -v` doit pointer sur l'org.
3. Projet Hermès : `hermes project create "<nom>" <path> --slug <slug> --board factory` s'il n'existe pas (`hermes project list`).
4. Détection : `hermes verify --detect-only <path> --json` puis `hermes verify --save <path>` (écrit `.hermes/environment.json`). Si la détection est incomplète (monorepo pnpm, Docker, e2e Playwright), complète le manifeste à la main et relance `hermes verify`. Bootstrap, test, typecheck, build et start doivent passer une fois ici ; sinon bloque avec la sortie.
5. Outillage : pour chaque CLI requis par le manifeste et par `package.json` / `pyproject` / `docker-compose` (node, pnpm, npm, docker, playwright, gh, python, uv, …) : `command -v`. Manquant = `kanban_block(kind="capability", reason="installer <outil> : <commande d'installation>")`. Ne l'installe pas toi-même sans que le brief l'autorise.
6. `AGENTS.md` à la racine (20 000 caractères max, en français), **passé par le formateur du repo avant commit** (`prettier --write`, `eslint --fix`, ou ce que `package.json` déclare : un fichier de doc qui casse `format:check` est un échec) : description en 5 lignes, commandes exactes (bootstrap, test, test d'un seul fichier, typecheck, build, start, e2e), conventions (gestionnaire de paquets, style, messages de commit), échecs connus de la suite, interdits du repo, chemins sensibles. Dépôt public aux types d'issues (`types: true` dans `factory.yaml`) : une issue Documentation dans le dépôt, puis une branche `docs/<n>-agents-md` et une PR au standard du type ; le ruleset « noms de branches » refuse toute autre branche. Ailleurs, sans types, le dépôt n'a ni ce ruleset ni le workflow « Conventions » (`factory-repo.py` ne les pose qu'avec les types) : une branche `factory/onboarding`, PR vers main avec `--fill`.
7. Graphe : `graphify extract <path> --code-only --out <path>/graphify-out --no-gitignore`, puis `graphify cluster-only <path>/graphify-out --no-label`, puis **nommage des communautés** : `~/.hermes/scripts/graphify-label.sh <path>/graphify-out` (modèle local du reviewer fixe ; sans ça le viewer affiche « Community N », inutilisable pour un humain). graphify écrit dans `<out>/graphify-out/`. Vérifie que `graphify-out/` est ignoré par git.
8. Contrat PR : `gh repo view OWNER/REPO --json isPrivate,visibility`. Public : propose dans le handoff la branch protection (check requis = job de test) et `completion_contract: OWNER/REPO`. Privé : `local-only`.
9. Remets le clone principal sur `main` (`git checkout main`) : la branche de l'onboarding est poussée, la PR suffit. Ajoute `.hermes/` et `graphify-out/` à `.git/info/exclude` s'ils ne sont pas ignorés par le repo. Arrête les conteneurs que tu as démarrés pour les tests (`docker compose down`) sauf si le brief dit de les laisser.
10. **CI verte obligatoire** : `gh pr checks <url> --watch --fail-fast` doit terminer sans échec. Rouge = corrige (format, lint), pousse, relance la vérification. Tu ne termines jamais une carte dont la PR a un check en échec ; si la cause t'échappe, `kanban_block(kind="needs_input")` avec l'URL du check.
11. `kanban_complete(summary="repo prêt : <path>, projet <slug>, manifeste, AGENTS.md (PR <url>), graphe", metadata={"path": ..., "project": ..., "recipe": {...}, "clis": {...}, "visibility": ..., "contract": ...})`.
