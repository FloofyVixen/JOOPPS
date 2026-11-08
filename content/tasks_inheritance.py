"""Write-it-yourself tasks for the Inheritance section.
Every solution and test file here is compiled and run by build.py."""
from tasks_classes import task

EXT = [
    task("w-truck", "A superclass and a subclass",
         "Write `Vehicle` with a private `make`, a constructor, `getMake()` and `honk()` (prints `<make> honks.`). Write `Truck extends Vehicle`, which adds `load(int tons)` (prints `<make> truck loads <tons> tons.`). In `TruckTester`, make a Volvo truck honk and load 8 tons.",
         {"Vehicle.java": """public class Vehicle {
    private String make;

    public Vehicle(String make) {
        this.make = make;
    }

    public String getMake() {
        return make;
    }

    public void honk() {
        System.out.println(make + " honks.");
    }
}
""", "Truck.java": """public class Truck extends Vehicle {
    public Truck(String make) {
        super(make);
    }

    public void load(int tons) {
        System.out.println(getMake() + " truck loads " + tons + " tons.");
    }
}
""", "TruckTester.java": """public class TruckTester {
    public static void main(String[] args) {
        Truck volvo = new Truck("Volvo");
        volvo.honk();
        volvo.load(8);
    }
}
"""}, "TruckTester", "Volvo honks.\nVolvo truck loads 8 tons.",
         tests={"CheckTruck.java": """public class CheckTruck {
    public static void main(String[] args) {
        Truck mack = new Truck("Mack");
        mack.honk();
        mack.load(1);
        new Vehicle("Ford").honk();
    }
}
"""}, tests_run="CheckTruck", tests_output="Mack honks.\nMack truck loads 1 tons.\nFord honks.",
         requirements=["`Truck` doesn't declare its own `make` field or `honk()`; it inherits them"],
         hints=["`Truck`'s constructor is one line: `super(make);`", "Inside `Truck`, read the make with `getMake()`."],
         checks=[{"pattern": r"class\s+Truck\s+extends\s+Vehicle", "message": "Declare `public class Truck extends Vehicle`."}]),

    task("w-savingsaccount", "A subclass that uses inherited methods",
         "Write `Account` (private `double balance`, a constructor, `getBalance()`, and `deposit(double)` for positive amounts) and `SavingsAccount extends Account`, which also stores an interest rate. `addInterest()` deposits `balance × rate`, using only the inherited methods.",
         {"Account.java": """public class Account {
    private double balance;

    public Account(double balance) {
        this.balance = balance;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance = balance + amount;
        }
    }
}
""", "SavingsAccount.java": """public class SavingsAccount extends Account {
    private double rate;

    public SavingsAccount(double balance, double rate) {
        super(balance);
        this.rate = rate;
    }

    public void addInterest() {
        deposit(getBalance() * rate);
    }
}
""", "SavingsTester.java": """public class SavingsTester {
    public static void main(String[] args) {
        SavingsAccount savings = new SavingsAccount(200.0, 0.05);
        savings.addInterest();
        System.out.println(savings.getBalance());
    }
}
"""}, "SavingsTester", "210.0",
         tests={"CheckSavings.java": """public class CheckSavings {
    public static void main(String[] args) {
        SavingsAccount s = new SavingsAccount(40.0, 0.25);
        s.addInterest();
        System.out.println(s.getBalance());
        s.deposit(-5.0);
        System.out.println(s.getBalance());
    }
}
"""}, tests_run="CheckSavings", tests_output="50.0\n50.0",
         requirements=["`balance` stays `private` in `Account`", "`SavingsAccount` changes the balance only by calling `deposit`"],
         hints=["`SavingsAccount(double balance, double rate)` passes the balance up with `super(balance);`, then stores the rate.",
                "`addInterest` is one line: `deposit(getBalance() * rate);`"],
         checks=[{"pattern": r"private\s+double\s+balance", "message": "Keep `balance` as `private double balance` in `Account`."}]),

    task("w-devices", "A chain of three classes",
         "Write `Device` (private `name`, `getName()`, `powerOn()` prints `<name> is on.`), `Phone extends Device` (adds `call(String who)`, which prints `<name> calls <who>.`) and `SmartPhone extends Phone` (adds `browse()`, which prints `<name> opens the browser.`). A `SmartPhone` can do all three.",
         {"Device.java": """public class Device {
    private String name;

    public Device(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void powerOn() {
        System.out.println(name + " is on.");
    }
}
""", "Phone.java": """public class Phone extends Device {
    public Phone(String name) {
        super(name);
    }

    public void call(String who) {
        System.out.println(getName() + " calls " + who + ".");
    }
}
""", "SmartPhone.java": """public class SmartPhone extends Phone {
    public SmartPhone(String name) {
        super(name);
    }

    public void browse() {
        System.out.println(getName() + " opens the browser.");
    }
}
""", "DeviceTester.java": """public class DeviceTester {
    public static void main(String[] args) {
        SmartPhone pixel = new SmartPhone("Pixel");
        pixel.powerOn();
        pixel.call("Mom");
        pixel.browse();
    }
}
"""}, "DeviceTester", "Pixel is on.\nPixel calls Mom.\nPixel opens the browser.",
         tests={"CheckDevices.java": """public class CheckDevices {
    public static void main(String[] args) {
        Phone flip = new Phone("Flip");
        flip.powerOn();
        flip.call("Sam");
        new SmartPhone("Tab").powerOn();
    }
}
"""}, tests_run="CheckDevices", tests_output="Flip is on.\nFlip calls Sam.\nTab is on.",
         hints=["`SmartPhone extends Phone`, not `Device`. It gets `Device`'s methods through `Phone`.",
                "Each constructor passes the name one level up with `super(name);`."]),
]

SUPER = [
    task("w-bedroom", "A subclass with its own field",
         "Write `Room` (private `name`, `width`, `length`; a constructor; `getName()`; `area()` returns width × length) and `Bedroom extends Room`, which adds a private `beds` field. `Bedroom`'s constructor takes all four values. Its `describe()` prints `<name>: <area> sq m, <beds> beds`.",
         {"Room.java": """public class Room {
    private String name;
    private double width;
    private double length;

    public Room(String name, double width, double length) {
        this.name = name;
        this.width = width;
        this.length = length;
    }

    public String getName() {
        return name;
    }

    public double area() {
        return width * length;
    }
}
""", "Bedroom.java": """public class Bedroom extends Room {
    private int beds;

    public Bedroom(String name, double width, double length, int beds) {
        super(name, width, length);
        this.beds = beds;
    }

    public void describe() {
        System.out.println(getName() + ": " + area() + " sq m, " + beds + " beds");
    }
}
""", "RoomTester.java": """public class RoomTester {
    public static void main(String[] args) {
        Bedroom guest = new Bedroom("Guest room", 3.0, 4.0, 2);
        guest.describe();
    }
}
"""}, "RoomTester", "Guest room: 12.0 sq m, 2 beds",
         tests={"CheckBedroom.java": """public class CheckBedroom {
    public static void main(String[] args) {
        Bedroom b = new Bedroom("Loft", 5.0, 2.5, 1);
        b.describe();
        System.out.println(b.area());
    }
}
"""}, tests_run="CheckBedroom", tests_output="Loft: 12.5 sq m, 1 beds\n12.5",
         hints=["`super(name, width, length);` must be the first line of `Bedroom`'s constructor.",
                "`describe()` can call the inherited `getName()` and `area()`."],
         checks=[{"pattern": r"super\s*\(\s*\w+\s*,\s*\w+\s*,\s*\w+\s*\)", "message": "Pass the three room values up with `super(name, width, length);`."}]),

    task("w-plants", "Constructor order",
         "Write `Plant`, `Tree extends Plant` and `Oak extends Tree`. Each has a no-parameter constructor that prints one line: `Plant ready`, `Tree ready`, `Oak ready`. `new Oak()` should print all three, top of the chain first. Don't write any `super()` calls; let Java insert them.",
         {"Plant.java": """public class Plant {
    public Plant() {
        System.out.println("Plant ready");
    }
}
""", "Tree.java": """public class Tree extends Plant {
    public Tree() {
        System.out.println("Tree ready");
    }
}
""", "Oak.java": """public class Oak extends Tree {
    public Oak() {
        System.out.println("Oak ready");
    }
}
""", "PlantTester.java": """public class PlantTester {
    public static void main(String[] args) {
        new Oak();
    }
}
"""}, "PlantTester", "Plant ready\nTree ready\nOak ready",
         tests={"CheckPlants.java": """public class CheckPlants {
    public static void main(String[] args) {
        new Tree();
        System.out.println("--");
        new Plant();
    }
}
"""}, tests_run="CheckPlants", tests_output="Plant ready\nTree ready\n--\nPlant ready",
         hints=["You only need to print in each constructor. The order comes from Java's automatic `super();`."]),

    task("w-vipticket", "Constructor chaining with getters",
         "Write `Ticket` (private `event` and `price`, a constructor, getters) and `VipTicket extends Ticket`, which adds a private `seat`. Its `summary()` returns text like `Gala, seat A1: $120.0`.",
         {"Ticket.java": """public class Ticket {
    private String event;
    private double price;

    public Ticket(String event, double price) {
        this.event = event;
        this.price = price;
    }

    public String getEvent() {
        return event;
    }

    public double getPrice() {
        return price;
    }
}
""", "VipTicket.java": """public class VipTicket extends Ticket {
    private String seat;

    public VipTicket(String event, double price, String seat) {
        super(event, price);
        this.seat = seat;
    }

    public String getSeat() {
        return seat;
    }

    public String summary() {
        return getEvent() + ", seat " + seat + ": $" + getPrice();
    }
}
""", "TicketTester.java": """public class TicketTester {
    public static void main(String[] args) {
        VipTicket gala = new VipTicket("Gala", 120.0, "A1");
        System.out.println(gala.summary());
        System.out.println(gala.getSeat());
    }
}
"""}, "TicketTester", "Gala, seat A1: $120.0\nA1",
         tests={"CheckTicket.java": """public class CheckTicket {
    public static void main(String[] args) {
        VipTicket t = new VipTicket("Opera", 95.5, "B7");
        System.out.println(t.summary());
        System.out.println(t.getEvent() + " " + t.getPrice());
    }
}
"""}, tests_run="CheckTicket", tests_output="Opera, seat B7: $95.5\nOpera 95.5",
         hints=["`summary()` returns a `String`; the tester prints it."]),
]

OVERRIDE = [
    task("w-instruments", "Override a method",
         "Write `Instrument` (private `name`, a constructor, `play()` prints `<name> plays a note.`), `Guitar` (prints `Guitar strums a chord.`) and `Drum` (prints `Drum goes boom.`). `Guitar` and `Drum` have no-parameter constructors that pass their own name up, and override `play()`.",
         {"Instrument.java": """public class Instrument {
    private String name;

    public Instrument(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void play() {
        System.out.println(name + " plays a note.");
    }
}
""", "Guitar.java": """public class Guitar extends Instrument {
    public Guitar() {
        super("Guitar");
    }

    @Override
    public void play() {
        System.out.println(getName() + " strums a chord.");
    }
}
""", "Drum.java": """public class Drum extends Instrument {
    public Drum() {
        super("Drum");
    }

    @Override
    public void play() {
        System.out.println(getName() + " goes boom.");
    }
}
""", "BandTester.java": """public class BandTester {
    public static void main(String[] args) {
        new Instrument("Kazoo").play();
        new Guitar().play();
        new Drum().play();
    }
}
"""}, "BandTester", "Kazoo plays a note.\nGuitar strums a chord.\nDrum goes boom.",
         tests={"CheckBand.java": """public class CheckBand {
    public static void main(String[] args) {
        new Drum().play();
        System.out.println(new Guitar().getName());
    }
}
"""}, tests_run="CheckBand", tests_output="Drum goes boom.\nGuitar",
         hints=["`Guitar`'s constructor: `super(\"Guitar\");`"],
         checks=[{"pattern": r"@Override", "message": "Mark the overriding methods with `@Override`."}]),

    task("w-manager-tostring", "toString with super.toString()",
         "Write `Employee` (private `name` and `salary`, a constructor, and `toString` returning `Jo earns 52000.0`) and `Manager extends Employee`, which adds a private `teamSize`. `Manager`'s `toString` reuses `Employee`'s and adds ` and manages 6`.",
         {"Employee.java": """public class Employee {
    private String name;
    private double salary;

    public Employee(String name, double salary) {
        this.name = name;
        this.salary = salary;
    }

    @Override
    public String toString() {
        return name + " earns " + salary;
    }
}
""", "Manager.java": """public class Manager extends Employee {
    private int teamSize;

    public Manager(String name, double salary, int teamSize) {
        super(name, salary);
        this.teamSize = teamSize;
    }

    @Override
    public String toString() {
        return super.toString() + " and manages " + teamSize;
    }
}
""", "StaffTester.java": """public class StaffTester {
    public static void main(String[] args) {
        System.out.println(new Employee("Jo", 52000.0));
        System.out.println(new Manager("Kim", 78000.0, 6));
    }
}
"""}, "StaffTester", "Jo earns 52000.0\nKim earns 78000.0 and manages 6",
         tests={"CheckStaff.java": """public class CheckStaff {
    public static void main(String[] args) {
        Employee e = new Manager("Lee", 60000.0, 2);
        System.out.println(e);
    }
}
"""}, tests_run="CheckStaff", tests_output="Lee earns 60000.0 and manages 2",
         hints=["`Manager` can't read `name` or `salary`. `super.toString()` gives it that part ready-made."],
         checks=[{"pattern": r"super\.toString\s*\(\s*\)", "message": "Reuse the parent's text with `super.toString()`."}]),

    task("w-urgent", "Add to the parent's behavior",
         "Write `Message` (private `text`, a constructor, `send()` prints `Sending: <text>`) and `UrgentMessage extends Message`, whose `send()` first prints `URGENT!` and then does everything a normal message does.",
         {"Message.java": """public class Message {
    private String text;

    public Message(String text) {
        this.text = text;
    }

    public void send() {
        System.out.println("Sending: " + text);
    }
}
""", "UrgentMessage.java": """public class UrgentMessage extends Message {
    public UrgentMessage(String text) {
        super(text);
    }

    @Override
    public void send() {
        System.out.println("URGENT!");
        super.send();
    }
}
""", "MessageTester.java": """public class MessageTester {
    public static void main(String[] args) {
        new Message("Lunch at noon").send();
        new UrgentMessage("Fire drill now").send();
    }
}
"""}, "MessageTester", "Sending: Lunch at noon\nURGENT!\nSending: Fire drill now",
         tests={"CheckMessage.java": """public class CheckMessage {
    public static void main(String[] args) {
        Message m = new UrgentMessage("Test");
        m.send();
    }
}
"""}, tests_run="CheckMessage", tests_output="URGENT!\nSending: Test",
         checks=[{"pattern": r"super\.send\s*\(\s*\)", "message": "Call the parent's version with `super.send()`."}]),
]

ABSTRACT = [
    task("w-cars", "Each car starts its own way",
         "Write the exam guide's example from scratch: an abstract `Car` with a private `model`, a constructor, `getModel()` and an abstract `start()`. `ElectricCar` prints `<model> hums silently.` and `GasCar` prints `<model> roars to life.`",
         {"Car.java": """public abstract class Car {
    private String model;

    public Car(String model) {
        this.model = model;
    }

    public String getModel() {
        return model;
    }

    public abstract void start();
}
""", "ElectricCar.java": """public class ElectricCar extends Car {
    public ElectricCar(String model) {
        super(model);
    }

    @Override
    public void start() {
        System.out.println(getModel() + " hums silently.");
    }
}
""", "GasCar.java": """public class GasCar extends Car {
    public GasCar(String model) {
        super(model);
    }

    @Override
    public void start() {
        System.out.println(getModel() + " roars to life.");
    }
}
""", "GarageTester.java": """public class GarageTester {
    public static void main(String[] args) {
        new ElectricCar("Volt").start();
        new GasCar("Mustang").start();
    }
}
"""}, "GarageTester", "Volt hums silently.\nMustang roars to life.",
         tests={"CheckCars.java": """public class CheckCars {
    public static void main(String[] args) {
        Car c = new GasCar("Civic");
        c.start();
        System.out.println(c.getModel());
    }
}
"""}, tests_run="CheckCars", tests_output="Civic roars to life.\nCivic",
         checks=[{"pattern": r"abstract\s+class\s+Car", "message": "Declare `public abstract class Car`."},
                 {"pattern": r"abstract\s+void\s+start\s*\(\s*\)\s*;", "message": "Declare `public abstract void start();` (no body)."}]),

    task("w-beverages", "An ordinary method that uses an abstract one",
         "Write an abstract `Beverage` with a private `name`, an abstract `int brewMinutes()`, and a normal method `describe()` that prints `<name> takes <minutes> minutes.` Write `Tea` (4 minutes) and `Coffee` (6 minutes).",
         {"Beverage.java": """public abstract class Beverage {
    private String name;

    public Beverage(String name) {
        this.name = name;
    }

    public abstract int brewMinutes();

    public void describe() {
        System.out.println(name + " takes " + brewMinutes() + " minutes.");
    }
}
""", "Tea.java": """public class Tea extends Beverage {
    public Tea() {
        super("Tea");
    }

    @Override
    public int brewMinutes() {
        return 4;
    }
}
""", "Coffee.java": """public class Coffee extends Beverage {
    public Coffee() {
        super("Coffee");
    }

    @Override
    public int brewMinutes() {
        return 6;
    }
}
""", "CafeTester.java": """public class CafeTester {
    public static void main(String[] args) {
        new Tea().describe();
        new Coffee().describe();
    }
}
"""}, "CafeTester", "Tea takes 4 minutes.\nCoffee takes 6 minutes.",
         tests={"CheckCafe.java": """public class CheckCafe {
    public static void main(String[] args) {
        Beverage b = new Coffee();
        System.out.println(b.brewMinutes());
        b.describe();
    }
}
"""}, tests_run="CheckCafe", tests_output="6\nCoffee takes 6 minutes.",
         hints=["`describe()` lives in `Beverage` and calls `brewMinutes()`; each subclass supplies the number."]),

    task("w-games", "Two abstract methods",
         "Write an abstract `Game` with two abstract methods, `String name()` and `int players()`, and a normal method `summary()` that returns text like `Chess (players: 2)`. Write `Chess` (2 players) and `Solitaire` (1 player).",
         {"Game.java": """public abstract class Game {
    public abstract String name();

    public abstract int players();

    public String summary() {
        return name() + " (players: " + players() + ")";
    }
}
""", "Chess.java": """public class Chess extends Game {
    @Override
    public String name() {
        return "Chess";
    }

    @Override
    public int players() {
        return 2;
    }
}
""", "Solitaire.java": """public class Solitaire extends Game {
    @Override
    public String name() {
        return "Solitaire";
    }

    @Override
    public int players() {
        return 1;
    }
}
""", "GameTester.java": """public class GameTester {
    public static void main(String[] args) {
        System.out.println(new Chess().summary());
        System.out.println(new Solitaire().summary());
    }
}
"""}, "GameTester", "Chess (players: 2)\nSolitaire (players: 1)",
         tests={"CheckGames.java": """public class CheckGames {
    public static void main(String[] args) {
        Game g = new Solitaire();
        System.out.println(g.name() + " " + g.players());
    }
}
"""}, tests_run="CheckGames", tests_output="Solitaire 1",
         hints=["`Game` has no fields and no constructor, so the subclasses don't need `super(...)`.",
                "A subclass that implements only one of the two abstract methods won't compile. Read that message: it names the missing one."]),
]

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

POLY = [
    task("w-chorus", "One loop, many forms",
         "Write `Animal` (private `name`, `getName()`, `speak()` prints `<name> makes a sound.`) and three subclasses that override `speak()`: `Dog` (`says Woof!`), `Cat` (`says Meow.`) and `Cow` (`says Moo.`). In `ChorusTester`, put one of each in an `Animal[]` and make them all speak in one loop.",
         {"Animal.java": ANIMAL, "Dog.java": """public class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }

    @Override
    public void speak() {
        System.out.println(getName() + " says Woof!");
    }
}
""", "Cat.java": """public class Cat extends Animal {
    public Cat(String name) {
        super(name);
    }

    @Override
    public void speak() {
        System.out.println(getName() + " says Meow.");
    }
}
""", "Cow.java": """public class Cow extends Animal {
    public Cow(String name) {
        super(name);
    }

    @Override
    public void speak() {
        System.out.println(getName() + " says Moo.");
    }
}
""", "ChorusTester.java": """public class ChorusTester {
    public static void main(String[] args) {
        Animal[] chorus = {new Dog("Rex"), new Cat("Tom"), new Cow("Bess")};
        for (Animal a : chorus) {
            a.speak();
        }
    }
}
"""}, "ChorusTester", "Rex says Woof!\nTom says Meow.\nBess says Moo.",
         tests={"CheckChorus.java": """public class CheckChorus {
    public static void main(String[] args) {
        Animal a = new Cow("Daisy");
        a.speak();
        Animal b = new Animal("Plain");
        b.speak();
    }
}
"""}, tests_run="CheckChorus", tests_output="Daisy says Moo.\nPlain makes a sound.",
         checks=[{"pattern": r"Animal\s*\[\s*\]", "message": "Store the animals in an `Animal[]`."}]),

    task("w-purr", "instanceof and a cast",
         "Write `Animal` (as in the previous task), `Dog` and `Cat` (no overrides needed), where only `Cat` has `purr()` (prints `<name> purrs.`). In `CatCount`, loop over `{Dog Rex, Cat Tom, Cat Kit, Dog Fido}`, make each cat purr, and print how many cats there were.",
         {"Animal.java": ANIMAL, "Dog.java": """public class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }
}
""", "Cat.java": """public class Cat extends Animal {
    public Cat(String name) {
        super(name);
    }

    public void purr() {
        System.out.println(getName() + " purrs.");
    }
}
""", "CatCount.java": """public class CatCount {
    public static void main(String[] args) {
        Animal[] animals = {new Dog("Rex"), new Cat("Tom"), new Cat("Kit"), new Dog("Fido")};
        int cats = 0;
        for (Animal a : animals) {
            if (a instanceof Cat) {
                cats++;
                Cat c = (Cat) a;
                c.purr();
            }
        }
        System.out.println(cats + " cats");
    }
}
"""}, "CatCount", "Tom purrs.\nKit purrs.\n2 cats",
         requirements=["Check with `instanceof` before casting"],
         hints=["`if (a instanceof Cat)`, then `Cat c = (Cat) a;`"],
         checks=[{"pattern": r"instanceof\s+Cat", "message": "Use `instanceof Cat` to find the cats."},
                 {"pattern": r"\(\s*Cat\s*\)", "message": "Cast with `(Cat)` before calling `purr()`."}]),

    task("w-showcase", "Everything is an Object",
         "Write `Pet` (private `name`, `toString` returns `<name> the pet`) and `Showcase`, with a method `public static void show(Object item)` that prints `Showing: ` followed by the item. Because every class extends `Object`, `show` accepts a `String`, a `Pet`, or anything else.",
         {"Pet.java": """public class Pet {
    private String name;

    public Pet(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return name + " the pet";
    }
}
""", "Showcase.java": """public class Showcase {
    public static void show(Object item) {
        System.out.println("Showing: " + item);
    }

    public static void main(String[] args) {
        show("hello");
        show(new Pet("Biscuit"));
    }
}
"""}, "Showcase", "Showing: hello\nShowing: Biscuit the pet",
         tests={"CheckShowcase.java": """public class CheckShowcase {
    public static void main(String[] args) {
        Showcase.show(new Pet("Nib"));
        Object o = new Pet("Pip");
        System.out.println(o);
    }
}
"""}, tests_run="CheckShowcase", tests_output="Showing: Nib the pet\nPip the pet",
         hints=["The parameter type is `Object`. Joining it to text with `+` calls its `toString()`, so `Pet`'s version runs."],
         checks=[{"pattern": r"show\s*\(\s*Object\s+\w+\s*\)", "message": "Give `show` a parameter of type `Object`."}]),
]

VEHICLE = """public abstract class Vehicle {
    private String id;

    public Vehicle(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
    }

    public abstract double costFor(int km);

    @Override
    public String toString() {
        return id;
    }
}
"""


def vsub(name, base, per):
    return f"""public class {name} extends Vehicle {{
    public {name}(String id) {{
        super(id);
    }}

    @Override
    public double costFor(int km) {{
        return {base} + {per} * km;
    }}
}}
"""


FLEET = """public class Fleet {
    private Vehicle[] vehicles;

    public Fleet(int size) {
        vehicles = new Vehicle[size];
    }

    public boolean add(Vehicle v) {
        for (int i = 0; i < vehicles.length; i++) {
            if (vehicles[i] == null) {
                vehicles[i] = v;
                return true;
            }
        }
        return false;
    }

    public void quote(int km) {
        for (Vehicle v : vehicles) {
            if (v != null) {
                System.out.println(v + ": $" + v.costFor(km));
            }
        }
    }

    public Vehicle cheapestFor(int km) {
        Vehicle best = null;
        for (Vehicle v : vehicles) {
            if (v != null && (best == null || v.costFor(km) < best.costFor(km))) {
                best = v;
            }
        }
        return best;
    }
}
"""

PROJECT = [
    task("w-fleet-rebuild", "Rebuild the fleet from the spec",
         "Without looking back, write the whole delivery-fleet project from its specification: abstract `Vehicle`, `Bike`, `Van`, `Drone` and `Fleet` (with `add`, `quote` and `cheapestFor`). Use this tester's output as your target.",
         {"Vehicle.java": VEHICLE, "Bike.java": vsub("Bike", 2, 0.5), "Van.java": vsub("Van", 10, 1.5),
          "Drone.java": vsub("Drone", 8, 0.25), "Fleet.java": FLEET, "FleetTester.java": """public class FleetTester {
    public static void main(String[] args) {
        Fleet fleet = new Fleet(3);
        fleet.add(new Bike("B1"));
        fleet.add(new Van("V1"));
        fleet.add(new Drone("D1"));
        fleet.quote(10);
        System.out.println("Cheapest for 2 km: " + fleet.cheapestFor(2));
        System.out.println("Cheapest for 30 km: " + fleet.cheapestFor(30));
    }
}
"""}, "FleetTester", "B1: $7.0\nV1: $25.0\nD1: $10.5\nCheapest for 2 km: B1\nCheapest for 30 km: D1",
         tests={"CheckFleet.java": """public class CheckFleet {
    public static void main(String[] args) {
        Fleet f = new Fleet(2);
        System.out.println(f.cheapestFor(5));
        System.out.println(f.add(new Van("V9")));
        System.out.println(f.add(new Van("V8")));
        System.out.println(f.add(new Bike("B9")));
        Vehicle d = new Drone("D9");
        System.out.println(d.costFor(4));
    }
}
"""}, tests_run="CheckFleet", tests_output="null\ntrue\ntrue\nfalse\n9.0",
         requirements=["Six files; follow the specification at the top of this page"],
         hints=["Start with `Vehicle` and one subclass, and run the tester with only the lines that work so far."]),

    task("w-tickets", "Same design, new subject",
         "Write an abstract `Ticket` (private `holder`, `getHolder()`, abstract `double price()`, and `toString` returning `<holder>: $<price>`). `AdultTicket` costs 12.0, `ChildTicket` 6.0 and `SeniorTicket` 8.0. `Order` keeps a private `Ticket[]` and has `add(Ticket)` (returns `false` when full) and `total()`.",
         {"Ticket.java": """public abstract class Ticket {
    private String holder;

    public Ticket(String holder) {
        this.holder = holder;
    }

    public String getHolder() {
        return holder;
    }

    public abstract double price();

    @Override
    public String toString() {
        return holder + ": $" + price();
    }
}
""", "AdultTicket.java": """public class AdultTicket extends Ticket {
    public AdultTicket(String holder) {
        super(holder);
    }

    @Override
    public double price() {
        return 12.0;
    }
}
""", "ChildTicket.java": """public class ChildTicket extends Ticket {
    public ChildTicket(String holder) {
        super(holder);
    }

    @Override
    public double price() {
        return 6.0;
    }
}
""", "SeniorTicket.java": """public class SeniorTicket extends Ticket {
    public SeniorTicket(String holder) {
        super(holder);
    }

    @Override
    public double price() {
        return 8.0;
    }
}
""", "Order.java": """public class Order {
    private Ticket[] tickets;

    public Order(int size) {
        tickets = new Ticket[size];
    }

    public boolean add(Ticket t) {
        for (int i = 0; i < tickets.length; i++) {
            if (tickets[i] == null) {
                tickets[i] = t;
                return true;
            }
        }
        return false;
    }

    public double total() {
        double sum = 0;
        for (Ticket t : tickets) {
            if (t != null) {
                sum = sum + t.price();
            }
        }
        return sum;
    }
}
""", "OrderTester.java": """public class OrderTester {
    public static void main(String[] args) {
        Order family = new Order(3);
        Ticket mom = new AdultTicket("Mom");
        family.add(mom);
        family.add(new ChildTicket("Leo"));
        family.add(new SeniorTicket("Gran"));
        System.out.println(family.add(new ChildTicket("Extra")));
        System.out.println(mom);
        System.out.println("Total: $" + family.total());
    }
}
"""}, "OrderTester", "false\nMom: $12.0\nTotal: $26.0",
         tests={"CheckOrder.java": """public class CheckOrder {
    public static void main(String[] args) {
        Order o = new Order(2);
        System.out.println(o.total());
        o.add(new SeniorTicket("Al"));
        System.out.println(o.total());
        System.out.println(new ChildTicket("Mo"));
    }
}
"""}, tests_run="CheckOrder", tests_output="0.0\n8.0\nMo: $6.0",
         hints=["This is the fleet with different names: `Ticket` is `Vehicle`, `price()` is `costFor`, `Order` is `Fleet`."]),
]

TASKS = {
    "inh-extends": EXT,
    "inh-super": SUPER,
    "inh-override": OVERRIDE,
    "inh-abstract": ABSTRACT,
    "inh-polymorphism": POLY,
    "inh-project-fleet": PROJECT,
}
