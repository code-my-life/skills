---
name: gril
description: "Passer un sujet sur le gril avant d'écrire le document qu'il prépare (issue, rétro, architecture, glossaire) : rondes de questions en QCM, faits cherchés par l'agent, décisions prises par le propriétaire. Use when a skill says to call \"gril\", or when the owner asks to be grilled on a plan, an issue or a design (\"passe-moi sur le gril\", \"grill me\")."
---

# Le gril

Méthode de la skill grill-me de Hermès (Rafael Zendron, d'après le « grilling » de Matt Pocock, licence MIT) et de
`grilling` de mattpocock/skills (commit `4ae2317`, licence MIT), adaptée à la factory. But : que chaque décision soit
prise par le propriétaire avant la première ligne du document que le gril prépare.

La skill qui appelle le gril apporte son arbre de questions et ce qu'elle ne lâche pas. Le gril dit comment les poser.

## Les faits sont à toi, les décisions au propriétaire

Avant chaque ronde, cherche toi-même ce qui se trouve dans le dépôt : fichiers, composants, tests existants, captures,
comportement actuel. Un document cite des chemins réels. Ne pose jamais une question dont la réponse est dans le code.

Une recherche longue ne retient pas la ronde : confie-la à un sous-agent, et pose tout de suite les questions qui n'en
dépendent pas. Seules celles qui attendent ses faits passent à la ronde suivante.

## Les rondes

Une ronde pose toutes les questions dont les prérequis sont tranchés. Une question qui dépend d'une réponse encore
ouverte attend la ronde suivante. Attends les réponses, regarde ce qui est devenu posable, puis pose la ronde suivante.

## En QCM

Pose chaque ronde avec l'outil de questions à choix (AskUserQuestion), jamais en liste de texte :
- une question par décision, de 2 à 4 options, ta recommandation en premier avec « (recommandé) » dans son libellé ;
- pour chaque option, une description courte : ce qu'elle implique, ce qu'elle coûte ;
- un aperçu en ASCII (`preview`) quand on compare des variantes d'interface : boutons, menu, légende ;
- 4 questions au plus par appel : au-delà, enchaîne les appels ;
- les faits trouvés dans le dépôt vont dans un court message juste avant l'appel, pour que le choix se fasse sur pièces.

Le propriétaire peut répondre hors des options. Lis sa réponse telle quelle : elle peut ouvrir une question nouvelle,
à creuser dans le code avant la ronde suivante.

## Ce que tu ne lâches pas

- **« je ne sais pas »** n'est pas une réponse finale : propose des options, ce qu'elles coûtent, et ta recommandation ;
- **la complaisance** : si tout semble clair, cherche encore (cas limites, données réelles, erreurs, valeurs absentes).

## La taille

Un sujet évident : une ronde suffit. Un sujet qui touche plusieurs écrans ou plusieurs modules : autant de rondes qu'il
en faut, jusqu'à ce qu'aucune question ne reste ouverte.

## La synthèse

Quand plus rien n'est ouvert : la liste des décisions, ce qui reste ouvert et ce qui est hors du périmètre, puis le
brouillon du document. Demande en QCM : « Aligné ? Je le crée, ou on ajuste ? » Rien n'est créé sans cet accord, sauf
si le propriétaire a demandé de le créer directement.
