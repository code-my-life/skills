# Fins de phase

Une **phase** est un morceau de travail dans une séance : le gril, l'implémentation, la recette. La définition est floue
exprès : une phase finit quand on pense « bon, c'est fait ».

La **frontière de phase** est l'écart entre deux phases, et le seul endroit où cette décision se prend. Au milieu d'une
phase, il n'y a rien à décider : on continue, ou on confie le reste à des sous-agents. Compacter au milieu d'une phase
fait perdre le fil à l'agent.

## Les cinq options

| Option | Ce qu'elle fait |
|---|---|
| **Continuer** | Rester dans la séance. Aucun changement de contexte. |
| **Vider** (`/clear`) | Vider la fenêtre et repartir de rien. |
| **Sous-agent** | Envoyer la tâche à sa propre fenêtre et recevoir un rapport. |
| **Compacter** (`/compact`) | Résumer ce contexte et repartir d'un résumé. |
| **Passer la main** | Écrire un fichier Markdown portable et amorcer une séance ailleurs avec lui. |

## L'arbre

On descend l'arbre à la frontière. Le premier **oui** l'emporte.

**1. Peut-on continuer dans cette séance ?** Deux choses font répondre oui : la phase suivante a besoin de celle-ci comme
**source primaire**, ou il reste assez de place dans la « zone intelligente » (environ 150 000 jetons) pour que la
phase suivante y tienne. Du gril à l'implémentation, c'est le oui classique : l'implémentation veut le raisonnement mot
pour mot, pas un résumé. Continuer ne coûte rien et ne perd rien : on l'écarte avant tout le reste.

**2. Le contexte est-il sans intérêt pour la suite ?** Tout ce qu'il y a ici (l'exploration, les décisions, les
impasses) est-il jetable ? Alors **vider**. C'est le geste le moins cher : il ne prend aucun temps et rend toute la
fenêtre. Vider n'est pas non plus définitif : l'ancienne séance se reprend.

Se tromper coûte à sens unique. Vider un contexte **utile**, c'est perdre le **pourquoi** de ce qu'on a construit, et
relire le diff ne le rend pas.

**3. Faut-il passer la main ?** Seulement pour :
- changer d'**harnais** (Claude Code vers OpenCode ou Codex) ;
- aller dans un autre **dossier** ou un autre dépôt ;
- envoyer le travail à un **collègue** ;
- ou détacher une tâche annexe trouvée **en cours de phase** sans dérailler.

C'est toute la liste. Ce que la main passée achète, c'est la **portabilité** : un fichier qui voyage. Si rien ne
voyage, on n'en a pas besoin. Il n'y a pas de skill pour cela ici : écris le fichier toi-même (la question, ce qui est
décidé, les liens vers les sources, la suite).

**4. La tâche peut-elle tourner sans toi ?** Est-elle assez bornée pour tourner pendant que le propriétaire est parti,
sans consigne en route ? Alors **sous-agent**, et cette séance reste intacte. La relecture automatique en est le cas
classique : l'agent lit le diff et rend compte. Un sous-agent démarre avec un contexte vierge (certains harnais copient
la conversation du parent : dis-le dans sa consigne).

**5. Sinon, `/compact`.** Contexte utile, même harnais, même dossier, et le propriétaire doit rester dans la boucle :
l'arbre arrive souvent ici. Donne-lui une consigne (`/compact on va recetter cette zone`) pour que le résumé garde ce
que la suite demande.

`/compact` est le **choix par défaut, pas le premier réflexe**. Il est en bas parce que les quatre questions du dessus
sont moins chères ou plus précises. Quand on commence par lui, la nouvelle séance est sûre d'elle et fausse sur une
décision que le résumé a aplatie.

## Sources primaires et secondaires

Chaque option sauf **continuer** change une **source primaire** en **source secondaire** : la séance telle qu'elle s'est
passée, remplacée par son résumé. Le marché a toujours la même forme :

| Source | Information | Bruit | Marge de manœuvre |
|---|---|---|---|
| Primaire (continuer) | Complète | Beaucoup | Peu |
| Secondaire (compacter, passer la main) | Perdue en partie | Moins | Beaucoup |

C'est pourquoi la question 1 vient en premier : on ne paie la perte que lorsque rester coûte plus qu'il ne rapporte.

## Ce sont des jugements

Les questions ne sont pas objectives : chacune a du goût dedans, et la même frontière peut aller dans deux sens deux jours
différents. La valeur est de les poser **dans l'ordre**, à la frontière plutôt qu'au milieu du travail.

---

Adaptée de `PHASE-BOUNDARIES.md` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
