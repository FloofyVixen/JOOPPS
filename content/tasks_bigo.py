"""Write-it-yourself tasks for unit 15, big O. Compiled and run by build.py."""
from tasks_classes import task

NO_LOOPS = r"^(?![\s\S]*\b(for|while)\b)"
NOT_NESTED = r"^(?![\s\S]*\bfor\b[^}]*\{[^}]*\bfor\b)"

CODE = [
    task("w-bigo-sorted-dups", "Duplicates in O(n)",
         "In a **sorted** array, equal values sit next to each other, so you only need to compare neighbours. Write `Dups` with `public static boolean hasDuplicate(int[] sorted)` that runs in O(n): one loop, no nested loop. `DupsTester` (a separate file) prints the result for `{1, 3, 3, 7}` and `{2, 4, 6}`.",
         {"Dups.java": """public class Dups {
    public static boolean hasDuplicate(int[] sorted) {
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i] == sorted[i - 1]) {
                return true;
            }
        }
        return false;
    }
}
""", "DupsTester.java": """public class DupsTester {
    public static void main(String[] args) {
        System.out.println(Dups.hasDuplicate(new int[] {1, 3, 3, 7}));
        System.out.println(Dups.hasDuplicate(new int[] {2, 4, 6}));
    }
}
"""}, "DupsTester", "true\nfalse",
         tests={"CheckDups.java": """public class CheckDups {
    public static void main(String[] args) {
        System.out.println(Dups.hasDuplicate(new int[] {}) + " " + Dups.hasDuplicate(new int[] {5})
                + " " + Dups.hasDuplicate(new int[] {-2, -2}) + " " + Dups.hasDuplicate(new int[] {1, 2, 3, 4, 4}));
    }
}
"""}, tests_run="CheckDups", tests_output="false false true true",
         checks=[{"pattern": NOT_NESTED, "file": "Dups.java", "message": "`Dups.java` has no loop inside a loop, so it's O(n)."}],
         hints=["Start at `i = 1` and compare `sorted[i]` with `sorted[i - 1]`, so you never read past either end."]),

    task("w-bigo-stepcounter", "Count the steps yourself",
         "Write `StepCounter` with three methods that return how many times their innermost line runs for a given `n`: `linear(int n)` (one loop to `n`), `quadratic(int n)` (two nested loops to `n`) and `logarithmic(int n)` (halve `n` until it reaches 1). All return `long`. `main` prints the three counts for `n = 8` on one line, separated by spaces.",
         {"StepCounter.java": """public class StepCounter {
    public static long linear(int n) {
        long steps = 0;
        for (int i = 0; i < n; i++) {
            steps++;
        }
        return steps;
    }

    public static long quadratic(int n) {
        long steps = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                steps++;
            }
        }
        return steps;
    }

    public static long logarithmic(int n) {
        long steps = 0;
        while (n > 1) {
            n = n / 2;
            steps++;
        }
        return steps;
    }

    public static void main(String[] args) {
        System.out.println(linear(8) + " " + quadratic(8) + " " + logarithmic(8));
    }
}
"""}, "StepCounter", "8 64 3",
         tests={"CheckSteps.java": """public class CheckSteps {
    public static void main(String[] args) {
        System.out.println(StepCounter.linear(1024) + " " + StepCounter.quadratic(1024) + " " + StepCounter.logarithmic(1024));
        System.out.println(StepCounter.linear(1) + " " + StepCounter.quadratic(1) + " " + StepCounter.logarithmic(1));
    }
}
"""}, tests_run="CheckSteps", tests_output="1024 1048576 10\n1 1 0"),
]

WRITE = [
    task("w-bigo-constant", "Write O(1) methods",
         "Write `Constant` with two O(1) methods, **with no loops at all**: `lastValue(int[] data)` returns the last value, and `sumTo(int n)` returns 1 + 2 + … + n as a `long`, using the formula n(n + 1)/2. Put `main` in a separate `ConstantTester`, which prints `lastValue` of `{7, 2, 9}` and `sumTo(10)` and `sumTo(100000)`.",
         {"Constant.java": """public class Constant {
    public static int lastValue(int[] data) {
        return data[data.length - 1];
    }

    public static long sumTo(int n) {
        return (long) n * (n + 1) / 2;
    }
}
""", "ConstantTester.java": """public class ConstantTester {
    public static void main(String[] args) {
        System.out.println(Constant.lastValue(new int[] {7, 2, 9}));
        System.out.println(Constant.sumTo(10));
        System.out.println(Constant.sumTo(100000));
    }
}
"""}, "ConstantTester", "9\n55\n5000050000",
         checks=[{"pattern": NO_LOOPS, "file": "Constant.java", "message": "`Constant.java` has no `for` or `while` loops, so both methods are O(1)."}],
         hints=["`100000 * 100001` is too big for an `int`. Cast to `long` before multiplying: `(long) n * (n + 1) / 2`."]),

    task("w-bigo-linear", "Write an O(n) method",
         "Write `Linear` with `public static boolean isSorted(int[] data)`, which returns `true` if every value is at least the one before it. Use one loop: O(n). `LinearTester` prints the result for `{1, 2, 2, 5}`, `{3, 1, 4}` and an empty array.",
         {"Linear.java": """public class Linear {
    public static boolean isSorted(int[] data) {
        for (int i = 1; i < data.length; i++) {
            if (data[i] < data[i - 1]) {
                return false;
            }
        }
        return true;
    }
}
""", "LinearTester.java": """public class LinearTester {
    public static void main(String[] args) {
        System.out.println(Linear.isSorted(new int[] {1, 2, 2, 5}));
        System.out.println(Linear.isSorted(new int[] {3, 1, 4}));
        System.out.println(Linear.isSorted(new int[] {}));
    }
}
"""}, "LinearTester", "true\nfalse\ntrue",
         tests={"CheckLinear.java": """public class CheckLinear {
    public static void main(String[] args) {
        System.out.println(Linear.isSorted(new int[] {9}) + " " + Linear.isSorted(new int[] {1, 2, 3, 0}));
    }
}
"""}, tests_run="CheckLinear", tests_output="true false",
         checks=[{"pattern": NOT_NESTED, "file": "Linear.java", "message": "`Linear.java` has no loop inside a loop."}]),

    task("w-bigo-quadratic", "Write an O(n²) method",
         "Write `Quadratic` with `public static int countInversions(int[] data)`: the number of pairs `i < j` where `data[i] > data[j]`. (A sorted array has 0; a reversed one has the most.) Use nested loops. `QuadraticTester` prints it for `{2, 4, 1, 3}` and `{5, 4, 3, 2, 1}`.",
         {"Quadratic.java": """public class Quadratic {
    public static int countInversions(int[] data) {
        int count = 0;
        for (int i = 0; i < data.length; i++) {
            for (int j = i + 1; j < data.length; j++) {
                if (data[i] > data[j]) {
                    count++;
                }
            }
        }
        return count;
    }
}
""", "QuadraticTester.java": """public class QuadraticTester {
    public static void main(String[] args) {
        System.out.println(Quadratic.countInversions(new int[] {2, 4, 1, 3}));
        System.out.println(Quadratic.countInversions(new int[] {5, 4, 3, 2, 1}));
    }
}
"""}, "QuadraticTester", "3\n10",
         tests={"CheckInv.java": """public class CheckInv {
    public static void main(String[] args) {
        System.out.println(Quadratic.countInversions(new int[] {1, 2, 3}) + " " + Quadratic.countInversions(new int[] {3, 3, 1}));
    }
}
"""}, tests_run="CheckInv", tests_output="0 2",
         hints=["Start `j` at `i + 1` so each pair is checked once, and in the right order.", "In `{2, 4, 1, 3}` the inversions are (2, 1), (4, 1) and (4, 3)."]),
]

TASKS = {"bigo-code": CODE, "bigo-write": WRITE}
