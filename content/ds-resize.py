from sources import ALGS4_13, ARRAYS_API, ARRAYLIST_API, EXCEPTIONS_TUT

INTLIST = """public class IntList {
    private int[] data;
    private int size;

    public IntList() {
        data = new int[2];
        size = 0;
    }

    public void add(int value) {
        if (size == data.length) {
            grow();
        }
        data[size] = value;
        size++;
    }

    private void grow() {
        int[] bigger = new int[data.length * 2];
        for (int i = 0; i < size; i++) {
            bigger[i] = data[i];
        }
        data = bigger;
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

    public int capacity() {
        return data.length;
    }
}
"""
TESTER = """public class ListTester {
    public static void main(String[] args) {
        IntList list = new IntList();
        for (int i = 1; i <= 5; i++) {
            list.add(i * 10);
            System.out.println("size " + list.size() + ", capacity " + list.capacity());
        }
        System.out.println(list.get(4));
    }
}
"""
TESTER2 = """public class ListTester {
    public static void main(String[] args) {
        IntList list = new IntList();
        for (int i = 1; i <= 5; i++) {
            list.add(i * 10);
        }
        System.out.println("capacity " + list.capacity());
        for (int i = 0; i < list.size(); i++) {
            System.out.print(list.get(i) + " ");
        }
        System.out.println();
    }
}
"""
BAD = """public class BadIndex {
    public static void main(String[] args) {
        IntList list = new IntList();
        list.add(7);
        System.out.println(list.get(0));
        System.out.println(list.get(1));
    }
}
"""

LESSON = {
    "id": "ds-resize",
    "title": "Resizing an array",
    "summary": "Make a list that never runs out of room: when the array is full, make a bigger one and copy everything across.",
    "goals": [
        "Tell size (values stored) from capacity (slots available)",
        "Grow a full array by doubling it and copying the values",
        "Reject bad indexes with an exception, the way Java's own lists do",
    ],
    "blocks": [
        {"type": "h", "text": "Size and capacity"},
        {"type": "p", "text": "A growable list keeps two numbers: its **size**, how many values it holds, and its **capacity**, how many slots its array has. While size is below capacity, `add` just fills the next slot. When they're equal, the array is full."},

        {"type": "h", "text": "Grow by doubling"},
        {"type": "p", "text": "An array can't get bigger, so the list makes a new, larger array, copies the values over, and switches its field to the new array. The old one is no longer referenced, and Java reclaims its memory automatically. Doubling the size each time (as Princeton's *Algorithms* textbook does) means copies happen rarely: a list that grows to a million values copies only about twenty times."},
        {"type": "code", "files": {"IntList.java": INTLIST, "ListTester.java": TESTER}, "run": "ListTester"},
        {"type": "list", "items": [
            "`grow()` is `private`: it's a helper only the list uses. Outside code just calls `add` and never needs to know the array was replaced.",
            "Capacity goes 2, 2, 4, 4, 8. It doubles only on the adds that find the array full.",
            "`data = bigger;` is the switch. From then on, the field refers to the new array.",
        ]},

        {"type": "h", "text": "Refusing a bad index"},
        {"type": "p", "text": "Slots beyond `size` exist in the array but hold no real values, so `get` must refuse them, even though the array itself wouldn't complain. `throw new IndexOutOfBoundsException(...)` stops the method and reports the problem, just as Java's `ArrayList` does. The message you pass becomes part of the crash report:"},
        {"type": "code", "files": {"IntList.java": INTLIST, "BadIndex.java": BAD}, "run": "BadIndex", "expect": "runtime",
         "after": "The array has 2 slots, so `data[1]` would have quietly returned 0, a value that was never added. The exception points at the real problem instead: the tester asked for index 1 in a list of size 1."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "resize-grow", "title": "Write grow",
         "prompt": "Finish `grow`: make a new array twice as big, copy the values, and switch to it.",
         "files": {"IntList.java": INTLIST.replace("""        int[] bigger = new int[data.length * 2];
        for (int i = 0; i < size; i++) {
            bigger[i] = data[i];
        }
        data = bigger;""", """        int[] bigger = new int[[[cap]]];
        for (int i = 0; i < size; i++) {
            [[copy]];
        }
        [[swap]];"""), "ListTester.java": TESTER2},
         "run": "ListTester",
         "output": "capacity 8\n10 20 30 40 50",
         "blanks": {
             "cap": {"accept": ["data.length * 2", "2 * data.length"], "hint": "Twice the current capacity.",
                     "wrong": [{"answer": "data.length + 1", "why": "This works, but the capacity only creeps up by one (2, 3, 4, 5), so every add after the first two triggers a full copy of the array. Doubling keeps copies rare."}]},
             "copy": {"accept": ["bigger[i] = data[i]"], "hint": "Copy slot `i` from the old array into the new one.",
                      "wrong": [{"answer": "data[i] = bigger[i]", "why": "That copies the wrong way: from the new, empty array into the old one, wiping out your values with 0s."}]},
             "swap": {"accept": ["data = bigger"], "hint": "Make the field refer to the new array.",
                      "wrong": [{"answer": "bigger = data", "why": "That points the local variable back at the old array, so the field still refers to the full one and the next write runs off its end."}]},
         },
         "explain": "Make a new array, copy each value into it, then point the field at it."},
        {"type": "quiz", "id": "resize-cap",
         "question": "An `IntList` starts with capacity 2 and doubles when full. After 9 `add` calls, what is its capacity?",
         "choices": ["9", "10", "16", "18"],
         "answer": 2,
         "explain": "It grows 2 → 4 (3rd add) → 8 (5th add) → 16 (9th add). Size is 9; capacity is 16."},
    ],
    "sources": [ALGS4_13, ARRAYS_API, ARRAYLIST_API, EXCEPTIONS_TUT],
}
