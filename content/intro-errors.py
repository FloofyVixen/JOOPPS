from sources import JAVAC_MAN, EXCEPTIONS_TUT, AIOOBE, HEL_3_1, VSCODE_JAVA

SEMICOLON = """public class Weather {
    public static void main(String[] args) {
        int high = 72
        System.out.println("High: " + high);
    }
}
"""

SYMBOL = """public class Totals {
    public static void main(String[] args) {
        int itemCount = 3;
        System.out.println("Items: " + itemcount);
    }
}
"""

CASCADE = """public class Cascade {
    public static void main(String[] args) {
        System.out.println("Start");
        if (true) {
            System.out.println("Inside");

    }
}
"""

INDEX = """public class Scores {
    public static void main(String[] args) {
        int[] scores = {90, 85, 77};
        System.out.println("First: " + scores[0]);
        System.out.println("Fourth: " + scores[3]);
        System.out.println("Done");
    }
}
"""

LESSON = {
    "id": "intro-errors",
    "title": "Reading error messages",
    "summary": "Error messages tell you the file, the line and the problem. Learning to read them saves more time than anything else in this course.",
    "goals": [
        "Tell a compile error from a runtime error",
        "Find the file, line number and position in a `javac` message",
        "Recognize the most common messages and what usually causes them",
    ],
    "blocks": [
        {"type": "h", "text": "Two kinds of errors"},
        {"type": "p", "text": "A **compile error** comes from `javac` before your program runs at all. It means the code breaks one of Java's rules, such as a missing semicolon or a misspelled name. No `.class` file is made, so there's nothing to run."},
        {"type": "p", "text": "A **runtime error** happens while the program is running. The code was valid Java, but it asked for something impossible, such as an array item that doesn't exist. Java calls this an **exception**. The program prints a message and stops at that line."},

        {"type": "h", "text": "Anatomy of a compile error"},
        {"type": "code", "files": {"Weather.java": SEMICOLON}, "run": "Weather", "expect": "compile"},
        {"type": "list", "items": [
            "`Weather.java:3` is the file and line number. Start there.",
            "`error: ';' expected` is the problem itself.",
            "The next line repeats your code, and the `^` points to the exact spot. For a missing semicolon, it points just past the end of the line where the `;` should be.",
            "`1 error` is the total count.",
        ]},

        {"type": "h", "text": "\"cannot find symbol\""},
        {"type": "p", "text": "This is the most common message you'll see. A **symbol** is any name: a variable, method or class. Java can't find one with the name you wrote, which usually means a typo, wrong capitalization, or a variable that was declared somewhere else."},
        {"type": "code", "files": {"Totals.java": SYMBOL}, "run": "Totals", "expect": "compile",
         "after": "The `symbol:` line names what's missing (`itemcount`). The variable was declared as `itemCount`, with a capital C."},

        {"type": "h", "text": "Fix the first error first"},
        {"type": "p", "text": "One mistake can confuse the compiler about everything after it. A missing `}` is the classic case: Java reaches the end of the file still waiting for it. When there are several errors, fix the top one and compile again. Often the others disappear."},
        {"type": "code", "files": {"Cascade.java": CASCADE}, "run": "Cascade", "expect": "compile",
         "after": "\"reached end of file while parsing\" almost always means a `{` that was never closed. Here, the `if` block on line 4 is missing its closing brace."},

        {"type": "h", "text": "Anatomy of a runtime error"},
        {"type": "code", "files": {"Scores.java": INDEX}, "run": "Scores", "expect": "runtime"},
        {"type": "list", "items": [
            "Output printed before the crash still appears, which shows how far the program got. Notice that \"Done\" never prints.",
            "`java.lang.ArrayIndexOutOfBoundsException` is the type of exception. The text after it explains it: index 3 was asked for, but the array only has 3 items, numbered 0 to 2.",
            "`at Scores.main(Scores.java:5)` is the line that crashed. Later, when methods call other methods, you'll see several `at` lines. The top one is where it happened.",
        ]},

        {"type": "note", "label": "In VS Code",
         "text": "The red underlines in VS Code come from a different compiler (Eclipse's), so they're worded differently from the `javac` messages shown on this site. They point at the same problems. When you run `javac` in VS Code's terminal, you get exactly the messages shown here."},

        {"type": "h", "text": "Practice"},
        {"type": "error", "id": "errors-which-line",
         "prompt": "Read the message carefully.",
         "files": {"Bill.java": """public class Bill {
    public static void main(String[] args) {
        double subtotal = 40.0;
        double tip = subtotal * 0.2;
        System.out.println("Tip: " + tip)
        System.out.println("Total: " + (subtotal + tip));
    }
}
"""},
         "run": "Bill", "expect": "compile",
         "question": "Which line needs to be fixed?",
         "choices": ["Line 3", "Line 4", "Line 5", "Line 6"],
         "answer": 2,
         "explain": "The message starts with `Bill.java:5`, and the `^` sits at the end of line 5, where the semicolon is missing.",
         "fix": [["Bill.java", "+ tip)\n", "+ tip);\n"]]},
        {"type": "error", "id": "errors-symbol-method",
         "prompt": "This program uses a method from the previous lesson.",
         "files": {"Area.java": """public class Area {
    public static int square(int n) {
        return n * n;
    }

    public static void main(String[] args) {
        System.out.println(Square(5));
    }
}
"""},
         "run": "Area", "expect": "compile",
         "question": "What does `symbol: method Square(int)` tell you?",
         "choices": ["Java can't find a method named `Square` that takes an `int`; the method is actually named `square`",
                     "The number 5 is not an `int`",
                     "Methods can't be called from `main`",
                     "`square` is missing a return statement"],
         "answer": 0,
         "explain": "The name is wrong only in its capital letter. Java treats `Square` and `square` as completely different names.",
         "fix": [["Area.java", "println(Square(5))", "println(square(5))"]],
         "fixed_output": "25"},
        {"type": "quiz", "id": "errors-kind",
         "question": "A program prints two lines, then stops with `Exception in thread \"main\"`. What kind of error is it?",
         "choices": ["A compile error, because `javac` found a problem", "A runtime error, because the program had already started running", "No error; this is normal output", "A VS Code error that `javac` wouldn't report"],
         "answer": 1,
         "explain": "Anything that prints output first must have compiled successfully. An exception is a runtime error: valid code that hit an impossible situation while running."},
    ],
    "sources": [JAVAC_MAN, EXCEPTIONS_TUT, AIOOBE, HEL_3_1, VSCODE_JAVA],
}
