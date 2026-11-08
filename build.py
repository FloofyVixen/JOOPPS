"""Build script for the Java course site.

Every piece of Java shown on the site goes through this script:
  - examples are compiled and run; their real output (or real error) is recorded
  - fill-in-the-blank exercises are compiled with every accepted answer
    (all must run and print the same thing) and with every listed wrong answer
    (each must fail or print something different; the real message is recorded)
  - "read the error" exercises must really fail, and their fix must really work
  - "predict the output" answers must equal the real output
  - snippets must appear word-for-word in a verified file of the same lesson

If anything doesn't hold, the build stops with an error.
Output: web/course-data.js
"""
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, ".work")
CACHE_FILE = os.path.join(ROOT, ".cache.json")
OUT = os.path.join(ROOT, "docs", "course-data.js")

# Run Java without the sandbox's proxy settings so output looks like a normal machine.
ENV = {k: v for k, v in os.environ.items()
       if k not in ("JAVA_TOOL_OPTIONS", "_JAVA_OPTIONS", "JDK_JAVA_OPTIONS")}

BLANK_RE = re.compile(r"\[\[(\w+)\]\]")
TASKS = {}

try:
    with open(CACHE_FILE) as f:
        CACHE = json.load(f)
except (OSError, ValueError):
    CACHE = {}


class BuildError(Exception):
    pass


def fail(where, msg):
    raise BuildError(f"{where}: {msg}")


# ---------- answer normalisation (app.js has an identical copy) ----------

def norm(s, exact=False):
    s = s.strip()
    if exact:
        return s
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r" ?([^\w ]) ?", r"\1", s, flags=re.ASCII)
    return s


# ---------- running Java ----------

def java_version():
    r = subprocess.run(["java", "-version"], capture_output=True, text=True, env=ENV)
    first = (r.stderr or r.stdout).splitlines()[0]
    m = re.search(r'"([^"]+)"', first)
    return m.group(1) if m else first


def run_java(files, main, stdin=""):
    key = hashlib.sha256(json.dumps([files, main, stdin], sort_keys=True).encode()).hexdigest()
    if key in CACHE:
        return CACHE[key]
    os.makedirs(WORK, exist_ok=True)
    d = tempfile.mkdtemp(dir=WORK)
    try:
        for name, src in files.items():
            with open(os.path.join(d, name), "w") as f:
                f.write(src)
        c = subprocess.run(["javac", *sorted(files)], cwd=d, capture_output=True,
                           text=True, env=ENV, timeout=120)
        if c.returncode != 0:
            res = {"kind": "compile", "command": "javac " + " ".join(sorted(files)),
                   "text": (c.stdout + c.stderr).rstrip("\n")}
        elif not main:
            res = {"kind": "ok", "stdout": ""}
        else:
            r = subprocess.run(["java", main], cwd=d, capture_output=True, text=True,
                               env=ENV, timeout=20, input=stdin)
            if r.returncode != 0:
                err = r.stderr.rstrip("\n").split("\n")
                if len(err) > 14:  # e.g. StackOverflowError prints ~1000 identical lines
                    err = err[:12] + [f"\t... ({len(err) - 12} more lines not shown)"]
                res = {"kind": "runtime", "command": "java " + main,
                       "stdout": r.stdout.rstrip("\n"), "text": "\n".join(err)}
            else:
                res = {"kind": "ok", "command": "java " + main, "stdout": r.stdout.rstrip("\n")}
    finally:
        shutil.rmtree(d, ignore_errors=True)
    CACHE[key] = res
    return res


def run_commands(files, commands):
    """Run literal javac/java commands in order, as a student would in a terminal."""
    key = hashlib.sha256(json.dumps(["cmd", files, commands], sort_keys=True).encode()).hexdigest()
    if key in CACHE:
        return CACHE[key]
    os.makedirs(WORK, exist_ok=True)
    d = tempfile.mkdtemp(dir=WORK)
    out = []
    try:
        for name, src in files.items():
            with open(os.path.join(d, name), "w") as f:
                f.write(src)
        for cmd in commands:
            parts = cmd.split()
            if parts[0] not in ("javac", "java", "ls"):
                raise BuildError(f"command not allowed: {cmd}")
            r = subprocess.run(parts, cwd=d, capture_output=True, text=True, env=ENV, timeout=60)
            out.append({"command": cmd, "output": (r.stdout + r.stderr).rstrip("\n"),
                        "code": r.returncode})
    finally:
        shutil.rmtree(d, ignore_errors=True)
    CACHE[key] = out
    return out


def fill(files, values):
    return {name: BLANK_RE.sub(lambda m: values[m.group(1)], src) for name, src in files.items()}


def same_output(a, b):
    """Compare program output the way the editor does: trailing spaces on a line don't count."""
    if a is None or b is None:
        return a == b
    clean = lambda t: "\n".join(line.rstrip() for line in t.split("\n")).rstrip("\n")
    return clean(a) == clean(b)


def blank_ids(files):
    ids = []
    for src in files.values():
        for m in BLANK_RE.finditer(src):
            if m.group(1) in ids:
                raise BuildError(f"blank {m.group(1)} used twice")
            ids.append(m.group(1))
    return ids


# ---------- inline text markup ----------

def inline(text):
    """`code`, **bold**, [label](url). Everything else is escaped."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>" + html.escape(p[1:-1]) + "</code>")
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                   lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', p)
        out.append(p)
    return "".join(out)


# ---------- block processing ----------

def process_block(lesson_id, i, b, verified_sources):
    where = f"{lesson_id} block {i} ({b['type']})"
    t = b["type"]

    if t in ("p", "h", "note", "list", "steps"):
        o = dict(b)
        if "text" in b:
            o["html"] = inline(b["text"])
            del o["text"]
        if "items" in b:
            o["items"] = [inline(x) for x in b["items"]]
        if "label" in b:
            o["label"] = b["label"]
        return o

    if t == "code":
        files = b["files"]
        expect = b.get("expect", "ok")
        res = run_java(files, b.get("run"), b.get("stdin", ""))
        if res["kind"] != expect:
            fail(where, f"expected {expect}, got {res['kind']}: {res.get('text', res.get('stdout'))}")
        if "output" in b and not same_output(res.get("stdout"), b["output"]):
            fail(where, f"output mismatch.\nexpected:\n{b['output']}\nactual:\n{res.get('stdout')}")
        verified_sources.extend(files.values())
        hide = b.get("hide", [])
        return {"type": "code", "files": [[n, s] for n, s in files.items() if n not in hide],
                "result": res, "showResult": b.get("show", True),
                "collapsed": b.get("collapsed", False),
                "caption": inline(b["caption"]) if b.get("caption") else None,
                "after": inline(b["after"]) if b.get("after") else None}

    if t == "terminal":
        out = run_commands(b["files"], b["commands"])
        for step, want in zip(out, b.get("codes", [0] * len(out))):
            if step["code"] != want:
                fail(where, f"command {step['command']} exited {step['code']}: {step['output']}")
        verified_sources.extend(b["files"].values())
        return {"type": "terminal", "steps": out,
                "caption": inline(b["caption"]) if b.get("caption") else None}

    if t == "snippet":
        code = b["code"]
        if not any(code in s for s in verified_sources):
            fail(where, "snippet does not appear in any verified file earlier in this lesson:\n" + code)
        return {"type": "snippet", "code": code,
                "caption": inline(b["caption"]) if b.get("caption") else None}

    if t == "blanks":
        files = b["files"]
        ids = blank_ids(files)
        spec = b["blanks"]
        if set(ids) != set(spec):
            fail(where, f"blank ids in code {ids} != spec {list(spec)}")
        correct = {k: spec[k]["accept"][0] for k in ids}
        base = run_java(fill(files, correct), b["run"])
        if base["kind"] != "ok":
            fail(where, f"correct answer does not run: {base}")
        if "output" in b and not same_output(base["stdout"], b["output"]):
            fail(where, f"output mismatch.\nexpected:\n{b['output']}\nactual:\n{base['stdout']}")
        verified_sources.extend(fill(files, correct).values())
        out_blanks = {}
        for k in ids:
            s = spec[k]
            exact = s.get("exact", False)
            accepted = []
            for alt in s["accept"]:
                vals = dict(correct)
                vals[k] = alt
                r = run_java(fill(files, vals), b["run"])
                if r["kind"] != "ok" or not same_output(r["stdout"], base["stdout"]):
                    fail(where, f"accepted answer {alt!r} for blank {k} does not behave the same: {r}")
                accepted.append(norm(alt, exact))
            wrongs = []
            for w in s.get("wrong", []):
                if norm(w["answer"], exact) in accepted:
                    fail(where, f"wrong answer {w['answer']!r} normalises to an accepted one")
                vals = dict(correct)
                vals[k] = w["answer"]
                r = run_java(fill(files, vals), b["run"])
                if r["kind"] == "ok" and same_output(r["stdout"], base["stdout"]):
                    fail(where, f"wrong answer {w['answer']!r} for blank {k} behaves exactly like the right one")
                wrongs.append({"answer": norm(w["answer"], exact), "shown": w["answer"],
                               "why": inline(w["why"]), "result": r})
            out_blanks[k] = {"accept": accepted, "solution": s["accept"][0],
                             "hint": inline(s["hint"]) if s.get("hint") else None,
                             "exact": exact, "wrong": wrongs,
                             "width": max(len(a) for a in s["accept"] + [w["answer"] for w in s.get("wrong", [])])}
        return {"type": "blanks", "id": b["id"], "title": b.get("title"),
                "prompt": inline(b["prompt"]), "files": [[n, s] for n, s in files.items()],
                "run": b["run"], "blanks": out_blanks, "result": base,
                "explain": inline(b["explain"]) if b.get("explain") else None}

    if t == "predict":
        res = run_java(b["files"], b["run"])
        if res["kind"] != "ok":
            fail(where, f"predict program must run: {res}")
        choices = b["choices"]
        if choices[b["answer"]] != res["stdout"]:
            fail(where, f"marked answer != real output.\nmarked:\n{choices[b['answer']]}\nreal:\n{res['stdout']}")
        for j, c in enumerate(choices):
            if j != b["answer"] and c == res["stdout"]:
                fail(where, f"choice {j} is also the real output")
        verified_sources.extend(b["files"].values())
        return {"type": "predict", "id": b["id"], "prompt": inline(b["prompt"]),
                "files": [[n, s] for n, s in b["files"].items()], "choices": choices,
                "answer": b["answer"], "result": res, "explain": inline(b["explain"])}

    if t == "error":
        files = b["files"]
        res = run_java(files, b.get("run"))
        if res["kind"] != b["expect"]:
            fail(where, f"expected {b['expect']}, got {res['kind']}: {res}")
        fixed = dict(files)
        for fname, old, new in b["fix"]:
            if fixed[fname].count(old) != 1:
                fail(where, f"fix text {old!r} must appear exactly once in {fname}")
            fixed[fname] = fixed[fname].replace(old, new)
        fres = run_java(fixed, b.get("run"))
        if fres["kind"] != "ok":
            fail(where, f"fixed version does not run: {fres}")
        if b.get("fixed_output") is not None and fres["stdout"] != b["fixed_output"]:
            fail(where, f"fixed output mismatch: {fres['stdout']}")
        verified_sources.extend(fixed.values())
        return {"type": "error", "id": b["id"], "prompt": inline(b["prompt"]),
                "files": [[n, s] for n, s in files.items()], "result": res,
                "question": inline(b["question"]), "choices": [inline(c) for c in b["choices"]],
                "answer": b["answer"], "explain": inline(b["explain"]),
                "fixedFiles": [[n, s] for n, s in fixed.items()], "fixedResult": fres}

    if t == "write":
        return process_write(where, b)

    if t == "quiz":
        if not 0 <= b["answer"] < len(b["choices"]):
            fail(where, "answer index out of range")
        return {"type": "quiz", "id": b["id"], "question": inline(b["question"]),
                "choices": [inline(c) for c in b["choices"]], "answer": b["answer"],
                "explain": inline(b["explain"])}

    fail(where, f"unknown block type {t}")


def strip_comments(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"//[^\n]*", "", src)


def check_stage(where, files, tests, run, output, tests_run, tests_output, checks):
    """Verify one finished state of a write-it-yourself task."""
    allf = dict(files)
    allf.update(tests)
    r = run_java(allf, run)
    if r["kind"] != "ok":
        fail(where, f"reference solution does not run: {r}")
    if not same_output(r["stdout"], output):
        fail(where, f"reference output mismatch.\nexpected:\n{output}\nactual:\n{r['stdout']}")
    if tests_run:
        t = run_java(allf, tests_run)
        if t["kind"] != "ok" or not same_output(t["stdout"], tests_output):
            fail(where, f"hidden tests do not pass on the reference solution: {t}")
    code = "\n".join(strip_comments(s) for s in files.values())
    for c in checks:
        if not re.search(c["pattern"], code):
            fail(where, f"reference solution fails its own check {c['pattern']!r}")


def process_write(where, b):
    tests = b.get("tests", {})
    tests_run = b.get("tests_run")
    checks = b.get("checks", [])
    for c in checks:
        re.compile(c["pattern"])
    out = {
        "type": "write", "id": b["id"], "mode": b["mode"], "title": b["title"],
        "goal": inline(b["goal"]),
        "requirements": [inline(x) for x in b.get("requirements", [])],
        "files": b["files"], "starter": [[n, s] for n, s in b.get("starter", {}).items()],
        "tests": [[n, s] for n, s in tests.items()], "testsRun": tests_run,
        "hints": [inline(h) for h in b.get("hints", [])],
        "checks": [{"pattern": c["pattern"], "message": inline(c["message"])} for c in checks],
    }
    starter = b.get("starter", {})
    if starter:
        sres = run_java({**starter, **tests}, b.get("run") or b["steps"][-1]["run"])
        out["starterResult"] = sres
    if b["mode"] == "guided":
        steps = []
        for k, st in enumerate(b["steps"]):
            sw = f"{where} step {k + 1}"
            st_checks = st.get("checks", [])
            check_stage(sw, st["solution"], tests if st.get("use_tests") else {}, st["run"], st["output"],
                        tests_run if st.get("use_tests") else None, st.get("tests_output"), st_checks)
            if set(st["solution"]) != set(st.get("files", b["files"])):
                fail(sw, "solution files differ from the files the step asks for")
            steps.append({"title": st["title"], "text": inline(st["text"]),
                          "hint": inline(st["hint"]) if st.get("hint") else None,
                          "files": st.get("files", b["files"]), "run": st["run"], "output": st["output"],
                          "checks": [{"pattern": c["pattern"], "message": inline(c["message"])} for c in st_checks],
                          "solution": [[n, s] for n, s in st["solution"].items()]})
        out["steps"] = steps
        return out
    sol = b["solution"]
    if set(sol) != set(b["files"]):
        fail(where, "solution files differ from the files the task asks for")
    check_stage(where, sol, tests, b["run"], b["output"], tests_run, b.get("tests_output"), checks)
    if starter and out["starterResult"]["kind"] == "ok" and same_output(out["starterResult"]["stdout"], b["output"]):
        fail(where, "starter code already passes the task")
    out.update({"run": b["run"], "output": b["output"], "testsOutput": b.get("tests_output"),
                "solution": [[n, s] for n, s in sol.items()]})
    return out


def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    sys.path.insert(0, os.path.join(ROOT, "content"))
    course = load(os.path.join(ROOT, "content", "course.py"))
    TASKS.update(load(os.path.join(ROOT, "content", "tasks_intro.py")).TASKS)
    TASKS.update(load(os.path.join(ROOT, "content", "tasks_classes.py")).TASKS)
    TASKS.update(load(os.path.join(ROOT, "content", "tasks_inheritance.py")).TASKS)
    TASKS.update(load(os.path.join(ROOT, "content", "tasks_interfaces.py")).TASKS)
    TASKS.update(load(os.path.join(ROOT, "content", "tasks_ds.py")).TASKS)
    lessons = {}
    ex_ids = set()
    for section in course.SECTIONS:
        for lid in section.get("lessons", []):
            path = os.path.join(ROOT, "content", lid + ".py")
            if not os.path.exists(path) and os.environ.get("PARTIAL"):
                print(f"skip {lid} (not written yet)")
                continue
            mod = load(path)
            L = mod.LESSON
            if L["id"] != lid:
                raise BuildError(f"{lid}: id mismatch")
            verified = []
            blocks = []
            extra = TASKS.get(lid, [])
            if extra:
                extra = [{"type": "h", "text": "Write it yourself"},
                         {"type": "p", "text": "Now write code with no blanks to fill in. Create each file in the editor, write the whole program, and press **Run**. Your code is compiled and run for real, and the task passes when the output and checks match."}] + extra
            for i, b in enumerate(L["blocks"] + extra):
                if "id" in b:
                    if b["id"] in ex_ids:
                        raise BuildError(f"duplicate exercise id {b['id']}")
                    ex_ids.add(b["id"])
                blocks.append(process_block(lid, i, b, verified))
            for s in L["sources"]:
                if not s["url"].startswith("https://"):
                    raise BuildError(f"{lid}: source url must be https: {s['url']}")
            lessons[lid] = {
                "id": lid, "section": section["id"], "title": L["title"],
                "summary": inline(L["summary"]),
                "goals": [inline(g) for g in L.get("goals", [])],
                "cos225": inline(L["cos225"]) if L.get("cos225") else None,
                "blocks": blocks,
                "sources": [{"title": s["title"], "url": s["url"], "org": s["org"],
                             "note": inline(s["note"]) if s.get("note") else None}
                            for s in L["sources"]],
            }
            print(f"ok  {lid}: {len(blocks)} blocks")
    data = {
        "title": course.TITLE,
        "built": date.today().isoformat(),
        "java": java_version(),
        "sections": course.SECTIONS,
        "lessons": lessons,
    }
    with open(OUT, "w") as f:
        f.write("// Generated by build.py. Do not edit by hand.\n")
        f.write("window.COURSE = ")
        json.dump(data, f, indent=1)
        f.write(";\n")
    with open(CACHE_FILE, "w") as f:
        json.dump(CACHE, f)
    stamp_versions()
    print(f"wrote {OUT}")


def stamp_versions():
    """Add ?v=<content hash> to the site's own files in index.html, so browsers
    fetch the new version after every update instead of a cached copy."""
    docs = os.path.join(ROOT, "docs")
    index = os.path.join(docs, "index.html")
    with open(index) as f:
        page = f.read()

    def repl(m):
        name = m.group(2)
        with open(os.path.join(docs, name), "rb") as g:
            v = hashlib.sha256(g.read()).hexdigest()[:10]
        return f'{m.group(1)}="{name}?v={v}"'

    page = re.sub(r'(src|href)="(app\.js|editor\.js|styles\.css|course-data\.js)(?:\?v=\w+)?"', repl, page)
    with open(index, "w") as f:
        f.write(page)


if __name__ == "__main__":
    try:
        main()
    except BuildError as e:
        with open(CACHE_FILE, "w") as f:
            json.dump(CACHE, f)
        print("BUILD FAILED:", e, file=sys.stderr)
        sys.exit(1)
