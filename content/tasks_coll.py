"""Write-it-yourself tasks for unit 21, Introduction to Collections. Compiled and run by build.py."""
from tasks_classes import task

HIER = [
    task("w-coll-count", "Works with any collection",
         "Write `Counter` with `public static int countMatches(Collection<String> items, String target)`, which counts the elements equal to `target`, using only `Collection` methods (a for-each loop). `CounterTester` builds the same three words, `yes`, `no`, `yes`, in an `ArrayList` and in a `LinkedList`, both declared as `Collection<String>`, and prints `countMatches(..., \"yes\")` for each on one line.",
         {"Counter.java": """import java.util.Collection;

public class Counter {
    public static int countMatches(Collection<String> items, String target) {
        int count = 0;
        for (String item : items) {
            if (item.equals(target)) {
                count++;
            }
        }
        return count;
    }
}
""", "CounterTester.java": """import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;

public class CounterTester {
    public static void main(String[] args) {
        Collection<String> a = new ArrayList<>();
        Collection<String> b = new LinkedList<>();
        for (String w : new String[] {"yes", "no", "yes"}) {
            a.add(w);
            b.add(w);
        }
        System.out.println(Counter.countMatches(a, "yes") + " " + Counter.countMatches(b, "yes"));
    }
}
"""}, "CounterTester", "2 2",
         tests={"CheckCounter.java": """import java.util.ArrayDeque;
import java.util.Collection;

public class CheckCounter {
    public static void main(String[] args) {
        Collection<String> q = new ArrayDeque<>();
        q.add("a");
        q.add("a");
        System.out.println(Counter.countMatches(q, "a") + " " + Counter.countMatches(q, "b"));
    }
}
"""}, tests_run="CheckCounter", tests_output="2 0",
         checks=[{"pattern": r"Collection<String>\s+items", "message": "The parameter's type is `Collection<String>`."}],
         hints=["The tests pass an `ArrayDeque`, which is a `Collection` but not a `List`. A `Collection` parameter accepts it."]),

    task("w-coll-range", "Extend AbstractList",
         "`AbstractList` does most of a list's work if you supply `get(int)` and `size()`. Write `Range`, which `extends AbstractList<Integer>` and represents the numbers from `start` up to, but not including, `end` (both from the constructor), **without storing them**: `get(i)` returns `start + i` (throw `IndexOutOfBoundsException` for a bad index) and `size()` returns `end - start`. You get `toString`, `contains`, `indexOf` and for-each for free. `RangeTester` makes `new Range(3, 7)` and prints it, `contains(5)`, `indexOf(6)` and the sum from a for-each loop.",
         {"Range.java": """import java.util.AbstractList;

public class Range extends AbstractList<Integer> {
    private int start;
    private int end;

    public Range(int start, int end) {
        this.start = start;
        this.end = end;
    }

    @Override
    public Integer get(int index) {
        if (index < 0 || index >= size()) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size());
        }
        return start + index;
    }

    @Override
    public int size() {
        return end - start;
    }
}
""", "RangeTester.java": """public class RangeTester {
    public static void main(String[] args) {
        Range r = new Range(3, 7);
        System.out.println(r);
        System.out.println(r.contains(5) + " " + r.indexOf(6));
        int sum = 0;
        for (int x : r) {
            sum += x;
        }
        System.out.println(sum);
    }
}
"""}, "RangeTester", "[3, 4, 5, 6]\ntrue 3\n18",
         tests={"CheckRange.java": """import java.util.List;

public class CheckRange {
    public static void main(String[] args) {
        List<Integer> empty = new Range(5, 5);
        System.out.println(empty + " " + empty.isEmpty());
        try {
            new Range(0, 2).get(2);
        } catch (IndexOutOfBoundsException e) {
            System.out.println("bad index");
        }
    }
}
"""}, tests_run="CheckRange", tests_output="[] true\nbad index",
         checks=[{"pattern": r"extends\s+AbstractList<Integer>", "message": "`Range` extends `AbstractList<Integer>`."}],
         hints=["`get` must return `Integer` (the type parameter), not `int`, to override `AbstractList`'s `get`."]),
]

LIST = [
    task("w-list-removeevens", "Remove from any list",
         "Write `Evens` with `public static void removeEvens(List<Integer> list)`, which removes every even number. Loop over the indexes **from the end down to 0**, so removing an element doesn't shift the ones you haven't checked yet. `EvensTester` runs it on an `ArrayList` and a `LinkedList` holding 1 to 8 and prints both.",
         {"Evens.java": """import java.util.List;

public class Evens {
    public static void removeEvens(List<Integer> list) {
        for (int i = list.size() - 1; i >= 0; i--) {
            if (list.get(i) % 2 == 0) {
                list.remove(i);
            }
        }
    }
}
""", "EvensTester.java": """import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class EvensTester {
    public static void main(String[] args) {
        List<Integer> a = new ArrayList<>();
        List<Integer> b = new LinkedList<>();
        for (int i = 1; i <= 8; i++) {
            a.add(i);
            b.add(i);
        }
        Evens.removeEvens(a);
        Evens.removeEvens(b);
        System.out.println(a + " " + b);
    }
}
"""}, "EvensTester", "[1, 3, 5, 7] [1, 3, 5, 7]",
         tests={"CheckEvens.java": """import java.util.ArrayList;
import java.util.List;

public class CheckEvens {
    public static void main(String[] args) {
        List<Integer> l = new ArrayList<>();
        l.add(2);
        l.add(4);
        l.add(-6);
        l.add(9);
        Evens.removeEvens(l);
        System.out.println(l);
    }
}
"""}, tests_run="CheckEvens", tests_output="[9]",
         hints=["Counting up and removing at `i` skips the element that slides into slot `i`. Counting down avoids that.", "`remove(i)` with an `int` removes by index, which is what you want here."]),

    task("w-list-zip", "Zip two lists together",
         "Write `Zip` with `public static List<String> zip(List<String> a, List<String> b)`, returning a new `ArrayList` with elements taken alternately from `a` and `b`: `a[0]`, `b[0]`, `a[1]`, `b[1]`, … When one list runs out, the rest of the other follows. `ZipTester` zips `[1, 2, 3]` with `[x]` and prints the result.",
         {"Zip.java": """import java.util.ArrayList;
import java.util.List;

public class Zip {
    public static List<String> zip(List<String> a, List<String> b) {
        List<String> result = new ArrayList<>();
        int longest = Math.max(a.size(), b.size());
        for (int i = 0; i < longest; i++) {
            if (i < a.size()) {
                result.add(a.get(i));
            }
            if (i < b.size()) {
                result.add(b.get(i));
            }
        }
        return result;
    }
}
""", "ZipTester.java": """import java.util.ArrayList;
import java.util.List;

public class ZipTester {
    public static void main(String[] args) {
        List<String> a = new ArrayList<>();
        a.add("1");
        a.add("2");
        a.add("3");
        List<String> b = new ArrayList<>();
        b.add("x");
        System.out.println(Zip.zip(a, b));
    }
}
"""}, "ZipTester", "[1, x, 2, 3]",
         tests={"CheckZip.java": """import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class CheckZip {
    public static void main(String[] args) {
        List<String> a = new LinkedList<>();
        List<String> b = new ArrayList<>();
        b.add("p");
        b.add("q");
        System.out.println(Zip.zip(a, b) + " " + Zip.zip(b, b));
    }
}
"""}, tests_run="CheckZip", tests_output="[p, q] [p, p, q, q]"),
]

TASKS = {"coll-hierarchy": HIER, "coll-list": LIST}
