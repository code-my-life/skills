---
name: prototype-logique
description: Valider une règle, une machine à états ou un modèle de données avec une page HTML unique que le propriétaire peut manipuler, publiée en artifact privé, avant d'écrire l'issue. À lancer à la main.
disable-model-invocation: true
---

# Prototype de logique

Un prototype est un **code jetable qui répond à une question**. Ici la question porte sur une **règle** : une machine à
états, un cycle de vie (celui d'une carte release, par exemple), une forme de données. Elle paraît juste sur le papier
et ne sonne faux qu'une fois poussée dans des cas réels.

Le résultat est une page HTML unique, sans rien à installer, que le propriétaire clique pour sentir la règle, et qui
est publiée en **artifact privé** pour valider la règle **avant** l'issue. Cette skill vient de la branche « logique » de
`prototype` de mattpocock/skills (MIT). Une question d'**apparence** relève de la skill `prototype`, pas de celle-ci.

## Quand c'est la bonne forme

- « Cette machine à états gère-t-elle le cas où X puis Y ? »
- « Ce modèle de données permet-il de représenter... ? »
- « Je veux sentir à quoi ressemble la règle avant de la coder. »
- Tout ce qu'on comprend mieux en **appuyant sur des boutons et en regardant l'état changer**.

## Règles

1. **Jetable dès le premier jour.** Rien n'entre dans le code du dépôt. La page est marquée « PROTOTYPE » en tête.
2. **Aucune persistance.** L'état vit en mémoire.
3. **Pas de finition.** Ni test, ni gestion d'erreur au-delà de ce qui fait tourner la page, ni abstraction.
4. **Montrer l'état.** Après chaque action, l'état utile s'affiche en entier.
5. **Une page, sans framework.** Du HTML, du CSS et du JavaScript simples, tout en ligne, sans bibliothèque ni serveur.

## Étapes

### 1. Poser la question

Avant d'écrire, écris le modèle d'état et la question en un paragraphe, en tête de la page (visible, pas en commentaire).
Un prototype qui répond à la mauvaise question est du temps perdu, et la question écrite se vérifie plus tard.

Cherche toi-même dans le dépôt la règle telle qu'elle est écrite aujourd'hui (le code, l'ADR, le `factory.yaml`) : les
états et les transitions viennent de là, pas de ta mémoire.

### 2. Isoler la logique dans un module pur

Mets la logique (ce qui répond à la question) dans un seul bloc `<script>`, écrit comme un petit module **pur** qui
pourrait être sorti et déposé dans le vrai code. La page autour est jetable, ce module non.

La forme dépend de la question :
- **un réducteur pur** : `(état, action) => état`. Bon quand les actions sont des événements discrets et l'état une
  valeur unique ;
- **une machine à états** : états et transitions explicites. Bon quand « quelles actions sont permises maintenant » fait
  partie de la question ;
- **un petit jeu de fonctions pures** sur un type de données simple ;
- **une classe** quand la logique possède vraiment un état interne durable.

Choisis la forme qui sert la question, pas celle qui se branche le plus facilement à une page. Garde-le pur : pas de DOM,
pas de `document`, pas de gestionnaire de bouton qui atteint l'intérieur. La page appelle le module, jamais l'inverse.

### 3. Construire la page

Une page, HTML/CSS/JS simples. Écris-la pour quelqu'un qui n'est pas développeur : chaque libellé est dans la **langue
du métier**, pas celle du code. Le propriétaire voit « carte en revue », pas `STATE_REVIEW`.

Du haut vers le bas :
1. **Le titre et une ligne** qui dit ce que la page permet d'explorer (la question).
2. **L'état courant**, en entier, dans un panneau lisible (des champs nommés, pas un JSON brut), redessiné après chaque
   clic. Signale ce qui vient de changer.
3. **Les boutons libres** : un par action, toujours disponibles, pour pousser le modèle dans n'importe quel ordre. Une
   action interdite dans l'état courant se montre grisée, avec la raison.
4. **Des scénarios**, un par **onglet**. Chaque onglet porte une courte description (la situation et ce qu'il faut
   regarder), puis les **boutons à presser** dans l'ordre. Chaque étape est un vrai bouton : le clic fait l'action et
   passe à la suivante. Lancer un scénario remet l'état à un point connu.

Choisis des scénarios qui montrent les cas difficiles à raisonner sur le papier : le chemin heureux, un cas limite
retors, une tentative de faire ce qui doit être interdit.

Reste sobre : une typographie nette, de l'air, une seule couleur d'accent. Pas d'animation.

### 4. Publier en artifact privé

Charge la skill `artifact-design`, puis publie la page avec l'outil Artifact, **en privé** (c'est son état par
défaut). Ne partage rien : le propriétaire décide seul de transmettre le lien. Donne-lui le lien et la question, et
regarde avec lui : les moments utiles sont « attends, ça ne devrait pas être possible » et « tiens, je pensais que X
serait autre ». Ce sont les bugs de l'**idée**, tout l'objet du prototype. S'il veut une action ou un scénario de plus,
ajoute-les : un prototype évolue.

### 5. Garder la réponse

Une fois la question tranchée :
- le **verdict** et la question qu'il règle vont dans l'issue (dans « Constat » ou « Contexte »), avec le lien de
  l'artifact ;
- le module pur validé se lève dans le vrai code, par l'issue, pas ici.

L'artifact garde la page. Aucune branche Git jetable : ni la skill, ni la factory n'en tiennent.

## À éviter

- **Pas de test.** Un prototype qui en demande n'est plus un prototype.
- **Pas de lien avec la vraie base ni avec GitHub.** L'état est en mémoire.
- **Ne généralise pas.** Pas de « et si on voulait gérer X plus tard ». Une seule question.
- **Ne mélange pas la logique et la page.** Un module pur qui touche le DOM n'est plus déposable.
- **Pas de framework, de bundler ni de serveur.**
- **Ne livre pas la page en production.** Elle est faite pour être cliquée. Le module derrière vaut seul d'être gardé.

---

Adaptée de `prototype` (branche « logique », `LOGIC.md`) de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
