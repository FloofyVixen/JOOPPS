from sources import SUBCLASSES_TUT, SUPER_TUT, JLS_SUPERCLASS, ACCESS_TUT, HEL_9_1

ANIMAL = """public class Animal {
    private String name;

    public Animal(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void eat() {
        System.out.println(name + " is eating.");
    }
}
"""

DOG = """public class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }

    public void fetch() {
        System.out.println(getName() + " fetches the ball.");
    }
}
"""

TESTER = """public class AnimalTester {
    public static void main(String[] args) {
        Dog rex = new Dog("Rex");
        rex.eat();
        rex.fetch();

        Animal generic = new Animal("Generic");
        generic.eat();
    }
}
"""

DUP_DOG = """public class Dog {
    private String name;

    public Dog(String name) {
        this.name = name;
    }

    public void eat() {
        System.out.println(name + " is eating.");
    }

    public void fetch() {
        System.out.println(name + " fetches the ball.");
    }
}
"""

DUP_CAT = """public class Cat {
    private String name;

    public Cat(String name) {
        this.name = name;
    }

    public void eat() {
        System.out.println(name + " is eating.");
    }

    public void climb() {
        System.out.println(name + " climbs the shelf.");
    }
}
"""

DUP_TESTER = """public class PetTester {
    public static void main(String[] args) {
        new Dog("Rex").eat();
        new Cat("Tom").eat();
    }
}
"""

LESSON = {
    "id": "inh-extends",
    "title": "Subclasses with extends",
    "summary": "Write the shared parts once in a superclass, and let subclasses inherit them and add their own.",
    "goals": [
        "Define the terms superclass and subclass, and recognize an \"is-a\" relationship",
        "Write a subclass with `extends` that inherits fields' getters and methods",
        "Explain why a subclass can't touch its superclass's `private` fields directly",
    ],
    "cos225": "The COS 225 exam guide asks you to \"know the definition of superclass and subclass, and be ready to write them\". Its example: all cars can start, so a subclass of car inherits the behavior of starting.",
    "blocks": [
        {"type": "h", "text": "The same code, twice"},
        {"type": "p", "text": "Here are two classes written separately. Look at how much of them is identical: the `name` field, the constructor and `eat()`. If you fixed a bug in `eat()`, you'd have to remember to fix it in both."},
        {"type": "code", "files": {"Dog.java": DUP_DOG, "Cat.java": DUP_CAT, "PetTester.java": DUP_TESTER}, "run": "PetTester"},

        {"type": "h", "text": "A superclass and a subclass"},
        {"type": "p", "text": "**Inheritance** lets you write the shared part once. Put it in a general class, the **superclass** (also called the parent). Then each specific class **extends** it: it becomes a **subclass** (the child) and automatically has everything the superclass offers. The subclass adds only what's different about it."},
        {"type": "code", "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "AnimalTester.java": TESTER}, "run": "AnimalTester"},
        {"type": "list", "items": [
            "`public class Dog extends Animal` makes `Dog` a subclass of `Animal`.",
            "`Dog` never declares `eat()` or `getName()`, but `rex.eat()` works: those methods are **inherited** from `Animal`.",
            "`fetch()` exists only in `Dog`. An `Animal` that isn't a `Dog` can't fetch.",
            "`super(name);` hands the name to `Animal`'s constructor, which stores it. You'll see exactly how this works in the next lesson.",
        ]},
        {"type": "p", "text": "Use inheritance when the subclass really **is a** kind of the superclass: a dog is an animal, a truck is a vehicle. If the sentence \"a ___ is a ___\" sounds wrong, inheritance is probably the wrong tool."},
        {"type": "note", "label": "One parent only",
         "text": "In Java, a class extends exactly one class. Every class except `Object` has one, and only one, direct superclass. You can still build chains (`Puppy extends Dog`, `Dog extends Animal`), and the \"Interfaces vs Objects\" unit shows how a class can promise several kinds of behavior."},

        {"type": "h", "text": "Private fields stay private"},
        {"type": "p", "text": "`name` is `private` in `Animal`. Private means \"only code inside `Animal`\", and that includes subclasses: `Dog` can't read `name` directly. It uses the public getter instead. That's encapsulation working across the hierarchy. Each class is responsible for its own data."},
        {"type": "error", "id": "ext-private",
         "prompt": "This version of `fetch` tries to use the inherited field directly.",
         "files": {"Animal.java": ANIMAL, "Dog.java": DOG.replace("getName() + \" fetches", "name + \" fetches"),
                   "AnimalTester.java": TESTER},
         "run": "AnimalTester", "expect": "compile",
         "question": "What's the best fix?",
         "choices": ["Make `name` public in `Animal`",
                     "Use the inherited getter, `getName()`, instead of `name`",
                     "Declare another `name` field in `Dog`",
                     "Remove `extends Animal`"],
         "answer": 1,
         "explain": "`Dog` inherits the public `getName()` method, so it can read the name without breaking `Animal`'s encapsulation. A second `name` field in `Dog` would compile, but it would be a separate, empty variable.",
         "fix": [["Dog.java", "name + \" fetches", "getName() + \" fetches"]]},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "ext-cat", "title": "Write a subclass",
         "prompt": "Make `Cat` a subclass of `Animal` and pass the name up to `Animal`'s constructor.",
         "files": {"Animal.java": ANIMAL, "Cat.java": """public class Cat [[ext]] Animal {
    public Cat(String name) {
        [[sup]](name);
    }

    public void climb() {
        System.out.println([[who]] + " climbs the shelf.");
    }
}
""", "CatTester.java": """public class CatTester {
    public static void main(String[] args) {
        Cat tom = new Cat("Tom");
        tom.eat();
        tom.climb();
    }
}
"""},
         "run": "CatTester", "output": "Tom is eating.\nTom climbs the shelf.",
         "blanks": {
             "ext": {"accept": ["extends"], "hint": "Which keyword makes a class a subclass?",
                     "wrong": [{"answer": "implements", "why": "`implements` is for interfaces, which come later in the course; hence \"interface expected here\". `Animal` is a class, so use `extends`. The other errors all follow from the first one: without `extends`, `Cat` has no parent with a `getName()` or `eat()`. Fix the first error and they disappear."},
                               {"answer": "inherits", "why": "Java's keyword is `extends`, not `inherits`."}]},
             "sup": {"accept": ["super"], "hint": "Call the superclass's constructor.",
                     "wrong": [{"answer": "Animal", "why": "You can't call a constructor by its class name like a method, so `Animal(name)` is \"cannot find symbol\". And because the constructor no longer starts with `super(...)`, Java adds `super();` for you, but `Animal` has no constructor without parameters. That's the first error. The next lesson explains this in detail."},
                               {"answer": "this", "why": "`this(name)` would call `Cat`'s own constructor, which is the one you're writing, so it would call itself forever. Java catches this as \"recursive constructor invocation\"."}]},
             "who": {"accept": ["getName()"], "hint": "`name` is private in `Animal`.",
                     "wrong": [{"answer": "name", "why": "`name` is `private` in `Animal`, so `Cat` can't use it directly. Use the inherited getter."},
                               {"answer": "getName", "why": "Without parentheses, Java looks for a field called `getName`. Calling a method needs `()`."}]},
         },
         "explain": "`Cat` gets `eat()` and `getName()` from `Animal` and adds `climb()`."},
        {"type": "error", "id": "ext-not-in-parent",
         "prompt": "The tester calls a `Dog` method on a plain `Animal`.",
         "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "AnimalTester.java": """public class AnimalTester {
    public static void main(String[] args) {
        Animal generic = new Animal("Generic");
        generic.fetch();
    }
}
"""},
         "run": "AnimalTester", "expect": "compile",
         "question": "Why can't Java find `fetch()`?",
         "choices": ["`fetch` is spelled wrong",
                     "Inheritance goes one way: `Dog` gets `Animal`'s methods, but `Animal` doesn't get `Dog`'s",
                     "`generic` should be declared `private`",
                     "Animals can only call `static` methods"],
         "answer": 1,
         "explain": "A subclass inherits from its superclass, never the other way round. `Animal` has no `fetch()` method, so only a `Dog` object can fetch.",
         "fix": [["AnimalTester.java", "Animal generic = new Animal(\"Generic\");\n        generic.fetch();",
                  "Dog generic = new Dog(\"Generic\");\n        generic.fetch();"]],
         "fixed_output": "Generic fetches the ball."},
        {"type": "quiz", "id": "ext-terms",
         "question": "`public class Truck extends Vehicle`. Which statement is correct?",
         "choices": ["`Truck` is the superclass and `Vehicle` is the subclass",
                     "`Vehicle` is the superclass and `Truck` is the subclass",
                     "`Truck` and `Vehicle` share the same fields, but not methods",
                     "`Truck` can extend a second class as well"],
         "answer": 1,
         "explain": "The class after `extends` is the superclass (parent). `Truck` inherits its public methods, and can't extend anything else, because Java allows one direct superclass."},
        {"type": "quiz", "id": "ext-is-a",
         "question": "Which pair is a good fit for inheritance?",
         "choices": ["`Wheel extends Car`", "`Square extends Shape`", "`Garage extends Car`", "`Playlist extends Song`"],
         "answer": 1,
         "explain": "A square is a shape. A wheel is part of a car, a garage holds cars and a playlist holds songs. Those are \"has-a\" relationships, which are better modeled with fields, like the manager classes in the OOP units."},
    ],
    "sources": [SUBCLASSES_TUT, JLS_SUPERCLASS, SUPER_TUT, ACCESS_TUT, HEL_9_1],
}
