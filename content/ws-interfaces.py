from sources import IFACE_TUT, IFACE_TYPE_TUT, COMPARABLE_API, ARRAYS_API, HEL_9_2
from wshelp import step, guided, workshop, task

SW = """public interface Switchable {
    void turnOn();

    boolean isOn();
}
"""
DIM = """public interface Dimmable {
    void setLevel(int percent);
}
"""
LAMP1 = """public class Lamp implements Switchable {
    private String room;
    private boolean on;

    public Lamp(String room) {
        this.room = room;
    }

    @Override
    public void turnOn() {
        on = true;
        System.out.println(room + " lamp on");
    }

    @Override
    public boolean isOn() {
        return on;
    }
}
"""
LAMP2 = LAMP1.replace("public class Lamp implements Switchable {", "public class Lamp implements Switchable, Dimmable {").replace("""    @Override
    public boolean isOn() {
        return on;
    }
}
""", """    @Override
    public boolean isOn() {
        return on;
    }

    @Override
    public void setLevel(int percent) {
        System.out.println(room + " lamp at " + percent + "%");
    }
}
""")
FAN = """public class Fan implements Switchable {
    private boolean on;

    @Override
    public void turnOn() {
        on = true;
        System.out.println("Fan spinning");
    }

    @Override
    public boolean isOn() {
        return on;
    }
}
"""
HT1 = """public class HomeTester {
    public static void main(String[] args) {
        Lamp desk = new Lamp("Office");
        System.out.println(desk.isOn());
        desk.turnOn();
        System.out.println(desk.isOn());
    }
}
"""
HT2 = """public class HomeTester {
    public static void main(String[] args) {
        Lamp desk = new Lamp("Office");
        desk.turnOn();
        desk.setLevel(40);
    }
}
"""
HT3 = """public class HomeTester {
    public static void main(String[] args) {
        Switchable[] devices = {new Lamp("Office"), new Fan(), new Lamp("Hall")};
        for (Switchable s : devices) {
            s.turnOn();
        }
    }
}
"""
HT4 = """public class HomeTester {
    public static void main(String[] args) {
        Switchable[] devices = {new Lamp("Office"), new Fan(), new Lamp("Hall")};
        for (Switchable s : devices) {
            s.turnOn();
            if (s instanceof Dimmable) {
                ((Dimmable) s).setLevel(30);
            }
        }
    }
}
"""

PLAYER = """public class Player implements Comparable<Player> {
    private String name;
    private int score;

    public Player(String name, int score) {
        this.name = name;
        this.score = score;
    }

    public String getName() {
        return name;
    }

    @Override
    public int compareTo(Player other) {
        return Integer.compare(other.score, score);
    }

    @Override
    public String toString() {
        return name + " (" + score + ")";
    }
}
"""
LT1 = """public class Leaderboard {
    public static void main(String[] args) {
        Player ana = new Player("Ana", 120);
        Player sam = new Player("Sam", 340);
        System.out.println(sam.compareTo(ana) < 0);
        System.out.println(ana);
    }
}
"""
LT2 = """import java.util.Arrays;

public class Leaderboard {
    public static void main(String[] args) {
        Player[] players = {new Player("Ana", 120), new Player("Sam", 340), new Player("Lee", 95), new Player("Kim", 210)};
        Arrays.sort(players);
        for (int i = 0; i < players.length; i++) {
            System.out.println((i + 1) + ". " + players[i]);
        }
    }
}
"""
LT3 = """import java.util.Arrays;

public class Leaderboard {
    public static void main(String[] args) {
        Player[] players = {new Player("Ana", 120), new Player("Sam", 340), new Player("Lee", 95), new Player("Kim", 210)};
        Arrays.sort(players);
        for (int i = 0; i < 3; i++) {
            System.out.println((i + 1) + ". " + players[i]);
        }
        System.out.println("Last place: " + players[players.length - 1].getName());
    }
}
"""

LESSON = workshop(
    "ws-interfaces", "Workshop: interfaces",
    "Practice declaring interfaces, implementing several at once, using interface types for mixed arrays, and sorting with `Comparable`.",
    ["Write interfaces and classes that implement them from an empty editor",
     "Use an interface type for an array of unrelated objects",
     "Make your own class sortable with `Comparable`"],
    guided("ws-u9-home", "Smart home devices", "Build devices that share one interface, and a lamp that also has a second ability.", [
        step("Switchable and Lamp", "Create the interface `Switchable` with `void turnOn()` and `boolean isOn()`. Create `Lamp` (private `room` and `on`) that implements it; turning on prints `<room> lamp on`.",
             {"Switchable.java": SW, "Lamp.java": LAMP1, "HomeTester.java": HT1}, "HomeTester",
             "false\nOffice lamp on\ntrue",
             checks=[{"pattern": r"interface\s+Switchable", "message": "Declare `Switchable` as an `interface`."}]),
        step("A second interface", "Create the interface `Dimmable` with `void setLevel(int percent)`. Make `Lamp` implement both interfaces; `setLevel` prints `<room> lamp at <percent>%`.",
             {"Switchable.java": SW, "Dimmable.java": DIM, "Lamp.java": LAMP2, "HomeTester.java": HT2}, "HomeTester",
             "Office lamp on\nOffice lamp at 40%",
             checks=[{"pattern": r"implements\s+Switchable\s*,\s*Dimmable|implements\s+Dimmable\s*,\s*Switchable", "message": "Make `Lamp` implement both: `implements Switchable, Dimmable`."}]),
        step("A fan", "Create `Fan`, which is `Switchable` but not `Dimmable`; turning it on prints `Fan spinning`. Put two lamps and a fan in one `Switchable[]` and turn them all on.",
             {"Switchable.java": SW, "Dimmable.java": DIM, "Lamp.java": LAMP2, "Fan.java": FAN, "HomeTester.java": HT3}, "HomeTester",
             "Office lamp on\nFan spinning\nHall lamp on"),
        step("Dim what can be dimmed", "In the same loop, dim every device that is `Dimmable` to 30%. Check with `instanceof`, then cast.",
             {"Switchable.java": SW, "Dimmable.java": DIM, "Lamp.java": LAMP2, "Fan.java": FAN, "HomeTester.java": HT4}, "HomeTester",
             "Office lamp on\nOffice lamp at 30%\nFan spinning\nHall lamp on\nHall lamp at 30%",
             hint="`((Dimmable) s).setLevel(30);` The extra parentheses cast first, then call.",
             checks=[{"pattern": r"instanceof\s+Dimmable", "message": "Check with `instanceof Dimmable`."}]),
    ]),
    guided("ws-u9-board", "A leaderboard", "Make players sortable from the highest score down, then print a ranked table.", [
        step("Comparable players", "Create `Player` (private `name` and `score`, `getName()`, `toString` like `Ana (120)`) that implements `Comparable<Player>` so **higher** scores come first.",
             {"Player.java": PLAYER, "Leaderboard.java": LT1}, "Leaderboard", "true\nAna (120)",
             hint="`return Integer.compare(other.score, score);` puts the other score first to reverse the order."),
        step("Ranked list", "Sort four players with `Arrays.sort` and print them numbered from 1.",
             {"Player.java": PLAYER, "Leaderboard.java": LT2}, "Leaderboard",
             "1. Sam (340)\n2. Kim (210)\n3. Ana (120)\n4. Lee (95)"),
        step("Top three and last place", "Print only the top three, then the name of whoever came last.",
             {"Player.java": PLAYER, "Leaderboard.java": LT3}, "Leaderboard",
             "1. Sam (340)\n2. Kim (210)\n3. Ana (120)\nLast place: Lee",
             hint="The last item of an array is at index `length - 1`."),
    ]),
    task("ws-u9-areas", "Shapes through an interface",
         "Write an interface `HasArea` (`double area()`) and two classes that implement it: `Rectangle` (width × height) and `RightTriangle` (base × height ÷ 2). In `AreaTester`, write `public static double totalArea(HasArea[] shapes)` and print the total for one of each.",
         {"HasArea.java": """public interface HasArea {
    double area();
}
""", "Rectangle.java": """public class Rectangle implements HasArea {
    private double width;
    private double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }
}
""", "RightTriangle.java": """public class RightTriangle implements HasArea {
    private double base;
    private double height;

    public RightTriangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    @Override
    public double area() {
        return base * height / 2;
    }
}
""", "AreaTester.java": """public class AreaTester {
    public static double totalArea(HasArea[] shapes) {
        double total = 0;
        for (HasArea s : shapes) {
            total = total + s.area();
        }
        return total;
    }

    public static void main(String[] args) {
        HasArea[] shapes = {new Rectangle(3, 4), new RightTriangle(6, 5)};
        System.out.println("Total area: " + totalArea(shapes));
    }
}
"""}, "AreaTester", "Total area: 27.0",
         tests={"CheckAreas.java": """public class CheckAreas {
    public static void main(String[] args) {
        HasArea t = new RightTriangle(3, 3);
        System.out.println(t.area());
        HasArea[] two = {new Rectangle(1, 1), new Rectangle(2, 2)};
        System.out.println(AreaTester.totalArea(two));
    }
}
"""}, tests_run="CheckAreas", tests_output="4.5\n5.0",
         checks=[{"pattern": r"interface\s+HasArea", "message": "Declare `HasArea` as an `interface`."}]),
    task("ws-u9-office", "One machine, two promises (exam-sized)",
         "Write interfaces `Printer` (`void print(String doc)`) and `Faxer` (`void fax(String doc, String number)`), and an `OfficeMachine` with a private `pagesPrinted` count that implements both. `print` prints `Printing <doc>` and counts a page; `fax` prints `Faxing <doc> to <number>`. Add `getPagesPrinted()`.",
         {"Printer.java": """public interface Printer {
    void print(String doc);
}
""", "Faxer.java": """public interface Faxer {
    void fax(String doc, String number);
}
""", "OfficeMachine.java": """public class OfficeMachine implements Printer, Faxer {
    private int pagesPrinted;

    public int getPagesPrinted() {
        return pagesPrinted;
    }

    @Override
    public void print(String doc) {
        System.out.println("Printing " + doc);
        pagesPrinted++;
    }

    @Override
    public void fax(String doc, String number) {
        System.out.println("Faxing " + doc + " to " + number);
    }
}
""", "OfficeTester.java": """public class OfficeTester {
    public static void main(String[] args) {
        OfficeMachine m = new OfficeMachine();
        m.print("memo.txt");
        m.print("report.pdf");
        m.fax("contract.pdf", "555-0142");
        System.out.println(m.getPagesPrinted() + " pages printed");
    }
}
"""}, "OfficeTester", "Printing memo.txt\nPrinting report.pdf\nFaxing contract.pdf to 555-0142\n2 pages printed",
         tests={"CheckOffice.java": """public class CheckOffice {
    public static void main(String[] args) {
        Printer p = new OfficeMachine();
        p.print("a");
        Faxer f = new OfficeMachine();
        f.fax("b", "c");
    }
}
"""}, tests_run="CheckOffice", tests_output="Printing a\nFaxing b to c",
         hints=["The class header lists both interfaces after `implements`, separated by a comma."],
         checks=[{"pattern": r"implements\s+Printer\s*,\s*Faxer|implements\s+Faxer\s*,\s*Printer", "message": "Implement both: `implements Printer, Faxer`."}]),
    [IFACE_TUT, IFACE_TYPE_TUT, COMPARABLE_API, ARRAYS_API, HEL_9_2],
)
