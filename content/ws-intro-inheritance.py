from sources import SUBCLASSES_TUT, SUPER_TUT, JLS_CTOR_BODY, HEL_9_1
from wshelp import step, guided, workshop, task

EXT = lambda sub, sup: {"pattern": r"class\s+" + sub + r"\s+extends\s+" + sup, "message": f"Declare `{sub} extends {sup}`."}

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

    public void introduce() {
        System.out.println("Hi, I'm " + name + ", " + age + ".");
    }
}
"""
TEACHER = """public class Teacher extends Person {
    private String subject;

    public Teacher(String name, int age, String subject) {
        super(name, age);
        this.subject = subject;
    }

    public String getSubject() {
        return subject;
    }

    public void teach() {
        System.out.println(getName() + " teaches " + subject + ".");
    }
}
"""
HEAD = """public class HeadTeacher extends Teacher {
    private String school;

    public HeadTeacher(String name, int age, String subject, String school) {
        super(name, age, subject);
        this.school = school;
    }

    public void announce() {
        System.out.println(getName() + " leads " + school + ".");
    }
}
"""
ST1 = """public class SchoolTester {
    public static void main(String[] args) {
        new Person("Ana", 30).introduce();
    }
}
"""
ST2 = """public class SchoolTester {
    public static void main(String[] args) {
        Teacher raj = new Teacher("Raj", 41, "math");
        raj.introduce();
        raj.teach();
    }
}
"""
ST3 = """public class SchoolTester {
    public static void main(String[] args) {
        HeadTeacher kim = new HeadTeacher("Kim", 52, "history", "Elm School");
        kim.introduce();
        kim.teach();
        kim.announce();
    }
}
"""

CARD = """public class Card {
    private String holder;

    public Card(String holder) {
        this.holder = holder;
    }

    public String getHolder() {
        return holder;
    }
}
"""
CREDIT = """public class CreditCard extends Card {
    private double limit;
    private double balance;

    public CreditCard(String holder, double limit) {
        super(holder);
        this.limit = limit;
        balance = 0;
    }

    public double getBalance() {
        return balance;
    }

    public boolean charge(double amount) {
        if (amount > 0 && balance + amount <= limit) {
            balance = balance + amount;
            return true;
        }
        return false;
    }
}
"""
GIFT = """public class GiftCard extends Card {
    private double value;

    public GiftCard(String holder, double value) {
        super(holder);
        this.value = value;
    }

    public double getValue() {
        return value;
    }

    public boolean spend(double amount) {
        if (amount > 0 && amount <= value) {
            value = value - amount;
            return true;
        }
        return false;
    }
}
"""
WT1 = """public class WalletTester {
    public static void main(String[] args) {
        Card c = new Card("Ana");
        System.out.println(c.getHolder());
    }
}
"""
WT2 = """public class WalletTester {
    public static void main(String[] args) {
        CreditCard visa = new CreditCard("Ana", 100.0);
        System.out.println(visa.charge(60.0));
        System.out.println(visa.charge(50.0));
        System.out.println(visa.getHolder() + " owes $" + visa.getBalance());
    }
}
"""
WT3 = """public class WalletTester {
    public static void main(String[] args) {
        CreditCard visa = new CreditCard("Ana", 100.0);
        System.out.println(visa.charge(60.0));
        System.out.println(visa.charge(50.0));
        System.out.println(visa.getHolder() + " owes $" + visa.getBalance());

        GiftCard gift = new GiftCard("Sam", 25.0);
        System.out.println(gift.spend(30.0));
        System.out.println(gift.spend(25.0));
        System.out.println(gift.getHolder() + " has $" + gift.getValue() + " left");
    }
}
"""

LESSON = workshop(
    "ws-intro-inheritance", "Workshop: introduction to inheritance",
    "Practice writing superclasses and subclasses with `extends`, passing values up with `super(...)`, and keeping each class's fields private.",
    ["Write a superclass and subclasses from an empty editor",
     "Build a three-level chain where each constructor calls `super(...)`",
     "Give two subclasses of the same parent different abilities"],
    guided("ws-u7-school", "People at a school", "Build a three-level chain: `Person`, `Teacher`, `HeadTeacher`.", [
        step("Person", "Create `Person.java` with private `name` and `age`, a constructor, getters, and `introduce()`, which prints `Hi, I'm <name>, <age>.`",
             {"Person.java": PERSON, "SchoolTester.java": ST1}, "SchoolTester", "Hi, I'm Ana, 30."),
        step("Teacher", "Create `Teacher extends Person` with a private `subject`. Its constructor takes name, age and subject and passes the first two up with `super`. Add `teach()`, which prints `<name> teaches <subject>.`",
             {"Person.java": PERSON, "Teacher.java": TEACHER, "SchoolTester.java": ST2}, "SchoolTester",
             "Hi, I'm Raj, 41.\nRaj teaches math.", checks=[EXT("Teacher", "Person")]),
        step("HeadTeacher", "Create `HeadTeacher extends Teacher` with a private `school`, and `announce()`, which prints `<name> leads <school>.` A head teacher can introduce themselves, teach and announce.",
             {"Person.java": PERSON, "Teacher.java": TEACHER, "HeadTeacher.java": HEAD, "SchoolTester.java": ST3}, "SchoolTester",
             "Hi, I'm Kim, 52.\nKim teaches history.\nKim leads Elm School.",
             hint="`super(name, age, subject);` goes to `Teacher`'s constructor, which passes name and age on to `Person`.",
             checks=[EXT("HeadTeacher", "Teacher")]),
    ]),
    guided("ws-u7-cards", "Cards in a wallet", "Build a `Card` superclass and two subclasses with different rules for spending.", [
        step("Card", "Create `Card.java` with a private `holder`, a constructor and `getHolder()`.",
             {"Card.java": CARD, "WalletTester.java": WT1}, "WalletTester", "Ana"),
        step("CreditCard", "Create `CreditCard extends Card` with a private limit and a balance that starts at 0. `charge(double amount)` adds to the balance and returns `true` only if the new balance stays within the limit.",
             {"Card.java": CARD, "CreditCard.java": CREDIT, "WalletTester.java": WT2}, "WalletTester",
             "true\nfalse\nAna owes $60.0", checks=[EXT("CreditCard", "Card")]),
        step("GiftCard", "Create `GiftCard extends Card` with a private value. `spend(double amount)` takes money off and returns `true` only if there's enough. Spending the exact value is allowed.",
             {"Card.java": CARD, "CreditCard.java": CREDIT, "GiftCard.java": GIFT, "WalletTester.java": WT3}, "WalletTester",
             "true\nfalse\nAna owes $60.0\nfalse\ntrue\nSam has $0.0 left", checks=[EXT("GiftCard", "Card")]),
    ]),
    task("ws-u7-buildings", "Two kinds of building",
         "Write `Building` (private `address`, constructor, `getAddress()`), `House extends Building` (private `bedrooms`; `describe()` prints `<address>: house with <n> bedrooms`) and `Office extends Building` (private `floors`; `describe()` prints `<address>: office with <n> floors`).",
         {"Building.java": """public class Building {
    private String address;

    public Building(String address) {
        this.address = address;
    }

    public String getAddress() {
        return address;
    }
}
""", "House.java": """public class House extends Building {
    private int bedrooms;

    public House(String address, int bedrooms) {
        super(address);
        this.bedrooms = bedrooms;
    }

    public void describe() {
        System.out.println(getAddress() + ": house with " + bedrooms + " bedrooms");
    }
}
""", "Office.java": """public class Office extends Building {
    private int floors;

    public Office(String address, int floors) {
        super(address);
        this.floors = floors;
    }

    public void describe() {
        System.out.println(getAddress() + ": office with " + floors + " floors");
    }
}
""", "StreetTester.java": """public class StreetTester {
    public static void main(String[] args) {
        new House("12 Oak St", 3).describe();
        new Office("1 Main St", 5).describe();
    }
}
"""}, "StreetTester", "12 Oak St: house with 3 bedrooms\n1 Main St: office with 5 floors",
         tests={"CheckStreet.java": """public class CheckStreet {
    public static void main(String[] args) {
        House h = new House("9 Pine Rd", 1);
        h.describe();
        System.out.println(h.getAddress());
    }
}
"""}, tests_run="CheckStreet", tests_output="9 Pine Rd: house with 1 bedrooms\n9 Pine Rd",
         checks=[EXT("House", "Building"), EXT("Office", "Building")]),
    task("ws-u7-contacts", "A work contact",
         "Write `Contact` (private `name` and `phone`, constructor, getters) and `WorkContact extends Contact`, which adds a private `company` and a method `card()` that returns `<name>, <company>, <phone>`.",
         {"Contact.java": """public class Contact {
    private String name;
    private String phone;

    public Contact(String name, String phone) {
        this.name = name;
        this.phone = phone;
    }

    public String getName() {
        return name;
    }

    public String getPhone() {
        return phone;
    }
}
""", "WorkContact.java": """public class WorkContact extends Contact {
    private String company;

    public WorkContact(String name, String phone, String company) {
        super(name, phone);
        this.company = company;
    }

    public String card() {
        return getName() + ", " + company + ", " + getPhone();
    }
}
""", "ContactTester.java": """public class ContactTester {
    public static void main(String[] args) {
        WorkContact ana = new WorkContact("Ana Ruiz", "555-0100", "Acme");
        System.out.println(ana.card());
    }
}
"""}, "ContactTester", "Ana Ruiz, Acme, 555-0100",
         tests={"CheckContact.java": """public class CheckContact {
    public static void main(String[] args) {
        WorkContact w = new WorkContact("Lee", "555-0199", "Globex");
        System.out.println(w.card());
        System.out.println(w.getPhone());
    }
}
"""}, tests_run="CheckContact", tests_output="Lee, Globex, 555-0199\n555-0199",
         checks=[EXT("WorkContact", "Contact"),
                 {"pattern": r"super\s*\(\s*\w+\s*,\s*\w+\s*\)", "message": "Pass the name and phone up with `super(name, phone);`."}]),
    [SUBCLASSES_TUT, SUPER_TUT, JLS_CTOR_BODY, HEL_9_1],
)
