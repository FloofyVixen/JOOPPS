"""Helpers for workshop pages. Every step solution and task solution is
compiled and run by build.py, so nothing here is unchecked."""
from tasks_classes import task  # noqa: F401  (re-exported for workshop files)


def step(title, text, files, run, output, hint=None, checks=()):
    return {"title": title, "text": text, "files": list(files), "solution": files,
            "run": run, "output": output, "hint": hint, "checks": list(checks)}


def guided(id, title, goal, steps):
    names = []
    for s in steps:
        for n in s["files"]:
            if n not in names:
                names.append(n)
    return {"type": "write", "id": id, "mode": "guided", "title": title, "goal": goal,
            "files": names, "steps": steps}


INTRO = ("Two guided tasks build a program one step at a time; a step is done when your output matches, "
         "and your code carries over to the next step. Then two independent tasks give you only the goal, "
         "the expected output and a test file. Create every file yourself with **New file**.")


def workshop(id, title, summary, goals, g1, g2, i1, i2, sources, cos225=None):
    blocks = [
        {"type": "h", "text": "How this workshop works"},
        {"type": "p", "text": INTRO},
        {"type": "h", "text": "Guided 1: " + g1["title"]}, g1,
        {"type": "h", "text": "Guided 2: " + g2["title"]}, g2,
        {"type": "h", "text": "Independent 1: " + i1["title"]}, i1,
        {"type": "h", "text": "Independent 2: " + i2["title"]}, i2,
    ]
    d = {"id": id, "title": title, "summary": summary, "goals": goals, "blocks": blocks, "sources": sources}
    if cos225:
        d["cos225"] = cos225
    return d
