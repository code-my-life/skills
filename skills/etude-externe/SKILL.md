---
name: etude-externe
description: Étudier un outil, une méthode ou un dépôt externe contre ses sources primaires, rendre un verdict par projet (ce qui sert, ce qui ne sert pas, ce qui pose problème) et le garder dans docs/etudes/. À lancer à la main.
disable-model-invocation: true
---

# Étude d'un outil externe

Avant d'adopter un outil externe (Graphify, ICM, Impeccable, Motion, mattpocock/skills...), on lit : sa doc, ses
conventions et le code de ses scripts. On ne reprend rien sur la foi d'un article. Cette skill vient de `research` de
mattpocock/skills (MIT) : un sous-agent en arrière-plan fait la lecture pendant que tu continues.

## Étapes

1. **Cadrer.** Écris la question en une phrase, et la liste des projets de code-my-life qui pourraient s'en servir.
   Si elle n'est pas claire, demande-la en QCM (outil AskUserQuestion).
2. **Lire en arrière-plan.** Lance un sous-agent en arrière-plan, avec un contexte vierge (il ne reçoit que ta
   consigne, pas la conversation). Dis-lui de ne lancer ni skill ni agent. Tu gardes la main pendant qu'il lit.
3. **Trancher par projet**, en QCM.
4. **Écrire l'issue** et garder l'étude.

## 2. La consigne du sous-agent

Il lit les **sources primaires** : la doc officielle, les conventions du dépôt, le code des scripts, les specs, les API
du fournisseur. Pas un article qui les résume. Il suit chaque affirmation jusqu'à la source qui la porte.

Il lit en particulier :
- **la doc** : ce que l'outil promet ;
- **les conventions** : comment ses auteurs veulent qu'on s'en serve ;
- **le code de ses scripts** : ce qu'ils vérifient vraiment, et leurs limites (ce qu'ils laissent passer, ce qui les
  désactive, ce qu'ils supposent de l'environnement).

Il écrit un seul fichier Markdown :
- **chaque affirmation est citée** : le fichier et la ligne, ou l'URL et le commit ou la version, lue le jour de
  l'étude (date en tête) ;
- un fait lu et une déduction se distinguent ;
- ce qu'il n'a pas pu lire est dit, pas deviné ;
- il se termine par un verdict par projet (voir plus bas), en citant ses preuves.

Il écrit dans `docs/etudes/<sujet>.md` du dépôt qui porte la décision (la factory en général), sans toucher au reste.
Un dépôt externe se lit dans le scratchpad de la séance, jamais cloné dans un dépôt de code-my-life.

## 3. Le verdict par projet

Pour chaque projet de code-my-life concerné, trois colonnes :

| Projet | Ce qui sert | Ce qui ne sert pas | Ce qui pose problème |
|---|---|---|---|

Ce qui **pose problème** est le plus utile : un conflit avec une règle de la factory (un hook réécrit, un déclenchement
qui part dans les lanes, une licence, une mise à jour automatique). Cite la règle contredite.

Présente le verdict au propriétaire, puis pose chaque décision en QCM (outil AskUserQuestion) : ta recommandation en
premier avec « (recommandé) », 4 questions au plus par appel. Il peut répondre hors des options.

## 4. L'issue et l'étude gardée

Ce qui est retenu aboutit à une issue (rédigée avec `factory-issue`) dont le corps contient un tableau
**Pris / Laissé / Adapté** : pour chaque élément de l'outil, ce qu'on prend tel quel, ce qu'on laisse (avec la raison)
et ce qu'on adapte (avec comment). L'issue cite l'étude.

L'étude reste dans `docs/etudes/`, avec sa date et le commit ou la version étudiés : elle évite de refaire la lecture, et
elle dit à quel état de l'outil elle est vraie. Une étude ne se réécrit pas : une relecture ultérieure s'ajoute, datée.

Ne crée rien sur GitHub sans le GO du propriétaire.

---

Adaptée de `research` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
