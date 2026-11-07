from sources import VARIABLES, DATATYPES, ARITH, JLS_DIV, HEL_1_4, HEL_1_5

VARS = """public class Variables {
    public static void main(String[] args) {
        int age = 19;
        double gpa = 3.4;
        boolean enrolled = true;
        String name = "Riley";

        System.out.println(name + " is " + age + " years old.");
        System.out.println("GPA: " + gpa);
        System.out.println("Enrolled: " + enrolled);

        age = age + 1;
        System.out.println("Next year " + name + " will be " + age + ".");
    }
}
"""

DIVISION = """public class Division {
    public static void main(String[] args) {
        System.out.println(7 / 2);
        System.out.println(7 / 2.0);
        System.out.println(7 % 2);
    }
}
"""

LESSON = {
    "id": "intro-variables",
    "title": "Variables and types",
    "summary": "Store values in named variables, and pick the right type for each one.",
    "goals": [
        "Declare variables with the types `int`, `double`, `boolean` and `String`",
        "Change a variable's value and join values into text with `+`",
        "Predict what integer division and `%` (remainder) give you",
    ],
    "blocks": [
        {"type": "h", "text": "A variable is a named box for a value"},
        {"type": "p", "text": "A **variable** has a type, a name, and a value. The type says what kind of value fits in the box, and Java won't let you put the wrong kind in. Declare a variable by writing its type, then its name, then (usually) `=` and a starting value."},
        {"type": "code", "files": {"Variables.java": VARS}, "run": "Variables"},
        {"type": "list", "items": [
            "`int` holds whole numbers, like `19` or `-4`.",
            "`double` holds numbers with a decimal point, like `3.4`.",
            "`boolean` holds `true` or `false`.",
            "`String` holds text in double quotes. It starts with a capital S because it's a class, which you'll learn about in the next section. The other three are **primitive** types, built into the language.",
        ]},
        {"type": "p", "text": "The line `age = age + 1;` reads the current value of `age`, adds one, and stores the result back in `age`. You only write the type once, when you first declare the variable."},
        {"type": "p", "text": "When one side of `+` is a `String`, Java joins the two sides into longer text instead of adding numbers. That's how `name + \" is \" + age` builds a sentence."},
        {"type": "note", "label": "Naming variables",
         "text": "Variable names start with a lowercase letter, and each new word starts with a capital: `age`, `openSeats`, `shoulderLength`. Java programmers call this camelCase."},

        {"type": "h", "text": "Dividing whole numbers"},
        {"type": "p", "text": "When both numbers are `int`, the `/` operator gives a whole-number answer and throws away the remainder. To get the remainder itself, use `%`. If either number is a `double`, you get a decimal answer."},
        {"type": "predict", "id": "vars-division",
         "prompt": "What does this program print?",
         "files": {"Division.java": DIVISION}, "run": "Division",
         "choices": ["3.5\n3.5\n1", "3\n3.5\n1", "3\n3.5\n0", "4\n3.5\n1"],
         "answer": 1,
         "explain": "`7 / 2` uses two `int`s, so the result is `3` with the remainder dropped (not rounded). `7 / 2.0` has a `double`, so you get `3.5`. `7 % 2` is the remainder of 7 divided by 2, which is `1`."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "vars-types", "title": "Choose the types",
         "prompt": "Fill in a type for each variable so the program compiles and prints the ticket details.",
         "files": {"Ticket.java": """public class Ticket {
    public static void main(String[] args) {
        [[t1]] movie = "The Quiet Planet";
        [[t2]] seats = 2;
        [[t3]] price = 12.50;
        boolean matinee = false;

        System.out.println(movie + " for " + seats + " people");
        System.out.println("Total: $" + (seats * price));
        System.out.println("Matinee: " + matinee);
    }
}
"""},
         "run": "Ticket",
         "blanks": {
             "t1": {"accept": ["String"], "hint": "The value is text in double quotes.",
                    "wrong": [{"answer": "string", "why": "Java is case-sensitive, and the type is `String` with a capital S. To the compiler, `string` is an unknown name."},
                              {"answer": "char", "why": "A `char` holds a single character in single quotes, like `'A'`. Text in double quotes is a `String`."}]},
             "t2": {"accept": ["int"], "hint": "A whole number of seats.",
                    "wrong": [{"answer": "Int", "why": "Primitive types are all lowercase: `int`, not `Int`."},
                              {"answer": "String", "why": "`2` without quotes is a number, and a number can't be stored in a `String` variable."}]},
             "t3": {"accept": ["double"], "hint": "The price has a decimal point.",
                    "wrong": [{"answer": "int", "why": "`12.50` has a decimal part. Storing it in an `int` would lose the `.50`, so Java refuses and calls it a \"lossy conversion\"."}]},
         },
         "explain": "Text goes in a `String`, whole numbers in an `int`, and numbers with a decimal point in a `double`. In the output, `seats * price` is worked out before it's joined to the text because it's in parentheses."},

        {"type": "error", "id": "vars-wrong-type",
         "prompt": "This program doesn't compile. Read the compiler's message.",
         "files": {"Score.java": """public class Score {
    public static void main(String[] args) {
        int points = "ten";
        System.out.println(points);
    }
}
"""},
         "run": "Score", "expect": "compile",
         "question": "What is the best fix?",
         "choices": ["Change `int` to `double`",
                     "Change `\"ten\"` to `10`",
                     "Remove the semicolon on line 3",
                     "Rename the variable to `Points`"],
         "answer": 1,
         "explain": "The message says a `String` can't be converted to an `int`. `\"ten\"` is text, but `points` is declared as a whole number, so give it the number `10`. A `double` can't hold text either.",
         "fix": [["Score.java", "\"ten\"", "10"]]},

        {"type": "quiz", "id": "vars-redeclare",
         "question": "You declared `int count = 5;` and later want to make it 6. Which line does that?",
         "choices": ["`int count = 6;`", "`count = 6;`", "`count == 6;`", "`int count + 1;`"],
         "answer": 1,
         "explain": "After a variable is declared, assign to it with just its name and `=`. Writing `int` again would try to make a second variable with the same name, which is an error. `==` compares values; it doesn't assign."},
    ],
    "sources": [VARIABLES, DATATYPES, ARITH, JLS_DIV, HEL_1_4, HEL_1_5],
}
