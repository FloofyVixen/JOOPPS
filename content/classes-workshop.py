from sources import CLASSES_TUT, CONSTRUCTORS_TUT, ACCESS_TUT, OBJECT_TOSTRING, ARRAYS_TUT, HEL_4_2

# ---------- Guided 1: playlist ----------
SONG1 = """public class Song {
    private String title;
    private int seconds;

    public Song(String title, int seconds) {
        this.title = title;
        this.seconds = seconds;
    }

    public String getTitle() {
        return title;
    }

    public int getSeconds() {
        return seconds;
    }
}
"""
SONG2 = SONG1.replace("""    public int getSeconds() {
        return seconds;
    }
""", """    public int getSeconds() {
        return seconds;
    }

    @Override
    public String toString() {
        int minutes = seconds / 60;
        int rest = seconds % 60;
        if (rest < 10) {
            return title + " (" + minutes + ":0" + rest + ")";
        }
        return title + " (" + minutes + ":" + rest + ")";
    }
""")
PT1 = """public class PlaylistTester {
    public static void main(String[] args) {
        Song first = new Song("Blue Hour", 214);
        System.out.println(first.getTitle() + ": " + first.getSeconds() + " seconds");
    }
}
"""
PT2 = """public class PlaylistTester {
    public static void main(String[] args) {
        Song first = new Song("Blue Hour", 214);
        Song second = new Song("Low Tide", 187);
        System.out.println(first);
        System.out.println(second);
    }
}
"""
PL3 = """public class Playlist {
    private Song[] songs;

    public Playlist(int size) {
        songs = new Song[size];
    }

    public boolean add(Song song) {
        for (int i = 0; i < songs.length; i++) {
            if (songs[i] == null) {
                songs[i] = song;
                return true;
            }
        }
        return false;
    }

    @Override
    public String toString() {
        String result = "";
        for (Song song : songs) {
            if (song != null) {
                result = result + song + "\\n";
            }
        }
        return result;
    }
}
"""
PT3 = """public class PlaylistTester {
    public static void main(String[] args) {
        Playlist trip = new Playlist(3);
        System.out.println(trip.add(new Song("Blue Hour", 214)));
        System.out.println(trip.add(new Song("Low Tide", 187)));
        System.out.println(trip.add(new Song("Northbound", 240)));
        System.out.println(trip.add(new Song("One Too Many", 100)));
        System.out.print(trip);
    }
}
"""
PL4 = PL3.replace("""    @Override
    public String toString() {""", """    public int totalSeconds() {
        int total = 0;
        for (Song song : songs) {
            if (song != null) {
                total = total + song.getSeconds();
            }
        }
        return total;
    }

    public Song longest() {
        Song best = null;
        for (Song song : songs) {
            if (song != null && (best == null || song.getSeconds() > best.getSeconds())) {
                best = song;
            }
        }
        return best;
    }

    @Override
    public String toString() {""")
PT4 = """public class PlaylistTester {
    public static void main(String[] args) {
        Playlist trip = new Playlist(4);
        trip.add(new Song("Blue Hour", 214));
        trip.add(new Song("Low Tide", 187));
        trip.add(new Song("Northbound", 240));
        System.out.println("Total: " + trip.totalSeconds() + " seconds");
        System.out.println("Longest: " + trip.longest());

        Playlist empty = new Playlist(2);
        System.out.println("Longest in an empty playlist: " + empty.longest());
    }
}
"""

# ---------- Guided 2: bank ----------
ACC1 = """public class Account {
    private int id;
    private String owner;
    private double balance;

    public Account(int id, String owner) {
        this.id = id;
        this.owner = owner;
        balance = 0.0;
    }

    public int getId() {
        return id;
    }

    public String getOwner() {
        return owner;
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
"""
ACC2 = ACC1.replace("""            balance = balance + amount;
        }
    }
}
""", """            balance = balance + amount;
        }
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance = balance - amount;
            return true;
        }
        return false;
    }
}
""")
BT1 = """public class BankTester {
    public static void main(String[] args) {
        Account ana = new Account(0, "Ana");
        ana.deposit(40.0);
        ana.deposit(-10.0);
        System.out.println(ana.getOwner() + " has $" + ana.getBalance());
    }
}
"""
BT2 = """public class BankTester {
    public static void main(String[] args) {
        Account ana = new Account(0, "Ana");
        ana.deposit(40.0);
        ana.deposit(-10.0);
        System.out.println(ana.getOwner() + " has $" + ana.getBalance());
        System.out.println(ana.withdraw(15.0));
        System.out.println(ana.withdraw(100.0));
        System.out.println(ana.getOwner() + " has $" + ana.getBalance());
    }
}
"""
BANK3 = """public class Bank {
    private Account[] accounts;

    public Bank(int size) {
        accounts = new Account[size];
    }

    public int open(String owner) {
        for (int i = 0; i < accounts.length; i++) {
            if (accounts[i] == null) {
                accounts[i] = new Account(i, owner);
                return i;
            }
        }
        return -1;
    }

    public Account get(int id) {
        if (id < 0 || id >= accounts.length) {
            return null;
        }
        return accounts[id];
    }
}
"""
BT3 = """public class BankTester {
    public static void main(String[] args) {
        Bank bank = new Bank(2);
        int a = bank.open("Ana");
        int b = bank.open("Sam");
        int c = bank.open("Lee");
        System.out.println(a + " " + b + " " + c);

        bank.get(1).deposit(30.0);
        System.out.println(bank.get(1).getOwner() + " has $" + bank.get(1).getBalance());
        System.out.println(bank.get(5));
    }
}
"""
BANK4 = BANK3.replace("""        return accounts[id];
    }
}
""", """        return accounts[id];
    }

    public Account richest() {
        Account best = null;
        for (Account account : accounts) {
            if (account != null && (best == null || account.getBalance() > best.getBalance())) {
                best = account;
            }
        }
        return best;
    }
}
""")
BT4 = """public class BankTester {
    public static void main(String[] args) {
        Bank bank = new Bank(3);
        bank.open("Ana");
        bank.open("Sam");
        bank.open("Lee");
        bank.get(0).deposit(40.0);
        bank.get(1).deposit(90.0);
        bank.get(2).deposit(15.0);
        System.out.println("Richest: " + bank.richest().getOwner());

        Bank empty = new Bank(2);
        System.out.println(empty.richest());
    }
}
"""

NULL_CHECK = {"pattern": r"!=\s*null", "message": "Skip empty slots with a `!= null` check."}
PRIVATE_FIELDS = {"pattern": r"private\s+\w+\s+\w+\s*;", "message": "Make the fields `private`."}

LESSON = {
    "id": "classes-workshop",
    "title": "Workshop: classes and objects",
    "summary": "Design classes from scratch: two guided builds, then two you write on your own.",
    "goals": [
        "Write classes with private fields, constructors, getters and `toString` without starter code",
        "Build a manager class around an array of your own objects",
        "Grow a program step by step, running it after every change",
    ],
    "cos225": "The COS 225 exam guide says you may need to \"construct classes from scratch, along with constructors and other methods\", graded more on whether each piece is right than on exact syntax. The independent tasks here are that kind of question. Try writing each one on paper before you type it in.",
    "blocks": [
        {"type": "h", "text": "Before you start"},
        {"type": "p", "text": "Each guided task builds a program across several files. A step tells you which file to create or change, and it's done when your program's output matches. Your code carries over from step to step. The independent tasks give only the specification, the expected output and a test file, just like an assignment."},
        {"type": "p", "text": "Read the whole task before you write anything. The exam guide's last piece of advice applies here too: spend a few minutes reading each coding problem before you start writing."},

        {"type": "h", "text": "Guided 1: a playlist"},
        {"type": "write", "id": "ws-classes-playlist", "mode": "guided", "title": "A playlist",
         "goal": "Build a `Song` class and a `Playlist` that holds songs in an array, with a total length and the longest song.",
         "files": ["Song.java", "PlaylistTester.java", "Playlist.java"],
         "steps": [
             {"title": "The Song class", "run": "PlaylistTester",
              "files": ["Song.java", "PlaylistTester.java"],
              "solution": {"Song.java": SONG1, "PlaylistTester.java": PT1},
              "text": "Create `Song.java` with private fields `title` (`String`) and `seconds` (`int`), a constructor that takes both, and the getters `getTitle()` and `getSeconds()`. Create `PlaylistTester.java` whose `main` makes the song \"Blue Hour\" (214 seconds) and prints it using the getters.",
              "hint": "`System.out.println(first.getTitle() + \": \" + first.getSeconds() + \" seconds\");`",
              "checks": [PRIVATE_FIELDS],
              "output": "Blue Hour: 214 seconds"},
             {"title": "Minutes and seconds", "run": "PlaylistTester",
              "files": ["Song.java", "PlaylistTester.java"],
              "solution": {"Song.java": SONG2, "PlaylistTester.java": PT2},
              "text": "Give `Song` a `toString` that shows the length as minutes and seconds, like `Blue Hour (3:34)`. Seconds below 10 need a leading zero. Change the tester to print two songs directly: \"Blue Hour\" (214) and \"Low Tide\" (187).",
              "hint": "Minutes are `seconds / 60` and the rest is `seconds % 60`. This is the same leading-zero problem as the `Clock` task.",
              "output": "Blue Hour (3:34)\nLow Tide (3:07)"},
             {"title": "The Playlist class", "run": "PlaylistTester",
              "files": ["Song.java", "PlaylistTester.java", "Playlist.java"],
              "solution": {"Song.java": SONG2, "PlaylistTester.java": PT3, "Playlist.java": PL3},
              "text": "Create `Playlist.java` with a private `Song[]` sized by the constructor. `add(Song)` puts the song in the first empty slot and returns `true`, or `false` when full. `toString` returns every song, each followed by a line break (`\"\\n\"`). In the tester, make a playlist of size 3, print what `add` returns for four songs, and finish with `System.out.print(trip);`.",
              "hint": "Use `print`, not `println`, for the playlist, because `toString` already ends with a line break.",
              "checks": [NULL_CHECK],
              "output": "true\ntrue\ntrue\nfalse\nBlue Hour (3:34)\nLow Tide (3:07)\nNorthbound (4:00)"},
             {"title": "Total and longest", "run": "PlaylistTester",
              "files": ["Song.java", "PlaylistTester.java", "Playlist.java"],
              "solution": {"Song.java": SONG2, "PlaylistTester.java": PT4, "Playlist.java": PL4},
              "text": "Add `totalSeconds()` and `longest()` to `Playlist`. `longest()` returns the song with the most seconds, or `null` for an empty playlist. Update the tester to match the expected output: a size-4 playlist with three songs, then an empty playlist of size 2.",
              "hint": "In `longest()`, keep the best song so far in a variable that starts as `null`. A song beats it if `best == null` or the song is longer.",
              "output": "Total: 641 seconds\nLongest: Northbound (4:00)\nLongest in an empty playlist: null"},
         ]},

        {"type": "h", "text": "Guided 2: a small bank"},
        {"type": "write", "id": "ws-classes-bank", "mode": "guided", "title": "A small bank",
         "goal": "Build an `Account` class that protects its balance, and a `Bank` that opens accounts and finds the richest one.",
         "files": ["Account.java", "BankTester.java", "Bank.java"],
         "steps": [
             {"title": "The Account class", "run": "BankTester",
              "files": ["Account.java", "BankTester.java"],
              "solution": {"Account.java": ACC1, "BankTester.java": BT1},
              "text": "Create `Account.java` with private fields `id` (`int`), `owner` (`String`) and `balance` (`double`). The constructor takes the id and the owner, and the balance starts at 0. Add the three getters and `deposit(double)`, which ignores amounts that aren't positive. In `BankTester`, deposit 40.0 and then -10.0 into Ana's account and print her balance.",
              "checks": [PRIVATE_FIELDS],
              "output": "Ana has $40.0"},
             {"title": "Withdrawing", "run": "BankTester",
              "files": ["Account.java", "BankTester.java"],
              "solution": {"Account.java": ACC2, "BankTester.java": BT2},
              "text": "Add `withdraw(double)`, which returns `true` and takes the money if the amount is positive and no more than the balance, and otherwise returns `false` and changes nothing. Print what two withdrawals return (15.0, then 100.0) and the balance after.",
              "hint": "Return `true` inside the `if`, after changing the balance, and `return false;` after it.",
              "output": "Ana has $40.0\ntrue\nfalse\nAna has $25.0"},
             {"title": "The Bank class", "run": "BankTester",
              "files": ["Account.java", "BankTester.java", "Bank.java"],
              "solution": {"Account.java": ACC2, "BankTester.java": BT3, "Bank.java": BANK3},
              "text": "Create `Bank.java` with a private `Account[]`. `open(String owner)` creates a new account in the first empty slot, using the slot number as its id, and returns the id (or -1 when full). `get(int id)` returns the account in that slot, or `null` if the id is out of range.",
              "hint": "`accounts[i] = new Account(i, owner);` The bank creates the account itself; the tester only passes the owner's name.",
              "output": "0 1 -1\nSam has $30.0\nnull"},
             {"title": "The richest account", "run": "BankTester",
              "files": ["Account.java", "BankTester.java", "Bank.java"],
              "solution": {"Account.java": ACC2, "BankTester.java": BT4, "Bank.java": BANK4},
              "text": "Add `richest()` to `Bank`, which returns the account with the highest balance, or `null` if the bank has no accounts. Update the tester as shown by the expected output.",
              "hint": "This is the same pattern as `longest()` in the playlist.",
              "checks": [NULL_CHECK],
              "output": "Richest: Sam\nnull"},
         ]},

        {"type": "h", "text": "Independent 1: an inventory"},
        {"type": "write", "id": "ws-classes-inventory", "mode": "independent", "title": "A store inventory",
         "goal": "Write `Item` (private `name` and `quantity`, a constructor, getters, and `toString` like `Eraser x12`) and `Inventory`, which keeps a private `Item[]` sized by its constructor. `add(Item)` returns the slot used, or -1 when full. `remove(String name)` removes and returns that item, or `null`. `totalQuantity()` adds up every item's quantity. `toString` returns text like `3 items, 57 units`. Finish with `InventoryTester`.",
         "files": ["Item.java", "Inventory.java", "InventoryTester.java"], "run": "InventoryTester",
         "output": "0\n1\n2\n-1\n3 items, 57 units\nEraser x12\nnull\n2 items, 45 units",
         "solution": {"Item.java": """public class Item {
    private String name;
    private int quantity;

    public Item(String name, int quantity) {
        this.name = name;
        this.quantity = quantity;
    }

    public String getName() {
        return name;
    }

    public int getQuantity() {
        return quantity;
    }

    @Override
    public String toString() {
        return name + " x" + quantity;
    }
}
""", "Inventory.java": """public class Inventory {
    private Item[] items;

    public Inventory(int size) {
        items = new Item[size];
    }

    public int add(Item item) {
        for (int i = 0; i < items.length; i++) {
            if (items[i] == null) {
                items[i] = item;
                return i;
            }
        }
        return -1;
    }

    public Item remove(String name) {
        for (int i = 0; i < items.length; i++) {
            if (items[i] != null && items[i].getName().equals(name)) {
                Item removed = items[i];
                items[i] = null;
                return removed;
            }
        }
        return null;
    }

    public int totalQuantity() {
        int total = 0;
        for (Item item : items) {
            if (item != null) {
                total = total + item.getQuantity();
            }
        }
        return total;
    }

    @Override
    public String toString() {
        int count = 0;
        for (Item item : items) {
            if (item != null) {
                count++;
            }
        }
        return count + " items, " + totalQuantity() + " units";
    }
}
""", "InventoryTester.java": """public class InventoryTester {
    public static void main(String[] args) {
        Inventory shop = new Inventory(3);
        System.out.println(shop.add(new Item("Pencil", 40)));
        System.out.println(shop.add(new Item("Eraser", 12)));
        System.out.println(shop.add(new Item("Ruler", 5)));
        System.out.println(shop.add(new Item("Glue", 3)));
        System.out.println(shop);
        System.out.println(shop.remove("Eraser"));
        System.out.println(shop.remove("Tape"));
        System.out.println(shop);
    }
}
"""},
         "tests": {"CheckInventory.java": """public class CheckInventory {
    public static void main(String[] args) {
        Inventory inv = new Inventory(2);
        System.out.println(inv);
        inv.add(new Item("A", 1));
        inv.remove("A");
        System.out.println(inv.add(new Item("B", 2)));
        System.out.println(inv);
    }
}
"""}, "tests_run": "CheckInventory", "tests_output": "0 items, 0 units\n0\n1 items, 2 units",
         "requirements": ["Three files: `Item.java`, `Inventory.java`, `InventoryTester.java`",
                          "Fields are `private`", "A removed item's slot can be used again"],
         "hints": ["Write and test one method at a time. Comment out the tester lines for methods you haven't written yet.",
                   "`toString` can call `totalQuantity()` instead of adding up the quantities a second time."],
         "checks": [PRIVATE_FIELDS, {"pattern": r"\.equals\s*\(", "message": "Compare names with `.equals(...)`."}]},

        {"type": "h", "text": "Independent 2: a class from scratch, exam-sized"},
        {"type": "write", "id": "ws-classes-course", "mode": "independent", "title": "A course with limited seats",
         "goal": "Write a `Course` class with private fields for its name, its capacity and how many students are enrolled. The constructor takes the name and capacity; nobody is enrolled yet. `enroll()` adds one student and returns `true` if there's a seat, otherwise `false`. `getOpenSeats()` returns the seats left. `toString` returns text like `BIO 100: 2 of 2 seats taken`. Then write `CourseTester`.",
         "files": ["Course.java", "CourseTester.java"], "run": "CourseTester",
         "output": "BIO 100: 0 of 2 seats taken\ntrue\ntrue\nfalse\n0\nBIO 100: 2 of 2 seats taken",
         "solution": {"Course.java": """public class Course {
    private String name;
    private int capacity;
    private int enrolled;

    public Course(String name, int capacity) {
        this.name = name;
        this.capacity = capacity;
        enrolled = 0;
    }

    public boolean enroll() {
        if (enrolled < capacity) {
            enrolled++;
            return true;
        }
        return false;
    }

    public int getOpenSeats() {
        return capacity - enrolled;
    }

    @Override
    public String toString() {
        return name + ": " + enrolled + " of " + capacity + " seats taken";
    }
}
""", "CourseTester.java": """public class CourseTester {
    public static void main(String[] args) {
        Course bio = new Course("BIO 100", 2);
        System.out.println(bio);
        System.out.println(bio.enroll());
        System.out.println(bio.enroll());
        System.out.println(bio.enroll());
        System.out.println(bio.getOpenSeats());
        System.out.println(bio);
    }
}
"""},
         "tests": {"CheckCourse.java": """public class CheckCourse {
    public static void main(String[] args) {
        Course art = new Course("ART 101", 30);
        art.enroll();
        art.enroll();
        art.enroll();
        System.out.println(art.getOpenSeats());
        System.out.println(art);
    }
}
"""}, "tests_run": "CheckCourse", "tests_output": "27\nART 101: 3 of 30 seats taken",
         "requirements": ["About 20 lines for `Course`, the size of an exam question", "Fields are `private`"],
         "hints": ["Three fields, one constructor, three methods. Write the field list first, then each method header, then fill in the bodies."],
         "checks": [PRIVATE_FIELDS]},
    ],
    "sources": [CLASSES_TUT, CONSTRUCTORS_TUT, ACCESS_TUT, OBJECT_TOSTRING, ARRAYS_TUT, HEL_4_2],
}
