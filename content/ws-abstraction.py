from sources import ABSTRACT_TUT, JLS_ABSTRACT, POLY_TUT, HEL_9_1
from wshelp import step, guided, workshop, task

ABS = lambda cls: {"pattern": r"abstract\s+class\s+" + cls, "message": f"Declare `{cls}` as `abstract`."}

PAY = """public abstract class Payment {
    private double amount;

    public Payment(double amount) {
        this.amount = amount;
    }

    public double getAmount() {
        return amount;
    }

    public abstract double fee();

    public double total() {
        return amount + fee();
    }
}
"""
CARDPAY = """public class CardPayment extends Payment {
    public CardPayment(double amount) {
        super(amount);
    }

    @Override
    public double fee() {
        return getAmount() * 0.02;
    }
}
"""
CASHPAY = """public class CashPayment extends Payment {
    public CashPayment(double amount) {
        super(amount);
    }

    @Override
    public double fee() {
        return 0;
    }
}
"""
PYT1 = """public class PayTester {
    public static void main(String[] args) {
        CardPayment p = new CardPayment(100.0);
        System.out.println("Fee: " + p.fee());
        System.out.println("Total: " + p.total());
    }
}
"""
PYT2 = """public class PayTester {
    public static void main(String[] args) {
        Payment[] payments = {new CardPayment(100.0), new CashPayment(40.0), new CardPayment(50.0)};
        for (Payment p : payments) {
            System.out.println(p.getAmount() + " -> " + p.total());
        }
    }
}
"""
PYT3 = """public class PayTester {
    public static void main(String[] args) {
        Payment[] payments = {new CardPayment(100.0), new CashPayment(40.0), new CardPayment(50.0)};
        double fees = 0;
        double charged = 0;
        for (Payment p : payments) {
            fees = fees + p.fee();
            charged = charged + p.total();
        }
        System.out.println("Fees: " + fees);
        System.out.println("Charged: " + charged);
    }
}
"""

HERO = """public abstract class Hero {
    private String name;
    private int health;

    public Hero(String name, int health) {
        this.name = name;
        this.health = health;
    }

    public String getName() {
        return name;
    }

    public int getHealth() {
        return health;
    }

    public abstract int attackPower();

    public void takeDamage(int amount) {
        health = health - amount;
        if (health < 0) {
            health = 0;
        }
    }

    public boolean isAlive() {
        return health > 0;
    }
}
"""
ATTACK = """
    public void attack(Hero target) {
        target.takeDamage(attackPower());
        System.out.println(getName() + " hits " + target.getName() + " for " + attackPower() + ".");
    }
"""
HERO3 = HERO[:-2] + ATTACK + "}\n"
WARRIOR = """public class Warrior extends Hero {
    public Warrior(String name) {
        super(name, 30);
    }

    @Override
    public int attackPower() {
        return 10;
    }
}
"""
MAGE = """public class Mage extends Hero {
    public Mage(String name) {
        super(name, 20);
    }

    @Override
    public int attackPower() {
        return 7;
    }
}
"""
AT1 = """public class ArenaTester {
    public static void main(String[] args) {
        Warrior w = new Warrior("Brin");
        w.takeDamage(12);
        System.out.println(w.getName() + ": " + w.getHealth() + " health, power " + w.attackPower());
        w.takeDamage(50);
        System.out.println(w.getHealth() + " " + w.isAlive());
    }
}
"""
AT2 = """public class ArenaTester {
    public static void main(String[] args) {
        Hero[] party = {new Warrior("Brin"), new Mage("Ivy")};
        for (Hero h : party) {
            System.out.println(h.getName() + ": " + h.getHealth() + " health, power " + h.attackPower());
        }
    }
}
"""
AT3 = """public class ArenaTester {
    public static void main(String[] args) {
        Hero brin = new Warrior("Brin");
        Hero ivy = new Mage("Ivy");
        brin.attack(ivy);
        ivy.attack(brin);
        brin.attack(ivy);
        System.out.println(ivy.getName() + " alive: " + ivy.isAlive());
        System.out.println(brin.getName() + " health: " + brin.getHealth());
    }
}
"""

LESSON = workshop(
    "ws-abstraction", "Workshop: abstraction",
    "Practice abstract classes: concrete methods that rely on abstract ones, and subclasses that each fill in the missing piece.",
    ["Write abstract classes with both abstract and normal methods",
     "Implement abstract methods in several subclasses",
     "Call an abstract method from a normal method in the superclass"],
    guided("ws-u10-pay", "Payments with fees", "Build an abstract `Payment` whose `total()` works for every kind of payment.", [
        step("Payment and CardPayment", "Create an abstract `Payment` with a private `amount`, `getAmount()`, an abstract `double fee()`, and a normal method `total()` that returns amount + fee. Create `CardPayment`, whose fee is 2% of the amount.",
             {"Payment.java": PAY, "CardPayment.java": CARDPAY, "PayTester.java": PYT1}, "PayTester", "Fee: 2.0\nTotal: 102.0",
             hint="`total()` calls `fee()` without knowing which subclass will supply it.",
             checks=[ABS("Payment"), {"pattern": r"abstract\s+double\s+fee\s*\(\s*\)\s*;", "message": "Declare `public abstract double fee();`"}]),
        step("Cash", "Create `CashPayment`, which has no fee. Loop over a `Payment[]` with two card payments and one cash payment and print each amount and total.",
             {"Payment.java": PAY, "CardPayment.java": CARDPAY, "CashPayment.java": CASHPAY, "PayTester.java": PYT2}, "PayTester",
             "100.0 -> 102.0\n40.0 -> 40.0\n50.0 -> 51.0"),
        step("Totals", "Change the tester to add up all the fees and everything charged, and print both.",
             {"Payment.java": PAY, "CardPayment.java": CARDPAY, "CashPayment.java": CASHPAY, "PayTester.java": PYT3}, "PayTester",
             "Fees: 3.0\nCharged: 193.0"),
    ]),
    guided("ws-u10-arena", "Heroes in an arena", "Build an abstract `Hero` whose `attack` works for every kind of hero.", [
        step("Hero and Warrior", "Create an abstract `Hero` with private `name` and `health`, getters, an abstract `int attackPower()`, `takeDamage(int)` (health never below 0) and `isAlive()`. Create `Warrior`: 30 health, attack power 10.",
             {"Hero.java": HERO, "Warrior.java": WARRIOR, "ArenaTester.java": AT1}, "ArenaTester",
             "Brin: 18 health, power 10\n0 false",
             hint="`Warrior`'s constructor takes just the name: `super(name, 30);`",
             checks=[ABS("Hero")]),
        step("Mage", "Create `Mage`: 20 health, attack power 7. Print both heroes from a `Hero[]`.",
             {"Hero.java": HERO, "Warrior.java": WARRIOR, "Mage.java": MAGE, "ArenaTester.java": AT2}, "ArenaTester",
             "Brin: 30 health, power 10\nIvy: 20 health, power 7"),
        step("Attacking", "Add a normal method `attack(Hero target)` to `Hero`. It damages the target by this hero's attack power and prints `<name> hits <target> for <power>.`",
             {"Hero.java": HERO3, "Warrior.java": WARRIOR, "Mage.java": MAGE, "ArenaTester.java": AT3}, "ArenaTester",
             "Brin hits Ivy for 10.\nIvy hits Brin for 7.\nBrin hits Ivy for 10.\nIvy alive: false\nBrin health: 23",
             hint="`target.takeDamage(attackPower());` The abstract method decides how hard each kind of hero hits."),
    ]),
    task("ws-u10-plans", "Subscription plans",
         "Write an abstract `Plan` (private `name`, abstract `double monthlyCost()`, and `describe()` printing `<name>: $<cost> per month`). `BasicPlan` costs 8.0. `FamilyPlan` takes a number of members and costs 12.0 plus 2.0 per member.",
         {"Plan.java": """public abstract class Plan {
    private String name;

    public Plan(String name) {
        this.name = name;
    }

    public abstract double monthlyCost();

    public void describe() {
        System.out.println(name + ": $" + monthlyCost() + " per month");
    }
}
""", "BasicPlan.java": """public class BasicPlan extends Plan {
    public BasicPlan() {
        super("Basic");
    }

    @Override
    public double monthlyCost() {
        return 8.0;
    }
}
""", "FamilyPlan.java": """public class FamilyPlan extends Plan {
    private int members;

    public FamilyPlan(int members) {
        super("Family");
        this.members = members;
    }

    @Override
    public double monthlyCost() {
        return 12.0 + 2.0 * members;
    }
}
""", "PlanTester.java": """public class PlanTester {
    public static void main(String[] args) {
        new BasicPlan().describe();
        new FamilyPlan(4).describe();
    }
}
"""}, "PlanTester", "Basic: $8.0 per month\nFamily: $20.0 per month",
         tests={"CheckPlans.java": """public class CheckPlans {
    public static void main(String[] args) {
        Plan p = new FamilyPlan(0);
        System.out.println(p.monthlyCost());
        p = new FamilyPlan(1);
        p.describe();
    }
}
"""}, tests_run="CheckPlans", tests_output="12.0\nFamily: $14.0 per month",
         checks=[ABS("Plan")]),
    task("ws-u10-animals", "Abstract animals (exam-sized)",
         "Write an abstract `Animal` (private `name`, abstract `String sound()`, and `speak()`, which prints `<name> says <sound>`), plus `Dog` (`Woof`) and `Cat` (`Meow`). About 25 lines in all. Try it on paper first.",
         {"Animal.java": """public abstract class Animal {
    private String name;

    public Animal(String name) {
        this.name = name;
    }

    public abstract String sound();

    public void speak() {
        System.out.println(name + " says " + sound());
    }
}
""", "Dog.java": """public class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }

    @Override
    public String sound() {
        return "Woof";
    }
}
""", "Cat.java": """public class Cat extends Animal {
    public Cat(String name) {
        super(name);
    }

    @Override
    public String sound() {
        return "Meow";
    }
}
""", "AnimalTester.java": """public class AnimalTester {
    public static void main(String[] args) {
        Animal[] pets = {new Dog("Rex"), new Cat("Tom")};
        for (Animal a : pets) {
            a.speak();
        }
    }
}
"""}, "AnimalTester", "Rex says Woof\nTom says Meow",
         tests={"CheckAnimals.java": """public class CheckAnimals {
    public static void main(String[] args) {
        Animal a = new Cat("Kit");
        System.out.println(a.sound());
        a.speak();
    }
}
"""}, tests_run="CheckAnimals", tests_output="Meow\nKit says Meow",
         checks=[ABS("Animal"), {"pattern": r"abstract\s+String\s+sound\s*\(\s*\)\s*;", "message": "Declare `public abstract String sound();`"}]),
    [ABSTRACT_TUT, JLS_ABSTRACT, POLY_TUT, HEL_9_1],
)
