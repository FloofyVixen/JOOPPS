from sources import CLASSES_TUT, OBJECTS_TUT, FIELDS_TUT, HEL_4_1
from wshelp import step, guided, workshop, task

PET1 = """public class Pet {
    public String name;
    public String species;
    public int age;
}
"""
PET2 = PET1.replace("""    public int age;
}
""", """    public int age;

    public void introduce() {
        System.out.println("I'm " + name + ", a " + age + "-year-old " + species + ".");
    }
}
""")
PET3 = PET2.replace("""    }
}
""", """    }

    public void haveBirthday() {
        age = age + 1;
    }
}
""")
PT1 = """public class PetTester {
    public static void main(String[] args) {
        Pet first = new Pet();
        first.name = "Biscuit";
        first.species = "dog";
        first.age = 4;
        System.out.println(first.name + " is a " + first.species + ".");
    }
}
"""
PT2 = PT1.replace("""        System.out.println(first.name + " is a " + first.species + ".");""", """        first.introduce();""")
PT3 = """public class PetTester {
    public static void main(String[] args) {
        Pet first = new Pet();
        first.name = "Biscuit";
        first.species = "dog";
        first.age = 4;

        Pet second = new Pet();
        second.name = "Mochi";
        second.species = "cat";
        second.age = 2;

        first.haveBirthday();
        first.introduce();
        second.introduce();
    }
}
"""

PED1 = """public class Pedometer {
    public String owner;
    public int steps;

    public void walk(int count) {
        steps = steps + count;
    }
}
"""
PED2 = PED1.replace("""        steps = steps + count;
    }
}
""", """        steps = steps + count;
    }

    public void report() {
        System.out.println(owner + " walked " + steps + " steps.");
    }
}
""")
PED3 = """public class Pedometer {
    public String owner;
    public int steps;
    public int goal;

    public void walk(int count) {
        steps = steps + count;
    }

    public void report() {
        System.out.println(owner + " walked " + steps + " steps.");
    }

    public boolean reachedGoal() {
        return steps >= goal;
    }
}
"""
WT1 = """public class WalkTester {
    public static void main(String[] args) {
        Pedometer ana = new Pedometer();
        ana.owner = "Ana";
        ana.walk(500);
        ana.walk(700);
        System.out.println(ana.owner + ": " + ana.steps);
    }
}
"""
WT2 = WT1.replace("""        System.out.println(ana.owner + ": " + ana.steps);""", """        ana.report();""")
WT3 = """public class WalkTester {
    public static void main(String[] args) {
        Pedometer ana = new Pedometer();
        ana.owner = "Ana";
        ana.goal = 1000;
        ana.walk(500);
        ana.walk(700);
        ana.report();
        System.out.println(ana.reachedGoal());

        Pedometer sam = new Pedometer();
        sam.owner = "Sam";
        sam.goal = 5000;
        sam.walk(4999);
        sam.report();
        System.out.println(sam.reachedGoal());
    }
}
"""

LESSON = workshop(
    "ws-intro-oop", "Workshop: introduction to OOP",
    "Practice writing classes with fields and methods, creating objects with `new`, and keeping each object's values separate.",
    ["Write a class with fields and methods from an empty file",
     "Create several objects and call methods on each",
     "Write methods that change an object's fields or answer a question about them"],
    guided("ws-u2-pets", "A pet tracker", "Build a `Pet` class step by step, then use two pets that keep their own values.", [
        step("Fields", "Create `Pet.java` with public fields `name`, `species` (both `String`) and `age` (`int`). Create `PetTester.java`, make one pet, set its fields, and print a sentence about it.",
             {"Pet.java": PET1, "PetTester.java": PT1}, "PetTester", "Biscuit is a dog.",
             hint="`Pet first = new Pet();` then `first.name = \"Biscuit\";` and so on.",
             checks=[{"pattern": r"new\s+Pet\s*\(", "message": "Create the pet with `new Pet()`."}]),
        step("A method", "Add a method `introduce()` to `Pet` that prints `I'm <name>, a <age>-year-old <species>.` Replace the tester's `println` with a call to it.",
             {"Pet.java": PET2, "PetTester.java": PT2}, "PetTester", "I'm Biscuit, a 4-year-old dog.",
             hint="Inside `introduce()`, use the fields directly: `name`, `age`, `species`."),
        step("Two pets", "Add `haveBirthday()`, which adds one to `age`. Make a second pet, Mochi, a 2-year-old cat. Give Biscuit a birthday, then introduce both.",
             {"Pet.java": PET3, "PetTester.java": PT3}, "PetTester",
             "I'm Biscuit, a 5-year-old dog.\nI'm Mochi, a 2-year-old cat.",
             hint="Only Biscuit gets older, because `haveBirthday()` changes the fields of the object it's called on."),
    ]),
    guided("ws-u2-steps", "A step counter", "Build a `Pedometer` whose methods change and report its own count.", [
        step("Counting", "Create `Pedometer.java` with public `owner` and `steps`, and a method `walk(int count)` that adds to `steps`. In `WalkTester`, walk 500 and then 700 steps and print the owner and total.",
             {"Pedometer.java": PED1, "WalkTester.java": WT1}, "WalkTester", "Ana: 1200",
             hint="`steps` starts at 0 by itself: the default for an `int` field."),
        step("Reporting", "Add `report()`, which prints `<owner> walked <steps> steps.`, and use it in the tester.",
             {"Pedometer.java": PED2, "WalkTester.java": WT2}, "WalkTester", "Ana walked 1200 steps."),
        step("A goal", "Add a public `int goal` and a method `reachedGoal()` that returns `true` when the steps are at least the goal. Test it with two people, one who reaches the goal and one who misses by a single step.",
             {"Pedometer.java": PED3, "WalkTester.java": WT3}, "WalkTester",
             "Ana walked 1200 steps.\ntrue\nSam walked 4999 steps.\nfalse",
             hint="`return steps >= goal;` A comparison is already a `boolean`."),
    ]),
    task("ws-u2-thermo", "A thermometer",
         "Write `Thermometer` with a public `double celsius`, a method `fahrenheit()` that returns celsius × 9 ÷ 5 + 32, and `describe()`, which prints `<celsius> C is <fahrenheit> F`. In `ThermoTester`, describe 20.0 and then 37.5 degrees using the same object.",
         {"Thermometer.java": """public class Thermometer {
    public double celsius;

    public double fahrenheit() {
        return celsius * 9 / 5 + 32;
    }

    public void describe() {
        System.out.println(celsius + " C is " + fahrenheit() + " F");
    }
}
""", "ThermoTester.java": """public class ThermoTester {
    public static void main(String[] args) {
        Thermometer t = new Thermometer();
        t.celsius = 20.0;
        t.describe();
        t.celsius = 37.5;
        t.describe();
    }
}
"""}, "ThermoTester", "20.0 C is 68.0 F\n37.5 C is 99.5 F",
         tests={"CheckThermo.java": """public class CheckThermo {
    public static void main(String[] args) {
        Thermometer t = new Thermometer();
        t.celsius = -40.0;
        System.out.println(t.fahrenheit());
        t.celsius = 100.0;
        System.out.println(t.fahrenheit());
    }
}
"""}, tests_run="CheckThermo", tests_output="-40.0\n212.0",
         hints=["`describe()` can call `fahrenheit()` on the same object."]),
    task("ws-u2-score", "A scoreboard",
         "Write `Scoreboard` with public `int` fields `home` and `away`, methods `homeScores(int points)` and `awayScores(int points)`, and `leader()`, which returns `\"Home\"`, `\"Away\"` or `\"Tied\"`.",
         {"Scoreboard.java": """public class Scoreboard {
    public int home;
    public int away;

    public void homeScores(int points) {
        home = home + points;
    }

    public void awayScores(int points) {
        away = away + points;
    }

    public String leader() {
        if (home > away) {
            return "Home";
        } else if (away > home) {
            return "Away";
        }
        return "Tied";
    }
}
""", "GameTester.java": """public class GameTester {
    public static void main(String[] args) {
        Scoreboard game = new Scoreboard();
        game.homeScores(3);
        game.awayScores(7);
        System.out.println(game.leader());
        game.homeScores(4);
        System.out.println(game.leader());
        System.out.println(game.home + "-" + game.away);
    }
}
"""}, "GameTester", "Away\nTied\n7-7",
         tests={"CheckScore.java": """public class CheckScore {
    public static void main(String[] args) {
        Scoreboard s = new Scoreboard();
        System.out.println(s.leader());
        s.homeScores(2);
        System.out.println(s.leader());
    }
}
"""}, tests_run="CheckScore", tests_output="Tied\nHome",
         hints=["A new scoreboard is 0-0, so it should say `Tied`."]),
    [CLASSES_TUT, OBJECTS_TUT, FIELDS_TUT, HEL_4_1],
)
