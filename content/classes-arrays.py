from sources import ARRAYS_TUT, FOR_TUT, JLS_ARRAY_CREATE, NPE, JEP358, STRING_EQUALS, HEL_3_3, HEL_4_2

SONG = """public class Song {
    private String title;
    private String artist;
    private int seconds;

    public Song(String title, String artist, int seconds) {
        this.title = title;
        this.artist = artist;
        this.seconds = seconds;
    }

    public String getTitle() {
        return title;
    }

    public int getSeconds() {
        return seconds;
    }

    @Override
    public String toString() {
        return title + " by " + artist;
    }
}
"""

INT_ARRAY = """public class Laps {
    public static void main(String[] args) {
        int[] laps = new int[3];
        laps[0] = 62;
        laps[1] = 58;

        System.out.println("Number of laps: " + laps.length);
        for (int i = 0; i < laps.length; i++) {
            System.out.println("Lap " + i + ": " + laps[i]);
        }
    }
}
"""

ARRAY_DEMO = """public class ArrayDemo {
    public static void main(String[] args) {
        Song[] songs = new Song[3];
        songs[0] = new Song("Blue Hour", "The Lanterns", 214);
        songs[2] = new Song("Low Tide", "Mira Holt", 187);

        for (int i = 0; i < songs.length; i++) {
            System.out.println(i + ": " + songs[i]);
        }
    }
}
"""

PLAYLIST = """public class Playlist {
    private Song[] songs;

    public Playlist(int size) {
        songs = new Song[size];
    }

    public void set(int slot, Song song) {
        songs[slot] = song;
    }

    public int totalSeconds() {
        int total = 0;
        for (int i = 0; i < songs.length; i++) {
            if (songs[i] != null) {
                total = total + songs[i].getSeconds();
            }
        }
        return total;
    }

    @Override
    public String toString() {
        String result = "";
        for (Song song : songs) {
            if (song != null) {
                result = result + song + "\\n";
            }
        }
        return result + "Total: " + totalSeconds() + " seconds";
    }
}
"""

PL_TESTER = """public class PlaylistTester {
    public static void main(String[] args) {
        Playlist roadTrip = new Playlist(4);
        roadTrip.set(0, new Song("Blue Hour", "The Lanterns", 214));
        roadTrip.set(1, new Song("Low Tide", "Mira Holt", 187));
        roadTrip.set(3, new Song("Northbound", "Kesh", 240));

        System.out.println(roadTrip);
    }
}
"""

PLAYLIST_NO_CHECK = PLAYLIST.replace("""            if (songs[i] != null) {
                total = total + songs[i].getSeconds();
            }
""", """            total = total + songs[i].getSeconds();
""")

LESSON = {
    "id": "classes-arrays",
    "title": "Arrays of objects",
    "summary": "Keep many objects in one array, and handle the empty slots safely.",
    "goals": [
        "Create an array of objects and fill its slots",
        "Explain why a new array of objects is full of `null`",
        "Loop over an array with an index or with a for-each loop, skipping empty slots",
        "Read a `NullPointerException` and find its cause",
    ],
    "cos225": "Several COS 225 assignments are built on a \"manager\" class that holds an array of other objects, with methods to add, remove and count them. This lesson covers the array side of that pattern. The project after it builds the whole thing.",
    "blocks": [
        {"type": "h", "text": "A quick review of arrays"},
        {"type": "p", "text": "An array holds a fixed number of values of one type. You choose its size when you create it, and it can't grow afterwards. Slots are numbered from 0, so an array of length 3 has slots 0, 1 and 2. `laps.length` gives the size (no parentheses)."},
        {"type": "code", "files": {"Laps.java": INT_ARRAY}, "run": "Laps",
         "after": "Slot 2 was never set, so it holds the default value for `int`, which is 0."},

        {"type": "h", "text": "Arrays of objects start out empty"},
        {"type": "p", "text": "An array can hold objects too. `new Song[3]` creates the array, the row of slots, but **no `Song` objects**. Each slot holds the default for an object type, which is `null`. You fill a slot by putting a real object in it."},
        {"type": "p", "text": "From here on, `Song` uses `private` fields with getters, as in the last lesson, plus the `toString` from the lesson before that."},
        {"type": "code", "files": {"Song.java": SONG}, "show": False, "caption": "`Song.java`"},
        {"type": "code", "files": {"Song.java": SONG, "ArrayDemo.java": ARRAY_DEMO}, "run": "ArrayDemo",
         "after": "Printing `null` is fine. `println` and `+` just show the word \"null\". The trouble starts when you call a method on it."},

        {"type": "h", "text": "A class that holds an array"},
        {"type": "p", "text": "Usually the array lives inside another class, which manages it. `Playlist` keeps its songs in a private array, and its methods are the only way in. Its loops skip empty slots by checking `!= null` before using a song."},
        {"type": "code", "files": {"Song.java": SONG, "Playlist.java": PLAYLIST, "PlaylistTester.java": PL_TESTER},
         "run": "PlaylistTester"},
        {"type": "list", "items": [
            "The constructor creates the array, using the size it's given. The field starts as `null` until then.",
            "`totalSeconds` uses an index loop: `songs[i]` is the song in slot `i`.",
            "`toString` uses a **for-each** loop: `for (Song song : songs)` gives you each item in turn. Use it when you don't need the slot number.",
            "`\"\\n\"` inside a string is a line break.",
        ]},

        {"type": "h", "text": "When the null check is missing"},
        {"type": "error", "id": "arrays-npe",
         "prompt": "This `totalSeconds` forgot to skip empty slots. Slot 2 of the road-trip playlist is empty.",
         "files": {"Song.java": SONG, "Playlist.java": PLAYLIST_NO_CHECK, "PlaylistTester.java": PL_TESTER},
         "run": "PlaylistTester", "expect": "runtime",
         "question": "What does `Cannot invoke \"Song.getSeconds()\" because \"this.songs[<local2>]\" is null` tell you?",
         "choices": ["The `songs` array was never created",
                     "The program tried to call `getSeconds()` on a slot of the array that holds no `Song`",
                     "`getSeconds` is spelled wrong",
                     "The playlist has too many songs"],
         "answer": 1,
         "explain": "Java names the exact expression that was `null`: one slot of `this.songs`. The method call that failed was `getSeconds()`. The fix is to check the slot before using it.",
         "fix": [["Playlist.java", "            total = total + songs[i].getSeconds();\n",
                  "            if (songs[i] != null) {\n                total = total + songs[i].getSeconds();\n            }\n"]]},
        {"type": "p", "text": "Two things in that message are worth knowing:"},
        {"type": "list", "items": [
            "**Follow the `at` lines to your own code.** Read from the top: `totalSeconds` crashed on line 15 of `Playlist.java`. It was called by `toString` (line 28), which Java's own `println` called, which `main` called on line 8. Lines starting with `java.base/` are inside Java's library. Skip past them to the files you wrote.",
            "**`<local2>` is the loop variable `i`.** By default, `javac` doesn't store the names of local variables in the `.class` file, so Java can only number them. Compile with `javac -g` to keep the names, and the same crash reads `this.songs[i]`:",
        ]},
        {"type": "terminal", "files": {"Song.java": SONG, "Playlist.java": PLAYLIST_NO_CHECK, "PlaylistTester.java": PL_TESTER},
         "commands": ["javac -g Song.java Playlist.java PlaylistTester.java", "java PlaylistTester"],
         "codes": [0, 1]},
        {"type": "p", "text": "Messages that name the `null` expression arrived in Java 14. On older versions you'd see only `java.lang.NullPointerException` and the line number."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "arrays-find", "title": "Find a song by title",
         "prompt": "Add a `find` method to `Playlist`. It returns the song with the given title, or `null` if there isn't one. Check the slot before you use it.",
         "files": {"Song.java": SONG, "Playlist.java": PLAYLIST.replace("""    @Override
    public String toString() {""", """    public Song find(String title) {
        for (int i = 0; i < songs.length; i++) {
            if (songs[i] [[check]] null && songs[i].getTitle().[[same]](title)) {
                return songs[i];
            }
        }
        return [[none]];
    }

    @Override
    public String toString() {"""), "FindTester.java": """public class FindTester {
    public static void main(String[] args) {
        Playlist roadTrip = new Playlist(4);
        roadTrip.set(0, new Song("Blue Hour", "The Lanterns", 214));
        roadTrip.set(2, new Song("Low Tide", "Mira Holt", 187));

        System.out.println(roadTrip.find("Low Tide"));
        System.out.println(roadTrip.find("Thunder Road"));
    }
}
"""},
         "run": "FindTester", "output": "Low Tide by Mira Holt\nnull",
         "blanks": {
             "check": {"accept": ["!="], "hint": "Only look inside slots that hold a song.",
                       "wrong": [{"answer": "==", "why": "This reverses the check. For the empty slot 1, `songs[1] == null` is true, so Java goes on to call `getTitle()` on `null` and crashes. (`<local2>` is the loop variable `i`, as explained above.)"}]},
             "same": {"accept": ["equals"], "hint": "Strings are compared with a method, not with `==`.",
                      "wrong": [{"answer": "equal", "why": "The `String` method is `equals`, with an s."}]},
             "none": {"accept": ["null"], "hint": "What does \"no song\" look like?",
                      "wrong": [{"answer": "-1", "why": "The method promises to return a `Song`, and `-1` is an `int`. For objects, \"nothing found\" is `null`."},
                                {"answer": "\"\"", "why": "`\"\"` is an empty `String`, not a `Song`. For \"no object\", return `null`."}]},
         },
         "explain": "`&&` stops as soon as its left side is false. So when a slot is empty, `songs[i] != null` is false and Java never calls `getTitle()` on it. That's why the null check must come first."},
        {"type": "note", "label": "Why equals and not ==",
         "text": "For objects, `==` asks \"are these the same object in memory?\". `equals` asks \"do these strings contain the same characters?\". Two separate `String` objects can hold the same text, so always compare strings with `equals`."},
        {"type": "quiz", "id": "arrays-how-many-objects",
         "question": "After `Song[] list = new Song[5];` runs, how many `Song` objects exist?",
         "choices": ["5", "1", "0", "It depends on the Song constructor"],
         "answer": 2,
         "explain": "`new Song[5]` creates an array with 5 empty slots, each holding `null`. No `Song` constructor runs until you write `new Song(...)` for a slot."},
    ],
    "sources": [ARRAYS_TUT, FOR_TUT, JLS_ARRAY_CREATE, NPE, JEP358, STRING_EQUALS, HEL_3_3, HEL_4_2],
}
