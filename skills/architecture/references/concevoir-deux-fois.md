# Concevoir deux fois

Quand le propriétaire veut comparer des interfaces possibles pour un candidat retenu, applique ce motif de sous-agents en
parallèle. Il vient de « Design It Twice » (Ousterhout) : la première idée a peu de chances d'être la meilleure.

Il emploie le vocabulaire de [vocabulaire.md](vocabulaire.md) : **module**, **interface**, **couture**, **adaptateur**,
**levier**.

## Étapes

### 1. Poser le problème

Avant de lancer les sous-agents, écris pour le propriétaire une explication du problème pour le candidat retenu :
- les contraintes que toute nouvelle interface devrait satisfaire ;
- les dépendances sur lesquelles elle reposerait, et leur catégorie (voir [approfondir.md](approfondir.md)) ;
- une esquisse de code pour rendre les contraintes concrètes : pas une proposition, un moyen de les ancrer.

Montre-la, puis passe tout de suite à l'étape 2 : il lit et réfléchit pendant que les sous-agents travaillent.

### 2. Lancer les sous-agents

Lance au moins 3 sous-agents en parallèle, chacun avec un contexte vierge, qui ne lancent ni skill ni agent. Chacun doit
produire une interface **radicalement différente** pour le module approfondi.

Donne à chacun un dossier technique séparé (chemins de fichiers, détails de couplage, catégorie de dépendance, ce qui
se trouve derrière la couture), indépendant de l'explication de l'étape 1. Donne à chacun une contrainte de conception
différente :
- Agent 1 : « Minimise l'interface : 1 à 3 points d'entrée au plus. Maximise le levier par point d'entrée. »
- Agent 2 : « Maximise la souplesse : beaucoup d'usages et d'extension. »
- Agent 3 : « Optimise pour l'appelant le plus courant : le cas par défaut doit être trivial. »
- Agent 4 (si cela s'applique) : « Conçois autour de ports et d'adaptateurs pour les dépendances qui traversent la
  couture. »

Joins le vocabulaire de [vocabulaire.md](vocabulaire.md) à chaque dossier, pour que chaque sous-agent nomme les choses
comme l'architecture du dépôt.

Chacun rend :
1. l'interface (types, méthodes, paramètres, plus invariants, ordre, erreurs) ;
2. un exemple d'usage montrant comment les appelants s'en servent ;
3. ce que l'implémentation cache derrière la couture ;
4. la stratégie de dépendances et les adaptateurs (voir [approfondir.md](approfondir.md)) ;
5. les compromis : où le levier est fort, où il est mince.

### 3. Présenter et comparer

Présente les conceptions l'une après l'autre pour que le propriétaire les absorbe, puis compare-les en prose. Oppose-les
par **profondeur** (le levier à l'interface), **localité** (où le changement se concentre) et **placement de la
couture**.

Après la comparaison, donne ta recommandation : laquelle te paraît la plus forte et pourquoi. Si des éléments de
conceptions différentes s'accordent bien, propose un hybride. Sois tranché : le propriétaire veut une lecture forte, pas
un menu. Il décide en QCM (outil AskUserQuestion).

---

Adapté de `DESIGN-IT-TWICE.md` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
