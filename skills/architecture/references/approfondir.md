# Approfondir

Comment approfondir sans casser un groupe de modules peu profonds, selon ses dépendances. Suppose le vocabulaire de
[vocabulaire.md](vocabulaire.md) : **module**, **interface**, **couture**, **adaptateur**.

## Les catégories de dépendances

En jugeant un candidat, classe ses dépendances. La catégorie décide comment le module approfondi se teste à travers sa
couture.

### 1. Dans le processus

Du calcul pur, un état en mémoire, aucune entrée-sortie. Toujours approfondissable : fusionne les modules et teste par la
nouvelle interface directement. Aucun adaptateur nécessaire.

### 2. Substituable en local

Des dépendances qui ont un remplaçant local pour les tests (PGLite pour Postgres, un système de fichiers en mémoire).
Approfondissable si le remplaçant existe. Le module approfondi se teste avec le remplaçant dans la suite de tests. La
couture est interne ; aucun port à l'interface externe du module.

### 3. À distance, mais à nous (ports et adaptateurs)

Nos propres services de l'autre côté d'un réseau (microservices, API internes). Définis un **port** (une interface) à la
couture. Le module profond porte la logique ; le transport est injecté comme **adaptateur**. Les tests prennent un
adaptateur en mémoire, la production un adaptateur HTTP, gRPC ou file d'attente.

Forme de recommandation : « Définir un port à la couture, écrire un adaptateur HTTP pour la production et un adaptateur
en mémoire pour les tests, pour que la logique tienne dans un seul module profond même déployée à travers un réseau. »

### 4. Vraiment externe (simulé)

Des services tiers (Stripe, Twilio...) qu'on ne contrôle pas. Le module approfondi reçoit la dépendance externe comme
port injecté ; les tests fournissent un adaptateur simulé.

## Discipline des coutures

- **Un adaptateur fait une couture hypothétique, deux en font une vraie.** N'introduis pas de port sans au moins deux
  adaptateurs justifiés (en général la production et le test). Une couture à un seul adaptateur n'est que de
  l'indirection.
- **Coutures internes contre externes.** Un module profond peut avoir des coutures internes (privées à son
  implémentation, utilisées par ses propres tests) en plus de la couture externe à son interface. N'expose pas une
  couture interne par l'interface parce que les tests s'en servent.

## Stratégie de test : remplacer, pas empiler

- Les anciens tests unitaires de modules peu profonds deviennent du déchet dès que des tests existent à l'interface du
  module approfondi : supprime-les.
- Écris les nouveaux tests à l'interface du module approfondi. **L'interface est la surface de test.**
- Les tests affirment des résultats observables par l'interface, pas un état interne.
- Les tests doivent survivre aux refontes internes : ils décrivent un comportement, pas une implémentation. Un test qu'il
  faut changer quand l'implémentation change teste au-delà de l'interface.

---

Adapté de `DEEPENING.md` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
