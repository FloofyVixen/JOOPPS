from sources import ARRAYS_TUT, ARRAYS_API, JLS_ARRAY_CREATE, ALGS4_13

ALIAS = """public class Alias {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = a;
        b[0] = 99;
        System.out.println(a[0]);

        int[] c = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            c[i] = a[i];
        }
        c[1] = 50;
        System.out.println(a[1] + " " + c[1]);
    }
}
"""
TOOLS = """import java.util.Arrays;

public class ArrayTools {
    public static void main(String[] args) {
        int[] a = {4, 8, 15};
        int[] b = {4, 8, 15};
        System.out.println(a);
        System.out.println(Arrays.toString(a));
        System.out.println(a == b);
        System.out.println(Arrays.equals(a, b));

        int[] bigger = Arrays.copyOf(a, 5);
        System.out.println(Arrays.toString(bigger));
    }
}
"""
SHIFT = """import java.util.Arrays;

public class Shift {
    public static void main(String[] args) {
        int[] data = {10, 20, 30, 40, 0};
        int size = 4;

        int index = 1;
        for (int i = size; i > index; i--) {
            data[i] = data[i - 1];
        }
        data[index] = 15;
        size++;

        System.out.println(Arrays.toString(data) + " size " + size);
    }
}
"""

LESSON = {
    "id": "ds-memory",
    "title": "Arrays in memory",
    "summary": "What an array variable really holds, why copying one is trickier than it looks, and what inserting in the middle costs.",
    "goals": [
        "Explain that an array variable holds a reference to the array",
        "Copy an array properly, and compare arrays by content",
        "Insert into the middle of an array by shifting elements",
    ],
    "blocks": [
        {"type": "h", "text": "One block, fixed size, fast to index"},
        {"type": "p", "text": "An array is one block of memory split into equal-sized slots, one after another. Because every slot is the same size, Java can jump straight to slot `i` without looking at the others, so reading `data[500]` is as fast as reading `data[0]`. The price is that the size is fixed when the array is created."},

        {"type": "h", "text": "An array variable is a reference"},
        {"type": "p", "text": "Like an object variable, an array variable doesn't contain the array. It **refers** to it. So `int[] b = a;` doesn't copy anything: `a` and `b` are two names for the same array. To get an independent copy, create a new array and copy the values over."},
        {"type": "predict", "id": "mem-alias",
         "prompt": "What does this print?",
         "files": {"Alias.java": ALIAS}, "run": "Alias",
         "choices": ["1\n2 50", "99\n2 50", "99\n50 50", "1\n50 50"],
         "answer": 1,
         "explain": "`b = a` makes `b` refer to the same array, so changing `b[0]` changes what `a[0]` shows. `c` is a new array filled by the loop, so changing `c[1]` leaves `a` alone."},
        {"type": "p", "text": "The `java.util.Arrays` class has helpers for the things that don't work the way you might expect:"},
        {"type": "code", "files": {"ArrayTools.java": TOOLS}, "run": "ArrayTools",
         "after": "Printing an array directly shows its type code (`[I` means \"array of int\") and a hash number, which will be different on your machine. `Arrays.toString` shows the contents. `==` asks whether two variables refer to the same array; `Arrays.equals` compares the contents. `Arrays.copyOf` makes a new array (here, a longer one, padded with 0s)."},

        {"type": "h", "text": "Inserting means shifting"},
        {"type": "p", "text": "A partly filled array, with a `size` that counts the used slots, has no gap in the middle. To insert at position 1, every value from position 1 onward must move one slot to the right first. Work from the end backwards, so that nothing gets overwritten before it has moved."},
        {"type": "code", "files": {"Shift.java": SHIFT}, "run": "Shift"},
        {"type": "p", "text": "Inserting near the front of a big array moves almost every element. That's a real cost, and it's one reason later units introduce linked structures, which can insert without shifting."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "mem-remove", "title": "Remove by shifting left",
         "prompt": "Remove the value at `index` by shifting everything after it one slot to the left.",
         "files": {"RemoveAt.java": """import java.util.Arrays;

public class RemoveAt {
    public static void main(String[] args) {
        int[] data = {10, 15, 20, 30, 40};
        int size = 5;

        int index = 1;
        for (int i = index; i < [[end]]; i++) {
            data[i] = data[[[from]]];
        }
        size--;
        data[size] = 0;

        System.out.println(Arrays.toString(data) + " size " + size);
    }
}
"""},
         "run": "RemoveAt", "output": "[10, 20, 30, 40, 0] size 4",
         "blanks": {
             "end": {"accept": ["size - 1"], "hint": "The last slot that receives a value is the second-to-last used one.",
                     "wrong": [{"answer": "size", "why": "On the last pass, `i` is 4, so the loop reads `data[5]`, which doesn't exist. Stop at `size - 1`."}]},
             "from": {"accept": ["i + 1"], "hint": "Each slot takes the value from its right-hand neighbor.",
                      "wrong": [{"answer": "i - 1", "why": "That copies from the left, so the value at `index - 1` spreads across the array instead of the gap closing."}]},
         },
         "explain": "Removing is the mirror image of inserting: go left to right, and each slot takes its right-hand neighbor's value."},
        {"type": "quiz", "id": "mem-fast",
         "question": "Which operation on an array of 1,000,000 values is fastest?",
         "choices": ["Inserting a value at index 0", "Reading the value at index 999,999", "Removing the value at index 0", "Making the array one slot bigger"],
         "answer": 1,
         "explain": "Indexing jumps straight to the slot. Inserting or removing at the front shifts nearly every value, and an array can't grow: you'd have to create a new one and copy everything."},
    ],
    "sources": [ARRAYS_TUT, ARRAYS_API, JLS_ARRAY_CREATE, ALGS4_13],
}
