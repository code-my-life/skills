# Règles Clean Architecture

Distillé de « Clean Architecture » (Robert C. Martin, 2017), étudié en entier : rapport complet dans
code-my-life/clean-code-book, `notes/rapport-clean-architecture.md`. Ici : la Dependency Rule, les 21 règles
vérifiables sur le graphe de dépendances, les métriques du livre, la hiérarchie de mise en place et les outils par
stack. « Dépendance » = dépendance de code source : import, include, require, nom qualifié, héritage, implémentation,
instanciation, annotation, type référencé.

## La Dependency Rule et les cercles

Quatre cercles, du centre vers le bord : **Entities** (règles métier de l'entreprise), **Use Cases** (règles métier de
l'application, les interactors), **Interface Adapters** (controllers, presenters, gateways : la conversion de format),
**Frameworks and Drivers** (web, base de données, UI, le câblage). La règle : **toute dépendance de code source pointe
vers l'intérieur**. Rien dans un cercle intérieur ne mentionne le nom de quoi que ce soit déclaré dans un cercle
extérieur : ni fonction, ni classe, ni format de données. Le flux de contrôle traverse en sens inverse grâce au
polymorphisme : le use case appelle une interface qu'il possède (output port), implémentée dehors. Niveau d'une
politique = sa distance aux entrées/sorties.

## Les 21 règles du graphe

Chaque règle : énoncé, signal de violation, verdict (outil / signal / consigne, au sens de clean-audit).

1. **Dependency Rule** (ch. 22) : les dépendances pointent vers l'intérieur. Violation : un module entities ou use
   cases importe un contrôleur, un framework, un driver, un ORM ; type extérieur en paramètre, retour, champ,
   annotation ; héritage d'une classe de framework. Verdict : outil (avec un mapping chemins vers cercles).
2. **ADP, pas de cycles** (ch. 14) : le graphe des composants est un DAG. Violation : tout cycle détecté. Remèdes du
   livre : DIP (interface chez l'utilisateur) ou nouveau composant commun. Verdict : outil.
3. **SDP, dépendre vers le stable** (ch. 14) : I décroît le long de chaque arête. Violation : une arête A vers B avec
   I(A) < I(B). Verdict : outil (le remède se juge).
4. **SAP, stable donc abstrait** (ch. 14) : D = |A+I-1| proche de 0. Violation : composant concret et très dépendu
   (zone of pain, douloureuse si volatile) ; composant abstrait sans dépendants (zone of uselessness). Verdict :
   signal (la volatilité se juge, le churn git l'approxime).
5. **DIP sur le volatil** (ch. 11) : ne dépendre que d'abstractions pour ce qui est volatil ; le concret stable
   (stdlib, plateforme) est toléré. Violation : import, héritage ou new d'une classe concrète volatile hors
   factories et Main. Verdict : signal (la volatilité se juge).
6. **Les détails dans les cercles externes** (ch. 22, 23, 30, 31, 32) : SQL confiné aux adapters ; ni HTTP, ni ORM,
   ni annotations de framework dans entities et use cases ; les data mappers vivent dans la couche base. Violation :
   un import SQL/ORM/HTTP/framework dans un module intérieur. Verdict : outil.
7. **Des structures simples traversent les frontières** (ch. 20, 22) : jamais une Entity ni une row de base.
   Violation : un gateway qui retourne un type de l'ORM ; une Entity passée au presenter ; un request/response model
   qui référence une Entity ou dérive d'un type de framework. Verdict : outil.
8. **Les frontières se traversent par des ports** (ch. 22) : un use case qui appelle vers l'extérieur passe par une
   interface qu'il possède. Violation : import direct d'un presenter, d'un mailer, d'un client HTTP concret depuis
   un use case. Verdict : outil.
9. **L'interface appartient à l'utilisateur** (ch. 25) : l'interface se déclare dans le composant de haut niveau qui
   l'appelle, l'implémentation chez le fournisseur. Violation : interface déclarée à côté de son unique
   implémentation et importée par le haut niveau (l'inversion n'a pas eu lieu). Verdict : signal.
10. **L'injection au Main seulement** (ch. 26, 32) : le framework d'injection n'est connu que du point de composition,
    qui distribue ensuite normalement. Violation : annotations ou lookup du conteneur dans le code métier ; new de
    concret volatil hors Main et factories. Verdict : outil.
11. **Main est une feuille** (ch. 26) : rien ne dépend de Main. Violation : un import du module de composition depuis
    un autre composant. Verdict : outil.
12. **ISP/CRP, dépendre du nécessaire** (ch. 10, 13) : une interface grasse dont les clients n'utilisent que des
    sous-ensembles disjoints se ségrège. Violation mesurable : ratio symboles utilisés / symboles exposés. Verdict :
    signal.
13. **CCP/SRP des composants** (ch. 7, 13) : ce qui change ensemble vit ensemble. Signal : fichiers co-modifiés
    systématiquement dans des composants différents (historique git) ; un fichier modifié par des acteurs différents
    pour des raisons différentes. Verdict : signal.
14. **Aucune connaissance physique du bas niveau** (ch. 18) : ni URI, ni hôte, ni chemin d'un service de bas niveau en
    dur dans un module de haut niveau ; la configuration s'injecte. Verdict : outil.
15. **Pas de saut de couche non déclaré** (ch. 34) : un contrôleur web n'accède jamais directement au repository.
    Violation : toute arête qui court-circuite une couche déclarée. Verdict : outil.
16. **Encapsulation des composants** (ch. 34) : seuls les types d'entrée d'un composant sont publics ou publiés.
    Violation : implémentations exportées ; imports profonds qui contournent l'interface du composant. Verdict :
    outil (la visibilité du langage, voir la hiérarchie).
17. **Les tests, cercle le plus externe** (ch. 28) : les tests dépendent vers l'intérieur, rien ne dépend d'eux ; les
    règles métier se testent sans GUI ni infrastructure. Violations : code de production qui importe du code de
    test (outil) ; couplage structurel un-test-par-classe systématique et tests de règles métier qui passent par le
    GUI (signal : fragile tests problem).
18. **Frontière matérielle en embarqué** (ch. 29) : registres et extensions compilateur sous la HAL, l'OS sous
    l'OSAL, les #ifdef de cible jamais répétés. Verdict : outil.
19. **Screaming architecture** (ch. 21) : l'arborescence de premier niveau nomme le domaine et les use cases, pas le
    framework. Le test décisif : chaque use case se teste sans serveur web ni base connectée. Verdict : signal
    (le test décisif : outil, c'est un test).
20. **Le cœur ignore ses plugins** (ch. 17) : UI, base, delivery dépendent du cœur métier, jamais l'inverse.
    Violation : une arête du cœur vers un plugin. Verdict : outil.
21. **LSP, substituabilité** (ch. 9) : toute implémentation d'une interface (classe, module, service REST) se
    substitue aux autres sans que le client le remarque. Violation : le client détecte le type concret (instanceof,
    cast descendant, if sur le type, if sur l'URI du fournisseur) ; une implémentation lève « non supporté » ou
    affaiblit le contrat (carré/rectangle). Verdict : signal ; devient outil quand un test de contrat unique
    s'exécute contre chaque implémentation (property-based ou suite partagée).

## Où SOLID se vérifie

| Principe | Formulation du livre | Où dans l'audit | Verdict |
|---|---|---|---|
| SRP | un module répond à un seul acteur | règle 13 (co-modifications git, acteurs multiples) ; proxys de cohésion du catalogue code (ch. 10) | signal |
| OCP | ouvert à l'extension, fermé à la modification | règles 1 et 3 (le protégé ne dépend jamais du protecteur) ; G23 (switch répétés) | outil (sens des arêtes), signal (switch) |
| LSP | substituabilité des implémentations | règle 21 | signal, outil avec tests de contrat |
| ISP | ne pas dépendre de ce qu'on n'utilise pas | règle 12 (interfaces grasses, clients disjoints) | signal |
| DIP | dépendre d'abstractions, pas de concrétions volatiles | règles 1, 5, 10 (imports concrets volatils, new hors Main et factories) | outil avec mapping des couches, signal sur la volatilité |

## Les métriques du livre (ch. 14)

- **Fan-in** : dépendances entrantes ; **Fan-out** : sortantes.
- **I (instabilité) = Fan-out / (Fan-in + Fan-out)**, de 0 (stable) à 1 (instable).
- **A (abstraction) = Na / Nc** : classes abstraites et interfaces sur total. Transposer : interfaces et types exportés
  sans implémentation (TypeScript, Python protocols), interfaces Go, traits Rust.
- **D (distance de la main sequence) = |A + I - 1|** : 0 = bien placé. Usage du livre : examiner tout composant dont D
  s'éloigne de 0 ; suivre D par composant au fil des releases avec un seuil de contrôle (exemple du livre : 0,1).
- Mise en garde du livre : « a metric is not a god » ; ces métriques orientent l'examen, elles ne condamnent pas.

## La hiérarchie de mise en place (ch. 34, Simon Brown)

Dans l'ordre d'efficacité ; chaque niveau rattrape ce que le précédent ne couvre pas :

1. **Le compilateur et la visibilité du langage** : ce que le code ne peut physiquement pas violer. Packages
   non exportés (Go internal/), package-private (Java), internal (C#, Kotlin), pub(crate) (Rust), exports du
   package.json et project references (TypeScript), `__all__` (Python). Sans modificateurs d'accès, tous les styles
   d'organisation s'effondrent en couches molles : c'est l'argument central de Brown.
2. **Les tests d'architecture** : le graphe vérifié à chaque CI. dependency-cruiser ou eslint-boundaries (JS/TS),
   import-linter (Python), ArchUnit (Java/Kotlin), NetArchTest (.NET), deptrac (PHP), depguard (Go), cargo-modules
   (Rust) ; détection de cycles : madge, ou l'outil ci-dessus.
3. **Les hooks git et la CI** : les règles des niveaux 1 et 2 exécutées avant chaque commit/push et sur chaque PR,
   plus les règles de code (linter, formateur, couverture) ; un hook d'agent (par exemple PostToolUse de Claude Code)
   donne le même verdict pendant que l'agent code.
4. **La discipline et les consignes** : CLAUDE.md, AGENTS.md, revues. Le livre est explicite : la discipline échoue
   sous pression de budget et de délai ; elle ne porte que ce qui ne se mesure pas.

## Transpositions modernes

- **Composant** : l'unité de build et de propriété (package de monorepo, workspace pnpm/Cargo, module Gradle, projet
  Bazel) ; le graphe déclaré du monorepo est le graphe à contrôler, ADP et SDP s'y appliquent tels quels.
- **Front (React, Vue, SwiftUI)** : le Humble Object devient : composants d'affichage purs (rendu de props), logique
  dans des hooks, stores ou présenteurs testables sans DOM ; le ViewModel de strings et booléens devient les props
  calculées et les selectors ; la règle testable : la logique d'un écran se teste sans navigateur.
- **ORM** : signaux actuels de la règle 7 : entités Prisma/TypeORM/ActiveRecord/SQLAlchemy qui fuient dans les use
  cases ou le front ; types générés par l'ORM servant de request/response models ; une vue qui requête la base.
- **Main** : le framework (Next.js, NestJS, Spring Boot, serverless) possède le point d'entrée ; « Main » devient le
  module de composition ; les annotations et hooks du framework restent au-dessus des adapters.
- **Services** : des services qui ne font que découper un comportement sont des appels de fonction coûteux ; les
  vraies frontières traversent les services (component-based services, monolithe modulaire). Le couplage par les
  données partagées survit au réseau.
- **Base de données** : le data model est architecturalement significatif, le logiciel base est un détail ; la règle
  porte sur la dépendance du code au logiciel (SQL, ORM dans les cercles intérieurs), pas sur la conception du schéma.
- **Petit projet** : le minimum vital (voir calibrage.md) : pas de cycles, le cœur sans imports de
  framework/base/HTTP, un point d'entrée qui câble. Les frontières complètes (ports réciproques, DTO partout) sont
  des partial boundaries à activer au point d'inflexion, quand ignorer coûte plus cher qu'implémenter.
