from sources import COMPARABLE_API, ARRAYS_API, IFACE_IMPL_TUT, GENERICS_TUT

SONG = """public class Song implements Comparable<Song> {
    private String title;
    private int seconds;

    public Song(String title, int seconds) {
        this.title = title;
        this.seconds = seconds;
    }

    @Override
    public int compareTo(Song other) {
        return Integer.compare(seconds, other.seconds);
    }

    @Override
    public String toString() {
        return title + " (" + seconds + "s)";
    }
}
"""
SORT = """import java.util.Arrays;

public class SortSongs {
    public static void main(String[] args) {
        Song[] songs = {
            new Song("Northbound", 240),
            new Song("Low Tide", 187),
            new Song("Blue Hour", 214)
        };
        Arrays.sort(songs);
        for (Song s : songs) {
            System.out.println(s);
        }
    }
}
"""
COMPARE = """public class CompareDemo {
    public static void main(String[] args) {
        Song a = new Song("Low Tide", 187);
        Song b = new Song("Blue Hour", 214);
        System.out.println(a.compareTo(b) < 0);
        System.out.println(b.compareTo(a) > 0);
        System.out.println(a.compareTo(a) == 0);
        System.out.println("apple".compareTo("banana") < 0);
    }
}
"""

LESSON = {
    "id": "iface-comparable",
    "title": "The Comparable interface",
    "summary": "Java's own `Comparable` interface lets your objects say which comes first, so the library can sort them for you.",
    "goals": [
        "Implement `Comparable<T>` and its `compareTo` method",
        "Read what a negative, zero or positive result means",
        "Sort an array of your own objects with `Arrays.sort`",
    ],
    "blocks": [
        {"type": "h", "text": "An interface Java already uses"},
        {"type": "p", "text": "Java's library is full of interfaces. One of the most useful is `Comparable`, which has a single method, `compareTo`. If your class implements it, Java's sorting methods know how to put your objects in order."},
        {"type": "p", "text": "`a.compareTo(b)` returns a **negative** number if `a` comes before `b`, **zero** if they're equal in order, and a **positive** number if `a` comes after `b`. Only the sign matters, not the size of the number."},
        {"type": "code", "files": {"Song.java": SONG, "SortSongs.java": SORT}, "run": "SortSongs"},
        {"type": "list", "items": [
            "`Comparable<Song>` means \"comparable with other `Song`s\". The type in angle brackets is a **type parameter**; you'll write your own in the generics lesson of unit 12. It makes `compareTo` take a `Song` instead of an `Object`.",
            "`Integer.compare(x, y)` returns the right sign for two `int`s. It's the safe way to compare numbers inside `compareTo`.",
            "`Arrays.sort` comes from `java.util.Arrays`, so the file starts with `import java.util.Arrays;`. It calls your `compareTo` to decide the order.",
            "`compareTo` can read `other.seconds` directly, even though it's private: private means \"inside this class\", and `other` is the same class.",
        ]},
        {"type": "code", "files": {"Song.java": SONG, "CompareDemo.java": COMPARE}, "run": "CompareDemo",
         "caption": "`String` already implements `Comparable`, comparing alphabetically (by character codes, so capital letters sort before lowercase)."},

        {"type": "h", "text": "Sorting something that can't be compared"},
        {"type": "p", "text": "If the class doesn't implement `Comparable`, the code still compiles, because `Arrays.sort` accepts any array of objects. But at run time Java has no way to order them, and it crashes:"},
        {"type": "code", "files": {"Song.java": SONG.replace(" implements Comparable<Song>", "").replace("""    @Override
    public int compareTo(Song other) {
        return Integer.compare(seconds, other.seconds);
    }

""", ""), "SortSongs.java": SORT}, "run": "SortSongs", "expect": "runtime",
         "after": "The `ClassCastException` says `Song` can't be treated as a `java.lang.Comparable`. The `at` lines run through Java's own sorting code before reaching line 10 of `SortSongs`, which is the line to look at."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "comp-player", "title": "Highest score first",
         "prompt": "Players should sort from the **highest** score down. Swap the order of the two numbers to reverse the sort.",
         "files": {"Player.java": """public class Player [[impl]] {
    private String name;
    private int score;

    public Player(String name, int score) {
        this.name = name;
        this.score = score;
    }

    @Override
    public int compareTo(Player other) {
        return Integer.compare([[first]], [[second]]);
    }

    @Override
    public String toString() {
        return name + ": " + score;
    }
}
""", "Leaderboard.java": """import java.util.Arrays;

public class Leaderboard {
    public static void main(String[] args) {
        Player[] players = {new Player("Ana", 120), new Player("Sam", 340), new Player("Lee", 95)};
        Arrays.sort(players);
        for (Player p : players) {
            System.out.println(p);
        }
    }
}
"""},
         "run": "Leaderboard", "output": "Sam: 340\nAna: 120\nLee: 95",
         "blanks": {
             "impl": {"accept": ["implements Comparable<Player>"], "hint": "Promise to be comparable with other players.",
                      "wrong": [{"answer": "implements Comparable", "why": "Without `<Player>`, `Comparable` expects `compareTo(Object)`, so your `compareTo(Player)` doesn't match it. The compiler says the class doesn't override `compareTo(Object)`."},
                                {"answer": "extends Comparable<Player>", "why": "`Comparable` is an interface, so a class `implements` it."}]},
             "first": {"accept": ["other.score"], "hint": "For highest-first, put the other player's score first.",
                       "wrong": [{"answer": "score", "why": "With the second blank already `score`, this compares each player's score with itself. That's always 0, so every player counts as equal and nothing moves. For highest-first, the other player's score goes first."}]},
             "second": {"accept": ["score", "this.score"], "hint": "Then this player's score.",
                        "wrong": [{"answer": "other.score", "why": "Comparing `other.score` with itself is always 0, so every player counts as equal and the order never changes."}]},
         },
         "explain": "`Integer.compare(other.score, score)` is negative when this player has the higher score, so higher scores sort first."},
        {"type": "quiz", "id": "comp-sign",
         "question": "`x.compareTo(y)` returns `-3`. What does that mean?",
         "choices": ["`x` comes 3 places before `y`", "`x` comes before `y`", "`x` and `y` are equal", "`x` comes after `y`"],
         "answer": 1,
         "explain": "Only the sign matters: negative means `x` comes first. The number 3 itself carries no meaning."},
    ],
    "sources": [COMPARABLE_API, ARRAYS_API, IFACE_IMPL_TUT, GENERICS_TUT],
}
