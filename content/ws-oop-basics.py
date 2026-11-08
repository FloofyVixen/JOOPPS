from sources import CONSTRUCTORS_TUT, THIS_TUT, OBJECT_TOSTRING, HEL_5_2
from wshelp import step, guided, workshop, task

CARD1 = """public class LibraryCard {
    public String owner;
    public int number;
    public int booksOut;

    public LibraryCard(String owner, int number) {
        this.owner = owner;
        this.number = number;
        booksOut = 0;
    }
}
"""
TOSTR = """
    @Override
    public String toString() {
        return "Card " + number + " (" + owner + "): " + booksOut + " books out";
    }
}
"""
CARD2 = CARD1[:-2] + TOSTR
CHECKOUT = """
    public void checkOut() {
        booksOut = booksOut + 1;
    }

    public void returnBook() {
        if (booksOut > 0) {
            booksOut = booksOut - 1;
        }
    }
"""
CARD3 = CARD1[:-2] + CHECKOUT + TOSTR
DEFAULT = """    public LibraryCard() {
        owner = "Guest";
        number = 0;
        booksOut = 0;
    }

"""
CARD4 = CARD3.replace("    public LibraryCard(String owner", DEFAULT + "    public LibraryCard(String owner")
CT1 = """public class CardTester {
    public static void main(String[] args) {
        LibraryCard ana = new LibraryCard("Ana", 1042);
        System.out.println(ana.owner + " " + ana.number + " " + ana.booksOut);
    }
}
"""
CT2 = CT1.replace("""        System.out.println(ana.owner + " " + ana.number + " " + ana.booksOut);""", """        System.out.println(ana);""")
CT3 = """public class CardTester {
    public static void main(String[] args) {
        LibraryCard ana = new LibraryCard("Ana", 1042);
        ana.checkOut();
        ana.checkOut();
        ana.returnBook();
        System.out.println(ana);
        ana.returnBook();
        ana.returnBook();
        System.out.println(ana);
    }
}
"""
CT4 = CT3.replace("""        System.out.println(ana);
    }
}
""", """        System.out.println(ana);
        System.out.println(new LibraryCard());
    }
}
""")

COLOR1 = """public class Color {
    public int red;
    public int green;
    public int blue;

    public Color(int red, int green, int blue) {
        this.red = red;
        this.green = green;
        this.blue = blue;
    }

    @Override
    public String toString() {
        return "rgb(" + red + ", " + green + ", " + blue + ")";
    }
}
"""
COLOR2 = COLOR1.replace("    public Color(int red", """    public Color() {
        red = 0;
        green = 0;
        blue = 0;
    }

    public Color(int red""")
COLOR3 = COLOR2.replace("""    @Override
    public String toString()""", """    public Color mix(Color other) {
        return new Color((red + other.red) / 2, (green + other.green) / 2, (blue + other.blue) / 2);
    }

    @Override
    public String toString()""")
PT1 = """public class PaintTester {
    public static void main(String[] args) {
        Color red = new Color(255, 0, 0);
        Color blue = new Color(0, 0, 255);
        System.out.println(red);
        System.out.println(blue);
    }
}
"""
PT2 = PT1.replace("""        System.out.println(blue);
""", """        System.out.println(blue);
        System.out.println(new Color());
""")
PT3 = """public class PaintTester {
    public static void main(String[] args) {
        Color red = new Color(255, 0, 0);
        Color blue = new Color(0, 0, 255);
        Color purple = red.mix(blue);
        System.out.println(purple);
        System.out.println(red);
        System.out.println(new Color().mix(new Color(100, 50, 20)));
    }
}
"""

LESSON = workshop(
    "ws-oop-basics", "Workshop: OOP basics in Java",
    "Practice constructors, `this`, a second constructor, and `toString`, including a method that builds and returns a new object.",
    ["Write parameterized and default constructors from scratch",
     "Write `toString` methods that match an exact format",
     "Write a method that takes an object and returns a new one"],
    guided("ws-u3-card", "A library card", "Build a `LibraryCard` with a constructor, a `toString`, methods that change it, and a default constructor.", [
        step("The constructor", "Create `LibraryCard.java` with public fields `owner`, `number` and `booksOut`. The constructor takes the owner and number; `booksOut` starts at 0. Print the three fields from `CardTester`.",
             {"LibraryCard.java": CARD1, "CardTester.java": CT1}, "CardTester", "Ana 1042 0",
             checks=[{"pattern": r"this\.owner\s*=", "message": "Store the owner with `this.owner = owner;`."}]),
        step("toString", "Add a `toString` that returns `Card <number> (<owner>): <booksOut> books out`, and print the card directly.",
             {"LibraryCard.java": CARD2, "CardTester.java": CT2}, "CardTester", "Card 1042 (Ana): 0 books out"),
        step("Borrowing", "Add `checkOut()` (one more book out) and `returnBook()` (one fewer, but never below 0). Check out twice, return three times, and print along the way as shown.",
             {"LibraryCard.java": CARD3, "CardTester.java": CT3}, "CardTester",
             "Card 1042 (Ana): 1 books out\nCard 1042 (Ana): 0 books out",
             hint="`returnBook()` needs an `if (booksOut > 0)`."),
        step("A guest card", "Add a default constructor for a guest card: owner `Guest`, number 0. Print a new guest card at the end of the tester.",
             {"LibraryCard.java": CARD4, "CardTester.java": CT4}, "CardTester",
             "Card 1042 (Ana): 1 books out\nCard 1042 (Ana): 0 books out\nCard 0 (Guest): 0 books out",
             hint="Two constructors can live in one class as long as their parameter lists differ."),
    ]),
    guided("ws-u3-color", "A color mixer", "Build a `Color` class whose `mix` method returns a brand-new color.", [
        step("Color and toString", "Create `Color.java` with public `int` fields `red`, `green`, `blue`, a constructor that takes all three, and a `toString` like `rgb(255, 0, 0)`. Print red and blue.",
             {"Color.java": COLOR1, "PaintTester.java": PT1}, "PaintTester", "rgb(255, 0, 0)\nrgb(0, 0, 255)"),
        step("Default black", "Add a default constructor that makes black, `rgb(0, 0, 0)`, and print one.",
             {"Color.java": COLOR2, "PaintTester.java": PT2}, "PaintTester", "rgb(255, 0, 0)\nrgb(0, 0, 255)\nrgb(0, 0, 0)"),
        step("Mixing", "Add `mix(Color other)`, which returns a **new** `Color` whose channels are the averages of the two colors (integer division). Mixing must not change either original color.",
             {"Color.java": COLOR3, "PaintTester.java": PT3}, "PaintTester",
             "rgb(127, 0, 127)\nrgb(255, 0, 0)\nrgb(50, 25, 10)",
             hint="`return new Color((red + other.red) / 2, (green + other.green) / 2, (blue + other.blue) / 2);`"),
    ]),
    task("ws-u3-fraction", "A fraction",
         "Write `Fraction` with public `numerator` and `denominator`, a constructor, a `toString` like `3/4`, and `times(Fraction other)`, which returns a new fraction (multiply the tops and the bottoms; no simplifying).",
         {"Fraction.java": """public class Fraction {
    public int numerator;
    public int denominator;

    public Fraction(int numerator, int denominator) {
        this.numerator = numerator;
        this.denominator = denominator;
    }

    public Fraction times(Fraction other) {
        return new Fraction(numerator * other.numerator, denominator * other.denominator);
    }

    @Override
    public String toString() {
        return numerator + "/" + denominator;
    }
}
""", "FractionTester.java": """public class FractionTester {
    public static void main(String[] args) {
        Fraction half = new Fraction(1, 2);
        Fraction threeQuarters = new Fraction(3, 4);
        System.out.println(half);
        System.out.println(half.times(threeQuarters));
    }
}
"""}, "FractionTester", "1/2\n3/8",
         tests={"CheckFraction.java": """public class CheckFraction {
    public static void main(String[] args) {
        Fraction a = new Fraction(2, 3);
        Fraction b = new Fraction(5, 7);
        System.out.println(a.times(b));
        System.out.println(a);
    }
}
"""}, tests_run="CheckFraction", tests_output="10/21\n2/3",
         hints=["`times` builds the answer with `new Fraction(...)`; it doesn't change `this` fraction."]),
    task("ws-u3-duration", "Two ways to build a duration",
         "Write `Duration` with public `minutes` and `seconds` and two constructors: `Duration(int totalSeconds)` works out the minutes and seconds, and `Duration(int minutes, int seconds)` stores them directly. `toString` returns text like `2m 5s`.",
         {"Duration.java": """public class Duration {
    public int minutes;
    public int seconds;

    public Duration(int totalSeconds) {
        minutes = totalSeconds / 60;
        seconds = totalSeconds % 60;
    }

    public Duration(int minutes, int seconds) {
        this.minutes = minutes;
        this.seconds = seconds;
    }

    @Override
    public String toString() {
        return minutes + "m " + seconds + "s";
    }
}
""", "DurationTester.java": """public class DurationTester {
    public static void main(String[] args) {
        System.out.println(new Duration(125));
        System.out.println(new Duration(3, 40));
    }
}
"""}, "DurationTester", "2m 5s\n3m 40s",
         tests={"CheckDuration.java": """public class CheckDuration {
    public static void main(String[] args) {
        System.out.println(new Duration(59));
        System.out.println(new Duration(60));
        System.out.println(new Duration(0, 0));
    }
}
"""}, tests_run="CheckDuration", tests_output="0m 59s\n1m 0s\n0m 0s",
         hints=["Java picks the constructor by the number of arguments: one `int` or two."]),
    [CONSTRUCTORS_TUT, THIS_TUT, OBJECT_TOSTRING, HEL_5_2],
)
