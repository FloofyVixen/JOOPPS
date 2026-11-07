from sources import CONSTRUCTORS_TUT, THIS_TUT, JLS_DEFAULT_CTOR, HEL_4_1, HEL_5_2

SONG = """public class Song {
    public String title;
    public String artist;
    public int seconds;

    public Song(String title, String artist, int seconds) {
        this.title = title;
        this.artist = artist;
        this.seconds = seconds;
    }

    public void play() {
        System.out.println("Now playing: " + title + " by " + artist);
    }
}
"""

TESTER = """public class SongTester {
    public static void main(String[] args) {
        Song first = new Song("Blue Hour", "The Lanterns", 214);
        Song second = new Song("Low Tide", "Mira Holt", 187);

        first.play();
        second.play();
    }
}
"""

SONG2 = """public class Song {
    public String title;
    public String artist;
    public int seconds;

    public Song() {
        title = "Untitled";
        artist = "Unknown artist";
        seconds = 0;
    }

    public Song(String title, String artist, int seconds) {
        this.title = title;
        this.artist = artist;
        this.seconds = seconds;
    }

    public void play() {
        System.out.println("Now playing: " + title + " by " + artist);
    }
}
"""

TESTER2 = """public class SongTester {
    public static void main(String[] args) {
        Song draft = new Song();
        Song finished = new Song("Blue Hour", "The Lanterns", 214);

        draft.play();
        finished.play();
    }
}
"""

BUGGY_SONG = """public class Song {
    public String title;
    public String artist;
    public int seconds;

    public Song(String title, String artist, int seconds) {
        title = title;
        artist = artist;
        seconds = seconds;
    }

    public void play() {
        System.out.println("Now playing: " + title + " by " + artist);
    }
}
"""

LESSON = {
    "id": "classes-constructors",
    "title": "Constructors and this",
    "summary": "A constructor sets up a new object the moment it's created, so it never starts out half-finished.",
    "goals": [
        "Write a constructor that takes parameters and stores them in fields",
        "Use `this` when a parameter has the same name as a field",
        "Give a class both a default constructor and a parameterized one",
    ],
    "cos225": "COS 225 assignments regularly ask for a \"default constructor\" (no parameters, sensible starting values) and a \"parameterized constructor\" (values passed in). This lesson writes both.",
    "blocks": [
        {"type": "h", "text": "Setting fields one at a time is fragile"},
        {"type": "p", "text": "In the last lesson the tester set every field by hand after `new Song()`. Forget one line and the object quietly has a `null` title. A **constructor** fixes this. It's a special method that runs automatically when `new` creates the object, and it can require the values the object needs."},
        {"type": "code", "files": {"Song.java": SONG, "SongTester.java": TESTER}, "run": "SongTester"},
        {"type": "list", "items": [
            "A constructor has the **same name as the class** and **no return type**, not even `void`.",
            "Its parameters are the values you pass in the parentheses after `new Song`.",
            "The constructor's job is to copy those values into the object's fields.",
        ]},

        {"type": "h", "text": "What this means"},
        {"type": "snippet", "code": "        this.title = title;"},
        {"type": "p", "text": "The parameter and the field are both called `title`. Inside the constructor, the plain name `title` means the parameter, because the closest declaration wins. `this` means \"the object being built\", so `this.title` is the field. The line copies the parameter into the field."},
        {"type": "predict", "id": "ctor-missing-this",
         "prompt": "Someone left out `this`. What does the tester print now?",
         "files": {"Song.java": BUGGY_SONG, "SongTester.java": TESTER}, "run": "SongTester",
         "choices": ["Now playing: Blue Hour by The Lanterns\nNow playing: Low Tide by Mira Holt",
                     "Now playing: null by null\nNow playing: null by null",
                     "Now playing: title by artist\nNow playing: title by artist",
                     "Now playing:  by \nNow playing:  by "],
         "answer": 1,
         "explain": "`title = title;` copies the parameter into itself, so the field is never touched and keeps its default, `null`. The program compiles and runs without complaint, which makes this bug hard to spot. If you see `null` where you expected data, check your constructor for missing `this.`."},

        {"type": "h", "text": "Default and parameterized constructors"},
        {"type": "p", "text": "A class can have more than one constructor, as long as their parameter lists differ. This is called **overloading**. Java picks the one that matches the values you pass. A constructor with no parameters is often called the **default constructor**: it fills in sensible starting values."},
        {"type": "code", "files": {"Song.java": SONG2, "SongTester.java": TESTER2}, "run": "SongTester"},
        {"type": "note", "label": "Where the default goes missing",
         "text": "If you write no constructor at all, Java quietly gives your class an empty one, which is why `new Song()` worked in the last lesson. Once you write any constructor, Java stops providing it. If you still want `new Song()` to work, write the no-parameter constructor yourself."},
        {"type": "error", "id": "ctor-no-default",
         "prompt": "This `Song` has only the three-parameter constructor. The tester tries to make an empty song.",
         "files": {"Song.java": SONG, "SongTester.java": """public class SongTester {
    public static void main(String[] args) {
        Song draft = new Song();
        draft.play();
    }
}
"""},
         "run": "SongTester", "expect": "compile",
         "question": "What does \"actual and formal argument lists differ in length\" mean here?",
         "choices": ["The song title is too long",
                     "You passed 0 values, but the only constructor needs 3",
                     "`Song.java` and `SongTester.java` have different numbers of lines",
                     "`play()` needs an argument"],
         "answer": 1,
         "explain": "\"Formal\" arguments are the ones the constructor declares (`String, String, int`). \"Actual\" arguments are the ones you passed (none). One fix is to pass the three values. The other is to add a no-parameter constructor to `Song`.",
         "fix": [["SongTester.java", "new Song()", "new Song(\"Draft\", \"Me\", 0)"]],
         "fixed_output": "Now playing: Draft by Me"},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "ctor-recipe", "title": "Write both constructors",
         "prompt": "`Recipe` needs a default constructor (name \"Untitled\", 1 serving) and a parameterized one.",
         "files": {"Recipe.java": """public class Recipe {
    public String name;
    public int servings;

    public Recipe() {
        name = "Untitled";
        servings = [[defServ]];
    }

    public [[ctorName]](String name, int servings) {
        [[self]].name = name;
        this.servings = servings;
    }
}
""", "RecipeTester.java": """public class RecipeTester {
    public static void main(String[] args) {
        Recipe blank = new Recipe();
        Recipe soup = new Recipe("Tomato soup", 4);

        System.out.println(blank.name + ", serves " + blank.servings);
        System.out.println(soup.name + ", serves " + soup.servings);
    }
}
"""},
         "run": "RecipeTester", "output": "Untitled, serves 1\nTomato soup, serves 4",
         "blanks": {
             "defServ": {"accept": ["1"], "hint": "The default is 1 serving."},
             "ctorName": {"accept": ["Recipe"], "hint": "A constructor is named after its class, with no return type.",
                          "wrong": [{"answer": "void Recipe", "why": "With `void`, this is an ordinary method that happens to be named `Recipe`, not a constructor. So the class has no constructor taking a `String` and an `int`, and `new Recipe(\"Tomato soup\", 4)` fails. Constructors never have a return type."},
                                    {"answer": "recipe", "why": "The constructor's name must match the class name exactly, including the capital R. Java treats `recipe(...)` as a method that's missing its return type."}]},
             "self": {"accept": ["this"], "hint": "How do you refer to the object being built?",
                      "wrong": [{"answer": "Recipe", "why": "`Recipe.name` would mean a field shared by the whole class (a `static` field). `name` belongs to each object, so use `this`."}]},
         },
         "explain": "`new Recipe()` runs the first constructor and `new Recipe(\"Tomato soup\", 4)` runs the second, because Java matches the arguments to the parameter lists."},
        {"type": "quiz", "id": "ctor-return-type",
         "question": "Which line correctly starts a constructor for a class named `Lamp`?",
         "choices": ["`public void Lamp() {`", "`public Lamp() {`", "`public lamp() {`", "`public Lamp Lamp() {`"],
         "answer": 1,
         "explain": "A constructor has the class's exact name and no return type. The other choices are methods (or invalid code), so `new Lamp()` would not run them."},
    ],
    "sources": [CONSTRUCTORS_TUT, THIS_TUT, JLS_DEFAULT_CTOR, HEL_4_1, HEL_5_2],
}
