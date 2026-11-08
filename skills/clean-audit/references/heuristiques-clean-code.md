# Heuristiques Clean Code

Distillé de « Clean Code » (Robert C. Martin, 2008), étudié en entier : rapports complets dans
code-my-life/clean-code-book, `notes/rapport-clean-code.md`. Chaque entrée porte son verdict :
**outil** (vérifiable par un programme), **signal** (un programme détecte, un humain tranche),
**consigne** (pur jugement, à transmettre en texte d'agent).

## Seuils chiffrés du livre

Ce sont des préférences d'expérience, pas des lois (voir calibrage.md) : le livre le dit lui-même.

| Mesure | Le livre | Seuil d'audit raisonnable |
|---|---|---|
| Longueur d'une fonction | « hardly ever be 20 lines long », idéal montré : 2 à 4 | alerte au-delà de 20 lignes |
| Imbrication dans une fonction | un ou deux niveaux au plus | alerte au-delà de 2 |
| Arguments d'une fonction | 0 idéal, 3 « à éviter », plus de 3 refusé | alerte à 3, refus au-delà |
| Longueur d'un fichier | typiquement ~200 lignes, limite haute 500 | alerte au-delà de 500 |
| Largeur de ligne | 80 arbitraire, 100-120 acceptable, Martin : 120 | le formateur du projet tranche |
| Asserts par test | minimiser ; un concept par test | un concept par test |
| Return/break/continue | multiples admis dans une petite fonction | aucune règle « un seul return » |

## Catalogue du chapitre 17 (66 codes)

### Commentaires (C)

| Code | Nom | Prescription | Verdict |
|---|---|---|---|
| C1 | Inappropriate Information | L'historique, l'auteur, la date appartiennent au VCS et au tracker, pas aux commentaires. | signal |
| C2 | Obsolete Comment | Un commentaire périmé se met à jour ou se supprime. | signal |
| C3 | Redundant Comment | Un commentaire qui redit le code se supprime ; il doit dire ce que le code ne peut pas dire. | signal |
| C4 | Poorly Written Comment | Un commentaire qui mérite d'exister s'écrit bien : bref, précis, grammatical. | consigne |
| C5 | Commented-Out Code | Le code commenté se supprime ; le VCS s'en souvient. | outil |

### Environnement (E)

| Code | Nom | Prescription | Verdict |
|---|---|---|---|
| E1 | Build Requires More Than One Step | Le build tient en une commande. | outil |
| E2 | Tests Require More Than One Step | Tous les tests se lancent en une commande. | outil |

### Fonctions (F)

| Code | Nom | Prescription | Verdict |
|---|---|---|---|
| F1 | Too Many Arguments | Zéro argument idéal ; plus de trois se refuse. | outil |
| F2 | Output Arguments | Une fonction qui change un état change celui de son propre objet, pas d'un argument. | signal |
| F3 | Flag Arguments | Un booléen en argument révèle une fonction qui fait deux choses : scinder. | outil |
| F4 | Dead Function | Une fonction jamais appelée se supprime. | outil |

### Général (G)

| Code | Nom | Prescription | Verdict |
|---|---|---|---|
| G1 | Multiple Languages in One Source File | Un langage par fichier ; minimiser l'étendue des autres. | signal |
| G2 | Obvious Behavior Is Unimplemented | Le comportement que tout lecteur attend existe (moindre surprise). | consigne |
| G3 | Incorrect Behavior at the Boundaries | Chaque condition limite se cherche et se teste. | signal |
| G4 | Overridden Safeties | Warnings coupés et tests désactivés : dette immédiate, à refuser. | outil |
| G5 | Duplication | Chaque duplication est une abstraction manquée : méthode, polymorphisme, Template Method ou Strategy. | outil (textuelle), signal (structurelle) |
| G6 | Code at Wrong Level of Abstraction | Les détails restent dans les bas niveaux ; une base générique ignore les détails de ses usages. | consigne |
| G7 | Base Classes Depending on Their Derivatives | Une classe de base ne mentionne jamais ses dérivées. | outil |
| G8 | Too Much Information | Interfaces petites et resserrées : peu de méthodes, peu d'exposé. | signal |
| G9 | Dead Code | Le code jamais exécuté (branche impossible, catch sans throw) s'enterre. | outil |
| G10 | Vertical Separation | Variables déclarées près de leur usage ; fonctions privées sous leur premier appel. | outil |
| G11 | Inconsistency | La même chose se fait de la même façon partout (noms, formes parallèles). | signal |
| G12 | Clutter | Constructeurs vides, variables inutilisées, commentaires creux : dehors. | outil |
| G13 | Artificial Coupling | Chaque déclaration vit au bon endroit ; une enum générale ne s'enferme pas dans une classe spécifique. | signal |
| G14 | Feature Envy | Une méthode qui manipule surtout les données d'un autre objet change de place (exceptions admises). | signal |
| G15 | Selector Arguments | Un argument qui sélectionne le comportement devient plusieurs fonctions. | signal |
| G16 | Obscured Intent | Expressions compactes et noms cryptiques se déplient en intention visible. | signal |
| G17 | Misplaced Responsibility | Le code se place là où le lecteur s'attend à le trouver. | consigne |
| G18 | Inappropriate Static | Méthode d'instance par défaut ; statique seulement sans aucune chance de polymorphisme. | signal |
| G19 | Use Explanatory Variables | Les calculs se découpent en intermédiaires nommés. | consigne |
| G20 | Function Names Should Say What They Do | Le nom suffit, sans lire l'implémentation. | consigne |
| G21 | Understand the Algorithm | Savoir que la solution est juste, pas seulement que les tests passent. | consigne |
| G22 | Make Logical Dependencies Physical | Demander l'information au module qui la possède au lieu de la supposer. | consigne |
| G23 | Prefer Polymorphism to If/Else or Switch/Case | Au plus un switch par type de sélection, qui fabrique des objets polymorphes. | signal |
| G24 | Follow Standard Conventions | Un standard d'équipe fondé sur les normes du secteur, outillé ; le code sert de document. | outil |
| G25 | Replace Magic Numbers with Named Constants | Constantes nommées ; tolérance pour l'évident dans une formule lisible. | outil |
| G26 | Be Precise | Décider précisément : null traité, concurrence verrouillée, monnaie hors flottants, types larges déclarés. | consigne |
| G27 | Structure over Convention | Imposer par la structure (méthode abstraite) ce qu'une convention ne force pas. | consigne |
| G28 | Encapsulate Conditionals | Les booléens composés deviennent des fonctions d'intention. | signal |
| G29 | Avoid Negative Conditionals | Les conditions s'expriment au positif. | outil |
| G30 | Functions Should Do One Thing | Une fonction à sections devient plusieurs fonctions. | signal |
| G31 | Hidden Temporal Couplings | Un ordre d'appel obligatoire se rend visible : chaque étape produit l'entrée de la suivante. | consigne |
| G32 | Don't Be Arbitrary | Chaque structure a une raison, communiquée par la structure. | consigne |
| G33 | Encapsulate Boundary Conditions | Les +1/-1 se calculent une fois sous un nom (nextLevel). | signal |
| G34 | Functions Should Descend Only One Level of Abstraction | Toutes les instructions d'une fonction sont un cran sous son nom. | signal |
| G35 | Keep Configurable Data at High Levels | La configuration vit en haut et descend en argument. | signal |
| G36 | Avoid Transitive Navigation | Parler aux voisins immédiats : a.getB().getC() interdit sur des objets. | outil |

### Java (J), à transposer par stack

| Code | Nom | Transposition | Verdict |
|---|---|---|---|
| J1 | Avoid Long Import Lists by Using Wildcards | Daté ; le fond : la liste d'imports dit avec qui le module collabore, l'outillage la gère. | outil |
| J2 | Don't Inherit Constants | Les constantes s'importent, elles ne s'héritent pas. | outil |
| J3 | Constants versus Enums | Types sommes, enums, unions plutôt que des entiers nus. | outil |

### Noms (N)

| Code | Nom | Prescription | Verdict |
|---|---|---|---|
| N1 | Choose Descriptive Names | Les noms font 90 % de la lisibilité ; se réévaluent à chaque lecture. | consigne |
| N2 | Choose Names at the Appropriate Level of Abstraction | Nommer le quoi, pas le comment (connect plutôt que dial). | consigne |
| N3 | Use Standard Nomenclature Where Possible | Patterns et langage du domaine dans les noms. | consigne |
| N4 | Unambiguous Names | Un nom long et exact bat un nom court et flou. | consigne |
| N5 | Use Long Names for Long Scopes | La longueur du nom suit la portée : i sur cinq lignes, un vrai nom au-delà. | signal |
| N6 | Avoid Encodings | Ni type ni portée dans le nom (m_, I, Impl, notation hongroise). | outil |
| N7 | Names Should Describe Side-Effects | Le nom dit tout ce que fait la fonction (createOrReturnOos). | consigne |

### Tests (T)

| Code | Nom | Prescription | Verdict |
|---|---|---|---|
| T1 | Insufficient Tests | Tout ce qui peut casser se teste ; « ça semble assez » ne vaut rien. | signal |
| T2 | Use a Coverage Tool! | La couverture révèle les trous de la stratégie de test. | outil |
| T3 | Don't Skip Trivial Tests | Leur valeur documentaire dépasse leur coût. | consigne |
| T4 | An Ignored Test Is a Question about an Ambiguity | Un test ignoré exprime une exigence floue, à lever. | signal |
| T5 | Test Boundary Conditions | Les limites se testent avec un soin particulier. | signal |
| T6 | Exhaustively Test Near Bugs | Un bug trouvé : la fonction entière se reteste, les bugs vont en groupe. | consigne |
| T7 | Patterns of Failure Are Revealing | Le motif des échecs diagnostique la cause. | consigne |
| T8 | Test Coverage Patterns Can Be Revealing | Ce que les tests verts exécutent explique les rouges. | consigne |
| T9 | Tests Should Be Fast | Un test lent finit retiré sous pression. | outil |

## Règles des chapitres hors catalogue

**Nommage (ch. 2)** : prononçable, cherchable ; un mot par concept dans toute la base (fetch ou get, pas les deux) et
un concept par mot ; classes = noms, méthodes = verbes ; les noms l et O interdits ; le contexte par des classes, pas
par des préfixes. Verdict : signal, sauf l/O et conventions de casse : outil.

**Fonctions (ch. 3)** : une fonction fait une chose, tous ses pas un cran sous son nom (règle du stepdown : lecture de
haut en bas) ; séparation commande/question (CQS) : faire ou répondre, jamais les deux ; aucun effet de bord caché, et
l'inévitable va dans le nom ; exceptions plutôt que codes d'erreur ; un try est le premier mot de sa fonction ; DRY.
Verdict : signal, sauf la détection des codes d'erreur et des try mélangés : outil.

**Commentaires (ch. 4)** : acceptables : licence, intention, clarification d'une API externe, avertissement de
conséquence, TODO référencé, amplification, doc d'API publique. Tout le reste se remplace par du code : un bon nom,
une fonction, une variable. Verdict : outil pour TODO sans référence et code commenté, signal pour le reste.

**Formatage (ch. 5)** : une règle d'équipe unique, appliquée par un formateur automatique ; le fichier se lit comme un
journal (le haut niveau en haut) ; l'appelant au-dessus de l'appelé ; les lignes liées restent collées. Verdict :
outil (le formateur), signal pour l'ordre vertical.

**Objets et structures de données (ch. 6)** : les objets cachent leurs données et exposent du comportement ; les
structures exposent leurs données sans comportement ; les hybrides cumulent les défauts des deux ; loi de Déméter :
une méthode n'appelle que sa classe, ses créations, ses arguments, ses champs ; DTO légitimes ; un Active Record ne
porte pas de règles métier. Verdict : signal (la part mécanique des chaînes d'appels : outil, G36).

**Erreurs (ch. 7)** : exceptions non vérifiées (transposé : erreurs typées Result/Either là où c'est l'idiome) ;
chaque erreur porte son contexte ; les classes d'erreurs se définissent selon l'appelant ; les API tierces
s'enveloppent ; Special Case pour que le flux normal reste plat ; ne jamais retourner null, ne jamais passer null
(transposé : activer la null-safety du langage, listes vides plutôt que null). Verdict : outil pour null-safety et
return null, signal pour le reste.

**Frontières (ch. 8)** : un type tiers (Map, client SDK) reste confiné dans la classe qui l'utilise, jamais dans une
API publique ; learning tests qui exercent l'API tierce comme la production, relancés à chaque montée de version ;
coder contre l'interface qu'on aurait aimée, puis un Adapter. Verdict : outil (types tiers dans les signatures
publiques), consigne pour le reste.

**Tests (ch. 9)** : les trois lois du TDD (un test rouge avant le code ; juste assez de test pour échouer ; juste
assez de code pour passer) ; F.I.R.S.T. : Fast, Independent (ordre quelconque), Repeatable (tout environnement),
Self-Validating (verdict booléen), Timely (juste avant le code) ; le code de test aussi propre que la production, en
moins optimisé si besoin ; un concept par test. Verdict : outil pour Fast/Independent/Repeatable (exécution en ordre
aléatoire, sans réseau), consigne pour le reste.

**Classes (ch. 10)** : petites, mesurées en responsabilités : une seule raison de changer (SRP) ; cohésion : quand des
sous-groupes de méthodes partagent des sous-groupes de champs, une classe veut sortir ; se décrit en 25 mots sans
« si », « et », « ou » ; ouverte à l'extension, fermée à la modification (OCP) ; dépend d'abstractions (DIP).
Verdict : signal (proxys mesurables : méthodes publiques, LCOM), consigne pour la raison de changer.

**Systèmes (ch. 11)** : la construction et le câblage des objets se séparent de l'usage ; tout se construit dans main
ou ses modules, et rien ne dépend de main ; injection de dépendances ; le cœur métier en objets purs du langage, les
préoccupations transverses (logs, transactions, sécurité) en décorateurs ou middleware ; différer les décisions.
Verdict : voir les règles d'architecture (ce chapitre y mène).

**Simple design (ch. 12)**, quatre règles en ordre de priorité : passe tous les tests ; aucune duplication ; exprime
l'intention ; minimise le nombre d'entités (le garde-fou contre le dogme des trois premières). Verdict : consigne,
sauf tests et duplication : outil.

**Concurrence (ch. 13)** : le code concurrent s'isole du reste (c'est une raison de changer à lui seul) ; la portée
des données partagées se restreint sévèrement ; copies et immutabilité plutôt que partage ; sections critiques
minimales ; connaître sa bibliothèque (collections thread-safe, exécuteurs, atomiques) ; un échec intermittent n'est
jamais ignoré ; tester sous charge, sur toutes les plateformes, avec plus de threads que de cœurs. Transposé :
async/await, goroutines, acteurs, immutabilité par défaut, race detectors (Go, TSan). Verdict : signal, sauf
l'exécution répétée sous charge en CI : outil.

## Transpositions hors Java

| Le livre (Java 2008) | Aujourd'hui, toute stack |
|---|---|
| Unchecked exceptions | Le fond : happy path séparé du traitement d'erreur ; erreurs typées (Result, Either, error Go, ? Rust) là où c'est l'idiome |
| Don't return/pass null | Null-safety du langage activée (strict TypeScript, Optional, Option/Maybe) ; Special Case ; collections vides |
| Enums (J3) | Types sommes, unions discriminées, enums |
| Getters/setters javabean | Propriétés, records, data classes ; le fond intact : un objet n'est pas un sac d'accesseurs |
| POJO + aspects (EJB2, Spring XML) | Cœur métier en objets purs ; middleware, décorateurs, intercepteurs au bord |
| synchronized, ConTest | Immutabilité par défaut, async, channels, race detectors ; mêmes principes de défense |
| Wildcard imports (J1) | L'outillage gère les imports ; la liste d'imports reste la carte des collaborations |
| Notation hongroise, m_ | Gagné ; le fond reste : ni type ni portée dans les noms (Impl, préfixe I) |
