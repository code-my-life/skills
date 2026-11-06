#!/usr/bin/env python3
"""The catalog of the skills of Code My Life (hermes-software-factory#37): checked, listed, and kept in step with
the pinned upstream of each copy.

    catalogue.py verifier                          every rule of the catalog; exit code 1, with each problem
    catalogue.py noms --pour AGENT [--copiees | --declarees]
                                                   the skills an agent receives, one per line
    catalogue.py manuelles                         the skills that only a person starts, one per line
    catalogue.py opencode                          the permission.skill rule of the OpenCode lane, as JSON
    catalogue.py readme [--ecrire]                 the list of the README, by family; --ecrire puts it in README.md
    catalogue.py attributs [--ecrire]              the .gitattributes that keeps each external copy as its upstream
    catalogue.py amont [--recopier] [NOM...]       each copy against its pinned upstream, with the diff; --recopier
                                                   copies it again
    catalogue.py adaptees [--depuis REF]           each adapted skill whose noted upstream commit moved since the
                                                   catalog at REF (origin/main): the upstream diff, to take over by hand

An agent is operateur (the sessions of Claude Code), lane-claude, lane-opencode, hermes:<profile> or
projet:<owner/repo>. Standard library only: tomllib reads the catalog, git and npm fetch the upstream.
"""
from __future__ import annotations

import argparse
import difflib
import filecmp
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent
ORIGINS = {"maison", "amont", "npm", "projet"}
TRIGGERS = {"manuel", "auto", "carte"}
AGENT = re.compile(r"^(operateur|lane-claude|lane-opencode|hermes:[a-z0-9-]+|projet:[\w.-]+/[\w.-]+)$")
CLAUDE_DIR = {"operateur", "lane-claude"}  # both read ~/.claude/skills, which OpenCode reads too
LICENSES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "NOTICE", "NOTICE.md")
# Commands and skills that ship with Claude Code: a skill of the same name would hide or shadow them.
BUILT_IN = {
    "add-dir", "agents", "artifacts", "bug", "claude-api", "clear", "code-review", "compact", "config", "context",
    "cost", "doctor", "export", "fewer-permission-prompts", "help", "hooks", "ide", "init", "keybindings-help",
    "login", "logout", "loop", "mcp", "memory", "model", "permissions", "plugin", "plugin-authoring", "pr-comments",
    "release-notes", "resume", "review", "rewind", "run", "schedule", "security-review", "simplify", "status",
    "statusline", "terminal-setup", "update-config", "upgrade", "usage", "vim", "workflow-authoring",
}
FAMILIES = {
    "factory": "La software factory",
    "animation": "Animation et mouvement",
    "interface": "Interface et design",
    "video": "Vidéo",
    "revue": "Revue de code",
    "outils": "Outils",
}
START = "<!-- catalogue : début, généré par scripts/catalogue.py readme --ecrire -->"
END = "<!-- catalogue : fin -->"
ATTRIBUTES_HEADER = ("# Généré par scripts/catalogue.py attributs --ecrire : "
                     "une copie externe reste identique à son amont,\n"
                     "# espaces de fin de ligne compris. C'est du code tiers (linguist-vendored) : "
                     "ni git ni les règles\n"
                     "# d'hygiène de la factory ne le jugent comme du code écrit ici.\n")


def load(root: Path = ROOT) -> dict:
    with open(root / "catalog.toml", "rb") as f:
        return tomllib.load(f).get("skills") or {}


def front_matter(skill_md: Path) -> dict[str, str]:
    """The top-level keys of the YAML front matter that the rules read: name, disable-model-invocation."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    block = text.split("---", 2)[1]
    out = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip("'\"")
    return out


def copied(entry: dict) -> bool:
    """Whether the skill's files live in this repository."""
    return entry.get("copie", entry.get("origine") != "projet")


def problems(root: Path = ROOT, skills: dict | None = None) -> list[str]:
    skills = load(root) if skills is None else skills
    out: list[str] = []
    folders = {p.name for p in (root / "skills").iterdir() if p.is_dir()} if (root / "skills").is_dir() else set()
    for name in sorted(folders - set(skills)):
        out.append(f"skills/{name} : absente du catalogue")
    seen: dict[str, str] = {}
    for name, entry in sorted(skills.items()):
        where = f"{name} :"
        if name.lower() in seen:
            out.append(f"{where} même nom que {seen[name.lower()]}")
        seen[name.lower()] = name
        if name in BUILT_IN:
            out.append(f"{where} nom d'une commande intégrée de Claude Code")
        origin = entry.get("origine")
        if origin not in ORIGINS:
            out.append(f"{where} origine « {origin} » inconnue ({', '.join(sorted(ORIGINS))})")
        for key in ("licence", "famille", "role"):
            if not entry.get(key):
                out.append(f"{where} {key} manquante")
        if entry.get("famille") and entry["famille"] not in FAMILIES:
            out.append(f"{where} famille « {entry['famille']} » inconnue")
        trigger = entry.get("declenchement")
        if trigger not in TRIGGERS:
            out.append(f"{where} déclenchement « {trigger} » inconnu ({', '.join(sorted(TRIGGERS))})")
        agents = entry.get("consommateurs") or []
        if not agents:
            out.append(f"{where} aucun consommateur")
        for agent in agents:
            if not AGENT.match(agent):
                out.append(f"{where} consommateur « {agent} » inconnu")
        source = {"amont": ("depot", "ref", "chemin"), "npm": ("paquet", "version"), "projet": ("depot", "chemin")}
        for key in source.get(origin, ()):
            if not (entry.get(origin) or {}).get(key):
                out.append(f"{where} {origin}.{key} manquant")
        if entry.get("adaptee") and not all((entry.get("d_apres") or {}).get(k) for k in ("depot", "ref")):
            out.append(f"{where} adaptée sans dépôt ni commit d'amont (table d_apres)")
        folder = root / "skills" / name
        if not copied(entry):
            if folder.exists():
                out.append(f"{where} déclarée seulement (copie = false), mais skills/{name} existe")
            continue
        if not (folder / "SKILL.md").is_file():
            out.append(f"{where} skills/{name}/SKILL.md manquant")
            continue
        meta = front_matter(folder / "SKILL.md")
        if meta.get("name") != name:
            out.append(f"{where} le name de SKILL.md est « {meta.get('name')} », pas le nom du dossier")
        manual_flag = meta.get("disable-model-invocation", "").lower() == "true"
        if manual_flag and any(not a.startswith(("operateur", "projet:")) for a in agents):
            out.append(f"{where} skill d'agent qui porte disable-model-invocation : aucun agent ne pourrait la lancer")
        if trigger == "manuel" and origin == "maison" and not manual_flag:
            out.append(f"{where} procédure de l'opérateur sans disable-model-invocation: true")
        if origin in ("amont", "npm") and not any((folder / f).is_file() for f in LICENSES):
            out.append(f"{where} copie externe sans fichier de licence")
    if (root / "README.md").is_file() and readme_block(skills) not in (root / "README.md").read_text(encoding="utf-8"):
        out.append("README.md : la liste des skills ne suit pas le catalogue (catalogue.py readme --ecrire)")
    attributes = root / ".gitattributes"
    if folders and (not attributes.is_file() or attributes.read_text(encoding="utf-8") != attributes_text(skills)):
        out.append(".gitattributes : ne suit pas les copies externes du catalogue (catalogue.py attributs --ecrire)")
    return out


def attributes_text(skills: dict) -> str:
    external = [n for n, e in sorted(skills.items()) if e.get("origine") in ("amont", "npm") and copied(e)]
    return ATTRIBUTES_HEADER + "".join(f"skills/{n}/** -whitespace linguist-vendored\n" for n in external)


def names_for(skills: dict, agent: str, which: str | None = None) -> list[str]:
    out = []
    for name, entry in sorted(skills.items()):
        if agent not in (entry.get("consommateurs") or []):
            continue
        if which == "copiees" and not copied(entry) or which == "declarees" and copied(entry):
            continue
        out.append(name)
    return out


def manual(skills: dict) -> list[str]:
    return sorted(name for name, entry in skills.items() if entry.get("declenchement") == "manuel")


def opencode_rule(skills: dict) -> dict[str, str]:
    """What the OpenCode lane may see. It reads ~/.claude/skills: every skill there that is not its own, or that
    only a person starts, is hidden from it (OpenCode ignores disable-model-invocation)."""
    rule = {"*": "allow"}
    for name, entry in sorted(skills.items()):
        agents = set(entry.get("consommateurs") or [])
        mine = "lane-opencode" in agents and entry.get("declenchement") != "manuel"
        if agents & CLAUDE_DIR and not mine:
            rule[name] = "deny"
    return rule


def readme_block(skills: dict) -> str:
    lines = [START, ""]
    for family, title in FAMILIES.items():
        members = [(n, e) for n, e in sorted(skills.items()) if e.get("famille") == family]
        if not members:
            continue
        lines += [f"### {title}", ""]
        for name, entry in members:
            origin = entry.get("origine")
            if origin == "amont":
                src = f"{entry['amont']['depot']}"
            elif origin == "npm":
                src = f"npm {entry['npm']['paquet']}"
            elif origin == "projet":
                src = f"dans {entry['projet']['depot']}"
            else:
                src = "maison"
            note = "" if copied(entry) else ", déclarée"
            lines.append(f"- **`{name}`** : {entry.get('role', '')} ({src}{note}, {entry.get('declenchement')})")
        lines.append("")
    lines.append(END)
    return "\n".join(lines)


def write_readme(skills: dict, root: Path = ROOT) -> None:
    path = root / "README.md"
    text = path.read_text(encoding="utf-8")
    block = readme_block(skills)
    if START in text and END in text:
        text = text[: text.index(START)] + block + text[text.index(END) + len(END):]
    else:
        text = text.rstrip("\n") + "\n\n## Les skills\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


# Upstream: each copy is the pinned upstream folder, plus the license of its repository.

def run(args: list[str], cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


def fetch_git(repo: str, ref: str, paths: list[str], dest: Path) -> Path:
    """repo (owner/name on GitHub, or a local path) at ref, with only paths and the license files, in dest."""
    run(["git", "init", "-q", str(dest)])
    url = repo if repo.startswith(("/", "file://")) else f"https://github.com/{repo}.git"
    run(["git", "remote", "add", "origin", url], cwd=dest)
    run(["git", "config", "core.sparseCheckout", "true"], cwd=dest)
    run(["git", "sparse-checkout", "set", "--no-cone", *[f"/{p.strip('/')}/" for p in paths],
         *[f"/{f}" for f in LICENSES]], cwd=dest)
    run(["git", "fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", ref], cwd=dest)
    run(["git", "checkout", "-q", "FETCH_HEAD"], cwd=dest)
    return dest


def fetch_npm(package: str, version: str, dest: Path) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    out = subprocess.run(["npm", "pack", "-q", f"{package}@{version}", "--pack-destination", str(dest)],
                         check=True, capture_output=True, text=True).stdout.strip().splitlines()[-1]
    with tarfile.open(dest / out) as tar:
        tar.extractall(dest, filter="data")
    return dest / "package"


def expected(name: str, entry: dict, cache: dict, work: Path) -> Path:
    """A folder with what skills/<name> must hold for its pinned upstream."""
    target = work / "attendu" / name
    if entry["origine"] == "amont":
        src = entry["amont"]
        key = (src["depot"], src["ref"])
        if key not in cache:
            paths = [e["amont"]["chemin"] for e in load_all_upstream(cache["__skills"], *key)]
            cache[key] = fetch_git(src["depot"], src["ref"], paths, work / f"git-{len(cache)}")
        repo = cache[key]
        shutil.copytree(repo / src["chemin"], target)
        for lic in LICENSES:
            if (repo / lic).is_file() and not (target / lic).exists():
                shutil.copy2(repo / lic, target / lic)
    else:
        src = entry["npm"]
        key = (src["paquet"], src["version"])
        if key not in cache:
            cache[key] = fetch_npm(src["paquet"], src["version"], work / f"npm-{len(cache)}")
        shutil.copytree(cache[key] / src["chemin"], target)
    return target


def load_all_upstream(skills: dict, repo: str, ref: str) -> list[dict]:
    return [e for e in skills.values() if e.get("origine") == "amont" and copied(e)
            and e["amont"]["depot"] == repo and e["amont"]["ref"] == ref]


def compare(local: Path, wanted: Path, keep: set[str]) -> list[str]:
    """The differences between a copy and its upstream, with a short diff for each changed text file."""
    def files(base: Path) -> set[str]:
        return {str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()}
    have, want = files(local) - keep, files(wanted) - keep
    out = [f"  + {f} (en trop ici)" for f in sorted(have - want)]
    out += [f"  - {f} (manque ici)" for f in sorted(want - have)]
    for f in sorted(have & want):
        out += short_diff(local / f, wanted / f, f, ("ici", "amont"), 40)
    return out


def short_diff(a: Path, b: Path, name: str, labels: tuple[str, str], limit: int) -> list[str]:
    """Nothing when both files are the same, else their name and the first lines of a unified diff."""
    if filecmp.cmp(a, b, shallow=False):
        return []
    try:
        before, after = a.read_text(encoding="utf-8").splitlines(), b.read_text(encoding="utf-8").splitlines()
        lines = difflib.unified_diff(before, after, *labels, lineterm="")
        return [f"  ~ {name}", *("    " + line for line in list(lines)[:limit])]
    except UnicodeDecodeError:
        return [f"  ~ {name}", "    (fichier binaire)"]


def catalog_at(ref: str, root: Path = ROOT) -> dict:
    """The skills of the catalog at a git revision of this repository; none when the catalog did not exist there yet."""
    if subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"], cwd=root,
                      capture_output=True).returncode != 0:
        raise SystemExit(f"révision inconnue : {ref}")
    shown = subprocess.run(["git", "show", f"{ref}:catalog.toml"], cwd=root, capture_output=True, text=True)
    return tomllib.loads(shown.stdout).get("skills") or {} if shown.returncode == 0 else {}


def adapted_moves(skills: dict, before: dict) -> list[tuple[str, str, str, str]]:
    """(name, upstream repository, former commit, new commit) of each adapted skill whose noted upstream moved."""
    out = []
    for name, entry in sorted(skills.items()):
        new, old = entry.get("d_apres") or {}, (before.get(name) or {}).get("d_apres") or {}
        if entry.get("adaptee") and new.get("depot") and old.get("ref") and new.get("ref") != old.get("ref"):
            out.append((name, new["depot"], old["ref"], new["ref"]))
    return out


def adapted(skills: dict, before: dict) -> list[str]:
    """For each adapted skill whose upstream moved: what to take over by hand, as the upstream diff of its path."""
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (name, repo, old, new) in enumerate(adapted_moves(skills, before)):
            out.append(f"{name} : adaptée de {repo}, amont monté de {old} à {new}, à reprendre à la main")
            if not repo.startswith(("/", "file://")):
                out.append(f"  https://github.com/{repo}/compare/{old}...{new}")
            path = skills[name]["d_apres"].get("chemin")
            if not path:
                continue
            a = fetch_git(repo, old, [path], Path(tmp) / f"{i}-avant") / path
            b = fetch_git(repo, new, [path], Path(tmp) / f"{i}-apres") / path
            files = {side: {str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()} if d.is_dir() else set()
                     for side, d in (("a", a), ("b", b))}
            out += [f"  + {f}" for f in sorted(files["b"] - files["a"])]
            out += [f"  - {f}" for f in sorted(files["a"] - files["b"])]
            for f in sorted(files["a"] & files["b"]):
                out += short_diff(a / f, b / f, f, (old, new), 80)
    return out


def upstream(skills: dict, only: list[str], recopy: bool, root: Path = ROOT) -> int:
    chosen = [n for n, e in sorted(skills.items()) if e.get("origine") in ("amont", "npm") and copied(e)
              and (not only or n in only)]
    cache: dict = {"__skills": skills}
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name in chosen:
            entry = skills[name]
            try:
                wanted = expected(name, entry, cache, Path(tmp))
            except (subprocess.CalledProcessError, OSError, KeyError) as exc:
                print(f"{name} : amont injoignable ({exc})")
                failures += 1
                continue
            local = root / "skills" / name
            keep = {"LICENSE"} if entry["origine"] == "npm" else set()  # an npm package may carry no license file
            if recopy:
                kept = {k: (local / k).read_bytes() for k in keep if (local / k).is_file()}
                shutil.rmtree(local, ignore_errors=True)
                shutil.copytree(wanted, local)
                for k, data in kept.items():
                    (local / k).write_bytes(data)
                print(f"{name} : recopiée depuis l'amont")
                continue
            diff = compare(local, wanted, keep)
            if diff:
                failures += 1
                print(f"{name} : diffère de son amont figé")
                print("\n".join(diff))
            else:
                print(f"{name} : identique à son amont figé")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="catalogue.py")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verifier")
    p = sub.add_parser("noms")
    p.add_argument("--pour", required=True)
    group = p.add_mutually_exclusive_group()
    group.add_argument("--copiees", action="store_const", const="copiees", dest="which")
    group.add_argument("--declarees", action="store_const", const="declarees", dest="which")
    sub.add_parser("manuelles")
    sub.add_parser("opencode")
    p = sub.add_parser("readme")
    p.add_argument("--ecrire", action="store_true")
    p = sub.add_parser("attributs")
    p.add_argument("--ecrire", action="store_true")
    p = sub.add_parser("amont")
    p.add_argument("--recopier", action="store_true")
    p.add_argument("noms", nargs="*")
    p = sub.add_parser("adaptees")
    p.add_argument("--depuis", default="origin/main")
    args = parser.parse_args(argv)
    skills = load()
    if args.command == "verifier":
        found = problems(ROOT, skills)
        for line in found:
            print(line)
        print("catalogue conforme" if not found else f"{len(found)} écart(s)", file=sys.stderr)
        return 1 if found else 0
    if args.command == "noms":
        print("\n".join(names_for(skills, args.pour, args.which)))
    elif args.command == "manuelles":
        print("\n".join(manual(skills)))
    elif args.command == "opencode":
        print(json.dumps(opencode_rule(skills), indent=2))
    elif args.command == "readme":
        if args.ecrire:
            write_readme(skills)
        else:
            print(readme_block(skills))
    elif args.command == "attributs":
        if args.ecrire:
            (ROOT / ".gitattributes").write_text(attributes_text(skills), encoding="utf-8")
        else:
            print(attributes_text(skills), end="")
    elif args.command == "amont":
        return upstream(skills, args.noms, args.recopier)
    elif args.command == "adaptees":
        found = adapted(skills, catalog_at(args.depuis))
        print("\n".join(found) if found else f"aucune skill adaptée dont l'amont a monté depuis {args.depuis}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
