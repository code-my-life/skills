---
name: factory-issue
description: Rédiger une issue GitHub au standard de la software factory (ADR 0017) pour un dépôt de code-my-life aux types d'issues (factory-live, claude-cockpit). Use when the owner asks to create, write or prepare an issue, a bug report or a feature request for one of these repositories, or to have the factory build something there ("fais une issue", "crée une issue", "rédige l'issue", "fais-la traiter par la factory").
---

# Rédiger une issue pour la factory

Une issue est le brief de la factory : la vitesse et la justesse d'une pièce se jouent ici. factory-live#11 (badges)
est le modèle : cadrée environ 3 heures sur une maquette validée, elle est passée en 74 minutes de fabrication.
factory-live#9 est le contre-exemple : une plainte d'une ligne traduite en 2 minutes en solution, faite exactement,
approuvée, puis rejetée le lendemain.

Le standard ne s'applique qu'aux dépôts marqués `types: true` dans `factory.yaml` (aujourd'hui factory-live et
claude-cockpit). Ailleurs, rédige comme avant.

## 1. Choisir le type

| Type | Quand | Label |
|---|---|---|
| Bug | un écart avec un comportement ou un rendu **déjà défini** : spécification, standard de l'app, version précédente | `type:bug` |
| Interface | une apparence nouvelle ou modifiée : écran, composant, style | `type:interface` |
| Fonctionnalité | une logique, une API, des données nouvelles ou modifiées | `type:fonctionnalite` |
| Diagnostic | la cause est inconnue : trouver la cause et un test qui reproduit, sans corriger | `type:diagnostic` |
| Tests | ajouter ou renforcer des tests, sans changer le code | `type:tests` |
| Maintenance | refactor, dépendances, CI, outillage, sans changement de comportement | `type:maintenance` |
| Documentation | README, guides, docs : seuls des documents changent | `type:documentation` |

Un « bug » sans référence existante est une demande d'Interface ou de Fonctionnalité : #9 l'était (rien ne disait que
l'étiquette devait être transparente). Une cause inconnue appelle un Diagnostic d'abord, puis un Bug avec la cause.

## 2. Passer l'issue sur le gril avant de l'écrire

Méthode de la skill grill-me de Hermès (Rafael Zendron, d'après le « grilling » de Matt Pocock, licence MIT), adaptée
aux types de la factory. But : que chaque décision soit prise par le propriétaire avant la première ligne de l'issue.

**Les faits sont à toi, les décisions au propriétaire.** Avant chaque ronde, cherche toi-même dans le dépôt ce qui s'y
trouve : fichiers, composants, tests existants, captures, comportement actuel. Une issue cite des chemins réels. Ne pose
jamais une question dont la réponse est dans le code.

**Les rondes.** Les questions partent des sections obligatoires du type : l'arbre est dans `references/questions.md`.
Une ronde pose toutes les questions dont les prérequis sont tranchés. Une question qui dépend d'une réponse encore
ouverte attend la ronde suivante.

**En QCM.** Pose chaque ronde avec l'outil de questions à choix (AskUserQuestion), jamais en liste de texte :
- une question par décision, de 2 à 4 options, ta recommandation en premier avec « (recommandé) » dans son libellé ;
- pour chaque option, une description courte : ce qu'elle implique, ce qu'elle coûte ;
- un aperçu en ASCII (`preview`) quand on compare des variantes d'interface : boutons, menu, légende ;
- 4 questions au plus par appel : au-delà, enchaîne les appels ;
- les faits trouvés dans le dépôt vont dans un court message juste avant l'appel, pour que le choix se fasse sur pièces.

Le propriétaire peut répondre hors des options. Lis sa réponse telle quelle : elle peut ouvrir une question nouvelle,
à creuser dans le code avant la ronde suivante.

Attends les réponses, regarde ce qui est devenu posable, puis pose la ronde suivante.

**Ce que tu ne lâches pas :**
- **le type** : un « bug » sans référence existante est une Interface ou une Fonctionnalité ; une cause inconnue appelle
  d'abord un Diagnostic ;
- **la cible** : pour une Interface, la maquette publiée en artifact sur la vraie forme des composants existants, et
  validée, avant toute issue. Son lien va dans « Maquette » ; un fichier HTML joint à l'issue convient aussi, et la démo
  d'une branche quand le propriétaire en fait la maquette (lien `github.com/code-my-life/<dépôt>/tree/<branche>`). Aucune
  solution non validée n'entre dans « Attendu » ;
- **la mesure** : pour chaque critère, « comment le vérifie-t-on ? », jusqu'à obtenir un chiffre, un nom de test ou une
  capture ;
- **le périmètre** : ce qui ne change pas, dit explicitement ;
- **« je ne sais pas »** n'est pas une réponse finale : propose des options, ce qu'elles coûtent, et ta recommandation ;
- **la complaisance** : si tout semble clair, cherche encore (thème sombre, 390 px, texte très long ou absent, liste
  vide, erreur réseau, données réelles).

**La taille.** Une coquille, ou un bug dont la référence est évidente : une ronde suffit. Une Interface ou une
Fonctionnalité qui touche plusieurs écrans : autant de rondes qu'il en faut, jusqu'à ce qu'aucune question ne reste
ouverte.

**La synthèse.** Quand plus rien n'est ouvert : la liste des décisions, ce qui reste ouvert et ce qui est hors du
périmètre, puis le brouillon de l'issue (section 3). Demande en QCM : « Aligné ? Je la crée, ou on ajuste ? » Rien
n'est créé sans cet accord, sauf si le propriétaire a demandé de créer l'issue directement.

## 3. Écrire les sections du type

Chaque section est un titre `### <libellé>` exact, dans l'ordre du formulaire du type
(`config/types.yaml` de hermes-software-factory). Les libellés : Constat, Impact, Reproduction, Référence, Cause,
Maquette, Inventaire, Règles chiffrées, Comportement, Contrat, Symptôme, Depuis quand, Pistes écartées, Zone non
couverte, Sabotages attendus, Objectif, Périmètre, Invariant, Documents, Lecteur, Contenu attendu, Attendu,
Critères d'acceptation, Tests, Captures, Ne change pas.

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

## 4. Vérifier, puis créer

1. Écris le corps dans un fichier du scratchpad, puis vérifie-le exactement comme l'intake le fera :
   `python3 ~/perso/hermes-software-factory/scripts/factory-issue-check.py <type> <fichier>`. Il doit répondre
   « prête ».
2. Montre l'issue au propriétaire avant de la créer, sauf s'il a demandé de la créer directement.
3. Crée-la avec son compte et le label du type :
   `env -u GH_TOKEN gh issue create --repo code-my-life/<dépôt> --title "<titre>" --label type:<type> --body-file <fichier>`.
   Le label `factory` lance la fabrication : ne le pose que si le propriétaire le demande.
4. Une issue existante se vérifie avec `factory-issue-check.py code-my-life/<dépôt>#<n>`.

Une issue incomplète reçoit le label « à cadrer » de l'intake et un commentaire qui liste les manques ; complétée, elle
part d'elle-même au passage suivant.
