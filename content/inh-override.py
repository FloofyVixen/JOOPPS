from sources import OVERRIDE_METHODS_TUT, OVERRIDE_TUT, SUPER_TUT, JLS_OVERRIDE, HEL_9_1

ANIMAL = """public class Animal {
    private String name;

    public Animal(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void speak() {
        System.out.println(name + " makes a sound.");
    }
}
"""

DOG = """public class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }

    @Override
    public void speak() {
        System.out.println(getName() + " says Woof!");
    }
}
"""

COW = """public class Cow extends Animal {
    public Cow(String name) {
        super(name);
    }
}
"""

TESTER = """public class SpeakTester {
    public static void main(String[] args) {
        new Animal("Generic").speak();
        new Dog("Rex").speak();
        new Cow("Bessie").speak();
    }
}
"""

PRODUCT = """public class Product {
    private String name;
    private double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public double getPrice() {
        return price;
    }

    @Override
    public String toString() {
        return name + ": $" + price;
    }
}
"""

SALE = """public class SaleProduct extends Product {
    private int percentOff;

    public SaleProduct(String name, double price, int percentOff) {
        super(name, price);
        this.percentOff = percentOff;
    }

    @Override
    public String toString() {
        return super.toString() + " (" + percentOff + "% off)";
    }
}
"""

SALE_T = """public class StoreTester {
    public static void main(String[] args) {
        System.out.println(new Product("Lamp", 30.0));
        System.out.println(new SaleProduct("Rug", 80.0, 25));
    }
}
"""

LESSON = {
    "id": "inh-override",
    "title": "Overriding methods",
    "summary": "A subclass can replace an inherited method with its own version, and still reuse the parent's version with `super.`",
    "goals": [
        "Override an inherited method and mark it with `@Override`",
        "Extend the parent's behavior with `super.methodName()`",
        "Tell overriding (same signature, in a subclass) from overloading (different parameters)",
    ],
    "cos225": "`@override` is its own bullet in the COS 225 exam guide. Know what it does, and why it's worth writing even though it's optional.",
    "blocks": [
        {"type": "h", "text": "Replacing an inherited method"},
        {"type": "p", "text": "Every `Animal` can `speak()`, but the general version is vague. A subclass can **override** the method: declare a method with the same name, the same parameters and the same return type. When the method is called on that subclass's objects, the subclass's version runs instead."},
        {"type": "code", "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "Cow.java": COW, "SpeakTester.java": TESTER}, "run": "SpeakTester"},
        {"type": "p", "text": "`Cow` doesn't override `speak()`, so it uses the inherited version. Overriding is optional: a subclass overrides only the methods it wants to behave differently."},

        {"type": "h", "text": "What @Override is for"},
        {"type": "p", "text": "`@Override` is an annotation: a note to the compiler that says \"this method is meant to replace one from a superclass\". If it doesn't (because of a typo in the name, or different parameters), the compiler stops with an error. Without the annotation, the misspelled method would silently become a new, separate method, and the old behavior would quietly stay."},
        {"type": "error", "id": "override-typo",
         "prompt": "`Dog`'s method name has a typo.",
         "files": {"Animal.java": ANIMAL, "Dog.java": DOG.replace("public void speak()", "public void speek()"),
                   "Cow.java": COW, "SpeakTester.java": TESTER},
         "run": "SpeakTester", "expect": "compile",
         "question": "What would happen if the `@Override` line weren't there?",
         "choices": ["The same compile error",
                     "It would compile, and `new Dog(\"Rex\").speak()` would print `Rex makes a sound.`",
                     "It would compile, and print `Rex says Woof!`",
                     "The program would crash when it runs"],
         "answer": 1,
         "explain": "Without `@Override`, `speek` is just a new method that nobody calls, and `Dog` inherits the general `speak()`. The annotation turns that silent bug into a compile error that points at the right line.",
         "fix": [["Dog.java", "public void speek()", "public void speak()"]]},
        {"type": "p", "text": "Here is the same typo with the `@Override` line removed. It compiles, and the dog has quietly lost its bark:"},
        {"type": "code", "files": {"Animal.java": ANIMAL,
                                   "Dog.java": DOG.replace("    @Override\n", "").replace("public void speak()", "public void speek()"),
                                   "Cow.java": COW, "SpeakTester.java": TESTER}, "run": "SpeakTester",
         "output": "Generic makes a sound.\nRex makes a sound.\nBessie makes a sound."},

        {"type": "h", "text": "Reusing the parent's version with super."},
        {"type": "p", "text": "Often the subclass wants to add to the parent's behavior, not throw it away. Inside the overriding method, `super.toString()` calls the superclass's version. This is the usual way to write `toString` in a hierarchy: each class adds its own part."},
        {"type": "code", "files": {"Product.java": PRODUCT, "SaleProduct.java": SALE, "StoreTester.java": SALE_T}, "run": "StoreTester"},
        {"type": "p", "text": "`SaleProduct` can't read `name` or `price` (they're private), but it doesn't need to: `super.toString()` already formats them."},

        {"type": "h", "text": "Overriding versus overloading"},
        {"type": "list", "items": [
            "**Overriding**: a subclass method with the **same** name and parameters as an inherited one. It replaces the inherited behavior.",
            "**Overloading**: methods (or constructors) with the same name but **different** parameters, like the two `Rectangle` constructors in the Classes section. Each one is a separate method.",
        ]},

        {"type": "h", "text": "Practice"},
        {"type": "predict", "id": "override-which",
         "prompt": "`Puppy extends Dog`, and only `Dog` overrides `speak()`. What prints?",
         "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "Puppy.java": """public class Puppy extends Dog {
    public Puppy(String name) {
        super(name);
    }
}
""", "PuppyTester.java": """public class PuppyTester {
    public static void main(String[] args) {
        new Puppy("Bit").speak();
    }
}
"""}, "run": "PuppyTester",
         "choices": ["Bit makes a sound.", "Bit says Woof!", "Nothing; Puppy has no speak method", "A compile error"],
         "answer": 1,
         "explain": "Java looks for `speak()` starting at the object's own class and moving up. `Puppy` has none, so it uses `Dog`'s, the closest one, before reaching `Animal`'s."},
        {"type": "blanks", "id": "override-tostring", "title": "Extend toString",
         "prompt": "`Ebook` adds its file size to the description that `Item` already builds.",
         "files": {"Item.java": """public class Item {
    private String title;

    public Item(String title) {
        this.title = title;
    }

    @Override
    public String toString() {
        return "Item: " + title;
    }
}
""", "Ebook.java": """public class Ebook extends Item {
    private int megabytes;

    public Ebook(String title, int megabytes) {
        super(title);
        this.megabytes = megabytes;
    }

    [[ann]]
    public String toString() {
        return [[parent]] + ", " + megabytes + " MB";
    }
}
""", "EbookTester.java": """public class EbookTester {
    public static void main(String[] args) {
        System.out.println(new Ebook("Night Trains", 3));
    }
}
"""},
         "run": "EbookTester", "output": "Item: Night Trains, 3 MB",
         "blanks": {
             "ann": {"accept": ["@Override"], "hint": "The annotation that asks the compiler to check this really replaces an inherited method.",
                     "wrong": [{"answer": "@override", "why": "Annotations are case-sensitive. It's `@Override` with a capital O."}]},
             "parent": {"accept": ["super.toString()"], "hint": "Reuse `Item`'s version.",
                        "wrong": [{"answer": "toString()", "why": "Calling `toString()` here calls `Ebook`'s own `toString`, which calls itself again, forever. Java runs out of room and crashes with a `StackOverflowError`. `super.` picks the parent's version."},
                                  {"answer": "title", "why": "`title` is `private` in `Item`, so `Ebook` can't use it. `super.toString()` gets the formatted text without touching the field."}]},
         },
         "explain": "`super.toString()` returns `Item: Night Trains`, and `Ebook` adds its own part to the end."},
        {"type": "quiz", "id": "override-vs-overload",
         "question": "`Animal` has `speak()`. Which method in `Dog` overrides it?",
         "choices": ["`public void speak(String sound)`", "`public void speak()`", "`public void Speak()`", "`public void speakLoudly()`"],
         "answer": 1,
         "explain": "Only the exact same name and parameter list overrides. `speak(String)` overloads it (a different method), and `Speak` is a different name, because Java is case-sensitive."},
    ],
    "sources": [OVERRIDE_METHODS_TUT, OVERRIDE_TUT, SUPER_TUT, JLS_OVERRIDE, HEL_9_1],
}
