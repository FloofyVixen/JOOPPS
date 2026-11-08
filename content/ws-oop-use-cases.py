from sources import ACCESS_TUT, NAMING, HEL_4_1
from wshelp import step, guided, workshop, task

PRIVATE = {"pattern": r"private\s+\w+\s+\w+\s*;", "message": "Make the fields `private`."}

GYM1 = """public class Membership {
    private String name;
    private int visitsLeft;

    public Membership(String name, int visitsLeft) {
        this.name = name;
        this.visitsLeft = visitsLeft;
    }

    public String getName() {
        return name;
    }

    public int getVisitsLeft() {
        return visitsLeft;
    }
}
"""
CHECKIN = """
    public boolean checkIn() {
        if (visitsLeft > 0) {
            visitsLeft = visitsLeft - 1;
            return true;
        }
        return false;
    }
"""
RENEW = """
    public void renew(int visits) {
        if (visits > 0) {
            visitsLeft = visitsLeft + visits;
        } else {
            System.out.println("Visits must be positive.");
        }
    }
"""
GYM2 = GYM1[:-2] + CHECKIN + "}\n"
GYM3 = GYM1[:-2] + CHECKIN + RENEW + "}\n"
GT1 = """public class GymTester {
    public static void main(String[] args) {
        Membership ana = new Membership("Ana", 10);
        System.out.println(ana.getName() + ": " + ana.getVisitsLeft() + " visits left");
    }
}
"""
GT2 = """public class GymTester {
    public static void main(String[] args) {
        Membership ana = new Membership("Ana", 2);
        System.out.println(ana.checkIn());
        System.out.println(ana.checkIn());
        System.out.println(ana.checkIn());
        System.out.println(ana.getVisitsLeft());
    }
}
"""
GT3 = GT2.replace("""        System.out.println(ana.getVisitsLeft());
""", """        System.out.println(ana.getVisitsLeft());
        ana.renew(-5);
        ana.renew(5);
        System.out.println(ana.getVisitsLeft());
""")

ELEV1 = """public class Elevator {
    private int floor;
    private int topFloor;

    public Elevator(int topFloor) {
        this.topFloor = topFloor;
        floor = 1;
    }

    public int getFloor() {
        return floor;
    }

    public int getTopFloor() {
        return topFloor;
    }
}
"""
MOVETO = """
    public void moveTo(int target) {
        if (target >= 1 && target <= topFloor) {
            floor = target;
        } else {
            System.out.println("No floor " + target + ".");
        }
    }
"""
UPDOWN = """
    public void goUp() {
        moveTo(floor + 1);
    }

    public void goDown() {
        moveTo(floor - 1);
    }
"""
ELEV2 = ELEV1[:-2] + MOVETO + "}\n"
ELEV3 = ELEV1[:-2] + MOVETO + UPDOWN + "}\n"
ET1 = """public class LiftTester {
    public static void main(String[] args) {
        Elevator lift = new Elevator(10);
        System.out.println("Floor " + lift.getFloor() + " of " + lift.getTopFloor());
    }
}
"""
ET2 = """public class LiftTester {
    public static void main(String[] args) {
        Elevator lift = new Elevator(10);
        lift.moveTo(7);
        lift.moveTo(12);
        System.out.println("Floor " + lift.getFloor());
    }
}
"""
ET3 = """public class LiftTester {
    public static void main(String[] args) {
        Elevator lift = new Elevator(10);
        lift.moveTo(10);
        lift.goUp();
        lift.goDown();
        System.out.println("Floor " + lift.getFloor());
        Elevator small = new Elevator(2);
        small.goDown();
        System.out.println("Floor " + small.getFloor());
    }
}
"""

LESSON = workshop(
    "ws-oop-use-cases", "Workshop: encapsulation",
    "Practice private fields, getters, and methods that refuse values that make no sense.",
    ["Write classes whose fields can only change through their own methods",
     "Return `true`/`false` to report whether an action worked",
     "Reuse one checking method from several others"],
    guided("ws-u4-gym", "A gym membership", "Build a `Membership` that can't be checked into once it runs out.", [
        step("Private fields", "Create `Membership.java` with private `name` and `visitsLeft`, a constructor that takes both, and getters. Print the member from `GymTester`.",
             {"Membership.java": GYM1, "GymTester.java": GT1}, "GymTester", "Ana: 10 visits left", checks=[PRIVATE]),
        step("Checking in", "Add `checkIn()`: if there are visits left, use one and return `true`; otherwise return `false` and change nothing.",
             {"Membership.java": GYM2, "GymTester.java": GT2}, "GymTester", "true\ntrue\nfalse\n0",
             hint="Return `true` inside the `if`, after subtracting, and `false` after it."),
        step("Renewing", "Add `renew(int visits)`, which adds visits only when the number is positive; otherwise it prints `Visits must be positive.`",
             {"Membership.java": GYM3, "GymTester.java": GT3}, "GymTester",
             "true\ntrue\nfalse\n0\nVisits must be positive.\n5"),
    ]),
    guided("ws-u4-lift", "An elevator", "Build an `Elevator` that can't be sent to a floor that doesn't exist.", [
        step("The elevator", "Create `Elevator.java` with private `floor` and `topFloor`. The constructor takes the top floor, and every elevator starts on floor 1. Add getters for both.",
             {"Elevator.java": ELEV1, "LiftTester.java": ET1}, "LiftTester", "Floor 1 of 10", checks=[PRIVATE]),
        step("Moving", "Add `moveTo(int target)`. Floors 1 to the top floor are allowed; anything else prints `No floor <target>.` and the elevator stays put.",
             {"Elevator.java": ELEV2, "LiftTester.java": ET2}, "LiftTester", "No floor 12.\nFloor 7"),
        step("Up and down", "Add `goUp()` and `goDown()`. Don't repeat the floor check: have them call `moveTo` with the next floor, so the rule lives in one place.",
             {"Elevator.java": ELEV3, "LiftTester.java": ET3}, "LiftTester", "No floor 11.\nFloor 9\nNo floor 0.\nFloor 1",
             hint="`goUp()` is one line: `moveTo(floor + 1);`",
             checks=[{"pattern": r"moveTo\s*\(\s*floor\s*\+\s*1\s*\)", "message": "Have `goUp()` call `moveTo(floor + 1)`."}]),
    ]),
    task("ws-u4-password", "A password that must be long enough",
         "Write `UserAccount` with private `username` and `password`. The constructor takes only the username, so the password starts as `null`. `setPassword(String)` accepts passwords of at least 8 characters and returns whether it worked. `checkPassword(String attempt)` returns `true` only if a password is set and the attempt matches.",
         {"UserAccount.java": """public class UserAccount {
    private String username;
    private String password;

    public UserAccount(String username) {
        this.username = username;
    }

    public String getUsername() {
        return username;
    }

    public boolean setPassword(String newPassword) {
        if (newPassword.length() >= 8) {
            password = newPassword;
            return true;
        }
        return false;
    }

    public boolean checkPassword(String attempt) {
        return password != null && password.equals(attempt);
    }
}
""", "LoginTester.java": """public class LoginTester {
    public static void main(String[] args) {
        UserAccount ana = new UserAccount("ana");
        System.out.println(ana.setPassword("short"));
        System.out.println(ana.setPassword("correcthorse"));
        System.out.println(ana.checkPassword("wrong"));
        System.out.println(ana.checkPassword("correcthorse"));
    }
}
"""}, "LoginTester", "false\ntrue\nfalse\ntrue",
         tests={"CheckLogin.java": """public class CheckLogin {
    public static void main(String[] args) {
        UserAccount fresh = new UserAccount("x");
        System.out.println(fresh.checkPassword("anything"));
        System.out.println(fresh.setPassword("abcdefgh"));
        System.out.println(fresh.checkPassword("abcdefgh"));
    }
}
"""}, tests_run="CheckLogin", tests_output="false\ntrue\ntrue",
         hints=["`text.length()` gives the number of characters in a `String`.",
                "Check `password != null` before calling `equals` on it, with `&&`."],
         checks=[PRIVATE]),
    task("ws-u4-battery", "A battery that stays between 0 and 100",
         "Write `Battery` with a private `charge` that starts at 100. `use(int amount)` lowers it but never below 0; `recharge(int amount)` raises it but never above 100; both ignore negative amounts. Add `getCharge()` and `isLow()`, which is `true` below 20.",
         {"Battery.java": """public class Battery {
    private int charge;

    public Battery() {
        charge = 100;
    }

    public int getCharge() {
        return charge;
    }

    public void use(int amount) {
        if (amount > 0) {
            charge = charge - amount;
            if (charge < 0) {
                charge = 0;
            }
        }
    }

    public void recharge(int amount) {
        if (amount > 0) {
            charge = charge + amount;
            if (charge > 100) {
                charge = 100;
            }
        }
    }

    public boolean isLow() {
        return charge < 20;
    }
}
""", "BatteryTester.java": """public class BatteryTester {
    public static void main(String[] args) {
        Battery phone = new Battery();
        phone.use(85);
        System.out.println(phone.getCharge() + " low: " + phone.isLow());
        phone.recharge(500);
        System.out.println(phone.getCharge());
        phone.use(150);
        System.out.println(phone.getCharge());
    }
}
"""}, "BatteryTester", "15 low: true\n100\n0",
         tests={"CheckBattery.java": """public class CheckBattery {
    public static void main(String[] args) {
        Battery b = new Battery();
        b.use(-10);
        b.recharge(-5);
        System.out.println(b.getCharge());
        b.use(80);
        System.out.println(b.getCharge() + " " + b.isLow());
    }
}
"""}, tests_run="CheckBattery", tests_output="100\n20 false",
         hints=["After changing the charge, fix it up if it went past a limit.", "Exactly 20 is not low."],
         checks=[PRIVATE]),
    [ACCESS_TUT, NAMING, HEL_4_1],
)
