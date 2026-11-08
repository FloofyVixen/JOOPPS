"""Write-it-yourself tasks for the Classes and objects section.
Every solution and test file here is compiled and run by build.py."""


def task(id, title, goal, solution, run, output, tests=None, tests_run=None, tests_output=None,
         requirements=(), hints=(), checks=()):
    t = {"type": "write", "id": id, "mode": "independent", "title": title, "goal": goal,
         "files": list(solution), "solution": solution, "run": run, "output": output,
         "requirements": list(requirements), "hints": list(hints), "checks": list(checks)}
    if tests:
        t.update({"tests": tests, "tests_run": tests_run, "tests_output": tests_output})
    return t


# ---------------------------------------------------------------- first class
FIRST = [
    task("w-planet", "A class with fields and a method",
         "Write a `Planet` class with two public fields, `name` (`String`) and `moons` (`int`), and a method `describe()` that prints `Moons of <name>: <moons>`. Then write `PlanetTester`, whose `main` makes two planets and calls `describe()` on each.",
         {"Planet.java": """public class Planet {
    public String name;
    public int moons;

    public void describe() {
        System.out.println("Moons of " + name + ": " + moons);
    }
}
""", "PlanetTester.java": """public class PlanetTester {
    public static void main(String[] args) {
        Planet first = new Planet();
        first.name = "Earth";
        first.moons = 1;

        Planet second = new Planet();
        second.name = "Mars";
        second.moons = 2;

        first.describe();
        second.describe();
    }
}
"""}, "PlanetTester", "Moons of Earth: 1\nMoons of Mars: 2",
         tests={"CheckPlanet.java": """public class CheckPlanet {
    public static void main(String[] args) {
        Planet p = new Planet();
        p.name = "Testworld";
        p.moons = 16;
        p.describe();

        Planet q = new Planet();
        q.name = "Emptyworld";
        q.describe();
    }
}
"""}, tests_run="CheckPlanet", tests_output="Moons of Testworld: 16\nMoons of Emptyworld: 0",
         requirements=["Two files: `Planet.java` and `PlanetTester.java`",
                       "`describe()` has no `static` and uses the object's own fields"],
         hints=["`Planet` is like `Song` in the lesson: fields at the top, then the method.",
                "In the tester, `Planet first = new Planet();` then set `first.name` and `first.moons`."],
         checks=[{"pattern": r"new\s+Planet\s*\(", "message": "Create `Planet` objects with `new Planet()`."}]),

    task("w-counter", "Objects keep their own values",
         "Write a `Counter` class with a public `int` field `count` and two methods: `click()` adds one to `count`, and `reset()` sets it back to 0. In `CounterTester`, click counter `a` three times and counter `b` once, print both, then reset only `a` and print both again.",
         {"Counter.java": """public class Counter {
    public int count;

    public void click() {
        count = count + 1;
    }

    public void reset() {
        count = 0;
    }
}
""", "CounterTester.java": """public class CounterTester {
    public static void main(String[] args) {
        Counter a = new Counter();
        Counter b = new Counter();
        a.click();
        a.click();
        a.click();
        b.click();
        System.out.println("a: " + a.count);
        System.out.println("b: " + b.count);

        a.reset();
        System.out.println("a after reset: " + a.count);
        System.out.println("b after reset: " + b.count);
    }
}
"""}, "CounterTester", "a: 3\nb: 1\na after reset: 0\nb after reset: 1",
         tests={"CheckCounter.java": """public class CheckCounter {
    public static void main(String[] args) {
        Counter c = new Counter();
        for (int i = 0; i < 5; i++) {
            c.click();
        }
        System.out.println("after 5 clicks: " + c.count);
        c.reset();
        c.click();
        System.out.println("after reset and 1 click: " + c.count);
    }
}
"""}, tests_run="CheckCounter", tests_output="after 5 clicks: 5\nafter reset and 1 click: 1",
         requirements=["Resetting `a` must not change `b`"],
         hints=["Inside `click()`, `count = count + 1;` changes the count of whichever object you called it on."]),

    task("w-lamp", "A boolean field",
         "Write a `Lamp` class with a public `boolean` field `on`, a method `toggle()` that switches it, and a method `showStatus()` that prints `The lamp is on.` or `The lamp is off.` In `LampTester`, show the status, toggle, show it, toggle twice more, and show it again.",
         {"Lamp.java": """public class Lamp {
    public boolean on;

    public void toggle() {
        on = !on;
    }

    public void showStatus() {
        if (on) {
            System.out.println("The lamp is on.");
        } else {
            System.out.println("The lamp is off.");
        }
    }
}
""", "LampTester.java": """public class LampTester {
    public static void main(String[] args) {
        Lamp desk = new Lamp();
        desk.showStatus();
        desk.toggle();
        desk.showStatus();
        desk.toggle();
        desk.toggle();
        desk.showStatus();
    }
}
"""}, "LampTester", "The lamp is off.\nThe lamp is on.\nThe lamp is on.",
         tests={"CheckLamp.java": """public class CheckLamp {
    public static void main(String[] args) {
        Lamp a = new Lamp();
        Lamp b = new Lamp();
        a.toggle();
        a.showStatus();
        b.showStatus();
    }
}
"""}, tests_run="CheckLamp", tests_output="The lamp is on.\nThe lamp is off.",
         requirements=["A new lamp starts off (remember the default value of a `boolean` field)"],
         hints=["`!` means \"not\": `on = !on;` makes `on` the opposite of what it was.",
                "You can also write it with `if (on) { on = false; } else { on = true; }`."]),
]

# ---------------------------------------------------------------- constructors
CONSTRUCTORS = [
    task("w-concert", "A parameterized constructor",
         "Write a `Concert` class with public fields `artist`, `city` (both `String`) and `year` (`int`), a constructor that takes all three, and a `describe()` method. In `ConcertTester`, create two concerts in one line each and describe them.",
         {"Concert.java": """public class Concert {
    public String artist;
    public String city;
    public int year;

    public Concert(String artist, String city, int year) {
        this.artist = artist;
        this.city = city;
        this.year = year;
    }

    public void describe() {
        System.out.println(artist + " in " + city + " (" + year + ")");
    }
}
""", "ConcertTester.java": """public class ConcertTester {
    public static void main(String[] args) {
        Concert one = new Concert("Mira Holt", "Bangor", 2026);
        Concert two = new Concert("The Lanterns", "Portland", 2027);
        one.describe();
        two.describe();
    }
}
"""}, "ConcertTester", "Mira Holt in Bangor (2026)\nThe Lanterns in Portland (2027)",
         tests={"CheckConcert.java": """public class CheckConcert {
    public static void main(String[] args) {
        Concert c = new Concert("Kesh", "Orono", 2030);
        c.describe();
        System.out.println("city field: " + c.city);
    }
}
"""}, tests_run="CheckConcert", tests_output="Kesh in Orono (2030)\ncity field: Orono",
         requirements=["The constructor's parameters are in the order artist, city, year",
                       "Use `this.` to store each parameter in its field"],
         hints=["If the output says `null in null (0)`, look for a missing `this.` in the constructor."],
         checks=[{"pattern": r"this\.\w+\s*=", "message": "Store the parameters with `this.field = parameter;`."}]),

    task("w-rectangle", "Two constructors",
         "Write a `Rectangle` class with public `int` fields `width` and `height`. Give it a default constructor that makes a 1 by 1 rectangle, a constructor that takes the width and height, and a method `area()` that returns the area.",
         {"Rectangle.java": """public class Rectangle {
    public int width;
    public int height;

    public Rectangle() {
        width = 1;
        height = 1;
    }

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public int area() {
        return width * height;
    }
}
""", "RectangleTester.java": """public class RectangleTester {
    public static void main(String[] args) {
        Rectangle unit = new Rectangle();
        Rectangle big = new Rectangle(4, 5);
        System.out.println("unit: " + unit.area());
        System.out.println("big: " + big.area());
    }
}
"""}, "RectangleTester", "unit: 1\nbig: 20",
         tests={"CheckRectangle.java": """public class CheckRectangle {
    public static void main(String[] args) {
        System.out.println("area of 3 x 7: " + new Rectangle(3, 7).area());
        Rectangle d = new Rectangle();
        System.out.println("default: " + d.width + " x " + d.height);
    }
}
"""}, tests_run="CheckRectangle", tests_output="area of 3 x 7: 21\ndefault: 1 x 1",
         requirements=["Both constructors are named exactly like the class and have no return type",
                       "`area()` returns an `int`; it doesn't print"]),

    task("w-player", "A constructor that sets a starting value",
         "Write a `Player` class with public fields `name` and `score`. The constructor takes only the name; every player starts with a score of 0. Add `addPoints(int points)`.",
         {"Player.java": """public class Player {
    public String name;
    public int score;

    public Player(String name) {
        this.name = name;
        score = 0;
    }

    public void addPoints(int points) {
        score = score + points;
    }
}
""", "PlayerTester.java": """public class PlayerTester {
    public static void main(String[] args) {
        Player sam = new Player("Sam");
        sam.addPoints(10);
        sam.addPoints(5);
        Player ana = new Player("Ana");
        System.out.println(sam.name + ": " + sam.score);
        System.out.println(ana.name + ": " + ana.score);
    }
}
"""}, "PlayerTester", "Sam: 15\nAna: 0",
         tests={"CheckPlayer.java": """public class CheckPlayer {
    public static void main(String[] args) {
        Player p = new Player("Lee");
        p.addPoints(7);
        p.addPoints(7);
        System.out.println(p.name + ": " + p.score);
    }
}
"""}, tests_run="CheckPlayer", tests_output="Lee: 14",
         requirements=["`new Player(\"Sam\")` is the only constructor call you need"],
         hints=["A constructor can set fields that aren't parameters: `score = 0;`"]),
]

# ---------------------------------------------------------------- toString
TOSTRING = [
    task("w-point", "A toString with punctuation",
         "Write a `Point` class with public `int` fields `x` and `y`, a constructor, and a `toString` that returns the point as `(3, 4)`.",
         {"Point.java": """public class Point {
    public int x;
    public int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}
""", "PointTester.java": """public class PointTester {
    public static void main(String[] args) {
        System.out.println(new Point(3, 4));
        Point start = new Point(-2, 0);
        System.out.println("Start: " + start);
    }
}
"""}, "PointTester", "(3, 4)\nStart: (-2, 0)",
         tests={"CheckPoint.java": """public class CheckPoint {
    public static void main(String[] args) {
        System.out.println(new Point(10, -7));
    }
}
"""}, tests_run="CheckPoint", tests_output="(10, -7)",
         hints=["Build the text from pieces: `\"(\" + x + \", \" + y + \")\"`."],
         checks=[{"pattern": r"public\s+String\s+toString\s*\(\s*\)", "message": "Write `public String toString()`."}]),

    task("w-clock", "A toString with a decision in it",
         "Write a `Clock` class with public fields `hour` and `minute`, a constructor, and a `toString` that returns the time like `9:05` or `14:30`. Minutes below 10 need a leading zero.",
         {"Clock.java": """public class Clock {
    public int hour;
    public int minute;

    public Clock(int hour, int minute) {
        this.hour = hour;
        this.minute = minute;
    }

    @Override
    public String toString() {
        if (minute < 10) {
            return hour + ":0" + minute;
        }
        return hour + ":" + minute;
    }
}
""", "ClockTester.java": """public class ClockTester {
    public static void main(String[] args) {
        System.out.println(new Clock(9, 5));
        System.out.println(new Clock(14, 30));
    }
}
"""}, "ClockTester", "9:05\n14:30",
         tests={"CheckClock.java": """public class CheckClock {
    public static void main(String[] args) {
        System.out.println(new Clock(0, 0));
        System.out.println(new Clock(12, 10));
        System.out.println(new Clock(7, 59));
    }
}
"""}, tests_run="CheckClock", tests_output="0:00\n12:10\n7:59",
         requirements=["`toString` returns the text; it doesn't print"],
         hints=["Use an `if`: when `minute < 10`, put `\"0\"` before it.",
                "The test tries `0:00` and `12:10`. Check both edges of your condition."]),

    task("w-card", "toString inside other text",
         "Write a `Card` class with public `String` fields `rank` and `suit`, a constructor, and a `toString` that returns `Queen of Hearts`. In the tester, print a card on its own and inside a sentence.",
         {"Card.java": """public class Card {
    public String rank;
    public String suit;

    public Card(String rank, String suit) {
        this.rank = rank;
        this.suit = suit;
    }

    @Override
    public String toString() {
        return rank + " of " + suit;
    }
}
""", "CardTester.java": """public class CardTester {
    public static void main(String[] args) {
        Card drawn = new Card("Queen", "Hearts");
        System.out.println("You drew the " + drawn + ".");
        System.out.println(new Card("7", "Clubs"));
    }
}
"""}, "CardTester", "You drew the Queen of Hearts.\n7 of Clubs",
         tests={"CheckCard.java": """public class CheckCard {
    public static void main(String[] args) {
        Card c = new Card("Ace", "Spades");
        String text = c.toString();
        System.out.println(text + " has " + text.length() + " characters");
    }
}
"""}, tests_run="CheckCard", tests_output="Ace of Spades has 13 characters",
         hints=["`\"You drew the \" + drawn + \".\"` calls `toString()` for you."]),
]

# ---------------------------------------------------------------- encapsulation
ENCAPSULATION = [
    task("w-bankaccount", "Private data with checks",
         "Write a `BankAccount` class with a private `double balance`, a constructor that takes the starting balance, `getBalance()`, `deposit(double)` (positive amounts only) and `withdraw(double)` (positive amounts, and never more than the balance). There is no `setBalance`.",
         {"BankAccount.java": """public class BankAccount {
    private double balance;

    public BankAccount(double balance) {
        this.balance = balance;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance = balance + amount;
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance = balance - amount;
        }
    }
}
""", "BankAccountTester.java": """public class BankAccountTester {
    public static void main(String[] args) {
        BankAccount account = new BankAccount(50.0);
        account.deposit(25.0);
        System.out.println("After deposit: " + account.getBalance());
        account.withdraw(100.0);
        System.out.println("After big withdrawal: " + account.getBalance());
        account.withdraw(75.0);
        System.out.println("After withdrawing everything: " + account.getBalance());
    }
}
"""}, "BankAccountTester",
         "After deposit: 75.0\nAfter big withdrawal: 75.0\nAfter withdrawing everything: 0.0",
         tests={"CheckBankAccount.java": """public class CheckBankAccount {
    public static void main(String[] args) {
        BankAccount a = new BankAccount(10.0);
        a.deposit(-5.0);
        System.out.println("deposit(-5): " + a.getBalance());
        a.withdraw(-3.0);
        System.out.println("withdraw(-3): " + a.getBalance());
        a.withdraw(4.0);
        System.out.println("withdraw(4): " + a.getBalance());
    }
}
"""}, tests_run="CheckBankAccount",
         tests_output="deposit(-5): 10.0\nwithdraw(-3): 10.0\nwithdraw(4): 6.0",
         requirements=["`balance` is `private`", "Bad amounts are ignored; the balance doesn't change"],
         hints=["Withdrawing exactly the whole balance is allowed, so compare with `<=`.",
                "The test tries negative amounts. A negative deposit shouldn't lower the balance."],
         checks=[{"pattern": r"private\s+double\s+balance", "message": "Make the field `private double balance`."}]),

    task("w-speaker", "A setter that refuses bad values",
         "Write a `Speaker` class with a private `int volume` that starts at 5. `setVolume` accepts values from 0 to 10; anything else prints `Volume must be 0 to 10.` and leaves the volume unchanged. Add `getVolume()`.",
         {"Speaker.java": """public class Speaker {
    private int volume;

    public Speaker() {
        volume = 5;
    }

    public int getVolume() {
        return volume;
    }

    public void setVolume(int volume) {
        if (volume >= 0 && volume <= 10) {
            this.volume = volume;
        } else {
            System.out.println("Volume must be 0 to 10.");
        }
    }
}
""", "SpeakerTester.java": """public class SpeakerTester {
    public static void main(String[] args) {
        Speaker speaker = new Speaker();
        System.out.println("Start: " + speaker.getVolume());
        speaker.setVolume(8);
        System.out.println("Now: " + speaker.getVolume());
        speaker.setVolume(11);
        System.out.println("Still: " + speaker.getVolume());
    }
}
"""}, "SpeakerTester", "Start: 5\nNow: 8\nVolume must be 0 to 10.\nStill: 8",
         tests={"CheckSpeaker.java": """public class CheckSpeaker {
    public static void main(String[] args) {
        Speaker s = new Speaker();
        s.setVolume(0);
        System.out.println(s.getVolume());
        s.setVolume(-1);
        System.out.println(s.getVolume());
        s.setVolume(10);
        System.out.println(s.getVolume());
    }
}
"""}, tests_run="CheckSpeaker", tests_output="0\nVolume must be 0 to 10.\n0\n10",
         hints=["The parameter and the field are both named `volume`, so the setter needs `this.volume`.",
                "0 and 10 are both allowed. Check that your condition includes them."],
         checks=[{"pattern": r"private\s+int\s+volume", "message": "Make the field `private int volume`."}]),

    task("w-person", "Getters, a setter and a boolean method",
         "Write a `Person` class with private fields `name` and `age`, a constructor, `getName()`, `getAge()`, `setAge(int)` that ignores negative ages, and `isAdult()`, which returns `true` at 18 or older.",
         {"Person.java": """public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        if (age >= 0) {
            this.age = age;
        }
    }

    public boolean isAdult() {
        return age >= 18;
    }
}
""", "PersonTester.java": """public class PersonTester {
    public static void main(String[] args) {
        Person riley = new Person("Riley", 17);
        System.out.println(riley.getName() + " is " + riley.getAge() + ". Adult: " + riley.isAdult());
        riley.setAge(18);
        System.out.println(riley.getName() + " is " + riley.getAge() + ". Adult: " + riley.isAdult());
        riley.setAge(-4);
        System.out.println(riley.getAge());
    }
}
"""}, "PersonTester", "Riley is 17. Adult: false\nRiley is 18. Adult: true\n18",
         tests={"CheckPerson.java": """public class CheckPerson {
    public static void main(String[] args) {
        Person kai = new Person("Kai", 30);
        System.out.println(kai.isAdult());
        kai.setAge(-1);
        System.out.println(kai.getAge());
        System.out.println(new Person("Bo", 0).isAdult());
    }
}
"""}, tests_run="CheckPerson", tests_output="true\n30\nfalse",
         hints=["`isAdult` can return the comparison directly: `return age >= 18;`"],
         checks=[{"pattern": r"private\s+String\s+name", "message": "Make `name` a `private String` field."},
                 {"pattern": r"private\s+int\s+age", "message": "Make `age` a `private int` field."}]),
]

# ---------------------------------------------------------------- arrays of objects
FOOD = """public class Food {
    private String name;
    private int calories;

    public Food(String name, int calories) {
        this.name = name;
        this.calories = calories;
    }

    public String getName() {
        return name;
    }

    public int getCalories() {
        return calories;
    }
}
"""

ANIMAL = """public class Animal {
    private String name;
    private String species;

    public Animal(String name, String species) {
        this.name = name;
        this.species = species;
    }

    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        return name + " the " + species;
    }
}
"""

MESSAGE = """public class Message {
    private String sender;
    private String text;

    public Message(String sender, String text) {
        this.sender = sender;
        this.text = text;
    }

    public String getSender() {
        return sender;
    }
}
"""

ARRAYS = [
    task("w-fridge", "Loop over an array and skip empty slots",
         "Write `Food` (private `name` and `calories`, a constructor and getters) and `Fridge`, which keeps a private `Food[]` whose size is given to its constructor. `Fridge` has `put(int slot, Food food)`, `count()` (how many slots hold food) and `totalCalories()`. Then write `FridgeTester`.",
         {"Food.java": FOOD, "Fridge.java": """public class Fridge {
    private Food[] items;

    public Fridge(int size) {
        items = new Food[size];
    }

    public void put(int slot, Food food) {
        items[slot] = food;
    }

    public int count() {
        int count = 0;
        for (Food food : items) {
            if (food != null) {
                count++;
            }
        }
        return count;
    }

    public int totalCalories() {
        int total = 0;
        for (Food food : items) {
            if (food != null) {
                total = total + food.getCalories();
            }
        }
        return total;
    }
}
""", "FridgeTester.java": """public class FridgeTester {
    public static void main(String[] args) {
        Fridge fridge = new Fridge(5);
        fridge.put(0, new Food("Apple", 95));
        fridge.put(2, new Food("Yogurt", 150));
        fridge.put(4, new Food("Cheese", 110));
        System.out.println("Items: " + fridge.count());
        System.out.println("Calories: " + fridge.totalCalories());
    }
}
"""}, "FridgeTester", "Items: 3\nCalories: 355",
         tests={"CheckFridge.java": """public class CheckFridge {
    public static void main(String[] args) {
        Fridge empty = new Fridge(3);
        System.out.println("empty: " + empty.count() + " items, " + empty.totalCalories() + " calories");
        Fridge one = new Fridge(1);
        one.put(0, new Food("Soup", 200));
        System.out.println("one item: " + one.count() + " items, " + one.totalCalories() + " calories");
    }
}
"""}, tests_run="CheckFridge",
         tests_output="empty: 0 items, 0 calories\none item: 1 items, 200 calories",
         requirements=["Three files: `Food.java`, `Fridge.java`, `FridgeTester.java`",
                       "Both loops check for `null` before using a slot"],
         hints=["Slots 1 and 3 stay empty in the tester. Without a null check, you'll see a `NullPointerException`.",
                "`for (Food food : items)` visits every slot, empty or not."]),

    task("w-zoo", "Search an array of objects",
         "Write `Animal` (private `name` and `species`, a constructor, `getName()`, and a `toString` like `Max the otter`) and `Zoo`, which keeps a private `Animal[]`. `Zoo` has `set(int slot, Animal animal)` and `find(String name)`, which returns the matching animal or `null`.",
         {"Animal.java": ANIMAL, "Zoo.java": """public class Zoo {
    private Animal[] animals;

    public Zoo(int size) {
        animals = new Animal[size];
    }

    public void set(int slot, Animal animal) {
        animals[slot] = animal;
    }

    public Animal find(String name) {
        for (Animal animal : animals) {
            if (animal != null && animal.getName().equals(name)) {
                return animal;
            }
        }
        return null;
    }
}
""", "ZooTester.java": """public class ZooTester {
    public static void main(String[] args) {
        Zoo zoo = new Zoo(3);
        zoo.set(0, new Animal("Rosie", "giraffe"));
        zoo.set(2, new Animal("Max", "otter"));
        System.out.println(zoo.find("Max"));
        System.out.println(zoo.find("Leo"));
    }
}
"""}, "ZooTester", "Max the otter\nnull",
         tests={"CheckZoo.java": """public class CheckZoo {
    public static void main(String[] args) {
        Zoo z = new Zoo(4);
        z.set(3, new Animal("Pip", "penguin"));
        System.out.println(z.find("Pip"));
        System.out.println(z.find("pip"));
    }
}
"""}, tests_run="CheckZoo", tests_output="Pip the penguin\nnull",
         hints=["Compare names with `equals`, not `==`.",
                "Check `animal != null` before calling `getName()`, with `&&` between them."],
         checks=[{"pattern": r"\.equals\s*\(", "message": "Compare the names with `.equals(...)`."}]),

    task("w-inbox", "Fill the first empty slot",
         "Write `Message` (private `sender` and `text`, a constructor, `getSender()`) and `Inbox`, which keeps a private `Message[]`. `receive(Message m)` stores the message in the first empty slot and returns `true`, or returns `false` if the inbox is full. `countFrom(String sender)` counts that sender's messages.",
         {"Message.java": MESSAGE, "Inbox.java": """public class Inbox {
    private Message[] messages;

    public Inbox(int size) {
        messages = new Message[size];
    }

    public boolean receive(Message m) {
        for (int i = 0; i < messages.length; i++) {
            if (messages[i] == null) {
                messages[i] = m;
                return true;
            }
        }
        return false;
    }

    public int countFrom(String sender) {
        int count = 0;
        for (Message m : messages) {
            if (m != null && m.getSender().equals(sender)) {
                count++;
            }
        }
        return count;
    }
}
""", "InboxTester.java": """public class InboxTester {
    public static void main(String[] args) {
        Inbox inbox = new Inbox(4);
        inbox.receive(new Message("Ana", "Hi!"));
        inbox.receive(new Message("Sam", "Lunch?"));
        inbox.receive(new Message("Ana", "See you at 1"));
        System.out.println(inbox.countFrom("Ana"));
        System.out.println(inbox.countFrom("Lee"));
        System.out.println(inbox.receive(new Message("Lee", "Hello")));
        System.out.println(inbox.receive(new Message("Lee", "Anyone?")));
    }
}
"""}, "InboxTester", "2\n0\ntrue\nfalse",
         tests={"CheckInbox.java": """public class CheckInbox {
    public static void main(String[] args) {
        Inbox tiny = new Inbox(1);
        System.out.println(tiny.receive(new Message("X", "one")));
        System.out.println(tiny.receive(new Message("X", "two")));
        System.out.println(tiny.countFrom("X"));
    }
}
"""}, tests_run="CheckInbox", tests_output="true\nfalse\n1",
         hints=["`receive` needs the slot number, so use an index loop and `return true;` as soon as you store the message.",
                "If the loop ends without finding a gap, the inbox is full: `return false;`"]),
]

# ---------------------------------------------------------------- project
CAR = """public class Car {
    private String plate;
    private String model;

    public Car(String plate, String model) {
        this.plate = plate;
        this.model = model;
    }

    @Override
    public String toString() {
        return model + " (" + plate + ")";
    }
}
"""

LOT = """public class ParkingLot {
    private Car[] spots;
    private String name;

    public ParkingLot(String name) {
        this.name = name;
        spots = new Car[6];
    }

    public String getName() {
        return name;
    }

    public int park(Car car) {
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] == null) {
                spots[i] = car;
                return i;
            }
        }
        return -1;
    }

    public Car leave(int spot) {
        if (spot < 0 || spot >= spots.length) {
            return null;
        }
        Car gone = spots[spot];
        spots[spot] = null;
        return gone;
    }

    @Override
    public String toString() {
        int parked = 0;
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] != null) {
                parked++;
            }
        }
        return "" + parked;
    }
}
"""

LOT_TESTER = """public class ParkingLotTester {
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot("Elm Street Garage");
        System.out.println(lot.getName());
        System.out.println(lot);

        for (int i = 1; i <= 5; i++) {
            lot.park(new Car("ME-10" + i, "Civic"));
        }
        System.out.println(lot);

        lot.leave(1);
        lot.leave(3);
        System.out.println(lot);

        int spot = lot.park(new Car("NH-2090", "Outback"));
        System.out.println("Outback got spot " + spot);
        System.out.println(lot);
    }
}
"""

PROJECT = [
    task("w-parking-rebuild", "Rebuild the parking lot from the spec",
         "Without looking back at the steps above, write all three files of the parking-lot project from its specification: `Car`, `ParkingLot` (6 spots, `getName`, `park`, `leave`, `toString` returning the count) and the full `ParkingLotTester` from Step 5.",
         {"Car.java": CAR, "ParkingLot.java": LOT, "ParkingLotTester.java": LOT_TESTER}, "ParkingLotTester",
         "Elm Street Garage\n0\n5\n3\nOutback got spot 1\n4",
         tests={"CheckParkingLot.java": """public class CheckParkingLot {
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot("Test");
        for (int i = 0; i < 6; i++) {
            lot.park(new Car("T-" + i, "Civic"));
        }
        System.out.println(lot.park(new Car("X", "Extra")));
        System.out.println(lot.leave(-1));
        System.out.println(lot.leave(6));
        System.out.println(lot.leave(2));
        System.out.println(lot);
    }
}
"""}, tests_run="CheckParkingLot", tests_output="-1\nnull\nnull\nCivic (T-2)\n5",
         requirements=["Follow the specification at the top of this page exactly; the test checks a full lot and out-of-range spots"],
         hints=["Write `Car` first and run the tester with only the parts that exist, one method at a time.",
                "`leave` must save the car in a variable before emptying the spot."]),

    task("w-bikerack", "A new problem with the same shape",
         "Write `Bike` (private `owner` and `color`, a constructor, `getOwner()`, and `toString` like `red bike (Ana)`) and `BikeRack`, which always has 4 spots. `lock(Bike)` uses the first empty spot and returns its number, or -1 when full. `unlock(String owner)` removes and returns that owner's bike, or `null`. `toString` returns text like `2 of 4 spots used`.",
         {"Bike.java": """public class Bike {
    private String owner;
    private String color;

    public Bike(String owner, String color) {
        this.owner = owner;
        this.color = color;
    }

    public String getOwner() {
        return owner;
    }

    @Override
    public String toString() {
        return color + " bike (" + owner + ")";
    }
}
""", "BikeRack.java": """public class BikeRack {
    private Bike[] spots;

    public BikeRack() {
        spots = new Bike[4];
    }

    public int lock(Bike bike) {
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] == null) {
                spots[i] = bike;
                return i;
            }
        }
        return -1;
    }

    public Bike unlock(String owner) {
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] != null && spots[i].getOwner().equals(owner)) {
                Bike bike = spots[i];
                spots[i] = null;
                return bike;
            }
        }
        return null;
    }

    @Override
    public String toString() {
        int used = 0;
        for (Bike bike : spots) {
            if (bike != null) {
                used++;
            }
        }
        return used + " of " + spots.length + " spots used";
    }
}
""", "BikeRackTester.java": """public class BikeRackTester {
    public static void main(String[] args) {
        BikeRack rack = new BikeRack();
        System.out.println(rack);
        System.out.println(rack.lock(new Bike("Ana", "red")));
        System.out.println(rack.lock(new Bike("Sam", "blue")));
        System.out.println(rack);
        System.out.println(rack.unlock("Ana"));
        System.out.println(rack.unlock("Ana"));
        System.out.println(rack);
        System.out.println(rack.lock(new Bike("Lee", "green")));
    }
}
"""}, "BikeRackTester",
         "0 of 4 spots used\n0\n1\n2 of 4 spots used\nred bike (Ana)\nnull\n1 of 4 spots used\n0",
         tests={"CheckBikeRack.java": """public class CheckBikeRack {
    public static void main(String[] args) {
        BikeRack rack = new BikeRack();
        for (int i = 0; i < 4; i++) {
            rack.lock(new Bike("Owner" + i, "black"));
        }
        System.out.println(rack.lock(new Bike("Late", "pink")));
        System.out.println(rack.unlock("Nobody"));
        System.out.println(rack);
    }
}
"""}, tests_run="CheckBikeRack", tests_output="-1\nnull\n4 of 4 spots used",
         hints=["`lock` is `park` from the project. `unlock` searches by owner, like `find` in the arrays lesson.",
                "In `unlock`, save the bike before setting its spot to `null`."]),
]

TASKS = {
    "classes-first-class": FIRST,
    "classes-constructors": CONSTRUCTORS,
    "classes-tostring": TOSTRING,
    "classes-encapsulation": ENCAPSULATION,
    "classes-arrays": ARRAYS,
    "classes-project-parking": PROJECT,
}
