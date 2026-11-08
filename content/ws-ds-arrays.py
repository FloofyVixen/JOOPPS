from sources import ALGS4_13, ARRAYS_API, MIT_ADT, GENERICS_TUT
from wshelp import step, guided, workshop, task

SL1 = """public class StringList {
    private String[] items;
    private int size;

    public StringList() {
        items = new String[2];
        size = 0;
    }

    public void add(String item) {
        items[size] = item;
        size++;
    }

    public String get(int index) {
        return items[index];
    }

    public int size() {
        return size;
    }
}
"""
SL2 = SL1.replace("""    public void add(String item) {
        items[size] = item;
        size++;
    }
""", """    public void add(String item) {
        if (size == items.length) {
            String[] bigger = new String[items.length * 2];
            for (int i = 0; i < size; i++) {
                bigger[i] = items[i];
            }
            items = bigger;
        }
        items[size] = item;
        size++;
    }
""")
SL3 = SL2.replace("""    public String get(int index) {
        return items[index];
    }
""", """    public String get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size);
        }
        return items[index];
    }
""")
REMOVE = """
    public String remove(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size);
        }
        String removed = items[index];
        for (int i = index; i < size - 1; i++) {
            items[i] = items[i + 1];
        }
        size--;
        items[size] = null;
        return removed;
    }
"""
SL4 = SL3[:-2] + REMOVE + "}\n"
T1 = """public class TodoTester {
    public static void main(String[] args) {
        StringList todo = new StringList();
        todo.add("wash dishes");
        todo.add("call Gran");
        System.out.println(todo.size() + ": " + todo.get(0) + ", " + todo.get(1));
    }
}
"""
T2 = """public class TodoTester {
    public static void main(String[] args) {
        StringList todo = new StringList();
        todo.add("wash dishes");
        todo.add("call Gran");
        todo.add("study Java");
        todo.add("water plants");
        for (int i = 0; i < todo.size(); i++) {
            System.out.println((i + 1) + ". " + todo.get(i));
        }
    }
}
"""
T3 = """public class TodoTester {
    public static void main(String[] args) {
        StringList todo = new StringList();
        todo.add("wash dishes");
        System.out.println(todo.get(0));
        System.out.println(todo.size());
    }
}
"""
T4 = """public class TodoTester {
    public static void main(String[] args) {
        StringList todo = new StringList();
        todo.add("wash dishes");
        todo.add("call Gran");
        todo.add("study Java");
        System.out.println("Done: " + todo.remove(0));
        for (int i = 0; i < todo.size(); i++) {
            System.out.println((i + 1) + ". " + todo.get(i));
        }
    }
}
"""

ARR1 = """import java.util.Arrays;

public class ArrayOps {
    public static void reverse(int[] data) {
        int left = 0;
        int right = data.length - 1;
        while (left < right) {
            int temp = data[left];
            data[left] = data[right];
            data[right] = temp;
            left++;
            right--;
        }
    }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4, 5};
        reverse(nums);
        System.out.println(Arrays.toString(nums));
    }
}
"""
ARR2 = ARR1.replace("""    public static void main""", """    public static void rotateLeft(int[] data) {
        if (data.length == 0) {
            return;
        }
        int first = data[0];
        for (int i = 0; i < data.length - 1; i++) {
            data[i] = data[i + 1];
        }
        data[data.length - 1] = first;
    }

    public static void main""").replace("""        reverse(nums);
        System.out.println(Arrays.toString(nums));""", """        reverse(nums);
        System.out.println(Arrays.toString(nums));
        rotateLeft(nums);
        System.out.println(Arrays.toString(nums));""")
ARR3 = ARR2.replace("""    public static void main""", """    public static int[] appended(int[] data, int value) {
        int[] result = Arrays.copyOf(data, data.length + 1);
        result[data.length] = value;
        return result;
    }

    public static void main""").replace("""        rotateLeft(nums);
        System.out.println(Arrays.toString(nums));""", """        rotateLeft(nums);
        System.out.println(Arrays.toString(nums));
        int[] longer = appended(nums, 99);
        System.out.println(Arrays.toString(longer) + " " + nums.length);""")

LESSON = workshop(
    "ws-ds-arrays", "Workshop: arrays as data structures",
    "Practice building a growable list from scratch and writing the array algorithms data structures depend on: reversing, rotating, shifting and copying.",
    ["Build a growable list with bounds checks and removal",
     "Write in-place array algorithms with two indexes",
     "Return a new array instead of changing the original"],
    guided("ws-u12-todo", "A growable to-do list", "Build `StringList` one feature at a time, until it grows, checks indexes and removes.", [
        step("A fixed list", "Create `StringList` with a private `String[]` of capacity 2 and a `size`. Add `add`, `get(int)` and `size()`. For now, `add` doesn't grow.",
             {"StringList.java": SL1, "TodoTester.java": T1}, "TodoTester", "2: wash dishes, call Gran"),
        step("Growing", "Make `add` double the array when it's full, so four items fit. Print them numbered.",
             {"StringList.java": SL2, "TodoTester.java": T2}, "TodoTester",
             "1. wash dishes\n2. call Gran\n3. study Java\n4. water plants",
             hint="If `size == items.length`, make a bigger array, copy, and switch the field before storing the new item."),
        step("Checking indexes", "Make `get` throw an `IndexOutOfBoundsException` with the message `Index <i>, size <size>` for any index below 0 or at least `size`. Then try it: change the tester to ask for `get(1)` and run it to see your exception, then change it back so the step passes.",
             {"StringList.java": SL3, "TodoTester.java": T3}, "TodoTester", "wash dishes\n1",
             hint="Without the check, `get(1)` would quietly return `null` from the unused slot.",
             checks=[{"pattern": r"throw\s+new\s+IndexOutOfBoundsException", "message": "Throw an `IndexOutOfBoundsException` for a bad index."},
                     {"pattern": r">=\s*size", "message": "Reject indexes that are `>= size`, not just ones past the array's length."}]),
        step("Removing", "Add `remove(int index)`, which shifts the later items left, clears the old last slot, shrinks `size`, and returns the removed item. Remove the first to-do item.",
             {"StringList.java": SL4, "TodoTester.java": T4}, "TodoTester",
             "Done: wash dishes\n1. call Gran\n2. study Java",
             checks=[{"pattern": r"items\s*\[\s*i\s*\]\s*=\s*items\s*\[\s*i\s*\+\s*1\s*\]", "message": "Shift left with `items[i] = items[i + 1];`."}]),
    ]),
    guided("ws-u12-ops", "Array algorithms", "Write three classic array operations as static methods.", [
        step("Reverse in place", "In `ArrayOps`, write `reverse(int[] data)`, which reverses the array in place by swapping the outermost pair, then moving both indexes inward.",
             {"ArrayOps.java": ARR1}, "ArrayOps", "[5, 4, 3, 2, 1]",
             hint="Swapping needs a temporary variable: `int temp = data[left]; data[left] = data[right]; data[right] = temp;`"),
        step("Rotate left", "Add `rotateLeft(int[] data)`: every value moves one slot left, and the first value wraps around to the end. Apply it after the reverse.",
             {"ArrayOps.java": ARR2}, "ArrayOps", "[5, 4, 3, 2, 1]\n[4, 3, 2, 1, 5]",
             hint="Save `data[0]` first, shift everything left, then put the saved value in the last slot."),
        step("A longer copy", "Add `appended(int[] data, int value)`, which returns a **new** array one slot longer with the value at the end, leaving the original unchanged. Use `Arrays.copyOf`.",
             {"ArrayOps.java": ARR3}, "ArrayOps", "[5, 4, 3, 2, 1]\n[4, 3, 2, 1, 5]\n[4, 3, 2, 1, 5, 99] 5"),
    ]),
    task("ws-u12-set", "A set with no duplicates",
         "Write `IntSet`, a growable collection of `int`s (capacity 2, doubling) that never holds the same value twice. `add(int)` returns `true` if the value was new and `false` if it was already there. Add `contains(int)` and `size()`.",
         {"IntSet.java": """public class IntSet {
    private int[] values = new int[2];
    private int size;

    public boolean contains(int value) {
        for (int i = 0; i < size; i++) {
            if (values[i] == value) {
                return true;
            }
        }
        return false;
    }

    public boolean add(int value) {
        if (contains(value)) {
            return false;
        }
        if (size == values.length) {
            int[] bigger = new int[values.length * 2];
            for (int i = 0; i < size; i++) {
                bigger[i] = values[i];
            }
            values = bigger;
        }
        values[size] = value;
        size++;
        return true;
    }

    public int size() {
        return size;
    }
}
""", "SetTester.java": """public class SetTester {
    public static void main(String[] args) {
        IntSet seen = new IntSet();
        int[] rolls = {4, 2, 4, 6, 2, 1};
        for (int r : rolls) {
            System.out.print(seen.add(r) + " ");
        }
        System.out.println();
        System.out.println(seen.size() + " different values");
    }
}
"""}, "SetTester", "true true false true false true\n4 different values",
         tests={"CheckSet.java": """public class CheckSet {
    public static void main(String[] args) {
        IntSet s = new IntSet();
        System.out.println(s.contains(0));
        for (int i = 0; i < 20; i++) {
            s.add(i % 7);
        }
        System.out.println(s.size() + " " + s.contains(6) + " " + s.contains(7));
    }
}
"""}, tests_run="CheckSet", tests_output="false\n7 true false",
         hints=["`add` can call `contains` first and stop early if the value is already there."]),
    task("ws-u12-counts", "Exam-sized array methods",
         "In `Stats`, write two static methods: `countAbove(int[] data, int limit)` returns how many values are greater than `limit`, and `maxIndex(int[] data)` returns the index of the largest value (the first one, if there's a tie). Assume the array isn't empty.",
         {"Stats.java": """public class Stats {
    public static int countAbove(int[] data, int limit) {
        int count = 0;
        for (int x : data) {
            if (x > limit) {
                count++;
            }
        }
        return count;
    }

    public static int maxIndex(int[] data) {
        int best = 0;
        for (int i = 1; i < data.length; i++) {
            if (data[i] > data[best]) {
                best = i;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        int[] scores = {72, 95, 88, 95, 60};
        System.out.println(countAbove(scores, 80));
        System.out.println(maxIndex(scores));
    }
}
"""}, "Stats", "3\n1",
         tests={"CheckStats.java": """public class CheckStats {
    public static void main(String[] args) {
        int[] neg = {-5, -2, -9};
        System.out.println(Stats.countAbove(neg, -3) + " " + Stats.maxIndex(neg));
        int[] one = {4};
        System.out.println(Stats.countAbove(one, 4) + " " + Stats.maxIndex(one));
    }
}
"""}, tests_run="CheckStats", tests_output="1 1\n0 0",
         hints=["`maxIndex` remembers the best **index** so far, not the best value. Compare with `data[best]`.",
                "Strictly greater (`>`) keeps the first of two tied maximums."]),
    [ALGS4_13, ARRAYS_API, MIT_ADT, GENERICS_TUT],
)
