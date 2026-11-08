from sources import IFACE_IMPL_TUT, SUBCLASSES_TUT, JLS_IFACES, HEL_9_2

DEVICE = """public class Device {
    private String name;

    public Device(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
"""
MUSIC = """public interface MusicPlayer {
    void playMusic(String song);
}
"""
ALARM = """public interface Alarm {
    void setAlarm(int hour);
}
"""
SPEAKER = """public class SmartSpeaker extends Device implements MusicPlayer, Alarm {
    public SmartSpeaker(String name) {
        super(name);
    }

    @Override
    public void playMusic(String song) {
        System.out.println(getName() + " plays " + song + ".");
    }

    @Override
    public void setAlarm(int hour) {
        System.out.println(getName() + " will ring at " + hour + ":00.");
    }
}
"""
TESTER = """public class SpeakerTester {
    public static void main(String[] args) {
        SmartSpeaker echo = new SmartSpeaker("Kitchen speaker");
        echo.playMusic("Low Tide");
        echo.setAlarm(7);
    }
}
"""

LESSON = {
    "id": "iface-multiple",
    "title": "extends versus implements",
    "summary": "A class can extend only one class, but it can implement as many interfaces as it needs, and do both at once.",
    "goals": [
        "Explain the difference between `extends` and `implements`",
        "Write a class that implements more than one interface",
        "Write a class that extends a class and implements interfaces at the same time",
    ],
    "cos225": "From the exam guide: \"A Class can only extend one other Class. A Class may implement multiple Interfaces, as long as it implements all of the abstract methods of each.\" Interfaces are \"useful for unifying many behaviors (or multiple methods) under one Class\". Know extends versus implements.",
    "blocks": [
        {"type": "h", "text": "One parent, many promises"},
        {"type": "p", "text": "A smart speaker **is a** device, so it extends `Device` and inherits its name. It can also play music and act as an alarm. Those are two separate abilities, described by two interfaces. List them after `implements`, separated by commas. `extends` comes first, then `implements`."},
        {"type": "code", "files": {"Device.java": DEVICE, "MusicPlayer.java": MUSIC, "Alarm.java": ALARM,
                                   "SmartSpeaker.java": SPEAKER, "SpeakerTester.java": TESTER}, "run": "SpeakerTester"},
        {"type": "list", "items": [
            "**`extends` a class**: inherit its fields, methods and constructor chain. One class only.",
            "**`implements` an interface**: promise to provide its methods. You inherit no code, so you write every body yourself. Any number of interfaces.",
            "A class that implements several interfaces must implement **every** method of **every** one.",
        ]},

        {"type": "h", "text": "Why not extend two classes?"},
        {"type": "p", "text": "If two parent classes both had a `charge()` method with different bodies, which one would the child inherit? Java avoids that question by allowing a single superclass. Interfaces have no bodies to clash, so a class can take on as many as it likes. Trying to extend two classes doesn't even parse:"},
        {"type": "code", "files": {"Device.java": DEVICE, "Gadget.java": """public class Gadget {
}
""", "Combo.java": """public class Combo extends Device, Gadget {
    public Combo() {
        super("Combo");
    }
}
"""}, "run": None, "expect": "compile",
         "after": "After `extends Device`, Java expects the class body (`{`) or `implements`, not a second class."},

        {"type": "h", "text": "Every method of every interface"},
        {"type": "error", "id": "imult-missing",
         "prompt": "This speaker forgot one of its promises.",
         "files": {"Device.java": DEVICE, "MusicPlayer.java": MUSIC, "Alarm.java": ALARM,
                   "SmartSpeaker.java": SPEAKER.replace("""
    @Override
    public void setAlarm(int hour) {
        System.out.println(getName() + " will ring at " + hour + ":00.");
    }
""", ""), "SpeakerTester.java": TESTER.replace("        echo.setAlarm(7);\n", "")},
         "run": "SpeakerTester", "expect": "compile",
         "question": "What's missing?",
         "choices": ["A second `extends`", "The `setAlarm(int)` method from `Alarm`", "A constructor in `Alarm`", "`playMusic` must be `static`"],
         "answer": 1,
         "explain": "The message names both the method and the interface it comes from: `setAlarm(int)` in `Alarm`.",
         "fix": [["SmartSpeaker.java", "        System.out.println(getName() + \" plays \" + song + \".\");\n    }\n}\n",
                  "        System.out.println(getName() + \" plays \" + song + \".\");\n    }\n\n    @Override\n    public void setAlarm(int hour) {\n        System.out.println(getName() + \" will ring at \" + hour + \":00.\");\n    }\n}\n"]]},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "imult-phone", "title": "Extend one, implement two",
         "prompt": "`Phone` is a `Device` that can also play music and set alarms.",
         "files": {"Device.java": DEVICE, "MusicPlayer.java": MUSIC, "Alarm.java": ALARM, "Phone.java": """public class Phone [[ext]] Device [[impl]] MusicPlayer[[sep]]Alarm {
    public Phone(String name) {
        super(name);
    }

    @Override
    public void playMusic(String song) {
        System.out.println(getName() + " streams " + song + ".");
    }

    @Override
    public void setAlarm(int hour) {
        System.out.println(getName() + " alarm set for " + hour + ":00.");
    }
}
""", "PhoneTester.java": """public class PhoneTester {
    public static void main(String[] args) {
        Phone pixel = new Phone("Pixel");
        pixel.playMusic("Northbound");
        pixel.setAlarm(6);
    }
}
"""},
         "run": "PhoneTester", "output": "Pixel streams Northbound.\nPixel alarm set for 6:00.",
         "blanks": {
             "ext": {"accept": ["extends"], "hint": "`Device` is a class.",
                     "wrong": [{"answer": "implements", "why": "`Device` is a class, so it's extended. You `implement` interfaces."}]},
             "impl": {"accept": ["implements"], "hint": "`MusicPlayer` and `Alarm` are interfaces.",
                      "wrong": [{"answer": "extends", "why": "A class can only `extends` once, and only a class. Interfaces come after `implements`."}]},
             "sep": {"accept": [","], "hint": "How are several interfaces separated?",
                     "wrong": [{"answer": "and", "why": "Java separates the interfaces with a comma: `implements MusicPlayer, Alarm`."},
                               {"answer": "&", "why": "Java separates the interfaces with a comma: `implements MusicPlayer, Alarm`."}]},
         },
         "explain": "`extends` comes first (one class), then `implements` with a comma-separated list of interfaces."},
        {"type": "quiz", "id": "imult-which",
         "question": "Which class header is valid?",
         "choices": ["`class A extends B, C`", "`class A implements X, Y, Z`",
                     "`class A implements X extends B`", "`class A extends X implements B, C` where `X` is an interface"],
         "answer": 1,
         "explain": "Any number of interfaces can follow `implements`. A class extends at most one class, `extends` must come before `implements`, and you can't `extends` an interface from a class."},
        {"type": "quiz", "id": "imult-inherit",
         "question": "What does a class get from an interface it implements (in COS 225's fully abstract style)?",
         "choices": ["The method bodies, ready to use", "Fields to store data in", "A list of methods it must write itself", "A constructor"],
         "answer": 2,
         "explain": "With `extends` you inherit working code. With `implements` you take on a list of method headers and provide every body yourself."},
    ],
    "sources": [IFACE_IMPL_TUT, SUBCLASSES_TUT, JLS_IFACES, HEL_9_2],
}
