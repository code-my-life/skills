---
name: factory-cli-lane
description: "Lane d'implémentation déléguée à un CLI externe (Claude Code via claude -p, OpenCode via opencode run) : Hermès reste propriétaire de la carte, le CLI est une entrée non fiable, Hermès relance les tests et fait le handoff."
version: 0.1.0
author: Clément Devillez (code-my-life) + Hermès Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [factory, claude-code, opencode, kanban, lane]
    category: software-development
---


# factory-cli-lane

S'applique aux profils `coder-claude`, `coder-opencode`, et, pour la partie Claude, `coordinator-claude` (section « mode Claude » du skill factory-brief : même contrat, Claude produit, Hermès vérifie et écrit sur le board). La revue et la release ne sont jamais confiées à un CLI : ce sont des scripts de la factory (ADR 0015). Le modèle est toujours `claude_model` du brief, identifiant exact.

Contrat identique au skill upstream `kanban-codex-lane` : le dispatcher spawne Hermès (toi), jamais le CLI. Tu décides si la carte convient, tu prépares le worktree, tu lances le CLI, tu réconcilies le diff, tu vérifies, tu fais le handoff. Le CLI n'appelle jamais un outil `kanban_*`.

## Préconditions (sinon `kanban_block(kind="capability")`)

- `coder-claude` : `command -v claude` et `claude auth status` ok (abonnement Claude, jamais freellmapi, jamais `ANTHROPIC_BASE_URL`).
- `coder-opencode` : `command -v opencode` et `opencode auth list` montre `freellmapi` ; `~/.config/opencode/opencode.json` déployé par install.sh.
- Carte bornée : un brief factory-brief, des commandes de test connues, un worktree.

## Déroulé

1. Étapes 0 et 1 de `factory-author-proof` toi-même (orientation, test fail-first prouvé sur la base). Le CLI ne touche pas au test fail-first.
2. Écris le brief dans `evidence/brief.md` en ajoutant en tête : « Ne modifie pas <fichier de test>. Ne lance pas git push, git commit, git add . Ne touche pas aux fichiers hors : <liste>. Travaille uniquement dans ce dossier. »
3. Lance le CLI dans le worktree, en arrière-plan avec timeout :
   - Claude Code : le modèle est **celui du brief** (`claude_model`), identifiant exact, pas d'alias, et chaque lane porte un nom : `claude -p "$(cat evidence/brief.md)" --name "Implémentation : <objet>" --model <claude_model> --allowedTools "Read,Edit,Write,Bash(npm *),Bash(pnpm *),Bash(node *),Bash(git diff*),Bash(git status*)" --max-turns 40 --output-format json > evidence/10-claude-run.json 2> evidence/10-claude-stderr.txt`
     - `--name "<Rôle> : <objet>"` (ADR 0018) : `Implémentation` pour le travail du brief, `Correction` pour une reprise après un refus du hook, de la gate ou de la revue, `Tests` pour des tests seuls. L'objet dit en 60 caractères au plus ce que fait cette lane : « Correction : ordre des groupes par nom de projet ». Chaque relance du CLI est une nouvelle lane, avec son propre nom. factory-live affiche ce nom dans la transcription ; coder-guard refuse un `claude -p` sans nom au bon format.
   - OpenCode : `opencode run "$(cat evidence/brief.md)" --model freellmapi/agnes-2.5-flash > evidence/10-opencode-run.txt 2>&1`
   `kanban_heartbeat` toutes les 5 minutes pendant l'exécution.
4. Réconcilie : `git status`, `git diff` dans `evidence/11-cli-diff.patch`. Rejette tout fichier hors liste (`git checkout -- <fichier>`), toute modification du test fail-first, toute assertion affaiblie, tout timeout allongé. Note chaque rejet dans le handoff.
5. Reprends `factory-author-proof` à l'étape 2.3 (le test passe), puis 2.4 (mutation check), 3 (suite complète), 4 (commits et `kanban_request_review` avec `metadata.harness`).
6. Si le CLI échoue ou produit un diff inutilisable deux fois : `kanban_block(kind="transient", reason="lane <cli> inutilisable : <détail>")`. Le coordinateur réassignera à `coder`.
