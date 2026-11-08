from sources import OBJECT_TOSTRING, OBJECT_TUT, OVERRIDE_TUT, HEL_4_1

SONG_NO_TS = """public class Song {
    public String title;
    public String artist;
    public int seconds;

    public Song(String title, String artist, int seconds) {
        this.title = title;
        this.artist = artist;
        this.seconds = seconds;
    }
}
"""

TESTER = """public class SongTester {
    public static void main(String[] args) {
        Song first = new Song("Blue Hour", "The Lanterns", 214);
        System.out.println(first);
    }
}
"""

SONG_TS = """public class Song {
    public String title;
    public String artist;
    public int seconds;

    public Song(String title, String artist, int seconds) {
        this.title = title;
        this.artist = artist;
        this.seconds = seconds;
    }

    @Override
    public String toString() {
        return title + " by " + artist + " (" + seconds + "s)";
    }
}
"""

TESTER2 = """public class SongTester {
    public static void main(String[] args) {
        Song first = new Song("Blue Hour", "The Lanterns", 214);
        Song second = new Song("Low Tide", "Mira Holt", 187);

        System.out.println(first);
        System.out.println("Up next: " + second);

        String label = first.toString();
        System.out.println(label.length() + " characters");
    }
}
"""

LESSON = {
    "id": "classes-tostring",
    "title": "toString: printing objects",
    "summary": "Teach your class how to describe itself as text, so `println` shows something useful.",
    "goals": [
        "Explain the odd text `println` shows for an object without `toString`",
        "Write a `toString` method that returns a description",
        "Know that `toString` returns text and doesn't print it",
    ],
    "cos225": "COS 225 homework often asks you to \"implement a toString() method\" with an exact format, and checks your program's output line by line. Getting `toString` right is usually what makes that output match.",
    "blocks": [
        {"type": "h", "text": "Printing an object"},
        {"type": "code", "files": {"Song.java": SONG_NO_TS, "SongTester.java": TESTER}, "run": "SongTester",
         "after": "Your output will show different characters after the `@`. They change from run to run."},
        {"type": "p", "text": "Every Java class automatically comes with a `toString` method, inherited from Java's built-in `Object` class. You'll learn exactly how that works in the inheritance units. The built-in version returns the class name, an `@`, and a number in hexadecimal. That's rarely what you want to see."},

        {"type": "h", "text": "Writing your own toString"},
        {"type": "p", "text": "To replace it, write a method with exactly this header: `public String toString()`. It must **return** a `String`. `println` calls it for you whenever you print the object, and so does `+` when you join an object to text."},
        {"type": "code", "files": {"Song.java": SONG_TS, "SongTester.java": TESTER2}, "run": "SongTester"},
        {"type": "list", "items": [
            "`@Override` tells the compiler \"this replaces an inherited method\". It's optional, but if you misspell the method name, it turns a silent bug into a compile error.",
            "`\"Up next: \" + second` calls `second.toString()` automatically.",
            "You can also call `toString()` yourself. It's an ordinary method that returns a `String`.",
        ]},
        {"type": "note", "label": "Return, don't print",
         "text": "`toString` builds the text and hands it back. Whoever called it decides what to do with it, such as print it, store it, or join it to other text. Putting `System.out.println` inside `toString` is a common mistake."},
        {"type": "error", "id": "tostring-void",
         "prompt": "This `toString` prints instead of returning.",
         "files": {"Song.java": """public class Song {
    public String title;
    public String artist;

    public Song(String title, String artist) {
        this.title = title;
        this.artist = artist;
    }

    public void toString() {
        System.out.println(title + " by " + artist);
    }
}
""", "SongTester.java": """public class SongTester {
    public static void main(String[] args) {
        System.out.println(new Song("Blue Hour", "The Lanterns"));
    }
}
"""},
         "run": "SongTester", "expect": "compile",
         "question": "What does the message say is wrong?",
         "choices": ["`toString` must be `private`",
                     "The return type `void` doesn't match the inherited `toString`, which returns `String`",
                     "`println` can't be used inside a class",
                     "A class can't have both a constructor and `toString`"],
         "answer": 1,
         "explain": "To replace the inherited `toString`, your version must return a `String`. Change `void` to `String`, and change the `println` to a `return`.",
         "fix": [["Song.java", "public void toString() {\n        System.out.println(title + \" by \" + artist);",
                  "public String toString() {\n        return title + \" by \" + artist;"]],
         "fixed_output": "Blue Hour by The Lanterns"},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "tostring-recipe", "title": "Describe a recipe",
         "prompt": "Write `toString` so a `Recipe` prints as `Tomato soup (serves 4)`.",
         "files": {"Recipe.java": """public class Recipe {
    public String name;
    public int servings;

    public Recipe(String name, int servings) {
        this.name = name;
        this.servings = servings;
    }

    @Override
    public [[rtype]] toString() {
        [[kw]] name + " (serves " + [[field]] + ")";
    }
}
""", "RecipeTester.java": """public class RecipeTester {
    public static void main(String[] args) {
        Recipe soup = new Recipe("Tomato soup", 4);
        Recipe bread = new Recipe("Flatbread", 6);
        System.out.println(soup);
        System.out.println(bread);
    }
}
"""},
         "run": "RecipeTester", "output": "Tomato soup (serves 4)\nFlatbread (serves 6)",
         "blanks": {
             "rtype": {"accept": ["String"], "hint": "What type of value does `toString` hand back?",
                       "wrong": [{"answer": "void", "why": "The inherited `toString` returns a `String`, so yours must too. `@Override` makes the compiler point this out right away."},
                                 {"answer": "string", "why": "The type is `String`, with a capital S."}]},
             "kw": {"accept": ["return"], "hint": "Send the text back to the caller.",
                    "wrong": [{"answer": "System.out.println(", "why": "That would print instead of returning, and the parentheses wouldn't match. `toString` must `return` its text."}]},
             "field": {"accept": ["servings", "this.servings"], "hint": "Which field holds the number of servings?",
                       "wrong": [{"answer": "\"servings\"", "why": "In quotes, `\"servings\"` is the word itself, so every recipe would print \"(serves servings)\". Without quotes, it's the field's value."}]},
         },
         "explain": "`println(soup)` calls `soup.toString()`, which returns the text, and `println` prints it."},
        {"type": "quiz", "id": "tostring-when-called",
         "question": "`Song s = new Song(\"Low Tide\", \"Mira Holt\", 187);` Which line does not call `s.toString()`?",
         "choices": ["`System.out.println(s);`", "`String t = \"Song: \" + s;`", "`System.out.println(s.title);`", "`String u = s.toString();`"],
         "answer": 2,
         "explain": "`s.title` is already a `String` field, so it's printed directly. The other three need `s` as text: printing it, joining it with `+`, or calling the method yourself."},
    ],
    "sources": [OBJECT_TOSTRING, OBJECT_TUT, OVERRIDE_TUT, HEL_4_1],
}
