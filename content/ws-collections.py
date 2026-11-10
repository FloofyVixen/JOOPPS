from sources import COLL_IFACES, LIST_API, ABSTRACTLIST_API, ARRAYLIST_API, LINKEDLIST_API, GENERICS_TUT
from wshelp import step, guided, workshop, task

G1 = """import java.util.ArrayList;
import java.util.List;

public class Gradebook {
    public static double average(List<Integer> scores) {
        int sum = 0;
        for (int s : scores) {
            sum += s;
        }
        return (double) sum / scores.size();
    }

    public static void main(String[] args) {
        List<Integer> scores = new ArrayList<>();
        int[] marks = {88, 42, 95, 67, 30};
        for (int m : marks) {
            scores.add(m);
        }
        System.out.println(scores + " average " + average(scores));
    }
}
"""
G2 = G1.replace("""    public static void main""", """    public static int removeBelow(List<Integer> scores, int limit) {
        int removed = 0;
        for (int i = scores.size() - 1; i >= 0; i--) {
            if (scores.get(i) < limit) {
                scores.remove(i);
                removed++;
            }
        }
        return removed;
    }

    public static void main""").replace("""        System.out.println(scores + " average " + average(scores));""", """        System.out.println(scores + " average " + average(scores));
        int removed = removeBelow(scores, 50);
        System.out.println(removed + " removed: " + scores + " average " + average(scores));""")
G3 = G2.replace("import java.util.ArrayList;\n", "import java.util.LinkedList;\n").replace("new ArrayList<>()", "new LinkedList<>()").replace("""    public static void main""", """    public static int highest(List<Integer> scores) {
        int best = scores.get(0);
        for (int s : scores) {
            if (s > best) {
                best = s;
            }
        }
        return best;
    }

    public static void main""").replace("""        System.out.println(removed + " removed: " + scores + " average " + average(scores));""", """        System.out.println(removed + " removed: " + scores + " average " + average(scores));
        System.out.println("highest " + highest(scores) + ", stored in a " + scores.getClass().getSimpleName());""")

F1 = """import java.util.AbstractList;

public class FixedList<T> extends AbstractList<T> {
    private Object[] data = new Object[4];
    private int size = 0;

    @SuppressWarnings("unchecked")
    @Override
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size);
        }
        return (T) data[index];
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public void add(int index, T element) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size);
        }
        if (size == data.length) {
            Object[] bigger = new Object[data.length * 2];
            for (int i = 0; i < size; i++) {
                bigger[i] = data[i];
            }
            data = bigger;
        }
        for (int i = size; i > index; i--) {
            data[i] = data[i - 1];
        }
        data[index] = element;
        size++;
    }
}
"""
F2 = F1.replace("""    @Override
    public void add(int index, T element) {""", """    @Override
    public T set(int index, T element) {
        T old = get(index);
        data[index] = element;
        return old;
    }

    @Override
    public T remove(int index) {
        T old = get(index);
        for (int i = index; i < size - 1; i++) {
            data[i] = data[i + 1];
        }
        size--;
        data[size] = null;
        return old;
    }

    @Override
    public void add(int index, T element) {""")
FT1 = """import java.util.List;

public class FixedTester {
    public static void main(String[] args) {
        List<String> list = new FixedList<>();
        list.add("b");
        list.add("d");
        list.add(0, "a");
        list.add(2, "c");
        list.add("e");
        System.out.println(list + " " + list.size());
        System.out.println(list.contains("c") + " " + list.indexOf("e"));
    }
}
"""
FT2 = """import java.util.List;

public class FixedTester {
    public static void main(String[] args) {
        List<String> list = new FixedList<>();
        for (String s : new String[] {"a", "b", "c", "d"}) {
            list.add(s);
        }
        System.out.println(list.set(1, "B") + " " + list.remove(0) + " " + list);
        list.remove("d");
        System.out.println(list);
    }
}
"""
FT3 = """import java.util.ArrayList;
import java.util.List;

public class FixedTester {
    public static void main(String[] args) {
        List<Integer> mine = new FixedList<>();
        List<Integer> javas = new ArrayList<>();
        for (int i = 1; i <= 5; i++) {
            mine.add(i * i);
            javas.add(i * i);
        }
        System.out.println(mine.equals(javas) + " " + mine.lastIndexOf(16));
        mine.removeIf(x -> x % 2 == 0);
        System.out.println(mine + " " + mine.isEmpty());
        mine.clear();
        System.out.println(mine + " " + mine.isEmpty());
    }
}
"""

LESSON = workshop(
    "ws-collections", "Workshop: collections",
    "Write code against the `List` interface and switch implementations in one line, then build your own list class on `AbstractList` and see how much Java gives you for free.",
    ["Declare and pass collections by their interface types",
     "Extend `AbstractList` by supplying the few methods it leaves abstract",
     "Explain what interfaces, abstract classes and concrete classes each contribute"],
    guided("ws-u21-gradebook", "A gradebook on the List interface", "Every method takes a `List<Integer>`, so the implementation can change without touching them.", [
        step("Average", "In `Gradebook`, write `average(List<Integer> scores)` with a for-each loop. In `main`, put five marks into a `List<Integer>` created as an `ArrayList`, and print the list and its average.",
             {"Gradebook.java": G1}, "Gradebook", "[88, 42, 95, 67, 30] average 64.4"),
        step("Removing low marks", "Add `removeBelow(List<Integer> scores, int limit)`, which removes every mark below `limit` (loop from the end) and returns how many it removed. Remove those below 50.",
             {"Gradebook.java": G2}, "Gradebook", "[88, 42, 95, 67, 30] average 64.4\n2 removed: [88, 95, 67] average 83.33333333333333"),
        step("Switch to LinkedList", "Change the one `new ArrayList<>()` to `new LinkedList<>()` (and the import). Nothing else needs to change. Add `highest(List<Integer>)`, and print it with `scores.getClass().getSimpleName()` to prove which class you're using.",
             {"Gradebook.java": G3}, "Gradebook",
             "[88, 42, 95, 67, 30] average 64.4\n2 removed: [88, 95, 67] average 83.33333333333333\nhighest 95, stored in a LinkedList",
             checks=[{"pattern": r"new\s+LinkedList<>\(\)", "message": "The list is created as a `LinkedList`."}]),
    ]),
    guided("ws-u21-abstractlist", "Your own list on AbstractList", "Write `FixedList<T>` by extending `AbstractList<T>`: supply storage and a few methods, and inherit the rest of `List`.", [
        step("get, size and add", "Extend `AbstractList<T>` with an `Object[]` of 4 and a `size`. Override `get(int)`, `size()` and `add(int index, T element)` (shift right, growing when full). `AbstractList`'s `add(T)` calls your `add(size(), element)`, and `toString`, `contains` and `indexOf` work through your `get`.",
             {"FixedList.java": F1, "FixedTester.java": FT1}, "FixedTester", "[a, b, c, d, e] 5\ntrue 4"),
        step("set and remove", "Override `set(int, T)` (return the old element) and `remove(int)` (shift left, clear the last slot). `AbstractList`'s `remove(Object)` now works too, because it finds the index and calls yours.",
             {"FixedList.java": F2, "FixedTester.java": FT2}, "FixedTester", "b a [B, c, d]\n[B, c]"),
        step("All of List, for free", "Without changing `FixedList`, try more `List` methods: `equals` against an `ArrayList`, `lastIndexOf`, `removeIf` and `clear`. Every one comes from `AbstractList` and `AbstractCollection`, built on your overrides.",
             {"FixedList.java": F2, "FixedTester.java": FT3}, "FixedTester", "true 3\n[1, 9, 25] false\n[] true",
             hint="`x -> x % 2 == 0` is a lambda: a small function that returns `true` for even numbers. `removeIf` removes each element it returns `true` for."),
    ]),
    task("ws-u21-dedupe", "Remove duplicates, keep the order",
         "Write `Dedupe` with `public static List<String> unique(List<String> words)`, returning a new `ArrayList` with each word once, in the order it first appeared. Use `contains` on the result list to check. (This is O(n²), since `contains` searches; a `Set` would be faster, but sets aren't covered here.) `DedupeTester` prints `unique` of `to be or not to be`, split on spaces.",
         {"Dedupe.java": """import java.util.ArrayList;
import java.util.List;

public class Dedupe {
    public static List<String> unique(List<String> words) {
        List<String> result = new ArrayList<>();
        for (String w : words) {
            if (!result.contains(w)) {
                result.add(w);
            }
        }
        return result;
    }
}
""", "DedupeTester.java": """import java.util.ArrayList;
import java.util.List;

public class DedupeTester {
    public static void main(String[] args) {
        List<String> words = new ArrayList<>();
        for (String w : "to be or not to be".split(" ")) {
            words.add(w);
        }
        System.out.println(Dedupe.unique(words));
    }
}
"""}, "DedupeTester", "[to, be, or, not]",
         tests={"CheckDedupe.java": """import java.util.LinkedList;
import java.util.List;

public class CheckDedupe {
    public static void main(String[] args) {
        List<String> words = new LinkedList<>();
        words.add("a");
        words.add("a");
        System.out.println(Dedupe.unique(words) + " " + words + " " + Dedupe.unique(new LinkedList<>()));
    }
}
"""}, tests_run="CheckDedupe", tests_output="[a] [a, a] []"),
    task("ws-u21-rotate", "A generic rotate",
         "Write `Rotate` with a **generic** method `public static <T> void rotateRight(List<T> list, int k)` that moves the last element to the front, `k` times, using `list.add(0, list.remove(list.size() - 1))`. Do nothing for an empty list. `RotateTester` rotates a `List<String>` of `a` to `e` by 2 and a `List<Integer>` of 1 to 3 by 4, and prints both.",
         {"Rotate.java": """import java.util.List;

public class Rotate {
    public static <T> void rotateRight(List<T> list, int k) {
        if (list.isEmpty()) {
            return;
        }
        for (int i = 0; i < k; i++) {
            list.add(0, list.remove(list.size() - 1));
        }
    }
}
""", "RotateTester.java": """import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class RotateTester {
    public static void main(String[] args) {
        List<String> letters = new ArrayList<>();
        for (String s : new String[] {"a", "b", "c", "d", "e"}) {
            letters.add(s);
        }
        List<Integer> nums = new LinkedList<>();
        for (int i = 1; i <= 3; i++) {
            nums.add(i);
        }
        Rotate.rotateRight(letters, 2);
        Rotate.rotateRight(nums, 4);
        System.out.println(letters + " " + nums);
    }
}
"""}, "RotateTester", "[d, e, a, b, c] [3, 1, 2]",
         tests={"CheckRotate.java": """import java.util.ArrayList;
import java.util.List;

public class CheckRotate {
    public static void main(String[] args) {
        List<Double> empty = new ArrayList<>();
        Rotate.rotateRight(empty, 3);
        System.out.println(empty);
    }
}
"""}, tests_run="CheckRotate", tests_output="[]",
         checks=[{"pattern": r"static\s+<T>", "message": "`rotateRight` is a generic method: `public static <T> void ...`."}],
         hints=["`<T>` before the return type declares the method's type parameter, so the same method works for a `List<String>` and a `List<Integer>`."]),
    [COLL_IFACES, LIST_API, ABSTRACTLIST_API, ARRAYLIST_API, LINKEDLIST_API, GENERICS_TUT],
)
