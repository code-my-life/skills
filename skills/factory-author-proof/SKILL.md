---
name: factory-author-proof
description: "Preuve d'auteur : test qui échoue sur le commit de base, correctif minimal, test qui passe, mutation check, preuves sur disque, handoff vers la gate scriptée. Pour toute carte d'implémentation."
version: 0.1.0
author: Clément Devillez (code-my-life) + Hermès Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [factory, tdd, evidence, kanban]
    category: software-development
---


# factory-author-proof

Tu implémentes une carte dont le brief suit le gabarit factory-brief. Résultat attendu : une branche, une PR, des preuves sous `evidence/`, et une demande de revue à la gate scriptée (`factory-gate`, du code, sans LLM). Tu ne marques jamais ta carte `done` toi-même : elle se termine à la fusion de sa PR, et coder-guard refuse `kanban_complete`.

## 0. Orientation

0. **Lis tout le brief**, jusqu'à sa dernière section « Issue, recopiée mot pour mot par la factory » (ADR 0019) : elle fait foi. La gate vérifie les tests de sa section « Tests » ; la revue juge l'Attendu, les Règles chiffrées et « Ne change pas ». Un brief sans cette section : lis l'issue (`python3 ~/.hermes/scripts/factory-trusted-thread.py <issue>`).
1. `kanban_show()` puis `cd $HERMES_KANBAN_WORKSPACE`. Vérifie que c'est un worktree git (`git rev-parse --show-toplevel`) sur la branche `$HERMES_KANBAN_BRANCH`. Sinon, crée-le depuis le clone du projet, `~/perso/<dépôt>` (par exemple `~/perso/factory-live`) : `git -C ~/perso/<dépôt> fetch origin`, puis `git -C ~/perso/<dépôt> worktree add $HERMES_KANBAN_WORKSPACE -b <branch_name du brief> <base_commit>` (`origin/main` si le brief ne donne pas de sha). Ne clone jamais le dépôt ailleurs : les hooks git de la factory ne tournent que dans ce clone, et coder-guard refuse `git clone`.
2. **Base fraîche** : `git fetch origin && git rebase origin/main` (branche pas encore poussée) avant d'écrire quoi que ce soit ; ton `base_commit` réel est alors `origin/main` du moment, note-le dans le handoff s'il diffère du brief. Le hook git `pre-push` de la factory refuse un push si la branche est en retard sur `origin/main` ou sur sa propre branche distante ; une fois la branche poussée, on rattrape `main` par `git merge origin/main`, jamais par rebase ni force push.
3. Les commandes du projet sont dans la section « Commandes de vérification (factory.yaml) » du brief, écrite par la factory : installation, hooks, un test, couverture, build, bout en bout. `AGENTS.md` et `.hermes/environment.json` du repo les complètent. Lance l'installation.
4. `mkdir -p evidence && grep -qx 'evidence/' .git/info/exclude 2>/dev/null || echo 'evidence/' >> "$(git rev-parse --git-path info/exclude)"` : les preuves ne sont **jamais** commitées (le hook `pre-commit` refuse un commit qui les indexe) ; elles voyagent par le handoff Kanban (`artifacts`) et par les commentaires de revue.
5. Branche lisible : la `branch_name` du brief. Si le worktree est sur une autre branche, `git checkout -b <branch_name du brief>` (le worktree technique reste en place).

## 1. Test fail-first

1. **Ajoute** le cas de test nommé dans le brief (nouveau `test(...)`/`it(...)` dans le fichier indiqué, ou nouveau fichier). Un test qui existe déjà et passe n'est pas le test fail-first : si le cas n'est pas encore écrit, l'écrire est cette étape, pas une raison de bloquer. Lance uniquement ce fichier. Le nouveau cas **doit échouer** (le reste du fichier peut passer). Sauvegarde la sortie : `... > evidence/01-test-fails-on-base.txt 2>&1`.
2. Si le **nouveau cas** passe déjà sur la base (après l'avoir réellement écrit et lu la sortie) : le brief est faux ou le bug est ailleurs. `kanban_comment` avec la sortie, puis `kanban_block(kind="needs_input", reason="le test fail-first passe sur la base : <détail>")`. Ne « corrige » pas le test pour qu'il échoue.

### 1bis. PR de tests (brief avec `test_only: true`)

Le brief ajoute des tests sur un comportement qui marche déjà : aucun test ne peut être rouge sur la base sans tricher. La preuve fail-first devient un **sabotage** par scénario, et les étapes 1, 2 et la section 2 ci-dessous ne s'appliquent pas.

1. Pour chaque scénario du brief, le patch de sabotage indiqué (ou un équivalent qui casse le même comportement) est écrit sous `evidence/sabotage/<scénario>.patch`, jamais commité. Il casse **le code de l'app** (source, ou bibliothèque embarquée comme `mod/assets/systems-generator/`), **jamais le test** : supprimer, inverser ou dérouter une assertion rend n'importe quel test rouge et ne prouve rien (le verrou le refuse).
2. **Commite ton travail avant de saboter.** Applique et retire un sabotage uniquement par `git apply <patch>` et `git apply -R <patch>` ; jamais `git checkout <fichier>`, `git restore` ni `git stash` : ils remettent le fichier au dernier commit et effacent ton travail non commité (cause du blocage de claude-cockpit #42 le 2026-10-19). `git diff --stat` doit être vide entre deux sabotages.
3. Sur la tête de branche avec le patch appliqué (`git apply`), le scénario est **rouge** ; patch retiré (`git apply -R`), il est **vert**. Sortie des deux passages : `evidence/01-sabotage-red.txt` et `evidence/02-tip-green.txt`, un bloc par scénario, qui commence par l'id du scénario. Les e2e Electron se lancent en local sous écran virtuel (`xvfb-run -a npm run test:e2e`) : itère en local, puis confirme dans le job CI de la PR, qui fait foi.
   Le script `python3 ~/.hermes/scripts/factory-sabotage-replay.py --out evidence` fait ces deux passages pour tous tes patchs, dans un worktree jetable, sans toucher ton espace de travail : préfère-le à une boucle à la main.
4. Un scénario qui reste vert sous sabotage n'affirme rien : renforce ses assertions, jamais le sabotage.
5. Un scénario **rouge sans sabotage** révèle un bug de l'app : tu ne modifies pas l'app pour le faire passer. Retire le scénario de la PR, `kanban_comment` avec la sortie et le fichier:ligne en cause ; il partira avec le correctif.
6. Côté app, seuls changements admis : attributs `data-testid`, sondes et coutures actives uniquement sous le mode test du repo. Tout autre changement de code source = blocage `needs_input`. Jamais de changement de structure pour accommoder un test : point d'entrée, `"type"` ou `"exports"` d'un `package.json`, fichier source renommé ou supprimé (le verrou les refuse). Un test qui exige ça est mal écrit : adapte le test (ex. `__dirname` plutôt que `import.meta.url` dans un harnais CommonJS).
7. Aucune montée de version dans une PR de tests, même si le brief en demande une (le verrou la refuse) : le fichier de version déclenche le tag et la release. Hors PR de tests : une seule fois, celle du brief, pas à chaque tour.

### 1ter. Issue typée (brief avec `- type :`, ADR 0017)

Le type du brief fixe la preuve :
- **bug, interface, fonctionnalite** : le test fail-first ci-dessus ;
- **tests** : la PR de tests (1bis) ;
- **maintenance** : aucun test fail-first ; tu ne modifies, ne renommes ni ne retires **aucun test existant** (la gate
  refuse sinon), la suite complète reste verte ;
- **documentation** : aucun test ; tu ne touches **que des documents** (`*.md`, `docs/`), la gate refuse tout autre
  fichier.
- **skill** : aucun test fail-first ; dans le fichier nommé par le brief, tu remplaces le texte d'origine par le texte
  proposé, tels quels, et rien d'autre dans ce fichier (une skill nouvelle : un fichier nouveau qui porte le texte
  proposé). Tu montes la version de `package.json`, celle du brief : `patch`, ou `minor` pour une skill nouvelle. La
  gate compare le fichier à sa base avec ce seul remplacement, et la CI du dépôt fait ses contrôles (tests, catalogue,
  copies identiques à leur amont).

## 2. Correctif minimal

1. Modifie uniquement les fichiers listés dans « fichiers impactés ». Tout fichier hors liste est noté dans le handoff avec la raison.
2. Interdits du brief, sans exception. Si un interdit semble nécessaire, bloque et explique.
3. Relance le test : il passe. `evidence/02-test-passes-on-tip.txt`.
4. Mutation check : retire ou inverse le garde que tu viens d'ajouter, relance, le test redevient rouge, remets le garde. `evidence/03-mutation-check.txt` (les deux sorties).

## 3. Vérification complète

1. Suite complète + typecheck + build, commandes du repo. `evidence/04-full-suite.txt`, `evidence/05-typecheck.txt`, `evidence/06-build.txt`.
2. Changement visible (UI, CLI, fichier produit) : mesure la sortie réelle, pas un proxy. UI : `agent-browser` aux largeurs 390 et 1280, thèmes clair et sombre, captures sous `evidence/ui/`. Fichier produit : relis les octets. Son ou animation : enregistre.
3. Mesures de temps : uniquement machine au repos (`uptime` load < nombre de cœurs / 2), sinon note « non mesuré ».

## 4. Commits et handoff

1. Commits atomiques, messages en français, fichiers ajoutés un par un (`git add <fichier>`, jamais `git add .`). Les **hooks git de la factory** contrôlent chaque commit et chaque push, avec les commandes de `factory.yaml` (jamais celles de ta branche) :
   - `pre-commit` (90 s au plus) : règles du diff indexé (preuves commitées, `.only`/`.skip`, tests factices, assertions retirées, TDD, identité du bot ; un test qui garde son nom garde toutes ses vérifications, même si d'autres tests en ajoutent : sinon « tests affaiblis »), puis format des fichiers indexés, lint et typecheck ;
   - `pre-push` (300 s au plus) : seule la tête de ta branche part, d'un arbre propre (commite ou range tout le reste), branche à jour, puis la suite rapide du projet, puis la **gate locale** (ADR 0019) : les règles de la gate qui n'attendent ni PR ni CI (branche, version, tests nommés de l'issue, diff, conventions, test fail-first vert sur ta tête, couverture du diff), tous les rouges listés d'un coup. Lance-la aussi à la demande : `python3 ~/.hermes/scripts/factory-gate.py --local`.
   - conventions du code (ADR 0016), sur tes lignes ajoutées ou modifiées : commentaires et docstrings **en anglais**, aucun nom de personne dans un commentaire ou un titre de test, pas de TODO sans issue (`TODO(#42)`), pas de `debugger` oublié.
   Un refus affiche la commande rouge et la fin de sa sortie : corrige, puis recommence. Ne contourne jamais un hook (`--no-verify`, `git commit -n`, `core.hooksPath`, `GIT_CONFIG_*` : coder-guard les refuse) : la gate refait ces contrôles sur la PR. Un hook qui dépasse son budget n'est pas de ta faute : `kanban_block(kind="capability")` en citant son message.
2. Bump de version selon `version_bump` du brief, dans le fichier de version du repo, dans un commit dédié `chore: version X.Y.Z` (jamais `npm version`).
3. Push de la branche lisible : `git push -u origin <branch_name>`, puis PR **en brouillon** : écris d'abord `evidence/pr-body.md` (outil d'écriture, ou commande à part), puis lance seul `gh pr create --draft --base main --title "<type>: <titre>" --body-file evidence/pr-body.md`. Sur un brief typé, coder-guard lit ce fichier et refuse un titre ou un texte que la gate refuserait (règle Type), avec la liste des manques ; un texte que la commande fabrique elle-même (`$(…)`, heredoc) est refusé, faute de pouvoir être lu avant. Le corps contient `Fixes #<n>`, ce qui change, ce qui est prouvé (chemins evidence/), ce qui n'est pas prouvé, le bump de version. Note l'URL : `metadata.pr_url`.
   - **Brief typé** (`- type :`, ADR 0017) : le titre est `<préfixe>: <titre>`, le préfixe de ta branche (fix, interface, feat, test, chore, docs). Le corps reprend exactement ces sections, dans cet ordre :
     ```
     Fixes #<n>

     ## Ce qui a été fait
     ## Critères
     - C1 : <la preuve : nom du test, mesure ou capture, avec le chemin evidence/>
     - C2 : non prouvé : <pourquoi>
     ## Preuves
     ## Ce qui n'est pas prouvé
     ## Version
     ```
     plus la section du type : `## Reproduction` (bug), `## Captures` (interface : les captures refaites, avant et après), `## Sabotages` (tests), `## Invariant` (maintenance), `## Documents` (documentation). **Une ligne par critère du brief**, avec son numéro : la gate et le job « Conventions » refusent une PR à laquelle il en manque une. « non prouvé » se dit, il ne se tait pas. La PR reste en brouillon tant que la gate ne l'a pas validée : c'est elle qui la passe en « prête » et demande la revue de Clément.
   - **Un visuel dans « Ce qui a été fait »** (d'après `pr` de mattpocock/skills) : le plus petit qui montre le
     changement, en bloc de texte : un arbre de composants, le diff d'un arbre de fichiers ou un arbre d'appels. Aucune
     règle de la gate ne le vérifie.
   - **Push ou `gh pr create` refusé** (`Authentication failed`, `Invalid username or token`, 403, réseau) : relance une fois, telle quelle (le wrapper `gh` demande un jeton neuf à chaque appel). Si c'est encore refusé : `kanban_block(kind="capability", reason="push refusé : <sortie exacte>")`. Jamais de demande de revue sans branche poussée : coder-guard la refuse (refs locales), la gate rend rouge une revue sans PR, et taire un échec de push est une faute (incident claude-cockpit#25).
4. Avant de demander la revue, tout ton travail est commité et poussé : coder-guard refuse la demande tant que `git status` liste un fichier modifié, indexé ou nouveau que git n'ignore pas (ADR 0020). La gate locale est verte (le hook `pre-push` l'a lancée sur ce que tu as poussé). Puis `kanban_request_review(` **sans reviewer** (aucun agent ne relit : la gate scriptée prend la carte ; Hermès refuse un relecteur qui n'est pas un profil, et coder-guard refuse tout reviewer), `summary="<2 phrases : ce qui a été fait, ce qui est prouvé>", metadata={"branch": "...", "base_commit": "...", "tip_commit": "...", "commits": [...], "changed_files": [...], "tests_run": N, "evidence": ["evidence/01-...", ...], "not_claimed": ["<ce que tu n'as pas prouvé>"], "pr_url": "<URL de la PR, obligatoire si la carte a un contrat PR>", "harness": "<coder|coder-claude|coder-opencode>"})`.
5. Si tu as repéré un fichier qui collisionne avec d'autres cartes : `kanban_comment("hotspot: <chemin> : <raison>")` et répète-le dans `metadata.hotspots`.

## Si ta carte revient de la revue

La gate scriptée (ou Clément sur la PR) t'a renvoyé la carte. Le dernier commentaire de `factory-gate` dans `kanban_show()` donne **toutes** les règles rouges du verdict, avec pour chacune les faits, quoi faire et l'extrait de log : corrige-les toutes dans le même commit (ADR 0019). Une demande de Clément donne le lien de sa revue. Ce que la gate vérifie, dans cet ordre, en jugeant chaque règle :

1. **PR** : une PR ouverte par l'App, sur la branche nommée par le brief (`branch_name`) ; brief typé : **Type**, la branche, le titre, `Fixes #<n>`, les sections et une ligne de preuve par critère (corrige avec `gh pr edit --title` ou `--body-file`, sans nouveau commit) ; **Demande de changements** : si la dernière décision du propriétaire est une demande de changements sur la tête de la PR, la gate reste rouge tant que tu n'as pas poussé de nouveau commit (ADR 0020) ;
2. **Fraîcheur** : `main` incluse (la gate met elle-même la branche à jour quand c'est possible ; en cas de conflit, `git merge origin/main`) ;
3. **Version** : les fichiers de version du projet (factory-live : `apps/web/package.json` et `apps/server/package.json` ; claude-cockpit : `desktop/package.json`) portent la montée `version_bump` du brief, comptée depuis la base de la PR. Édite leur champ `version` à la main : `npm version` est refusé ;
4. **Tests nommés** : chaque test de la section Tests de l'issue (recopiée à la fin du brief) existe dans le fichier indiqué, sous son nom exact, et vérifie ce que son critère demande ;
5. **CI** : tous les checks de la tête verts ;
6. **Diff** : les règles du pre-commit sur tout le diff de la PR ;
7. **Fail-first** : le test **nommé par le brief** (nom exact) rouge sur la base avec tes tests, vert sur ta tête, trois essais ; PR de tests : tes sabotages rejoués ; maintenance : **Invariance**, aucun test existant modifié ni retiré ; documentation : **Documentation**, seuls des documents changent ; skill : **Skill**, le fichier de la skill est sa base avec le texte d'origine remplacé par le texte proposé, et rien d'autre ;
8. **Build hors ligne** : le build du projet sans réseau ;
9. **Couverture du diff** : chaque ligne exécutable que tu ajoutes ou modifies est exécutée par au moins un test.

Reproduis d'abord la signature sur ta branche (`evidence/07-regression-repro.txt`), corrige, pousse, puis **toujours** un nouveau `kanban_request_review` sans reviewer, avec `metadata.review_iteration` incrémenté. Au 3e rouge de suite, la gate bloque la carte pour Clément.

**Une carte, une branche, une PR.** Après un rouge, corrige par de **nouveaux commits** sur la branche du brief : sa PR se met à jour seule. Jamais de rebase ni de force push d'une branche déjà poussée ; pour retirer un commit déjà poussé, `git revert`. N'ouvre jamais de seconde PR sous un autre nom de branche : la gate la rejette, et l'ancienne PR restée ouverte ne pourrait plus être fermée sans risque (hermes-software-factory#16).
