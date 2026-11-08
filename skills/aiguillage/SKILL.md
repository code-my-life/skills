---
name: aiguillage
description: Quelle skill prendre, et que faire à la fin d'une phase (continuer, vider, passer la main, sous-agent, compacter). Le point d'entrée de toutes les skills des séances de l'opérateur. À lancer à la main.
disable-model-invocation: true
---

# Aiguillage

On ne retient pas toutes les skills : on demande ici. Cette skill nomme chaque skill des séances de l'opérateur et dit
quand la prendre. Elle vient de `ask-matt` et de `PHASE-BOUNDARIES.md` de mattpocock/skills (MIT).

Avant d'affirmer ce qu'une skill fait ou de conseiller d'en sauter une étape, lis son `SKILL.md` : les résumés
d'ici ne servent qu'à s'orienter.

Le catalogue (`catalog.toml`) fait foi, et un contrôle (`catalogue.py verifier`) refuse cet aiguillage s'il oublie une
skill de l'opérateur : en ajouter une au catalogue, c'est l'ajouter ici.

Une skill **manuelle** ne part que sur la demande du propriétaire (`/nom`). Une skill **auto** est reprise seule par
le modèle quand la tâche s'y prête.

## La software factory

| Situation | Skill |
|---|---|
| Écrire une issue pour la factory (types d'issues, gril en QCM) | `factory-issue` (auto) |
| Créer un dépôt de code-my-life et le brancher sur la factory | `factory-nouveau-depot` (manuel) |
| Une carte est bloquée, en triage ou rouge deux fois : que changer dans l'environnement des agents | `factory-retro` (manuel) |

## Penser, décider, écrire

| Situation | Skill |
|---|---|
| Étudier un outil ou une méthode externe avant de l'adopter | `etude-externe` (manuel) |
| Valider une règle ou une machine à états avant d'écrire l'issue | `prototype-logique` (manuel) |
| Choisir entre plusieurs pistes de design d'interface | `prototype` (manuel) |
| Choisir une bibliothèque d'interface | `pick-ui-library` (manuel) |
| Chercher où l'architecture d'un dépôt freine les agents | `architecture` (manuel) |
| Écrire ou relire une skill, un `SOUL.md`, un `AGENTS.md` | `writing-for-agents` (auto) |
| Se faire passer sur le gril avant d'écrire un document (rondes de QCM) | `gril` (auto) |
| Une étape que seul le propriétaire peut faire (identifiants, secrets, tableau de bord tiers) | `wizard` (manuel) |
| Ranger la mémoire de Claude Code | `controle-memoire` (manuel) |

## Relire

| Situation | Skill |
|---|---|
| Avant d'approuver une PR de la factory : fait-elle ce que l'issue demandait ? | `revue-spec` (manuel) |
| Faire relire la branche en local par Greptile avant le push | `cli-review` (manuel) |
| Relever les commentaires et les checks d'une PR, puis les traiter | `check-pr` (manuel) |
| Relire des animations avec un œil exigeant sur le rendu | `review-animations` (manuel) |

## Interface et design

| Situation | Skill |
|---|---|
| Concevoir, critiquer ou polir une interface | `impeccable` (auto) |
| La finition d'un composant, ses détails invisibles | `emil-design-eng` (auto) |
| Casser une interface avec des données extrêmes | `break-ui` (auto) |
| Faire qu'une application web se sente native sur téléphone | `mobile-native` (auto) |
| Toasts React | `ask-sonner` (auto) |

## Animation

| Situation | Skill |
|---|---|
| Construire une animation, décisions dans le bon ordre | `animate` (auto) |
| Animer avec Motion ou en CSS, chercher dans sa doc | `motion` (auto) |
| Animations React Native et Expo | `animate-expo` (auto) |
| Mouvement physique à l'Apple : ressorts, gestes, matières | `apple-design` (auto) |
| Une animation saccade ou dépasse le budget d'une image | `animation-performance` (auto) |
| Nommer un effet décrit avec des mots vagues | `animation-vocabulary` (auto) |
| Trouver où une animation servirait | `find-animation-opportunities` (auto) |
| Auditer les animations d'une base de code et planifier les corrections | `improve-animations` (auto) |
| Un graphe animé React (ligne d'usine, flux) | `motion-graph` (auto) |

## Vidéo (HyperFrames)

| Situation | Skill |
|---|---|
| Faire, monter, animer ou rendre une vidéo | `hyperframes` (auto) |
| Le CLI d'HyperFrames : créer, vérifier, prévisualiser, rendre, publier | `hyperframes-cli` (auto) |
| Un bloc ou composant prêt à l'emploi (transition, titre, graphique) | `hyperframes-registry` (auto) |
| Amener Figma dans une vidéo | `figma` (auto) |
| Musique, sons, images, voix, mixage | `media-use` (auto) |
| Porter dans HyperFrames une vidéo faite avec un autre outil | `remotion-to-hyperframes` (auto) |
| Refaire une vidéo existante, couche par couche | `reverse-any-video` (auto) |
| Un diaporama à présenter en direct | `slideshow` (auto) |
| Un nouvel épisode dans un style vidéo éprouvé | `style-sampling` (auto) |

## Outils

| Situation | Skill |
|---|---|
| Piloter un navigateur, tester des pages | `playwright-cli` (auto) |
| Écrire du Swift moderne | `write-swift` (auto) |

## À la fin d'une phase

Une **phase** est un morceau de travail dans une séance : le gril, l'implémentation, la recette. Elle finit quand on
pense « bon, c'est fait ». Entre deux phases, on a cinq options, et choisir entre elles est la décision la plus floue de
toutes. Lis [fins-de-phase.md](fins-de-phase.md) pour l'arbre ordonné, ses raisons, et pourquoi **continuer** est la
première option à écarter.

- **Continuer** : rester dans la séance. Ne coûte rien, ne perd rien.
- **Vider** (`/clear`) : repartir d'une fenêtre vide, quand rien de ce qui est ici ne sert à la suite.
- **Sous-agent** : confier une tâche bien bornée à sa propre fenêtre et en recevoir un rapport.
- **Compacter** (`/compact`) : résumer ce contexte et repartir de ce résumé. C'est le choix par défaut, mais au bas de
  l'arbre, pas le premier réflexe.
- **Passer la main** : écrire un fichier portable pour un autre harnais, un autre dossier ou un collègue.

La décision se prend **à** la frontière entre deux phases. Au milieu d'une phase, on continue, ou on confie le reste à
des sous-agents.

---

Adaptée de `ask-matt` et de `PHASE-BOUNDARIES.md` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
