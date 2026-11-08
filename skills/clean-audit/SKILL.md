---
name: clean-audit
description: "Auditer un projet selon Clean Code et Clean Architecture (Robert C. Martin), sur toute stack : mesures, constats cités par heuristique, plan de garde-fous priorisé. Use when asked to audit code quality or architecture, to find what a project lacks in clean code or clean architecture, or to prepare quality gates (linters, architecture tests, hooks, CI) before installing them."
---

# clean-audit

Produire un document d'audit qui dit où un projet s'écarte de Clean Code et de Clean Architecture, preuves à l'appui,
et quel garde-fou installer pour chaque écart. L'audit est en lecture seule : la mise en place viendra d'une
validation du propriétaire sur ce document, jamais de l'audit lui-même.

Chaque constat porte un **verdict**, qui décide de son avenir :
- **outil** : un programme donne le même verdict pour les mêmes entrées ; candidat à un linter, un test
  d'architecture, un hook, un check CI ;
- **signal** : un programme détecte, un humain tranche ; candidat à un rapport consultatif, jamais à une CI bloquante
  sans tri humain ;
- **consigne** : pur jugement ; candidat à une ligne de CLAUDE.md, d'AGENTS.md ou d'un skill, jamais à une gate.

## Références

- `references/heuristiques-clean-code.md` : les 66 heuristiques codées du chapitre 17, les seuils chiffrés et les
  règles des chapitres, chacune avec son verdict. À charger pour la passe code (étape 3).
- `references/regles-architecture.md` : les 21 règles du graphe de dépendances (SOLID compris), les métriques I/A/D, la hiérarchie de
  mise en place et les outils par stack. À charger pour la passe architecture (étape 4) et pour le plan (étape 5).
- `references/calibrage.md` : les seuils comme préférences, le calibrage sur l'existant, le minimum vital d'un petit
  projet, les tolérances du livre. À charger avant d'écrire le plan (étape 5).

## Déroulé

1. **Observer.** La stack (langages, frameworks, gestionnaire de paquets), l'outillage en place (formateur, linter,
   typecheck, tests, hooks git, CI, consignes d'agents : CLAUDE.md, AGENTS.md, règles), la structure des dossiers et
   la taille du projet. L'étape est finie quand l'inventaire de l'outillage en place est écrit : l'audit complète
   l'existant, il ne le redécouvre pas en doublon.
2. **Mesurer.** Taille des fonctions et des fichiers, profondeur d'imbrication, nombre d'arguments, duplication,
   couverture si elle existe, et le graphe de dépendances : cycles, sens des arêtes entre couches, I/A/D par
   composant quand le projet en a. Chaque chiffre vient d'une commande reproductible, notée à côté de lui. L'étape
   est finie quand chaque mesure du rapport a sa commande.
3. **Constats code.** Parcourir le code avec le catalogue des heuristiques. Un constat cite : le code de
   l'heuristique (G5, F1, N5...), un exemple en fichier:ligne, la mesure quand il y en a une, le verdict. L'étape est
   finie quand chaque heuristique de verdict outil ou signal du catalogue a été considérée sur ce projet : violée
   avec preuve, respectée, ou sans objet pour cette stack.
4. **Constats architecture.** Appliquer les 21 règles du graphe, même format : numéro de la règle, arête ou module en
   cause, verdict. Sur un projet sans couches déclarées, la première fiche du plan sera la déclaration des couches :
   le mapping chemins vers cercles, validé par le propriétaire.
5. **Plan.** Une fiche par garde-fou, priorisée par effet sur le projet puis par coût, dans l'ordre de la hiérarchie
   de mise en place (compilateur, tests d'architecture, hooks et CI, consignes). Une fiche tient en six lignes :
   - Source : livre, chapitre ou code d'heuristique ;
   - Règle : l'énoncé précis, seuil calibré sur la mesure de l'étape 2 ;
   - Outil : le programme qui la vérifie, et sa règle de configuration ;
   - Où : éditeur, hook d'agent, pre-commit, pre-push, CI ;
   - Faux positifs attendus : ce que la règle attrapera à tort, et l'échappatoire prévue ;
   - Coût : mise en place et bruit quotidien estimés.
   Les constats de verdict consigne vont dans une section à part : le texte prêt à coller dans CLAUDE.md ou
   AGENTS.md, une ligne par consigne.
6. **Rendre.** Le document d'audit suit le format ci-dessous, et se termine par la liste de ce que l'audit écarte
   volontairement (dogme écarté, règles sans objet), pour que le propriétaire voie aussi ce qui a été jugé. Rien ne
   s'installe : la mise en place attend sa validation fiche par fiche.

## Format du document d'audit

1. **Contexte** : stack, taille, domaine, ce que le projet fait.
2. **Outillage en place** : l'inventaire de l'étape 1.
3. **Mesures** : les chiffres de l'étape 2, chaque chiffre avec sa commande.
4. **Constats code** : par famille d'heuristiques, du plus grave au plus bénin.
5. **Constats architecture** : par règle, avec le graphe ou l'extrait qui le montre.
6. **Plan de mise en place** : les fiches priorisées.
7. **Consignes** : le texte prêt à coller pour ce qui ne se mesure pas.
8. **Écarté** : ce que l'audit a jugé sans objet ou dogmatique pour ce projet, et pourquoi.

## Garde-fous

- **Calibrer, jamais imposer** : un seuil se cale sur la mesure de l'existant et bloque la régression sur les lignes
  modifiées ; la réécriture de l'existant est hors du périmètre d'un garde-fou (voir calibrage.md).
- **Respecter les verdicts** : un signal entre en rapport consultatif, une consigne en texte d'agent ; seule une
  règle de verdict outil peut bloquer un commit ou une CI.
- **Minimum vital d'abord** : sur un petit projet, trois fiches suffisent souvent : pas de cycles, le cœur métier
  sans imports de framework, de base de données ni de HTTP, un point d'entrée qui câble tout.
- **Citer** : un constat sans code d'heuristique, sans fichier:ligne ou sans commande n'entre pas dans l'audit.
