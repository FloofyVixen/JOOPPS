from sources import CLASSES_TUT, OBJECTS_TUT, FIELDS_TUT, DEV_CLASSES, HEL_4_1, JLS_DEFAULTS

SONG = """public class Song {
    public String title;
    public String artist;
    public int seconds;

    public void play() {
        System.out.println("Now playing: " + title + " by " + artist);
    }
}
"""

TESTER = """public class SongTester {
    public static void main(String[] args) {
        Song first = new Song();
        first.title = "Blue Hour";
        first.artist = "The Lanterns";
        first.seconds = 214;

        Song second = new Song();
        second.title = "Low Tide";
        second.artist = "Mira Holt";
        second.seconds = 187;

        first.play();
        second.play();
        System.out.println(first.title + " is " + first.seconds + " seconds long.");
    }
}
"""

DEFAULTS = """public class DefaultsTester {
    public static void main(String[] args) {
        Song empty = new Song();
        System.out.println(empty.title);
        System.out.println(empty.seconds);
    }
}
"""

LESSON = {
    "id": "classes-first-class",
    "title": "Your first class",
    "summary": "A class describes a kind of thing. An object is one of those things, made with `new`.",
    "goals": [
        "Write a class with fields (instance variables) and a method",
        "Create objects with `new` and use the dot to reach their fields and methods",
        "Explain why two objects of the same class don't share their values",
    ],
    "cos225": "This is the shape of the first COS 225 homework: one class with a few instance variables, plus a separate tester class whose `main` creates objects and prints them.",
    "blocks": [
        {"type": "h", "text": "Classes and objects"},
        {"type": "p", "text": "Until now, every program has been one class with one `main` method. Object-oriented programming adds your own types. A **class** is a blueprint: it says what information each object holds and what each object can do. An **object** is one thing built from that blueprint."},
        {"type": "p", "text": "Think of a music app. `Song` is the class. \"Blue Hour\" and \"Low Tide\" are two `Song` objects. Each one has its own title, artist and length."},
        {"type": "code", "files": {"Song.java": SONG}, "show": False,
         "caption": "`Song.java`: this class has no `main`, so it isn't a program by itself. Other classes use it."},
        {"type": "list", "items": [
            "`title`, `artist` and `seconds` are **fields**, also called **instance variables**. Each object gets its own copy.",
            "`play()` is a method with no `static`. It belongs to an object, so it can use that object's fields directly.",
            "The fields are `public` for now so the tester can set them. In \"OOP: Basics and Use cases\" you'll see why most classes make them `private`.",
        ]},

        {"type": "h", "text": "Making objects with new"},
        {"type": "p", "text": "A second class, the **tester**, holds `main` and uses `Song`. Both files go in the same folder. `new Song()` builds a new object, and the variable `first` holds a reference to it. The dot `.` reaches into an object: `first.title` is the title field of the `first` object."},
        {"type": "code", "files": {"Song.java": SONG, "SongTester.java": TESTER}, "run": "SongTester",
         "caption": "Run `SongTester`, the class with `main`. Java compiles `Song.java` too, because the tester uses it."},
        {"type": "p", "text": "Calling `first.play()` runs `play` for the `first` object, so inside the method `title` means \"Blue Hour\". Calling `second.play()` runs the same code with the other object's fields."},

        {"type": "h", "text": "Fields you never set"},
        {"type": "p", "text": "A field that is never given a value isn't empty. Java fills it with a default: `0` for numbers, `false` for `boolean`, and `null` for objects such as `String`. `null` means \"no object\"."},
        {"type": "code", "files": {"Song.java": SONG, "DefaultsTester.java": DEFAULTS}, "run": "DefaultsTester"},
        {"type": "p", "text": "Seeing `null` or `0` in your output when you expected real data usually means a field never got set. You'll meet a common cause of this in the lesson on constructors."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "class-movie", "title": "Create and use an object",
         "prompt": "Finish the tester so it creates a `Movie`, sets both fields and calls `describe()`.",
         "files": {"Movie.java": """public class Movie {
    public String title;
    public int year;

    public void describe() {
        System.out.println(title + " (" + [[field]] + ")");
    }
}
""", "MovieTester.java": """public class MovieTester {
    public static void main(String[] args) {
        Movie pick = [[make]] Movie();
        pick.title = "Paper Moon Station";
        pick.[[set]] = 1998;
        pick.describe();
    }
}
"""},
         "run": "MovieTester", "output": "Paper Moon Station (1998)",
         "blanks": {
             "field": {"accept": ["year", "this.year"], "hint": "Inside the class, use the field's name.",
                       "wrong": [{"answer": "Year", "why": "Field names are case-sensitive. The field is `year`, lowercase."},
                                 {"answer": "pick.year", "why": "`pick` is a variable in the tester's `main`. `Movie` can't see it. Inside its own methods, a class uses its fields by name."}]},
             "make": {"accept": ["new"], "hint": "Which keyword builds a new object?",
                      "wrong": [{"answer": "", "why": "Without `new`, Java thinks `Movie()` is a call to a method named `Movie`, and there isn't one."}]},
             "set": {"accept": ["year"], "hint": "Which field holds 1998?",
                     "wrong": [{"answer": "title", "why": "`title` is a `String`, and `1998` without quotes is an `int`."}]},
         },
         "explain": "`new Movie()` builds the object, `pick.year = 1998` sets one of its fields, and `pick.describe()` runs the method using that object's values."},
        {"type": "quiz", "id": "class-how-many",
         "question": "How many `Song` objects does this code create? `Song a = new Song(); Song b = new Song(); Song c = a;`",
         "choices": ["1", "2", "3", "0"],
         "answer": 1,
         "explain": "Only `new` creates an object, and it appears twice. `Song c = a;` doesn't copy anything. It makes `c` refer to the same object as `a`."},
        {"type": "quiz", "id": "class-vs-object",
         "question": "Which sentence is correct?",
         "choices": ["A class is one specific song; an object is the general idea of a song",
                     "A class describes what every song has; an object is one particular song",
                     "Classes and objects are two names for the same thing",
                     "Every class must contain a `main` method"],
         "answer": 1,
         "explain": "The class is the blueprint, and objects are built from it. Only the class you run needs a `main` method; `Song` has none."},
    ],
    "sources": [CLASSES_TUT, FIELDS_TUT, OBJECTS_TUT, DEV_CLASSES, HEL_4_1, JLS_DEFAULTS],
}
