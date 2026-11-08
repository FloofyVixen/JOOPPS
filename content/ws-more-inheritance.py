from sources import OVERRIDE_METHODS_TUT, OVERRIDE_TUT, POLY_TUT, JLS_INSTANCEOF, HEL_9_3
from wshelp import step, guided, workshop, task

OVR = {"pattern": r"@Override", "message": "Mark overriding methods with `@Override`."}

NOTE = """public class Notification {
    private String text;

    public Notification(String text) {
        this.text = text;
    }

    public String getText() {
        return text;
    }

    public void deliver() {
        System.out.println("Notice: " + text);
    }
}
"""
EMAIL = """public class EmailNotification extends Notification {
    private String to;

    public EmailNotification(String to, String text) {
        super(text);
        this.to = to;
    }

    @Override
    public void deliver() {
        System.out.println("To: " + to);
        super.deliver();
    }
}
"""
SMS = """public class SmsNotification extends Notification {
    private String phone;

    public SmsNotification(String phone, String text) {
        super(text);
        this.phone = phone;
    }

    @Override
    public void deliver() {
        System.out.println("SMS to " + phone + ": " + getText());
    }
}
"""
NT1 = """public class NotifyTester {
    public static void main(String[] args) {
        new Notification("Server restarts at 9").deliver();
    }
}
"""
NT2 = """public class NotifyTester {
    public static void main(String[] args) {
        new Notification("Server restarts at 9").deliver();
        new EmailNotification("ana@example.com", "Your order shipped").deliver();
    }
}
"""
NT3 = """public class NotifyTester {
    public static void main(String[] args) {
        new EmailNotification("ana@example.com", "Your order shipped").deliver();
        new SmsNotification("555-0100", "Code: 4821").deliver();
    }
}
"""
NT4 = """public class NotifyTester {
    public static void main(String[] args) {
        Notification[] queue = {
            new Notification("Server restarts at 9"),
            new SmsNotification("555-0100", "Code: 4821"),
            new EmailNotification("ana@example.com", "Your order shipped"),
            new SmsNotification("555-0199", "Running late")
        };
        int texts = 0;
        for (Notification n : queue) {
            n.deliver();
            if (n instanceof SmsNotification) {
                texts++;
            }
        }
        System.out.println(texts + " text messages");
    }
}
"""

ITEM = """public class MenuItem {
    private String name;
    private double price;

    public MenuItem(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public double getPrice() {
        return price;
    }

    @Override
    public String toString() {
        return name + " $" + price;
    }
}
"""
DRINK = """public class Drink extends MenuItem {
    private boolean large;

    public Drink(String name, double price, boolean large) {
        super(name, price);
        this.large = large;
    }

    @Override
    public String toString() {
        if (large) {
            return super.toString() + " (large)";
        }
        return super.toString() + " (small)";
    }
}
"""
DESSERT = """public class Dessert extends MenuItem {
    private boolean vegan;

    public Dessert(String name, double price, boolean vegan) {
        super(name, price);
        this.vegan = vegan;
    }

    @Override
    public String toString() {
        if (vegan) {
            return super.toString() + " [vegan]";
        }
        return super.toString();
    }
}
"""
MT1 = """public class MenuTester {
    public static void main(String[] args) {
        System.out.println(new MenuItem("Soup", 6.0));
        System.out.println(new Drink("Lemonade", 3.5, true));
        System.out.println(new Drink("Lemonade", 2.5, false));
    }
}
"""
MT2 = """public class MenuTester {
    public static void main(String[] args) {
        System.out.println(new Dessert("Brownie", 4.0, false));
        System.out.println(new Dessert("Sorbet", 4.5, true));
    }
}
"""
MT3 = """public class MenuTester {
    public static void main(String[] args) {
        MenuItem[] menu = {
            new MenuItem("Soup", 6.0),
            new Drink("Lemonade", 3.5, true),
            new Dessert("Sorbet", 4.5, true)
        };
        MenuItem cheapest = menu[0];
        for (MenuItem item : menu) {
            System.out.println(item);
            if (item.getPrice() < cheapest.getPrice()) {
                cheapest = item;
            }
        }
        System.out.println("Cheapest: " + cheapest);
    }
}
"""

LESSON = workshop(
    "ws-more-inheritance", "Workshop: more inheritance",
    "Practice overriding with `@Override` and `super.`, and polymorphic loops over arrays of a superclass type.",
    ["Override methods and extend the parent's version with `super.`",
     "Store different subclasses in one superclass array and loop over it",
     "Use `instanceof` to count one kind of object"],
    guided("ws-u8-notify", "Notifications", "Build a `Notification` and two subclasses that deliver differently, then send a mixed queue.", [
        step("Notification", "Create `Notification.java` with a private `text`, a constructor, `getText()`, and `deliver()`, which prints `Notice: <text>`.",
             {"Notification.java": NOTE, "NotifyTester.java": NT1}, "NotifyTester", "Notice: Server restarts at 9"),
        step("Email", "Create `EmailNotification extends Notification` with a private `to` address. Override `deliver()` to print `To: <address>` and then do the normal delivery with `super.deliver()`.",
             {"Notification.java": NOTE, "EmailNotification.java": EMAIL, "NotifyTester.java": NT2}, "NotifyTester",
             "Notice: Server restarts at 9\nTo: ana@example.com\nNotice: Your order shipped",
             checks=[OVR, {"pattern": r"super\.deliver\s*\(\s*\)", "message": "Reuse the parent's delivery with `super.deliver()`."}]),
        step("SMS", "Create `SmsNotification extends Notification` with a private `phone`. Its `deliver()` replaces the parent's completely: it prints `SMS to <phone>: <text>`.",
             {"Notification.java": NOTE, "EmailNotification.java": EMAIL, "SmsNotification.java": SMS, "NotifyTester.java": NT3}, "NotifyTester",
             "To: ana@example.com\nNotice: Your order shipped\nSMS to 555-0100: Code: 4821",
             hint="`text` is private in `Notification`; use `getText()`."),
        step("A mixed queue", "Put four notifications of different kinds in one `Notification[]`, deliver them in a loop, and count the text messages with `instanceof`.",
             {"Notification.java": NOTE, "EmailNotification.java": EMAIL, "SmsNotification.java": SMS, "NotifyTester.java": NT4}, "NotifyTester",
             "Notice: Server restarts at 9\nSMS to 555-0100: Code: 4821\nTo: ana@example.com\nNotice: Your order shipped\nSMS to 555-0199: Running late\n2 text messages",
             checks=[{"pattern": r"instanceof\s+SmsNotification", "message": "Count with `instanceof SmsNotification`."}]),
    ]),
    guided("ws-u8-menu", "A café menu", "Build menu items whose `toString` grows with each subclass, then find the cheapest item in a mixed menu.", [
        step("Items and drinks", "Create `MenuItem` (private `name` and `price`, `getPrice()`, `toString` like `Soup $6.0`) and `Drink extends MenuItem` with a private `boolean large`. `Drink`'s `toString` adds ` (large)` or ` (small)` to the item's text.",
             {"MenuItem.java": ITEM, "Drink.java": DRINK, "MenuTester.java": MT1}, "MenuTester",
             "Soup $6.0\nLemonade $3.5 (large)\nLemonade $2.5 (small)",
             checks=[{"pattern": r"super\.toString\s*\(\s*\)", "message": "Build on the parent's text with `super.toString()`."}]),
        step("Desserts", "Create `Dessert extends MenuItem` with a private `boolean vegan`. Its `toString` adds ` [vegan]` for vegan desserts and nothing otherwise.",
             {"MenuItem.java": ITEM, "Drink.java": DRINK, "Dessert.java": DESSERT, "MenuTester.java": MT2}, "MenuTester",
             "Brownie $4.0\nSorbet $4.5 [vegan]"),
        step("The whole menu", "Put one of each kind in a `MenuItem[]`. Print every item in a loop, and keep track of the cheapest one as you go.",
             {"MenuItem.java": ITEM, "Drink.java": DRINK, "Dessert.java": DESSERT, "MenuTester.java": MT3}, "MenuTester",
             "Soup $6.0\nLemonade $3.5 (large)\nSorbet $4.5 [vegan]\nCheapest: Lemonade $3.5 (large)",
             hint="Start with `MenuItem cheapest = menu[0];` and replace it whenever an item is cheaper."),
    ]),
    task("ws-u8-raises", "Different raises",
         "Write `Employee` (private `name` and `int salary`, `getSalary()`, `raiseBy(int amount)`, and `raise()`, which raises by 1000) and `Manager extends Employee`, which overrides `raise()` to raise by 3000. In `RaiseTester`, give everyone in an `Employee[]` a raise in one loop and print the new total payroll.",
         {"Employee.java": """public class Employee {
    private String name;
    private int salary;

    public Employee(String name, int salary) {
        this.name = name;
        this.salary = salary;
    }

    public int getSalary() {
        return salary;
    }

    public void raiseBy(int amount) {
        salary = salary + amount;
    }

    public void raise() {
        raiseBy(1000);
    }
}
""", "Manager.java": """public class Manager extends Employee {
    public Manager(String name, int salary) {
        super(name, salary);
    }

    @Override
    public void raise() {
        raiseBy(3000);
    }
}
""", "RaiseTester.java": """public class RaiseTester {
    public static void main(String[] args) {
        Employee[] staff = {new Employee("Ana", 40000), new Manager("Kim", 70000), new Employee("Sam", 38000)};
        int total = 0;
        for (Employee e : staff) {
            e.raise();
            total = total + e.getSalary();
        }
        System.out.println("Total: " + total);
    }
}
"""}, "RaiseTester", "Total: 153000",
         tests={"CheckRaise.java": """public class CheckRaise {
    public static void main(String[] args) {
        Employee m = new Manager("Lee", 50000);
        m.raise();
        System.out.println(m.getSalary());
        Employee e = new Employee("Bo", 10);
        e.raise();
        System.out.println(e.getSalary());
    }
}
"""}, tests_run="CheckRaise", tests_output="53000\n1010",
         hints=["`salary` is private, so `Manager` changes it through the inherited `raiseBy`."],
         checks=[OVR]),
    task("ws-u8-greeters", "Three ways to say hello",
         "Write `Greeter` with `greet(String name)` returning `Hello, <name>.`, and two subclasses that override it: `FormalGreeter` returns `Good day, <name>.` and `PirateGreeter` returns `Ahoy, <name>!`. In `GreetTester`, greet Ana with each one from a `Greeter[]`.",
         {"Greeter.java": """public class Greeter {
    public String greet(String name) {
        return "Hello, " + name + ".";
    }
}
""", "FormalGreeter.java": """public class FormalGreeter extends Greeter {
    @Override
    public String greet(String name) {
        return "Good day, " + name + ".";
    }
}
""", "PirateGreeter.java": """public class PirateGreeter extends Greeter {
    @Override
    public String greet(String name) {
        return "Ahoy, " + name + "!";
    }
}
""", "GreetTester.java": """public class GreetTester {
    public static void main(String[] args) {
        Greeter[] greeters = {new Greeter(), new FormalGreeter(), new PirateGreeter()};
        for (Greeter g : greeters) {
            System.out.println(g.greet("Ana"));
        }
    }
}
"""}, "GreetTester", "Hello, Ana.\nGood day, Ana.\nAhoy, Ana!",
         tests={"CheckGreet.java": """public class CheckGreet {
    public static void main(String[] args) {
        Greeter g = new PirateGreeter();
        System.out.println(g.greet("Lee"));
        Object o = new FormalGreeter();
        System.out.println(o instanceof Greeter);
    }
}
"""}, tests_run="CheckGreet", tests_output="Ahoy, Lee!\ntrue",
         checks=[OVR, {"pattern": r"Greeter\s*\[\s*\]", "message": "Store the greeters in a `Greeter[]`."}]),
    [OVERRIDE_METHODS_TUT, OVERRIDE_TUT, POLY_TUT, JLS_INSTANCEOF, HEL_9_3],
)
