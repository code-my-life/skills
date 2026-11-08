# Calibrage

Comment appliquer les deux livres sans dogme. Les garde-fous viennent des livres eux-mêmes : Martin présente son
école comme une école (« don't make the mistake of thinking that we are somehow "right" in any absolute sense ») et
ses chiffres comme des préférences d'expérience.

## Les seuils sont des préférences

- Fonctions de 2 à 4 lignes : « This is not an assertion that I can justify » (ch. 3 de Clean Code).
- Fichiers de 200 à 500 lignes : « should not be a hard and fast rule » (ch. 5).
- 120 caractères : « I personally set my limit at 120 » (ch. 5).
- « A metric is not a god; it is merely a measurement against an arbitrary standard » (ch. 14 de Clean Architecture).

Conséquence pour un audit : un seuil se propose avec sa mesure sur le code réel, jamais comme une vérité.

## Calibrer sur l'existant

1. Mesurer la distribution actuelle (longueur des fonctions, arguments, imbrication, D par composant).
2. Poser le seuil au niveau qui bloque la régression, pas au niveau du livre : si le 95e centile des fonctions fait
   35 lignes, le seuil de départ est 35, pas 20 ; il descendra quand le code descendra.
3. Contrôler les lignes ajoutées et modifiées seulement. L'existant ne se réécrit pas pour un garde-fou : c'est le
   Boy Scout (laisser un peu plus propre que trouvé), pas la campagne de réécriture.
4. Prévoir l'échappatoire : chaque règle outillée dit comment on la désactive localement (commentaire de
   désactivation nominatif, avec raison), et ce taux de désactivation se surveille.

## Le minimum vital selon la taille

Le livre l'admet : on n'applique pas la clean architecture à un programme de 200 lignes, et un monolithe sans
composants convient à une petite équipe qui démarre. Le problème est de ne jamais payer la dette.

- **Petit projet (un dossier, une personne)** : trois garde-fous : pas de cycles ; le cœur métier sans imports de
  framework, de base ni de HTTP ; un point d'entrée qui câble tout. Plus un formateur et un linter de base.
- **Projet qui grossit** : surveiller les premiers frottements (fichiers co-modifiés en masse, D qui dérive, PR qui se
  marchent dessus) et implémenter la frontière « au point d'inflexion, quand le coût d'implémenter devient inférieur
  au coût d'ignorer » (ch. 25).
- **Gros projet, plusieurs équipes** : la panoplie complète, dans l'ordre de la hiérarchie de mise en place.

La sur-ingénierie est l'échec symétrique : « over-engineering is often much worse than under-engineering » ; ROSE est
mort de ses couches (annexe du livre). Une frontière coûte des interfaces réciproques, des DTO, de l'administration :
les frontières partielles (Strategy seul, Facade, « tout sauf la dernière étape ») existent pour ça, avec leur risque
assumé d'érosion.

## Les tolérances des livres

À rappeler dans un audit pour chaque règle voisine, pour juger au lieu de condamner :

- **Switch** : approprié là où ajouter des fonctions est plus probable qu'ajouter des types ; la règle : un seul par
  type de sélection, qui fabrique du polymorphisme (G23).
- **Statique** : légitime si toutes les données viennent des arguments et qu'aucun polymorphisme n'est plausible (G18).
- **Nombres nus** : tolérés quand ils se lisent mieux que leur constante (5280 ; TWO serait absurde) (G25).
- **Feature Envy** : parfois un mal nécessaire, pour ne pas coupler une donnée à son format de sortie (G14).
- **Plusieurs asserts** : la vraie règle est un concept par test, pas un assert par test (ch. 9).
- **Return multiples, break, continue** : admis dans une petite fonction (ch. 3).
- **Dépendre du concret stable** : stdlib et plateforme se consomment telles quelles ; le DIP vise le volatil, et ses
  violations résiduelles se concentrent dans Main (ch. 11).
- **Duplication** : distinguer la vraie (change toujours ensemble : unifier) de l'accidentelle (évolutions
  divergentes : laisser) ; unifier deux écrans qui se ressemblent par réflexe est une erreur (ch. 16 de Clean
  Architecture).
- **Compromis assumés** : le livre lui-même en signe (errorMessage dans ArgsException : « Frankly, it's a
  compromise ») ; un audit peut en accepter, à condition de les écrire.

## Divergences modernes à signaler sans imposer

L'école Martin a des positions que la pratique actuelle conteste ; un audit les signale comme choix d'équipe, jamais
comme défaut : l'extraction très agressive en micro-fonctions et micro-classes (coût de navigation ; sa propre règle 4
du simple design sert de contrepoids) ; les imports wildcard (J1) ; son rejet de final/const sur les arguments, contre
la préférence actuelle pour l'immutabilité déclarée ; l'event sourcing présenté comme simple (coûts réels de
versioning et de projections).

## L'esprit

La dernière ligne du chapitre 17 : la liste « implique un système de valeurs » ; « Professionalism and craftsmanship
come from values that drive disciplines ». Un audit transmet l'arbitrage, pas seulement les règles : les quatre règles
du simple design sont ordonnées (tests, duplication, expression, économie d'entités) précisément pour trancher quand
elles se contredisent.
