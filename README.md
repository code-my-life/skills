# skills

La base de connaissance de Code My Life : toutes les skills de ses agents, au format
[Agent Skills](https://agentskills.io/specification), à lire ici et à installer chez chaque agent.

## Ce qu'on y trouve

- Les skills maison, écrites pour la software factory et pour les séances de Claude Code.
- Les skills adaptées d'autres dépôts, avec leur licence et le commit d'amont dont elles partent.
- Des copies de skills externes, chacune avec sa licence, quand celle-ci permet la redistribution. Les autres sont
  seulement déclarées, et s'installent depuis leur amont.

Le catalogue, `catalog.toml`, dit pour chaque skill d'où elle vient, à quelle version figée, sous quelle licence,
quels agents s'en servent et comment elle se déclenche : à la main, d'elle-même, ou attachée à une carte de la factory.
La liste ci-dessous en est tirée par `python3 scripts/catalogue.py readme --ecrire`.

## Installer une skill

Claude Code, OpenCode, Codex et les autres agents du [CLI skills](https://github.com/vercel-labs/skills) :

```bash
DISABLE_TELEMETRY=1 npx skills@1.7.6 add code-my-life/skills --skill <nom> -a claude-code -g
```

Hermès Agent :

```bash
hermes skills tap add code-my-life/skills
hermes skills install code-my-life/skills/<nom>
```

Une skill déclarée seulement s'installe depuis son amont, nommé dans le catalogue. Chez Code My Life, `install.sh` de
la software factory installe chaque agent depuis le catalogue.

## Demander un changement

Ouvrez une issue avec l'un des modèles. Elle passe par la software factory de Code My Life : une carte, une pull
request, des contrôles automatiques, puis l'approbation du propriétaire.

## Une nouvelle version amont

Renovate lit les versions figées du catalogue et ouvre une pull request par montée de version. Le workflow « Amont »
montre alors le diff de chaque copie qui s'écarte de son amont : la copie se refait par
`python3 scripts/catalogue.py amont --recopier <nom>`, poussé sur la même pull request. Pour une skill adaptée, il liste
le diff amont depuis le commit noté dans `d_apres` (`catalogue.py adaptees`) : l'adaptation se reprend à la main.

## Licence

Ce qui est propre à ce dépôt est sous licence MIT (voir `LICENSE`). Chaque skill copiée garde la licence de son amont,
dans le fichier `LICENSE` de son dossier.

## Les skills

<!-- catalogue : début, généré par scripts/catalogue.py readme --ecrire -->

### La software factory

- **`factory-author-proof`** : Preuve d'auteur d'une carte : test rouge sur la base, correctif minimal, test vert, preuves sur disque. (maison, carte)
- **`factory-brief`** : Changer une issue en brief exécutable et en cartes Kanban, pour le coordinateur. (maison, carte)
- **`factory-cli-lane`** : Déléguer l'implémentation à un CLI (claude -p, opencode run), Hermès gardant la carte. (maison, carte)
- **`factory-diagnostic`** : Procédure de la carte Diagnostic : boucle rouge, repro réduite, hypothèses réfutables, constat en commentaire. (maison, carte)
- **`factory-issue`** : Rédiger une issue au standard de la factory (types d'issues, ADR 0017), gril en QCM. (maison, auto)
- **`factory-nouveau-depot`** : Créer un dépôt de code-my-life et le brancher sur la factory, du dépôt modèle au contrôle final. (maison, manuel)
- **`factory-onboard`** : Préparer un dépôt pour la factory : clone, projet Hermès, AGENTS.md, outils. (maison, carte)
- **`factory-retro`** : Rétrospective d'une carte de la factory : pistes sur l'environnement des agents, rattachées à un événement. (maison, manuel)
- **`gril`** : Passer un sujet sur le gril : rondes de QCM, faits cherchés par l'agent, décisions du propriétaire. (maison, auto)

### Animation et mouvement

- **`animate`** : Construire une animation en prenant les décisions dans le bon ordre, jusqu'au code. (emilkowalski/skills, auto)
- **`animate-expo`** : Animations React Native et Expo : Reanimated, gestes, transitions, retours haptiques. (emilkowalski/skills, auto)
- **`animation-performance`** : Garder les animations web dans le budget d'une image, et trouver ce qui saccade. (emilkowalski/skills, auto)
- **`animation-vocabulary`** : Donner le nom exact d'un effet d'animation décrit avec des mots vagues. (emilkowalski/skills, auto)
- **`apple-design`** : Le mouvement fluide et physique d'Apple, adapté au web : ressorts, gestes, matières. (emilkowalski/skills, auto)
- **`find-animation-opportunities`** : Trouver les endroits d'une interface où une animation servirait, et écarter les autres. (emilkowalski/skills, auto)
- **`improve-animations`** : Auditer les animations d'une base de code et écrire les plans de correction. (emilkowalski/skills, auto)
- **`motion`** : Bonnes pratiques de Motion et des animations CSS, recherche dans sa doc, audits de performance. (npm motion-ai, auto)
- **`motion-graph`** : Graphe animé d'une interface React (ligne d'usine, flux) avec Motion et Primer. (maison, auto)
- **`review-animations`** : Relire des animations avec un œil exigeant sur le rendu, à la demande. (emilkowalski/skills, manuel)

### Interface et design

- **`ask-sonner`** : Guide de Sonner, la bibliothèque de toasts React : mise en place, style, dépannage. (emilkowalski/skills, auto)
- **`break-ui`** : Casser une interface avec des données extrêmes, et rendre chaque défaut avec sa correction. (emilkowalski/skills, auto)
- **`emil-design-eng`** : La finition d'une interface selon Emil Kowalski : composants, animations, détails invisibles. (emilkowalski/skills, auto)
- **`impeccable`** : Concevoir, critiquer et polir une interface, du design system aux détails. (npm impeccable, déclarée, auto)
- **`mobile-native`** : Faire qu'une application web se sente native sur un téléphone, réglage par réglage. (emilkowalski/skills, auto)
- **`pick-ui-library`** : Choisir une bibliothèque d'interface dans une liste vérifiée, à la demande. (emilkowalski/skills, manuel)
- **`prototype`** : Explorer plusieurs pistes de design vraiment différentes avant d'en choisir une, à la demande. (emilkowalski/skills, manuel)

### Vidéo

- **`captions-overlay`** : Les sous-titres d'une vidéo HyperFrames, posés par-dessus le film, jamais dans une bande réservée. (dans code-my-life/video-factory, déclarée, auto)
- **`cut-the-curve`** : Le catalogue des raccords de video-factory : coupes accordées en vitesse et entrées en cascade. (dans code-my-life/video-factory, déclarée, auto)
- **`figma`** : Amener Figma dans une vidéo HyperFrames : éléments, jetons de marque, maquettes animées. (heygen-com/hyperframes, auto)
- **`hyperframes`** : Faire, monter, animer ou rendre une vidéo avec HyperFrames (HTML rendu en vidéo). (heygen-com/hyperframes, auto)
- **`hyperframes-cli`** : Le CLI d'HyperFrames par tâche : créer, vérifier, prévisualiser, rendre, publier. (heygen-com/hyperframes, auto)
- **`hyperframes-registry`** : Les blocs et composants prêts à l'emploi d'HyperFrames : transitions, titres, graphiques. (heygen-com/hyperframes, auto)
- **`media-use`** : Trouver ou produire les médias d'une vidéo : musique, sons, images, voix, mixage. (heygen-com/hyperframes, auto)
- **`motion-doctrine`** : La loi du mouvement de video-factory : une vidéo à plusieurs scènes comme un seul plan continu. (dans code-my-life/video-factory, déclarée, auto)
- **`remotion-to-hyperframes`** : Porter dans HyperFrames une vidéo faite avec un autre outil, vérifiée image par image. (heygen-com/hyperframes, auto)
- **`reverse-any-video`** : Refaire une vidéo existante en projet HyperFrames modifiable, couche par couche. (heygen-com/hyperframes, auto)
- **`seam-craft`** : Les conditions d'un raccord correct entre deux scènes sur la timeline principale. (dans code-my-life/video-factory, déclarée, auto)
- **`slideshow`** : Un diaporama HyperFrames à présenter en direct, avec notes de l'orateur. (heygen-com/hyperframes, auto)
- **`style-sampling`** : Un nouvel épisode dans un style vidéo éprouvé, sur le sujet voulu. (heygen-com/hyperframes, auto)
- **`video-factory`** : Comment video-factory change un script annoté en projet HyperFrames, jusqu'au rendu. (dans code-my-life/video-factory, déclarée, auto)

### Revue de code

- **`architecture`** : Trouver où l'architecture d'un dépôt freine les agents, en rapport visuel privé, à la demande. (maison, manuel)
- **`check-pr`** : Relever les commentaires, les checks et le texte d'une PR, puis les traiter, à la demande. (greptileai/skills, manuel)
- **`clean-audit`** : Auditer un projet selon Clean Code et Clean Architecture : mesures, constats cités, plan de garde-fous. (maison, auto)
- **`clean-setup`** : Installer les garde-fous d'un audit clean-audit validé : tests d'architecture, lint, hooks, CI, consignes. (maison, auto)
- **`cli-review`** : Faire relire la branche en local par le CLI de Greptile avant le push, à la demande. (greptileai/skills, manuel)
- **`revue-spec`** : Relire une PR de la factory contre son issue avant l'approbation, sans la poster, à la demande. (maison, manuel)

### Outils

- **`aiguillage`** : Quelle skill prendre, et que faire à la fin d'une phase : le point d'entrée des séances. (maison, manuel)
- **`controle-memoire`** : Contrôler la mémoire de Claude Code : contradictions, pages orphelines, faits dépassés. (maison, manuel)
- **`etude-externe`** : Étudier un outil externe contre ses sources primaires, verdict par projet, étude gardée. (maison, manuel)
- **`playwright-cli`** : Piloter un navigateur et tester des pages avec Playwright, en ligne de commande. (microsoft/playwright-cli, auto)
- **`prototype-logique`** : Valider une règle ou une machine à états en page unique, publiée en artifact privé. (maison, manuel)
- **`wizard`** : Un script bash qui guide pas à pas une étape que seul le propriétaire peut faire, à la demande. (maison, manuel)
- **`write-swift`** : Écrire du Swift moderne : types valeur, concurrence de Swift 6, tests, performance. (emilkowalski/skills, auto)
- **`writing-for-agents`** : Écrire une skill, un SOUL ou un AGENTS.md : les règles d'écriture pour un agent. (mattpocock/skills, auto)

<!-- catalogue : fin -->
