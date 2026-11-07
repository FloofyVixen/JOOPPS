# JOOPPS: Java Object Oriented Programming Practice Site


Also titled "Java Objects, Step by Step" on the site itself.
A free course on object-oriented programming in Java for people with little or
no experience. The order follows UMaine's COS 225 (Object-Oriented Design,
Programming and Data Structures). Where COS 225 materials aren't public, the
University of Helsinki's Java MOOC and similar university courses fill the gaps.

The site is in `docs/` and is published with GitHub Pages.

## How the code is checked

Every piece of Java on the site goes through `build.py` before it's published:

- examples are compiled and run, and their real output or error is recorded
- fill-in-the-blank exercises are compiled with every accepted answer and every
  listed wrong answer; the real `javac`/`java` message for each wrong answer is
  what the learner sees
- write-it-yourself tasks: the reference solution and the hidden test file must
  compile, run and print exactly the expected output, for every guided step too
- "predict the output" answers must equal the real output

If anything doesn't hold, the build stops.

```
python3 build.py        # needs JDK 21 (javac and java on the PATH)
```

The build writes `docs/course-data.js`. Lesson content lives in `content/`:
one Python file per lesson, plus `tasks_*.py` for the write-it-yourself tasks.

## Running Java in the browser

The editor's Run button uses [CheerpJ](https://cheerpj.com/) (Java 21 runtime,
loaded from the CheerpJ CDN under its free Community licence, with the required
"Built with CheerpJ" credit in the footer) and the OpenJDK 21 compiler in
`docs/javac/javac21.jar`. See `docs/javac/legal/NOTICE.md` for its license.

## Status

No instructor has reviewed this material yet. If something looks wrong, trust
the sources linked on each lesson and your instructor over this site.
