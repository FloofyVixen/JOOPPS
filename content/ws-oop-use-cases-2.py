from sources import ARRAYS_TUT, NPE, STRING_EQUALS, HEL_4_2
from wshelp import step, guided, workshop, task

NULLCHK = {"pattern": r"!=\s*null", "message": "Skip empty slots with a `!= null` check."}

PLAYER = """public class Player {
    private String name;
    private int number;

    public Player(String name, int number) {
        this.name = name;
        this.number = number;
    }

    public String getName() {
        return name;
    }

    public int getNumber() {
        return number;
    }

    @Override
    public String toString() {
        return "#" + number + " " + name;
    }
}
"""
TEAM2 = """public class Team {
    private Player[] players;

    public Team(int size) {
        players = new Player[size];
    }

    public boolean add(Player p) {
        for (int i = 0; i < players.length; i++) {
            if (players[i] == null) {
                players[i] = p;
                return true;
            }
        }
        return false;
    }

    @Override
    public String toString() {
        String result = "";
        for (Player p : players) {
            if (p != null) {
                result = result + p + "\\n";
            }
        }
        return result;
    }
}
"""
FIND = """    public Player findByNumber(int number) {
        for (Player p : players) {
            if (p != null && p.getNumber() == number) {
                return p;
            }
        }
        return null;
    }

"""
COUNT = """    public int count() {
        int count = 0;
        for (Player p : players) {
            if (p != null) {
                count++;
            }
        }
        return count;
    }

"""
TEAM3 = TEAM2.replace("    @Override", FIND + "    @Override")
TEAM4 = TEAM2.replace("    @Override", FIND + COUNT + "    @Override")
TT1 = """public class TeamTester {
    public static void main(String[] args) {
        Player ana = new Player("Ana", 7);
        System.out.println(ana);
        System.out.println(ana.getName() + " wears " + ana.getNumber());
    }
}
"""
TT2 = """public class TeamTester {
    public static void main(String[] args) {
        Team team = new Team(3);
        team.add(new Player("Ana", 7));
        team.add(new Player("Sam", 10));
        team.add(new Player("Lee", 4));
        System.out.println(team.add(new Player("Kai", 9)));
        System.out.print(team);
    }
}
"""
TT3 = """public class TeamTester {
    public static void main(String[] args) {
        Team team = new Team(3);
        team.add(new Player("Ana", 7));
        team.add(new Player("Sam", 10));
        System.out.println(team.findByNumber(10));
        System.out.println(team.findByNumber(99));
    }
}
"""
TT4 = TT3.replace("""        System.out.println(team.findByNumber(99));
""", """        System.out.println(team.findByNumber(99));
        System.out.println(team.count() + " players");
""")

PRODUCT = """public class Product {
    private String name;
    private double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    @Override
    public String toString() {
        return name + " ($" + price + ")";
    }
}
"""
CART2 = """public class Cart {
    private Product[] items;

    public Cart(int size) {
        items = new Product[size];
    }

    public boolean add(Product p) {
        for (int i = 0; i < items.length; i++) {
            if (items[i] == null) {
                items[i] = p;
                return true;
            }
        }
        return false;
    }

    public double total() {
        double sum = 0;
        for (Product p : items) {
            if (p != null) {
                sum = sum + p.getPrice();
            }
        }
        return sum;
    }
}
"""
MOST = """
    public Product mostExpensive() {
        Product best = null;
        for (Product p : items) {
            if (p != null && (best == null || p.getPrice() > best.getPrice())) {
                best = p;
            }
        }
        return best;
    }
"""
REMOVE = """
    public boolean remove(String name) {
        for (int i = 0; i < items.length; i++) {
            if (items[i] != null && items[i].getName().equals(name)) {
                items[i] = null;
                return true;
            }
        }
        return false;
    }
"""
CART3 = CART2[:-2] + MOST + "}\n"
CART4 = CART2[:-2] + MOST + REMOVE + "}\n"
CAT1 = """public class ShopTester {
    public static void main(String[] args) {
        Product mug = new Product("Mug", 8.5);
        System.out.println(mug);
    }
}
"""
CAT2 = """public class ShopTester {
    public static void main(String[] args) {
        Cart cart = new Cart(3);
        cart.add(new Product("Mug", 8.5));
        cart.add(new Product("Tea", 4.0));
        System.out.println("Total: $" + cart.total());
    }
}
"""
CAT3 = CAT2.replace("""        System.out.println("Total: $" + cart.total());
""", """        cart.add(new Product("Kettle", 25.0));
        System.out.println("Total: $" + cart.total());
        System.out.println("Most expensive: " + cart.mostExpensive());
""")
CAT4 = CAT3.replace("""        System.out.println("Most expensive: " + cart.mostExpensive());
""", """        System.out.println("Most expensive: " + cart.mostExpensive());
        System.out.println(cart.remove("Kettle"));
        System.out.println(cart.remove("Spoon"));
        System.out.println("Total: $" + cart.total());
        System.out.println("Most expensive: " + cart.mostExpensive());
""")

LESSON = workshop(
    "ws-oop-use-cases-2", "Workshop: arrays of objects",
    "Practice classes that manage an array of other objects: adding to the first empty slot, searching, counting and removing.",
    ["Write a manager class around a private array from scratch",
     "Search an array of objects and handle \"not found\"",
     "Create objects inside a loop"],
    guided("ws-u5-team", "A team roster", "Build a `Team` that holds `Player` objects in an array.", [
        step("The Player", "Create `Player.java` with private `name` and `number`, a constructor, getters, and a `toString` like `#7 Ana`.",
             {"Player.java": PLAYER, "TeamTester.java": TT1}, "TeamTester", "#7 Ana\nAna wears 7"),
        step("The Team", "Create `Team.java` with a private `Player[]` sized by the constructor. `add(Player)` uses the first empty slot and returns `true`, or `false` when full. `toString` lists the players, each followed by `\"\\n\"`. Print the team with `System.out.print`.",
             {"Player.java": PLAYER, "Team.java": TEAM2, "TeamTester.java": TT2}, "TeamTester",
             "false\n#7 Ana\n#10 Sam\n#4 Lee", checks=[NULLCHK]),
        step("Finding a player", "Add `findByNumber(int number)`, which returns the matching player or `null`. Numbers are `int`s, so compare them with `==`.",
             {"Player.java": PLAYER, "Team.java": TEAM3, "TeamTester.java": TT3}, "TeamTester", "#10 Sam\nnull",
             hint="Check the slot isn't `null` before calling `getNumber()`."),
        step("Counting", "Add `count()`, the number of slots that hold a player.",
             {"Player.java": PLAYER, "Team.java": TEAM4, "TeamTester.java": TT4}, "TeamTester", "#10 Sam\nnull\n2 players"),
    ]),
    guided("ws-u5-cart", "A shopping cart", "Build a `Cart` of `Product`s with a total, the most expensive item, and removal.", [
        step("The Product", "Create `Product.java` with private `name` and `price`, a constructor, getters, and a `toString` like `Mug ($8.5)`.",
             {"Product.java": PRODUCT, "ShopTester.java": CAT1}, "ShopTester", "Mug ($8.5)"),
        step("Cart and total", "Create `Cart.java` with a private `Product[]`, `add(Product)` (first empty slot, `false` when full) and `total()`.",
             {"Product.java": PRODUCT, "Cart.java": CART2, "ShopTester.java": CAT2}, "ShopTester", "Total: $12.5", checks=[NULLCHK]),
        step("The priciest item", "Add `mostExpensive()`, which returns the product with the highest price, or `null` for an empty cart.",
             {"Product.java": PRODUCT, "Cart.java": CART3, "ShopTester.java": CAT3}, "ShopTester",
             "Total: $37.5\nMost expensive: Kettle ($25.0)",
             hint="Keep the best so far in a variable that starts as `null`."),
        step("Removing", "Add `remove(String name)`, which empties the slot of the product with that name and returns `true`, or returns `false` if it isn't in the cart.",
             {"Product.java": PRODUCT, "Cart.java": CART4, "ShopTester.java": CAT4}, "ShopTester",
             "Total: $37.5\nMost expensive: Kettle ($25.0)\ntrue\nfalse\nTotal: $12.5\nMost expensive: Mug ($8.5)",
             checks=[{"pattern": r"\.equals\s*\(", "message": "Compare names with `.equals(...)`."}]),
    ]),
    task("ws-u5-hotel", "A hotel that builds its own rooms",
         "Write `Room` (private `number` and `booked`, a constructor taking the number, `getNumber()`, `isBooked()`, `book()`) and `Hotel`, whose constructor takes how many rooms and the first room number and **creates every `Room` itself** in a loop. `bookFirstFree()` books the first free room and returns its number, or -1. `freeCount()` counts free rooms.",
         {"Room.java": """public class Room {
    private int number;
    private boolean booked;

    public Room(int number) {
        this.number = number;
    }

    public int getNumber() {
        return number;
    }

    public boolean isBooked() {
        return booked;
    }

    public void book() {
        booked = true;
    }
}
""", "Hotel.java": """public class Hotel {
    private Room[] rooms;

    public Hotel(int count, int firstNumber) {
        rooms = new Room[count];
        for (int i = 0; i < count; i++) {
            rooms[i] = new Room(firstNumber + i);
        }
    }

    public int bookFirstFree() {
        for (Room r : rooms) {
            if (!r.isBooked()) {
                r.book();
                return r.getNumber();
            }
        }
        return -1;
    }

    public int freeCount() {
        int free = 0;
        for (Room r : rooms) {
            if (!r.isBooked()) {
                free++;
            }
        }
        return free;
    }
}
""", "HotelTester.java": """public class HotelTester {
    public static void main(String[] args) {
        Hotel inn = new Hotel(3, 101);
        System.out.println(inn.bookFirstFree());
        System.out.println(inn.bookFirstFree());
        System.out.println(inn.freeCount() + " free");
        System.out.println(inn.bookFirstFree());
        System.out.println(inn.bookFirstFree());
        System.out.println(inn.freeCount() + " free");
    }
}
"""}, "HotelTester", "101\n102\n1 free\n103\n-1\n0 free",
         tests={"CheckHotel.java": """public class CheckHotel {
    public static void main(String[] args) {
        Hotel h = new Hotel(2, 500);
        System.out.println(h.freeCount());
        System.out.println(h.bookFirstFree());
        System.out.println(h.freeCount());
    }
}
"""}, tests_run="CheckHotel", tests_output="2\n500\n1",
         hints=["In the constructor: `rooms[i] = new Room(firstNumber + i);`",
                "Every slot holds a room here, so these loops don't need a null check. `!` means \"not\": `!r.isBooked()`."]),
    task("ws-u5-grades", "A gradebook",
         "Write `Assignment` (private `name` and `int score`, a constructor, getters, `toString` like `Lab 2 (90)`) and `Gradebook` with a private `Assignment[]`, `add` (`false` when full), `average()` (a `double`; 0.0 when empty) and `best()` (or `null`).",
         {"Assignment.java": """public class Assignment {
    private String name;
    private int score;

    public Assignment(String name, int score) {
        this.name = name;
        this.score = score;
    }

    public String getName() {
        return name;
    }

    public int getScore() {
        return score;
    }

    @Override
    public String toString() {
        return name + " (" + score + ")";
    }
}
""", "Gradebook.java": """public class Gradebook {
    private Assignment[] work;

    public Gradebook(int size) {
        work = new Assignment[size];
    }

    public boolean add(Assignment a) {
        for (int i = 0; i < work.length; i++) {
            if (work[i] == null) {
                work[i] = a;
                return true;
            }
        }
        return false;
    }

    public double average() {
        int total = 0;
        int count = 0;
        for (Assignment a : work) {
            if (a != null) {
                total = total + a.getScore();
                count++;
            }
        }
        if (count == 0) {
            return 0.0;
        }
        return (double) total / count;
    }

    public Assignment best() {
        Assignment top = null;
        for (Assignment a : work) {
            if (a != null && (top == null || a.getScore() > top.getScore())) {
                top = a;
            }
        }
        return top;
    }
}
""", "GradeTester.java": """public class GradeTester {
    public static void main(String[] args) {
        Gradebook book = new Gradebook(4);
        book.add(new Assignment("Quiz 1", 80));
        book.add(new Assignment("Lab 2", 90));
        book.add(new Assignment("Quiz 2", 70));
        System.out.println("Average: " + book.average());
        System.out.println("Best: " + book.best());
    }
}
"""}, "GradeTester", "Average: 80.0\nBest: Lab 2 (90)",
         tests={"CheckGrades.java": """public class CheckGrades {
    public static void main(String[] args) {
        Gradebook empty = new Gradebook(2);
        System.out.println(empty.average() + " " + empty.best());
        empty.add(new Assignment("Essay", 55));
        empty.add(new Assignment("Exam", 60));
        System.out.println(empty.average());
    }
}
"""}, tests_run="CheckGrades", tests_output="0.0 null\n57.5",
         hints=["Count the assignments as you add up the scores; empty slots don't count.",
                "`total / count` with two `int`s drops the decimal. `(double) total / count` keeps it. Check the test with 55 and 60."]),
    [ARRAYS_TUT, NPE, STRING_EQUALS, HEL_4_2],
)
