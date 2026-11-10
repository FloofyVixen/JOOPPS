from sources import ALGS4_14, OPENDSA_ANAL
from wshelp import step, guided, workshop, task
from tasks_bigo import NOT_NESTED

PS1 = """public class PairSum {
    public static boolean slowHasPair(int[] sorted, int target) {
        for (int i = 0; i < sorted.length; i++) {
            for (int j = i + 1; j < sorted.length; j++) {
                if (sorted[i] + sorted[j] == target) {
                    return true;
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        int[] data = {1, 3, 4, 6, 9, 12};
        System.out.println(slowHasPair(data, 13));
        System.out.println(slowHasPair(data, 2));
    }
}
"""
PS2 = """public class PairSum {
    public static long checks = 0;

    public static boolean slowHasPair(int[] sorted, int target) {
        for (int i = 0; i < sorted.length; i++) {
            for (int j = i + 1; j < sorted.length; j++) {
                checks++;
                if (sorted[i] + sorted[j] == target) {
                    return true;
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        int[] big = new int[1000];
        for (int i = 0; i < big.length; i++) {
            big[i] = 2 * i;
        }
        System.out.println(slowHasPair(big, 1));
        System.out.println(checks + " checks");
    }
}
"""
PS3 = """public class PairSum {
    public static long checks = 0;

    public static boolean slowHasPair(int[] sorted, int target) {
        for (int i = 0; i < sorted.length; i++) {
            for (int j = i + 1; j < sorted.length; j++) {
                checks++;
                if (sorted[i] + sorted[j] == target) {
                    return true;
                }
            }
        }
        return false;
    }

    public static boolean fastHasPair(int[] sorted, int target) {
        int left = 0;
        int right = sorted.length - 1;
        while (left < right) {
            checks++;
            int sum = sorted[left] + sorted[right];
            if (sum == target) {
                return true;
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        int[] big = new int[1000];
        for (int i = 0; i < big.length; i++) {
            big[i] = 2 * i;
        }
        System.out.println(slowHasPair(big, 1) + " " + checks + " checks");
        checks = 0;
        System.out.println(fastHasPair(big, 1) + " " + checks + " checks");
        checks = 0;
        System.out.println(fastHasPair(big, 1990) + " " + checks + " checks");
    }
}
"""

SR1 = """public class Search {
    public static long steps = 0;

    public static int linearSearch(int[] data, int target) {
        for (int i = 0; i < data.length; i++) {
            steps++;
            if (data[i] == target) {
                return i;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] data = new int[1000];
        for (int i = 0; i < data.length; i++) {
            data[i] = 3 * i;
        }
        System.out.println(linearSearch(data, 2997) + " after " + steps + " steps");
    }
}
"""
SR2 = SR1.replace("""    public static void main""", """    public static int binarySearch(int[] sorted, int target) {
        int low = 0;
        int high = sorted.length - 1;
        while (low <= high) {
            steps++;
            int mid = (low + high) / 2;
            if (sorted[mid] == target) {
                return mid;
            } else if (sorted[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    public static void main""").replace("""        System.out.println(linearSearch(data, 2997) + " after " + steps + " steps");""", """        System.out.println(linearSearch(data, 2997) + " after " + steps + " steps");
        steps = 0;
        System.out.println(binarySearch(data, 2997) + " after " + steps + " steps");""")
SR3 = SR2.replace("""        int[] data = new int[1000];
        for (int i = 0; i < data.length; i++) {
            data[i] = 3 * i;
        }
        System.out.println(linearSearch(data, 2997) + " after " + steps + " steps");
        steps = 0;
        System.out.println(binarySearch(data, 2997) + " after " + steps + " steps");""", """        for (int n = 1000; n <= 1000000; n *= 10) {
            int[] data = new int[n];
            for (int i = 0; i < n; i++) {
                data[i] = 3 * i;
            }
            steps = 0;
            linearSearch(data, -1);
            long linear = steps;
            steps = 0;
            binarySearch(data, -1);
            System.out.println("n = " + n + ": linear " + linear + ", binary " + steps);
        }""")

LESSON = workshop(
    "ws-big-o", "Workshop: big O",
    "Measure the difference between growth rates for yourself: replace an O(n²) search with an O(n) one, and an O(n) search with an O(log n) one, counting the steps each takes.",
    ["Count an algorithm's steps to see its growth rate",
     "Replace a nested loop with a single pass when the data allows it",
     "Write methods that meet a required big O"],
    guided("ws-u15-pairs", "From O(n²) to O(n)", "Does a sorted array contain two values that add up to a target? Write the obvious nested-loop version, measure it, then write a single-pass version.", [
        step("Every pair", "In `PairSum`, write `slowHasPair(int[] sorted, int target)`, which checks every pair `i < j` with nested loops.",
             {"PairSum.java": PS1}, "PairSum", "true\nfalse"),
        step("Count the checks", "Add a `public static long checks` counter and increase it once per pair checked. Search a 1000-value array of even numbers for a pair adding to 1, which can't exist, so every pair is checked.",
             {"PairSum.java": PS2}, "PairSum", "false\n499500 checks",
             hint="1000 × 999 / 2 = 499,500: that's n(n − 1)/2, O(n²)."),
        step("Two pointers", "Write `fastHasPair`: start `left` at 0 and `right` at the end. If the pair sums to the target, you're done; if it's too small, move `left` right; if too big, move `right` left. Each step moves one pointer, so it's O(n). Count its checks too.",
             {"PairSum.java": PS3}, "PairSum", "false 499500 checks\nfalse 999 checks\ntrue 5 checks",
             hint="This only works because the array is sorted: moving `left` right always makes the sum bigger, and moving `right` left makes it smaller.",
             checks=[{"pattern": r"while\s*\(\s*left\s*<\s*right\s*\)", "message": "`fastHasPair` loops `while (left < right)`."}]),
    ]),
    guided("ws-u15-search", "From O(n) to O(log n)", "Finding a value in an array means checking values one by one, unless the array is sorted. Then you can halve the search each step.", [
        step("Linear search", "In `Search`, write `linearSearch(int[] data, int target)`, returning the index of `target` or -1, and count each comparison in `steps`. Search 1000 multiples of 3 for 2997, the last one.",
             {"Search.java": SR1}, "Search", "999 after 1000 steps"),
        step("Binary search", "Add `binarySearch` for sorted arrays: look at the middle of the range `low..high`; if the target is bigger, search the right half (`low = mid + 1`), otherwise the left half (`high = mid - 1`). Stop when `low > high`. Count each middle you look at.",
             {"Search.java": SR2}, "Search", "999 after 1000 steps\n999 after 10 steps"),
        step("Watch them grow", "Search arrays of 1000, 10,000, 100,000 and 1,000,000 values for -1, which isn't there, so both searches do their maximum work. Print the steps for each.",
             {"Search.java": SR3}, "Search",
             "n = 1000: linear 1000, binary 9\nn = 10000: linear 10000, binary 13\nn = 100000: linear 100000, binary 16\nn = 1000000: linear 1000000, binary 19",
             hint="Linear search grows ×10 each time. Binary search grows by only 3 or 4 steps, because multiplying `n` by 10 is a bit more than 3 doublings."),
    ]),
    task("ws-u15-range", "Largest difference in O(n)",
         "The largest difference between any two values in an array is just the maximum minus the minimum, so you don't need to compare pairs. Write `Spread` with `public static int maxDifference(int[] data)` (at least one value) that finds both in **one loop**. `SpreadTester` prints it for `{7, 2, 9, 4}` and `{-3, -8}`.",
         {"Spread.java": """public class Spread {
    public static int maxDifference(int[] data) {
        int min = data[0];
        int max = data[0];
        for (int i = 1; i < data.length; i++) {
            if (data[i] < min) {
                min = data[i];
            }
            if (data[i] > max) {
                max = data[i];
            }
        }
        return max - min;
    }
}
""", "SpreadTester.java": """public class SpreadTester {
    public static void main(String[] args) {
        System.out.println(Spread.maxDifference(new int[] {7, 2, 9, 4}));
        System.out.println(Spread.maxDifference(new int[] {-3, -8}));
    }
}
"""}, "SpreadTester", "7\n5",
         tests={"CheckSpread.java": """public class CheckSpread {
    public static void main(String[] args) {
        System.out.println(Spread.maxDifference(new int[] {4}) + " " + Spread.maxDifference(new int[] {1, 100, -100}));
    }
}
"""}, tests_run="CheckSpread", tests_output="0 200",
         checks=[{"pattern": NOT_NESTED, "file": "Spread.java", "message": "`Spread.java` has no loop inside a loop, so it's O(n)."}]),
    task("ws-u15-common", "Count common values two ways",
         "Write `Common` with two methods that count how many values of `a` also appear in `b` (each array has no repeats): `countSlow(int[] a, int[] b)` with nested loops (O(n²)), and `countSorted(int[] a, int[] b)` for **sorted** arrays in O(n), walking an index through each array: if `a[i] == b[j]` count it and advance both, otherwise advance the one with the smaller value. `CommonTester` prints both counts for `a = {1, 4, 6, 8, 10}` and `b = {2, 4, 5, 8, 11}`.",
         {"Common.java": """public class Common {
    public static int countSlow(int[] a, int[] b) {
        int count = 0;
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < b.length; j++) {
                if (a[i] == b[j]) {
                    count++;
                }
            }
        }
        return count;
    }

    public static int countSorted(int[] a, int[] b) {
        int count = 0;
        int i = 0;
        int j = 0;
        while (i < a.length && j < b.length) {
            if (a[i] == b[j]) {
                count++;
                i++;
                j++;
            } else if (a[i] < b[j]) {
                i++;
            } else {
                j++;
            }
        }
        return count;
    }
}
""", "CommonTester.java": """public class CommonTester {
    public static void main(String[] args) {
        int[] a = {1, 4, 6, 8, 10};
        int[] b = {2, 4, 5, 8, 11};
        System.out.println(Common.countSlow(a, b) + " " + Common.countSorted(a, b));
    }
}
"""}, "CommonTester", "2 2",
         tests={"CheckCommon.java": """public class CheckCommon {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = {3, 4};
        int[] e = {};
        System.out.println(Common.countSorted(a, b) + " " + Common.countSorted(a, e) + " " + Common.countSorted(a, a));
    }
}
"""}, tests_run="CheckCommon", tests_output="1 0 3",
         checks=[{"pattern": r"while\s*\(", "message": "`countSorted` walks both arrays with one `while` loop."}]),
    [ALGS4_14, OPENDSA_ANAL],
)
