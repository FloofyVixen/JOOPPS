"""Write-it-yourself tasks for Data Structures intro (arrays). Compiled and run by build.py."""
from tasks_classes import task

BAG = """public interface IntBag {
    void add(int value);

    int size();

    boolean contains(int value);
}
"""

ADT = [
    task("w-arraybag", "Implement an ADT",
         "The `IntBag` interface (given) is the ADT. Write `ArrayIntBag`, which implements it with a private `int[]` of the capacity passed to its constructor and a private count of values stored.",
         {"IntBag.java": BAG, "ArrayIntBag.java": """public class ArrayIntBag implements IntBag {
    private int[] items;
    private int count;

    public ArrayIntBag(int capacity) {
        items = new int[capacity];
    }

    @Override
    public void add(int value) {
        items[count] = value;
        count++;
    }

    @Override
    public int size() {
        return count;
    }

    @Override
    public boolean contains(int value) {
        for (int i = 0; i < count; i++) {
            if (items[i] == value) {
                return true;
            }
        }
        return false;
    }
}
""", "BagTester.java": """public class BagTester {
    public static void main(String[] args) {
        IntBag bag = new ArrayIntBag(4);
        bag.add(12);
        bag.add(-3);
        System.out.println(bag.size());
        System.out.println(bag.contains(-3));
        System.out.println(bag.contains(0));
    }
}
"""}, "BagTester", "2\ntrue\nfalse",
         tests={"CheckBag.java": """public class CheckBag {
    public static void main(String[] args) {
        IntBag empty = new ArrayIntBag(3);
        System.out.println(empty.size() + " " + empty.contains(0));
        IntBag b = new ArrayIntBag(3);
        b.add(0);
        System.out.println(b.contains(0));
    }
}
"""}, tests_run="CheckBag", tests_output="0 false\ntrue",
         hints=["`contains` must look only at the first `count` slots, or an empty bag will \"contain\" 0."]),

    task("w-arraylist-names", "Use Java's ArrayList",
         "In `Roster`, use an `ArrayList<String>`: add `Ana`, `Sam`, `Lee` and `Kim`, remove `Sam`, then print the size, the item at index 1, and the whole list.",
         {"Roster.java": """import java.util.ArrayList;

public class Roster {
    public static void main(String[] args) {
        ArrayList<String> names = new ArrayList<>();
        names.add("Ana");
        names.add("Sam");
        names.add("Lee");
        names.add("Kim");
        names.remove("Sam");
        System.out.println(names.size());
        System.out.println(names.get(1));
        System.out.println(names);
    }
}
"""}, "Roster", "3\nLee\n[Ana, Lee, Kim]",
         hints=["Start the file with `import java.util.ArrayList;`.",
                "After removing `Sam`, the items after it move down one position, so index 1 is now `Lee`."],
         checks=[{"pattern": r"ArrayList\s*<\s*String\s*>", "message": "Use an `ArrayList<String>`."}]),

    task("w-minmax", "One ADT, two data structures",
         "The interface `MinMax` (`add(int)`, `min()`, `max()`) describes an ADT. Write **two** implementations: `ArrayMinMax` stores every value in a growing array and searches it; `RunningMinMax` stores only the smallest and largest seen so far. Both must pass the same test.",
         {"MinMax.java": """public interface MinMax {
    void add(int value);

    int min();

    int max();
}
""", "ArrayMinMax.java": """public class ArrayMinMax implements MinMax {
    private int[] values = new int[2];
    private int size;

    @Override
    public void add(int value) {
        if (size == values.length) {
            int[] bigger = new int[values.length * 2];
            for (int i = 0; i < size; i++) {
                bigger[i] = values[i];
            }
            values = bigger;
        }
        values[size] = value;
        size++;
    }

    @Override
    public int min() {
        int m = values[0];
        for (int i = 1; i < size; i++) {
            if (values[i] < m) {
                m = values[i];
            }
        }
        return m;
    }

    @Override
    public int max() {
        int m = values[0];
        for (int i = 1; i < size; i++) {
            if (values[i] > m) {
                m = values[i];
            }
        }
        return m;
    }
}
""", "RunningMinMax.java": """public class RunningMinMax implements MinMax {
    private int smallest;
    private int largest;
    private boolean empty = true;

    @Override
    public void add(int value) {
        if (empty || value < smallest) {
            smallest = value;
        }
        if (empty || value > largest) {
            largest = value;
        }
        empty = false;
    }

    @Override
    public int min() {
        return smallest;
    }

    @Override
    public int max() {
        return largest;
    }
}
""", "MinMaxTester.java": """public class MinMaxTester {
    public static void main(String[] args) {
        MinMax[] both = {new ArrayMinMax(), new RunningMinMax()};
        for (MinMax m : both) {
            m.add(5);
            m.add(-2);
            m.add(9);
            System.out.println(m.min() + " " + m.max());
        }
    }
}
"""}, "MinMaxTester", "-2 9\n-2 9",
         tests={"CheckMinMax.java": """public class CheckMinMax {
    public static void main(String[] args) {
        MinMax[] both = {new ArrayMinMax(), new RunningMinMax()};
        for (MinMax m : both) {
            m.add(-7);
            System.out.println(m.min() + " " + m.max());
            m.add(-7);
            m.add(-10);
            m.add(-1);
            System.out.println(m.min() + " " + m.max());
        }
    }
}
"""}, tests_run="CheckMinMax", tests_output="-7 -7\n-10 -1\n-7 -7\n-10 -1",
         hints=["The test only adds negative numbers. If `RunningMinMax` starts `largest` at 0, it will report 0 as the max. The first value added must set both.",
                "One way: a `boolean empty = true;` field that `add` checks and then sets to `false`."]),
]

MEMORY = [
    task("w-copy-array", "A real copy",
         "In `Copier`, write `public static int[] copy(int[] source)`, which returns a **new** array with the same values (use a loop, not `Arrays.copyOf`). Show that changing the copy leaves the original alone.",
         {"Copier.java": """public class Copier {
    public static int[] copy(int[] source) {
        int[] result = new int[source.length];
        for (int i = 0; i < source.length; i++) {
            result[i] = source[i];
        }
        return result;
    }

    public static void main(String[] args) {
        int[] original = {3, 1, 4};
        int[] duplicate = copy(original);
        duplicate[0] = 100;
        System.out.println(original[0] + " " + duplicate[0]);
        System.out.println(original == duplicate);
    }
}
"""}, "Copier", "3 100\nfalse",
         tests={"CheckCopier.java": """import java.util.Arrays;

public class CheckCopier {
    public static void main(String[] args) {
        int[] a = {7, 8};
        int[] b = Copier.copy(a);
        System.out.println(Arrays.toString(b) + " " + (a != b));
        System.out.println(Copier.copy(new int[0]).length);
    }
}
"""}, tests_run="CheckCopier", tests_output="[7, 8] true\n0",
         checks=[{"pattern": r"new\s+int\s*\[", "message": "Create a new array with `new int[...]`."}]),

    task("w-insert-at", "Insert by shifting",
         "In `Inserter`, write `public static void insertAt(int[] data, int size, int index, int value)`. The array has room for at least one more value; shift everything from `index` onward one slot right, then put the value in.",
         {"Inserter.java": """import java.util.Arrays;

public class Inserter {
    public static void insertAt(int[] data, int size, int index, int value) {
        for (int i = size; i > index; i--) {
            data[i] = data[i - 1];
        }
        data[index] = value;
    }

    public static void main(String[] args) {
        int[] data = {5, 10, 20, 0};
        insertAt(data, 3, 2, 15);
        System.out.println(Arrays.toString(data));
    }
}
"""}, "Inserter", "[5, 10, 15, 20]",
         tests={"CheckInserter.java": """import java.util.Arrays;

public class CheckInserter {
    public static void main(String[] args) {
        int[] front = {1, 2, 0};
        Inserter.insertAt(front, 2, 0, 9);
        System.out.println(Arrays.toString(front));
        int[] end = {1, 2, 0};
        Inserter.insertAt(end, 2, 2, 9);
        System.out.println(Arrays.toString(end));
    }
}
"""}, tests_run="CheckInserter", tests_output="[9, 1, 2]\n[1, 2, 9]",
         hints=["Shift from the end backwards, so nothing is overwritten before it moves.",
                "The method changes the array it was given; it doesn't need to return anything."]),

    task("w-without", "A smaller array without one value",
         "In `Filter`, write `public static int[] without(int[] data, int value)`, which returns a new array holding every element except those equal to `value`, in the same order. Count first, so the new array is exactly the right size.",
         {"Filter.java": """import java.util.Arrays;

public class Filter {
    public static int[] without(int[] data, int value) {
        int keep = 0;
        for (int x : data) {
            if (x != value) {
                keep++;
            }
        }
        int[] result = new int[keep];
        int next = 0;
        for (int x : data) {
            if (x != value) {
                result[next] = x;
                next++;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        int[] data = {3, 7, 3, 1, 3};
        System.out.println(Arrays.toString(without(data, 3)));
        System.out.println(Arrays.toString(data));
    }
}
"""}, "Filter", "[7, 1]\n[3, 7, 3, 1, 3]",
         tests={"CheckFilter.java": """import java.util.Arrays;

public class CheckFilter {
    public static void main(String[] args) {
        System.out.println(Arrays.toString(Filter.without(new int[]{4, 4}, 4)));
        System.out.println(Arrays.toString(Filter.without(new int[]{1, 2}, 9)));
    }
}
"""}, tests_run="CheckFilter", tests_output="[]\n[1, 2]",
         hints=["Two loops: one to count how many to keep, one to copy them into the new array using a separate `next` index."]),
]

RESIZE = [
    task("w-doublelist", "A growable list of doubles",
         "Write `DoubleList`, a growable list of `double`s: starts with capacity 2, doubles when full. Methods: `add(double)`, `get(int)` (throws `IndexOutOfBoundsException` for bad indexes), `size()` and `average()` (0.0 when empty).",
         {"DoubleList.java": """public class DoubleList {
    private double[] data;
    private int size;

    public DoubleList() {
        data = new double[2];
    }

    public void add(double value) {
        if (size == data.length) {
            double[] bigger = new double[data.length * 2];
            for (int i = 0; i < size; i++) {
                bigger[i] = data[i];
            }
            data = bigger;
        }
        data[size] = value;
        size++;
    }

    public double get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size);
        }
        return data[index];
    }

    public int size() {
        return size;
    }

    public double average() {
        if (size == 0) {
            return 0.0;
        }
        double total = 0;
        for (int i = 0; i < size; i++) {
            total = total + data[i];
        }
        return total / size;
    }
}
""", "TempsTester.java": """public class TempsTester {
    public static void main(String[] args) {
        DoubleList temps = new DoubleList();
        temps.add(20.5);
        temps.add(22.0);
        temps.add(18.5);
        temps.add(23.0);
        System.out.println(temps.size() + " readings");
        System.out.println("Last: " + temps.get(3));
        System.out.println("Average: " + temps.average());
    }
}
"""}, "TempsTester", "4 readings\nLast: 23.0\nAverage: 21.0",
         tests={"CheckDoubleList.java": """public class CheckDoubleList {
    public static void main(String[] args) {
        DoubleList d = new DoubleList();
        System.out.println(d.average());
        for (int i = 0; i < 10; i++) {
            d.add(i);
        }
        System.out.println(d.size() + " " + d.get(9));
    }
}
"""}, tests_run="CheckDoubleList", tests_output="0.0\n10 9.0",
         hints=["The test adds 10 values to a list that starts with room for 2, so `add` must grow more than once."]),

    task("w-capacity", "Watch the capacity grow",
         "Write `NameList`, a growable list of `String`s starting at capacity 1 and doubling when full, with `add`, `size()`, `capacity()` and `contains(String)`. In the tester, add five names and print the capacity after each add.",
         {"NameList.java": """public class NameList {
    private String[] names;
    private int size;

    public NameList() {
        names = new String[1];
    }

    public void add(String name) {
        if (size == names.length) {
            String[] bigger = new String[names.length * 2];
            for (int i = 0; i < size; i++) {
                bigger[i] = names[i];
            }
            names = bigger;
        }
        names[size] = name;
        size++;
    }

    public int size() {
        return size;
    }

    public int capacity() {
        return names.length;
    }

    public boolean contains(String name) {
        for (int i = 0; i < size; i++) {
            if (names[i].equals(name)) {
                return true;
            }
        }
        return false;
    }
}
""", "NameTester.java": """public class NameTester {
    public static void main(String[] args) {
        NameList list = new NameList();
        String[] incoming = {"Ana", "Sam", "Lee", "Kim", "Bo"};
        for (String n : incoming) {
            list.add(n);
            System.out.print(list.capacity() + " ");
        }
        System.out.println();
        System.out.println(list.contains("Kim") + " " + list.contains("Zed"));
    }
}
"""}, "NameTester", "1 2 4 4 8\ntrue false",
         tests={"CheckNameList.java": """public class CheckNameList {
    public static void main(String[] args) {
        NameList n = new NameList();
        System.out.println(n.size() + " " + n.capacity() + " " + n.contains("x"));
    }
}
"""}, tests_run="CheckNameList", tests_output="0 1 false",
         hints=["`contains` must stop at `size`: the unused slots are `null`, and calling `equals` on `null` crashes."]),

    task("w-list-insert", "Insert into a growable list",
         "Write `IntList` with `add(int)`, `get(int)`, `size()`, and `insert(int index, int value)`, which grows the array if needed, shifts later values right, and puts the value at `index`. An index from 0 to `size` is allowed (inserting at `size` appends); anything else throws `IndexOutOfBoundsException`.",
         {"IntList.java": """public class IntList {
    private int[] data = new int[2];
    private int size;

    private void growIfFull() {
        if (size == data.length) {
            int[] bigger = new int[data.length * 2];
            for (int i = 0; i < size; i++) {
                bigger[i] = data[i];
            }
            data = bigger;
        }
    }

    public void add(int value) {
        growIfFull();
        data[size] = value;
        size++;
    }

    public void insert(int index, int value) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size);
        }
        growIfFull();
        for (int i = size; i > index; i--) {
            data[i] = data[i - 1];
        }
        data[index] = value;
        size++;
    }

    public int get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size);
        }
        return data[index];
    }

    public int size() {
        return size;
    }
}
""", "InsertTester.java": """public class InsertTester {
    public static void main(String[] args) {
        IntList list = new IntList();
        list.add(10);
        list.add(30);
        list.insert(1, 20);
        list.insert(0, 5);
        list.insert(4, 40);
        for (int i = 0; i < list.size(); i++) {
            System.out.print(list.get(i) + " ");
        }
        System.out.println();
    }
}
"""}, "InsertTester", "5 10 20 30 40",
         tests={"CheckInsert.java": """public class CheckInsert {
    public static void main(String[] args) {
        IntList list = new IntList();
        list.insert(0, 1);
        System.out.println(list.size() + " " + list.get(0));
        try {
            list.insert(5, 2);
            System.out.println("no error");
        } catch (IndexOutOfBoundsException e) {
            System.out.println("rejected index 5");
        }
    }
}
"""}, tests_run="CheckInsert", tests_output="1 1\nrejected index 5",
         hints=["Grow first, then shift, then place the value, then increase `size`.",
                "Putting the growing code in a private helper lets `add` and `insert` share it."]),
]

GENERICS = [
    task("w-box", "A generic box",
         "Write `Box<T>` with a private `T item`, `put(T)`, `get()`, `isEmpty()`, and `take()`, which returns the item and leaves the box empty.",
         {"Box.java": """public class Box<T> {
    private T item;

    public void put(T item) {
        this.item = item;
    }

    public T get() {
        return item;
    }

    public boolean isEmpty() {
        return item == null;
    }

    public T take() {
        T result = item;
        item = null;
        return result;
    }
}
""", "BoxTester.java": """public class BoxTester {
    public static void main(String[] args) {
        Box<String> gift = new Box<>();
        gift.put("scarf");
        System.out.println(gift.take() + " " + gift.isEmpty());
        Box<Integer> number = new Box<>();
        number.put(7);
        System.out.println(number.get() * 6);
    }
}
"""}, "BoxTester", "scarf true\n42",
         tests={"CheckBox.java": """public class CheckBox {
    public static void main(String[] args) {
        Box<Double> b = new Box<>();
        System.out.println(b.isEmpty() + " " + b.take());
        b.put(1.5);
        System.out.println(b.get() + " " + b.isEmpty());
    }
}
"""}, tests_run="CheckBox", tests_output="true null\n1.5 false",
         checks=[{"pattern": r"class\s+Box\s*<\s*T\s*>", "message": "Declare the class as `Box<T>`."}]),

    task("w-growlist", "A generic growable list",
         "Write `GrowList<T>`: a growable list of any type, stored in an `Object[]` with capacity 2 that doubles when full. Methods: `add(T)`, `get(int)` (cast back to `T`, with `@SuppressWarnings(\"unchecked\")`), `size()` and `contains(T)`, which compares with `equals`.",
         {"GrowList.java": """public class GrowList<T> {
    private Object[] data = new Object[2];
    private int size;

    public void add(T value) {
        if (size == data.length) {
            Object[] bigger = new Object[data.length * 2];
            for (int i = 0; i < size; i++) {
                bigger[i] = data[i];
            }
            data = bigger;
        }
        data[size] = value;
        size++;
    }

    @SuppressWarnings("unchecked")
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + size);
        }
        return (T) data[index];
    }

    public int size() {
        return size;
    }

    public boolean contains(T value) {
        for (int i = 0; i < size; i++) {
            if (data[i].equals(value)) {
                return true;
            }
        }
        return false;
    }
}
""", "GrowTester.java": """public class GrowTester {
    public static void main(String[] args) {
        GrowList<String> fruit = new GrowList<>();
        fruit.add("pear");
        fruit.add("fig");
        fruit.add("kiwi");
        System.out.println(fruit.size() + " " + fruit.get(2) + " " + fruit.contains("fig"));
    }
}
"""}, "GrowTester", "3 kiwi true",
         tests={"CheckGrow.java": """public class CheckGrow {
    public static void main(String[] args) {
        GrowList<Integer> nums = new GrowList<>();
        for (int i = 0; i < 9; i++) {
            nums.add(i * i);
        }
        System.out.println(nums.get(8) + " " + nums.contains(49) + " " + nums.contains(50));
    }
}
"""}, tests_run="CheckGrow", tests_output="64 true false",
         hints=["Compare with `data[i].equals(value)`, not `==`: two `Integer` or `String` objects with the same value aren't always the same object."]),

    task("w-pair", "A generic pair with a swap",
         "Write `Pair<T>` holding `first` and `second` of the same type, with getters, a `toString` like `(left, right)`, and `swapped()`, which returns a **new** pair with the two values switched.",
         {"Pair.java": """public class Pair<T> {
    private T first;
    private T second;

    public Pair(T first, T second) {
        this.first = first;
        this.second = second;
    }

    public T getFirst() {
        return first;
    }

    public T getSecond() {
        return second;
    }

    public Pair<T> swapped() {
        return new Pair<>(second, first);
    }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}
""", "PairTester.java": """public class PairTester {
    public static void main(String[] args) {
        Pair<String> p = new Pair<>("left", "right");
        System.out.println(p);
        System.out.println(p.swapped());
        System.out.println(p);
    }
}
"""}, "PairTester", "(left, right)\n(right, left)\n(left, right)",
         tests={"CheckPair.java": """public class CheckPair {
    public static void main(String[] args) {
        Pair<Integer> n = new Pair<>(1, 2).swapped();
        System.out.println(n.getFirst() + n.getSecond() * 10);
    }
}
"""}, tests_run="CheckPair", tests_output="12",
         hints=["`swapped()` returns `Pair<T>`, built with `new Pair<>(second, first)`."]),
]

TASKS = {"ds-adt": ADT, "ds-memory": MEMORY, "ds-resize": RESIZE, "ds-generics": GENERICS}
