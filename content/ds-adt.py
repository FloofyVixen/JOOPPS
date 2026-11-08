from sources import MIT_ADT, ALGS4_13, ARRAYLIST_API, IFACE_TUT, HEL_12_2

BAG = """public interface IntBag {
    void add(int value);

    int size();

    boolean contains(int value);
}
"""
ARRAYBAG = """public class ArrayIntBag implements IntBag {
    private int[] items;
    private int count;

    public ArrayIntBag(int capacity) {
        items = new int[capacity];
        count = 0;
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
"""
BAGT = """public class BagTester {
    public static void main(String[] args) {
        IntBag bag = new ArrayIntBag(5);
        bag.add(7);
        bag.add(3);
        bag.add(7);
        System.out.println("Size: " + bag.size());
        System.out.println("Has 3? " + bag.contains(3));
        System.out.println("Has 9? " + bag.contains(9));
    }
}
"""
OVERFLOW = """public class Overflow {
    public static void main(String[] args) {
        IntBag bag = new ArrayIntBag(2);
        bag.add(1);
        bag.add(2);
        bag.add(3);
    }
}
"""
LIST = """import java.util.ArrayList;

public class ListDemo {
    public static void main(String[] args) {
        ArrayList<String> names = new ArrayList<>();
        names.add("Ana");
        names.add("Sam");
        names.add("Lee");
        System.out.println(names.size() + " names, first is " + names.get(0));

        names.remove("Sam");
        for (String n : names) {
            System.out.println(n);
        }
        System.out.println(names);
    }
}
"""

LESSON = {
    "id": "ds-adt",
    "title": "Data structures and abstract data types",
    "summary": "A data structure is a way to organize data; an abstract data type says what you can do with it, without saying how it's stored.",
    "goals": [
        "Explain the difference between an abstract data type and a data structure",
        "Describe an ADT with an interface and implement it with an array",
        "Recognize Java's `ArrayList` as a ready-made list",
    ],
    "cos225": "This unit opens the data-structures half of COS 225. The exam guide's basics include arrays and lists (\"don't need to use them, just know what they are\"). This lesson shows what a list is and how it relates to the arrays you already know.",
    "blocks": [
        {"type": "h", "text": "What versus how"},
        {"type": "p", "text": "An **abstract data type (ADT)** is defined by its operations: what you can do with it. A \"bag of numbers\" lets you add a number, ask how many there are, and ask whether one is there. Nothing about how they're stored. A **data structure** is a concrete way to store the data so those operations work, such as an array, or (later in the course) linked nodes or a tree."},
        {"type": "p", "text": "You already have the Java tool for describing \"what\" without \"how\": an interface. Here the `IntBag` interface is the ADT, and `ArrayIntBag` is one data structure that implements it."},
        {"type": "code", "files": {"IntBag.java": BAG, "ArrayIntBag.java": ARRAYBAG, "BagTester.java": BAGT}, "run": "BagTester"},
        {"type": "list", "items": [
            "`items` is the array. `count` tracks how many slots are actually used, which is different from `items.length`, the capacity.",
            "`add` puts the new value in the first unused slot, `items[count]`, then increases `count`.",
            "`contains` only looks at the first `count` slots. The rest of the array holds leftover zeros that aren't really in the bag.",
            "The tester only uses the `IntBag` type. Any other class implementing `IntBag` (a faster one, say) could be swapped in without changing a line of the tester.",
        ]},

        {"type": "h", "text": "The weakness of a fixed array"},
        {"type": "p", "text": "An array's size is fixed when it's created. This bag has room for 2, so a third `add` runs off the end:"},
        {"type": "code", "files": {"IntBag.java": BAG, "ArrayIntBag.java": ARRAYBAG, "Overflow.java": OVERFLOW}, "run": "Overflow", "expect": "runtime",
         "after": "The crash happens inside `ArrayIntBag.add` (line 12), called from `Overflow.main` (line 6). The \"Resizing an array\" lesson fixes this by growing the array when it fills up."},

        {"type": "h", "text": "Lists: Java's ready-made answer"},
        {"type": "p", "text": "A **list** is an ADT: an ordered sequence you can add to, read by position, and remove from, and it grows as needed. Java provides one, `ArrayList`, in `java.util`. Inside, it's an array that grows itself, which is exactly what you'll build in this unit."},
        {"type": "code", "files": {"ListDemo.java": LIST}, "run": "ListDemo"},
        {"type": "list", "items": [
            "`ArrayList<String>` is a list of `String`s. The type in angle brackets says what it holds; the generics lesson explains how that works.",
            "`add`, `get(index)`, `size()` and `remove(...)` are its operations. Unlike an array, there's no size to choose up front.",
            "Printing a list directly gives `[Ana, Lee]`, because `ArrayList` has its own `toString`.",
        ]},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "adt-contains", "title": "Search only the used part",
         "prompt": "Finish `contains`. The array may be bigger than the number of values stored.",
         "files": {"IntBag.java": BAG, "ArrayIntBag.java": ARRAYBAG.replace("""        for (int i = 0; i < count; i++) {
            if (items[i] == value) {""", """        for (int i = 0; i < [[limit]]; i++) {
            if ([[check]] == value) {"""), "ZeroTester.java": """public class ZeroTester {
    public static void main(String[] args) {
        IntBag bag = new ArrayIntBag(4);
        bag.add(5);
        System.out.println(bag.contains(5));
        System.out.println(bag.contains(0));
    }
}
"""},
         "run": "ZeroTester", "output": "true\nfalse",
         "blanks": {
             "limit": {"accept": ["count"], "hint": "How many slots hold real values?",
                       "wrong": [{"answer": "items.length", "why": "That checks the whole array, including unused slots, which hold 0. So the bag wrongly says it contains 0."}]},
             "check": {"accept": ["items[i]"], "hint": "The value in slot `i`.",
                       "wrong": [{"answer": "i", "why": "`i` is the slot number, not the value stored there. Compare `items[i]`."}]},
         },
         "explain": "Only slots 0 to `count - 1` are part of the bag. The 0s after that are just the array's default values."},
        {"type": "quiz", "id": "adt-which",
         "question": "Which is an abstract data type rather than a data structure?",
         "choices": ["An array of 10 `int`s", "\"A list: add items, get by position, remove\"", "The `int[] items` field in `ArrayIntBag`", "A block of memory"],
         "answer": 1,
         "explain": "An ADT is described only by its operations. The array is one concrete way to store the data, a data structure that can implement the ADT."},
    ],
    "sources": [MIT_ADT, ALGS4_13, IFACE_TUT, ARRAYLIST_API, HEL_12_2],
}
