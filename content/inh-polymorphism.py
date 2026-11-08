from sources import POLY_TUT, OBJECT_TUT, OBJECT_API, SUBCLASSES_TUT, JLS_INSTANCEOF, HEL_9_3

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

    public void fetch() {
        System.out.println(getName() + " fetches the ball.");
    }
}
"""
CAT = """public class Cat extends Animal {
    public Cat(String name) {
        super(name);
    }

    @Override
    public void speak() {
        System.out.println(getName() + " says Meow.");
    }
}
"""
SHELTER = """public class Shelter {
    public static void main(String[] args) {
        Animal[] animals = new Animal[3];
        animals[0] = new Dog("Rex");
        animals[1] = new Cat("Tom");
        animals[2] = new Animal("Hoppy");

        for (Animal a : animals) {
            a.speak();
        }
    }
}
"""
CAST = """public class Walk {
    public static void main(String[] args) {
        Animal[] animals = {new Dog("Rex"), new Cat("Tom"), new Dog("Fido")};
        for (Animal a : animals) {
            if (a instanceof Dog) {
                Dog d = (Dog) a;
                d.fetch();
            }
        }
    }
}
"""

# exam guide: "A Programmer Cat is a Cat in Sweater is a Cat is an Object"
CAT2 = """public class Cat {
    private String name;

    public Cat(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return name + " the cat";
    }
}
"""
SWEATER = """public class CatInSweater extends Cat {
    private String color;

    public CatInSweater(String name, String color) {
        super(name);
        this.color = color;
    }

    @Override
    public String toString() {
        return super.toString() + " in a " + color + " sweater";
    }
}
"""
PROGRAMMER = """public class ProgrammerCat extends CatInSweater {
    private String language;

    public ProgrammerCat(String name, String color, String language) {
        super(name, color);
        this.language = language;
    }

    @Override
    public String toString() {
        return super.toString() + ", writing " + language;
    }
}
"""
CHAIN_T = """public class CatTester {
    public static void main(String[] args) {
        ProgrammerCat byte1 = new ProgrammerCat("Byte", "green", "Java");
        CatInSweater asSweater = byte1;
        Cat asCat = byte1;
        Object asObject = byte1;

        System.out.println(byte1);
        System.out.println(asCat);
        System.out.println(asObject);
        System.out.println(asObject instanceof Cat);
    }
}
"""

LESSON = {
    "id": "inh-polymorphism",
    "title": "Polymorphism and the Object class",
    "summary": "A variable of a superclass type can hold any subclass object, and each object still runs its own version of a method.",
    "goals": [
        "Store subclass objects in superclass variables and arrays",
        "Predict which version of an overridden method runs",
        "Use `instanceof` and a cast to reach subclass-only methods",
        "Explain that every class ultimately inherits from `Object`, and summarize the four core ideas of OOP",
    ],
    "cos225": "The exam guide lists polymorphism (\"cats and dogs can be used where animals can be used\"), the question \"what does everything ultimately inherit from?\", and the four core features of Java OOP. All three are in this lesson; the four features are summarized at the end.",
    "blocks": [
        {"type": "h", "text": "A dog can be used where an animal is expected"},
        {"type": "p", "text": "Because a `Dog` **is an** `Animal`, Java lets you store a `Dog` in a variable or array of type `Animal`. **Polymorphism** (Greek for \"many forms\") means one variable type can hold objects of many classes, and when you call an overridden method, **the object's actual class decides which version runs**."},
        {"type": "code", "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "Cat.java": CAT, "Shelter.java": SHELTER}, "run": "Shelter"},
        {"type": "p", "text": "The loop doesn't know or care which kind of animal is in each slot. It calls `speak()`, and each object answers in its own way. Add a `Cow` class tomorrow, and this loop works with cows without a single change."},

        {"type": "h", "text": "The variable's type decides what you can call"},
        {"type": "p", "text": "There are two types in play. The **variable's type** (`Animal`) decides which methods the compiler lets you call. The **object's type** (`Dog`) decides which version runs. So `Animal a = new Dog(\"Rex\");` lets you call `a.speak()` (and Rex barks), but not `a.fetch()`: as far as the compiler knows, `a` might be a cat."},
        {"type": "error", "id": "poly-fetch",
         "prompt": "Rex really is a dog, but the variable says `Animal`.",
         "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "Fetch.java": """public class Fetch {
    public static void main(String[] args) {
        Animal a = new Dog("Rex");
        a.speak();
        a.fetch();
    }
}
"""},
         "run": "Fetch", "expect": "compile",
         "question": "Why does the compiler reject `a.fetch()` even though the object is a `Dog`?",
         "choices": ["Because `fetch` is private",
                     "Because the compiler only checks the variable's type, `Animal`, and `Animal` has no `fetch()`",
                     "Because `Rex` was spelled differently",
                     "Because `speak()` must be called last"],
         "answer": 1,
         "explain": "The compiler goes by what the variable promises. The message even says `location: variable a of type Animal`. Declaring `Dog a = new Dog(\"Rex\");` fixes it.",
         "fix": [["Fetch.java", "Animal a = new Dog", "Dog a = new Dog"]],
         "fixed_output": "Rex says Woof!\nRex fetches the ball."},
        {"type": "p", "text": "When you have an `Animal` and need dog-only behavior, check with `instanceof` first, then **cast**: `(Dog) a` tells the compiler to treat the object as a `Dog`. Checking first matters, because casting a `Cat` to `Dog` crashes with a `ClassCastException`."},
        {"type": "code", "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "Cat.java": CAT, "Walk.java": CAST}, "run": "Walk"},

        {"type": "h", "text": "Everything is an Object"},
        {"type": "p", "text": "A class with no `extends` still has a superclass: Java's built-in `Object`. So every class sits in one big hierarchy with `Object` at the top. That's where the `toString()` you've been overriding comes from, along with `equals()` and a few other methods every object has."},
        {"type": "p", "text": "The exam guide puts it this way: a Programmer Cat is a Cat in Sweater, which is a Cat, which is an Object. Here's that chain in code. One object, referred to by four variables of different types:"},
        {"type": "code", "files": {"Cat.java": CAT2, "CatInSweater.java": SWEATER, "ProgrammerCat.java": PROGRAMMER, "CatTester.java": CHAIN_T},
         "run": "CatTester"},
        {"type": "p", "text": "All three `println` calls print the same thing, because they're the same object, and `ProgrammerCat`'s `toString` runs no matter which variable you go through. Each level adds its part with `super.toString()`."},

        {"type": "h", "text": "The four core ideas of OOP"},
        {"type": "p", "text": "You've now used all four of the features the exam guide asks you to know:"},
        {"type": "list", "items": [
            "**Encapsulation**: each object is responsible for its own data. Fields are `private`, and other code goes through methods that can check values (the Classes and objects section).",
            "**Inheritance**: a subclass takes an existing class and adds to it with `extends`. Java allows one direct superclass, but chains can be as long as you like.",
            "**Abstraction**: describe what something does while leaving out how. An abstract method says every car can `start()` without saying how any particular car does it.",
            "**Polymorphism**: objects of different subclasses can be used wherever the superclass is expected, and each runs its own version of overridden methods.",
        ]},

        {"type": "h", "text": "Practice"},
        {"type": "predict", "id": "poly-predict",
         "prompt": "Which version of `speak()` runs for each slot?",
         "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "Cat.java": CAT, "Mix.java": """public class Mix {
    public static void main(String[] args) {
        Animal first = new Cat("Tom");
        Animal second = new Animal("Hoppy");
        Dog third = new Dog("Fido");
        Animal fourth = third;
        first.speak();
        second.speak();
        fourth.speak();
    }
}
"""}, "run": "Mix",
         "choices": ["Tom makes a sound.\nHoppy makes a sound.\nFido makes a sound.",
                     "Tom says Meow.\nHoppy makes a sound.\nFido says Woof!",
                     "Tom says Meow.\nHoppy makes a sound.\nFido makes a sound.",
                     "A compile error: a Dog can't be stored in an Animal variable"],
         "answer": 1,
         "explain": "The object, not the variable, picks the version. `fourth` is an `Animal` variable, but it refers to Fido, a `Dog`, so Fido barks."},
        {"type": "blanks", "id": "poly-count", "title": "Count the dogs",
         "prompt": "Count how many animals in the array are dogs, and make each dog fetch.",
         "files": {"Animal.java": ANIMAL, "Dog.java": DOG, "Cat.java": CAT, "DogCount.java": """public class DogCount {
    public static void main(String[] args) {
        Animal[] animals = {new Dog("Rex"), new Cat("Tom"), new Dog("Fido"), new Cat("Kit")};
        int dogs = 0;
        for (Animal a : animals) {
            if (a [[check]] Dog) {
                dogs++;
                Dog d = [[cast]] a;
                d.fetch();
            }
        }
        System.out.println(dogs + " dogs");
    }
}
"""},
         "run": "DogCount", "output": "Rex fetches the ball.\nFido fetches the ball.\n2 dogs",
         "blanks": {
             "check": {"accept": ["instanceof"], "hint": "Which operator tests an object's class?",
                       "wrong": [{"answer": "==", "why": "`==` compares two values, so Java looks for a variable named `Dog` and finds none. `Dog` is a class, not a value. `instanceof` asks \"is this object a Dog (or a subclass of Dog)?\""}]},
             "cast": {"accept": ["(Dog)"], "hint": "Tell the compiler to treat `a` as a `Dog`.",
                      "wrong": [{"answer": "", "why": "Without a cast, Java won't put an `Animal` into a `Dog` variable, even inside the `instanceof` check. Write `(Dog) a`."},
                                {"answer": "new Dog", "why": "`new Dog a` isn't valid. A cast doesn't create a new object; it changes how the compiler sees an existing one: `(Dog) a`."}]},
         },
         "explain": "`instanceof` makes the cast safe: only dogs get cast to `Dog`."},
        {"type": "quiz", "id": "poly-object",
         "question": "`public class Plant { }` has no `extends`. What is its superclass?",
         "choices": ["It has none", "`Object`", "`Main`", "Whichever class uses it"],
         "answer": 1,
         "explain": "Every class without an explicit `extends` implicitly extends `java.lang.Object`. That's why every object has `toString()`."},
        {"type": "quiz", "id": "poly-pillar",
         "question": "\"Our objects should be responsible for themselves, and not depend on others.\" Which core idea does the exam guide describe with this?",
         "choices": ["Abstraction", "Encapsulation", "Inheritance", "Polymorphism"],
         "answer": 1,
         "explain": "Encapsulation: private data, managed by the object's own methods. Abstraction is about leaving out details (like how each car starts), inheritance about extending a class, and polymorphism about using subclasses where a superclass is expected."},
    ],
    "sources": [POLY_TUT, SUBCLASSES_TUT, OBJECT_TUT, OBJECT_API, JLS_INSTANCEOF, HEL_9_3],
}
