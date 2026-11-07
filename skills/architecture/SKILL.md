---
name: architecture
description: Parcourir un dépôt pour trouver des occasions d'approfondir ses modules (là où l'architecture freine les agents), les présenter en rapport visuel privé, puis creuser celle que le propriétaire choisit. Lancée par le propriétaire seul.
disable-model-invocation: true
---

# Architecture à la demande

Faire apparaître les frictions d'architecture et proposer des **occasions d'approfondir** : des refontes qui changent
des modules **peu profonds** en modules **profonds**. Le but est que le dépôt se teste et se parcoure mieux, pour les
agents comme pour le propriétaire. Cette skill vient de `improve-codebase-architecture` et `codebase-design` de
mattpocock/skills (MIT).

Le propriétaire la lance **seul**, quand il a un moment : jamais à la fin d'une carte, jamais par un agent.

Elle parle un vocabulaire fixe, dans [references/vocabulaire.md](references/vocabulaire.md) : **module**, **interface**,
**implémentation**, **profondeur**, **couture**, **adaptateur**, **levier**, **localité**. Lis-le d'abord, et emploie
ces mots tels quels dans chaque proposition : ne glisse pas vers « composant », « service », « API » ou « frontière ».
Les ADR (`docs/decisions/`) disent ce qui est déjà tranché : n'y reviens pas à la légère.

## Étapes

### 1. Explorer

**Cadre avant de scanner.** Approfondir un module paie en rendant les changements futurs plus faciles : pèse davantage
ce qui change souvent. Décide où regarder avant de regarder.

- Si le propriétaire nomme une direction (un module, un sous-système, une gêne), prends-la.
- Sinon, remonte `git log --oneline` sur une bonne durée pour trouver les **points chauds** : les fichiers et zones qui
  reviennent sans cesse. Qu'ils attirent ton attention d'abord. Si les changements sont éparpillés sans point chaud,
  élargis.

Lis les ADR de la zone, puis lance un sous-agent avec un contexte vierge pour parcourir le code (dis-lui de ne lancer
ni skill ni agent). Il explore sans règle rigide, et note où il sent de la friction :
- Où comprendre une idée oblige-t-il à rebondir entre beaucoup de petits modules ?
- Où des modules sont-ils **peu profonds**, avec une interface presque aussi complexe que l'implémentation ?
- Où des fonctions pures ont-elles été extraites pour le test seul, alors que les vrais bugs se cachent dans leur
  appel (pas de **localité**) ?
- Où des modules très couplés fuient-ils à travers leurs coutures ?
- Quelles parties ne sont pas testées, ou sont difficiles à tester par leur interface actuelle ?

Applique le **test de suppression** à tout ce que tu soupçonnes peu profond : supprimer ce module concentrerait-il la
complexité, ou la déplacerait-il seulement ? « Elle se concentre » est le signal cherché.

### 2. Présenter les candidats en rapport visuel, en artifact privé

Charge la skill `artifact-design`, écris le rapport en une page HTML et publie-le en **artifact privé** avec l'outil
Artifact, au lieu d'un fichier dans `/tmp`. Donne le lien au propriétaire. Le contenu du rapport est dans
[references/rapport.md](references/rapport.md).

Ne propose **pas** encore d'interfaces. Une fois le rapport publié, demande en QCM (outil AskUserQuestion) lequel des
candidats explorer.

Un candidat qui contredit une ADR n'est montré que si la friction est assez réelle pour rouvrir l'ADR : marque-le
clairement (« contredit l'ADR 0007, mais vaut la peine d'être rouvert parce que... »). Ne liste pas chaque refonte
théorique qu'une ADR interdit.

### 3. Creuser le candidat choisi

Une fois que le propriétaire choisit, parcours avec lui l'arbre des décisions, en QCM : les contraintes, les
dépendances (voir [references/approfondir.md](references/approfondir.md)), la forme du module approfondi, ce qui se
trouve derrière la couture, les tests qui survivent. Pose les questions d'une ronde ensemble ; celles qui dépendent
d'une réponse encore ouverte attendent la ronde suivante. Les faits sont à toi (cherche-les dans le code), les
décisions au propriétaire.

S'il veut comparer plusieurs interfaces pour le module approfondi, applique
[references/concevoir-deux-fois.md](references/concevoir-deux-fois.md).

S'il écarte un candidat pour une raison qui compte, propose de l'écrire dans une ADR, pour que les revues futures ne le
reproposent pas. Seulement quand la raison servirait vraiment à un futur explorateur : pas pour « pas le moment » ni pour
l'évident.

### 4. Ce qui devient une issue

Un candidat **retenu** devient une issue **Maintenance** (refonte sans changement de comportement), rédigée avec
`factory-issue`. Rien n'est créé sans le GO du propriétaire.

---

Adaptée de `improve-codebase-architecture` et `codebase-design` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
