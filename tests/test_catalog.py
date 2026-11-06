"""The catalog of the skills (skills#3, hermes-software-factory#37): python3 -m unittest discover -s tests

Each rule is tested on a small repository built in a temporary folder, then the real catalog is checked whole.
Standard library only, like scripts/catalogue.py.
"""
from __future__ import annotations

import importlib.util
import json
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
        self.assertEqual(rule, {"*": "allow", "maison-auto": "deny", "procedure": "deny"})
        out = subprocess.run([sys.executable, str(ROOT / "scripts" / "catalogue.py"), "opencode"],
                             capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out), cat.opencode_rule(cat.load()))

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

    def test_le_nom_de_skill_md_suit_son_dossier(self):
        self.skill("maison-auto", front_name="autre-nom")
        self.assertTrue(any("pas le nom du dossier" in p for p in self.catalog(MAISON)))


class VraiCatalogueTest(unittest.TestCase):
    def test_le_catalogue_du_depot_est_conforme(self):
        self.assertEqual(cat.problems(ROOT), [])

    def test_les_listes_lues_par_la_factory(self):
        skills = cat.load()
        self.assertIn("factory-author-proof", cat.names_for(skills, "hermes:coder"))
        self.assertIn("design-taste-frontend", cat.names_for(skills, "operateur", "declarees"))
        self.assertNotIn("design-taste-frontend", cat.names_for(skills, "operateur", "copiees"))
        self.assertIn("factory-nouveau-depot", cat.manual(skills))
        self.assertNotIn("factory-nouveau-depot", cat.names_for(skills, "lane-claude"))
        # The root profile of Hermès: no manual skill, since Hermès has no manual mode.
        self.assertIn("hyperframes", cat.names_for(skills, "hermes:default"))
        self.assertEqual(set(cat.names_for(skills, "hermes:default")) & set(cat.manual(skills)), set())


if __name__ == "__main__":
    unittest.main()
