---
name: factory-diagnostic
description: "Procédure de la carte Diagnostic : une boucle qui va au rouge sur le symptôme exact, la repro réduite, 3 à 5 hypothèses réfutables, une sonde par prédiction, puis un commentaire de carte (cause, reproduction, test rouge proposé, hypothèses). Lecture seule, sans correctif. Pour toute carte « diagnostic <repo>#<n> »."
version: 0.1.0
author: Clément Devillez (code-my-life) + Hermès Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [factory, diagnostic, debugging, kanban]
    category: software-development
---

# factory-diagnostic

Adaptée de `diagnosing-bugs` (mattpocock/skills, `skills/engineering/diagnosing-bugs`, commit `4ae2317`), licence MIT, copyright Matt Pocock : le texte de la licence est dans le `LICENSE` de ce dossier. Ce qui est repris : la boucle d'abord, la repro réduite, les hypothèses réfutables, les sondes étiquetées. Ce qui est laissé : le correctif, le nettoyage qui le suit, le script d'étapes humaines, la liste d'hypothèses montrée au propriétaire (la carte tourne seule).

Tu traites une carte « diagnostic <repo>#<n> » : une issue de type Diagnostic (ADR 0017), un problème dont la cause est inconnue. Tu **livres un constat**, jamais un correctif : l'issue Bug suivante le reprend tel quel. Pas de branche, pas de PR, pas de commit, rien n'est poussé. Tu ne marques pas la carte `done` avant d'avoir posté le constat.

## 0. Orientation

1. `kanban_show()`, puis lis tout le brief, jusqu'à la section de l'issue recopiée mot pour mot : elle fait foi (symptôme, « depuis quand », reproduction, pistes déjà écartées). Un brief sans cette section : `python3 ~/.hermes/scripts/factory-trusted-thread.py <issue>`.
2. Travaille dans le worktree de la carte (`cd $HERMES_KANBAN_WORKSPACE`), à la base indiquée par le brief, en **lecture seule** pour le code du dépôt : tu ne modifies aucun fichier suivi, hors les logs de sonde de la phase 4, retirés avant la fin.
3. `mkdir -p evidence && grep -qx 'evidence/' .git/info/exclude 2>/dev/null || echo 'evidence/' >> "$(git rev-parse --git-path info/exclude)"` : tout ce que tu écris (boucle, sorties, test rouge) vit sous `evidence/`, **jamais commité**.
4. Lis le glossaire (`GLOSSARY.md`) et les ADR de la zone, s'ils existent.

## Masquer les secrets

Tu montres des commandes, des sorties et des artefacts capturés. **Masque chaque secret avant de l'écrire**, dans `evidence/` comme dans le commentaire : `<REDACTED>` à sa place. Construis les boucles sur des variables d'environnement, pour que la clé reste dans l'environnement et pas dans ce que tu montres. Un artefact capturé porte des en-têtes d'authentification : ne cite que les lignes qui portent le signal. Une clé d'exemple d'Hermès arrive déjà masquée : ne la reconstruis pas. Si la sortie masquée ne suffit pas à diagnostiquer, c'est un blocage (section « Sans boucle possible »).

## Phase 1 : la boucle d'abord

**C'est le cœur de la skill.** Avec un signal passe/échec serré, qui devient rouge sur *ce* bug, tu trouveras la cause : hypothèses et sondes ne font que le consommer. Sans lui, relire le code ne sauve rien. Aucune théorie avant la boucle : si tu te surprends à lire du code pour bâtir une explication, arrête-toi.

Dépense un effort disproportionné ici. Voies, à peu près dans cet ordre :

1. un test qui échoue, à la couture qui atteint le bug (unitaire, intégration, e2e) ;
2. un script `curl` contre un serveur de dev ;
3. une commande CLI sur une entrée fixe, sa sortie comparée à une référence ;
4. un script de navigateur sans tête (`playwright-cli`) qui assert sur le DOM, la console, le réseau ;
5. le rejeu d'une trace capturée sur disque ;
6. un harnais jetable : un sous-ensemble minimal du système, dépendances simulées ;
7. une boucle de propriétés ou de fuzz, pour « parfois faux » ;
8. une bissection automatisée (`git bisect run`) quand le bug est apparu entre deux états connus (le « depuis quand » de l'issue) ;
9. une boucle différentielle : même entrée dans l'ancienne et la nouvelle version, sorties comparées.

Resserre-la : plus rapide (cache, périmètre réduit), plus nette (assertion sur le symptôme exact, pas « ne plante pas »), plus déterministe (heure figée, graine fixée, système de fichiers isolé, réseau gelé). Un bug non déterministe : le but est un **taux de reproduction plus haut** (100 passages, parallélisme, fenêtres de timing resserrées) ; 50 % se débogue, 1 % non.

**Fin de phase 1** : tu nommes **une commande**, déjà lancée au moins une fois (invocation et sortie masquée sauvegardées dans `evidence/01-boucle.txt`), qui est :

- capable de rouge : elle parcourt le vrai chemin du bug et assert le **symptôme exact de l'issue**, pas « tourne sans erreur » ;
- déterministe : même verdict à chaque passage (bug aléatoire : taux haut et mesuré) ;
- rapide : des secondes, pas des minutes ;
- lançable sans personne : aucune étape humaine.

Pas de commande rouge, pas de phase 2.

## Phase 2 : reproduire, puis réduire

Lance la boucle et regarde-la passer au rouge. Vérifie que :

- elle produit la défaillance **décrite par l'issue**, pas une autre qui lui ressemble (mauvais bug, mauvais constat) ;
- elle est reproductible sur plusieurs passages ;
- le symptôme exact (message, mauvaise sortie, durée) est capturé, masqué.

Puis **réduis** : coupe entrées, appelants, configuration, données et étapes **un à un**, boucle relancée après chaque coupe, et ne garde que ce qui est nécessaire au rouge. Fini quand retirer n'importe quel élément restant fait passer la boucle au vert. Ne passe pas à la suite sans avoir reproduit **et** réduit.

## Phase 3 : hypothèses

Écris **3 à 5 hypothèses classées** avant d'en tester une : une seule hypothèse ancre sur la première idée plausible. Chacune est réfutable et porte sa prédiction :

> Si <X> est la cause, alors <changer Y> fait disparaître le bug / <changer Z> l'aggrave.

Sans prédiction, c'est une impression : écarte-la ou affûte-la. Écarte d'emblée celles que la section « Pistes écartées » de l'issue a déjà réfutées, et dis-le. Personne à qui montrer la liste : tu la tranches seul, et elle part dans le constat.

## Phase 4 : une sonde par prédiction

Chaque sonde répond à une prédiction précise de la phase 3, **une variable à la fois**. Préfère un débogueur ou un REPL ; sinon des logs ciblés aux frontières qui départagent les hypothèses, jamais « tout journaliser puis grep ». **Étiquette chaque log** d'un préfixe unique, `[DEBUG-a4f2]` : le retrait tient en un grep. Un bug de performance : pas de logs, mais une mesure de référence puis une bissection.

Note chaque hypothèse **retenue** ou **écartée**, avec la sonde et ce qu'elle a montré, dans `evidence/02-hypotheses.md`.

## Le test rouge proposé

Écris le test rouge à la couture qui reproduit le **vrai motif** du bug, tel qu'il se produit à l'appel. Il vit dans `evidence/` (ex. `evidence/test-rouge/<fichier>`), **jamais dans l'arbre suivi ni commité** ; tu proposes seulement son fichier de destination et son nom exact. Lance-le : il doit **échouer**, pour la bonne raison (sortie masquée dans `evidence/03-test-rouge.txt`). Si tu as forcé le rouge en modifiant du code ou une donnée, un `diff` contre une copie intacte prouve que la modification a bien eu lieu.

Si **aucune couture correcte n'existe** (un test à la seule couture accessible serait trop superficiel : un appelant seul quand il en faut plusieurs, un unitaire qui ne rejoue pas la chaîne), **c'est un constat** : écris-le dans le commentaire, l'architecture empêche de verrouiller ce bug.

## Fin de carte : le constat

1. `git grep -n '\[DEBUG-'` ne trouve rien et `git status --short` est vide : tout log de sonde est retiré.
2. Poste **un seul** `kanban_comment`, au format de l'issue Bug (ses titres `### Cause` et `### Reproduction`, que l'issue Bug suivante recopie) :

```
### Cause
<fichier:ligne> : <en deux phrases, ce qui se passe et pourquoi>

### Reproduction
Commande : <la commande rouge, une ligne>
Sortie (secrets masqués) :
<les lignes qui portent le signal>

### Test rouge proposé
Fichier : <chemin de destination> (à créer | à compléter)
Nom : <nom exact du test>
Rouge constaté : <la ligne d'échec>
(ou : aucune couture correcte, avec ce qui l'empêche)

### Hypothèses
Retenue : <H> : sonde <laquelle>, résultat <lequel>
Écartées : <H> : <ce qui la réfute> (une ligne chacune)
```

3. Relis le commentaire avant de le poster : aucun secret (jeton, clé, en-tête d'authentification, cookie, URL signée), `<REDACTED>` partout où il en fallait un.
4. `kanban_complete` avec en `artifacts` les fichiers d'`evidence/`. Le test rouge reste sur disque : c'est l'implémenteur de l'issue Bug qui l'écrira dans le dépôt.

## Sans boucle possible

Si, malgré tout, tu ne peux pas construire de boucle, ou si la sortie masquée ne suffit pas : **ne fais pas d'hypothèse**. `kanban_comment` avec ce que tu as tenté (chaque boucle essayée et pourquoi elle n'est pas rouge), puis `kanban_block(kind="needs_input", reason="pas de boucle rouge sur <symptôme> : <ce qu'il faudrait : accès à l'environnement, artefact capturé masqué, ou sonde en production>")`.

## Interdits

- Corriger, même d'une ligne : le correctif est l'issue Bug suivante.
- Commiter, pousser, ouvrir une PR, modifier un fichier suivi autrement que par une sonde étiquetée retirée avant la fin.
- Une hypothèse avant la boucle rouge ; plusieurs variables changées à la fois.
- Un secret dans `evidence/` ou dans le commentaire.
