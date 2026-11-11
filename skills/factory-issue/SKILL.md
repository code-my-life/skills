---
name: factory-issue
description: Rédiger une issue GitHub au standard de la software factory (ADR 0017) pour un dépôt de code-my-life aux types d'issues (factory-live, claude-cockpit). Use when the owner asks to create, write or prepare an issue, a bug report or a feature request for one of these repositories, or to have the factory build something there ("fais une issue", "crée une issue", "rédige l'issue", "fais-la traiter par la factory").
---

# Rédiger une issue pour la factory

Une issue est le brief de la factory : la vitesse et la justesse d'une pièce se jouent ici. factory-live#11 (badges)
est le modèle : cadrée environ 3 heures sur une maquette validée, elle est passée en 74 minutes de fabrication.
factory-live#9 est le contre-exemple : une plainte d'une ligne traduite en 2 minutes en solution, faite exactement,
approuvée, puis rejetée le lendemain.

Le standard ne s'applique qu'aux dépôts marqués `types: true` dans `factory.yaml` (aujourd'hui claude-cockpit,
factory-live et skills). Ailleurs, rédige comme avant. La définition des types fait foi : `config/types.yaml` de
hermes-software-factory (label, type natif, sections).

## 1. Choisir le type

| Type | Quand | Label | Type natif |
|---|---|---|---|
| Bug | un écart avec un comportement ou un rendu **déjà défini** : spécification, standard de l'app, version précédente | `type:bug` | Bug |
| Interface | une apparence nouvelle ou modifiée : écran, composant, style | `type:interface` | Feature |
| Fonctionnalité | une logique, une API, des données nouvelles ou modifiées | `type:fonctionnalite` | Feature |
| Diagnostic | la cause est inconnue : trouver la cause et un test qui reproduit, sans corriger | `type:diagnostic` | Task |
| Tests | ajouter ou renforcer des tests, sans changer le code | `type:tests` | Task |
| Maintenance | refactor, dépendances, CI, outillage, sans changement de comportement | `type:maintenance` | Task |
| Documentation | README, guides, docs : seuls des documents changent | `type:documentation` | Task |
| Skill | le texte d'une skill, changé ou nouveau ; dans code-my-life/skills seulement | `type:skill` | Task |

Un « bug » sans référence existante est une demande d'Interface ou de Fonctionnalité : #9 l'était (rien ne disait que
l'étiquette devait être transparente). Une cause inconnue appelle un Diagnostic d'abord, puis un Bug avec la cause.

## 2. Passer l'issue sur le gril avant de l'écrire

Call the Skill tool with "gril" : il dit comment poser les décisions au propriétaire, en rondes de QCM. Les questions
partent des sections obligatoires du type : l'arbre est dans `references/questions.md`, qui commence par ce que tu
vérifies avant la première question.

**Ce que tu ne lâches pas**, en plus du gril :
- **le type** : un « bug » sans référence existante est une Interface ou une Fonctionnalité ; une cause inconnue appelle
  d'abord un Diagnostic ;
- **la cible** : pour une Interface, la maquette publiée en artifact sur la vraie forme des composants existants, et
  validée, avant toute issue. Son lien va dans « Maquette » ; un fichier HTML joint à l'issue convient aussi, et la démo
  d'une branche quand le propriétaire en fait la maquette (lien `github.com/code-my-life/<dépôt>/tree/<branche>`). Aucune
  solution non validée n'entre dans « Attendu » ;
- **la mesure** : pour chaque critère, « comment le vérifie-t-on ? », jusqu'à obtenir un chiffre, un nom de test ou une
  capture ;
- **le périmètre** : ce qui ne change pas, dit explicitement.

**La taille.** Une coquille, ou un bug dont la référence est évidente : une ronde suffit. Une Interface ou une
Fonctionnalité qui touche plusieurs écrans : autant de rondes qu'il en faut.

**La synthèse** est celle du gril : son brouillon est l'issue, écrite comme le dit la section 3.

## 3. Écrire les sections du type

Chaque section est un titre `### <libellé>` exact, dans l'ordre du formulaire du type
(`config/types.yaml` de hermes-software-factory). Les libellés : Constat, Impact, Reproduction, Référence, Cause,
Maquette, Inventaire, Règles chiffrées, Comportement, Contrat, Symptôme, Depuis quand, Pistes écartées, Zone non
couverte, Sabotages attendus, Objectif, Périmètre, Invariant, Documents, Lecteur, Contenu attendu, Skill et fichier,
Texte d'origine, Texte proposé, Raison, Preuve, Attendu, Critères d'acceptation, Tests, Captures, Ne change pas.

- **Critères d'acceptation** : une ligne par critère, `- C1 : …`, `- C2 : …`, sans trou. Chacun se vérifie par un test,
  une mesure ou une capture. Convertis le flou :
  - « lisible » devient « un caractère au moins et les points de suspension visibles » ;
  - « sur une ligne » devient « 20 px de haut » ;
  - « ne déborde pas » devient « pas de défilement horizontal à 390 px » ;
  - « comme les autres » devient la liste des propriétés communes (forme, jetons, tailles).
  Les défauts de #12 sont tombés exactement là où #11 ne donnait pas de chiffre : la largeur d'un badge, la coupe visible
  sur iPhone.
- **Tests** : une ligne par test, le fichier entre accents graves et le nom exact entre « ». Le premier échoue avant la
  correction et passe après : c'est le test fail-first de la gate.
- **Ne change pas** : ce qui reste tel quel, pour borner le travail.

## 4. Partir d'un ticket de Sofia (BMAD)

Sofia, l'agent product owner de BMad Method (skill `bmad-agent-po`), découpe un chantier dans `~/perso/_bmad-output/` :
une **initiative** (le chantier), ses **epics** (un résultat qui demande plusieurs séances), et pour chaque epic ses
**stories** (une étape qui tient dans une séance), rangées dans l'ordre dans des fichiers `tickets.toml`. Une story
prête devient ici une issue, et rien de ce que Sofia a écrit ne se perd.

**Avant la première question** : lis l'entrée de la story dans le `tickets.toml` de son epic (`title`, `description`,
`verify`, `covers`, `after`, `hitl`, `risk`, `estimate`, `unknown`, `references`, `notes`), son fichier
`story-<slug>.md` s'il existe, et le fichier de son epic. Une entrée qui porte déjà une clé `issue` est publiée : ne la
publie pas une seconde fois. Une question ouverte (`unknown`) se tranche au gril : une issue n'en porte aucune.

**Le type** : une story de logique, d'API ou de données est une Fonctionnalité ; une story d'apparence, une Interface
(sa maquette validée reste exigée) ; un `bug`, un Bug ; la story de ménage de fin d'epic (« Refactor sweep »), une
Maintenance. Une story qui touche deux dépôts se coupe en deux issues : une carte travaille dans un seul dépôt.

**Les sections**, toutes en français, chaque terme de BMAD expliqué à sa première apparition :

| Chez Sofia | Dans l'issue |
|---|---|
| `title` | le titre de l'issue |
| `description`, `## Description` | Constat (ce qui se passe aujourd'hui) et Impact (pour qui), complétés au gril |
| `verify`, `## Requirements` (critères numérotés, Given, When, Then) | Comportement, et Critères d'acceptation qui gardent l'exigence couverte : `- C1 : … (R1)` |
| les exigences de l'epic qu'elle couvre (`covers`) | recopiées dans Comportement ou Contrat, avec leur identifiant : la lane ne lit que l'issue |
| `## Constraints` | Contrat, ou Ne change pas |
| `## Boundaries` (« Must not change ») | Ne change pas |
| `references` | des liens GitHub ; un chemin de `_bmad-output/` va dans Origine BMAD |
| `notes` (`Decision:`, `Assumption:`), `risk`, `after`, `estimate`, les points de contrôle | Origine BMAD |

Les tests nommés viennent du gril : Sofia n'en écrit pas. La dernière section, `### Origine BMAD`, recopie le reste en
français : le chemin du ticket et son identifiant, les exigences couvertes, les prérequis (`after`), le risque,
l'estimation, les décisions et les hypothèses. L'intake ne lit que les sections du type : celle-ci passe sans gêner.

**Un spike ou une étape humaine** (`hitl = true`) ne se fabrique pas : il devient une issue de type natif Task, sans
label `type:*` ni `factory`, assignée au propriétaire, sous-issue de l'epic, et qui bloque les stories qui en
dépendent. Un spike qui cherche une cause inconnue est un Diagnostic.

## 5. L'issue d'un epic

Un epic devient une issue dès que son découpage est validé, avant ses stories, dans le dépôt qui porte le gros de son
travail. Type natif Epic, aucun label `type:*`, jamais `factory` : il ne se fabrique pas, ses sous-issues portent le
travail. Son corps est le fichier de l'epic, traduit section par section : `### Description`, `### Résultat`
(Outcome), `### Exigences` (Requirements, avec R1, R2…), `### Contraintes`, `### Fini quand` (Done when),
`### Limites` (Boundaries), `### Références`, `### Notes` ; puis `### Découpage`, les stories prévues dans l'ordre de
`tickets.toml` (chacune publiée devient une sous-issue), et `### Origine BMAD`. Le type Epic doit exister dans
l'organisation (`gh api orgs/code-my-life/issue-types`) ; sinon, demande au propriétaire de le créer.

## 6. Vérifier, puis créer

1. Écris le corps dans un fichier du scratchpad, puis vérifie-le exactement comme l'intake le fera :
   `python3 ~/perso/hermes-software-factory/scripts/factory-issue-check.py <type> <fichier>`. Il doit répondre
   « prête ». Une issue Epic ou Task n'a pas de type de la factory : elle ne passe pas ce contrôle.
2. Montre l'issue au propriétaire avant de la créer, sauf s'il a demandé de la créer directement.
3. Crée-la avec son compte, le label du type et son type natif :
   `env -u GH_TOKEN gh issue create --repo code-my-life/<dépôt> --title "<titre>" --label type:<type> --type <type natif> --body-file <fichier>`.
   Pour un epic : `--type Epic`, sans label ; pour un spike ou une étape humaine : `--type Task --assignee @me`, sans
   label. Le label `factory` lance la fabrication : ne le pose que si le propriétaire le demande.
4. Partie d'un ticket de Sofia, note son lien tout de suite dans l'arbre : une clé `issue = "<lien>"` dans l'entrée de
   la story, ou dans la table `[[epic]]` de l'epic. Puis rattache-la, toujours avec `env -u GH_TOKEN`, après avoir lu
   ce qui existe (`gh issue view <lien> --json parent,blockedBy`) pour ne rien poser deux fois :
   - à son epic : `gh issue edit <lien> --parent <lien de l'epic>` ;
   - à ses prérequis déjà publiés (`after`) : `gh issue edit <lien> --add-blocked-by <liens>`.
5. Range-la dans le projet n°3 de l'organisation, avec le même compte :
   - `gh project item-add 3 --owner code-my-life --url <lien>`, puis
     `gh project item-edit 3 --owner code-my-life --url <lien> --field Status --value Backlog` ;
   - Priority (Urgent, High, Medium, Low) et Effort (High, Medium, Low), tranchés au gril : ce sont des champs d'issue
     de l'organisation, dont `gh api orgs/code-my-life/issue-fields` donne les identifiants. Pose-les avec
     `gh api -X POST repos/code-my-life/<dépôt>/issues/<n>/issue-field-values --input <fichier>`, le fichier portant
     `{"issue_field_values": [{"field_id": <id>, "value": "<option>"}]}`.
6. Une issue existante se vérifie avec `factory-issue-check.py code-my-life/<dépôt>#<n>`.

L'intake ignore « bloquée par » : le propriétaire pose `factory` sur une story quand ses prérequis sont fermés.

Une issue incomplète reçoit le label « à cadrer » de l'intake et un commentaire qui liste les manques ; complétée, elle
part d'elle-même au passage suivant.
