from sources import IFACE_TYPE_TUT, OBJECT_TUT, POLY_TUT, JLS_INSTANCEOF, HEL_9_2

CHARGE = """public interface Chargeable {
    void charge(int minutes);

    int batteryPercent();
}
"""
PHONE = """public class Phone implements Chargeable {
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

    public void call(String who) {
        System.out.println("Calling " + who);
    }
}
"""
CAR = """public class ElectricCar implements Chargeable {
    private int battery;

    public ElectricCar(int battery) {
        this.battery = battery;
    }

    @Override
    public void charge(int minutes) {
        battery = Math.min(100, battery + minutes / 3);
    }

    @Override
    public int batteryPercent() {
        return battery;
    }
}
"""
STATION = """public class ChargingStation {
    public static void chargeAll(Chargeable[] items, int minutes) {
        for (Chargeable c : items) {
            c.charge(minutes);
        }
    }

    public static void main(String[] args) {
        Chargeable[] plugged = {new Phone(40), new ElectricCar(10), new Phone(95)};
        chargeAll(plugged, 30);
        for (Chargeable c : plugged) {
            System.out.println(c.batteryPercent() + "%");
        }
    }
}
"""

LESSON = {
    "id": "iface-type",
    "title": "Interfaces as types, and Object",
    "summary": "An interface can be used as a variable, array or parameter type, holding objects of unrelated classes that share one ability.",
    "goals": [
        "Store objects of different classes in a variable or array of an interface type",
        "Write a method whose parameter is an interface type",
        "Compare interface types with class types and with `Object`",
    ],
    "cos225": "This unit is called \"Interfaces vs Objects\". The comparison at the end of this lesson sets an interface type, a class type and `Object` side by side: what each can hold, and what you can call through it.",
    "blocks": [
        {"type": "h", "text": "Unrelated classes, one ability"},
        {"type": "p", "text": "A phone and an electric car have nothing in common as classes. Neither is a kind of the other, and they share no parent. But both can be charged. Because both implement `Chargeable`, one array of type `Chargeable[]` can hold both, and one method can charge them all."},
        {"type": "code", "files": {"Chargeable.java": CHARGE, "Phone.java": PHONE, "ElectricCar.java": CAR, "ChargingStation.java": STATION},
         "run": "ChargingStation"},
        {"type": "list", "items": [
            "`Chargeable[] plugged` holds two phones and a car. Each `charge` call runs the object's own version: the phone gains 1% per minute, the car 1% every 3 minutes.",
            "`chargeAll(Chargeable[] items, int minutes)` works for any class that implements `Chargeable`, including ones written later.",
            "`Math.min(100, ...)` keeps the battery from going over 100. It returns the smaller of its two numbers.",
        ]},
        {"type": "p", "text": "This is polymorphism again, but without inheritance: the interface is the shared type."},

        {"type": "h", "text": "The type decides what you can call"},
        {"type": "p", "text": "Just like with superclass variables, a `Chargeable` variable only offers the interface's methods. A phone in a `Chargeable` variable can't make calls until you check and cast:"},
        {"type": "error", "id": "itype-call",
         "prompt": "The variable's type is the interface.",
         "files": {"Chargeable.java": CHARGE, "Phone.java": PHONE, "CallTester.java": """public class CallTester {
    public static void main(String[] args) {
        Chargeable c = new Phone(50);
        c.call("Ana");
    }
}
"""},
         "run": "CallTester", "expect": "compile",
         "question": "Which change makes the call work while keeping the `Chargeable` variable?",
         "choices": ["Add `call` to every class",
                     "Check `c instanceof Phone`, then cast: `((Phone) c).call(\"Ana\")`",
                     "Change `Chargeable` to `Object`",
                     "Make `call` static"],
         "answer": 1,
         "explain": "`Chargeable` only promises `charge` and `batteryPercent`. To use a phone-only method, confirm it's a `Phone` and cast. `Object` would be worse: it promises even less.",
         "fix": [["CallTester.java", "        c.call(\"Ana\");\n",
                  "        if (c instanceof Phone) {\n            ((Phone) c).call(\"Ana\");\n        }\n"]],
         "fixed_output": "Calling Ana"},

        {"type": "h", "text": "Interface type, class type, Object"},
        {"type": "list", "items": [
            "**A class type** (`Phone p`) holds a `Phone` or any subclass of it. You can call every public method of `Phone`.",
            "**An interface type** (`Chargeable c`) holds an object of **any** class that implements `Chargeable`, related or not. You can call only `Chargeable`'s methods.",
            "**`Object o`** holds absolutely anything, because every class extends `Object`. You can call only `Object`'s methods, such as `toString()` and `equals()`.",
            "You can create objects of classes (`new Phone(50)`), but never of an interface. An interface describes objects; it isn't one.",
        ]},
        {"type": "p", "text": "`instanceof` works with interfaces too: `x instanceof Chargeable` asks whether the object's class implements it."},

        {"type": "h", "text": "Practice"},
        {"type": "predict", "id": "itype-predict",
         "prompt": "What does this print?",
         "files": {"Chargeable.java": CHARGE, "Phone.java": PHONE, "ElectricCar.java": CAR, "Sort.java": """public class Sort {
    public static void main(String[] args) {
        Object[] things = {new Phone(20), "a cable", new ElectricCar(50), 42};
        int chargeable = 0;
        for (Object o : things) {
            if (o instanceof Chargeable) {
                chargeable++;
            }
        }
        System.out.println(chargeable + " of " + things.length);
    }
}
"""}, "run": "Sort",
         "choices": ["4 of 4", "2 of 4", "1 of 4", "0 of 4"],
         "answer": 1,
         "explain": "An `Object[]` can hold anything: a phone, a `String`, a car, even the number 42 (Java wraps it in an `Integer` object). Only the phone and the car implement `Chargeable`."},
        {"type": "blanks", "id": "itype-param", "title": "A method for any Chargeable",
         "prompt": "Write the parameter type so `lowest` works for phones, cars, or a mix.",
         "files": {"Chargeable.java": CHARGE, "Phone.java": PHONE, "ElectricCar.java": CAR, "Lowest.java": """public class Lowest {
    public static int lowest([[ptype]] items) {
        int min = 100;
        for (Chargeable c : items) {
            if (c.[[call]] < min) {
                min = c.batteryPercent();
            }
        }
        return min;
    }

    public static void main(String[] args) {
        Chargeable[] mix = {new Phone(64), new ElectricCar(31), new Phone(88)};
        System.out.println("Lowest battery: " + lowest(mix) + "%");
    }
}
"""},
         "run": "Lowest", "output": "Lowest battery: 31%",
         "blanks": {
             "ptype": {"accept": ["Chargeable[]"], "hint": "An array of the interface type.",
                       "wrong": [{"answer": "Phone[]", "why": "A `Phone[]` can't hold an `ElectricCar`, and `mix` is a `Chargeable[]`, so the call doesn't compile."},
                                 {"answer": "Chargeable", "why": "That's a single object, but the loop needs an array to go through."}]},
             "call": {"accept": ["batteryPercent()"], "hint": "Which `Chargeable` method reports the charge?",
                      "wrong": [{"answer": "battery", "why": "`battery` is a private field inside each class, and `Chargeable` has no fields. Use the interface's method, `batteryPercent()`."}]},
         },
         "explain": "Because the parameter is the interface type, `lowest` works for any class that implements `Chargeable`."},
        {"type": "quiz", "id": "itype-object",
         "question": "`Object o = new Phone(50);` Which call compiles?",
         "choices": ["`o.charge(10);`", "`o.call(\"Ana\");`", "`o.toString();`", "`o.batteryPercent();`"],
         "answer": 2,
         "explain": "Through an `Object` variable you can only call `Object`'s methods, and `toString()` is one of them. (At run time, `Phone`'s own `toString` would run if it had one.)"},
    ],
    "sources": [IFACE_TYPE_TUT, POLY_TUT, OBJECT_TUT, JLS_INSTANCEOF, HEL_9_2],
}
