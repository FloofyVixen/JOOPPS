from sources import METHODS_TUT, RETURN_TUT, ARGS_TUT, HEL_2_4

METHODS = """public class Methods {
    public static void greet(String name) {
        System.out.println("Hi, " + name + "!");
    }

    public static int square(int n) {
        return n * n;
    }

    public static void main(String[] args) {
        greet("Sam");
        greet("Ana");

        int result = square(6);
        System.out.println("6 squared is " + result);
        System.out.println("3 squared is " + square(3));
    }
}
"""

LESSON = {
    "id": "intro-methods",
    "title": "Methods",
    "summary": "Give a piece of code a name so you can run it whenever you need it, with different inputs each time.",
    "goals": [
        "Define a method with parameters and call it",
        "Tell the difference between a `void` method and one that returns a value",
        "Read the parts of a method header",
    ],
    "blocks": [
        {"type": "h", "text": "Naming a piece of code"},
        {"type": "p", "text": "A **method** is a named block of code. You define it once, then **call** it by name as many times as you like. Values you pass in go into its **parameters**, which work like variables inside the method."},
        {"type": "code", "files": {"Methods.java": METHODS}, "run": "Methods"},
        {"type": "p", "text": "Read a method header from left to right:"},
        {"type": "snippet", "code": "public static int square(int n) {"},
        {"type": "list", "items": [
            "`public` means code outside this class may call it.",
            "`static` means it belongs to the class itself. Every method in this unit is `static`; in \"Introduction to OOP\" you'll write methods without it, which belong to objects.",
            "`int` is the **return type**: the kind of value the method hands back. `void` means it hands nothing back.",
            "`square` is the method's name, and `(int n)` is its parameter list.",
        ]},
        {"type": "p", "text": "`return` ends the method and sends a value back to the caller. That's why `int result = square(6);` works: the call is replaced by the value 36. A `void` method like `greet` does its job (here, printing) and returns nothing, so you can't store its result."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "methods-larger", "title": "Return the larger number",
         "prompt": "Complete `larger` so it returns whichever of its two numbers is bigger.",
         "files": {"Larger.java": """public class Larger {
    public static [[rtype]] larger(int a, int b) {
        if (a > b) {
            [[ret]] a;
        }
        return b;
    }

    public static void main(String[] args) {
        System.out.println(larger(4, 9));
        System.out.println(larger(12, 5));
    }
}
"""},
         "run": "Larger", "output": "9\n12",
         "blanks": {
             "rtype": {"accept": ["int"], "hint": "What type of value does the method give back?",
                       "wrong": [{"answer": "void", "why": "`void` means \"returns nothing\", but this method returns `a` or `b`, so each `return` is an \"unexpected return value\". The two `println` calls fail as well, because there's no value to print. Four errors, one cause."},
                                 {"answer": "double", "why": "This compiles, because an `int` fits in a `double`. But then the results print as `9.0` and `12.0`. The inputs are whole numbers, so return an `int`."}]},
             "ret": {"accept": ["return"], "hint": "Which keyword sends a value back?",
                     "wrong": [{"answer": "print", "why": "Java reads `print a;` as declaring a new variable `a` whose type is a class named `print`. No such class exists, and `a` is already a parameter, so you get two confusing errors from one word. To send a value back to the caller, use `return`."}]},
         },
         "explain": "When `a > b`, the method returns `a` right away and the last line never runs. Otherwise it falls through to `return b;`."},
        {"type": "error", "id": "methods-missing-return",
         "prompt": "This method should return 1 for positive numbers, -1 for negative numbers and 0 for zero.",
         "files": {"Sign.java": """public class Sign {
    public static int sign(int n) {
        if (n > 0) {
            return 1;
        } else if (n < 0) {
            return -1;
        }
    }

    public static void main(String[] args) {
        System.out.println(sign(-7));
        System.out.println(sign(0));
    }
}
"""},
         "run": "Sign", "expect": "compile",
         "question": "What is the compiler complaining about?",
         "choices": ["`-1` is not a valid `int`",
                     "If `n` is 0, neither `return` runs, so the method could end without returning anything",
                     "Methods can only have one `return` statement",
                     "`main` must come before `sign`"],
         "answer": 1,
         "explain": "A method that promises to return an `int` has to return one on every path. When `n` is 0, both conditions are false. Adding `return 0;` at the end covers that case.",
         "fix": [["Sign.java", "            return -1;\n        }\n", "            return -1;\n        }\n        return 0;\n"]],
         "fixed_output": "-1\n0"},
        {"type": "quiz", "id": "methods-void",
         "question": "`public static void greet(String name)` is defined. Which line will not compile?",
         "choices": ["`greet(\"Lee\");`", "`String s = greet(\"Lee\");`", "`greet(\"Lee\" + \"!\");`", "`greet(\"\");`"],
         "answer": 1,
         "explain": "`greet` is `void`, so it returns nothing that could be stored in `s`. The other calls pass a `String`, which is what the parameter expects."},
    ],
    "sources": [METHODS_TUT, RETURN_TUT, ARGS_TUT, HEL_2_4],
}
