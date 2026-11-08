from sources import ABSTRACT_TUT, POLY_TUT, SUPER_TUT, SUBCLASSES_TUT, HEL_9_3

VEHICLE = """public abstract class Vehicle {
    private String id;

    public Vehicle(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
    }

    public abstract double costFor(int km);

    @Override
    public String toString() {
        return id;
    }
}
"""
VEHICLE_BLANKS = """public [[abs]] class Vehicle {
    private String id;

    public Vehicle(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
    }

    public abstract [[rtype]] costFor(int km);

    @Override
    public String toString() {
        return id;
    }
}
"""
BIKE = """public class Bike extends Vehicle {
    public Bike(String id) {
        super(id);
    }

    @Override
    public double costFor(int km) {
        return 2 + 0.5 * km;
    }
}
"""
VAN = """public class Van extends Vehicle {
    public Van(String id) {
        super(id);
    }

    @Override
    public double costFor(int km) {
        return 10 + 1.5 * km;
    }
}
"""
VAN_BLANKS = """public class Van [[ext]] Vehicle {
    public Van(String id) {
        [[sup]];
    }

    @Override
    public double [[meth]](int km) {
        return 10 + 1.5 * km;
    }
}
"""
DRONE = """public class Drone extends Vehicle {
    public Drone(String id) {
        super(id);
    }

    @Override
    public double costFor(int km) {
        return 8 + 0.25 * km;
    }
}
"""
FLEET = """public class Fleet {
    private Vehicle[] vehicles;

    public Fleet(int size) {
        vehicles = new Vehicle[size];
    }

    public boolean add(Vehicle v) {
        for (int i = 0; i < vehicles.length; i++) {
            if (vehicles[i] == null) {
                vehicles[i] = v;
                return true;
            }
        }
        return false;
    }

    public void quote(int km) {
        for (Vehicle v : vehicles) {
            if (v != null) {
                System.out.println(v + ": $" + v.costFor(km));
            }
        }
    }
"""
FLEET_BLANKS = """public class Fleet {
    private [[arr]] vehicles;

    public Fleet(int size) {
        vehicles = new Vehicle[size];
    }

    public boolean add(Vehicle v) {
        for (int i = 0; i < vehicles.length; i++) {
            if (vehicles[i] == null) {
                vehicles[i] = v;
                return true;
            }
        }
        return false;
    }

    public void quote(int km) {
        for (Vehicle v : vehicles) {
            if (v != null) {
                System.out.println(v + ": $" + [[call]]);
            }
        }
    }
"""
CHEAPEST = """
    public Vehicle cheapestFor(int km) {
        Vehicle best = null;
        for (Vehicle v : vehicles) {
            if (v != null && (best == null || v.costFor(km) < best.costFor(km))) {
                best = v;
            }
        }
        return best;
    }
"""
END = "}\n"

T1 = """public class FleetTester {
    public static void main(String[] args) {
        Bike b = new Bike("B1");
        System.out.println(b + " costs $" + b.costFor(10) + " for 10 km");
    }
}
"""
T2 = """public class FleetTester {
    public static void main(String[] args) {
        Vehicle[] all = {new Bike("B1"), new Van("V1"), new Drone("D1")};
        for (Vehicle v : all) {
            System.out.println(v + ": $" + v.costFor(10));
        }
    }
}
"""
T3 = """public class FleetTester {
    public static void main(String[] args) {
        Fleet fleet = new Fleet(3);
        fleet.add(new Bike("B1"));
        fleet.add(new Van("V1"));
        fleet.add(new Drone("D1"));
        System.out.println(fleet.add(new Bike("B2")));
        fleet.quote(4);
    }
}
"""
T4 = """public class FleetTester {
    public static void main(String[] args) {
        Fleet fleet = new Fleet(4);
        fleet.add(new Bike("B1"));
        fleet.add(new Van("V1"));
        fleet.add(new Drone("D1"));
        System.out.println("2 km: " + fleet.cheapestFor(2));
        System.out.println("30 km: " + fleet.cheapestFor(30));
        System.out.println("Empty fleet: " + new Fleet(2).cheapestFor(5));
    }
}
"""

LESSON = {
    "id": "inh-project-fleet",
    "title": "Project: a delivery fleet",
    "summary": "Put the inheritance units together: an abstract `Vehicle`, three kinds of vehicle that price trips their own way, and a fleet that compares them without knowing which kind each one is.",
    "goals": [
        "Design an abstract superclass with one abstract method",
        "Write several subclasses that each implement it differently",
        "Write a manager class whose loops rely on polymorphism",
    ],
    "cos225": "This project combines what the exam guide groups under OOP: an abstract class, subclasses with `super(...)` and `@Override`, and polymorphism through an array of the superclass type. It's the same manager-class shape as the OOP units' projects, now holding a whole hierarchy.",
    "blocks": [
        {"type": "h", "text": "The specification"},
        {"type": "list", "items": [
            "**Vehicle** (abstract): a private `id`, a constructor that takes it, `getId()`, an abstract method `double costFor(int km)`, and a `toString` that returns the id.",
            "**Bike**: costs $2 plus $0.50 per km. **Van**: $10 plus $1.50 per km. **Drone**: $8 plus $0.25 per km.",
            "**Fleet**: a private `Vehicle[]` sized by its constructor; `add(Vehicle)` uses the first empty slot and returns `true`, or `false` when full; `quote(int km)` prints every vehicle's price; `cheapestFor(int km)` returns the cheapest vehicle for that distance, or `null` if the fleet is empty.",
        ]},

        {"type": "h", "text": "Step 1: the abstract Vehicle"},
        {"type": "blanks", "id": "fleet-vehicle", "title": "Write Vehicle",
         "prompt": "Make `Vehicle` abstract, and declare the abstract method's return type. `Bike` is already written.",
         "files": {"Vehicle.java": VEHICLE_BLANKS, "Bike.java": BIKE, "FleetTester.java": T1},
         "run": "FleetTester", "output": "B1 costs $7.0 for 10 km",
         "blanks": {
             "abs": {"accept": ["abstract"], "hint": "A class with an abstract method must be marked too.",
                     "wrong": [{"answer": "", "why": "`Vehicle` has an abstract method, so the class itself has to be `abstract`."}]},
             "rtype": {"accept": ["double"], "hint": "Prices like 7.0 have a decimal point.",
                       "wrong": [{"answer": "int", "why": "`Bike` overrides `costFor` with return type `double`. An override must return the same type as the method it replaces (or a subtype of it, for objects), so this doesn't compile."},
                                 {"answer": "void", "why": "The cost must be returned so the fleet can compare prices. `void` returns nothing, and `Bike`'s `double` version would no longer match."}]},
         },
         "explain": "`Vehicle` can't compute a cost by itself, but it guarantees that every vehicle can."},

        {"type": "h", "text": "Step 2: more kinds of vehicle"},
        {"type": "blanks", "id": "fleet-van", "title": "Write Van",
         "prompt": "Finish `Van`. `Drone` is written the same way. The tester stores all three kinds in one `Vehicle[]`.",
         "files": {"Vehicle.java": VEHICLE, "Bike.java": BIKE, "Van.java": VAN_BLANKS, "Drone.java": DRONE, "FleetTester.java": T2},
         "run": "FleetTester", "output": "B1: $7.0\nV1: $25.0\nD1: $10.5",
         "blanks": {
             "ext": {"accept": ["extends"], "hint": "A van is a vehicle.",
                     "wrong": [{"answer": "implements", "why": "`Vehicle` is a class (an abstract one), so a subclass `extends` it. `implements` is for interfaces."}]},
             "sup": {"accept": ["super(id)"], "hint": "`Vehicle` stores the id.",
                     "wrong": [{"answer": "this.id = id", "why": "`id` is private in `Vehicle`, so `Van` can't assign it. Pass it to `Vehicle`'s constructor with `super(id)`."}]},
             "meth": {"accept": ["costFor"], "hint": "Implement the abstract method, with exactly its name.",
                      "wrong": [{"answer": "cost", "why": "A method named `cost` is a new method, so `costFor` is still unimplemented and `@Override` reports that `cost` doesn't override anything."}]},
         },
         "explain": "The loop in the tester calls `costFor(10)` on each `Vehicle`, and each object uses its own formula."},

        {"type": "h", "text": "Step 3: the fleet"},
        {"type": "p", "text": "`Fleet` holds any mix of vehicles in one `Vehicle[]`. Its `quote` loop doesn't check what kind each one is. It calls `costFor`, and polymorphism does the rest."},
        {"type": "blanks", "id": "fleet-quote", "title": "Write Fleet",
         "prompt": "Declare the array field and complete the price in `quote`.",
         "files": {"Vehicle.java": VEHICLE, "Bike.java": BIKE, "Van.java": VAN, "Drone.java": DRONE,
                   "Fleet.java": FLEET_BLANKS + END, "FleetTester.java": T3},
         "run": "FleetTester", "output": "false\nB1: $4.0\nV1: $16.0\nD1: $9.0",
         "blanks": {
             "arr": {"accept": ["Vehicle[]"], "hint": "One array type that can hold bikes, vans and drones.",
                     "wrong": [{"answer": "Bike[]", "why": "A `Bike[]` can hold only bikes, so a `Vehicle[]` can't be stored in it. The superclass type is what lets one array hold every kind."},
                               {"answer": "Object[]", "why": "An `Object[]` could hold anything, so the for-each loop can't promise that each item is a `Vehicle`. That's why the error is on the loop line. Use the most specific type that covers every kind: `Vehicle[]`."}]},
             "call": {"accept": ["v.costFor(km)"], "hint": "Ask the vehicle for its price for `km` kilometres.",
                      "wrong": [{"answer": "costFor(km)", "why": "`Fleet` has no `costFor` method of its own. Call it on the vehicle: `v.costFor(km)`."},
                                {"answer": "v.costFor", "why": "A method call needs parentheses and its argument: `v.costFor(km)`."}]},
         },
         "explain": "The fleet has 3 slots, so the fourth `add` returns `false`."},

        {"type": "h", "text": "Step 4: the cheapest vehicle"},
        {"type": "p", "text": "`cheapestFor` uses the \"best so far\" pattern from the OOP wrap-up workshop, comparing each vehicle's own price."},
        {"type": "code", "files": {"Vehicle.java": VEHICLE, "Fleet.java": FLEET + CHEAPEST + END}, "hide": ["Vehicle.java"],
         "show": False, "caption": "`Fleet.java`, finished"},
        {"type": "predict", "id": "fleet-final",
         "prompt": "Which vehicle is cheapest for 2 km, and for 30 km?",
         "files": {"Vehicle.java": VEHICLE, "Bike.java": BIKE, "Van.java": VAN, "Drone.java": DRONE,
                   "Fleet.java": FLEET + CHEAPEST + END, "FleetTester.java": T4},
         "run": "FleetTester",
         "choices": ["2 km: B1\n30 km: B1\nEmpty fleet: null",
                     "2 km: B1\n30 km: D1\nEmpty fleet: null",
                     "2 km: D1\n30 km: D1\nEmpty fleet: null",
                     "2 km: B1\n30 km: D1\nEmpty fleet: B1"],
         "answer": 1,
         "explain": "For 2 km: bike $3.00, van $13.00, drone $8.50. For 30 km: bike $17.00, van $55.00, drone $15.50. The drone's low per-km rate wins on long trips. An empty fleet has no vehicles, so `best` stays `null`."},
    ],
    "sources": [ABSTRACT_TUT, SUPER_TUT, POLY_TUT, SUBCLASSES_TUT, HEL_9_3],
}
