---
name: factory-retro
description: "Rétrospective d'une carte de la factory : propose des changements à l'environnement des agents (contrôles, consignes, accès à l'information), jamais au code. À lancer à la main, de préférence sur une carte bloquée, en triage ou rouge deux fois."
disable-model-invocation: true
---

# Rétrospective d'une carte de la factory

Le propriétaire demande une **rétrospective**. Tu proposes des améliorations de l'**environnement** des agents (règles,
contrôles, consignes, outils) pour que la prochaine carte se passe mieux. Tu ne corriges pas le code de la carte.

Cette skill vient de `retro` et de `chief-of-staff` de mattpocock/skills (MIT), adaptées aux sources d'Hermès.

## Étapes

1. Charge la skill `writing-for-agents` : tu l'appliques à chaque consigne que tu proposes.
2. Choisis les cartes à relire, puis lis leurs sources primaires.
3. Cherche des pistes dans les catégories ci-dessous, chacune rattachée à un moment précis de la séance.
4. Trie par gravité et présente. Le propriétaire tranche en QCM.
5. Ce qui est retenu devient une issue, et rien d'autre.

## 1. Quelles cartes

Si le propriétaire nomme une carte, prends celle-là. Sinon, la retro coûte cher : relis d'abord les cartes où quelque
chose a mal tourné, dans cet ordre.

- **Bloquée** : `tasks.status` à `blocked`, ou un événement `blocked` (le `payload` donne `kind` : `needs_input` ou
  `capability`) ; `block_recurrences` au-dessus de 1 ; `block_loop_detected`.
- **En triage** : `tasks.status = 'triage'`.
- **Rouge deux fois** : au moins deux événements `review_reopened` (la gate a rendu un verdict rouge, la carte est
  revenue à l'implémenteur).
- À défaut, les cartes avec `respawn_guarded`, `protocol_violation`, `gave_up`, `timed_out` ou `crashed`.

Ne relis pas une carte qui s'est bien passée : une carte sur cinq suffit à voir l'environnement.

## 2. Les sources primaires

Lis-les en lecture seule : n'écris jamais dans une base d'Hermès ni dans `~/.hermes`.

- **Les événements de la carte** : `~/.hermes/kanban/boards/factory/kanban.db`, tables `task_events` (le déroulé :
  `created`, `claimed`, `spawned`, `blocked`, `review_requested`, `review_reopened`, `commented`...), `task_runs`
  (`profile`, `outcome`, `summary`, `error`) et `task_comments` (le brief, les relais, les verdicts).
- **Les verdicts de la gate** : les commentaires de la carte dont l'auteur est `gate`, `gate-claude` ou `factory-gate`,
  et les preuves sous `evidence/gate/<sha7>/` de l'espace de la carte.
- **Les transcriptions des lanes** : les séances de Claude Code de la carte, dans
  `~/.claude/projects/<dossier de travail de la carte, avec chaque `/` remplacé par `-`>` (un dossier par carte). Le
  dossier de travail est `tasks.workspace_path` de la carte dans `kanban.db` ; pour un espace sous
  `~/.hermes/kanban/boards/factory/workspaces/t_<id>`, le dossier se termine par `-t-<id>`. Liste
  `~/.claude/projects/` et cherche ce suffixe plutôt que de recopier un chemin.
- **Le vrai modèle** : `~/.hermes/state.db`, table `session_model_usage` (`model`, jetons, coût par séance). Le modèle
  réellement servi n'est pas celui qu'annonce la configuration : une surcharge sans fournisseur retombe sur un modèle
  gratuit.

Une base se lit par une connexion `file:...?mode=ro` (`sqlite3`, ou `python3 -I`). Ne cite que ce que tu as lu : une
piste dont tu n'as pas la ligne source est une hypothèse, dis-le.

## 3. Les catégories

Chaque piste porte l'**événement ou la ligne de transcription** où le problème est apparu (« le 12e appel de la séance,
`respawn_guarded` à 14:03 »), et la catégorie.

- **Navigation** : l'agent a-t-il trouvé vite les bons fichiers ? Une dépendance cachée entre fichiers ? Un **pointeur
  de navigation** aurait-il aidé ? À retenir quand la séance a longtemps cherché une information.
- **Contrôles automatiques** : un contrôle aurait-il attrapé l'erreur de l'agent : lint, types, test, hook git, règle de
  la gate ? Lis d'abord la commande de contrôle du dépôt (`factory.yaml`, hooks, CI) : un contrôle qui existe mais n'est
  pas branché, ou qui est muet, est la piste, pas un contrôle neuf. À retenir quand une erreur de l'agent était
  mécanique.
- **Consignes** : une consigne de `SOUL.md`, d'`AGENTS.md` ou d'une skill manque, est trop longue, ou se contredit.
- **Consignes sans effet** : des lignes qui ne changent pas ce que l'agent fait. À retenir quand les fichiers de
  consignes sont longs.
- **Accès à l'information** : une information décisive n'était pas à la portée de l'agent (journaux, lecture seule d'un
  service, état de la carte). À retenir quand la séance a deviné ce qu'elle aurait pu lire.
- **Coût des outils** : un appel coûteux qu'on pouvait alléger, un outil bavard, un modèle plus cher que la tâche.

### Contrôle ou consigne

Classe d'abord l'erreur.
- Une erreur **mécanique** (motif fixe, API interdite, emplacement d'un fichier) devient un **contrôle** : une règle du
  lint, un hook, une règle de la gate. Construis le contrôle plutôt que d'écrire une règle.
- Un **jugement** (cohérence entre fichiers, « suit le style voisin ») devient une **consigne**, courte, au bon fichier.

Ici, la revue, c'est la gate et le propriétaire : il n'y a pas de fichier de standards pour un agent relecteur, donc pas
de piste « nouvelle règle pour le relecteur ».

## 4. Présenter

Présente les pistes **par gravité**, la plus lourde d'abord : une ligne par piste avec la catégorie, le moment de la
séance (événement ou ligne de transcription), la correction proposée et sa nature (contrôle ou consigne).

Puis pose le choix en QCM (outil AskUserQuestion), 4 questions au plus par appel : pour chaque piste, « la poursuivre »
ou « l'écarter », ta recommandation en premier avec « (recommandé) ».

## 5. Ce qui devient une issue

Une piste retenue devient une issue, pas un correctif direct :
- une piste sur une skill (code-my-life/skills) : une issue **Skill**, avec le texte d'origine copié tel quel depuis
  main (ADR 0027) ;
- toute autre : une issue de la factory, au type qui convient (`factory-issue`).

Rédige-les avec `factory-issue`. Ne crée rien sans le GO du propriétaire.

## Référence

Tout travail passe par deux étapes : l'implémentation, qui porte la pression de contexte (exploration, code, débogage),
puis la revue, qui reçoit un diff. Ici, la revue est la gate : une règle déterministe vaut mieux qu'une consigne que
l'implémenteur doit retenir.

- `AGENTS.md` et `SOUL.md` arrivent dans le contexte de chaque agent : à garder pour des pointeurs vers d'autres
  fichiers.
- Une skill sert aux docs (sa description entre dans le contexte) et aux commandes lancées à la main.
- Cherche une doc existante avant d'en écrire une.

---

Adaptée de `retro` et `chief-of-staff` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
