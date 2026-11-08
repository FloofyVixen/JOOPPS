from sources import CLASSES_TUT, CONSTRUCTORS_TUT, ARRAYS_TUT, OBJECT_TOSTRING, HEL_4_2

CAR = """public class Car {
    private String plate;
    private String model;

    public Car(String plate, String model) {
        this.plate = plate;
        this.model = model;
    }

    @Override
    public String toString() {
        return model + " (" + plate + ")";
    }
}
"""

CAR_BLANKS = """public class Car {
    private String plate;
    private String model;

    public Car(String plate, String model) {
        [[self]].plate = plate;
        this.model = model;
    }

    @Override
    public [[rtype]] toString() {
        return model + " (" + plate + ")";
    }
}
"""

CAR_TESTER = """public class CarTester {
    public static void main(String[] args) {
        Car first = new Car("ME-4411", "Civic");
        Car second = new Car("NH-2090", "Outback");
        System.out.println(first);
        System.out.println(second);
    }
}
"""

# ---- ParkingLot pieces, each with a blank version and a finished version ----

HEAD = """public class ParkingLot {
    private Car[] spots;
    private String name;

    public ParkingLot(String name) {
        this.name = name;
        spots = new Car[6];
    }

    public String getName() {
        return name;
    }
"""

HEAD_BLANKS = """public class ParkingLot {
    private [[ftype]] spots;
    private String name;

    public ParkingLot(String name) {
        this.name = name;
        spots = [[arr]];
    }

    public String getName() {
        return name;
    }
"""

PARK = """
    public int park(Car car) {
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] == null) {
                spots[i] = car;
                return i;
            }
        }
        return -1;
    }
"""

PARK_BLANKS = """
    public int park(Car car) {
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] [[empty]] null) {
                spots[i] = [[what]];
                return i;
            }
        }
        return [[full]];
    }
"""

LEAVE = """
    public Car leave(int spot) {
        if (spot < 0 || spot >= spots.length) {
            return null;
        }
        Car gone = spots[spot];
        spots[spot] = null;
        return gone;
    }
"""

LEAVE_BLANKS = """
    public Car leave(int spot) {
        if (spot < 0 || spot >= [[len]]) {
            return null;
        }
        Car gone = spots[spot];
        spots[spot] = [[clear]];
        return [[back]];
    }
"""

TOSTRING = """
    @Override
    public String toString() {
        int parked = 0;
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] != null) {
                parked++;
            }
        }
        return "" + parked;
    }
}
"""

TOSTRING_BLANKS = """
    @Override
    public String toString() {
        int parked = 0;
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] != null) {
                parked++;
            }
        }
        return [[ret]];
    }
}
"""

LOT_FINAL = HEAD + PARK + LEAVE + TOSTRING

STEP2_TESTER = """public class ParkingLotTester {
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot("Elm Street Garage");
        System.out.println(lot.getName());
        System.out.println(lot);
    }
}
"""

STEP3_TESTER = """public class ParkingLotTester {
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot("Elm Street Garage");
        for (int i = 1; i <= 7; i++) {
            int spot = lot.park(new Car("ME-10" + i, "Civic"));
            System.out.println("Car " + i + " got spot " + spot);
        }
        System.out.println(lot);
    }
}
"""

STEP4_TESTER = """public class ParkingLotTester {
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot("Elm Street Garage");
        lot.park(new Car("ME-4411", "Civic"));
        lot.park(new Car("NH-2090", "Outback"));
        lot.park(new Car("VT-3302", "Corolla"));

        System.out.println("Left: " + lot.leave(1));
        System.out.println("Left again: " + lot.leave(1));
        System.out.println("Spot 9: " + lot.leave(9));
        System.out.println(lot);
    }
}
"""

FINAL_TESTER = """public class ParkingLotTester {
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot("Elm Street Garage");
        System.out.println(lot.getName());
        System.out.println(lot);

        for (int i = 1; i <= 5; i++) {
            lot.park(new Car("ME-10" + i, "Civic"));
        }
        System.out.println(lot);

        lot.leave(1);
        lot.leave(3);
        System.out.println(lot);

        int spot = lot.park(new Car("NH-2090", "Outback"));
        System.out.println("Outback got spot " + spot);
        System.out.println(lot);
    }
}
"""

LOT_WITH_FIND = LOT_FINAL.replace("""
    @Override
    public String toString() {""", """
    public int findPlate(String plate) {
        for (int i = 0; i < spots.length; i++) {
            if (spots[i] != null && spots[i].getPlate().equals(plate)) {
                return i;
            }
        }
        return -1;
    }

    @Override
    public String toString() {""")

CAR_WITH_GETTER = CAR.replace("""
    @Override""", """
    public String getPlate() {
        return plate;
    }

    @Override""")

FIND_TESTER = """public class FindTester {
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot("Elm Street Garage");
        lot.park(new Car("ME-4411", "Civic"));
        lot.park(new Car("NH-2090", "Outback"));

        System.out.println(lot.findPlate("NH-2090"));
        System.out.println(lot.findPlate("ZZ-0000"));
    }
}
"""

LESSON = {
    "id": "classes-project-parking",
    "title": "Project: a parking lot",
    "summary": "Put the OOP units together: a manager class that parks cars in a fixed number of spots, frees spots, and counts what's parked.",
    "goals": [
        "Build a class that manages a fixed-size array of other objects",
        "Place an object in the first empty slot, and report when there's no room",
        "Remove an object by slot number and hand it back",
        "Check a program's output line by line against what's expected",
    ],
    "cos225": "This project has the same structure as the COS 225 assignment where you plant trees in a grove: a fixed-size array, an add method that uses the first open spot and returns -1 when full, a remove method by index, and a `toString` that returns a count. Work through this project first, then write your assignment from scratch without looking back.",
    "blocks": [
        {"type": "h", "text": "The specification"},
        {"type": "p", "text": "Assignments usually arrive as a written spec. Here's this project's, in the same style:"},
        {"type": "list", "items": [
            "**Car**: two private fields, a license plate and a model, both `String`. A parameterized constructor sets both. `toString` returns the model followed by the plate in parentheses, like `Civic (ME-4411)`.",
            "**ParkingLot**: private fields for an array of 6 `Car` spots and the lot's name. A constructor takes the name and creates the array. Methods: `getName()`; `park(Car)` puts the car in the first empty spot and returns that spot's number, or -1 if the lot is full; `leave(int)` removes and returns the car in that spot, or returns `null` if the number is out of range; `toString` returns the number of parked cars.",
            "**ParkingLotTester**: a `main` that creates a lot, parks and removes cars, and prints the lot after each change.",
        ]},
        {"type": "p", "text": "You'll build it in four steps. Each step adds one piece and runs a small tester, so you always know the code so far works."},

        {"type": "h", "text": "Step 1: the Car class"},
        {"type": "blanks", "id": "parking-car", "title": "Write Car",
         "prompt": "Store the plate in its field, and give `toString` its return type.",
         "files": {"Car.java": CAR_BLANKS, "CarTester.java": CAR_TESTER},
         "run": "CarTester", "output": "Civic (ME-4411)\nOutback (NH-2090)",
         "blanks": {
             "self": {"accept": ["this"], "hint": "The parameter and the field are both named `plate`.",
                      "wrong": [{"answer": "Car", "why": "`Car.plate` would mean a field shared by the whole class. Each car has its own plate, so use `this`."}]},
             "rtype": {"accept": ["String"], "hint": "`toString` always hands back the same type.",
                       "wrong": [{"answer": "void", "why": "The inherited `toString` returns `String`, so yours must too."}]},
         },
         "explain": "Every `Car` now knows its own plate and model, and prints itself in the format the spec asks for."},

        {"type": "h", "text": "Step 2: the lot and its count"},
        {"type": "p", "text": "Start `ParkingLot` with its fields, constructor and `toString`. The constructor has to create the array, because a field of array type starts as `null`. `toString` counts the spots that aren't empty."},
        {"type": "blanks", "id": "parking-lot-ctor", "title": "Create the array and count",
         "prompt": "Declare the array field, create it with 6 spots, and return the count as a `String`.",
         "files": {"Car.java": CAR, "ParkingLot.java": HEAD_BLANKS + TOSTRING_BLANKS, "ParkingLotTester.java": STEP2_TESTER},
         "run": "ParkingLotTester", "output": "Elm Street Garage\n0",
         "blanks": {
             "ftype": {"accept": ["Car[]"], "hint": "An array of cars.",
                       "wrong": [{"answer": "Car", "why": "`Car` is one car. The square brackets in `Car[]` make it an array of cars. Without them, the array you create can't be stored in the field, and `spots.length` and `spots[i]` stop making sense."}]},
             "arr": {"accept": ["new Car[6]"], "hint": "`new`, the type, and the size in square brackets.",
                     "wrong": [{"answer": "new Car(6)", "why": "Parentheses call a `Car` constructor, which would try to build one car from the number 6. Square brackets create an array: `new Car[6]`."},
                               {"answer": "Car[6]", "why": "Without `new`, Java reads `Car[6]` as \"slot 6 of a variable named `Car`\", and there's no such variable. Creating an array always needs `new`."}]},
             "ret": {"accept": ["\"\" + parked", "String.valueOf(parked)", "Integer.toString(parked)"],
                     "hint": "`parked` is an `int`, but `toString` must return a `String`.",
                     "wrong": [{"answer": "parked", "why": "`parked` is an `int`, and `toString` promises a `String`. Joining it to an empty string, `\"\" + parked`, turns the number into text."}]},
         },
         "explain": "A brand-new lot has 6 empty spots, so the count is 0. `\"\" + parked` is a common shortcut for turning a number into a `String`; `String.valueOf(parked)` does the same thing more explicitly."},

        {"type": "h", "text": "Step 3: parking a car"},
        {"type": "p", "text": "`park` walks through the spots in order. At the first empty one, it stores the car and returns that spot's number right away. If the loop finishes without finding a gap, every spot is taken, so it returns -1. The spec uses -1 because it can never be a real spot number."},
        {"type": "blanks", "id": "parking-park", "title": "Write park",
         "prompt": "The tester tries to park 7 cars in a lot with 6 spots. The last one should get -1.",
         "files": {"Car.java": CAR, "ParkingLot.java": HEAD + PARK_BLANKS + TOSTRING, "ParkingLotTester.java": STEP3_TESTER},
         "run": "ParkingLotTester",
         "output": "Car 1 got spot 0\nCar 2 got spot 1\nCar 3 got spot 2\nCar 4 got spot 3\nCar 5 got spot 4\nCar 6 got spot 5\nCar 7 got spot -1\n6",
         "blanks": {
             "empty": {"accept": ["=="], "hint": "You're looking for a spot that has no car in it.",
                       "wrong": [{"answer": "!=", "why": "This looks for spots that already have a car. In a new lot there are none, so no car is ever parked: every call returns -1 and the count stays 0."},
                                 {"answer": "=", "why": "One `=` assigns. Here it would store `null` in the spot instead of comparing, and an `if` needs a `true`/`false` value."}]},
             "what": {"accept": ["car"], "hint": "Store the parameter that was passed in.",
                      "wrong": [{"answer": "Car", "why": "`Car` is the class name. The car to park is the parameter named `car`, lowercase."},
                                {"answer": "new Car()", "why": "That would try to build a new, blank car, and `Car` has no constructor without parameters. The car to park is already in the parameter `car`."}]},
             "full": {"accept": ["-1"], "hint": "The spec says what to return when the lot is full.",
                      "wrong": [{"answer": "0", "why": "0 is a real spot number, so the caller couldn't tell \"you got spot 0\" from \"the lot is full\". Look at the last \"got spot\" line."}]},
         },
         "explain": "`return i;` inside the loop is what stops the car from being parked in every empty spot. The method ends at the first one it finds."},

        {"type": "h", "text": "Step 4: leaving"},
        {"type": "p", "text": "`leave` first rejects spot numbers that don't exist, which would otherwise crash with `ArrayIndexOutOfBoundsException`. Then it saves the car in a variable before emptying the spot, so it can still hand that car back."},
        {"type": "blanks", "id": "parking-leave", "title": "Write leave",
         "prompt": "Check the range, empty the spot, and return the car that left.",
         "files": {"Car.java": CAR, "ParkingLot.java": HEAD + PARK + LEAVE_BLANKS + TOSTRING, "ParkingLotTester.java": STEP4_TESTER},
         "run": "ParkingLotTester",
         "output": "Left: Outback (NH-2090)\nLeft again: null\nSpot 9: null\n2",
         "blanks": {
             "len": {"accept": ["spots.length"], "hint": "The number of spots in the array.",
                     "wrong": [{"answer": "spots.length()", "why": "For arrays, `length` is a field, so there are no parentheses. (`String` is the one with a `length()` method.)"},
                               {"answer": "spots.size()", "why": "Arrays have no `size()` method. That's for `ArrayList`, which you'll meet later. Use `spots.length`."}]},
             "clear": {"accept": ["null"], "hint": "What does an empty spot hold?",
                       "wrong": [{"answer": "0", "why": "The array holds `Car` references, not numbers. An empty slot is `null`."}]},
             "back": {"accept": ["gone"], "hint": "You saved the car before emptying its spot.",
                      "wrong": [{"answer": "spots[spot]", "why": "The spot was set to `null` on the line before, so this returns `null` instead of the car. That's why the car is saved in `gone` first."}]},
         },
         "explain": "The second `leave(1)` returns `null` because spot 1 is already empty, and `leave(9)` returns `null` because there is no spot 9. Neither one crashes."},

        {"type": "h", "text": "Step 5: check the whole program"},
        {"type": "p", "text": "Here's the finished `ParkingLot`, followed by the full tester. Before you look at the output, work it out on paper. Assignments are usually graded by comparing your output with the expected output line by line."},
        {"type": "code", "files": {"Car.java": CAR, "ParkingLot.java": LOT_FINAL}, "hide": ["Car.java"],
         "show": False, "caption": "`ParkingLot.java`, finished"},
        {"type": "predict", "id": "parking-final",
         "prompt": "What does the full tester print?",
         "files": {"Car.java": CAR, "ParkingLot.java": LOT_FINAL, "ParkingLotTester.java": FINAL_TESTER},
         "run": "ParkingLotTester",
         "choices": ["Elm Street Garage\n0\n5\n3\nOutback got spot 5\n4",
                     "Elm Street Garage\n0\n5\n3\nOutback got spot 1\n4",
                     "Elm Street Garage\n0\n5\n5\nOutback got spot 5\n6",
                     "Elm Street Garage\n6\n5\n3\nOutback got spot 1\n4"],
         "answer": 1,
         "explain": "Five Civics fill spots 0 to 4. Leaving 1 and 3 drops the count to 3. `park` takes the **first** empty spot, which is 1, not the end of the lot. One more car makes 4."},

        {"type": "h", "text": "Going further"},
        {"type": "p", "text": "Try this on your own before opening the solution: add `findPlate(String plate)`, which returns the spot number of the car with that plate, or -1. You'll need a getter for the plate in `Car`, and the same null-check-first pattern from the arrays lesson."},
        {"type": "code", "files": {"Car.java": CAR_WITH_GETTER, "ParkingLot.java": LOT_WITH_FIND, "FindTester.java": FIND_TESTER},
         "run": "FindTester", "collapsed": True, "output": "1\n-1",
         "caption": "One possible solution"},
    ],
    "sources": [CLASSES_TUT, CONSTRUCTORS_TUT, ARRAYS_TUT, OBJECT_TOSTRING, HEL_4_2],
}
