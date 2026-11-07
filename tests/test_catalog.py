"""The catalog of the skills (skills#3, hermes-software-factory#37): python3 -m unittest discover -s tests

Each rule is tested on a small repository built in a temporary folder, then the real catalog is checked whole.
Standard library only, like scripts/catalogue.py.
"""
from __future__ import annotations

import fnmatch
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load():
    spec = importlib.util.spec_from_file_location("catalogue", ROOT / "scripts" / "catalogue.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cat = load()

MAISON = """
[skills.maison-auto]
famille = "factory"
role = "Une skill maison."
origine = "maison"
licence = "MIT"
declenchement = "auto"
consommateurs = ["operateur", "lane-claude", "hermes:coder"]
"""

EXTERNE = """
[skills.copie-externe]
famille = "outils"
role = "Une copie externe."
origine = "amont"
licence = "MIT"
declenchement = "auto"
consommateurs = ["operateur", "lane-claude", "lane-opencode"]

[skills.copie-externe.amont]
depot = "exemple/skills"
ref = "v1.0.0"
chemin = "skills/copie-externe"
"""


class CatalogueTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "skills").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def skill(self, name: str, *, manual: bool = False, license: bool = False, front_name: str | None = None) -> None:
        folder = self.root / "skills" / name
        folder.mkdir()
        flag = "disable-model-invocation: true\n" if manual else ""
        (folder / "SKILL.md").write_text(f"---\nname: {front_name or name}\ndescription: Essai.\n{flag}---\n\n# {name}\n")
        if license:
            (folder / "LICENSE").write_text("MIT License\n")

    def catalog(self, text: str) -> list[str]:
        (self.root / "catalog.toml").write_text(textwrap.dedent(text))
        (self.root / ".gitattributes").write_text(cat.attributes_text(cat.load(self.root)))
        return cat.problems(self.root)

    def test_une_skill_du_depot_absente_du_catalogue_fait_echouer_le_controle(self):
        self.skill("maison-auto")
        self.skill("oubliee")
        found = self.catalog(MAISON)
        self.assertIn("skills/oubliee : absente du catalogue", found)

    def test_une_skill_d_agent_qui_porte_disable_model_invocation_est_refusee(self):
        self.skill("maison-auto", manual=True)
        found = self.catalog(MAISON)
        self.assertTrue(any("skill d'agent qui porte disable-model-invocation" in p for p in found), found)

    def test_une_procedure_de_l_operateur_sans_disable_model_invocation_est_refusee(self):
        self.skill("procedure")
        found = self.catalog(MAISON.replace("maison-auto", "procedure").replace('"auto"', '"manuel"')
                             .replace('["operateur", "lane-claude", "hermes:coder"]', '["operateur"]'))
        self.assertTrue(any("procédure de l'opérateur sans disable-model-invocation" in p for p in found), found)
        shutil.rmtree(self.root / "skills" / "procedure")
        self.skill("procedure", manual=True)
        self.assertEqual(cat.problems(self.root), [])

    def test_deux_skills_du_meme_nom_ou_le_nom_d_une_commande_integree_de_claude_code_sont_refuses(self):
        self.skill("maison-auto")
        self.skill("Maison-Auto")
        twice = MAISON + MAISON.replace("[skills.maison-auto]", "[skills.Maison-Auto]")
        self.assertTrue(any("même nom que" in p for p in self.catalog(twice)))
        self.skill("code-review")
        built_in = MAISON + MAISON.replace("[skills.maison-auto]", "[skills.code-review]")
        self.assertTrue(any("commande intégrée de Claude Code" in p for p in self.catalog(built_in)))

    def test_une_copie_externe_sans_licence_est_refusee(self):
        self.skill("copie-externe")
        found = self.catalog(EXTERNE)
        self.assertIn("copie-externe : copie externe sans fichier de licence", found)
        (self.root / "skills" / "copie-externe" / "LICENSE").write_text("MIT License\n")
        self.assertEqual(cat.problems(self.root), [])

    def test_une_skill_adaptee_sans_depot_ni_commit_d_amont_est_refusee(self):
        self.skill("maison-auto")
        found = self.catalog(MAISON + 'adaptee = true\n')
        self.assertTrue(any("adaptée sans dépôt ni commit d'amont" in p for p in found), found)
        found = self.catalog(MAISON + 'adaptee = true\n\n[skills.maison-auto.d_apres]\ndepot = "mattpocock/skills"\nref = "4ae2317"\n')
        self.assertEqual(found, [])

    def test_la_regle_permission_skill_d_opencode_suit_le_catalogue(self):
        self.skill("maison-auto")
        self.skill("copie-externe", license=True)
        self.skill("procedure", manual=True)
        manual = MAISON.replace("maison-auto", "procedure").replace('"auto"', '"manuel"').replace(
            '["operateur", "lane-claude", "hermes:coder"]', '["operateur", "lane-opencode"]')
        self.catalog(MAISON + EXTERNE + manual)
        rule = cat.opencode_rule(cat.load(self.root))
        self.assertEqual(rule, {"*": "deny", "copie-externe": "allow"})
        out = subprocess.run([sys.executable, str(ROOT / "scripts" / "catalogue.py"), "opencode"],
                             capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out), cat.opencode_rule(cat.load()))

    def test_opencode_refuse_toute_skill_qui_n_est_pas_a_sa_lane(self):
        self.skill("maison-auto")
        self.skill("copie-externe", license=True)
        self.skill("procedure", manual=True)
        manual = MAISON.replace("maison-auto", "procedure").replace('"auto"', '"manuel"').replace(
            '["operateur", "lane-claude", "hermes:coder"]', '["operateur", "lane-opencode"]')
        self.catalog(MAISON + EXTERNE + manual)
        rule = cat.opencode_rule(cat.load(self.root))

        def seen(name):  # as OpenCode reads permission.skill: the last matching pattern wins
            return [action for pattern, action in rule.items() if fnmatch.fnmatchcase(name, pattern)][-1] == "allow"
        self.assertTrue(seen("copie-externe"))
        self.assertFalse(seen("maison-auto"))
        self.assertFalse(seen("procedure"))
        self.assertFalse(seen("jvogn-report-geo"))  # synced from claude.ai, unknown to the catalog

    def test_une_copie_externe_garde_ses_espaces_et_le_gitattributes_le_dit(self):
        self.skill("copie-externe", license=True)
        self.assertEqual(self.catalog(EXTERNE), [])
        self.assertIn("skills/copie-externe/** -whitespace linguist-vendored", (self.root / ".gitattributes").read_text())
        (self.root / ".gitattributes").write_text("")
        self.assertTrue(any(".gitattributes" in p for p in cat.problems(self.root)))

    def git(self, cwd: Path, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout

    def test_une_skill_adaptee_dont_l_amont_monte_liste_le_diff_amont_depuis_le_commit_note(self):
        upstream = self.root / "amont"
        (upstream / "skills" / "x").mkdir(parents=True)
        self.git(upstream, "init", "-q", "-b", "main")
        self.git(upstream, "config", "user.name", "t")
        self.git(upstream, "config", "user.email", "t@example.com")
        for tag, text in (("v1", "Première version."), ("v2", "Seconde version.")):
            (upstream / "skills" / "x" / "SKILL.md").write_text(f"---\nname: x\n---\n\n{text}\n")
            if tag == "v2":
                (upstream / "skills" / "x" / "notes.md").write_text("Nouveau.\n")
            self.git(upstream, "add", ".")
            self.git(upstream, "commit", "-q", "-m", tag)
            self.git(upstream, "tag", tag)
        entry = textwrap.dedent(MAISON) + (f'adaptee = true\n\n[skills.maison-auto.d_apres]\ndepot = "{upstream}"\n'
                                           'ref = "v1"\nchemin = "skills/x"\n')
        before = tomllib.loads(entry)["skills"]
        after = tomllib.loads(entry.replace('ref = "v1"', 'ref = "v2"'))["skills"]
        found = cat.adapted(after, before)
        self.assertEqual(found[0], f"maison-auto : adaptée de {upstream}, amont monté de v1 à v2, à reprendre à la main")
        self.assertIn("  + notes.md", found)
        self.assertIn("  ~ SKILL.md", found)
        self.assertIn("    +Seconde version.", found)
        self.assertEqual(cat.adapted(before, before), [])

    def test_sans_catalogue_a_la_revision_de_base_aucune_skill_adaptee_n_a_bouge(self):
        self.git(self.root, "init", "-q", "-b", "main")
        self.git(self.root, "config", "user.name", "t")
        self.git(self.root, "config", "user.email", "t@example.com")
        (self.root / "README.md").write_text("skills\n")
        self.git(self.root, "add", "README.md")
        self.git(self.root, "commit", "-q", "-m", "docs")
        self.assertEqual(cat.catalog_at("HEAD", self.root), {})
        with self.assertRaises(SystemExit):
            cat.catalog_at("nexistepas", self.root)

    def test_l_aiguillage_qui_oublie_une_skill_de_l_operateur_fait_echouer_le_controle(self):
        router = MAISON.replace("maison-auto", "aiguillage").replace('"auto"', '"manuel"').replace(
            '["operateur", "lane-claude", "hermes:coder"]', '["operateur"]')
        other = MAISON.replace("maison-auto", "autre-skill")
        agent_only = MAISON.replace("maison-auto", "skill-d-agent").replace('["operateur", "lane-claude", "hermes:coder"]',
                                                                          '["hermes:coder"]')
        self.skill("aiguillage", manual=True)
        self.skill("autre-skill")
        self.skill("skill-d-agent")
        found = self.catalog(router + other + agent_only)
        self.assertEqual(found, ["aiguillage : oublie la skill de l'opérateur « autre-skill »"])
        (self.root / "skills" / "aiguillage" / "SKILL.md").write_text(
            "---\nname: aiguillage\ndescription: Essai.\ndisable-model-invocation: true\n---\n\n`autre-skill`\n")
        self.assertEqual(cat.problems(self.root), [])

    def test_le_nom_de_skill_md_suit_son_dossier(self):
        self.skill("maison-auto", front_name="autre-nom")
        self.assertTrue(any("pas le nom du dossier" in p for p in self.catalog(MAISON)))


# The 39 tags of microsoft/playwright-cli on 2026-11-06 (git ls-remote): its former npm package playwright-cli
# (2020 and 2021), and its current one @playwright/cli, from which the skill is copied (skills#9).
PLAYWRIGHT_CLI_FORMER = ["v0.4.3", "v0.4.4", "v0.5.0", "v0.5.1", "v0.5.2", "v0.150.0", "v0.151.0", "v0.152.0",
                         "v0.161.0", "v0.162.0", "v0.162.1", "v0.170.0", "v0.171.0", "v0.180.0"]
PLAYWRIGHT_CLI_CURRENT = ["0.1.7", "v0.0.64", *(f"v0.1.{n}" for n in range(24) if n != 7)]


class VraiCatalogueTest(unittest.TestCase):
    def test_le_catalogue_du_depot_est_conforme(self):
        self.assertEqual(cat.problems(ROOT), [])

    def test_le_depot_porte_sa_version_et_publie_sa_release_quand_elle_change(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertRegex(package["version"], r"^\d+\.\d+\.\d+$")
        self.assertIs(package["private"], True)
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn("    branches: [main]\n    paths: [package.json]", workflow)
        self.assertIn('if gh release view "$v"', workflow)
        self.assertIn('gh release create "$v" --target "$GITHUB_SHA"', workflow)

    def test_factory_brief_connait_le_type_skill_et_l_envoie_a_scribe(self):
        text = (ROOT / "skills" / "factory-brief" / "SKILL.md").read_text(encoding="utf-8")
        row = next(line for line in text.splitlines() if line.startswith("| skill |"))
        self.assertIn("`skill/<n>-<sujet>`", row)
        self.assertIn("patch (texte changé), minor (skill nouvelle", row)
        self.assertIn("l'impl va à `scribe`", row)
        self.assertIn("`scribe` pour docs, renommages mécaniques et issues Skill", text)

    def test_factory_author_proof_et_la_gate_du_brief_decrivent_la_preuve_skill(self):
        proof = (ROOT / "skills" / "factory-author-proof" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("- **skill** : aucun test fail-first", proof)
        self.assertIn("skill : **Skill**, le fichier de la skill est sa base", proof)
        brief = (ROOT / "skills" / "factory-brief" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("pour les types qui ont leur propre preuve (maintenance, documentation, skill", brief)

    def test_la_borne_de_playwright_cli_ecarte_l_ancien_paquet(self):
        rules = json.loads((ROOT / "renovate.json").read_text(encoding="utf-8")).get("packageRules") or []
        bound = [r["allowedVersions"] for r in rules if r.get("matchDepNames") == ["microsoft/playwright-cli"]]
        self.assertEqual(len(bound), 1)
        self.assertTrue(bound[0].startswith("!/") and bound[0].endswith("/"), bound)
        refused = re.compile(bound[0][2:-1])

        def allowed(tag):  # as Renovate reads « !/…/ » : a tag that matches the expression is refused
            return not refused.search(tag)
        self.assertTrue(allowed(cat.load()["playwright-cli"]["amont"]["ref"]))
        for tag in PLAYWRIGHT_CLI_CURRENT + ["v0.1.24", "v0.2.0", "v0.4.0", "v0.4.5", "v0.5.3", "v0.150.1", "v0.162.2",
                                             "v0.181.0"]:
            self.assertTrue(allowed(tag), tag)
        for tag in PLAYWRIGHT_CLI_FORMER:
            self.assertFalse(allowed(tag), tag)

    def test_chaque_version_figee_du_catalogue_a_un_seul_gestionnaire_renovate(self):
        config = json.loads((ROOT / "renovate.json").read_text(encoding="utf-8"))
        text = (ROOT / "catalog.toml").read_text(encoding="utf-8")
        managers: dict[tuple[str, str], set[str]] = {}
        for manager in config["customManagers"]:
            for pattern in manager["matchStrings"]:
                for m in re.finditer(pattern.replace("(?<", "(?P<"), text):
                    found = m.groupdict()
                    key = (found["depName"], found.get("currentDigest") or found["currentValue"])
                    managers.setdefault(key, set()).add(manager["datasourceTemplate"])
        skills = cat.load()
        pins = {(e["amont"]["depot"], e["amont"]["ref"]) for e in skills.values() if e.get("origine") == "amont"}
        pins |= {(e["npm"]["paquet"], e["npm"]["version"]) for e in skills.values() if e.get("origine") == "npm"}
        self.assertEqual(set(managers), pins)
        self.assertEqual({pin: found for pin, found in managers.items() if len(found) != 1}, {})

    def test_les_listes_lues_par_la_factory(self):
        skills = cat.load()
        self.assertIn("factory-author-proof", cat.names_for(skills, "hermes:coder"))
        self.assertIn("design-taste-frontend", cat.names_for(skills, "operateur", "declarees"))
        self.assertNotIn("design-taste-frontend", cat.names_for(skills, "operateur", "copiees"))
        self.assertIn("factory-nouveau-depot", cat.manual(skills))
        self.assertNotIn("factory-nouveau-depot", cat.names_for(skills, "lane-claude"))
        # Emil Kowalski's skills leave the root profile of Hermès only, until the owner decides (#5).
        self.assertNotIn("animate", cat.names_for(skills, "hermes:default"))
        self.assertIn("animate", cat.names_for(skills, "lane-opencode"))
        self.assertIn("animate", cat.names_for(skills, "operateur"))
        # The root profile of Hermès: no manual skill, since Hermès has no manual mode.
        self.assertIn("hyperframes", cat.names_for(skills, "hermes:default"))
        self.assertEqual(set(cat.names_for(skills, "hermes:default")) & set(cat.manual(skills)), set())


if __name__ == "__main__":
    unittest.main()
