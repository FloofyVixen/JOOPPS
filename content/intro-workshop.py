from sources import FOR_TUT, IF_TUT, METHODS_TUT, RETURN_TUT, ARITH

T1 = """public class TimesTable {
    public static void main(String[] args) {
        System.out.println("7 times table");
    }
}
"""
T2 = """public class TimesTable {
    public static void main(String[] args) {
        System.out.println("7 times table");
        for (int i = 1; i <= 5; i++) {
            System.out.println("7 x " + i + " = " + (7 * i));
        }
    }
}
"""
T3 = """public class TimesTable {
    public static int times(int a, int b) {
        return a * b;
    }

    public static void main(String[] args) {
        System.out.println("7 times table");
        for (int i = 1; i <= 5; i++) {
            System.out.println("7 x " + i + " = " + times(7, i));
        }
    }
}
"""
T4 = """public class TimesTable {
    public static int times(int a, int b) {
        return a * b;
    }

    public static void main(String[] args) {
        System.out.println("7 times table");
        for (int i = 1; i <= 5; i++) {
            int product = times(7, i);
            if (product % 2 == 0) {
                System.out.println("7 x " + i + " = " + product + " (even)");
            } else {
                System.out.println("7 x " + i + " = " + product);
            }
        }
    }
}
"""

TIP1 = """public class TipCalculator {
    public static void main(String[] args) {
        double bill = 60.0;
        int people = 3;
        System.out.println("Bill: $" + bill);
        System.out.println("People: " + people);
    }
}
"""
TIP2 = """public class TipCalculator {
    public static double tip(double bill, double rate) {
        return bill * rate;
    }

    public static void main(String[] args) {
        double bill = 60.0;
        int people = 3;
        System.out.println("Bill: $" + bill);
        System.out.println("People: " + people);
        System.out.println("15% tip: $" + tip(bill, 0.15));
        System.out.println("20% tip: $" + tip(bill, 0.20));
    }
}
"""
TIP3 = """public class TipCalculator {
    public static double tip(double bill, double rate) {
        return bill * rate;
    }

    public static void main(String[] args) {
        double bill = 60.0;
        int people = 3;
        System.out.println("Bill: $" + bill);
        System.out.println("People: " + people);
        System.out.println("15% tip: $" + tip(bill, 0.15));
        System.out.println("20% tip: $" + tip(bill, 0.20));

        double each = (bill + tip(bill, 0.20)) / people;
        System.out.println("Each person pays: $" + each);
    }
}
"""
TIP4 = """public class TipCalculator {
    public static double tip(double bill, double rate) {
        return bill * rate;
    }

    public static void main(String[] args) {
        double bill = 60.0;
        int people = 3;
        System.out.println("Bill: $" + bill);
        System.out.println("People: " + people);
        System.out.println("15% tip: $" + tip(bill, 0.15));
        System.out.println("20% tip: $" + tip(bill, 0.20));

        double each = (bill + tip(bill, 0.20)) / people;
        System.out.println("Each person pays: $" + each);
        if (each > 20) {
            System.out.println("That's a pricey meal.");
        } else {
            System.out.println("That's a fair price.");
        }
    }
}
"""

TIMES_OUT = "7 times table\n7 x 1 = 7\n7 x 2 = 14\n7 x 3 = 21\n7 x 4 = 28\n7 x 5 = 35"
TIP_OUT2 = "Bill: $60.0\nPeople: 3\n15% tip: $9.0\n20% tip: $12.0"

LESSON = {
    "id": "intro-workshop",
    "title": "Workshop: the basics",
    "summary": "Four programs written by you, from an empty editor. The first two walk you through it one step at a time; the last two give you only the goal.",
    "goals": [
        "Create files and write complete programs without starter code",
        "Combine variables, `if`, loops and methods in one program",
        "Build a program in small steps, running it after each one",
    ],
    "cos225": "COS 225 exams include short code-writing questions (around eight lines) and are lenient about small syntax slips. Try each independent task on paper first, then type it in and let the compiler check you. That's good practice for writing code by hand.",
    "blocks": [
        {"type": "h", "text": "How the workshop works"},
        {"type": "p", "text": "In a **guided** task, you build one program over several steps. Each step tells you what to add and what the output should be when you run it. A step is done when your program's output matches, and then the next step opens. In an **independent** task, you get the goal and the expected output, and the rest is up to you."},
        {"type": "p", "text": "Create each file with **New file** in the editor and name it exactly as the task says. Remember the rule from the first lesson: the file name has to match the public class name."},

        {"type": "h", "text": "Guided 1: a times table"},
        {"type": "write", "id": "ws-intro-times", "mode": "guided", "title": "A times table",
         "goal": "Build `TimesTable.java`, a program that prints the 7 times table and marks the even results.",
         "files": ["TimesTable.java"],
         "steps": [
             {"title": "Create the program", "run": "TimesTable", "solution": {"TimesTable.java": T1},
              "text": "Create a file named `TimesTable.java`. Write the class and a `main` method that prints the heading `7 times table`.",
              "hint": "Start with `public class TimesTable {` and the usual `main` header.",
              "output": "7 times table"},
             {"title": "Add a loop", "run": "TimesTable", "solution": {"TimesTable.java": T2},
              "text": "Under the heading, add a `for` loop that counts `i` from 1 to 5 and prints a line like `7 x 3 = 21` for each value.",
              "hint": "`System.out.println(\"7 x \" + i + \" = \" + (7 * i));` The parentheses around `7 * i` keep it a multiplication.",
              "checks": [{"pattern": r"\bfor\s*\(", "message": "Use a `for` loop."}],
              "output": TIMES_OUT},
             {"title": "Move the math into a method", "run": "TimesTable", "solution": {"TimesTable.java": T3},
              "text": "Add `public static int times(int a, int b)`, which returns `a * b`. Change the loop to call `times(7, i)`. The output stays exactly the same; you're changing how the program is organized, not what it does.",
              "hint": "Write the method above `main`, inside the class.",
              "checks": [{"pattern": r"static\s+int\s+times\s*\(\s*int\s+\w+\s*,\s*int\s+\w+\s*\)", "message": "Write the method `public static int times(int a, int b)`."},
                         {"pattern": r"times\s*\(\s*7\s*,", "message": "Call `times(7, i)` inside the loop."}],
              "output": TIMES_OUT},
             {"title": "Mark the even results", "run": "TimesTable", "solution": {"TimesTable.java": T4},
              "text": "Store each result in a variable called `product`. If it's even, add ` (even)` to the end of the line.",
              "hint": "`if (product % 2 == 0)` prints the line with ` (even)`; `else` prints it without.",
              "checks": [{"pattern": r"%\s*2", "message": "Test for even numbers with `% 2`."}],
              "output": "7 times table\n7 x 1 = 7\n7 x 2 = 14 (even)\n7 x 3 = 21\n7 x 4 = 28 (even)\n7 x 5 = 35"},
         ]},

        {"type": "h", "text": "Guided 2: a tip calculator"},
        {"type": "write", "id": "ws-intro-tip", "mode": "guided", "title": "A tip calculator",
         "goal": "Build `TipCalculator.java`, which works out tips on a $60 bill and how much each of 3 people pays.",
         "files": ["TipCalculator.java"],
         "steps": [
             {"title": "Store the bill", "run": "TipCalculator", "solution": {"TipCalculator.java": TIP1},
              "text": "Create `TipCalculator.java`. In `main`, declare `double bill = 60.0;` and `int people = 3;`, then print them as shown.",
              "hint": "`System.out.println(\"Bill: $\" + bill);`",
              "output": "Bill: $60.0\nPeople: 3"},
             {"title": "Write a tip method", "run": "TipCalculator", "solution": {"TipCalculator.java": TIP2},
              "text": "Add `public static double tip(double bill, double rate)`, which returns the bill times the rate. Print the 15% tip (`0.15`) and the 20% tip (`0.20`).",
              "hint": "In `main`: `System.out.println(\"15% tip: $\" + tip(bill, 0.15));`",
              "checks": [{"pattern": r"static\s+double\s+tip\s*\(", "message": "Write `public static double tip(double bill, double rate)`."}],
              "output": TIP_OUT2},
             {"title": "Split the bill", "run": "TipCalculator", "solution": {"TipCalculator.java": TIP3},
              "text": "Work out what each person pays with a 20% tip: the bill plus the tip, divided by the number of people. Store it in a `double` called `each` and print it.",
              "hint": "`double each = (bill + tip(bill, 0.20)) / people;` Dividing a `double` by an `int` gives a `double`.",
              "output": TIP_OUT2 + "\nEach person pays: $24.0"},
             {"title": "Add a verdict", "run": "TipCalculator", "solution": {"TipCalculator.java": TIP4},
              "text": "If each person pays more than 20, print `That's a pricey meal.`; otherwise print `That's a fair price.`",
              "checks": [{"pattern": r"\bif\s*\(", "message": "Use an `if` statement."}],
              "output": TIP_OUT2 + "\nEach person pays: $24.0\nThat's a pricey meal."},
         ]},

        {"type": "h", "text": "Independent 1: parking fees"},
        {"type": "write", "id": "ws-intro-fee", "mode": "independent", "title": "Parking fees",
         "goal": "Create `ParkingFee.java` with `public static int fee(int hours)`. The first hour is free, each hour after that costs $2, and nobody pays more than $10. In `main`, print the fee for 1, 3 and 8 hours.",
         "files": ["ParkingFee.java"], "run": "ParkingFee",
         "output": "1 hours: $0\n3 hours: $4\n8 hours: $10",
         "tests": {"CheckParkingFee.java": """public class CheckParkingFee {
    public static void main(String[] args) {
        System.out.println("fee(0) = " + ParkingFee.fee(0));
        System.out.println("fee(2) = " + ParkingFee.fee(2));
        System.out.println("fee(6) = " + ParkingFee.fee(6));
        System.out.println("fee(7) = " + ParkingFee.fee(7));
    }
}
"""}, "tests_run": "CheckParkingFee",
         "tests_output": "fee(0) = 0\nfee(2) = 2\nfee(6) = 10\nfee(7) = 10",
         "requirements": ["`fee` returns the amount; `main` prints it", "Zero hours costs $0, not a negative amount"],
         "hints": ["Handle the free case first: if `hours <= 1`, return 0.",
                   "Otherwise the cost is `(hours - 1) * 2`. If that's more than 10, return 10."],
         "solution": {"ParkingFee.java": """public class ParkingFee {
    public static int fee(int hours) {
        if (hours <= 1) {
            return 0;
        }
        int cost = (hours - 1) * 2;
        if (cost > 10) {
            return 10;
        }
        return cost;
    }

    public static void main(String[] args) {
        System.out.println("1 hours: $" + fee(1));
        System.out.println("3 hours: $" + fee(3));
        System.out.println("8 hours: $" + fee(8));
    }
}
"""}},

        {"type": "h", "text": "Independent 2: a counting game"},
        {"type": "write", "id": "ws-intro-counting", "mode": "independent", "title": "A counting game",
         "goal": "Create `CountingGame.java` that prints the numbers 1 to 15, one per line. Replace multiples of 3 with `Fizz`, multiples of 5 with `Buzz`, and multiples of both with `FizzBuzz`.",
         "files": ["CountingGame.java"], "run": "CountingGame",
         "output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
         "requirements": ["One loop", "An `if` / `else if` chain that checks the \"both\" case first"],
         "hints": ["Why check \"both\" first? 15 is a multiple of 3, so a `% 3` check that comes first would catch it and print only `Fizz`.",
                   "Multiples of both 3 and 5 are the multiples of 15: `i % 15 == 0`."],
         "checks": [{"pattern": r"\b(for|while)\s*\(", "message": "Use a loop."}],
         "solution": {"CountingGame.java": """public class CountingGame {
    public static void main(String[] args) {
        for (int i = 1; i <= 15; i++) {
            if (i % 15 == 0) {
                System.out.println("FizzBuzz");
            } else if (i % 3 == 0) {
                System.out.println("Fizz");
            } else if (i % 5 == 0) {
                System.out.println("Buzz");
            } else {
                System.out.println(i);
            }
        }
    }
}
"""}},
    ],
    "sources": [FOR_TUT, IF_TUT, METHODS_TUT, RETURN_TUT, ARITH],
}
