from sources import SUBCLASSES_TUT, SUPER_TUT, OVERRIDE_METHODS_TUT, ABSTRACT_TUT, POLY_TUT, HEL_9_1, HEL_9_3

# ---------- Guided 1: payroll ----------
EMP = """public abstract class Employee {
    private String name;

    public Employee(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public abstract double monthlyPay();

    @Override
    public String toString() {
        return name + ": $" + monthlyPay();
    }
}
"""
HOURLY = """public class Hourly extends Employee {
    private double rate;
    private int hours;

    public Hourly(String name, double rate, int hours) {
        super(name);
        this.rate = rate;
        this.hours = hours;
    }

    @Override
    public double monthlyPay() {
        return rate * hours;
    }
}
"""
SALARIED = """public class Salaried extends Employee {
    private double yearly;

    public Salaried(String name, double yearly) {
        super(name);
        this.yearly = yearly;
    }

    @Override
    public double monthlyPay() {
        return yearly / 12;
    }
}
"""
PAYROLL3 = """public class Payroll {
    private Employee[] staff;

    public Payroll(int size) {
        staff = new Employee[size];
    }

    public boolean add(Employee e) {
        for (int i = 0; i < staff.length; i++) {
            if (staff[i] == null) {
                staff[i] = e;
                return true;
            }
        }
        return false;
    }

    public double total() {
        double sum = 0;
        for (Employee e : staff) {
            if (e != null) {
                sum = sum + e.monthlyPay();
            }
        }
        return sum;
    }
}
"""
PAYROLL4 = PAYROLL3.replace("""        return sum;
    }
}
""", """        return sum;
    }

    public Employee highestPaid() {
        Employee best = null;
        for (Employee e : staff) {
            if (e != null && (best == null || e.monthlyPay() > best.monthlyPay())) {
                best = e;
            }
        }
        return best;
    }
}
""")
PT1 = """public class PayrollTester {
    public static void main(String[] args) {
        Hourly ana = new Hourly("Ana", 20.0, 80);
        System.out.println(ana);
    }
}
"""
PT2 = """public class PayrollTester {
    public static void main(String[] args) {
        Employee[] people = {new Hourly("Ana", 20.0, 80), new Salaried("Raj", 60000.0)};
        for (Employee e : people) {
            System.out.println(e);
        }
    }
}
"""
PT3 = """public class PayrollTester {
    public static void main(String[] args) {
        Payroll payroll = new Payroll(3);
        payroll.add(new Hourly("Ana", 20.0, 80));
        payroll.add(new Salaried("Raj", 60000.0));
        payroll.add(new Hourly("Sam", 15.0, 40));
        System.out.println(payroll.add(new Hourly("Extra", 10.0, 1)));
        System.out.println("Total: $" + payroll.total());
    }
}
"""
PT4 = """public class PayrollTester {
    public static void main(String[] args) {
        Payroll payroll = new Payroll(3);
        payroll.add(new Hourly("Ana", 20.0, 80));
        payroll.add(new Salaried("Raj", 60000.0));
        payroll.add(new Hourly("Sam", 15.0, 40));
        System.out.println("Total: $" + payroll.total());
        System.out.println("Highest: " + payroll.highestPaid());
        System.out.println("Empty: " + new Payroll(2).highestPaid());
    }
}
"""

# ---------- Guided 2: media library ----------
ITEM = """public class Item {
    private String title;

    public Item(String title) {
        this.title = title;
    }

    @Override
    public String toString() {
        return title;
    }
}
"""
BOOK = """public class Book extends Item {
    private String author;

    public Book(String title, String author) {
        super(title);
        this.author = author;
    }

    @Override
    public String toString() {
        return super.toString() + " by " + author;
    }
}
"""
AUDIO = """public class Audiobook extends Book {
    private int minutes;

    public Audiobook(String title, String author, int minutes) {
        super(title, author);
        this.minutes = minutes;
    }

    @Override
    public String toString() {
        return super.toString() + " (" + minutes + " min audio)";
    }
}
"""
DVD = """public class Dvd extends Item {
    public Dvd(String title) {
        super(title);
    }

    @Override
    public String toString() {
        return super.toString() + " (DVD)";
    }
}
"""
LT1 = """public class LibraryTester {
    public static void main(String[] args) {
        System.out.println(new Item("Old Map"));
        System.out.println(new Book("Night Trains", "R. Vale"));
    }
}
"""
LT2 = """public class LibraryTester {
    public static void main(String[] args) {
        System.out.println(new Book("Night Trains", "R. Vale"));
        System.out.println(new Audiobook("Night Trains", "R. Vale", 410));
    }
}
"""
LT3 = """public class LibraryTester {
    public static void main(String[] args) {
        Item[] shelf = {
            new Book("Night Trains", "R. Vale"),
            new Dvd("Low Tide"),
            new Audiobook("The Long Road", "M. Okafor", 520)
        };
        for (Item item : shelf) {
            System.out.println(item);
        }
    }
}
"""
LT4 = """public class LibraryTester {
    public static void main(String[] args) {
        Item[] shelf = {
            new Book("Night Trains", "R. Vale"),
            new Dvd("Low Tide"),
            new Audiobook("The Long Road", "M. Okafor", 520)
        };
        int books = 0;
        for (Item item : shelf) {
            System.out.println(item);
            if (item instanceof Book) {
                books++;
            }
        }
        System.out.println("Books: " + books);
    }
}
"""

LESSON = {
    "id": "inh-workshop",
    "title": "Workshop: inheritance",
    "summary": "Design class hierarchies from scratch: two guided builds, then two you write on your own, one of them sized like an exam question.",
    "goals": [
        "Write abstract superclasses and subclasses with `super(...)` and `@Override` from an empty editor",
        "Chain `toString` through three levels with `super.toString()`",
        "Use polymorphism in a manager class, and `instanceof` to tell kinds apart",
    ],
    "cos225": "The exam guide asks you to know superclasses and subclasses \"and be ready to write them\", along with `@Override` and abstract methods. Independent 2 is exam-sized. Try it on paper first, then type it in.",
    "blocks": [
        {"type": "h", "text": "Before you start"},
        {"type": "p", "text": "Each task spans several files, one per class. When a step adds a new class, create its file with **New file**. If the compiler says a class \"is not abstract and does not override abstract method\", it's telling you exactly which method is still missing."},

        {"type": "h", "text": "Guided 1: a payroll"},
        {"type": "write", "id": "ws-inh-payroll", "mode": "guided", "title": "A payroll",
         "goal": "Build an abstract `Employee`, two ways of being paid, and a `Payroll` that totals everyone without caring how each person is paid.",
         "files": ["Employee.java", "Hourly.java", "PayrollTester.java", "Salaried.java", "Payroll.java"],
         "steps": [
             {"title": "Employee and Hourly", "run": "PayrollTester",
              "files": ["Employee.java", "Hourly.java", "PayrollTester.java"],
              "solution": {"Employee.java": EMP, "Hourly.java": HOURLY, "PayrollTester.java": PT1},
              "text": "Create an abstract `Employee` with a private `name`, a constructor, `getName()`, an abstract `double monthlyPay()`, and a `toString` that returns `<name>: $<monthly pay>`. Create `Hourly extends Employee` with a private rate and hours; it earns rate × hours. In the tester, print an hourly worker, Ana, at 20.0 an hour for 80 hours.",
              "hint": "`toString` in `Employee` can call `monthlyPay()` even though it's abstract. Each subclass supplies its own.",
              "checks": [{"pattern": r"abstract\s+class\s+Employee", "message": "Make `Employee` abstract."},
                         {"pattern": r"abstract\s+double\s+monthlyPay\s*\(\s*\)\s*;", "message": "Declare `public abstract double monthlyPay();`"}],
              "output": "Ana: $1600.0"},
             {"title": "A salaried worker", "run": "PayrollTester",
              "files": ["Employee.java", "Hourly.java", "PayrollTester.java", "Salaried.java"],
              "solution": {"Employee.java": EMP, "Hourly.java": HOURLY, "Salaried.java": SALARIED, "PayrollTester.java": PT2},
              "text": "Create `Salaried extends Employee` with a yearly salary; its monthly pay is yearly ÷ 12. Change the tester to put Ana and Raj (60000.0 a year) in an `Employee[]` and print each in a loop.",
              "output": "Ana: $1600.0\nRaj: $5000.0"},
             {"title": "The Payroll", "run": "PayrollTester",
              "files": ["Employee.java", "Hourly.java", "PayrollTester.java", "Salaried.java", "Payroll.java"],
              "solution": {"Employee.java": EMP, "Hourly.java": HOURLY, "Salaried.java": SALARIED,
                           "PayrollTester.java": PT3, "Payroll.java": PAYROLL3},
              "text": "Create `Payroll` with a private `Employee[]` sized by its constructor, `add(Employee)` (first empty slot, `false` when full) and `total()`, the sum of everyone's monthly pay. Add Ana, Raj and Sam (15.0 an hour, 40 hours) to a payroll of size 3, try to add a fourth person, and print the total.",
              "hint": "`total()` calls `e.monthlyPay()` on each non-null slot. Polymorphism picks the right formula.",
              "output": "false\nTotal: $7200.0"},
             {"title": "The highest paid", "run": "PayrollTester",
              "files": ["Employee.java", "Hourly.java", "PayrollTester.java", "Salaried.java", "Payroll.java"],
              "solution": {"Employee.java": EMP, "Hourly.java": HOURLY, "Salaried.java": SALARIED,
                           "PayrollTester.java": PT4, "Payroll.java": PAYROLL4},
              "text": "Add `highestPaid()`, which returns the employee with the highest monthly pay, or `null` for an empty payroll. Update the tester to match the output.",
              "output": "Total: $7200.0\nHighest: Raj: $5000.0\nEmpty: null"},
         ]},

        {"type": "h", "text": "Guided 2: a media library"},
        {"type": "write", "id": "ws-inh-library", "mode": "guided", "title": "A media library",
         "goal": "Build a three-level hierarchy where every level adds to the description with `super.toString()`, then mix the kinds in one shelf.",
         "files": ["Item.java", "Book.java", "LibraryTester.java", "Audiobook.java", "Dvd.java"],
         "steps": [
             {"title": "Item and Book", "run": "LibraryTester",
              "files": ["Item.java", "Book.java", "LibraryTester.java"],
              "solution": {"Item.java": ITEM, "Book.java": BOOK, "LibraryTester.java": LT1},
              "text": "Create `Item` with a private `title` and a `toString` that returns it. Create `Book extends Item` with a private `author`; its `toString` adds ` by <author>` to the item's text.",
              "hint": "`return super.toString() + \" by \" + author;`",
              "checks": [{"pattern": r"super\.toString\s*\(\s*\)", "message": "Build `Book`'s text with `super.toString()`."}],
              "output": "Old Map\nNight Trains by R. Vale"},
             {"title": "A third level", "run": "LibraryTester",
              "files": ["Item.java", "Book.java", "LibraryTester.java", "Audiobook.java"],
              "solution": {"Item.java": ITEM, "Book.java": BOOK, "Audiobook.java": AUDIO, "LibraryTester.java": LT2},
              "text": "Create `Audiobook extends Book` with a private `minutes`. Its constructor takes title, author and minutes, and its `toString` adds ` (<minutes> min audio)` to the book's text.",
              "hint": "`super(title, author);` goes to `Book`'s constructor, which passes the title on to `Item`.",
              "output": "Night Trains by R. Vale\nNight Trains by R. Vale (410 min audio)"},
             {"title": "A shelf of mixed items", "run": "LibraryTester",
              "files": ["Item.java", "Book.java", "LibraryTester.java", "Audiobook.java", "Dvd.java"],
              "solution": {"Item.java": ITEM, "Book.java": BOOK, "Audiobook.java": AUDIO, "Dvd.java": DVD, "LibraryTester.java": LT3},
              "text": "Create `Dvd extends Item`, whose `toString` adds ` (DVD)`. In the tester, put a book, a DVD and an audiobook in one `Item[]` and print each in a loop.",
              "output": "Night Trains by R. Vale\nLow Tide (DVD)\nThe Long Road by M. Okafor (520 min audio)"},
             {"title": "Count the books", "run": "LibraryTester",
              "files": ["Item.java", "Book.java", "LibraryTester.java", "Audiobook.java", "Dvd.java"],
              "solution": {"Item.java": ITEM, "Book.java": BOOK, "Audiobook.java": AUDIO, "Dvd.java": DVD, "LibraryTester.java": LT4},
              "text": "In the same loop, count the items that are books with `instanceof Book`, and print the count at the end. Before you run it, predict the number: is an audiobook a book?",
              "hint": "`instanceof Book` is true for a `Book` and for any subclass of `Book`.",
              "checks": [{"pattern": r"instanceof\s+Book", "message": "Count with `instanceof Book`."}],
              "output": "Night Trains by R. Vale\nLow Tide (DVD)\nThe Long Road by M. Okafor (520 min audio)\nBooks: 2"},
         ]},

        {"type": "h", "text": "Independent 1: a smart home"},
        {"type": "write", "id": "ws-inh-home", "mode": "independent", "title": "A smart home",
         "goal": "Write an abstract `Device` (private `name`, abstract `int watts()`, `toString` returning `<name> (<watts> W)`). `Lamp` always uses 10 watts. `Heater` has a level from 1 to 3 and uses level × 500 watts. `House` keeps a private `Device[]` with `add(Device)` (returns `false` when full), `totalWatts()` and `mostPowerful()` (or `null` when empty).",
         "files": ["Device.java", "Lamp.java", "Heater.java", "House.java", "HouseTester.java"], "run": "HouseTester",
         "output": "1020\nSpace heater (1000 W)\nfalse",
         "solution": {"Device.java": """public abstract class Device {
    private String name;

    public Device(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public abstract int watts();

    @Override
    public String toString() {
        return name + " (" + watts() + " W)";
    }
}
""", "Lamp.java": """public class Lamp extends Device {
    public Lamp(String name) {
        super(name);
    }

    @Override
    public int watts() {
        return 10;
    }
}
""", "Heater.java": """public class Heater extends Device {
    private int level;

    public Heater(String name, int level) {
        super(name);
        this.level = level;
    }

    @Override
    public int watts() {
        return level * 500;
    }
}
""", "House.java": """public class House {
    private Device[] devices;

    public House(int size) {
        devices = new Device[size];
    }

    public boolean add(Device d) {
        for (int i = 0; i < devices.length; i++) {
            if (devices[i] == null) {
                devices[i] = d;
                return true;
            }
        }
        return false;
    }

    public int totalWatts() {
        int total = 0;
        for (Device d : devices) {
            if (d != null) {
                total = total + d.watts();
            }
        }
        return total;
    }

    public Device mostPowerful() {
        Device best = null;
        for (Device d : devices) {
            if (d != null && (best == null || d.watts() > best.watts())) {
                best = d;
            }
        }
        return best;
    }
}
""", "HouseTester.java": """public class HouseTester {
    public static void main(String[] args) {
        House home = new House(3);
        home.add(new Lamp("Desk lamp"));
        home.add(new Heater("Space heater", 2));
        home.add(new Lamp("Porch light"));
        System.out.println(home.totalWatts());
        System.out.println(home.mostPowerful());
        System.out.println(home.add(new Lamp("Extra")));
    }
}
"""},
         "tests": {"CheckHouse.java": """public class CheckHouse {
    public static void main(String[] args) {
        House empty = new House(2);
        System.out.println(empty.totalWatts());
        System.out.println(empty.mostPowerful());
        Device d = new Heater("Big", 3);
        System.out.println(d);
    }
}
"""}, "tests_run": "CheckHouse", "tests_output": "0\nnull\nBig (1500 W)",
         "requirements": ["Five files", "`House` never checks which kind of device it has; it calls `watts()`"],
         "hints": ["Write `Device` and `Lamp` first, then run a two-line tester before moving on.",
                   "`House` is the fleet or payroll again, with `watts()` in place of the cost or pay method."],
         "checks": [{"pattern": r"abstract\s+int\s+watts\s*\(\s*\)\s*;", "message": "Declare `public abstract int watts();` in `Device`."}]},

        {"type": "h", "text": "Independent 2: a subclass that changes one rule (exam-sized)"},
        {"type": "write", "id": "ws-inh-checking", "mode": "independent", "title": "A checking account with a fee",
         "goal": "Write `Account` (private `double balance`, constructor, `getBalance()`, and `boolean withdraw(double amount)`, which succeeds only for positive amounts no larger than the balance). Then write `CheckingAccount extends Account`, which charges a fixed fee on every withdrawal: it overrides `withdraw` to take out the amount plus the fee, reusing `Account`'s rule with `super.withdraw(...)`.",
         "files": ["Account.java", "CheckingAccount.java", "AccountTester.java"], "run": "AccountTester",
         "output": "true\n78.5\nfalse\n78.5",
         "solution": {"Account.java": """public class Account {
    private double balance;

    public Account(double balance) {
        this.balance = balance;
    }

    public double getBalance() {
        return balance;
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance = balance - amount;
            return true;
        }
        return false;
    }
}
""", "CheckingAccount.java": """public class CheckingAccount extends Account {
    private double fee;

    public CheckingAccount(double balance, double fee) {
        super(balance);
        this.fee = fee;
    }

    @Override
    public boolean withdraw(double amount) {
        return super.withdraw(amount + fee);
    }
}
""", "AccountTester.java": """public class AccountTester {
    public static void main(String[] args) {
        CheckingAccount checking = new CheckingAccount(100.0, 1.5);
        System.out.println(checking.withdraw(20.0));
        System.out.println(checking.getBalance());
        System.out.println(checking.withdraw(78.0));
        System.out.println(checking.getBalance());
    }
}
"""},
         "tests": {"CheckAccounts.java": """public class CheckAccounts {
    public static void main(String[] args) {
        Account plain = new Account(10.0);
        System.out.println(plain.withdraw(10.0));
        System.out.println(plain.getBalance());
        Account x = new CheckingAccount(50.0, 2.0);
        x.withdraw(8.0);
        System.out.println(x.getBalance());
    }
}
"""}, "tests_run": "CheckAccounts", "tests_output": "true\n0.0\n40.0",
         "requirements": ["`CheckingAccount`'s `withdraw` is one line", "`balance` stays private in `Account`"],
         "hints": ["Withdrawing 78.0 with a 1.5 fee needs 79.5, but only 78.5 is left, so it fails and nothing changes.",
                   "The test stores a `CheckingAccount` in an `Account` variable. Your override must still run (that's polymorphism)."],
         "checks": [{"pattern": r"super\.withdraw\s*\(", "message": "Reuse `Account`'s rule with `super.withdraw(...)`."},
                    {"pattern": r"@Override", "message": "Mark the overriding `withdraw` with `@Override`."}]},
    ],
    "sources": [SUBCLASSES_TUT, SUPER_TUT, OVERRIDE_METHODS_TUT, ABSTRACT_TUT, POLY_TUT, HEL_9_1, HEL_9_3],
}
