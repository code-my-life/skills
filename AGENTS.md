# skills

La base de connaissance de Code My Life : toutes les skills de ses agents, au format
[Agent Skills](https://agentskills.io/specification). On les lit ici, et chaque agent les installe depuis ce dépôt.
`catalog.toml` décrit chaque skill : son origine, sa version figée, sa licence, ses agents et son déclenchement
(code-my-life/hermes-software-factory#37). `install.sh` de la factory installe chaque agent depuis ce catalogue.

## Commandes

| Quoi | Commande |
|---|---|
| Installer | aucune : le dépôt ne contient que des documents |
| Tous les tests | `python3 -m unittest discover -s tests`, lancé par le hook `pre-push` de la factory |
| Un seul fichier de test | `python3 -m unittest tests.test_catalog` |
| Catalogue | `python3 scripts/catalogue.py verifier` |
| Copies contre leur amont | `python3 scripts/catalogue.py amont` (réseau) ; `amont --recopier <nom>` refait une copie |
| Skills adaptées | `python3 scripts/catalogue.py adaptees --depuis origin/main` (réseau) : le diff amont depuis le commit noté |
| Types | aucun |
| Build | aucun |
| Démarrer | aucun |
| Bout en bout | aucun |

## Conventions

- Issues, branches et pull requests suivent les types de la software factory : un modèle d'issue de l'organisation par
  type, une branche `<préfixe>/<n° de l'issue>-<sujet>`, et le workflow « Conventions », qui juge chaque pull request.
- Une skill par dossier, `skills/<nom>/SKILL.md`, au format Agent Skills : son `name` est le nom du dossier.
- Chaque skill a son entrée dans `catalog.toml`, et la liste du README en est tirée (`catalogue.py readme --ecrire`).
- Une copie externe ne se retouche pas à la main : elle se refait depuis son amont figé (`catalogue.py amont
  --recopier <nom>`), avec le `LICENSE` de son amont dans son dossier. Une skill adaptée nomme son amont dans
  `d_apres` : `depot`, `ref` (un tag, ou un commit de 40 caractères suivi de `branche`, que Renovate sait suivre) et
  `chemin`, le dossier amont dont le diff se liste quand `ref` monte.
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
- `catalog.toml`, `scripts/catalogue.py`, `.github/workflows/tests.yml` et `.github/workflows/amont.yml` : le
  catalogue et ses contrôles.
- `renovate.json` : les montées de version amont.
- `.github/CODEOWNERS` : la revue obligatoire du propriétaire.
