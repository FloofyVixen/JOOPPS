from sources import IF_TUT, FOR_TUT, WHILE_TUT, EQUALITY, HEL_1_6, HEL_2_2

IF_DEMO = """public class Grade {
    public static void main(String[] args) {
        int score = 84;

        if (score >= 90) {
            System.out.println("A");
        } else if (score >= 80) {
            System.out.println("B");
        } else {
            System.out.println("Below B");
        }

        boolean onTime = true;
        if (score >= 70 && onTime) {
            System.out.println("Passed and on time");
        }
    }
}
"""

FOR_DEMO = """public class CountUp {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            System.out.println("Lap " + i);
        }
    }
}
"""

WHILE_DEMO = """public class Countdown {
    public static void main(String[] args) {
        int seconds = 3;
        while (seconds > 0) {
            System.out.println(seconds + "...");
            seconds = seconds - 1;
        }
        System.out.println("Go!");
    }
}
"""

SUM_DEMO = """public class Sum {
    public static void main(String[] args) {
        int total = 0;
        for (int i = 1; i <= 4; i++) {
            total = total + i;
        }
        System.out.println(total);
    }
}
"""

LESSON = {
    "id": "intro-decisions-loops",
    "title": "Decisions and loops",
    "summary": "Make a program choose between paths with `if`, and repeat work with `for` and `while`.",
    "goals": [
        "Write `if`, `else if` and `else` with comparisons like `>=` and `==`",
        "Combine conditions with `&&` (and) and `||` (or)",
        "Repeat code a set number of times with `for`, or until something changes with `while`",
    ],
    "blocks": [
        {"type": "h", "text": "Choosing with if"},
        {"type": "p", "text": "An `if` statement runs a block of code only when its condition is `true`. Add `else if` to check another condition, and `else` for everything left over. Java checks them from top to bottom and runs only the first block that matches."},
        {"type": "code", "files": {"Grade.java": IF_DEMO}, "run": "Grade"},
        {"type": "p", "text": "The comparison operators are `<`, `<=`, `>`, `>=`, `==` (equal to) and `!=` (not equal to). Each gives a `boolean`. Use `&&` when both conditions must be true and `||` when at least one must be."},
        {"type": "note", "label": "Common mistake",
         "text": "One `=` stores a value. Two `==` compare values. Writing `if (score = 90)` is a compile error, which you'll see in the practice below."},

        {"type": "h", "text": "Repeating with for"},
        {"type": "p", "text": "A `for` loop is the usual choice when you know how many times to repeat. Its header has three parts, separated by semicolons: where the counter starts, the condition to keep going, and how the counter changes after each pass. `i++` means \"add one to `i`\"."},
        {"type": "code", "files": {"CountUp.java": FOR_DEMO}, "run": "CountUp"},

        {"type": "h", "text": "Repeating with while"},
        {"type": "p", "text": "A `while` loop keeps going as long as its condition is true. Something inside the loop has to change the condition, or the loop never stops."},
        {"type": "code", "files": {"Countdown.java": WHILE_DEMO}, "run": "Countdown"},

        {"type": "h", "text": "Practice"},
        {"type": "predict", "id": "loops-sum",
         "prompt": "What does this program print?",
         "files": {"Sum.java": SUM_DEMO}, "run": "Sum",
         "choices": ["4", "6", "10", "1\n3\n6\n10"],
         "answer": 2,
         "explain": "The loop adds 1, 2, 3 and 4 to `total`, which gives 10. The `println` is after the loop's closing brace, so it runs once, at the end."},
        {"type": "blanks", "id": "loops-for-header", "title": "Write the loop header",
         "prompt": "Make the loop print the row numbers 0, 1, 2, 3 and 4, one per line.",
         "files": {"Rows.java": """public class Rows {
    public static void main(String[] args) {
        for (int row = [[start]]; row [[cmp]] 5; row++) {
            System.out.println("Row " + row);
        }
    }
}
"""},
         "run": "Rows", "output": "Row 0\nRow 1\nRow 2\nRow 3\nRow 4",
         "blanks": {
             "start": {"accept": ["0"], "hint": "The first row printed is row 0.",
                       "wrong": [{"answer": "1", "why": "Starting at 1 skips row 0."}]},
             "cmp": {"accept": ["<"], "hint": "Row 5 should not be printed.",
                     "wrong": [{"answer": "<=", "why": "`row <= 5` is still true when `row` is 5, so you get one extra row. This kind of mistake is called an off-by-one error."},
                               {"answer": ">", "why": "`0 > 5` is false from the start, so the loop body never runs and nothing is printed."}]},
         },
         "explain": "Counting from 0 while `row < 5` gives exactly five passes: 0, 1, 2, 3, 4. Later, when you loop over arrays, you'll write this same pattern constantly."},
        {"type": "error", "id": "loops-assign-in-if",
         "prompt": "This program is supposed to say whether the oven is ready. It doesn't compile.",
         "files": {"Oven.java": """public class Oven {
    public static void main(String[] args) {
        int temperature = 350;
        if (temperature = 350) {
            System.out.println("Ready");
        }
    }
}
"""},
         "run": "Oven", "expect": "compile",
         "question": "Why does the compiler say an `int` can't be converted to a `boolean`?",
         "choices": ["Because 350 is too large for an `int`",
                     "Because `=` stores a value instead of comparing, so the condition is an `int` rather than `true`/`false`",
                     "Because `if` statements can't use variables",
                     "Because `println` needs a number"],
         "answer": 1,
         "explain": "`temperature = 350` is an assignment, and its result is the `int` 350. An `if` needs a `boolean`. Comparing with `==` gives one.",
         "fix": [["Oven.java", "temperature = 350)", "temperature == 350)"]],
         "fixed_output": "Ready"},
        {"type": "quiz", "id": "loops-and-or",
         "question": "`int hour = 20;` Which condition is `true`?",
         "choices": ["`hour > 8 && hour < 17`", "`hour < 8 || hour > 18`", "`hour == 17`", "`hour != 20`"],
         "answer": 1,
         "explain": "20 isn't less than 8, but it is greater than 18. With `||`, one true side is enough. The first choice needs both sides to be true, and 20 isn't less than 17."},
    ],
    "sources": [IF_TUT, EQUALITY, FOR_TUT, WHILE_TUT, HEL_1_6, HEL_2_2],
}
