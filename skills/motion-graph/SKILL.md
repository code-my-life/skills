---
name: motion-graph
description: "Graphe animé d'une interface React (ligne d'usine, pipeline, flux, carte de dépendances) : boîtes reliées par des courbes, une carte qui voyage sur les liens, des comètes de données, zoom au doigt, avec Motion et Primer. Règles validées par le propriétaire sur la ligne de factory-live (ADR 0010), techniques, pièges et contrôles avant PR. Use when building or changing an animated graph, flow, pipeline or node-and-edge view, connectors with moving data, or a zoomable canvas in a React app."
version: 0.1.2
author: Clément Devillez (code-my-life) + Claude Code
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [factory, motion, react, primer, graph, animation]
    category: software-development
---

# motion-graph

Un graphe se lit d'un coup d'œil ou ne sert à rien. Cette skill reprend ce qui a été validé sur la ligne
d'usine de factory-live (maquette v5, issue factory-live#18, PR #19, ADR 0010 de factory-live) : l'exemple
complet est dans `apps/web/src/features/line/graph/` de factory-live. Pour l'API de Motion elle-même, la skill
`motion` du kit officiel (installée à côté) fait foi.

## 1. Avant le code

- **Maquette d'abord**, publiée et validée, sur la vraie forme des composants de l'app. Rien n'entre dans le
  code qui n'ait été vu par le propriétaire.
- Les données d'un nœud se déduisent des faits (règles pures du domaine, testées), jamais d'une mémoire de
  l'interface. Une animation montre un changement de faits ; elle n'en invente pas.

## 2. Règles de rendu (validées, à ne pas rediscuter)

- **Courbes**, jamais d'angle droit : Bézier cubiques ; un long trajet fait des quarts de tour arrondis.
- **Un port par lien**, rond aux deux bouts (pas de flèche en triangle), posé sur le bord de la boîte.
  Un éventail (plusieurs liens d'une même boîte) a ses ports espacés et ses courbes ne se croisent pas.
- **Liens et ports au-dessus des boîtes**, cadres de groupe compris : plans boîtes 1, liens et comètes 2,
  ports 3, carte qui voyage 4. On voit chaque lien entrer dans sa boîte.
- **Au repos, un lien pâlit sans disparaître** (opacité 0,42). Seul un lien en activité s'anime : il se
  redessine par-dessus, plein.
- **Le rouge est réservé aux problèmes.** Un retour (gate rouge, revert) est neutre au repos, rouge seulement
  quand une issue le prend après un échec, jaune après une demande.
- **Aucun texte sur un lien** ; une entrée de légende par sorte de lien (couleur, tirets), légende repliée à
  l'ouverture, ouverte par un bouton.
- **À l'ouverture, le graphe entier tient dans la fenêtre** ; les boutons de zoom sont sous le graphe, jamais
  dessus.
- **Une couleur par branche**, tirée de la palette « display » de Primer, vérifiée pour le daltonisme entre
  branches voisines (validateur de la skill dataviz), posée en style depuis une table TypeScript, comme les
  teintes des badges. Jamais de règle stylelint désactivée pour passer.

## 3. Disposition : une géométrie pure

- Un module sans React (`layout.ts`) place les boîtes et trace les liens à partir des seules hauteurs de
  contenu ; il rend `{ boxes, edges, width, height }`. Chaque lien a un `id` stable, sa branche, son `d` et
  ses deux ports.
- Les tests de ce module tiennent les règles du §2 : deux ports par lien et aucun partagé, aucun croisement
  dans un éventail (échantillonner les courbes), aucune boîte sur une autre, quel que soit le remplissage.
- **Cibles tactiles** : au plus petit zoom (`MIN_SCALE`), deux lignes qui se suivent restent à 24 px l'une
  de l'autre (WCAG 2.5.8, vérifié par axe). Hauteur d'une ligne ≥ 24 / `MIN_SCALE`. Une liste compacte ne
  montre qu'une ligne. Les contrôles du panneau font 44 px sur écran tactile.

## 4. Mouvement avec Motion (`motion/react`)

- **La carte qui voyage** : un `motion.div` avec `style={{ offsetPath: 'path("…")' }}` et
  `animate={{ offsetDistance: '100%' }}` ; durée selon la longueur du trajet, à vitesse constante (0,9 à
  2,6 s sur factory-live), courbe en S. Les liens successifs se raccordent en remplaçant le `M` du suivant
  par un `L`. La ligne de l'issue n'apparaît dans sa boîte qu'à l'arrivée (`onAnimationComplete`) : aucune
  information ne tient au seul mouvement.
- **Un flux ne coule que pendant un vrai échange** : des points montent d'un fournisseur pendant que son modèle
  répond (l'agent réfléchit, ou sa lane CLI travaille), pas pendant qu'un outil tourne ; la ligne dit alors l'outil.
- **Les comètes** : une horloge à soi (`useAnimationFrame` qui n'avance que si le mouvement est permis),
  puis `useTransform` pour l'`offsetDistance` de chaque comète (phase décalée). Pause et
  `prefers-reduced-motion` figent l'horloge ; chaque boucle porte `data-loop`.
- **Un lien qui s'active** se dessine par `pathLength` de 0 à 1 ; un lien en tirets apparaît en fondu
  (`pathLength` casserait ses tirets). Opacité coupée à 0,01 s au départ, sinon le bout rond fait un point.
- **Une ligne qui part** : `AnimatePresence mode="popLayout"` ; elle reste dans le DOM pendant sa sortie
  (tests : attendre sa disparition).
- **Le zoom** : une `MotionValue` d'échelle, la taille du conteneur par `useTransform`, `animate()` en ressort
  sans rebond pour les boutons (instantané si `useReducedMotion`) ; le point sous les doigts reste en place.
  Deux doigts : `touchmove` non passif, `preventDefault` seulement à deux doigts ; un doigt défile nativement
  (`touch-action: pan-x pan-y`) ; Ctrl ou ⌘ et la molette sur ordinateur.
- Jamais de SMIL (`<animateMotion>`) : fil principal, et le bouton de pause n'y peut rien. N'animer que
  `transform`, `opacity`, `offset-distance`, `pathLength`.

## 5. Pièges connus

- **Compilateur React** (`eslint-plugin-react-hooks`) :
  - pas de `setState` dans un effet pour suivre une prop : garder la valeur précédente en état et comparer
    pendant le rendu ;
  - ne pas lire `ref.current` pendant le rendu ;
  - ne pas modifier une valeur rendue par un hook : une écriture dans le DOM (défilement) va dans le hook
    qui détient la ref (`reveal()` du zoom) ;
  - un objet rendu par un hook dont un champ passe à `ref=` devient une ref : le déstructurer.
- **Stylelint de Primer** :
  - pas de taille de texte sans jeton (13 px n'existe pas : 12 ou 14) ;
  - pas d'ombre portée brute : un anneau se fait en `outline` ;
  - pas de rayon calculé avec une épaisseur de bordure.
- **jsdom** : ni `ResizeObserver`, ni `popover` (infobulles de Primer), ni `scrollTo` (écrire `scrollLeft`) ;
  les CSS modules n'y calculent rien : vérifier les opacités et les plans en e2e.
- **Trajets** : un trajet ne garde que les liens que le graphe dessine, et n'existe que s'il en reste un. Sinon
  (un recul sans lien, une revue approuvée puis contestée), la ligne attendrait une carte qui ne part jamais.
- **Noms** : un lien de flux porte le nom de la boîte qu'il alimente (`models:<poste>`), jamais une abréviation :
  sinon il ne s'allume jamais, sans erreur.
- **Zoom d'ouverture** : il se refait quand la taille du contenu change (premier état reçu en direct), tant que
  personne n'a zoomé.
- **État** : une icône d'état masquée aux lecteurs d'écran doit être doublée d'un texte caché quand aucun texte
  visible ne dit l'état.
- **Données gardées** : un état gardé sur l'appareil par une version antérieure se complète des champs nouveaux
  avant d'être lu.
- Les mesures dans un graphe zoomé sont à l'échelle : un badge de 20 px y mesure 20 × l'échelle. Mesurer
  dans le repère du canevas, ou hors du graphe.

## 6. Preuves avant la PR

1. Tests unitaires : la géométrie (§3), la recherche et les filtres, la légende, le trajet et la pause (une
   carte voyage, rien en pause).
2. E2E (bureau 1440 × 900 et iPhone 390 × 844) :
   - plans mesurés par `z-index` ;
   - opacité 0,42 au repos et aucun lien rouge ;
   - comètes seulement sur les liens actifs ;
   - le graphe entier dans la fenêtre à l'ouverture ;
   - pincer à deux doigts (CDP), puis défiler d'un doigt ;
   - aucune boîte qui déborde, aucun défilement horizontal ;
   - axe sans violation ;
   - les e2e de l'app branchée aussi (projet « live ») : son faux serveur porte chaque champ que le contrat ajoute,
     sinon la page plante au snapshot suivant, et seulement en CI.
3. Regarder le rendu soi-même à 1440 et 390 px, recadrer chaque boîte : CI, gate et revues ne voient pas une
   ligne coupée d'un pixel.
4. Captures de référence refaites dans l'image de Playwright du dépôt, avec `--update-snapshots=all` (un texte
   changé reste sous le seuil de 1 % et garderait l'ancienne image), relues avant le commit.
5. Dans la PR, chaque écart à la maquette, avec le contrôle qui l'impose.
