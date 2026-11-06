# skills

La base de connaissance de Code My Life : toutes les skills de ses agents, au format
[Agent Skills](https://agentskills.io/specification), à lire ici et à installer chez chaque agent.

## Ce qu'on y trouve

- Les skills maison, écrites pour la software factory et pour les séances de Claude Code.
- Les skills adaptées d'autres dépôts, avec leur licence et le commit d'amont dont elles partent.
- Des copies de skills externes, chacune avec sa licence, quand celle-ci permet la redistribution. Les autres sont
  seulement déclarées, et s'installent depuis leur amont.

Un catalogue dira, pour chaque skill, d'où elle vient, sa version, sa licence, quels agents s'en servent et comment elle
se déclenche : à la main, d'elle-même, ou attachée à une carte de la factory. Le dépôt se remplit au fil des issues.

## Installer une skill

Claude Code, OpenCode, Codex et les autres agents du [CLI skills](https://github.com/vercel-labs/skills) :

```bash
DISABLE_TELEMETRY=1 npx skills@1.7.6 add code-my-life/skills --skill <nom> -a claude-code -g
```

Hermès Agent :

```bash
hermes skills tap add code-my-life/skills
hermes skills install <nom>
```

## Demander un changement

Ouvrez une issue avec l'un des modèles. Elle passe par la software factory de Code My Life : une carte, une pull
request, des contrôles automatiques, puis l'approbation du propriétaire.

## Licence

Ce qui est propre à ce dépôt est sous licence MIT (voir `LICENSE`). Chaque skill copiée ou adaptée garde la licence
de son amont, indiquée dans son en-tête.
