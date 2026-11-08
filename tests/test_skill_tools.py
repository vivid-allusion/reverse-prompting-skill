import importlib.util
import io
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "reverse-prompting"
SCRIPTS = SKILL / "scripts"
EXAMPLE = ROOT / "examples" / "the-last-ferry"
sys.path.insert(0, str(SCRIPTS))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


validate = load("validate", ROOT / "tools" / "validate.py")
evidence = load("check_evidence", ROOT / "tools" / "check_evidence.py")
names = load("check_names", ROOT / "tools" / "check_names.py")
rp = load("rp_lib", SCRIPTS / "rp_lib.py")
scaffold = load("scaffold", SCRIPTS / "scaffold.py")
coverage = load("coverage", SCRIPTS / "coverage.py")
check_prompts = load("check_prompts", SCRIPTS / "check_prompts.py")
VERSION = re.search(r'^\s+version: "([^"]+)"', (SKILL / "SKILL.md").read_text(encoding="utf-8"), re.M).group(1)


def quiet(fn, *args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = fn(*args)
    return code, buf.getvalue()


class TempDir(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)


class FrontPageTest(TempDir):
    def setUp(self):
        super().setUp()
        self.root = self.tmp / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__", ".git"))

    def findings(self):
        return validate.check_front_page(self.root, self.root / "skills" / "reverse-prompting")

    def edit(self, old, new):
        p = self.root / "README.md"
        s = p.read_text(encoding="utf-8")
        self.assertIn(old, s)
        p.write_text(s.replace(old, new), encoding="utf-8")

    def test_real_front_page_is_clean(self):
        self.assertEqual(self.findings(), [])

    def test_stale_version_badge_fails(self):
        self.edit("badge/skill-%s-" % VERSION, "badge/skill-0.0.9-")
        self.assertTrue(any("skill badge" in f for f in self.findings()))

    def test_stale_model_badge_fails(self):
        self.edit("badge/model-any%20video%20model-", "badge/model-one%20video%20model-")
        self.assertTrue(any("model badge" in f for f in self.findings()))

    def test_missing_picture_fails(self):
        (self.root / "assets" / "reverse-prompting-loop.svg").unlink()
        self.assertTrue(any("reverse-prompting-loop.svg" in f for f in self.findings()))

    def test_a_website_link_fails(self):
        self.edit("## Licence", "[site](https://example.com/x)\n\n## Licence")
        self.assertTrue(any("web address" in f for f in self.findings()))

    def test_licence_badge_without_a_licence_file_fails(self):
        (self.root / "LICENSE").unlink()
        self.assertTrue(any("licence" in f.lower() or "LICENSE" in f for f in self.findings()))


class ValidatorTest(TempDir):
    def setUp(self):
        super().setUp()
        self.skill = self.tmp / "reverse-prompting"
        shutil.copytree(SKILL, self.skill, ignore=shutil.ignore_patterns("__pycache__"))

    def edit(self, rel, old, new):
        p = self.skill / rel
        s = p.read_text(encoding="utf-8")
        self.assertIn(old, s)
        p.write_text(s.replace(old, new, 1), encoding="utf-8")

    def check(self):
        return validate.check(self.skill, ROOT)

    def test_real_skill_is_clean(self):
        self.assertEqual(validate.check(SKILL), [])

    def test_name_must_match_folder(self):
        self.edit("SKILL.md", 'name: "reverse-prompting"', 'name: "other"')
        self.assertTrue(any("folder name" in f for f in self.check()))

    def test_description_needs_not_for(self):
        self.edit("SKILL.md", "NOT for", "Not for")
        self.assertTrue(any("NOT for" in f for f in self.check()))

    def test_body_over_500_lines_fails(self):
        p = self.skill / "SKILL.md"
        p.write_text(p.read_text(encoding="utf-8") + "\nx\n" * 500, encoding="utf-8")
        self.assertTrue(any("lines" in f for f in self.check()))

    def test_too_much_loaded_at_once_fails(self):
        (self.skill / "references" / "hero.md").write_text("---\ntitle: x\n---\n" + "word " * 5000, encoding="utf-8")
        self.assertTrue(any("load" in f and "words" in f for f in self.check()))

    def test_missing_entry_script_fails(self):
        (self.skill / "scripts" / "coverage.py").unlink()
        self.assertTrue(any("scripts/coverage.py" in f for f in self.check()))

    def test_missing_index_link_fails(self):
        (self.skill / "references" / "extra-page.md").write_text("---\ntitle: x\n---\n# x\n", encoding="utf-8")
        self.assertTrue(any("[[extra-page]]" in f for f in self.check()))

    def test_public_link_fails(self):
        self.edit("references/hero.md", "# What gets an asset", "# What gets an asset\n\nSee https://example.com/a.")
        self.assertTrue(any("allowlist" in f for f in self.check()))

    def test_absolute_path_fails(self):
        self.edit("references/hero.md", "# What gets an asset", "# What gets an asset\n\nIn /home/someone/film.")
        self.assertTrue(any("absolute path" in f for f in self.check()))

    def test_bare_product_name_fails_like_the_apps_brand_scan(self):
        self.edit("references/hero.md", "# What gets an asset", "# What gets an asset\n\nOpen Helmer.")
        self.assertTrue(any("brand scan" in f for f in self.check()))

    def test_a_structural_name_passes_the_brand_scan(self):
        self.assertFalse(any("brand scan" in f for f in self.check()))

    def test_changelog_version_must_match(self):
        self.edit("SKILL.md", 'version: "%s"' % VERSION, 'version: "9.9.9"')
        self.assertTrue(any("CHANGELOG top entry" in f for f in self.check()))

    def test_ungrounded_eval_fails(self):
        self.edit("evals/evals.json", '"text": "_CANON"', '"text": "a phrase no page says"')
        self.assertTrue(any("does not say" in f for f in self.check()))

    def test_repo_evidence_that_no_longer_holds_fails(self):
        self.edit("evals/evals.json", '"needle": "a note under PROMPTS/"', '"needle": "a sentence the script lost"')
        self.assertTrue(any("evidence" in f for f in self.check()))


class EvidenceTest(unittest.TestCase):
    CASES = [{"id": "c", "evidence": [{"tree": "repo", "path": "skills/reverse-prompting/scripts/coverage.py", "needle": "## Missing"},
                                      {"tree": "repo", "path": "skills/reverse-prompting/scripts/coverage.py", "needle": "no such text", "absent": True},
                                      {"tree": "elsewhere", "path": "x.md", "needle": "y"}]}]

    def test_a_needle_that_holds_passes_and_an_absent_one_is_absent(self):
        findings, checked, skipped = evidence.check(self.CASES, {"repo": ROOT})
        self.assertEqual((findings, checked, skipped), ([], 2, ["elsewhere"]))

    def test_a_needle_the_code_lost_fails(self):
        cases = [{"id": "c", "evidence": [{"tree": "repo", "path": "skills/reverse-prompting/scripts/coverage.py", "needle": "gone gone"}]}]
        self.assertTrue(evidence.check(cases, {"repo": ROOT})[0])

    def test_the_real_evals_hold_in_this_repo(self):
        self.assertEqual(quiet(evidence.main, [])[0], 0)


class NamesTest(unittest.TestCase):
    def test_tokens_come_out_of_backticks_and_not_fences(self):
        self.assertEqual(names.tokens_in("Run `scaffold.py`.\n```\n`not this`\n```\n"), {"scaffold.py"})

    def test_placeholders_and_counters_reduce_to_segments(self):
        self.assertEqual(names.pieces("PROMPTS/<MODEL>/<category>/Scene_NNN/@NAME.md"), ["PROMPTS", "Scene_", "md"])

    def test_the_own_prose_cannot_vouch_for_itself(self):
        blob = names.corpus([ROOT])
        self.assertNotIn("Reverse prompting: from animatic stills", blob)
        self.assertIn("def build(root)", blob)


class LibTest(unittest.TestCase):
    def test_numbers_become_scene_and_shot_names(self):
        self.assertEqual((rp.scene_dir("2"), rp.scene_dir("Scene_14"), rp.shot_name("7"), rp.shot_name("SHOT_120")),
                         ("Scene_002", "Scene_014", "SHOT_007", "SHOT_120"))

    def test_elements_cell(self):
        self.assertEqual(rp.parse_elements("@A:CAST; @B:PROPS:background"), [("@A", "01_CAST", "hero"), ("@B", "02_PROPS", "background")])
        with self.assertRaises(ValueError):
            rp.parse_elements("@A:LIGHTS")

    def test_both_table_forms_read_the_same(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            md = tmp / "shots.md"
            md.write_text("| shot | scene | still |\n|---|---|---|\n| 1 | 1 | https://x.example/a.png |\n", encoding="utf-8")
            csvf = tmp / "shots.csv"
            csvf.write_text("shot,scene,still\n1,1,https://x.example/a.png\n", encoding="utf-8")
            self.assertEqual(rp.read_table(md), rp.read_table(csvf))
        finally:
            shutil.rmtree(tmp)

    def test_read_prompt_shapes(self):
        good = rp.read_prompt("```prompt\nA harbour.\nEmpty.\n```\n![ref](https://x.example/a.png)\n")
        self.assertEqual((good["prompt"], len(good["embeds"]), good["errors"]), ("A harbour.\nEmpty.", 1, []))
        self.assertTrue(rp.read_prompt("```\nA harbour.\n```\n")["errors"])
        self.assertTrue(rp.read_prompt("```prompt\nA harbour.\n")["errors"])
        self.assertTrue(rp.read_prompt("A harbour.\nhttps://x.example/a.png\n")["errors"])
        self.assertTrue(rp.read_prompt("A harbour.\nA second line.\n")["errors"])
        self.assertTrue(rp.read_prompt("# Notes\n")["errors"])
        both = rp.read_prompt("A shot.\n![](https://x.example/a.png)\n![reference_images](https://x.example/b.png)\n")
        self.assertTrue(any("start frame" in e for e in both["errors"]))
        bookmark = rp.read_prompt("![](https://x.example/old.png)\nA harbour.\n![ref](https://x.example/a.png)\n")
        self.assertEqual((bookmark["prompt"], len(bookmark["embeds"]), bookmark["errors"]), ("A harbour.", 1, []))


class ScaffoldTest(TempDir):
    def test_scaffold_lays_out_scenes_shots_and_canon(self):
        code, _ = quiet(scaffold.main, [str(EXAMPLE / "shots.csv"), str(self.tmp)])
        self.assertEqual(code, 0)
        for rel in ("MAP/SCENES/Scene_002/SCENE.md", "MAP/SCENES/Scene_002/SHOT_004.md",
                    "02_PRE-PRODUCTION/01_CAST/_CANON/@MARTA/@MARTA_ABOUT.md",
                    "02_PRE-PRODUCTION/01_CAST/Scene_003/@MARTA/@MARTA_ABOUT.md",
                    "02_PRE-PRODUCTION/01_CAST/Scene_002/@TOMAS/@TOMAS_ABOUT.md"):
            self.assertTrue((self.tmp / rel).is_file(), rel)
        self.assertFalse((self.tmp / "02_PRE-PRODUCTION/01_CAST/_CANON/@TOMAS").exists(), "one scene: no canon")
        self.assertFalse((self.tmp / "02_PRE-PRODUCTION/02_PROPS/Scene_001/@ROPE").exists(), "background: no folder")
        self.assertTrue((self.tmp / "02_PRE-PRODUCTION/07_MISC/Scene_001").is_dir(), "every category gets its scene folders")
        self.assertFalse((self.tmp / "PROMPTS").exists())
        self.assertIn("| @ROPE | 02_PROPS | background | |", (self.tmp / "MAP/SCENES/Scene_001/SHOT_001.md").read_text(encoding="utf-8"))

    def test_scaffold_never_overwrites(self):
        target = self.tmp / "MAP/SCENES/Scene_001/SHOT_001.md"
        target.parent.mkdir(parents=True)
        target.write_text("the person's words\n", encoding="utf-8")
        _, out = quiet(scaffold.main, [str(EXAMPLE / "shots.csv"), str(self.tmp)])
        self.assertEqual(target.read_text(encoding="utf-8"), "the person's words\n")
        self.assertIn("kept", out)

    def test_dry_run_writes_nothing(self):
        quiet(scaffold.main, [str(EXAMPLE / "shots.csv"), str(self.tmp), "--dry-run"])
        self.assertEqual(list(self.tmp.iterdir()), [])


class ExampleTest(TempDir):
    def setUp(self):
        super().setUp()
        self.proj = self.tmp / "film"
        shutil.copytree(EXAMPLE, self.proj)

    def test_example_prompts_are_clean(self):
        self.assertEqual(quiet(check_prompts.main, [str(self.proj), "--min-refs", "1"])[0], 0)

    def test_example_coverage_is_complete_and_committed_as_built(self):
        code, _ = quiet(coverage.main, [str(self.proj)])
        self.assertEqual(code, 0)
        for rel in ("MAP/COVERAGE.md", "MAP/PROMPTS_INDEX.md", "MAP/SCENES/Scene_002/SHOT_002.md"):
            self.assertEqual((self.proj / rel).read_text(encoding="utf-8"), (EXAMPLE / rel).read_text(encoding="utf-8"), rel)

    def test_a_missing_hero_leads_the_report(self):
        (self.proj / "PROMPTS/SEEDREAM-5.0/06_VEHICLES/Scene_001/@LAST_FERRY.md").unlink()
        code, out = quiet(coverage.main, [str(self.proj)])
        self.assertEqual(code, 1)
        self.assertIn("MISSING: Scene_001 SHOT_001 `@LAST_FERRY`", out)
        cov = (self.proj / "MAP/COVERAGE.md").read_text(encoding="utf-8")
        self.assertLess(cov.index("@LAST_FERRY"), cov.index("## By shot"))

    def test_a_plate_from_another_scene_does_not_cover(self):
        src = self.proj / "PROMPTS/SEEDREAM-5.0/03_ENVIRONMENTS/Scene_003/@ISLAND_JETTY.md"
        for model in ("SEEDREAM-5.0", "GPT-IMAGE-2.5"):
            p = self.proj / ("PROMPTS/%s/03_ENVIRONMENTS/Scene_003/@ISLAND_JETTY.md" % model)
            text = p.read_text(encoding="utf-8")
            p.unlink()
        other = self.proj / "PROMPTS/SEEDREAM-5.0/03_ENVIRONMENTS/Scene_001/@ISLAND_JETTY.md"
        other.write_text(text, encoding="utf-8")
        self.assertFalse(src.exists())
        self.assertEqual(quiet(coverage.main, [str(self.proj), "--check"])[0], 1)

    def test_a_note_in_prompts_fails(self):
        (self.proj / "PROMPTS/SEEDREAM-5.0/02_PROPS/_CANON/@TIN_BOX_ABOUT.md").write_text("# @TIN_BOX\n", encoding="utf-8")
        code, out = quiet(check_prompts.main, [str(self.proj)])
        self.assertEqual(code, 1)
        self.assertIn("a note under PROMPTS/", out)

    def test_a_bare_address_line_fails(self):
        p = self.proj / "PROMPTS/SEEDREAM-5.0/02_PROPS/_CANON/@TIN_BOX.md"
        p.write_text(p.read_text(encoding="utf-8") + "https://x.example/a.png\n", encoding="utf-8")
        code, out = quiet(check_prompts.main, [str(self.proj)])
        self.assertEqual(code, 1)

    def test_a_multi_shot_video_prompt_reaches_every_shot_of_its_beat(self):
        quiet(coverage.main, [str(self.proj)])
        for n in (2, 3, 4):
            text = (self.proj / ("MAP/SCENES/Scene_002/SHOT_%03d.md" % n)).read_text(encoding="utf-8")
            self.assertIn("VIDEO/Scene_002/SHOTS_002-004.md", text)


if __name__ == "__main__":
    unittest.main()
