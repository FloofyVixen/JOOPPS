from sources import (SUBCLASSES_TUT, ABSTRACT_TUT, IFACE_TUT, POLY_TUT, ACCESS_TUT, ARRAYS_TUT,
                     OVERRIDE_TUT, ARRAYLIST_API, MIT_ADT)
from tasks_classes import task

ANIMAL = """public class Animal {
    private String name;

    public Animal(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
"""

BOOK = """public class Book {
    private String title;
    private boolean available;

    public Book(String title) {
        this.title = title;
        available = true;
    }

    public String getTitle() {
        return title;
    }

    public boolean isAvailable() {
        return available;
    }

    public void checkOut() {
        available = false;
    }
}
"""
LIB_SOLUTION = """public class Library {
    private Book[] books;

    public Library(Book[] books) {
        this.books = books;
    }

    public int countAvailable() {
        int count = 0;
        for (Book b : books) {
            if (b != null && b.isAvailable()) {
                count++;
            }
        }
        return count;
    }

    public Book find(String title) {
        for (Book b : books) {
            if (b != null && b.getTitle().equals(title)) {
                return b;
            }
        }
        return null;
    }
}
"""
LIB_STARTER = """public class Library {
    private Book[] books;

    public Library(Book[] books) {
        this.books = books;
    }

    public int countAvailable() {
        // Fill in: how many non-empty slots hold an available book?
        return 0;
    }

    public Book find(String title) {
        // Fill in: the book with this title, or null if there isn't one.
        return null;
    }
}
"""
LIB_TESTER = """public class LibraryTester {
    public static void main(String[] args) {
        Book[] shelf = {new Book("Night Trains"), null, new Book("Low Tide"), new Book("Northbound")};
        Library lib = new Library(shelf);
        System.out.println(lib.countAvailable());
        lib.find("Low Tide").checkOut();
        System.out.println(lib.countAvailable());
        System.out.println(lib.find("Missing Book"));
    }
}
"""

SHAPE = """public interface Shape {
    double area();
}
"""
SHAPES_SOLUTION = {"Shape.java": SHAPE, "Square.java": """public class Square implements Shape {
    private double side;

    public Square(double side) {
        this.side = side;
    }

    @Override
    public double area() {
        return side * side;
    }
}
""", "Triangle.java": """public class Triangle implements Shape {
    private double base;
    private double height;

    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    @Override
    public double area() {
        return base * height / 2;
    }
}
""", "Shapes.java": """public class Shapes {
    public static Shape largest(Shape[] shapes) {
        Shape best = shapes[0];
        for (Shape s : shapes) {
            if (s.area() > best.area()) {
                best = s;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        Shape[] all = {new Square(3), new Triangle(10, 4), new Square(4)};
        System.out.println(largest(all).area());
    }
}
"""}
SHAPES_STARTER = dict(SHAPES_SOLUTION)
SHAPES_STARTER["Square.java"] = SHAPES_SOLUTION["Square.java"].replace("        return side * side;", "        // Fill in\n        return 0;")
SHAPES_STARTER["Triangle.java"] = SHAPES_SOLUTION["Triangle.java"].replace("        return base * height / 2;", "        // Fill in\n        return 0;")
SHAPES_STARTER["Shapes.java"] = SHAPES_SOLUTION["Shapes.java"].replace("""        Shape best = shapes[0];
        for (Shape s : shapes) {
            if (s.area() > best.area()) {
                best = s;
            }
        }
        return best;""", """        // Fill in: return the shape with the largest area (the array is never empty)
        return shapes[0];""")

FILL_LIB = task("ex1-fill-library", "Fill in: a library's methods",
                "`Book` is finished. In `Library`, fill in the bodies of `countAvailable()` and `find(String title)`. Some slots in the array may be `null`.",
                {"Book.java": BOOK, "Library.java": LIB_SOLUTION, "LibraryTester.java": LIB_TESTER}, "LibraryTester",
                "3\n2\nnull",
                requirements=["Only change the two method bodies marked \"Fill in\""],
                hints=["Both loops need the null check first: `b != null && ...`", "Compare titles with `equals`."])
FILL_LIB["starter"] = {"Book.java": BOOK, "Library.java": LIB_STARTER, "LibraryTester.java": LIB_TESTER}

FILL_SHAPES = task("ex1-fill-shapes", "Fill in: shapes behind an interface",
                   "Fill in `area()` for `Square` and `Triangle`, and `largest(Shape[] shapes)` in `Shapes`.",
                   SHAPES_SOLUTION, "Shapes", "20.0",
                   requirements=["Only change the bodies marked \"Fill in\""],
                   hints=["`largest` keeps the best shape so far and compares areas."])
FILL_SHAPES["starter"] = SHAPES_STARTER

LESSON = {
    "id": "exam-practice-1",
    "title": "Exam practice 1",
    "summary": "A practice set in the COS 225 exam format covering units 1 to 12: short answers, fixing code, filling in method bodies, and writing classes from scratch.",
    "goals": [
        "Answer short definition questions about OOP, inheritance, interfaces and arrays",
        "Find and fix mistakes in small programs",
        "Fill in method bodies and write short classes from scratch",
    ],
    "cos225": "This page follows the exam guide's format: short-answer questions (a few words, or a small snippet), fixing code, filling in blanks that are usually method bodies, and code-writing that \"should not require more than eight lines of code optimally\". The real exam is on paper and lenient about syntax, so try each part on paper before you check it here.",
    "blocks": [
        {"type": "h", "text": "How to use this page"},
        {"type": "list", "items": [
            "Work through it in order, without looking back at the lessons. Afterwards, revisit only the topics you missed.",
            "For the coding parts, write your answer on paper first. Then type it in and run it, and let the compiler and the tests tell you what you missed.",
            "The exam guide's advice: stay calm, and spend a few minutes reading each coding problem before you write anything.",
        ]},

        {"type": "h", "text": "Part A: short answers"},
        {"type": "quiz", "id": "ex1-q-new",
         "question": "What does the keyword `new` do in `Dog rex = new Dog(\"Rex\");`?",
         "choices": ["Declares the variable `rex`", "Creates a new `Dog` object and runs its constructor", "Makes `Dog` a subclass", "Copies an existing dog"],
         "answer": 1, "explain": "`new` instantiates: it creates the object and runs the matching constructor. The variable then refers to it."},
        {"type": "quiz", "id": "ex1-q-super",
         "question": "In `class Truck extends Vehicle`, which is the superclass?",
         "choices": ["`Truck`", "`Vehicle`", "`Object`, always", "Neither; `extends` is for interfaces"],
         "answer": 1, "explain": "The class after `extends` is the superclass. `Truck` is the subclass that inherits from it."},
        {"type": "quiz", "id": "ex1-q-object",
         "question": "A class is written with no `extends`. What does it inherit from?",
         "choices": ["Nothing", "`Object`", "The class that uses it", "Its interface"],
         "answer": 1, "explain": "Every class without an explicit superclass extends `java.lang.Object`."},
        {"type": "quiz", "id": "ex1-q-implements",
         "question": "How many classes can a class extend, and how many interfaces can it implement?",
         "choices": ["One class; one interface", "Any number of each", "One class; any number of interfaces", "No classes; any number of interfaces"],
         "answer": 2, "explain": "Single inheritance for classes, but a class may implement multiple interfaces, as long as it implements all of their methods."},
        {"type": "quiz", "id": "ex1-q-abstract",
         "question": "What is an abstract method?",
         "choices": ["A method that's `private`", "A method with no body that every concrete subclass must implement",
                     "A method that can only be called once", "A method inherited from `Object`"],
         "answer": 1, "explain": "It defines a behavior without saying how it works: \"a car should start, but each car starts its own way\". A class with one must be abstract."},
        {"type": "quiz", "id": "ex1-q-encap",
         "question": "Which line best shows encapsulation?",
         "choices": ["`public int balance;`", "`private int balance;` with a `deposit` method that rejects negative amounts",
                     "`class Savings extends Account`", "`Animal a = new Dog();`"],
         "answer": 1, "explain": "Encapsulation: the object protects its own data and controls changes through its methods."},
        {"type": "quiz", "id": "ex1-q-poly",
         "question": "`Animal[] pets = {new Dog(\"Rex\"), new Cat(\"Tom\")};` and each overrides `speak()`. What does polymorphism mean here?",
         "choices": ["Both print the `Animal` version", "Each object runs its own class's `speak()`",
                     "The array can only hold one kind of animal", "`speak()` must be static"],
         "answer": 1, "explain": "Cats and dogs can be used where animals are expected, and each still behaves as its own class."},
        {"type": "quiz", "id": "ex1-q-override",
         "question": "What does `@Override` do?",
         "choices": ["Makes a method run faster", "Asks the compiler to confirm the method really replaces an inherited one",
                     "Makes a method private", "Creates a new method"],
         "answer": 1, "explain": "If the method doesn't match one in a superclass or interface (say, there's a typo), the compiler reports an error."},
        {"type": "quiz", "id": "ex1-q-array",
         "question": "`String[] names = new String[4];` What is `names[3]` right after this line?",
         "choices": ["`\"\"`", "`null`", "An error", "`\"names3\"`"],
         "answer": 1, "explain": "A new array of objects has `null` in every slot. Index 3 is the last valid one, since `length` is 4."},
        {"type": "quiz", "id": "ex1-q-list",
         "question": "What's the main difference between an array and an `ArrayList`?",
         "choices": ["An `ArrayList` can only hold numbers", "An array's size is fixed; an `ArrayList` grows as you add",
                     "Arrays are slower to index", "An `ArrayList` can't be looped over"],
         "answer": 1, "explain": "An `ArrayList` is a list ADT backed by an array that it resizes for you."},

        {"type": "h", "text": "Part B: fix the code"},
        {"type": "error", "id": "ex1-fix-super",
         "prompt": "`Dog` won't compile.",
         "files": {"Animal.java": ANIMAL, "Dog.java": """public class Dog extends Animal {
    private String breed;

    public Dog(String name, String breed) {
        this.breed = breed;
    }
}
""", "DogTester.java": """public class DogTester {
    public static void main(String[] args) {
        Dog d = new Dog("Rex", "lab");
        System.out.println(d.getName());
    }
}
"""},
         "run": "DogTester", "expect": "compile",
         "question": "What single line fixes it?",
         "choices": ["`this.name = name;` in `Dog`", "`super(name);` as the first line of `Dog`'s constructor",
                     "`super();` as the last line", "Delete `extends Animal`"],
         "answer": 1,
         "explain": "`Animal` has no no-argument constructor, so `Dog` must pass the name up with `super(name);` first. `name` is private to `Animal`.",
         "fix": [["Dog.java", "    public Dog(String name, String breed) {\n", "    public Dog(String name, String breed) {\n        super(name);\n"]],
         "fixed_output": "Rex"},
        {"type": "error", "id": "ex1-fix-iface",
         "prompt": "`Fan` claims to implement `Switchable`.",
         "files": {"Switchable.java": """public interface Switchable {
    void turnOn();
}
""", "Fan.java": """public class Fan implements Switchable {
    void turnOn() {
        System.out.println("Fan on");
    }
}
""", "FanTester.java": """public class FanTester {
    public static void main(String[] args) {
        new Fan().turnOn();
    }
}
"""},
         "run": "FanTester", "expect": "compile",
         "question": "What's wrong?",
         "choices": ["`turnOn` must be `public`", "`Fan` must extend `Switchable`", "Interfaces can't have methods", "`turnOn` must return `boolean`"],
         "answer": 0,
         "explain": "Interface methods are public, and an implementation can't be less accessible.",
         "fix": [["Fan.java", "    void turnOn() {", "    public void turnOn() {"]],
         "fixed_output": "Fan on"},
        {"type": "error", "id": "ex1-fix-loop",
         "prompt": "This compiles, but crashes.",
         "files": {"Total.java": """public class Total {
    public static void main(String[] args) {
        int[] prices = {4, 10, 6};
        int sum = 0;
        for (int i = 1; i <= prices.length; i++) {
            sum = sum + prices[i];
        }
        System.out.println(sum);
    }
}
"""},
         "run": "Total", "expect": "runtime",
         "question": "Which loop header is correct?",
         "choices": ["`for (int i = 1; i < prices.length; i++)`", "`for (int i = 0; i < prices.length; i++)`",
                     "`for (int i = 0; i <= prices.length; i++)`", "`for (int i = 1; i <= prices.length - 1; i++)`"],
         "answer": 1,
         "explain": "Indexes run from 0 to `length - 1`. The original skipped index 0 and then went past the end.",
         "fix": [["Total.java", "for (int i = 1; i <= prices.length; i++)", "for (int i = 0; i < prices.length; i++)"]],
         "fixed_output": "20"},

        {"type": "h", "text": "Part C: fill in the method bodies"},
        {"type": "p", "text": "Each file below compiles but gives wrong answers, because the method bodies are placeholders. Replace the placeholders, then run."},
        FILL_LIB,
        FILL_SHAPES,

        {"type": "h", "text": "Part D: write it from scratch"},
        task("ex1-write-temp", "A class with two constructors",
             "Write `Temperature` with a private `double degrees`. The default constructor sets 20.0; another constructor takes the degrees. Add `getDegrees()`, `setDegrees(double)` that ignores values below -273.15, and a `toString` like `20.0 C`.",
             {"Temperature.java": """public class Temperature {
    private double degrees;

    public Temperature() {
        degrees = 20.0;
    }

    public Temperature(double degrees) {
        this.degrees = degrees;
    }

    public double getDegrees() {
        return degrees;
    }

    public void setDegrees(double degrees) {
        if (degrees >= -273.15) {
            this.degrees = degrees;
        }
    }

    @Override
    public String toString() {
        return degrees + " C";
    }
}
""", "TempTester.java": """public class TempTester {
    public static void main(String[] args) {
        Temperature room = new Temperature();
        Temperature oven = new Temperature(180.0);
        System.out.println(room + ", " + oven);
        room.setDegrees(-500);
        System.out.println(room.getDegrees());
    }
}
"""}, "TempTester", "20.0 C, 180.0 C\n20.0",
             tests={"CheckTemp.java": """public class CheckTemp {
    public static void main(String[] args) {
        Temperature t = new Temperature(5);
        t.setDegrees(-273.15);
        System.out.println(t);
    }
}
"""}, tests_run="CheckTemp", tests_output="-273.15 C"),
        task("ex1-write-intern", "A superclass and a subclass",
             "Write `Worker` (private `name`, constructor, `getName()`, and `weeklyPay()` returning 800.0) and `Intern extends Worker`, which overrides `weeklyPay()` to return half of a worker's pay by calling `super.weeklyPay()`.",
             {"Worker.java": """public class Worker {
    private String name;

    public Worker(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public double weeklyPay() {
        return 800.0;
    }
}
""", "Intern.java": """public class Intern extends Worker {
    public Intern(String name) {
        super(name);
    }

    @Override
    public double weeklyPay() {
        return super.weeklyPay() / 2;
    }
}
""", "PayTester.java": """public class PayTester {
    public static void main(String[] args) {
        Worker[] team = {new Worker("Ana"), new Intern("Leo")};
        for (Worker w : team) {
            System.out.println(w.getName() + ": " + w.weeklyPay());
        }
    }
}
"""}, "PayTester", "Ana: 800.0\nLeo: 400.0",
             tests={"CheckPay.java": """public class CheckPay {
    public static void main(String[] args) {
        Worker w = new Intern("Kai");
        System.out.println(w.weeklyPay());
    }
}
"""}, tests_run="CheckPay", tests_output="400.0",
             checks=[{"pattern": r"super\.weeklyPay\s*\(\s*\)", "message": "Use `super.weeklyPay()` in `Intern`."}]),
        task("ex1-write-discount", "An interface and a class",
             "Write an interface `Discountable` with `double finalPrice()`, and a class `SaleItem` (private `price` and `percentOff`) that implements it: the final price is the price minus that percentage.",
             {"Discountable.java": """public interface Discountable {
    double finalPrice();
}
""", "SaleItem.java": """public class SaleItem implements Discountable {
    private double price;
    private int percentOff;

    public SaleItem(double price, int percentOff) {
        this.price = price;
        this.percentOff = percentOff;
    }

    @Override
    public double finalPrice() {
        return price - price * percentOff / 100;
    }
}
""", "SaleTester.java": """public class SaleTester {
    public static void main(String[] args) {
        Discountable lamp = new SaleItem(40.0, 25);
        System.out.println(lamp.finalPrice());
    }
}
"""}, "SaleTester", "30.0",
             tests={"CheckSale.java": """public class CheckSale {
    public static void main(String[] args) {
        System.out.println(new SaleItem(10.0, 0).finalPrice());
        System.out.println(new SaleItem(80.0, 50).finalPrice());
    }
}
"""}, tests_run="CheckSale", tests_output="10.0\n40.0",
             checks=[{"pattern": r"interface\s+Discountable", "message": "Declare `Discountable` as an interface."}]),
    ],
    "sources": [SUBCLASSES_TUT, ABSTRACT_TUT, IFACE_TUT, POLY_TUT, OVERRIDE_TUT, ACCESS_TUT, ARRAYS_TUT, ARRAYLIST_API, MIT_ADT],
}
