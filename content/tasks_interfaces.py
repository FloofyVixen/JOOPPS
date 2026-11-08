"""Write-it-yourself tasks for Interfaces vs Objects. Compiled and run by build.py."""
from tasks_classes import task

IMPL = lambda cls, iface: {"pattern": r"class\s+" + cls + r"\b[^{]*implements[^{]*\b" + iface + r"\b",
                           "message": f"`{cls}` should implement `{iface}`."}
IFACE = lambda name: {"pattern": r"interface\s+" + name, "message": f"Declare `{name}` as an `interface`."}

BASICS = [
    task("w-describable", "One interface, two classes",
         "Write an interface `Describable` with one method, `String describe()`. Write `City` (private `name` and `population`) and `River` (private `name` and `lengthKm`), both implementing it: a city describes itself as `Bangor, population 31000` and a river as `Penobscot River, 350 km`.",
         {"Describable.java": """public interface Describable {
    String describe();
}
""", "City.java": """public class City implements Describable {
    private String name;
    private int population;

    public City(String name, int population) {
        this.name = name;
        this.population = population;
    }

    @Override
    public String describe() {
        return name + ", population " + population;
    }
}
""", "River.java": """public class River implements Describable {
    private String name;
    private int lengthKm;

    public River(String name, int lengthKm) {
        this.name = name;
        this.lengthKm = lengthKm;
    }

    @Override
    public String describe() {
        return name + " River, " + lengthKm + " km";
    }
}
""", "MapTester.java": """public class MapTester {
    public static void main(String[] args) {
        System.out.println(new City("Bangor", 31000).describe());
        System.out.println(new River("Penobscot", 350).describe());
    }
}
"""}, "MapTester", "Bangor, population 31000\nPenobscot River, 350 km",
         tests={"CheckMap.java": """public class CheckMap {
    public static void main(String[] args) {
        Describable d = new River("Kennebec", 270);
        System.out.println(d.describe());
    }
}
"""}, tests_run="CheckMap", tests_output="Kennebec River, 270 km",
         checks=[IFACE("Describable"), IMPL("City", "Describable"), IMPL("River", "Describable")]),

    task("w-balloon", "An interface with two methods",
         "Write an interface `Resizable` with `void grow(int amount)` and `void shrink(int amount)`. `Balloon` implements it with a private `size` that starts at 10; shrinking can't take the size below 1. Add `getSize()`.",
         {"Resizable.java": """public interface Resizable {
    void grow(int amount);

    void shrink(int amount);
}
""", "Balloon.java": """public class Balloon implements Resizable {
    private int size;

    public Balloon() {
        size = 10;
    }

    public int getSize() {
        return size;
    }

    @Override
    public void grow(int amount) {
        size = size + amount;
    }

    @Override
    public void shrink(int amount) {
        size = size - amount;
        if (size < 1) {
            size = 1;
        }
    }
}
""", "BalloonTester.java": """public class BalloonTester {
    public static void main(String[] args) {
        Balloon b = new Balloon();
        b.grow(5);
        System.out.println(b.getSize());
        b.shrink(100);
        System.out.println(b.getSize());
    }
}
"""}, "BalloonTester", "15\n1",
         tests={"CheckBalloon.java": """public class CheckBalloon {
    public static void main(String[] args) {
        Balloon b = new Balloon();
        b.shrink(9);
        System.out.println(b.getSize());
        Resizable r = b;
        r.grow(4);
        System.out.println(b.getSize());
    }
}
"""}, tests_run="CheckBalloon", tests_output="1\n5",
         checks=[IFACE("Resizable"), IMPL("Balloon", "Resizable")]),

    task("w-speedlimit", "An interface constant",
         "Write an interface `Speedy` with a constant `int MAX_SPEED = 100;` and a method `void accelerate(int amount)`. `Scooter` implements it with a private `speed` that starts at 0 and never goes above `MAX_SPEED`. Add `getSpeed()`.",
         {"Speedy.java": """public interface Speedy {
    int MAX_SPEED = 100;

    void accelerate(int amount);
}
""", "Scooter.java": """public class Scooter implements Speedy {
    private int speed;

    public int getSpeed() {
        return speed;
    }

    @Override
    public void accelerate(int amount) {
        speed = speed + amount;
        if (speed > MAX_SPEED) {
            speed = MAX_SPEED;
        }
    }
}
""", "ScooterTester.java": """public class ScooterTester {
    public static void main(String[] args) {
        Scooter s = new Scooter();
        s.accelerate(30);
        System.out.println(s.getSpeed());
        s.accelerate(500);
        System.out.println(s.getSpeed());
        System.out.println("Limit: " + Speedy.MAX_SPEED);
    }
}
"""}, "ScooterTester", "30\n100\nLimit: 100",
         tests={"CheckScooter.java": """public class CheckScooter {
    public static void main(String[] args) {
        Scooter s = new Scooter();
        s.accelerate(100);
        System.out.println(s.getSpeed());
    }
}
"""}, tests_run="CheckScooter", tests_output="100",
         hints=["A constant in an interface is automatically `public static final`. Inside `Scooter` you can use the name `MAX_SPEED` directly; elsewhere, write `Speedy.MAX_SPEED`."],
         checks=[{"pattern": r"MAX_SPEED\s*=\s*100", "message": "Declare the constant `int MAX_SPEED = 100;` in `Speedy`."},
                 {"pattern": r">\s*MAX_SPEED", "message": "Use the constant `MAX_SPEED` in `Scooter` instead of typing 100."}]),
]

MULTIPLE = [
    task("w-duck", "Extend one, implement two",
         "Write a class `Bird` (private `name`, `getName()`), and interfaces `Swimmer` (`void swim()`) and `Flyer` (`void fly()`). Write `Duck extends Bird implements Swimmer, Flyer`: it prints `<name> paddles.` and `<name> flies south.`",
         {"Bird.java": """public class Bird {
    private String name;

    public Bird(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
""", "Swimmer.java": """public interface Swimmer {
    void swim();
}
""", "Flyer.java": """public interface Flyer {
    void fly();
}
""", "Duck.java": """public class Duck extends Bird implements Swimmer, Flyer {
    public Duck(String name) {
        super(name);
    }

    @Override
    public void swim() {
        System.out.println(getName() + " paddles.");
    }

    @Override
    public void fly() {
        System.out.println(getName() + " flies south.");
    }
}
""", "PondTester.java": """public class PondTester {
    public static void main(String[] args) {
        Duck daisy = new Duck("Daisy");
        daisy.swim();
        daisy.fly();
    }
}
"""}, "PondTester", "Daisy paddles.\nDaisy flies south.",
         tests={"CheckDuck.java": """public class CheckDuck {
    public static void main(String[] args) {
        Swimmer s = new Duck("Quack");
        s.swim();
        Flyer f = new Duck("Mallard");
        f.fly();
        Bird b = new Duck("Teal");
        System.out.println(b.getName());
    }
}
"""}, tests_run="CheckDuck", tests_output="Quack paddles.\nMallard flies south.\nTeal",
         checks=[{"pattern": r"class\s+Duck\s+extends\s+Bird\s+implements", "message": "Write `class Duck extends Bird implements Swimmer, Flyer`."}]),

    task("w-robot", "Two interfaces, no superclass",
         "Write interfaces `Walker` (`void walk(int steps)`) and `Talker` (`void say(String words)`), and a `Robot` with a private `model` that implements both: it prints `<model> walks <steps> steps.` and `<model> says: <words>`.",
         {"Walker.java": """public interface Walker {
    void walk(int steps);
}
""", "Talker.java": """public interface Talker {
    void say(String words);
}
""", "Robot.java": """public class Robot implements Walker, Talker {
    private String model;

    public Robot(String model) {
        this.model = model;
    }

    @Override
    public void walk(int steps) {
        System.out.println(model + " walks " + steps + " steps.");
    }

    @Override
    public void say(String words) {
        System.out.println(model + " says: " + words);
    }
}
""", "RobotTester.java": """public class RobotTester {
    public static void main(String[] args) {
        Robot r = new Robot("RX-7");
        r.walk(3);
        r.say("Hello");
    }
}
"""}, "RobotTester", "RX-7 walks 3 steps.\nRX-7 says: Hello",
         tests={"CheckRobot.java": """public class CheckRobot {
    public static void main(String[] args) {
        Talker t = new Robot("Tin");
        t.say("Beep");
        Walker w = new Robot("Bolt");
        w.walk(1);
    }
}
"""}, tests_run="CheckRobot", tests_output="Tin says: Beep\nBolt walks 1 steps.",
         checks=[IMPL("Robot", "Walker"), IMPL("Robot", "Talker")]),

    task("w-fix-printer", "Fix the broken promise",
         "`OfficeMachine` promises to be both a `Printer` and a `Scanner2`, but it doesn't compile. Read the messages, fix the class (don't change the interfaces), and make the tester's output match.",
         {"Printer.java": """public interface Printer {
    void print(String doc);
}
""", "Scanner2.java": """public interface Scanner2 {
    String scan();
}
""", "OfficeMachine.java": """public class OfficeMachine implements Printer, Scanner2 {
    @Override
    public void print(String doc) {
        System.out.println("Printing " + doc);
    }

    @Override
    public String scan() {
        return "scanned page";
    }
}
""", "OfficeTester.java": """public class OfficeTester {
    public static void main(String[] args) {
        OfficeMachine m = new OfficeMachine();
        m.print("report.pdf");
        System.out.println(m.scan());
    }
}
"""}, "OfficeTester", "Printing report.pdf\nscanned page",
         requirements=["Change only `OfficeMachine.java`"],
         hints=["There are two problems: one method isn't `public`, and the other returns the wrong type for what `Scanner2` promises."]),
]
MULTIPLE[2]["starter"] = {
    "Printer.java": MULTIPLE[2]["solution"]["Printer.java"],
    "Scanner2.java": MULTIPLE[2]["solution"]["Scanner2.java"],
    "OfficeMachine.java": """public class OfficeMachine implements Printer, Scanner2 {
    @Override
    void print(String doc) {
        System.out.println("Printing " + doc);
    }

    @Override
    public void scan() {
        System.out.println("scanned page");
    }
}
""",
    "OfficeTester.java": MULTIPLE[2]["solution"]["OfficeTester.java"],
}

CHARGE = """public interface Chargeable {
    void charge(int minutes);

    int batteryPercent();
}
"""

TYPE = [
    task("w-priced", "A method for anything with a price",
         "Write an interface `Priced` (`double price()`), and two unrelated classes that implement it: `Ticket` (always 12.5) and `Snack` (private `price` set by the constructor). Write `Till` with `public static double total(Priced[] items)`.",
         {"Priced.java": """public interface Priced {
    double price();
}
""", "Ticket.java": """public class Ticket implements Priced {
    @Override
    public double price() {
        return 12.5;
    }
}
""", "Snack.java": """public class Snack implements Priced {
    private double price;

    public Snack(double price) {
        this.price = price;
    }

    @Override
    public double price() {
        return price;
    }
}
""", "Till.java": """public class Till {
    public static double total(Priced[] items) {
        double sum = 0;
        for (Priced p : items) {
            sum = sum + p.price();
        }
        return sum;
    }

    public static void main(String[] args) {
        Priced[] order = {new Ticket(), new Snack(4.0), new Ticket(), new Snack(3.5)};
        System.out.println("Total: $" + total(order));
    }
}
"""}, "Till", "Total: $32.5",
         tests={"CheckTill.java": """public class CheckTill {
    public static void main(String[] args) {
        Priced[] none = {};
        System.out.println(Till.total(none));
        Priced[] one = {new Snack(2.25)};
        System.out.println(Till.total(one));
    }
}
"""}, tests_run="CheckTill", tests_output="0.0\n2.25",
         checks=[{"pattern": r"total\s*\(\s*Priced\s*\[\s*\]\s*\w+\s*\)", "message": "Give `total` a parameter of type `Priced[]`."}]),

    task("w-count-chargeable", "Which objects have the ability?",
         "Using the `Chargeable` interface (given), write `Phone` and `Watch` that implement it (battery starts at the value given, `charge` adds the minutes but never past 100), and `Kettle`, which doesn't. In `Gadgets`, loop over an `Object[]` holding a phone, a kettle and a watch, and count how many are `Chargeable`.",
         {"Chargeable.java": CHARGE, "Phone.java": """public class Phone implements Chargeable {
    private int battery;

    public Phone(int battery) {
        this.battery = battery;
    }

    @Override
    public void charge(int minutes) {
        battery = Math.min(100, battery + minutes);
    }

    @Override
    public int batteryPercent() {
        return battery;
    }
}
""", "Watch.java": """public class Watch implements Chargeable {
    private int battery;

    public Watch(int battery) {
        this.battery = battery;
    }

    @Override
    public void charge(int minutes) {
        battery = Math.min(100, battery + minutes);
    }

    @Override
    public int batteryPercent() {
        return battery;
    }
}
""", "Kettle.java": """public class Kettle {
    public void boil() {
        System.out.println("Boiling");
    }
}
""", "Gadgets.java": """public class Gadgets {
    public static void main(String[] args) {
        Object[] things = {new Phone(40), new Kettle(), new Watch(90)};
        int count = 0;
        for (Object o : things) {
            if (o instanceof Chargeable) {
                count++;
            }
        }
        System.out.println(count + " chargeable");
    }
}
"""}, "Gadgets", "2 chargeable",
         tests={"CheckGadgets.java": """public class CheckGadgets {
    public static void main(String[] args) {
        Chargeable w = new Watch(95);
        w.charge(20);
        System.out.println(w.batteryPercent());
        Object k = new Kettle();
        System.out.println(k instanceof Chargeable);
    }
}
"""}, tests_run="CheckGadgets", tests_output="100\nfalse",
         checks=[{"pattern": r"instanceof\s+Chargeable", "message": "Count with `instanceof Chargeable`."}]),

    task("w-object-vs-iface", "Interface type versus Object",
         "Write an interface `Named` (`String name()`) and a class `Team` that implements it. In `Labels`, write two static methods: `label(Named n)` returns `Name: ` plus the name, and `show(Object o)` returns `Object: ` plus `o.toString()`. `Team`'s `toString` returns `Team <name>`.",
         {"Named.java": """public interface Named {
    String name();
}
""", "Team.java": """public class Team implements Named {
    private String name;

    public Team(String name) {
        this.name = name;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public String toString() {
        return "Team " + name;
    }
}
""", "Labels.java": """public class Labels {
    public static String label(Named n) {
        return "Name: " + n.name();
    }

    public static String show(Object o) {
        return "Object: " + o.toString();
    }

    public static void main(String[] args) {
        Team bears = new Team("Black Bears");
        System.out.println(label(bears));
        System.out.println(show(bears));
        System.out.println(show("just text"));
    }
}
"""}, "Labels", "Name: Black Bears\nObject: Team Black Bears\nObject: just text",
         tests={"CheckLabels.java": """public class CheckLabels {
    public static void main(String[] args) {
        Named n = new Team("Owls");
        System.out.println(Labels.label(n));
        System.out.println(Labels.show(n));
    }
}
"""}, tests_run="CheckLabels", tests_output="Name: Owls\nObject: Team Owls",
         hints=["`show` accepts anything, even a `String`, but can only call `Object` methods like `toString()`. `label` accepts only `Named` things, but can call `name()`."]),
]

COMPARABLE = [
    task("w-sort-books", "Sort by a number",
         "Write `Book implements Comparable<Book>` with private `title` and `pages`, ordered by page count (fewest first), and a `toString` like `Short Stories (120 pages)`. In `Shelf`, sort three books with `Arrays.sort` and print them.",
         {"Book.java": """public class Book implements Comparable<Book> {
    private String title;
    private int pages;

    public Book(String title, int pages) {
        this.title = title;
        this.pages = pages;
    }

    @Override
    public int compareTo(Book other) {
        return Integer.compare(pages, other.pages);
    }

    @Override
    public String toString() {
        return title + " (" + pages + " pages)";
    }
}
""", "Shelf.java": """import java.util.Arrays;

public class Shelf {
    public static void main(String[] args) {
        Book[] books = {new Book("Night Trains", 310), new Book("Short Stories", 120), new Book("The Long Road", 540)};
        Arrays.sort(books);
        for (Book b : books) {
            System.out.println(b);
        }
    }
}
"""}, "Shelf", "Short Stories (120 pages)\nNight Trains (310 pages)\nThe Long Road (540 pages)",
         tests={"CheckBooks.java": """public class CheckBooks {
    public static void main(String[] args) {
        Book a = new Book("A", 50);
        Book b = new Book("B", 60);
        System.out.println(a.compareTo(b) < 0);
        System.out.println(b.compareTo(a) > 0);
        System.out.println(a.compareTo(new Book("C", 50)) == 0);
    }
}
"""}, tests_run="CheckBooks", tests_output="true\ntrue\ntrue",
         hints=["Start the tester file with `import java.util.Arrays;`."],
         checks=[IMPL("Book", "Comparable")]),

    task("w-fastest", "Find the smallest with compareTo",
         "Write `Runner implements Comparable<Runner>` with private `name` and `double minutes`, ordered by time (fastest first; use `Double.compare`). In `Race`, find the fastest runner with a loop that uses `compareTo`, without sorting.",
         {"Runner.java": """public class Runner implements Comparable<Runner> {
    private String name;
    private double minutes;

    public Runner(String name, double minutes) {
        this.name = name;
        this.minutes = minutes;
    }

    @Override
    public int compareTo(Runner other) {
        return Double.compare(minutes, other.minutes);
    }

    @Override
    public String toString() {
        return name + " " + minutes;
    }
}
""", "Race.java": """public class Race {
    public static Runner fastest(Runner[] runners) {
        Runner best = runners[0];
        for (Runner r : runners) {
            if (r.compareTo(best) < 0) {
                best = r;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        Runner[] field = {new Runner("Ana", 22.5), new Runner("Sam", 19.75), new Runner("Lee", 24.0)};
        System.out.println("Fastest: " + fastest(field));
    }
}
"""}, "Race", "Fastest: Sam 19.75",
         tests={"CheckRace.java": """public class CheckRace {
    public static void main(String[] args) {
        Runner[] one = {new Runner("Solo", 30.0)};
        System.out.println(Race.fastest(one));
        Runner[] tie = {new Runner("First", 20.0), new Runner("Second", 20.0)};
        System.out.println(Race.fastest(tie));
    }
}
"""}, tests_run="CheckRace", tests_output="Solo 30.0\nFirst 20.0",
         hints=["`Double.compare(a, b)` is the `double` version of `Integer.compare`.",
                "Replace `best` only when the runner is strictly faster (`< 0`), so the first of two tied runners wins."]),

    task("w-words", "Compare by two things",
         "Write `Word implements Comparable<Word>` with a private `text`. Shorter words come first; words of the same length are ordered alphabetically (use `String`'s own `compareTo`). `toString` returns the text. Sort and print five words.",
         {"Word.java": """public class Word implements Comparable<Word> {
    private String text;

    public Word(String text) {
        this.text = text;
    }

    @Override
    public int compareTo(Word other) {
        if (text.length() != other.text.length()) {
            return Integer.compare(text.length(), other.text.length());
        }
        return text.compareTo(other.text);
    }

    @Override
    public String toString() {
        return text;
    }
}
""", "WordSort.java": """import java.util.Arrays;

public class WordSort {
    public static void main(String[] args) {
        Word[] words = {new Word("pear"), new Word("fig"), new Word("apple"), new Word("kiwi"), new Word("date")};
        Arrays.sort(words);
        for (Word w : words) {
            System.out.println(w);
        }
    }
}
"""}, "WordSort", "fig\ndate\nkiwi\npear\napple",
         tests={"CheckWords.java": """public class CheckWords {
    public static void main(String[] args) {
        System.out.println(new Word("bb").compareTo(new Word("aaa")) < 0);
        System.out.println(new Word("bb").compareTo(new Word("ab")) > 0);
    }
}
"""}, tests_run="CheckWords", tests_output="true\ntrue",
         hints=["Compare lengths first. Only when they're equal, fall back to `text.compareTo(other.text)`."]),
]

TASKS = {"iface-basics": BASICS, "iface-multiple": MULTIPLE, "iface-type": TYPE, "iface-comparable": COMPARABLE}
