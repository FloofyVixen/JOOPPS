"""Write-it-yourself tasks for the Introduction section.
Every solution and test file here is compiled and run by build.py."""

FIRST = [
    {"type": "write", "id": "w-postcard", "mode": "independent", "title": "A postcard",
     "goal": "Create a file named `Postcard.java` with a class and a `main` method that prints these three lines, exactly as shown.",
     "files": ["Postcard.java"], "run": "Postcard",
     "output": "Greetings from Orono!\nThe weather is cold.\nSee you soon.",
     "requirements": ["The file is named `Postcard.java` and the class is named `Postcard`",
                      "Use `System.out.println` once for each line"],
     "hints": ["Start from the `Hello` program at the top of this lesson and change the class name and the text.",
               "Each line of output is one `System.out.println(\"...\");` statement."],
     "checks": [{"pattern": r"System\.out\.println\(", "message": "Print the lines with `System.out.println`."}],
     "solution": {"Postcard.java": """public class Postcard {
    public static void main(String[] args) {
        System.out.println("Greetings from Orono!");
        System.out.println("The weather is cold.");
        System.out.println("See you soon.");
    }
}
"""}},
    {"type": "write", "id": "w-oneline", "mode": "independent", "title": "Two statements, one line",
     "goal": "Create `OneLine.java`. Use `print` twice and `println` once so that the first line of output is built from three separate statements.",
     "files": ["OneLine.java"], "run": "OneLine",
     "output": "Java is fun.\nSecond line.",
     "requirements": ["`Java `, `is ` and `fun.` are printed by three different statements",
                      "`Second line.` is printed by its own `println`"],
     "hints": ["`System.out.print(\"Java \");` prints without ending the line.",
               "Only the statement that prints `fun.` should be a `println`, so the next output starts on a new line."],
     "checks": [{"pattern": r"System\.out\.print\(", "message": "Use `System.out.print` (without `ln`) at least once."}],
     "solution": {"OneLine.java": """public class OneLine {
    public static void main(String[] args) {
        System.out.print("Java ");
        System.out.print("is ");
        System.out.println("fun.");
        System.out.println("Second line.");
    }
}
"""}},
    {"type": "write", "id": "w-namecard", "mode": "independent", "title": "A name card",
     "goal": "Create `NameCard.java` that prints this box. Count the characters carefully: the output has to match exactly.",
     "files": ["NameCard.java"], "run": "NameCard",
     "output": "+-----------+\n| Hi, Java! |\n+-----------+",
     "requirements": ["Three `println` statements, one per line of the box"],
     "hints": ["The top and bottom lines are a `+`, eleven `-`, and a `+`.",
               "The middle line has one space after `|` and one space before the closing `|`."],
     "solution": {"NameCard.java": """public class NameCard {
    public static void main(String[] args) {
        System.out.println("+-----------+");
        System.out.println("| Hi, Java! |");
        System.out.println("+-----------+");
    }
}
"""}},
]

VARIABLES = [
    {"type": "write", "id": "w-pet", "mode": "independent", "title": "Describe a pet",
     "goal": "Create `Pet.java`. Store the pet's details in four variables (name `Biscuit`, age `4`, weight `11.5`, vaccinated `true`), then print them using the variables, not by typing the values into the text.",
     "files": ["Pet.java"], "run": "Pet",
     "output": "Biscuit is 4 years old.\nWeight: 11.5 lbs\nVaccinated: true",
     "requirements": ["One `String`, one `int`, one `double` and one `boolean` variable",
                      "Each printed value comes from a variable, joined to the text with `+`"],
     "hints": ["Pick the type by the kind of value: text, whole number, decimal number, true/false.",
               "`System.out.println(name + \" is \" + age + \" years old.\");`"],
     "checks": [
         {"pattern": r"\bString\s+\w+\s*=", "message": "Declare a `String` variable."},
         {"pattern": r"\bint\s+\w+\s*=", "message": "Declare an `int` variable."},
         {"pattern": r"\bdouble\s+\w+\s*=", "message": "Declare a `double` variable."},
         {"pattern": r"\bboolean\s+\w+\s*=", "message": "Declare a `boolean` variable."},
     ],
     "solution": {"Pet.java": """public class Pet {
    public static void main(String[] args) {
        String name = "Biscuit";
        int age = 4;
        double weight = 11.5;
        boolean vaccinated = true;

        System.out.println(name + " is " + age + " years old.");
        System.out.println("Weight: " + weight + " lbs");
        System.out.println("Vaccinated: " + vaccinated);
    }
}
"""}},
    {"type": "write", "id": "w-savings", "mode": "independent", "title": "Update a balance",
     "goal": "Create `Savings.java`. Start with a `double` balance of `100.0`. Print it, then add a deposit of `25.5` to the same variable and print it, then do that once more.",
     "files": ["Savings.java"], "run": "Savings",
     "output": "Start: 100.0\nAfter deposit: 125.5\nAfter deposit: 151.0",
     "requirements": ["Declare the balance once; change it with `balance = balance + ...`",
                      "Don't declare a second variable for the new total"],
     "hints": ["After the first `println`, write `balance = balance + 25.5;`.",
               "Notice how Java prints `151.0`, not `151`, because `balance` is a `double`."],
     "checks": [{"pattern": r"(\w+)\s*(\+=|=\s*\1\s*\+)", "message": "Add to the existing variable, for example `balance = balance + 25.5;`."}],
     "solution": {"Savings.java": """public class Savings {
    public static void main(String[] args) {
        double balance = 100.0;
        System.out.println("Start: " + balance);

        balance = balance + 25.5;
        System.out.println("After deposit: " + balance);

        balance = balance + 25.5;
        System.out.println("After deposit: " + balance);
    }
}
"""}},
    {"type": "write", "id": "w-pizza", "mode": "independent", "title": "Share a pizza",
     "goal": "Create `Pizza.java`. There are `13` slices and `4` people. Store both numbers in `int` variables, then use `/` and `%` to work out each person's share and the slices left over.",
     "files": ["Pizza.java"], "run": "Pizza",
     "output": "Each person gets 3 slices.\nLeftover slices: 1",
     "requirements": ["Use integer division `/` for the share", "Use `%` for the leftovers"],
     "hints": ["`slices / people` gives the whole-number share.", "`slices % people` gives what's left."],
     "checks": [{"pattern": r"\w+\s*/\s*\w+", "message": "Work out the share with `/`."},
                {"pattern": r"\w+\s*%\s*\w+", "message": "Work out the leftovers with `%`."}],
     "solution": {"Pizza.java": """public class Pizza {
    public static void main(String[] args) {
        int slices = 13;
        int people = 4;

        System.out.println("Each person gets " + (slices / people) + " slices.");
        System.out.println("Leftover slices: " + (slices % people));
    }
}
"""}},
]

LOOPS = [
    {"type": "write", "id": "w-ticketprice", "mode": "independent", "title": "Ticket price",
     "goal": "Create `TicketPrice.java` with `int age = 15;` and `boolean student = true;`. Children under 12 pay $5. Otherwise, students and people 65 or older pay $8. Everyone else pays $12. Print the price for these values.",
     "files": ["TicketPrice.java"], "run": "TicketPrice",
     "output": "Price: $8",
     "requirements": ["Use `if`, `else if` and `else`", "Use `||` to combine the student and age conditions"],
     "hints": ["Check the under-12 case first.", "`else if (student || age >= 65)`"],
     "checks": [{"pattern": r"\belse\s+if\b", "message": "Use an `else if` for the middle case."},
                {"pattern": r"\|\|", "message": "Combine the two conditions with `||`."}],
     "solution": {"TicketPrice.java": """public class TicketPrice {
    public static void main(String[] args) {
        int age = 15;
        boolean student = true;
        int price;

        if (age < 12) {
            price = 5;
        } else if (student || age >= 65) {
            price = 8;
        } else {
            price = 12;
        }
        System.out.println("Price: $" + price);
    }
}
"""}},
    {"type": "write", "id": "w-temptable", "mode": "independent", "title": "What to wear",
     "goal": "Create `WhatToWear.java`. Loop over the temperatures 30, 50, 70 and 90 (start at 30, add 20 each time). For each one, print `Coat` below 50, `Jacket` from 50 to 69, and `Shorts` at 70 or above.",
     "files": ["WhatToWear.java"], "run": "WhatToWear",
     "output": "30: Coat\n50: Jacket\n70: Shorts\n90: Shorts",
     "requirements": ["One `for` loop", "An `if` / `else if` / `else` inside the loop"],
     "hints": ["`for (int temp = 30; temp <= 90; temp = temp + 20)`",
               "Inside the loop, print `temp + \": Coat\"` and so on."],
     "checks": [{"pattern": r"\bfor\s*\(", "message": "Use a `for` loop."}],
     "solution": {"WhatToWear.java": """public class WhatToWear {
    public static void main(String[] args) {
        for (int temp = 30; temp <= 90; temp = temp + 20) {
            if (temp < 50) {
                System.out.println(temp + ": Coat");
            } else if (temp < 70) {
                System.out.println(temp + ": Jacket");
            } else {
                System.out.println(temp + ": Shorts");
            }
        }
    }
}
"""}},
    {"type": "write", "id": "w-evensum", "mode": "independent", "title": "Add up the even numbers",
     "goal": "Create `EvenSum.java`. Loop from 1 to 20 and add up only the even numbers, then print the total once.",
     "files": ["EvenSum.java"], "run": "EvenSum",
     "output": "Sum of even numbers from 1 to 20: 110",
     "requirements": ["Count from 1 to 20 with a loop", "Use `%` to test whether a number is even"],
     "hints": ["A number is even when `number % 2 == 0`.",
               "Declare `int total = 0;` before the loop, and print after the loop's closing brace."],
     "checks": [{"pattern": r"%\s*2", "message": "Test for even numbers with `% 2`."},
                {"pattern": r"\b(for|while)\s*\(", "message": "Use a loop."}],
     "solution": {"EvenSum.java": """public class EvenSum {
    public static void main(String[] args) {
        int total = 0;
        for (int i = 1; i <= 20; i++) {
            if (i % 2 == 0) {
                total = total + i;
            }
        }
        System.out.println("Sum of even numbers from 1 to 20: " + total);
    }
}
"""}},
]

METHODS = [
    {"type": "write", "id": "w-area", "mode": "independent", "title": "A method that returns",
     "goal": "Create `Shapes.java` with a method `public static int rectangleArea(int width, int height)` that returns the area. In `main`, print the area of a 3 by 4 rectangle and a 5 by 5 rectangle by calling your method.",
     "files": ["Shapes.java"], "run": "Shapes",
     "output": "Area: 12\nArea: 25",
     "tests": {"CheckShapes.java": """public class CheckShapes {
    public static void main(String[] args) {
        System.out.println("rectangleArea(7, 2) = " + Shapes.rectangleArea(7, 2));
        System.out.println("rectangleArea(1, 9) = " + Shapes.rectangleArea(1, 9));
    }
}
"""}, "tests_run": "CheckShapes",
     "tests_output": "rectangleArea(7, 2) = 14\nrectangleArea(1, 9) = 9",
     "requirements": ["The method header is exactly `public static int rectangleArea(int width, int height)`",
                      "The method returns the area; `main` does the printing"],
     "hints": ["The body is one line: `return width * height;`",
               "In `main`: `System.out.println(\"Area: \" + rectangleArea(3, 4));`"],
     "solution": {"Shapes.java": """public class Shapes {
    public static int rectangleArea(int width, int height) {
        return width * height;
    }

    public static void main(String[] args) {
        System.out.println("Area: " + rectangleArea(3, 4));
        System.out.println("Area: " + rectangleArea(5, 5));
    }
}
"""}},
    {"type": "write", "id": "w-banner", "mode": "independent", "title": "A void method",
     "goal": "Create `Banner.java` with a method `public static void printBanner(String text)` that prints the text between three stars on each side. Call it from `main` with `Welcome` and then `Goodbye`.",
     "files": ["Banner.java"], "run": "Banner",
     "output": "*** Welcome ***\n*** Goodbye ***",
     "tests": {"CheckBanner.java": """public class CheckBanner {
    public static void main(String[] args) {
        Banner.printBanner("Test");
    }
}
"""}, "tests_run": "CheckBanner", "tests_output": "*** Test ***",
     "requirements": ["`printBanner` returns nothing (`void`) and does the printing itself"],
     "hints": ["`System.out.println(\"*** \" + text + \" ***\");`"],
     "solution": {"Banner.java": """public class Banner {
    public static void printBanner(String text) {
        System.out.println("*** " + text + " ***");
    }

    public static void main(String[] args) {
        printBanner("Welcome");
        printBanner("Goodbye");
    }
}
"""}},
    {"type": "write", "id": "w-iseven", "mode": "independent", "title": "A method that answers yes or no",
     "goal": "Create `Numbers.java` with `public static boolean isEven(int n)`. It returns `true` when `n` is even. In `main`, print `isEven(4)` and `isEven(7)`.",
     "files": ["Numbers.java"], "run": "Numbers",
     "output": "true\nfalse",
     "tests": {"CheckNumbers.java": """public class CheckNumbers {
    public static void main(String[] args) {
        System.out.println("isEven(0) = " + Numbers.isEven(0));
        System.out.println("isEven(-3) = " + Numbers.isEven(-3));
        System.out.println("isEven(10) = " + Numbers.isEven(10));
    }
}
"""}, "tests_run": "CheckNumbers",
     "tests_output": "isEven(0) = true\nisEven(-3) = false\nisEven(10) = true",
     "requirements": ["The return type is `boolean`"],
     "hints": ["`n % 2 == 0` is already a `boolean`, so you can return it directly: `return n % 2 == 0;`"],
     "solution": {"Numbers.java": """public class Numbers {
    public static boolean isEven(int n) {
        return n % 2 == 0;
    }

    public static void main(String[] args) {
        System.out.println(isEven(4));
        System.out.println(isEven(7));
    }
}
"""}},
]

ERRORS = [
    {"type": "write", "id": "w-fix-receipt", "mode": "independent", "title": "Fix the compile errors",
     "goal": "`Receipt.java` has three mistakes. Run it, read the first message, fix that line, and run again until the program prints the receipt. The compiler reports only two of them at first; the third shows up once the first two are fixed. That's normal: `javac` checks spelling and punctuation before it checks names.",
     "files": ["Receipt.java"], "run": "Receipt",
     "output": "Coffee: 3.5\nMuffin: 2.25\nTotal: 5.75",
     "starter": {"Receipt.java": """public class Receipt {
    public static void main(String[] args) {
        double coffee = 3.5;
        double muffin = 2.25
        System.out.println("Coffee: " + coffee);
        System.out.println("Muffin: " + Muffin);
        System.out.println("Total: " + (coffee + muffin));
    }
"""},
     "requirements": ["Fix only what the compiler points to; don't rewrite the program"],
     "hints": ["Fix one message at a time, starting with the first.",
               "The last error is about the end of the file. Count the opening and closing braces."],
     "solution": {"Receipt.java": """public class Receipt {
    public static void main(String[] args) {
        double coffee = 3.5;
        double muffin = 2.25;
        System.out.println("Coffee: " + coffee);
        System.out.println("Muffin: " + muffin);
        System.out.println("Total: " + (coffee + muffin));
    }
}
"""}},
    {"type": "write", "id": "w-fix-crash", "mode": "independent", "title": "Fix the crash",
     "goal": "`Steps.java` compiles, but crashes while running. Read the exception, find the line, and fix the loop so it prints every day's steps and then the total.",
     "files": ["Steps.java"], "run": "Steps",
     "output": "Day 0: 4200\nDay 1: 6100\nDay 2: 3800\nTotal: 14100",
     "starter": {"Steps.java": """public class Steps {
    public static void main(String[] args) {
        int[] steps = {4200, 6100, 3800};
        int total = 0;
        for (int day = 0; day <= steps.length; day++) {
            System.out.println("Day " + day + ": " + steps[day]);
            total = total + steps[day];
        }
        System.out.println("Total: " + total);
    }
}
"""},
     "requirements": ["Change only the loop's condition"],
     "hints": ["The exception says which index was asked for, and how long the array is.",
               "An array of length 3 has slots 0, 1 and 2."],
     "checks": [{"pattern": r"day\s*<\s*steps\.length", "message": "Fix the loop condition so it stops before `steps.length`."}],
     "solution": {"Steps.java": """public class Steps {
    public static void main(String[] args) {
        int[] steps = {4200, 6100, 3800};
        int total = 0;
        for (int day = 0; day < steps.length; day++) {
            System.out.println("Day " + day + ": " + steps[day]);
            total = total + steps[day];
        }
        System.out.println("Total: " + total);
    }
}
"""}},
    {"type": "write", "id": "w-minutes", "mode": "independent", "title": "Write it from scratch",
     "goal": "Create `Minutes.java` with `public static String format(int minutes)`, which turns a number of minutes into hours and minutes, like `2 h 5 min` for 125. In `main`, print `format(125)` and `format(45)`. Expect a few errors along the way, and read each one.",
     "files": ["Minutes.java"], "run": "Minutes",
     "output": "2 h 5 min\n0 h 45 min",
     "tests": {"CheckMinutes.java": """public class CheckMinutes {
    public static void main(String[] args) {
        System.out.println("format(60) = " + Minutes.format(60));
        System.out.println("format(59) = " + Minutes.format(59));
        System.out.println("format(0) = " + Minutes.format(0));
    }
}
"""}, "tests_run": "CheckMinutes",
     "tests_output": "format(60) = 1 h 0 min\nformat(59) = 0 h 59 min\nformat(0) = 0 h 0 min",
     "requirements": ["`format` returns a `String`; it doesn't print", "Use `/` and `%`"],
     "hints": ["Hours are `minutes / 60`, and the minutes left over are `minutes % 60`.",
               "`return hours + \" h \" + rest + \" min\";`"],
     "solution": {"Minutes.java": """public class Minutes {
    public static String format(int minutes) {
        int hours = minutes / 60;
        int rest = minutes % 60;
        return hours + " h " + rest + " min";
    }

    public static void main(String[] args) {
        System.out.println(format(125));
        System.out.println(format(45));
    }
}
"""}},
]

TASKS = {
    "intro-first-program": FIRST,
    "intro-variables": VARIABLES,
    "intro-decisions-loops": LOOPS,
    "intro-methods": METHODS,
    "intro-errors": ERRORS,
}
