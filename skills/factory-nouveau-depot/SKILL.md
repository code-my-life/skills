---
name: factory-nouveau-depot
description: Créer un dépôt de code-my-life et le brancher sur la software factory, du dépôt modèle au contrôle final. Passage obligatoire pour tout nouveau dépôt que la factory gère.
disable-model-invocation: true
---

# Nouveau dépôt de la factory

Tout dépôt que la factory gère passe par cette procédure (ADR 0023). Elle repose sur trois pièces de
hermes-software-factory :
- **le dépôt modèle** `code-my-life/repo-template`, un dépôt comme les autres, cloné dans `~/perso/repo-template` :
  README, LICENSE MIT, un `AGENTS.md` à compléter, `CODEOWNERS`, le workflow « Conventions » et `docs/decisions/`.
  Les modèles d'issues et de PR et `SECURITY.md` n'y sont pas : le dépôt spécial `code-my-life/.github` les fournit par
  défaut à tous les dépôts de l'organisation ;
- **`scripts/factory-repo.py`**, qui pose ce que GitHub ne recopie pas d'un modèle, puis vérifie le tout ;
- **`factory.yaml`**, et les quatre listes qui recopient ses projets.

Lance les commandes depuis `~/perso/hermes-software-factory`. `factory-repo.py` retire lui-même `GH_TOKEN` et
travaille avec le gh du propriétaire.

## 1. Le gril

Cherche d'abord toi-même ce qu'un dépôt voisin de même stack fait déjà. Puis pose les décisions en QCM (outil
AskUserQuestion), ta recommandation en premier :
- **le nom** du dépôt, et sa description en une phrase ;
- **public ou privé**.
  - Public : rulesets, auto-merge, analyse des secrets, types d'issues.
  - Privé, sur l'offre gratuite : rien de tout cela, et la release fusionne après l'approbation (`merge: factory`).
- **les types d'issues** (`types: true`), pour un dépôt public seulement ;
- **la CI** : un modèle de `code-my-life/.github` (`workflow-templates/`), ou aucune pour l'instant ;
- **les commandes des contrôles** : `pre-commit`, `pre-push`, `install`, `test-one`, `coverage`, `offline-build` (leur
  sens est en tête de `factory.yaml`).

## 2. Créer

1. Mets ton clone du modèle à jour : `git -C ~/perso/repo-template pull --ff-only`.
2. Crée le dépôt : `python3 scripts/factory-repo.py create code-my-life/<nom> --description "<phrase>" --types`.
   - Le choix du gril est explicite : `--types` pour un dépôt public à types, `--sans-types` pour un dépôt public sans
     types, `--private` pour un dépôt privé, qui n'a jamais de types.
   - Sans types, le script retire du modèle le workflow « Conventions », qui ne juge que des PR typées.
   - Il clone le dépôt dans `~/perso/<nom>`, avec l'identité de l'App pour les commits.
3. Complète `README.md` et `AGENTS.md` (chaque `<à compléter>`), ajoute la CI choisie, puis commite et pousse sur main.
   C'est le seul push direct : les rulesets de l'étape « Configurer » l'interdisent ensuite.

## 3. Inscrire dans la factory

Inscris le projet avant de le configurer : `configure` et `check` lisent ses types dans `factory.yaml`. Sur une
branche de hermes-software-factory, liée à son issue :
1. Ajoute le projet dans `factory.yaml` : `projects`, avec `types: true` pour un dépôt public à types, et son bloc
   `checks`.
2. Mets à jour les quatre listes :
   - `PROJECTS` de `scripts/github-issue-to-card.py` ;
   - les boucles de `scripts/intake-poll.sh` et de `scripts/factory-watch.sh` ;
   - les liens de `scripts/graphs-index.sh`.

   `tests/test_projects.py` échoue si une liste ne suit pas, et son premier test nomme chaque dépôt.
3. Lance `python3 -m unittest discover -s tests`, puis ouvre la PR.

## 4. Configurer

Depuis la branche d'inscription, lance `python3 scripts/factory-repo.py configure code-my-life/<nom> --types`, avec
le même choix qu'à la création, et un `--check "<nom exact d'un job de la CI>"` par check requis en plus de
« Conventions » et de `factory/gate`.
- Le script pose, seulement là où il trouve un écart :
  - les réglages de fusion ;
  - la sécurité ;
  - le jeton des workflows en lecture ;
  - les labels de la factory et, avec les types, ceux des types ;
  - les webhooks vers Hermès ;
  - les rulesets : « main » sur tout dépôt public, « noms de branches » en plus avec les types.
- Les checks que main exige déjà restent exigés. `--retirer-check` en retire un qui n'est pas du standard.
- Puis il vérifie le résultat. Une inscription qui manque encore sur main est signalée, sans faire échouer la
  commande.
- `--dry-run` montre d'abord ce qu'il ferait.
- Le secret d'un webhook ne s'affiche jamais.

## 5. Déployer

1. Après la fusion de la PR d'inscription, lance `./install.sh` : il pose les hooks git du clone, les scripts et
   `checks.json`.
2. Crée le projet Hermès : `hermes project create "<nom>" ~/perso/<nom> --slug <nom> --board factory`, puis, quand le
   dépôt a ses commandes, `hermes verify --save ~/perso/<nom>`.

## 6. Vérifier

1. Relance `python3 scripts/factory-repo.py configure code-my-life/<nom>`, cette fois sans choix explicite :
   `factory.yaml` décide. Il doit répondre « rien à changer sur GitHub ».
2. Lance `python3 scripts/factory-repo.py check code-my-life/<nom>` : il doit répondre « conforme au standard de la
   factory ».

`install.sh` refait ce contrôle pour chaque projet et signale chaque écart.

## Changer le standard

- Un fichier commun : modifie-le dans `~/perso/repo-template`, puis commite et pousse.
- Un réglage : modifie les constantes et `standard()` de `factory-repo.py`, avec leurs tests.

Dans les deux cas, lance ensuite `check` sur chaque projet de `factory.yaml`.
