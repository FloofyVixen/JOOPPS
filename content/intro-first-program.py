from sources import HELLO_TUT, DEV_FIRST, JAVAC_MAN, JAVA_MAN, HEL_1_1, HEL_1_2

HELLO = """public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
        System.out.println("This is my first program.");
    }
}
"""

PRINT_VS_PRINTLN = """public class PrintDemo {
    public static void main(String[] args) {
        System.out.print("Same ");
        System.out.print("line. ");
        System.out.println("Now end the line.");
        System.out.println("This starts a new line.");
    }
}
"""

LESSON = {
    "id": "intro-first-program",
    "title": "Your first Java program",
    "summary": "What a Java program looks like, and the two commands that turn it into something you can run.",
    "goals": [
        "Recognize the parts of a Java program: the class, the `main` method, and statements",
        "Compile a program with `javac` and run it with `java`",
        "Print text with `System.out.println` and `System.out.print`",
    ],
    "blocks": [
        {"type": "h", "text": "A whole program, start to finish"},
        {"type": "p", "text": "Here is a complete Java program. Read it once, then we'll go through it line by line. Everything Java runs lives inside a **class**, and every program starts at a method called `main`."},
        {"type": "code", "files": {"Hello.java": HELLO}, "run": "Hello",
         "caption": "The file must be named `Hello.java`, because the class is named `Hello`."},
        {"type": "list", "items": [
            "`public class Hello` starts a class named `Hello`. The curly braces `{ }` mark where it begins and ends.",
            "`public static void main(String[] args)` is where the program starts. Java looks for exactly this line. For now, copy it as it is; you'll learn what each word means over the next few lessons.",
            "`System.out.println(...)` prints the text in the parentheses, then moves to a new line.",
            "Each instruction (a **statement**) ends with a semicolon `;`.",
        ]},
        {"type": "note", "label": "One rule to remember",
         "text": "A `public class` must be saved in a file with exactly the same name, plus `.java`. Capital letters count: `Hello` goes in `Hello.java`, not `hello.java`."},

        {"type": "h", "text": "Compiling, then running"},
        {"type": "p", "text": "Java runs your program in two steps. First the **compiler**, `javac`, checks your code and translates it into a `.class` file. If the code breaks one of Java's rules, `javac` stops and tells you where. Then the `java` command runs the `.class` file."},
        {"type": "terminal", "files": {"Hello.java": HELLO},
         "commands": ["javac Hello.java", "ls", "java Hello"],
         "caption": "Real output from these commands. `javac` prints nothing when it succeeds; `ls` shows the new `Hello.class` file it made."},
        {"type": "p", "text": "In VS Code, the **Run** button above `main` does both steps for you. It's still worth knowing the two commands, because error messages always come from one step or the other."},

        {"type": "h", "text": "print and println"},
        {"type": "p", "text": "`println` ends the line after printing. `print` doesn't, so the next thing printed continues on the same line."},
        {"type": "code", "files": {"PrintDemo.java": PRINT_VS_PRINTLN}, "run": "PrintDemo"},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "first-greeting", "title": "Finish the program",
         "prompt": "This file is saved as `Greeting.java`. Fill in the class name and the print method so the program prints two lines.",
         "files": {"Greeting.java": """public class [[name]] {
    public static void main(String[] args) {
        System.out.[[print]]("Welcome!");
        System.out.println("Let's write some Java.");
    }
}
"""},
         "run": "Greeting",
         "blanks": {
             "name": {"accept": ["Greeting"], "hint": "It has to match the file name exactly.",
                      "wrong": [{"answer": "greeting", "why": "Java is case-sensitive. `greeting` and `Greeting` are different names, and the file is `Greeting.java`."},
                                {"answer": "Greeting.java", "why": "The class name doesn't include `.java`. That's only part of the file name."}]},
             "print": {"accept": ["println"], "hint": "Which method prints and then moves to a new line?",
                       "wrong": [{"answer": "printline", "why": "There's no method called `printline`. The name is shortened to `println` (print line)."},
                                 {"answer": "Println", "why": "Method names are case-sensitive. It's `println` with a lowercase p."},
                                 {"answer": "print", "why": "`print` is a real method, so this compiles. But it doesn't end the line, so both messages end up on one line."}]},
         },
         "explain": "The class name matches the file, and `println` puts each message on its own line."},

        {"type": "quiz", "id": "first-javac-job",
         "question": "What does `javac Hello.java` do?",
         "choices": ["Runs the program and prints its output",
                     "Checks the code and translates it into `Hello.class`",
                     "Opens the file in an editor",
                     "Deletes the old version of the program"],
         "answer": 1,
         "explain": "`javac` is the compiler. It checks your code and, if there are no errors, writes `Hello.class`. Running the program is the job of the `java` command."},
        {"type": "quiz", "id": "first-semicolon",
         "question": "Which of these lines is a complete, correct Java statement?",
         "choices": ["`System.out.println(\"Hi\")`",
                     "`System.out.println(\"Hi\");`",
                     "`system.out.println(\"Hi\");`",
                     "`System.out.println(Hi);`"],
         "answer": 1,
         "explain": "Statements end with a semicolon, `System` starts with a capital S, and text must be inside double quotes. Without quotes, Java reads `Hi` as the name of a variable."},
    ],
    "sources": [HELLO_TUT, DEV_FIRST, JAVAC_MAN, JAVA_MAN, HEL_1_1, HEL_1_2],
}
