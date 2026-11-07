/* Write-it-yourself editor: file tabs, a code area, and a Run button that
   compiles with the real javac (JDK 21) and runs with Java 21 inside the
   browser, using CheerpJ. Exposes window.WriteTask.render(task). */
(function () {
  "use strict";

  var U, esc, el, store; // bound from window.CourseUtil when the first task renders
  function bind() { U = window.CourseUtil; esc = U.esc; el = U.el; store = U.store; }

  // ---------- Java runner (CheerpJ) ----------
  var Runner = (function () {
    var initPromise = null;
    var runCount = 0;
    var busy = false;

    function available() { return typeof window.cheerpjInit === "function"; }

    function basePath() { return window.location.pathname.replace(/[^/]*$/, ""); }
    function javacJar() { return "/app" + basePath() + "javac/javac21.jar"; }

    function init(onStatus) {
      if (!initPromise) {
        onStatus("Starting Java. The first run downloads the Java runtime, which can take a minute.");
        initPromise = window.cheerpjInit({ version: 21, status: "none" });
      }
      return initPromise;
    }

    function consoleEl() { return document.getElementById("console"); }

    function settle() { return new Promise(function (r) { setTimeout(r, 30); }); }

    async function capture(fn) {
      var c = consoleEl();
      c.textContent = "";
      var code = await fn();
      await settle();
      return { code: code, text: c.textContent.replace(/\n+$/, "") };
    }

    function write(path, text) {
      window.cheerpjAddStringFile(path, new TextEncoder().encode(text));
    }

    // Compile `files` ([[name, src]...]) into outDir. `extraCp` lets test files see the learner's classes.
    async function javac(srcDir, outDir, files, extraCp) {
      files.forEach(function (f) { write(srcDir + f[0], f[1]); });
      var args = ["com.sun.tools.javac.Main", javacJar(), "-d", outDir];
      if (extraCp) args.push("-cp", extraCp);
      files.forEach(function (f) { args.push(srcDir + f[0]); });
      var r = await capture(function () { return window.cheerpjRunMain.apply(null, args); });
      r.text = r.text.split(srcDir).join("");
      return r;
    }

    async function java(mainClass, outDir) {
      return capture(function () { return window.cheerpjRunMain(mainClass, outDir); });
    }

    function newRun() {
      runCount += 1;
      var id = "run" + Date.now().toString(36) + runCount;
      return { src: "/str/" + id + "/", testSrc: "/str/" + id + "t/", out: "/files/" + id + "/" };
    }

    return {
      available: available, init: init, javac: javac, java: java, newRun: newRun,
      isBusy: function () { return busy; }, setBusy: function (b) { busy = b; }
    };
  })();

  // ---------- helpers ----------
  function stripComments(src) {
    return src.replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/[^\n]*/g, "");
  }

  function normOut(s) {
    return String(s).split("\n").map(function (l) { return l.replace(/\s+$/, ""); }).join("\n").replace(/\n+$/, "");
  }

  function validName(name) { return /^[A-Za-z_$][A-Za-z0-9_$]*\.java$/.test(name); }

  function diffView(expected, actual) {
    var e = expected.split("\n"), a = actual.split("\n");
    var first = -1;
    for (var i = 0; i < Math.max(e.length, a.length); i++) {
      if (e[i] !== a[i]) { first = i; break; }
    }
    var wrap = el("div", { "class": "diff" });
    function col(title, lines) {
      var c = el("div", { "class": "terminal" });
      c.appendChild(el("div", { "class": "bar" }, esc(title)));
      var html = lines.map(function (l, i) {
        var cls = i === first ? ' class="diffline"' : "";
        return "<span" + cls + ">" + (esc(l) || " ") + "</span>";
      }).join("\n");
      c.appendChild(el("pre", null, html));
      return c;
    }
    wrap.appendChild(col("Expected output", e));
    wrap.appendChild(col("Your output", actual === "" ? ["(no output)"] : a));
    var note = first === -1 ? "" : "The first difference is on line " + (first + 1) + " of the output" +
      (e[first] !== undefined && a[first] !== undefined && e[first].trim() === a[first].trim() ? " (check the spaces)." : ".");
    return { node: wrap, note: note };
  }

  // ---------- the task widget ----------
  function render(task) {
    bind();
    var key = "write:" + task.id;
    var guided = task.mode === "guided";
    var testsByName = {};
    task.tests.forEach(function (t) { testsByName[t[0]] = t[1]; });

    function initialState() {
      var files = {}, order = [];
      task.starter.forEach(function (f) { files[f[0]] = f[1]; order.push(f[0]); });
      return { files: files, order: order, active: order[0] || null, step: 0, done: false, stepsDone: [] };
    }
    var state = store.get(key, null) || initialState();
    if (!state.files) state = initialState();
    function save() { store.set(key, state); }

    var box = el("section", { "class": "exercise write" });
    box.appendChild(el("p", { "class": "kind" }, guided ? "Write it yourself: guided" : "Write it yourself: independent"));
    box.appendChild(el("h3", null, esc(task.title)));
    box.appendChild(el("p", null, task.goal));

    // guided steps
    var stepsBox = null;
    function current() {
      if (!guided) return { files: task.files, run: task.run, output: task.output, checks: task.checks, solution: task.solution };
      return task.steps[Math.min(state.step, task.steps.length - 1)];
    }
    if (guided) {
      stepsBox = el("ol", { "class": "steps" });
      box.appendChild(stepsBox);
    }
    function paintSteps() {
      if (!guided) return;
      stepsBox.innerHTML = "";
      task.steps.forEach(function (s, i) {
        var status = i < state.step || (state.done && i === state.step) ? "done" : i === state.step ? "current" : "locked";
        var li = el("li", { "class": "step " + status });
        var label = status === "done" ? "Done" : status === "current" ? "Current step" : "Locked";
        li.innerHTML = '<p class="step-title"><span>' + esc(s.title) + '</span> <span class="step-status">' + label + "</span></p>";
        if (status === "current") {
          li.appendChild(el("p", null, s.text));
          li.appendChild(el("p", { "class": "step-expect" }, "When you run it, the output should be:"));
          li.appendChild(U.plain(s.output, "Expected output"));
          if (s.hint) {
            var hb = el("button", { "class": "btn quiet", type: "button" }, "Show a hint");
            var hint = el("div", { "class": "hint", hidden: "" }, s.hint);
            hb.addEventListener("click", function () { hint.hidden = !hint.hidden; });
            li.appendChild(hb);
            li.appendChild(hint);
          }
        }
        stepsBox.appendChild(li);
      });
    }

    if (!guided) {
      if (task.requirements.length) {
        var req = el("div", { "class": "reqs" });
        req.appendChild(el("p", { "class": "reqs-title" }, "Requirements"));
        var ul = el("ul");
        task.requirements.forEach(function (r) { ul.appendChild(el("li", null, r)); });
        req.appendChild(ul);
        box.appendChild(req);
      }
      box.appendChild(U.plain(task.output, "Expected output"));
    }

    // ---------- IDE ----------
    var ide = el("div", { "class": "ide" });
    var tabs = el("div", { "class": "tabs", role: "tablist", "aria-label": "Files" });
    var newForm = el("form", { "class": "newfile", hidden: "" });
    var nameId = "nf-" + task.id;
    newForm.innerHTML = '<label for="' + nameId + '">File name</label>' +
      '<input id="' + nameId + '" type="text" autocomplete="off" spellcheck="false" placeholder="Example.java">' +
      '<button class="btn primary" type="submit">Create</button><button class="btn quiet" type="button" data-cancel>Cancel</button>' +
      '<p class="nf-error" aria-live="polite"></p>';
    var area = el("div", { "class": "editor-area" });
    var gutter = el("pre", { "class": "gutter", "aria-hidden": "true" });
    var taId = "ta-" + task.id;
    var ta = el("textarea", { id: taId, spellcheck: "false", autocapitalize: "off", autocomplete: "off", wrap: "off" });
    var empty = el("div", { "class": "ide-empty" });
    area.appendChild(gutter);
    area.appendChild(ta);
    var bar = el("div", { "class": "ide-bar" });
    var runBtn = el("button", { "class": "btn primary", type: "button" }, "Run");
    var solBtn = el("button", { "class": "btn", type: "button" }, "Show solution");
    var resetBtn = el("button", { "class": "btn quiet", type: "button" }, "Start over");
    var copyBtn = el("button", { "class": "btn quiet", type: "button" }, "Copy all files");
    var status = el("span", { "class": "ide-status", "aria-live": "polite" });
    [runBtn, solBtn, resetBtn, copyBtn, status].forEach(function (n) { bar.appendChild(n); });
    var keysNote = el("p", { "class": "ide-keys" }, "In the editor, Tab inserts four spaces. Press Esc, then Tab, to move on to the next button.");
    ide.appendChild(tabs);
    ide.appendChild(newForm);
    ide.appendChild(empty);
    ide.appendChild(area);
    ide.appendChild(keysNote);
    ide.appendChild(bar);
    box.appendChild(ide);
    var out = el("div", { "class": "run-output", "aria-live": "polite" });
    box.appendChild(out);
    var solBox = el("div", { "class": "solution-box" });
    box.appendChild(solBox);

    function isTest(name) { return Object.prototype.hasOwnProperty.call(testsByName, name); }
    function allNames() { return state.order.concat(task.tests.map(function (t) { return t[0]; })); }

    function paintTabs() {
      tabs.innerHTML = "";
      allNames().forEach(function (name) {
        var t = el("div", { "class": "tab" + (name === state.active ? " active" : "") + (isTest(name) ? " readonly" : "") });
        var b = el("button", { type: "button", role: "tab", "aria-selected": name === state.active ? "true" : "false" },
          esc(name) + (isTest(name) ? ' <span class="ro">test, read-only</span>' : ""));
        b.addEventListener("click", function () { state.active = name; save(); paint(); });
        t.appendChild(b);
        if (!isTest(name)) {
          var x = el("button", { type: "button", "class": "close", "aria-label": "Delete " + name }, "×");
          x.addEventListener("click", function () { confirmDelete(t, name); });
          t.appendChild(x);
        }
        tabs.appendChild(t);
      });
      var add = el("button", { type: "button", "class": "tab add" }, "+ New file");
      add.addEventListener("click", function () {
        newForm.hidden = false;
        newForm.querySelector(".nf-error").textContent = "";
        var inp = newForm.querySelector("input");
        inp.value = "";
        inp.focus();
      });
      tabs.appendChild(add);
    }

    function confirmDelete(tabNode, name) {
      tabNode.innerHTML = "";
      tabNode.classList.add("confirm");
      tabNode.appendChild(el("span", null, "Delete " + esc(name) + "?"));
      var yes = el("button", { type: "button", "class": "btn quiet" }, "Delete");
      var no = el("button", { type: "button", "class": "btn quiet" }, "Keep");
      yes.addEventListener("click", function () {
        delete state.files[name];
        state.order = state.order.filter(function (n) { return n !== name; });
        if (state.active === name) state.active = state.order[0] || (task.tests[0] ? task.tests[0][0] : null);
        save(); paint();
      });
      no.addEventListener("click", paint);
      tabNode.appendChild(yes);
      tabNode.appendChild(no);
      no.focus();
    }

    newForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var inp = newForm.querySelector("input");
      var err = newForm.querySelector(".nf-error");
      var name = inp.value.trim();
      if (name && !/\.java$/.test(name)) name += ".java";
      if (!validName(name)) {
        err.textContent = "Use a class name followed by .java, with letters and digits only, like Postcard.java.";
        return;
      }
      if (state.files[name] !== undefined || isTest(name)) {
        err.textContent = "There's already a file named " + name + ".";
        return;
      }
      state.files[name] = "";
      state.order.push(name);
      state.active = name;
      newForm.hidden = true;
      save(); paint();
      ta.focus();
    });
    newForm.querySelector("[data-cancel]").addEventListener("click", function () { newForm.hidden = true; });

    function paintGutter() {
      var n = ta.value.split("\n").length;
      var s = "";
      for (var i = 1; i <= n; i++) s += i + "\n";
      gutter.textContent = s;
      gutter.scrollTop = ta.scrollTop;
    }

    function paintEditor() {
      var name = state.active;
      if (!name) {
        area.hidden = true;
        keysNote.hidden = true;
        empty.hidden = false;
        var need = current().files.join(", ");
        empty.innerHTML = "<p>No files yet. Click <strong>+ New file</strong> and create <code>" + esc(need) + "</code>.</p>";
        return;
      }
      empty.hidden = true;
      area.hidden = false;
      keysNote.hidden = false;
      var ro = isTest(name);
      ta.readOnly = ro;
      ta.value = ro ? testsByName[name] : (state.files[name] || "");
      ta.setAttribute("aria-label", (ro ? "Read-only test file " : "Code editor for ") + name);
      area.classList.toggle("readonly", ro);
      paintGutter();
    }

    function paint() { paintSteps(); paintTabs(); paintEditor(); }

    ta.addEventListener("input", function () {
      if (!state.active || isTest(state.active)) return;
      state.files[state.active] = ta.value;
      save();
      paintGutter();
    });
    ta.addEventListener("scroll", function () { gutter.scrollTop = ta.scrollTop; });

    var escPressed = false;
    ta.addEventListener("keydown", function (e) {
      if (ta.readOnly) return;
      if (e.key === "Escape") { escPressed = true; return; }
      if (e.key === "Tab" && !escPressed && !e.shiftKey) {
        e.preventDefault();
        insert("    ");
        return;
      }
      escPressed = false;
      if (e.key === "Enter") {
        e.preventDefault();
        var before = ta.value.slice(0, ta.selectionStart);
        var line = before.slice(before.lastIndexOf("\n") + 1);
        var indent = (line.match(/^\s*/) || [""])[0];
        if (/\{\s*$/.test(line)) indent += "    ";
        insert("\n" + indent);
      } else if (e.key === "}") {
        var b2 = ta.value.slice(0, ta.selectionStart);
        var cur = b2.slice(b2.lastIndexOf("\n") + 1);
        if (/^ {4,}$/.test(cur) && ta.selectionStart === ta.selectionEnd) {
          e.preventDefault();
          ta.setSelectionRange(ta.selectionStart - 4, ta.selectionStart);
          insert("}");
        }
      }
    });
    ta.addEventListener("blur", function () { escPressed = false; });

    function insert(text) {
      var s = ta.selectionStart, e = ta.selectionEnd;
      ta.setRangeText(text, s, e, "end");
      ta.dispatchEvent(new Event("input"));
    }

    // ---------- run ----------
    function learnerFiles() {
      return state.order.map(function (n) { return [n, state.files[n] || ""]; });
    }

    function line(ok, html) {
      return el("li", { "class": ok ? "pass" : "fail" }, '<span class="mark" aria-hidden="true">' + (ok ? "✓" : "✗") + "</span> " +
        '<span class="sr">' + (ok ? "Passed: " : "Not yet: ") + "</span>" + html);
    }

    async function run() {
      if (Runner.isBusy()) return;
      out.innerHTML = "";
      solBox.innerHTML = "";
      var step = current();
      var missing = step.files.filter(function (n) { return state.files[n] === undefined; });
      if (missing.length) {
        out.appendChild(el("div", { "class": "box bad" }, "<p>This task needs a file named <code>" + esc(missing[0]) +
          "</code>. Create it with <strong>+ New file</strong>. File names have to match exactly, including capital letters.</p>"));
        return;
      }
      if (!Runner.available()) {
        out.appendChild(el("div", { "class": "box bad" }, "<p>Java can't run on this copy of the course. The Run button works on the published course site, which loads a Java runtime in your browser. You can still use <strong>Copy all files</strong> and run your code in VS Code.</p>"));
        return;
      }
      Runner.setBusy(true);
      runBtn.disabled = true;
      var slow = setTimeout(function () {
        status.textContent = "Still running. If your program has a loop that never ends, reload the page to stop it.";
      }, 15000);
      try {
        await Runner.init(function (msg) { status.textContent = msg; });
        status.textContent = "Compiling…";
        var dirs = Runner.newRun();
        var files = learnerFiles();
        var term = el("div", { "class": "terminal" });
        term.appendChild(el("div", { "class": "bar" }, "Terminal"));
        var pre = el("pre");
        term.appendChild(pre);
        out.appendChild(term);
        var html = '<span class="cmd">javac ' + esc(files.map(function (f) { return f[0]; }).join(" ")) + "</span>";
        pre.innerHTML = html;
        var c = await Runner.javac(dirs.src, dirs.out, files, null);
        if (c.text) html += "\n" + (c.code === 0 ? esc(c.text) : '<span class="err">' + esc(c.text) + "</span>");
        pre.innerHTML = html;
        var results = el("ul", { "class": "results" });
        if (c.code !== 0) {
          results.appendChild(line(false, "Your code doesn't compile yet. Read the first error above: it gives the file, the line number and the problem."));
          finish(results, false);
          return;
        }
        results.appendChild(line(true, "Compiles"));
        status.textContent = "Running…";
        html += '\n<span class="cmd">java ' + esc(step.run) + "</span>";
        pre.innerHTML = html;
        var r = await Runner.java(step.run, dirs.out);
        if (r.text) html += "\n" + (r.code === 0 ? esc(r.text) : '<span class="err">' + esc(r.text) + "</span>");
        pre.innerHTML = html;
        var allOk = true;
        if (r.code !== 0) {
          allOk = false;
          results.appendChild(line(false, "The program stopped with an error. Read the message above: the <code>at</code> lines show where it happened."));
        } else if (normOut(r.text) !== normOut(step.output)) {
          allOk = false;
          var d = diffView(normOut(step.output), normOut(r.text));
          var li = line(false, "The output doesn't match yet. " + esc(d.note));
          li.appendChild(d.node);
          results.appendChild(li);
        } else {
          results.appendChild(line(true, "Output matches"));
        }
        if (allOk && !guided && task.tests.length) {
          status.textContent = "Running the tests…";
          var tc = await Runner.javac(dirs.testSrc, dirs.out, task.tests, dirs.out);
          if (tc.code !== 0) {
            allOk = false;
            var tl = line(false, "The test file can't use your code. Usually this means a method or constructor is named differently from the task, or has different parameters. The compiler says:");
            tl.appendChild(U.rawTerminal(tc.text, "javac " + task.tests.map(function (t) { return t[0]; }).join(" "), true));
            results.appendChild(tl);
          } else {
            var tr = await Runner.java(task.testsRun, dirs.out);
            if (tr.code === 0 && normOut(tr.text) === normOut(task.testsOutput)) {
              results.appendChild(line(true, "Tests pass (<code>" + esc(task.testsRun) + "</code> tried more values)"));
            } else {
              allOk = false;
              var dd = diffView(normOut(task.testsOutput), normOut(tr.text));
              var fl = line(false, "Your <code>main</code> works, but the tests in <code>" + esc(task.tests[0][0]) + "</code> found a difference. " + esc(dd.note));
              fl.appendChild(dd.node);
              results.appendChild(fl);
            }
          }
        }
        var code = learnerFiles().map(function (f) { return stripComments(f[1]); }).join("\n");
        (step.checks || []).forEach(function (chk) {
          var ok = new RegExp(chk.pattern).test(code);
          if (!ok) allOk = false;
          results.appendChild(line(ok, chk.message));
        });
        finish(results, allOk);
      } catch (err) {
        out.appendChild(el("div", { "class": "box bad" }, "<p>The Java runtime ran into a problem in the browser (" + esc(err && err.message ? err.message : String(err)) + "). Reload the page and try again.</p>"));
      } finally {
        clearTimeout(slow);
        status.textContent = "";
        runBtn.disabled = false;
        Runner.setBusy(false);
      }
    }

    function finish(results, ok) {
      var b = el("div", { "class": "box " + (ok ? "ok" : "bad") });
      var msg;
      if (!ok) msg = "Not done yet.";
      else if (guided && state.step < task.steps.length - 1) msg = "Step " + (state.step + 1) + " done.";
      else msg = "Task complete.";
      b.appendChild(el("p", { "class": "verdict " + (ok ? "ok" : "bad") }, msg));
      b.appendChild(results);
      out.appendChild(b);
      if (ok) {
        if (guided && state.step < task.steps.length - 1) {
          var next = el("button", { "class": "btn primary", type: "button" }, "Next step");
          next.addEventListener("click", function () {
            state.step += 1; save(); out.innerHTML = ""; paint();
            stepsBox.querySelector(".step.current").scrollIntoView({ block: "nearest" });
          });
          b.appendChild(next);
        } else {
          state.done = true; save(); paintSteps();
        }
      }
    }

    runBtn.addEventListener("click", run);

    solBtn.addEventListener("click", function () {
      if (solBtn.dataset.armed !== "1") {
        solBtn.dataset.armed = "1";
        solBtn.textContent = "Show it anyway?";
        setTimeout(function () { solBtn.dataset.armed = ""; solBtn.textContent = "Show solution"; }, 4000);
        return;
      }
      solBtn.dataset.armed = "";
      solBtn.textContent = "Show solution";
      solBox.innerHTML = "";
      solBox.appendChild(el("p", { "class": "sol-title" }, guided ? "One way to write this step" : "One way to write it"));
      current().solution.forEach(function (f) { solBox.appendChild(U.codeFile(f[0], f[1])); });
      solBox.appendChild(el("p", { "class": "caption" }, "This solution was compiled and checked against the expected output. Yours can look different and still be right."));
    });

    resetBtn.addEventListener("click", function () {
      if (resetBtn.dataset.armed !== "1") {
        resetBtn.dataset.armed = "1";
        resetBtn.textContent = "Erase your files?";
        setTimeout(function () { resetBtn.dataset.armed = ""; resetBtn.textContent = "Start over"; }, 4000);
        return;
      }
      resetBtn.dataset.armed = "";
      resetBtn.textContent = "Start over";
      state = initialState(); save(); out.innerHTML = ""; solBox.innerHTML = ""; paint();
    });

    copyBtn.addEventListener("click", function () {
      var text = learnerFiles().map(function (f) { return "// ===== " + f[0] + " =====\n" + f[1]; }).join("\n");
      U.copyText(text, copyBtn);
    });

    paint();
    return box;
  }

  window.WriteTask = { render: render, runner: Runner };
})();
