from sources import SUPER_TUT, JLS_CTOR_BODY, JLS_DEFAULT_CTOR, CONSTRUCTORS_TUT, ACCESS_TUT, HEL_9_1

PERSON = """public class Person {
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
}
"""

EMPLOYEE = """public class Employee extends Person {
    private double salary;

    public Employee(String name, int age, double salary) {
        super(name, age);
        this.salary = salary;
    }

    public double getSalary() {
        return salary;
    }
}
"""

TESTER = """public class EmployeeTester {
    public static void main(String[] args) {
        Employee jo = new Employee("Jo", 34, 52000.0);
        System.out.println(jo.getName() + ", " + jo.getAge());
        System.out.println("Salary: " + jo.getSalary());
    }
}
"""

ORDER_A = """public class Building {
    public Building() {
        System.out.println("Building constructor");
    }
}
"""
ORDER_B = """public class House extends Building {
    public House() {
        System.out.println("House constructor");
    }
}
"""
ORDER_C = """public class Cabin extends House {
    public Cabin() {
        super();
        System.out.println("Cabin constructor");
    }
}
"""
ORDER_T = """public class BuildTester {
    public static void main(String[] args) {
        new Cabin();
    }
}
"""

LESSON = {
    "id": "inh-super",
    "title": "Calling the parent with super",
    "summary": "A subclass object contains a superclass part, and `super(...)` is how the subclass's constructor sets that part up.",
    "goals": [
        "Write a subclass constructor that passes values to the superclass with `super(...)`",
        "Add new fields in a subclass while the superclass keeps its own fields private",
        "Predict the order constructors run in, and read the errors when `super` is missing or misplaced",
    ],
    "cos225": "The exam guide says encapsulation \"also refers to the management of data members in each class in an inheritance hierarchy\". In practice: each class stores and protects its own fields, and a subclass reaches the parent's through `super(...)` and getters.",
    "blocks": [
        {"type": "h", "text": "Each class sets up its own fields"},
        {"type": "p", "text": "An `Employee` is a `Person` with a salary. `Person` already knows how to store a name and an age, and those fields are private, so `Employee` couldn't set them even if it wanted to. Instead, its constructor calls `super(name, age)`: \"run my superclass's constructor with these values\". Then it sets the one field that belongs to `Employee`."},
        {"type": "code", "files": {"Person.java": PERSON, "Employee.java": EMPLOYEE, "EmployeeTester.java": TESTER}, "run": "EmployeeTester"},
        {"type": "list", "items": [
            "`super(...)` must be the **first statement** in the constructor, because the superclass part has to be ready before the subclass adds to it.",
            "The arguments must match one of the superclass's constructors, just like a normal `new` call.",
            "`Employee` reads the name with the inherited `getName()`. The subclass doesn't need its own copy of `name`.",
        ]},

        {"type": "h", "text": "Constructors run from the top down"},
        {"type": "p", "text": "When you create a subclass object, the superclass's constructor runs first, then the subclass's. In a longer chain, Java starts at the top. If a constructor doesn't call `super(...)` itself, Java quietly inserts `super();` (a call to the no-parameter constructor) as its first line."},
        {"type": "predict", "id": "super-order",
         "prompt": "`Cabin extends House`, and `House extends Building`. Only `Cabin` calls `super()` explicitly. What does `new Cabin()` print?",
         "files": {"Building.java": ORDER_A, "House.java": ORDER_B, "Cabin.java": ORDER_C, "BuildTester.java": ORDER_T},
         "run": "BuildTester",
         "choices": ["Cabin constructor",
                     "Cabin constructor\nHouse constructor\nBuilding constructor",
                     "Building constructor\nHouse constructor\nCabin constructor",
                     "House constructor\nCabin constructor"],
         "answer": 2,
         "explain": "`Cabin`'s `super()` runs `House`'s constructor before printing anything. `House` has no `super` line, so Java inserts `super();`, which runs `Building`'s constructor first. The prints happen as each constructor finishes its `super` call: top of the chain first."},

        {"type": "h", "text": "When the automatic super() doesn't work"},
        {"type": "p", "text": "The inserted `super();` only works if the superclass has a constructor with no parameters. `Person` has only `Person(String, int)`, so a subclass that forgets to call `super(...)` doesn't compile:"},
        {"type": "error", "id": "super-missing",
         "prompt": "This `Employee` constructor forgot `super(...)`.",
         "files": {"Person.java": PERSON, "Employee.java": EMPLOYEE.replace("        super(name, age);\n", ""),
                   "EmployeeTester.java": TESTER},
         "run": "EmployeeTester", "expect": "compile",
         "question": "Why does the compiler talk about `Person`'s constructor when the mistake is in `Employee`?",
         "choices": ["Because `Person.java` has a syntax error",
                     "Because Java inserted `super();` for you, and `Person` has no constructor without parameters",
                     "Because `salary` should be declared in `Person`",
                     "Because subclasses can't have constructors"],
         "answer": 1,
         "explain": "With no `super(...)` written, Java calls `super()`, meaning `Person()`. That constructor doesn't exist (\"actual and formal argument lists differ in length\"). Pass the name and age up with `super(name, age);`.",
         "fix": [["Employee.java", "    public Employee(String name, int age, double salary) {\n",
                  "    public Employee(String name, int age, double salary) {\n        super(name, age);\n"]]},
        {"type": "error", "id": "super-not-first",
         "prompt": "Here `super(...)` is called, but not first.",
         "files": {"Person.java": PERSON, "Employee.java": EMPLOYEE.replace(
             "        super(name, age);\n        this.salary = salary;\n",
             "        this.salary = salary;\n        super(name, age);\n"), "EmployeeTester.java": TESTER},
         "run": "EmployeeTester", "expect": "compile",
         "question": "How do you fix it?",
         "choices": ["Move `super(name, age);` to the first line of the constructor",
                     "Change `super` to `this`",
                     "Delete the `salary` line",
                     "Make `salary` public"],
         "answer": 0,
         "explain": "The superclass part must be built before anything else happens in the subclass constructor, so Java requires `super(...)` as the very first statement.",
         "fix": [["Employee.java", "        this.salary = salary;\n        super(name, age);\n",
                  "        super(name, age);\n        this.salary = salary;\n"]]},

        {"type": "note", "label": "What about protected?",
         "text": "Java has a fourth access level, `protected`, which lets subclasses use a field directly. Oracle's tutorial recommends using the most restrictive access that makes sense, so this course keeps fields `private` and gives subclasses getters. You'll see `protected` in other people's code; it's not wrong, but it ties subclasses to the parent's internals."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "super-manager", "title": "Pass values up the chain",
         "prompt": "`Manager` is an `Employee` that also has a team size. Finish its constructor.",
         "files": {"Person.java": PERSON, "Employee.java": EMPLOYEE, "Manager.java": """public class Manager extends Employee {
    private int teamSize;

    public Manager(String name, int age, double salary, int teamSize) {
        [[sup]];
        [[own]] = teamSize;
    }

    public int getTeamSize() {
        return teamSize;
    }
}
""", "ManagerTester.java": """public class ManagerTester {
    public static void main(String[] args) {
        Manager kim = new Manager("Kim", 45, 78000.0, 6);
        System.out.println(kim.getName() + " manages " + kim.getTeamSize() + " people.");
        System.out.println("Salary: " + kim.getSalary());
    }
}
"""},
         "run": "ManagerTester", "output": "Kim manages 6 people.\nSalary: 78000.0",
         "blanks": {
             "sup": {"accept": ["super(name, age, salary)"], "hint": "`Manager`'s parent is `Employee`, whose constructor takes three values.",
                     "wrong": [{"answer": "super(name, age)", "why": "`Manager`'s direct superclass is `Employee`, not `Person`, and `Employee`'s constructor needs the salary too."},
                               {"answer": "super(name, age, salary, teamSize)", "why": "`Employee` has no constructor with four parameters. The team size belongs to `Manager`, so set it here instead."}]},
             "own": {"accept": ["this.teamSize"], "hint": "The parameter and the field have the same name.",
                     "wrong": [{"answer": "teamSize", "why": "`teamSize = teamSize;` assigns the parameter to itself, so the field stays 0. Use `this.teamSize`."}]},
         },
         "explain": "Each class in the chain stores its own fields: `Person` the name and age, `Employee` the salary, `Manager` the team size."},
        {"type": "quiz", "id": "super-first",
         "question": "Which rule about `super(...)` in a constructor is correct?",
         "choices": ["It can go anywhere in the constructor",
                     "It must be the first statement, and if you leave it out Java inserts `super()`",
                     "It's only needed when the subclass has no fields",
                     "It calls the subclass's other constructor"],
         "answer": 1,
         "explain": "`super(...)` comes first. Leave it out and Java inserts a call to the superclass's no-parameter constructor, which is a compile error if that constructor doesn't exist. Calling another constructor of the same class is `this(...)`."},
    ],
    "sources": [SUPER_TUT, JLS_CTOR_BODY, JLS_DEFAULT_CTOR, CONSTRUCTORS_TUT, ACCESS_TUT, HEL_9_1],
}
