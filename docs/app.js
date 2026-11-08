(function () {
  "use strict";

  var C = window.COURSE;
  var main = document.getElementById("main");
  var sidebar = document.getElementById("sidebar");

  // ---------- small helpers ----------
  var store = {
    get: function (key, fallback) {
      try {
        var v = window.localStorage.getItem("jos:" + key);
        return v === null ? fallback : JSON.parse(v);
      } catch (e) { return fallback; }
    },
    set: function (key, value) {
      try { window.localStorage.setItem("jos:" + key, JSON.stringify(value)); } catch (e) { /* storage unavailable */ }
    }
  };

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function el(tag, attrs, html) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") node.className = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    if (html !== undefined) node.innerHTML = html;
    return node;
  }

  // Same rules as norm() in build.py: collapse spaces, ignore spaces next to symbols.
  function norm(s, exact) {
    s = String(s).trim();
    if (exact) return s;
    s = s.replace(/\s+/g, " ");
    s = s.replace(/ ?([^A-Za-z0-9_ ]) ?/g, "$1");
    return s;
  }

  var ORDER = [];
  C.sections.forEach(function (s) {
    (s.lessons || []).forEach(function (id) { if (C.lessons[id]) ORDER.push(id); });
  });

  function sectionOf(id) {
    for (var i = 0; i < C.sections.length; i++) {
      if ((C.sections[i].lessons || []).indexOf(id) !== -1) return C.sections[i];
    }
    return null;
  }

  function finished() { return store.get("finished", []); }

  // ---------- code rendering ----------
  function highlight(code) {
    if (window.Prism && window.Prism.languages && window.Prism.languages.java) {
      try { return window.Prism.highlight(code, window.Prism.languages.java, "java"); } catch (e) { /* fall back */ }
    }
    return esc(code);
  }

  function linesHtml(html) {
    var lines = html.replace(/\n$/, "").split("\n");
    return lines.map(function (line, i) {
      return '<span class="ln" data-n="' + (i + 1) + '">' + (line || " ") + "</span>";
    }).join("");
  }

  // Renders one .java file. With `blanks`, [[id]] markers become text inputs.
  function codeFile(name, src, blanks, exId) {
    var wrap = el("div", { "class": "codefile" });
    var bar = el("div", { "class": "filename" }, "<span>" + esc(name) + "</span>");
    wrap.appendChild(bar);
    var counter = 0;
    var prepared = src.replace(/\[\[(\w+)\]\]/g, function (_, id) { return "__BLANK_" + id + "__"; });
    var html = linesHtml(highlight(prepared));
    html = html.replace(/__BLANK_(\w+?)__/g, function (_, id) {
      counter += 1;
      var spec = blanks && blanks[id];
      var w = Math.max(4, (spec ? spec.width : 6) + 2);
      return '<input class="blank" type="text" data-blank="' + esc(id) + '" id="' + esc(exId + "-" + id) +
        '" style="width:' + w + 'ch" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="Blank in ' +
        esc(name) + '">';
    });
    var pre = el("pre", null, "<code>" + html + "</code>");
    wrap.appendChild(pre);
    if (!blanks) {
      var copy = el("button", { "class": "btn quiet", type: "button" }, "Copy");
      copy.addEventListener("click", function () { copyText(src, copy); });
      bar.appendChild(copy);
    }
    return wrap;
  }

  function snippet(code) {
    var wrap = el("div", { "class": "codefile snippet" });
    wrap.appendChild(el("pre", null, "<code>" + highlight(code) + "</code>"));
    return wrap;
  }

  function copyText(text, button) {
    var original = button.textContent;
    function done(msg) {
      button.textContent = msg;
      setTimeout(function () { button.textContent = original; }, 1800);
    }
    try {
      navigator.clipboard.writeText(text).then(function () { done("Copied"); }, function () { done("Copy failed"); });
    } catch (e) { done("Copy failed"); }
  }

  function javacCommand(fileNames) {
    return "javac " + fileNames.slice().sort().join(" ");
  }

  // A terminal panel showing what javac and java really printed.
  function terminal(result, fileNames, label) {
    var parts = [];
    var title;
    if (result.kind === "compile") {
      title = label || "Compiler output";
      parts.push('<span class="cmd">' + esc(result.command || javacCommand(fileNames)) + "</span>");
      parts.push('<span class="err">' + esc(result.text) + "</span>");
    } else {
      title = label || (result.kind === "runtime" ? "Output: the program crashed" : "Output");
      parts.push('<span class="cmd">' + esc(javacCommand(fileNames)) + "</span>");
      if (result.command) parts.push('<span class="cmd">' + esc(result.command) + "</span>");
      if (result.stdout) parts.push(esc(result.stdout));
      if (result.kind === "runtime") parts.push('<span class="err">' + esc(result.text) + "</span>");
      if (result.kind === "ok" && !result.stdout) parts.push('<span class="quiet">(no output)</span>');
    }
    var t = el("div", { "class": "terminal" });
    t.appendChild(el("div", { "class": "bar" }, esc(title)));
    t.appendChild(el("pre", null, parts.join("\n")));
    return t;
  }

  function terminalSteps(steps) {
    var t = el("div", { "class": "terminal" });
    t.appendChild(el("div", { "class": "bar" }, "Terminal"));
    var parts = [];
    steps.forEach(function (s) {
      parts.push('<span class="cmd">' + esc(s.command) + "</span>");
      if (s.output) parts.push(s.code === 0 ? esc(s.output) : '<span class="err">' + esc(s.output) + "</span>");
    });
    t.appendChild(el("pre", null, parts.join("\n")));
    return t;
  }

  function plainOutput(text, label) {
    var t = el("div", { "class": "terminal" });
    t.appendChild(el("div", { "class": "bar" }, esc(label)));
    t.appendChild(el("pre", null, esc(text)));
    return t;
  }

  function names(files) { return files.map(function (f) { return f[0]; }); }

  function rawTerminal(text, command, isErr) {
    var t = el("div", { "class": "terminal" });
    t.appendChild(el("div", { "class": "bar" }, "Compiler output"));
    t.appendChild(el("pre", null, '<span class="cmd">' + esc(command) + "</span>\n" +
      (isErr ? '<span class="err">' + esc(text) + "</span>" : esc(text))));
    return t;
  }

  window.CourseUtil = {
    esc: esc, el: el, store: store, plain: plainOutput, codeFile: codeFile,
    copyText: copyText, rawTerminal: rawTerminal
  };

  // ---------- blocks ----------
  function renderBlock(b) {
    var frag = document.createDocumentFragment();
    switch (b.type) {
      case "h": frag.appendChild(el("h2", null, b.html)); break;
      case "p": frag.appendChild(el("p", null, b.html)); break;
      case "list":
        var ul = el("ul");
        b.items.forEach(function (it) { ul.appendChild(el("li", null, it)); });
        frag.appendChild(ul);
        break;
      case "note":
        frag.appendChild(el("div", { "class": "note" }, "<strong>" + esc(b.label) + "</strong>" + b.html));
        break;
      case "snippet":
        frag.appendChild(snippet(b.code));
        if (b.caption) frag.appendChild(el("p", { "class": "caption" }, b.caption));
        break;
      case "terminal":
        frag.appendChild(terminalSteps(b.steps));
        if (b.caption) frag.appendChild(el("p", { "class": "caption" }, b.caption));
        break;
      case "code":
        var holder = frag;
        if (b.collapsed) {
          var det = el("details", { "class": "solution" });
          det.appendChild(el("summary", null, b.caption || "Show code"));
          frag.appendChild(det);
          holder = det;
        }
        b.files.forEach(function (f) { holder.appendChild(codeFile(f[0], f[1])); });
        if (b.caption && !b.collapsed) holder.appendChild(el("p", { "class": "caption" }, b.caption));
        if (b.showResult) holder.appendChild(terminal(b.result, names(b.files)));
        if (b.after) holder.appendChild(el("p", { "class": "after" }, b.after));
        break;
      case "blanks": frag.appendChild(blanksExercise(b)); break;
      case "predict": frag.appendChild(choiceExercise(b, "Predict the output")); break;
      case "error": frag.appendChild(choiceExercise(b, "Read the error")); break;
      case "quiz": frag.appendChild(choiceExercise(b, "Check your understanding")); break;
      case "write": frag.appendChild(window.WriteTask.render(b)); break;
    }
    return frag;
  }

  function exerciseShell(kind, title, promptHtml) {
    var box = el("section", { "class": "exercise" });
    box.appendChild(el("p", { "class": "kind" }, esc(kind)));
    if (title) box.appendChild(el("h3", null, esc(title)));
    if (promptHtml) box.appendChild(el("p", null, promptHtml));
    return box;
  }

  function blanksExercise(ex) {
    var box = exerciseShell("Fill in the blanks", ex.title, ex.prompt);
    ex.files.forEach(function (f) { box.appendChild(codeFile(f[0], f[1], ex.blanks, ex.id)); });
    var inputs = Array.prototype.slice.call(box.querySelectorAll("input.blank"));
    var saved = store.get("ex:" + ex.id, {});
    inputs.forEach(function (inp, i) {
      inp.setAttribute("aria-label", "Blank " + (i + 1) + " of " + inputs.length);
      if (saved[inp.dataset.blank] !== undefined) inp.value = saved[inp.dataset.blank];
      inp.addEventListener("input", function () {
        inp.classList.remove("is-right", "is-wrong");
        var vals = store.get("ex:" + ex.id, {});
        vals[inp.dataset.blank] = inp.value;
        store.set("ex:" + ex.id, vals);
      });
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); check(); } });
    });

    var actions = el("div", { "class": "actions" });
    var checkBtn = el("button", { "class": "btn primary", type: "button" }, "Check");
    var hintBtn = el("button", { "class": "btn", type: "button" }, "Hint");
    var answerBtn = el("button", { "class": "btn", type: "button" }, "Show answer");
    var copyBtn = el("button", { "class": "btn quiet", type: "button" }, "Copy my code");
    [checkBtn, hintBtn, answerBtn, copyBtn].forEach(function (b) { actions.appendChild(b); });
    box.appendChild(actions);
    var hintBox = el("div");
    box.appendChild(hintBox);
    var fb = el("div", { "class": "feedback", "aria-live": "polite" });
    box.appendChild(fb);

    function filledFiles(useSolution) {
      return ex.files.map(function (f) {
        var src = f[1].replace(/\[\[(\w+)\]\]/g, function (_, id) {
          if (useSolution) return ex.blanks[id].solution;
          var inp = box.querySelector('input[data-blank="' + id + '"]');
          return inp ? inp.value : "";
        });
        return [f[0], src];
      });
    }

    function firstProblem(states) {
      for (var i = 0; i < states.length; i++) if (states[i].state !== "right") return i;
      return -1;
    }

    function evaluate() {
      return inputs.map(function (inp, i) {
        var spec = ex.blanks[inp.dataset.blank];
        var n = norm(inp.value, spec.exact);
        if (spec.accept.indexOf(n) !== -1) return { i: i, inp: inp, state: "right" };
        for (var k = 0; k < spec.wrong.length; k++) {
          if (spec.wrong[k].answer === n) return { i: i, inp: inp, state: "known", wrong: spec.wrong[k] };
        }
        if (inp.value.trim() === "") return { i: i, inp: inp, state: "empty" };
        return { i: i, inp: inp, state: "unknown", spec: spec };
      });
    }

    function showSuccess(revealed) {
      fb.innerHTML = "";
      var b = el("div", { "class": "box ok" });
      b.appendChild(el("p", { "class": "verdict ok" }, revealed ? "Here is the answer." : "Correct."));
      b.appendChild(terminal(ex.result, names(ex.files)));
      if (ex.explain) b.appendChild(el("p", null, ex.explain));
      fb.appendChild(b);
    }

    function check() {
      hintBox.innerHTML = "";
      var states = evaluate();
      states.forEach(function (s) {
        s.inp.classList.remove("is-right", "is-wrong");
        s.inp.removeAttribute("aria-invalid");
        if (s.state === "right") s.inp.classList.add("is-right");
        else if (s.state !== "empty") { s.inp.classList.add("is-wrong"); s.inp.setAttribute("aria-invalid", "true"); }
      });
      var idx = firstProblem(states);
      if (idx === -1) { showSuccess(false); return; }
      var p = states[idx];
      var label = "Blank " + (p.i + 1);
      var rightCount = states.filter(function (s) { return s.state === "right"; }).length;
      fb.innerHTML = "";
      var b = el("div", { "class": "box bad" });
      b.appendChild(el("p", { "class": "verdict bad" }, rightCount + " of " + states.length + " blanks are right."));
      if (p.state === "empty") {
        b.appendChild(el("p", null, label + " is empty. Fill it in, then check again."));
      } else if (p.state === "known") {
        var r = p.wrong.result;
        var shown = p.wrong.shown === "" ? "nothing" : "<code>" + esc(p.wrong.shown) + "</code>";
        if (r.kind === "ok") {
          b.appendChild(el("p", null, "With " + shown + " in " + label.toLowerCase() + ", the program compiles and runs, but prints something different:"));
          b.appendChild(plainOutput(r.stdout || "(no output)", "Your output"));
          b.appendChild(plainOutput(ex.result.stdout, "Expected output"));
        } else {
          b.appendChild(el("p", null, "This is what Java really prints with " + shown + " in " + label.toLowerCase() +
            " and the other blanks filled in correctly:"));
          b.appendChild(terminal(r, names(ex.files)));
        }
        b.appendChild(el("p", null, p.wrong.why));
      } else {
        b.appendChild(el("p", null, label + " isn't right yet. This exact answer hasn't been run through the compiler, so there's no real Java message to show for it."));
        if (p.spec.hint) b.appendChild(el("p", null, "<strong>Hint:</strong> " + p.spec.hint));
        b.appendChild(el("p", null, "To see what Java says about your version, use <strong>Copy my code</strong> and run it in VS Code."));
      }
      fb.appendChild(b);
    }

    checkBtn.addEventListener("click", check);
    hintBtn.addEventListener("click", function () {
      var states = evaluate();
      var idx = firstProblem(states);
      var target = idx === -1 ? states[0] : states[idx];
      var spec = ex.blanks[target.inp.dataset.blank];
      hintBox.innerHTML = "";
      hintBox.appendChild(el("div", { "class": "hint" }, "<strong>Blank " + (target.i + 1) + ":</strong> " +
        (spec.hint || "Read the lesson text above this exercise again.")));
      target.inp.focus();
    });
    answerBtn.addEventListener("click", function () {
      inputs.forEach(function (inp) {
        inp.value = ex.blanks[inp.dataset.blank].solution;
        inp.classList.remove("is-wrong");
        inp.classList.add("is-right");
      });
      hintBox.innerHTML = "";
      showSuccess(true);
    });
    copyBtn.addEventListener("click", function () {
      var text = filledFiles(false).map(function (f) {
        return "// ===== " + f[0] + " =====\n" + f[1];
      }).join("\n");
      copyText(text, copyBtn);
    });
    return box;
  }

  function choiceExercise(ex, kind) {
    var box = exerciseShell(kind, null, ex.prompt || null);
    if (ex.files) ex.files.forEach(function (f) { box.appendChild(codeFile(f[0], f[1])); });
    if (ex.type === "error") box.appendChild(terminal(ex.result, names(ex.files)));
    var fs = el("fieldset");
    var question = ex.type === "predict" ? "Choose the exact output." : ex.question;
    fs.appendChild(el("legend", null, question));
    var name = "q-" + ex.id;
    ex.choices.forEach(function (c, i) {
      var lab = el("label", { "class": "choice" });
      var radio = el("input", { type: "radio", name: name, value: String(i), id: name + "-" + i });
      lab.appendChild(radio);
      lab.appendChild(ex.type === "predict" ? el("pre", null, esc(c)) : el("span", null, c));
      fs.appendChild(lab);
    });
    box.appendChild(fs);
    var actions = el("div", { "class": "actions" });
    var checkBtn = el("button", { "class": "btn primary", type: "button" }, "Check");
    actions.appendChild(checkBtn);
    box.appendChild(actions);
    var fb = el("div", { "class": "feedback", "aria-live": "polite" });
    box.appendChild(fb);

    checkBtn.addEventListener("click", function () {
      var picked = box.querySelector('input[name="' + name + '"]:checked');
      fb.innerHTML = "";
      if (!picked) {
        fb.appendChild(el("p", null, "Pick an answer first."));
        return;
      }
      var right = Number(picked.value) === ex.answer;
      Array.prototype.forEach.call(fs.querySelectorAll(".choice"), function (lab, i) {
        lab.classList.toggle("is-answer", i === ex.answer);
      });
      var b = el("div", { "class": "box " + (right ? "ok" : "bad") });
      b.appendChild(el("p", { "class": "verdict " + (right ? "ok" : "bad") },
        right ? "Correct." : "Not quite. The right answer is outlined in green."));
      if (ex.type === "predict") {
        b.appendChild(el("p", null, "This is the program's real output:"));
        b.appendChild(terminal(ex.result, names(ex.files)));
      }
      b.appendChild(el("p", null, ex.explain));
      if (ex.type === "error") {
        var original = {};
        ex.files.forEach(function (f) { original[f[0]] = f[1]; });
        var changed = ex.fixedFiles.filter(function (f) { return original[f[0]] !== f[1]; });
        b.appendChild(el("p", null, "<strong>The fixed version</strong>"));
        changed.forEach(function (f) { b.appendChild(codeFile(f[0], f[1])); });
        b.appendChild(terminal(ex.fixedResult, names(ex.fixedFiles)));
      }
      fb.appendChild(b);
    });
    return box;
  }

  // ---------- pages ----------
  function renderSidebar(currentId) {
    var done = finished();
    var html = '<a class="home-link" href="#start"' + (currentId ? "" : ' aria-current="page"') + ">Course home</a>";
    C.sections.forEach(function (s, n) {
      html += "<h2>" + (n + 1) + ". " + esc(s.title) + "</h2>";
      if (s.lessons && s.lessons.length) {
        html += "<ol>";
        s.lessons.forEach(function (id) {
          var L = C.lessons[id];
          if (!L) return;
          var isDone = done.indexOf(id) !== -1;
          html += '<li><a href="#' + id + '"' + (id === currentId ? ' aria-current="page"' : "") + ">" +
            esc(L.title) + (isDone ? '<span class="done" aria-label="finished">✓</span>' : "") + "</a></li>";
        });
        html += "</ol>";
      } else {
        html += '<p class="planned">Planned</p>';
      }
    });
    sidebar.innerHTML = html;
  }

  function renderHome() {
    document.title = C.title;
    var page = el("div", { "class": "page home" });
    var lessonCount = ORDER.length;
    page.innerHTML =
      "<h1>Java objects, one step at a time</h1>" +
      '<p class="lead">A free course on object-oriented programming in Java for people with little or no experience. ' +
      "Short explanations, real programs, and fill-in-the-blank practice that shows you the same error messages you'll see in VS Code's terminal.</p>" +
      '<p><a class="btn primary" href="#' + ORDER[0] + '">Start with lesson 1</a></p>' +
      '<div class="facts">' +
      "<div><h2>Follows COS 225</h2><p>The " + C.sections.length + " units follow the path of UMaine's COS 225 (Object-Oriented Design, Programming and Data Structures), from Introduction to Java to Introduction to Hashing. Where its materials aren't public, the University of Helsinki's Java MOOC and similar courses fill the gaps.</p></div>" +
      "<div><h2>Practice, not answers</h2><p>The projects have the same shape as COS 225 homework, with different subjects. Do the lesson, then write your assignment yourself.</p></div>" +
      "<div><h2>Every program is real</h2><p>All " + "code on this site was compiled and run with OpenJDK " + esc(C.java) + " on " + esc(C.built) +
      ". Every output and error message shown is exactly what Java printed. Each lesson lists the official documentation and university courses its explanations rely on.</p></div>" +
      "<div><h2>Not yet reviewed</h2><p>No instructor has reviewed this material yet. If something looks wrong, trust the linked sources and your instructor over this site.</p></div>" +
      "</div>" +
      "<h2>What's in the course</h2>" +
      "<p>" + lessonCount + " lessons are ready. The rest of the outline is planned and will be added unit by unit.</p>";
    var ol = el("ol", { "class": "outline" });
    C.sections.forEach(function (s, i) {
      var li = el("li");
      var inner = '<span class="num">' + (i + 1) + '</span><div><h3>' + esc(s.title) + "</h3><p>" + esc(s.blurb) + "</p>";
      var ready = (s.lessons || []).filter(function (id) { return C.lessons[id]; });
      if (!ready.length) inner += '<p class="status">Planned</p>';
      inner += "<ol>" + ready.map(function (id) {
        return '<li><a href="#' + id + '">' + esc(C.lessons[id].title) + "</a></li>";
      }).join("") + (s.planned || []).map(function (t) {
        return '<li class="soon">' + esc(t) + (ready.length ? " (planned)" : "") + "</li>";
      }).join("") + "</ol>";
      li.innerHTML = inner + "</div>";
      ol.appendChild(li);
    });
    page.appendChild(ol);
    main.innerHTML = "";
    main.appendChild(page);
  }

  function renderLesson(id) {
    var L = C.lessons[id];
    var s = sectionOf(id);
    var inSection = s.lessons.filter(function (x) { return C.lessons[x]; });
    document.title = L.title + " · " + C.title;
    var page = el("article", { "class": "page" });
    page.appendChild(el("p", { "class": "crumb" }, '<a href="#start">Course</a> / ' + esc(s.title) +
      " / Lesson " + (inSection.indexOf(id) + 1) + " of " + inSection.length));
    page.appendChild(el("h1", null, esc(L.title)));
    page.appendChild(el("p", { "class": "summary" }, L.summary));
    if (L.goals && L.goals.length) {
      var g = el("div", { "class": "goals" });
      g.appendChild(el("h2", null, "In this lesson"));
      var ul = el("ul");
      L.goals.forEach(function (x) { ul.appendChild(el("li", null, x)); });
      g.appendChild(ul);
      page.appendChild(g);
    }
    if (L.cos225) page.appendChild(el("div", { "class": "cos" }, "<strong>How this connects to COS 225</strong>" + L.cos225));
    L.blocks.forEach(function (b) { page.appendChild(renderBlock(b)); });

    var src = el("section", { "class": "sources" });
    src.appendChild(el("h2", null, "Sources for this lesson"));
    var sl = el("ul");
    L.sources.forEach(function (x) {
      sl.appendChild(el("li", null, '<a href="' + esc(x.url) + '">' + esc(x.title) + '</a> <span class="org">' + esc(x.org) + "</span>" +
        (x.note ? '<span class="why">' + x.note + "</span>" : "")));
    });
    src.appendChild(sl);
    page.appendChild(src);

    var row = el("div", { "class": "complete-row" });
    var doneBtn = el("button", { "class": "btn", type: "button" });
    function paint() {
      var isDone = finished().indexOf(id) !== -1;
      doneBtn.textContent = isDone ? "Finished ✓ (click to undo)" : "Mark this lesson as finished";
      doneBtn.setAttribute("aria-pressed", isDone ? "true" : "false");
    }
    doneBtn.addEventListener("click", function () {
      var list = finished();
      var at = list.indexOf(id);
      if (at === -1) list.push(id); else list.splice(at, 1);
      store.set("finished", list);
      paint();
      renderSidebar(id);
    });
    paint();
    row.appendChild(doneBtn);
    page.appendChild(row);

    var i = ORDER.indexOf(id);
    var pager = el("nav", { "class": "pager", "aria-label": "Lesson navigation" });
    if (i > 0) pager.appendChild(el("a", { href: "#" + ORDER[i - 1] }, '<span class="dir">Previous</span>' + esc(C.lessons[ORDER[i - 1]].title)));
    if (i < ORDER.length - 1) pager.appendChild(el("a", { href: "#" + ORDER[i + 1], "class": "next" }, '<span class="dir">Next</span>' + esc(C.lessons[ORDER[i + 1]].title)));
    page.appendChild(pager);
    page.appendChild(el("p", { "class": "report" }, "Spotted a mistake? Note the lesson title and which exercise, and tell whoever shared this course with you."));

    main.innerHTML = "";
    main.appendChild(page);
  }

  function route() {
    var id = window.location.hash.replace(/^#/, "");
    sidebar.classList.remove("open");
    document.getElementById("menu-btn").setAttribute("aria-expanded", "false");
    if (C.lessons[id]) {
      renderSidebar(id);
      renderLesson(id);
    } else {
      renderSidebar(null);
      renderHome();
    }
    window.scrollTo(0, 0);
    main.focus({ preventScroll: true });
  }

  // ---------- theme ----------
  var themeBtn = document.getElementById("theme-btn");
  var THEMES = ["system", "light", "dark"];
  var hostTheme = document.documentElement.getAttribute("data-theme");
  function applyTheme(t) {
    if (t !== "system") document.documentElement.setAttribute("data-theme", t);
    else if (hostTheme) document.documentElement.setAttribute("data-theme", hostTheme);
    else document.documentElement.removeAttribute("data-theme");
    document.getElementById("theme-val").textContent = t.charAt(0).toUpperCase() + t.slice(1);
  }
  var theme = store.get("theme", "system");
  if (THEMES.indexOf(theme) === -1) theme = "system";
  applyTheme(theme);
  themeBtn.addEventListener("click", function () {
    theme = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
    store.set("theme", theme);
    applyTheme(theme);
  });

  var menuBtn = document.getElementById("menu-btn");
  menuBtn.addEventListener("click", function () {
    var open = sidebar.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  var skip = document.querySelector(".skip");
  if (skip) skip.addEventListener("click", function (e) { e.preventDefault(); main.focus(); });

  window.addEventListener("hashchange", route);
  route();
})();
