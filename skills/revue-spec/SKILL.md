---
name: revue-spec
description: Avant d'approuver une PR de la factory, relire son diff contre l'issue d'origine : critères manquants ou partiels, ce qui n'était pas demandé, ce qui semble fait mais faux. Une passe, sans poster. À lancer à la main.
disable-model-invocation: true
---

# Revue de la PR contre l'issue

Une PR peut faire tout ce que l'issue demande et casser les conventions, ou suivre toutes les conventions et faire autre
chose. La gate juge les conventions : ce sont des contrôles. Cette skill juge l'**autre axe**, celui de l'**issue** :
le diff fait-il ce qui était demandé ? Elle vient de l'axe « Spec » de `code-review` de mattpocock/skills (MIT).

Le propriétaire la lance **à la main**, avant d'approuver une PR de la factory. Elle n'est **jamais une barrière** et ne
**poste rien sur la PR** : le rapport reste dans la séance.

## Étapes

### 1. Fixer ce qu'on relit

- La PR (numéro et dépôt) : `gh pr view <n> -R <dépôt>` (titre, corps, base, tête) et
  `gh pr diff <n> -R <dépôt>`. Si le diff est vide, ou si la PR n'existe pas, arrête-toi ici.
- L'issue d'origine : la ligne `Fixes #<n>` du corps de la PR (l'issue est alors dans le dépôt de la PR) ou
  `Fixes <dépôt>#<n>`, ou, à défaut, une référence dans les commits.
  `gh issue view <n> -R <dépôt>`. Sans issue, dis « pas d'issue » et arrête-toi : il n'y a rien à comparer.

### 2. Un sous-agent à contexte vierge

Lance **un** sous-agent, avec un contexte vierge : il ne voit pas cette conversation, seulement ce que tu lui donnes
(le diff, le texte de l'issue, les consignes ci-dessous). Dis-lui explicitement de **ne lancer ni skill ni agent** : un
relecteur qui en lance d'autres a déjà produit plus de 50 agents dans un cas connu.

Sa consigne :

> Voici une issue et le diff d'une PR qui prétend la traiter. Rapporte :
> (a) les critères que l'issue demande et que le diff **ne traite pas, ou traite en partie** ;
> (b) ce que le diff fait et que l'issue **ne demandait pas** (hors périmètre) ;
> (c) ce qui **semble fait mais où l'implémentation paraît fausse**.
> Pour chaque point, **cite la ligne de l'issue** (copie-la mot pour mot, avec sa section). Les tests nommés par la section
> « Tests » de l'issue existent-ils, sous exactement ce nom ? Les critères d'acceptation sont-ils prouvés par un test, une
> commande ou une capture, ou seulement affirmés ? Moins de 400 mots, sans mise en forme inutile.

### 3. Rendre compte

Présente le rapport du sous-agent tel quel, **sans le reclasser ni le fusionner** avec un jugement de conventions : ce
n'est pas l'axe d'ici. Termine par une ligne : le nombre de points par rubrique (a, b, c) et le plus grave de chacune.

Vérifie toi-même les points les plus graves avant de les répéter (une citation qui n'est pas dans l'issue, un test qui
existe sous un autre nom). Un point que tu ne peux pas vérifier est dit « non vérifié ».

## Ce qu'on ne fait pas

- **Pas de boucle.** Une seule passe : rien ne garantit que des passes répétées convergent. Un défaut corrigé se
  relit à la main, ou se relance par une nouvelle demande du propriétaire.
- **Pas de standards, pas d'odeurs de code.** Le style, le nommage et la forme du code sont des contrôles de la gate et
  des conventions du dépôt.
- **Pas de commentaire sur la PR**, pas de revue GitHub, pas de statut.
- **Pas de correction** : tu rends un rapport.

---

Adaptée de `code-review` (axe « Spec ») de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317. Le nom `code-review` est
déjà celui d'une commande intégrée de Claude Code.
