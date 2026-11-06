# skills

La base de connaissance de Code My Life : toutes les skills de ses agents, au format
[Agent Skills](https://agentskills.io/specification). On les lit ici, et chaque agent les installe depuis ce dépôt.
Le catalogue, la migration des skills et leur installation arrivent avec code-my-life/hermes-software-factory#37.

## Commandes

| Quoi | Commande |
|---|---|
| Installer | aucune : le dépôt ne contient que des documents |
| Tous les tests | `git diff --check origin/main...HEAD`, lancé par le hook `pre-push` de la factory |
| Un seul fichier de test | aucun pour l'instant : les tests du catalogue arrivent avec #37 |
| Types | aucun |
| Build | aucun |
| Démarrer | aucun |
| Bout en bout | aucun |

## Conventions

- Issues, branches et pull requests suivent les types de la software factory : un modèle d'issue de l'organisation par
  type, une branche `<préfixe>/<n° de l'issue>-<sujet>`, et le workflow « Conventions », qui juge chaque pull request.
- Une skill par dossier, `skills/<nom>/SKILL.md`, au format Agent Skills : son `name` est le nom du dossier.
- Une skill copiée ou adaptée garde la licence de son amont et le commit dont elle part, dans son en-tête.
- Les commentaires du code sont en anglais. Aucun nom de personne dans un commentaire ou un titre de test.
- Les décisions qui touchent ce dépôt vivent dans hermes-software-factory : l'issue #36 et ses sous-issues.

## Échecs connus

Aucun.

## Interdits

- Affaiblir ou retirer une assertion, allonger un timeout.
- Pousser sur main, forcer un push, contourner un hook git.
- Cloner un autre dépôt dans celui-ci : un dépôt externe se lit dans le scratchpad, et ses fichiers peuvent être copiés.

## Chemins sensibles

- `.github/workflows/conventions.yml` : le contrôle de chaque pull request.
- `.github/CODEOWNERS` : la revue obligatoire du propriétaire.
