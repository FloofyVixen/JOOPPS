from sources import ACCESS_TUT, NAMING, HEL_4_1, DEV_CLASSES

THERMO = """public class Thermostat {
    private int temperature;

    public Thermostat() {
        temperature = 68;
    }

    public int getTemperature() {
        return temperature;
    }

    public void setTemperature(int temperature) {
        if (temperature >= 50 && temperature <= 90) {
            this.temperature = temperature;
        } else {
            System.out.println(temperature + " is out of range (50 to 90).");
        }
    }
}
"""

TESTER = """public class ThermostatTester {
    public static void main(String[] args) {
        Thermostat hall = new Thermostat();
        System.out.println("Starts at " + hall.getTemperature());

        hall.setTemperature(72);
        System.out.println("Now " + hall.getTemperature());

        hall.setTemperature(450);
        System.out.println("Still " + hall.getTemperature());
    }
}
"""

BAD_TESTER = """public class ThermostatTester {
    public static void main(String[] args) {
        Thermostat hall = new Thermostat();
        hall.temperature = 450;
    }
}
"""

LESSON = {
    "id": "classes-encapsulation",
    "title": "Private fields, getters and setters",
    "summary": "Hide an object's fields so the only way to change them is through methods that check the values.",
    "goals": [
        "Make fields `private` and explain what that prevents",
        "Write getter and setter methods, and follow the `getX`/`setX` naming convention",
        "Use a setter to reject values that make no sense",
    ],
    "cos225": "The COS 225 practice code includes a class with a setter that refuses values above a limit and prints a warning instead. That is the pattern this lesson teaches.",
    "blocks": [
        {"type": "h", "text": "Public fields let anything happen"},
        {"type": "p", "text": "With `public` fields, any code anywhere can write `hall.temperature = 450;`, and the object can't stop it. As programs grow, values like that become hard to track down. **Encapsulation** means keeping an object's data private and letting other code change it only through the object's own methods."},
        {"type": "p", "text": "Marking a field `private` means only code inside the same class can use it. Oracle's tutorial gives this rule of thumb: use the most restrictive access that makes sense, and use `private` unless you have a good reason not to."},

        {"type": "h", "text": "Getters and setters"},
        {"type": "code", "files": {"Thermostat.java": THERMO, "ThermostatTester.java": TESTER}, "run": "ThermostatTester"},
        {"type": "list", "items": [
            "A **getter** returns a field's value. By convention it's named `get` plus the field name: `getTemperature`. For a `boolean` field, the name usually starts with `is`, as in `isOn`.",
            "A **setter** changes a field. It's named `set` plus the field name, takes the new value as a parameter, and returns `void`.",
            "Because the setter is the only way in, it can check the value first. The bad value 450 never reaches the field.",
        ]},
        {"type": "p", "text": "Here's what happens if the tester reaches for the private field directly:"},
        {"type": "code", "files": {"Thermostat.java": THERMO, "ThermostatTester.java": BAD_TESTER},
         "run": "ThermostatTester", "expect": "compile"},
        {"type": "note", "label": "Not every field needs both",
         "text": "Give a field a setter only if outside code should be able to change it. A bank account's balance should change through `deposit` and `withdraw`, not through `setBalance`, so it gets a getter and no setter."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "encap-wallet", "title": "A wallet that can't go negative",
         "prompt": "Finish `Wallet` so `spend` refuses to spend more than the wallet holds. Spending exactly everything is allowed.",
         "files": {"Wallet.java": """public class Wallet {
    private double money;

    public Wallet(double money) {
        this.money = money;
    }

    public [[gtype]] getMoney() {
        return money;
    }

    public void spend(double amount) {
        if (amount [[cmp]] money) {
            money = money - amount;
        } else {
            System.out.println("Not enough money for " + amount);
        }
    }
}
""", "WalletTester.java": """public class WalletTester {
    public static void main(String[] args) {
        Wallet mine = new Wallet(20.0);
        mine.spend(5.0);
        System.out.println(mine.[[call]]);
        mine.spend(30.0);
        mine.spend(15.0);
        System.out.println(mine.getMoney());
    }
}
"""},
         "run": "WalletTester", "output": "15.0\nNot enough money for 30.0\n0.0",
         "blanks": {
             "gtype": {"accept": ["double"], "hint": "The getter returns the field, so it has the field's type.",
                       "wrong": [{"answer": "void", "why": "A `void` method can't return anything, but a getter's whole job is to return the field."},
                                 {"answer": "int", "why": "`money` is a `double`. Returning it as an `int` would drop the cents, so Java refuses (\"possible lossy conversion\")."}]},
             "cmp": {"accept": ["<="], "hint": "Spending exactly 15.0 out of 15.0 should be allowed.",
                     "wrong": [{"answer": "<", "why": "With `<`, spending exactly what's left is refused. The last `spend(15.0)` fails and the wallet keeps 15.0."},
                               {"answer": ">", "why": "That reverses the check, so the wallet only lets you spend more than you have."}]},
             "call": {"accept": ["getMoney()"], "hint": "`money` is private. Use the getter, and remember the parentheses.",
                      "wrong": [{"answer": "money", "why": "`money` is `private`, so only code inside `Wallet` can use it. From the tester, call the getter."},
                                {"answer": "getMoney", "why": "Without parentheses, Java looks for a field named `getMoney`. To call a method, add `()`."}]},
         },
         "explain": "The tester never touches `money` directly. It can read the field through `getMoney()` and change it only through `spend`, which checks the amount first."},
        {"type": "quiz", "id": "encap-private-where",
         "question": "A field is declared `private int count;` in class `Counter`. Where can `count` be used by name?",
         "choices": ["Anywhere in the program", "Only inside `Counter`'s own methods and constructors", "Only in `main`", "Only in classes whose names start with `Counter`"],
         "answer": 1,
         "explain": "`private` limits a member to the class that declares it. Other classes have to go through the methods `Counter` chooses to make `public`."},
    ],
    "sources": [ACCESS_TUT, NAMING, HEL_4_1, DEV_CLASSES],
}
