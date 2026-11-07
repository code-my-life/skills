---
name: controle-memoire
description: Contrôler la mémoire de Claude Code (MEMORY.md et ses fichiers) : contradictions, pages orphelines, faits dépassés. Les corrections se tranchent en QCM. À lancer à la main.
disable-model-invocation: true
---

# Contrôle de la mémoire

La mémoire de Claude Code (`MEMORY.md` et les fichiers qu'il indexe, dans `~/.claude/projects/<projet>/memory/`)
s'enrichit à chaque séance et ne se relit jamais. Cette skill la passe au crible, comme l'opération « lint » de
`chief-of-staff` de mattpocock/skills (MIT) passe un wiki.

Elle ne corrige rien seule : elle propose, le propriétaire tranche.

## Ce qu'on cherche

1. **Les contradictions** : deux fichiers qui disent le contraire (une règle et son exception oubliée, deux versions
   d'une même décision).
2. **Les pages orphelines** : un fichier que `MEMORY.md` n'indexe pas, ou une ligne d'index dont le fichier n'existe
   plus.
3. **Les faits dépassés** : un fait que le code, une ADR ou une issue plus récente a remplacé.
4. **Les doublons** : deux fichiers pour une même idée, à fusionner.

## Chaque fait est daté

Un fait de mémoire est un fait **daté** : « le 2026-11-06, le propriétaire a décidé que... ». Pour un fait sur du code,
le commit ou la version où il était vrai. Jamais « actuellement » ni « est » sans date.

Quand un fait change, on ne réécrit pas l'ancien : on ajoute le nouveau, daté, et on marque l'ancien **remplacé**.
Un fait sans date est lui-même une trouvaille : propose de le dater, avec la date de création du fichier si elle est
tout ce qu'on sait, et dis que la date est approximative.

## Étapes

1. **Lire** `MEMORY.md`, puis chaque fichier qu'il indexe. Liste aussi les fichiers du dossier que l'index ne cite pas.
2. **Vérifier les faits vérifiables** contre leur source : une ADR (`docs/decisions/`), le code, une issue
   (`gh issue view`), le catalogue des skills. Un fait que tu ne peux pas vérifier n'est pas déclaré faux : il est
   marqué « non vérifié ».
3. **Dresser la liste des corrections**, par type (contradiction, orpheline, dépassé, doublon), chacune avec les
   fichiers et les lignes en cause et la correction proposée.
4. **Trancher en QCM** (outil AskUserQuestion) : pour chaque correction, « l'appliquer » ou « la laisser », ta
   recommandation en premier avec « (recommandé) », 4 questions au plus par appel.
5. **Appliquer** les seules corrections validées, puis relire l'index : chaque fichier y figure, chaque ligne mène à un
   fichier.

## Limites

- Tu ne supprimes aucun fichier sans accord explicite, même orphelin.
- Tu n'inventes pas une date.
- Tu ne touches ni aux skills, ni aux règles (`~/.claude/rules/`), ni au code : seule la mémoire est dans le périmètre.

## Tâche planifiée

Le contrôle ne se programme pas de lui-même. Si le propriétaire demande un passage régulier, propose une tâche
planifiée (skill `schedule`) qui lance ce contrôle et ne fait que **lister** les corrections : sans personne pour
trancher, rien ne s'applique, et le bilan du passage porte la liste.

---

Adaptée du « lint » de `chief-of-staff` de mattpocock/skills (MIT, Matt Pocock), commit 4ae2317.
