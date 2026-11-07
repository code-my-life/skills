# Le rapport d'architecture

Le rapport est une page HTML unique, publiée en **artifact privé** (skill `artifact-design` : son contrat vaut pour la mise
en page, les thèmes, les bibliothèques). Les diagrammes portent le poids ; la prose est rare, simple, et emploie le
vocabulaire de [vocabulaire.md](vocabulaire.md) sans cérémonie.

## En-tête

Le nom du dépôt, la date, et une légende compacte : boîte pleine = module, trait pointillé = couture, flèche rouge =
fuite, boîte épaisse et sombre = module profond. Pas de paragraphe d'introduction : on entre directement dans les
candidats.

## Une carte par candidat

- **Titre** : court, il nomme l'approfondissement (« Fusionner la chaîne d'arrivée des commandes »).
- **Pastilles** : la force de la recommandation (`Forte`, `À explorer`, `Spéculative`) et la catégorie de dépendance
  (voir [approfondir.md](approfondir.md)).
- **Fichiers** : la liste, en chasse fixe.
- **Schéma avant / après** : le centre de la carte, deux colonnes côte à côte (voir les motifs plus bas).
- **Problème** : une phrase. Ce qui fait mal.
- **Solution** : une phrase. Ce qui change.
- **Gains** : des puces de six mots au plus, dans les termes du glossaire : « localité : les bugs se concentrent dans un
  module », « levier : une interface, N appelants », « l'interface rétrécit ; l'implémentation absorbe les
  enveloppes ». Jamais « plus facile à maintenir » ni « code plus propre » : ces mots ne sont pas dans le glossaire.
- **Encart ADR** (si besoin) : une ligne, dans une boîte teintée d'ambre.

Pas de paragraphes d'explication : si le schéma a besoin d'un paragraphe pour se comprendre, redessine-le.

Finis par une section **Première recommandation** : le candidat que tu traiterais d'abord, et pourquoi, en une phrase,
avec un lien vers sa carte.

## Motifs de schéma

Prends celui qui convient, et varie : la variété fait partie de l'intérêt.

- **Graphe** (dépendances, flux d'appels) : « X appelle Y qui appelle Z, et regarde le désordre ». Colorie en rouge les
  arêtes qui fuient et en sombre le module profond. Un diagramme de séquence montre bien « avant : 6 allers-retours ;
  après : 1 ».
- **Boîtes et flèches dessinées à la main**, quand la mise en page automatique résiste : surtout pour que l'« après »
  ressemble à un seul module profond à bordure épaisse, aux entrailles estompées.
- **Coupe** (couches peu profondes) : des bandes horizontales empilées. Avant : 6 couches minces qui ne font rien.
  Après : 1 bande épaisse, nommée par la responsabilité réunie.
- **Masse** (« interface aussi large que l'implémentation ») : deux rectangles par module, l'un pour la surface
  d'interface, l'autre pour l'implémentation. Avant, l'interface est presque aussi haute que l'implémentation (peu
  profond). Après, l'interface est courte et l'implémentation haute (profond).
- **Effondrement de l'arbre d'appels** : avant, un arbre d'appels en boîtes imbriquées. Après, le même arbre réduit à
  une boîte, les appels devenus internes estompés dedans.

## Style

Éditorial, pas tableau de bord d'entreprise. Beaucoup d'air. Une couleur d'accent, du rouge pour les fuites, de l'ambre
pour les avertissements. Des schémas de 320 px de haut environ pour que l'avant et l'après tiennent côte à côte sans
défiler. Les étiquettes de module en petites capitales espacées, pour qu'elles se lisent comme un schéma. La page est
statique : aucune interaction.

## Ton

Du français simple et concis, mais les noms et verbes d'architecture viennent du glossaire. **À employer exactement** :
module, interface, implémentation, profondeur, profond, peu profond, couture, adaptateur, levier, localité. **Jamais à
leur place** : composant, service, unité (pour module) ; API, signature (pour interface) ; frontière (pour couture) ;
couche, enveloppe (pour module, quand c'est de module qu'on parle).

Phrases qui conviennent : « Le module d'arrivée des commandes est peu profond : son interface égale presque son
implémentation. » « La tarification fuit à travers la couture. » « Approfondir : une interface, un seul endroit où
tester. » « Deux adaptateurs justifient la couture : HTTP en production, en mémoire dans les tests. »

Pas de précaution oratoire. Si une phrase peut être une puce, fais-en une puce. Si une puce peut être coupée, coupe-la.

---

Adapté de `HTML-REPORT.md` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317, avec un artifact privé au lieu d'un
fichier dans `/tmp`.
