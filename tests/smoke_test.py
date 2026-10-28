"""Smoke tests for the yt-* skills. Standard library only.

    python3 tests/smoke_test.py          (or: python -m unittest discover -s tests -v)

Every tool is run as a subprocess from a temporary working directory, so the tests also prove the
tools do not depend on the current directory. The skills are copied to a temp folder first, the same
way the installer lays them out, which proves the cross-skill imports (yt-chapters -> yt-edit,
yt-viral -> yt-script/hooks.json) survive installation.
"""
import glob, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_SRC = os.path.join(ROOT, "skills")


def run(script, *args, cwd=None, env_extra=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    env.update(env_extra or {})
    p = subprocess.run([sys.executable, script, *args], cwd=cwd, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout + p.stderr


def srt(n=12, step=50, text="Point number {} about the topic and why it matters"):
    def ts(s):
        return "%02d:%02d:%02d,000" % (s // 3600, s % 3600 // 60, s % 60)
    return "\n".join("%d\n%s --> %s\n%s\n" % (i + 1, ts(i * step), ts(i * step + 8), text.format(i + 1))
                     for i in range(n))


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="ytskills_")
        cls.skills = os.path.join(cls.tmp, "installed")
        shutil.copytree(SKILLS_SRC, cls.skills, ignore=shutil.ignore_patterns("__pycache__"))
        cls.work = os.path.join(cls.tmp, "work")  # a cwd that is NOT the skill folder
        os.makedirs(cls.work)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def tool(self, skill, script, *args, **kw):
        return run(os.path.join(self.skills, skill, script), *args, cwd=self.work, **kw)

    def write(self, name, text, encoding="utf-8"):
        path = os.path.join(self.work, name)
        with open(path, "w", encoding=encoding, newline="\n") as fh:
            fh.write(text)
        return path


class TestPackaging(Base):
    def test_eleven_skills_with_valid_frontmatter(self):
        files = sorted(glob.glob(os.path.join(SKILLS_SRC, "*", "SKILL.md")))
        self.assertEqual(len(files), 12)
        for f in files:
            with open(f, encoding="utf-8") as fh:
                text = fh.read()
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            self.assertTrue(m, f + ": missing frontmatter")
            name = re.search(r"^name:\s*(.+)$", m.group(1), re.M)
            self.assertTrue(name, f + ": missing name")
            self.assertEqual(name.group(1).strip(), os.path.basename(os.path.dirname(f)))
            self.assertIn("description:", m.group(1))

    def test_every_skill_saves_to_the_pack_with_valid_sections(self):
        spec = importlib.util.spec_from_file_location("pack", os.path.join(SKILLS_SRC, "yt-pack", "pack.py"))
        pack = importlib.util.module_from_spec(spec); spec.loader.exec_module(pack)
        for f in glob.glob(os.path.join(SKILLS_SRC, "*", "SKILL.md")):
            skill = os.path.basename(os.path.dirname(f))
            if skill == "yt-pack":
                continue
            with open(f, encoding="utf-8") as fh:
                text = fh.read()
            self.assertIn("## Save to the video pack", text, skill)
            sections = re.findall(r"pack\.py add .*?--section (\w+)", text)
            self.assertTrue(sections, skill)
            for s in sections:
                self.assertIn(s, pack.ORDER, skill)

    def test_hooks_json(self):
        with open(os.path.join(SKILLS_SRC, "yt-script", "hooks.json"), encoding="utf-8") as fh:
            self.assertEqual(len(json.load(fh)["hooks"]), 21)

    def test_no_claude_specific_paths(self):
        for f in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
            if os.path.isfile(f) and f.endswith((".md", ".py", ".json", ".sh", ".ps1")) \
                    and os.path.basename(f) != "smoke_test.py":
                with open(f, encoding="utf-8") as fh:
                    self.assertNotIn(".claude", fh.read(), f)


class TestTools(Base):
    def test_hookscore(self):
        rc, out = self.tool("yt-script", "hookscore.py", "--hook", "I tried every AI editor so you don't have to")
        self.assertEqual(rc, 0); self.assertIn("VERDICT", out)

    def test_hookscore_bad_input_exits_nonzero(self):
        self.assertEqual(self.tool("yt-script", "hookscore.py", "missing.txt")[0], 1)
        self.assertEqual(self.tool("yt-script", "hookscore.py", "--hook")[0], 1)

    def test_hookscore_file_with_bom_and_accents(self):
        p = self.write("hooks.txt", "\ufeffỌmọ Naijá built an app in 7 days\nWhy nobody watches your videos\n")
        rc, out = self.tool("yt-script", "hookscore.py", p)
        self.assertEqual(rc, 0); self.assertIn("winner", out)

    def test_title_linter_and_accents(self):
        rc, out = self.tool("yt-package", "title.py", "--title", "I Tried Every AI Video Editor", "--thumb", "AI RAN IT")
        self.assertEqual(rc, 0); self.assertIn("score", out)
        p = self.write("titles.txt", "Ọmọ Naijá builds an app in 7 days\nI quit my 9–5 for this\n")
        rc, out = self.tool("yt-package", "title.py", p, env_extra={"PYTHONUTF8": "0", "LC_ALL": "C", "PYTHONCOERCECLOCALE": "0"})
        self.assertEqual(rc, 0, out)

    def test_deadair_srt_vtt_whisper(self):
        p = self.write("t.srt", srt(3, step=20))
        rc, out = self.tool("yt-edit", "deadair.py", p)
        self.assertEqual(rc, 0); self.assertIn("cuts", out)
        vtt = "WEBVTT\n\n00:00:00.000 --> 00:00:03.000\nhello there\n\n00:00:09.000 --> 00:00:12.000\nsecond line\n"
        rc, out = self.tool("yt-edit", "deadair.py", self.write("t.vtt", vtt))
        self.assertEqual(rc, 0, out)
        wj = json.dumps({"segments": [{"start": 0.0, "end": 3.0, "text": " hello"}, {"start": 9.0, "end": 12.0, "text": " again"}]})
        rc, out = self.tool("yt-edit", "deadair.py", self.write("t.json", wj))
        self.assertEqual(rc, 0, out)

    def test_deadair_json_flag_and_empty_input(self):
        p = self.write("t2.srt", srt(3, step=20))
        rc, out = self.tool("yt-edit", "deadair.py", p, "--json")
        self.assertEqual(rc, 0); json.loads(out)
        self.assertEqual(self.tool("yt-edit", "deadair.py", self.write("empty.srt", ""))[0], 1)

    def test_chapters_uses_sibling_skill(self):
        p = self.write("c.srt", srt(12))
        rc, out = self.tool("yt-chapters", "chapters.py", p, "--target", "4", "--json")
        self.assertEqual(rc, 0, out)
        data = json.loads(out)
        self.assertTrue(data["valid"]); self.assertEqual(data["chapters"][0]["label"], "0:00")

    def test_retention(self):
        rows = ["time,retention"] + ["%d,%s" % (t, max(20, 100 - t * 0.9)) for t in range(0, 200, 10)]
        p = self.write("r.csv", "\n".join(rows))
        rc, out = self.tool("yt-retention", "retention.py", p, "--duration", "200")
        self.assertEqual(rc, 0, out); self.assertIn("HOOK LEAK", out)

    def test_swipe_uses_sibling_hooks_json(self):
        vids = [{"channel": "A", "title": t, "views": v} for t, v in
                [("x1", 1000), ("x2", 1200), ("x3", 900), ("x4", 1100), ("The Statistic: 90% quit", 9000)]]
        rc, out = self.tool("yt-viral", "swipe.py", self.write("v.json", json.dumps(vids)), "--min", "2.0")
        self.assertEqual(rc, 0, out); self.assertIn("8.18x", out)

    def test_missing_files_exit_nonzero(self):
        for skill, script, arg in [("yt-package", "title.py", "nope.txt"), ("yt-edit", "deadair.py", "nope.srt"),
                                   ("yt-chapters", "chapters.py", "nope.srt"), ("yt-retention", "retention.py", "nope.csv"),
                                   ("yt-viral", "swipe.py", "nope.json")]:
            self.assertEqual(self.tool(skill, script, arg)[0], 1, script)


class TestPack(Base):
    def pack(self, *args, **kw):
        return self.tool("yt-pack", "pack.py", *args, **kw)

    def setUp(self):
        self.root = os.path.join(self.work, "videos")
        shutil.rmtree(self.root, ignore_errors=True)

    def add(self, video, section, text):
        f = self.write("section.md", text)
        return self.pack("add", "--root", self.root, "--video", video, "--section", section, "--file", f, "--delete-source")

    def read_pack(self, slug):
        with open(os.path.join(self.root, slug, "video-pack.md"), encoding="utf-8") as fh:
            return fh.read()

    def test_add_orders_sections_and_builds_index(self):
        self.assertEqual(self.add("My Video", "script", "SCRIPT TEXT")[0], 0)
        self.assertEqual(self.add("My Video", "hooks", "HOOK TEXT")[0], 0)
        text = self.read_pack("my-video")
        self.assertLess(text.index("HOOK TEXT"), text.index("SCRIPT TEXT"))  # fixed order
        with open(os.path.join(self.root, "index.md"), encoding="utf-8") as fh:
            self.assertIn("hooks, script", fh.read())
        self.assertFalse(os.path.exists(os.path.join(self.work, "section.md")))  # --delete-source

    def test_rerun_replaces_and_keeps_user_notes(self):
        self.add("My Video", "script", "FIRST")
        path = os.path.join(self.root, "my-video", "video-pack.md")
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("MY OWN NOTE\n")
        self.add("My Video", "script", "SECOND")
        text = self.read_pack("my-video")
        self.assertIn("SECOND", text); self.assertNotIn("FIRST", text)
        self.assertEqual(text.count("yt:begin script"), 1)
        self.assertIn("MY OWN NOTE", text)

    def test_accents_slug_and_path_traversal(self):
        self.assertEqual(self.add("Ọmọ Naijá: 30 days", "idea", "x")[0], 0)
        self.assertTrue(os.path.isfile(os.path.join(self.root, "omo-naija-30-days", "video-pack.md")))
        self.assertEqual(self.add("../../evil", "idea", "x")[0], 0)
        self.assertTrue(os.path.isfile(os.path.join(self.root, "evil", "video-pack.md")))
        self.assertFalse(os.path.exists(os.path.join(self.work, "..", "evil")))

    def test_bad_input_is_refused(self):
        self.assertEqual(self.add("V", "nonsense", "x")[0], 1)
        self.assertEqual(self.add("V", "script", "   ")[0], 1)
        rc, out = self.pack("add", "--root", self.skills, "--video", "V", "--section", "idea", "--text", "x")
        self.assertEqual(rc, 1); self.assertIn("refusing", out)  # never write into the skills folder

    def test_stdin_show_and_list(self):
        script = os.path.join(self.skills, "yt-pack", "pack.py")
        p = subprocess.run([sys.executable, script, "add", "--root", self.root, "--video", "Piped", "--section", "notes", "--stdin"],
                           input="Ọmọ from stdin".encode("utf-8"), capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        rc, out = self.pack("show", "--root", self.root, "--video", "Piped")
        self.assertEqual(rc, 0); self.assertIn("from stdin", out)
        rc, out = self.pack("list", "--root", self.root)
        self.assertIn("piped", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
