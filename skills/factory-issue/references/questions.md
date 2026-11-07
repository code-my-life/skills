# Arbre de questions par type

Les rondes de la section 2 puisent ici. Dans chaque liste, une question suppose les réponses de celles qui la
précèdent : pose ensemble celles dont les prérequis sont tranchés. Cherche d'abord dans le dépôt tout ce qui s'y trouve.

## Avant la première question

1. **Le constat, reproduit** : pour un Bug, reproduis-le toi-même et dis ce que tu as vu. S'il ne se reproduit pas,
   c'est la première question.
2. **Ce qui existe déjà** : le comportement demandé existe-t-il déjà dans le dépôt, en partie ou ailleurs ? Dis où.
3. **Les ADR** : relis les « Écartés » des ADR du dépôt (`docs/decisions/`). Une issue qui contredit une ADR le dit,
   avec sa raison.

## Commun à tous les types

1. **Le constat** : que se passe-t-il aujourd'hui, et où exactement (écran, fichier, commande) ?
2. **L'impact** : pour qui, et qu'est-ce que cela empêche ou coûte ?
3. **Le type** : une référence existe-t-elle (Bug), ou est-ce une apparence (Interface), une logique (Fonctionnalité),
   une cause inconnue (Diagnostic), des tests (Tests), du ménage sans changement de comportement (Maintenance), des
   documents seulement (Documentation) ?
4. **Le périmètre** : qu'est-ce qui ne doit pas changer ?
5. **Les critères** : pour chacun, comment le vérifie-t-on ? Un chiffre, un nom de test ou une capture.

## La ronde Tests (Bug, Interface, Fonctionnalité)

1. **Le point d'entrée** : le plus haut possible (l'écran, la commande, l'API), un seul si on peut.
2. **Le modèle** : quel test existant du dépôt sert de modèle ? Cite son chemin.
3. **L'attendu** : chaque test dit une capacité. Son attendu est écrit en dur et tiré de la spécification, jamais
   recalculé comme le code le calcule.

## Bug

1. **La référence** : quelle spécification, quel standard de l'app, quelle version précédente dit le bon
   comportement ? Sans référence, ce n'est pas un bug.
2. **La reproduction** : les étapes, l'appareil, le thème, la version. Le défaut revient-il à chaque fois ?
3. **L'attendu** : exactement ce que dit la référence.
4. **La cause** : le fichier et la ligne, si on les connaît. Sinon, un Diagnostic d'abord ?
5. **Le test** : quel fichier, quel nom exact, et pourquoi échoue-t-il aujourd'hui ?

## Interface

1. **La maquette** : existe-t-elle, sur la vraie forme des composants existants, et est-elle validée ? Sinon, on la fait
   d'abord, et l'issue attend.
2. **L'inventaire** : chaque endroit touché, écran par écran et état par état (vide, chargement, erreur, texte très long).
3. **Les règles chiffrées** : tailles, jetons de couleur, largeurs de 390 et 1440 px, thèmes clair et sombre, une ligne
   ou plusieurs, coupe d'un texte trop long.
4. **La mesure** : quel test de bout en bout vérifie chaque règle (hauteur, largeur, débordement, couleur, contraste) ?
5. **Ce qui reste identique** : composants, liens, traductions, noms accessibles.
6. **Les captures** : lesquelles faut-il refaire ?

## Fonctionnalité

1. **Le comportement** : les entrées, les sorties, les cas limites, les erreurs.
2. **Le contrat** : formats de données, API, schémas, compatibilité avec l'existant. Pour une interface nouvelle, trois
   sous-agents en proposent chacun une, radicalement différente. Compare-les par profondeur (ce que l'interface cache),
   localité (ce qu'un changement touche) et place de la couture (où un test se branche), puis le propriétaire tranche
   en QCM.
3. **Les données réelles** : volumes, valeurs extrêmes, valeurs absentes.
4. **Les tests** : lequel échoue avant le changement, lesquels couvrent les cas limites ?

## Diagnostic

1. **Le symptôme** : les messages d'erreur exacts, copiés tels quels.
2. **Depuis quand** : la version, la date ou le commit où c'est apparu.
3. **Les pistes écartées** : ce qui a déjà été vérifié, et pourquoi ce n'est pas la cause.
4. **Le livrable** : la cause localisée et un test rouge qui reproduit le problème, sans correctif. Le correctif fera
   l'objet d'une issue Bug.

## Tests

1. **La zone non couverte** : quels fichiers, fonctions ou parcours, et quel risque ?
2. **Les sabotages** : quels défauts les nouveaux tests doivent-ils attraper ? La gate rejoue chacun.
3. **Le projet** : la gate sait-elle rejouer les sabotages de ce projet ? Sur factory-live, pas encore : la carte serait
   bloquée.

## Maintenance

1. **L'objectif** : ce que la maintenance apporte.
2. **Le périmètre** : les fichiers, dépendances ou workflows touchés.
3. **L'invariant** : aucun test existant modifié ni retiré. S'il faut en changer un, ce n'est pas une maintenance.
4. **La vérification** : qu'est-ce qui prouve que rien n'a changé ?

## Documentation

1. **Les documents** : quels fichiers ou pages ?
2. **Le lecteur** : pour qui, et que doit-il savoir faire après sa lecture ?
3. **Le contenu** : ce que chaque section doit dire.
4. **Le périmètre** : seuls des documents changent ; un changement de code est une autre issue.
