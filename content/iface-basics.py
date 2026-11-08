from sources import IFACE_TUT, IFACE_DEF_TUT, IFACE_IMPL_TUT, DEFAULT_METHODS_TUT, JLS_IFACES, HEL_9_2

PLAYABLE = """public interface Playable {
    void play();
}
"""
SONG = """public class Song implements Playable {
    private String title;

    public Song(String title) {
        this.title = title;
    }

    @Override
    public void play() {
        System.out.println("Playing song: " + title);
    }
}
"""
PODCAST = """public class Podcast implements Playable {
    private String show;
    private int episode;

    public Podcast(String show, int episode) {
        this.show = show;
        this.episode = episode;
    }

    @Override
    public void play() {
        System.out.println("Playing " + show + ", episode " + episode);
    }
}
"""
TESTER = """public class PlayTester {
    public static void main(String[] args) {
        Song song = new Song("Blue Hour");
        Podcast pod = new Podcast("Night Shift", 12);
        song.play();
        pod.play();
    }
}
"""
SWITCH = """public interface Switchable {
    void turnOn();

    void turnOff();
}
"""

LESSON = {
    "id": "iface-basics",
    "title": "What an interface is",
    "summary": "An interface lists methods a class promises to have. Any class that implements it must provide every one.",
    "goals": [
        "Declare an interface and implement it in a class with `implements`",
        "Explain why every interface method must be implemented, and `public`",
        "Explain why you can't create an object of an interface",
    ],
    "cos225": "The exam guide describes an interface as a \"fully abstract alternative to Class\": no non-abstract methods, and only static data, which COS 225 doesn't use. A class must implement all of an interface's methods. This lesson follows that definition.",
    "blocks": [
        {"type": "h", "text": "A promise, not a class"},
        {"type": "p", "text": "Songs and podcasts are very different things, but a music app needs to `play()` both. An **interface** names that shared ability. It lists method headers with no bodies: what a class can do, not how. A class that `implements` the interface promises to provide a body for each one."},
        {"type": "code", "files": {"Playable.java": PLAYABLE, "Song.java": SONG, "Podcast.java": PODCAST, "PlayTester.java": TESTER},
         "run": "PlayTester"},
        {"type": "list", "items": [
            "`public interface Playable` goes in its own file, `Playable.java`, just like a class.",
            "`void play();` has no body, only a semicolon. Methods in an interface are automatically `public` and `abstract`, so you don't write those words.",
            "`implements Playable` makes the promise. `@Override` works here too, and catches typos the same way it does with inheritance.",
            "`Song` and `Podcast` share no code and no parent class (other than `Object`). They share only the promise to `play()`.",
        ]},
        {"type": "note", "label": "Interfaces in this course",
         "text": "Since Java 8, interfaces may also contain `default` and `static` methods with bodies. COS 225 treats interfaces as fully abstract, so this course does too: every method in our interfaces is a header that the class fills in. Interfaces can also hold constants, which are automatically `public static final`."},

        {"type": "h", "text": "What the compiler checks"},
        {"type": "p", "text": "**Every method must be implemented.** If a class leaves one out, it doesn't compile, and the message names the missing method."},
        {"type": "error", "id": "iface-missing",
         "prompt": "This `Audiobook` claims to be `Playable` but has no `play()`.",
         "files": {"Playable.java": PLAYABLE, "Audiobook.java": """public class Audiobook implements Playable {
    private String title;

    public Audiobook(String title) {
        this.title = title;
    }
}
""", "BookTester.java": """public class BookTester {
    public static void main(String[] args) {
        new Audiobook("Night Trains").play();
    }
}
"""},
         "run": "BookTester", "expect": "compile",
         "question": "How do you fix it?",
         "choices": ["Remove `play()` from the interface",
                     "Add a `public void play()` method to `Audiobook`",
                     "Change `implements` to `extends`",
                     "Create the audiobook with `new Playable()` instead"],
         "answer": 1,
         "explain": "`implements Playable` is a promise to have `play()`, and the compiler holds the class to it.",
         "fix": [["Audiobook.java", "        this.title = title;\n    }\n}\n",
                  "        this.title = title;\n    }\n\n    @Override\n    public void play() {\n        System.out.println(\"Playing audiobook: \" + title);\n    }\n}\n"]],
         "fixed_output": "Playing audiobook: Night Trains"},
        {"type": "p", "text": "**The implementing method must be `public`.** The interface's methods are public, and a class can't make a promised method harder to reach:"},
        {"type": "code", "files": {"Playable.java": PLAYABLE, "Song.java": SONG.replace("    public void play()", "    void play()"),
                                   "PlayTester.java": TESTER.replace("        Podcast pod = new Podcast(\"Night Shift\", 12);\n", "").replace("        pod.play();\n", "")},
         "run": "PlayTester", "expect": "compile",
         "after": "\"weaker access privileges\": the interface method is `public`, but the class's version (with no access word) isn't. Add `public`."},
        {"type": "p", "text": "**You can't create an object of an interface.** An interface has no method bodies, so there would be nothing to run:"},
        {"type": "code", "files": {"Playable.java": PLAYABLE, "MakePlayable.java": """public class MakePlayable {
    public static void main(String[] args) {
        Playable p = new Playable();
    }
}
"""}, "run": "MakePlayable", "expect": "compile"},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "iface-lamp", "title": "Keep the promise",
         "prompt": "`Switchable` has two methods. Make `Lamp` implement it.",
         "files": {"Switchable.java": SWITCH, "Lamp.java": """public class Lamp [[impl]] Switchable {
    private boolean on;

    @Override
    [[acc]] void turnOn() {
        on = true;
        System.out.println("Lamp on");
    }

    @Override
    public void [[second]]() {
        on = false;
        System.out.println("Lamp off");
    }
}
""", "LampTester.java": """public class LampTester {
    public static void main(String[] args) {
        Lamp desk = new Lamp();
        desk.turnOn();
        desk.turnOff();
    }
}
"""},
         "run": "LampTester", "output": "Lamp on\nLamp off",
         "blanks": {
             "impl": {"accept": ["implements"], "hint": "A class keeps an interface's promise with which keyword?",
                      "wrong": [{"answer": "extends", "why": "A class `extends` another class, but `implements` an interface. Java says \"no interface expected here\"."}]},
             "acc": {"accept": ["public"], "hint": "Interface methods are always public.",
                     "wrong": [{"answer": "", "why": "Without `public`, the method has weaker access than the interface's version, which is always public."},
                               {"answer": "private", "why": "A private method can't keep a public promise. Interface methods must be implemented as `public`."}]},
             "second": {"accept": ["turnOff"], "hint": "Which other method does `Switchable` list?",
                        "wrong": [{"answer": "turnoff", "why": "Names are case-sensitive. `turnoff` doesn't match `turnOff`, so the promise isn't kept and `@Override` complains as well."}]},
         },
         "explain": "Both methods from `Switchable` are implemented, and both are `public`."},
        {"type": "quiz", "id": "iface-contains",
         "question": "Using COS 225's definition, which of these belongs in an interface?",
         "choices": ["`private int brightness;`", "`void dim(int amount);`",
                     "`public Lamp() { }`", "`void dim(int amount) { brightness = amount; }`"],
         "answer": 1,
         "explain": "An interface lists method headers ending in a semicolon. It has no instance fields, no constructors, and (in COS 225's fully abstract style) no method bodies."},
        {"type": "quiz", "id": "iface-new",
         "question": "`Playable p = new Song(\"Low Tide\");` Is this allowed?",
         "choices": ["No, a variable can't have an interface type",
                     "Yes: `p` can hold any object whose class implements `Playable`",
                     "Only if `Song` extends `Playable`",
                     "Only inside the `Playable` interface"],
         "answer": 1,
         "explain": "You can't write `new Playable()`, but you can use `Playable` as a variable type for any object that implements it. The \"Using an interface as a type\" lesson builds on this."},
    ],
    "sources": [IFACE_TUT, IFACE_DEF_TUT, IFACE_IMPL_TUT, DEFAULT_METHODS_TUT, JLS_IFACES, HEL_9_2],
}
