from sources import ABSTRACT_TUT, JLS_ABSTRACT, OVERRIDE_TUT, HEL_9_1

SHAPE = """public abstract class Shape {
    private String name;

    public Shape(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public abstract double area();

    public void describe() {
        System.out.println(name + " with area " + area());
    }
}
"""

RECT = """public class Rectangle extends Shape {
    private double width;
    private double height;

    public Rectangle(double width, double height) {
        super("Rectangle");
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }
}
"""

TRI = """public class Triangle extends Shape {
    private double base;
    private double height;

    public Triangle(double base, double height) {
        super("Triangle");
        this.base = base;
        this.height = height;
    }

    @Override
    public double area() {
        return base * height / 2;
    }
}
"""

TESTER = """public class ShapeTester {
    public static void main(String[] args) {
        Rectangle r = new Rectangle(3, 4);
        Triangle t = new Triangle(6, 5);
        r.describe();
        t.describe();
    }
}
"""

LESSON = {
    "id": "inh-abstract",
    "title": "Abstract classes",
    "summary": "Declare a behavior every subclass must have, without saying how it works, and let each subclass fill it in.",
    "goals": [
        "Write an `abstract` method and an `abstract` class",
        "Explain why you can't create an object of an abstract class",
        "Write a subclass that implements every abstract method it inherits",
    ],
    "cos225": "From the exam guide: an abstract method defines a behavior that derived classes are required to implement, without saying how it works. \"A car should start, but each car starts its own way.\" You \"cannot inherit a class without defining its abstract methods\". An abstract class can be entirely abstract, or define a few things and leave the rest to the subclasses.",
    "blocks": [
        {"type": "h", "text": "A method with no body"},
        {"type": "p", "text": "Every shape has an area, but there's no single formula: a rectangle multiplies, a triangle halves. `Shape` can promise that every shape has `area()` without writing a body for it. That's an **abstract method**: the word `abstract`, the method header, and a semicolon instead of braces."},
        {"type": "p", "text": "A class with an abstract method must itself be marked `abstract`. An abstract class can still have fields, a constructor and ordinary methods. Here, `describe()` is a normal method that calls the abstract `area()`, trusting each subclass to provide it."},
        {"type": "code", "files": {"Shape.java": SHAPE, "Rectangle.java": RECT, "Triangle.java": TRI, "ShapeTester.java": TESTER},
         "run": "ShapeTester"},
        {"type": "list", "items": [
            "`public abstract double area();` has no body, just a semicolon.",
            "Each subclass **implements** `area()` by overriding it with a real body. `@Override` works here too.",
            "`describe()` is written once, in `Shape`, and works for every subclass, because each one supplies its own `area()`.",
            "This is **abstraction**: `Shape` describes what all shapes can do, while leaving out details it can't know.",
        ]},

        {"type": "h", "text": "Two rules the compiler enforces"},
        {"type": "p", "text": "**You can't create an object of an abstract class.** A plain `Shape` would have no way to compute its area, so `new Shape(...)` is an error:"},
        {"type": "code", "files": {"Shape.java": SHAPE, "MakeShape.java": """public class MakeShape {
    public static void main(String[] args) {
        Shape s = new Shape("Blob");
        s.describe();
    }
}
"""}, "run": "MakeShape", "expect": "compile"},
        {"type": "p", "text": "**A subclass must implement every abstract method it inherits**, or be declared abstract itself. Forgetting one is caught at compile time, with a message that names the missing method:"},
        {"type": "error", "id": "abstract-missing",
         "prompt": "This `Circle` forgot something.",
         "files": {"Shape.java": SHAPE, "Circle.java": """public class Circle extends Shape {
    private double radius;

    public Circle(double radius) {
        super("Circle");
        this.radius = radius;
    }
}
""", "CircleTester.java": """public class CircleTester {
    public static void main(String[] args) {
        new Circle(1).describe();
    }
}
"""},
         "run": "CircleTester", "expect": "compile",
         "question": "What does the message ask for?",
         "choices": ["Remove `abstract` from `Shape`",
                     "Give `Circle` an `area()` method (or make `Circle` abstract too)",
                     "Add a `describe()` method to `Circle`",
                     "Change `radius` to an `int`"],
         "answer": 1,
         "explain": "\"`Circle` is not abstract and does not override abstract method `area()` in `Shape`\": it inherited a promise it didn't keep. Implement `area()`. `describe()` is already inherited.",
         "fix": [["Circle.java", "        this.radius = radius;\n    }\n}\n",
                  "        this.radius = radius;\n    }\n\n    @Override\n    public double area() {\n        return 3 * radius * radius;\n    }\n}\n"]],
         "fixed_output": "Circle with area 3.0"},
        {"type": "p", "text": "(The fix above uses 3 instead of π just to keep the number short. A real circle would use `Math.PI`.)"},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "abstract-car", "title": "Each car starts its own way",
         "prompt": "Finish the exam guide's example: every `Car` can `start()`, but each kind of car starts differently.",
         "files": {"Car.java": """public [[cls]] class Car {
    private String model;

    public Car(String model) {
        this.model = model;
    }

    public String getModel() {
        return model;
    }

    public abstract void start()[[end]]
}
""", "ElectricCar.java": """public class ElectricCar extends Car {
    public ElectricCar(String model) {
        super(model);
    }

    @Override
    public void [[name]]() {
        System.out.println(getModel() + " hums silently.");
    }
}
""", "CarTester.java": """public class CarTester {
    public static void main(String[] args) {
        ElectricCar volt = new ElectricCar("Volt");
        volt.start();
    }
}
"""},
         "run": "CarTester", "output": "Volt hums silently.",
         "blanks": {
             "cls": {"accept": ["abstract"], "hint": "A class with an abstract method must say so.",
                     "wrong": [{"answer": "", "why": "Without `abstract` on the class, `Car` would claim to be complete while one of its methods has no body. Java points at the class."}]},
             "end": {"accept": [";"], "hint": "An abstract method has no body. What ends it instead of braces?",
                     "wrong": [{"answer": "{}", "why": "Braces give the method a body, even an empty one, and abstract methods can't have one."}]},
             "name": {"accept": ["start"], "hint": "The subclass must implement the abstract method with the same name.",
                      "wrong": [{"answer": "go", "why": "`go()` is a new method, so `start()` is still unimplemented, and `@Override` complains that `go` doesn't override anything."}]},
         },
         "explain": "`Car` promises `start()`, and `ElectricCar` keeps the promise. A `GasCar` would write its own `start()` that does something else."},
        {"type": "quiz", "id": "abstract-can-have",
         "question": "Which of these can an abstract class NOT do?",
         "choices": ["Have private fields", "Have a constructor", "Have methods with bodies", "Be created directly with `new`"],
         "answer": 3,
         "explain": "An abstract class can have fields, constructors and normal methods; subclasses use them through `super(...)` and inheritance. What it can't do is be instantiated with `new`."},
        {"type": "quiz", "id": "abstract-only",
         "question": "An abstract class has 3 abstract methods. A subclass implements 2 of them. What happens?",
         "choices": ["It compiles; the third method does nothing",
                     "It's a compile error, unless the subclass is also declared `abstract`",
                     "It compiles, but crashes when the third method is called",
                     "Java writes the third method automatically"],
         "answer": 1,
         "explain": "A concrete (non-abstract) class must implement every abstract method it inherits. A subclass that's also `abstract` can leave some for its own subclasses."},
    ],
    "sources": [ABSTRACT_TUT, JLS_ABSTRACT, OVERRIDE_TUT, HEL_9_1],
}
