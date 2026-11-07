# Le vocabulaire de l'architecture

Concevoir des **modules profonds** : beaucoup de comportement derrière une petite interface, posée à une couture nette,
testable par cette interface. Ces mots s'emploient tels quels partout où du code se conçoit ou se restructure. Le but est
le **levier** pour ceux qui appellent, la **localité** pour ceux qui maintiennent, et la testabilité pour tous.

## Glossaire

N'emploie pas « composant », « service », « API » ou « frontière » à leur place. Un langage constant est tout l'enjeu.

**Module** : tout ce qui a une interface et une implémentation. Volontairement indifférent à l'échelle : une fonction,
une classe, un paquet, une tranche qui traverse plusieurs niveaux. _À éviter_ : unité, composant, service.

**Interface** : tout ce qu'un appelant doit savoir pour utiliser correctement le module : la signature de types, mais
aussi les invariants, l'ordre des appels, les erreurs possibles, la configuration requise, les caractéristiques de
performance. _À éviter_ : API, signature (trop étroits : ils ne disent que le niveau des types).

**Implémentation** : ce qu'il y a dans un module, son corps de code. Distincte de l'**adaptateur** : une chose peut être
un petit adaptateur avec une grosse implémentation (un dépôt Postgres) ou un gros adaptateur avec une petite
implémentation (un faux en mémoire). On dit « adaptateur » quand la couture est le sujet, « implémentation » sinon.

**Profondeur** : le levier à l'interface. La quantité de comportement qu'un appelant (ou un test) exerce par unité
d'interface à apprendre. Un module est **profond** quand beaucoup de comportement tient derrière une petite interface,
**peu profond** quand l'interface est presque aussi complexe que l'implémentation.

**Couture** _(Michael Feathers)_ : un endroit où l'on peut changer le comportement sans éditer à cet endroit ; le
**lieu** où vit l'interface d'un module. Où poser la couture est une décision à part, distincte de ce qu'on met derrière.
_À éviter_ : frontière (surchargé par le « bounded context » du DDD).

**Adaptateur** : une chose concrète qui satisfait une interface à une couture. Il décrit un **rôle** (la place qu'il
remplit), pas une substance (ce qu'il contient).

**Levier** : ce que les appelants tirent de la profondeur. Plus de capacité par unité d'interface apprise. Une
implémentation rembourse sur N appelants et M tests.

**Localité** : ce que les mainteneurs tirent de la profondeur. Le changement, les bugs, le savoir et la vérification se
concentrent à un seul endroit au lieu de se répandre chez les appelants. Corrigé une fois, corrigé partout.

## Profond contre peu profond

**Module profond** = petite interface + beaucoup d'implémentation :

```
┌─────────────────────┐
│   Petite interface  │  ← peu de méthodes, paramètres simples
├─────────────────────┤
│                     │
│ Implémentation      │  ← la logique complexe est cachée
│ profonde            │
│                     │
└─────────────────────┘
```

**Module peu profond** = grande interface + peu d'implémentation (à éviter) :

```
┌─────────────────────────────────┐
│       Grande interface          │  ← beaucoup de méthodes, paramètres complexes
├─────────────────────────────────┤
│  Implémentation mince           │  ← ne fait que passer l'appel
└─────────────────────────────────┘
```

En concevant une interface, demande-toi : puis-je réduire le nombre de méthodes ? Simplifier les paramètres ? Cacher plus
de complexité à l'intérieur ?

## Principes

- **La profondeur est une propriété de l'interface, pas de l'implémentation.** Un module profond peut être composé en
  interne de petites pièces, simulables et remplaçables ; elles ne sont simplement pas dans l'interface. Un module peut
  avoir des **coutures internes** (privées à son implémentation, utilisées par ses propres tests) en plus de la
  **couture externe** à son interface.
- **Le test de suppression.** Imagine supprimer le module. Si la complexité disparaît, c'était un simple passe-plat. Si
  elle réapparaît chez N appelants, il méritait sa place.
- **L'interface est la surface de test.** Les appelants et les tests franchissent la même couture. Si l'on veut tester
  **au-delà** de l'interface, le module n'a sans doute pas la bonne forme.
- **Un adaptateur fait une couture hypothétique, deux en font une vraie.** N'introduis pas de couture si rien ne varie à
  travers elle.

## Concevoir pour tester

1. **Accepter les dépendances, ne pas les créer.** `traiter(commande, passerelle)` se teste ; `traiter(commande)` qui
   fabrique sa propre passerelle, non.
2. **Rendre des résultats, ne pas produire d'effets de bord.** Une fonction qui calcule la remise et la rend se teste ;
   une qui modifie le total du panier, non.
3. **Une petite surface.** Moins de méthodes, moins de tests. Moins de paramètres, un montage de test plus simple.

## Relations

- Un **module** a exactement une **interface** (la surface qu'il présente aux appelants et aux tests).
- La **profondeur** est une propriété du **module**, mesurée contre son **interface**.
- Une **couture** est l'endroit où vit l'**interface** d'un **module**.
- Un **adaptateur** se trouve à une **couture** et satisfait l'**interface**.
- La **profondeur** donne du **levier** aux appelants et de la **localité** aux mainteneurs.

## Cadrages écartés

- **La profondeur comme rapport lignes d'implémentation sur lignes d'interface** (Ousterhout) : elle récompense le
  remplissage de l'implémentation. On prend la profondeur comme levier.
- **« Interface » comme le mot-clé `interface` de TypeScript ou les méthodes publiques d'une classe** : trop étroit,
  l'interface comprend tout ce qu'un appelant doit savoir.
- **« Frontière »** : surchargé par le « bounded context » du DDD. Dis **couture** ou **interface**.

---

Adapté de `codebase-design` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
