from sources import LIST_TUT, LIST_API, COLLECTION_API, ARRAYLIST_API, LINKEDLIST_API, DEV_LISTS

SWAP = """import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Swap {
    public static void fill(List<String> list) {
        list.add("b");
        list.add("c");
        list.add(0, "a");
        list.set(2, "C");
    }

    public static void main(String[] args) {
        List<String> first = new ArrayList<>();
        List<String> second = new LinkedList<>();
        fill(first);
        fill(second);
        System.out.println(first + " " + second);
        System.out.println(first.equals(second));
        System.out.println(first.get(1) + " " + second.indexOf("C"));
    }
}
"""
NOGET = """import java.util.ArrayList;
import java.util.Collection;

public class NoGet {
    public static void main(String[] args) {
        Collection<String> words = new ArrayList<>();
        words.add("only");
        System.out.println(words.get(0));
    }
}
"""
REMOVE = """import java.util.ArrayList;
import java.util.List;

public class RemoveCalls {
    public static void main(String[] args) {
        List<Integer> nums = new ArrayList<>();
        nums.add(10);
        nums.add(20);
        nums.add(30);
        nums.remove(1);
        System.out.println(nums);
        nums.remove(Integer.valueOf(10));
        System.out.println(nums);
    }
}
"""
LOOPS = """import java.util.LinkedList;
import java.util.List;

public class Loops {
    public static void main(String[] args) {
        List<String> list = new LinkedList<>();
        list.add("x");
        list.add("y");
        list.add("z");
        for (String s : list) {
            System.out.print(s + " ");
        }
        System.out.println();
        for (int i = 0; i < list.size(); i++) {
            System.out.print(list.get(i) + " ");
        }
        System.out.println();
    }
}
"""
BL = """import java.util.ArrayList;
import java.util.List;

public class Totals {
    public static int total([[ptype]] scores) {
        int sum = 0;
        for ([[elem]] s : scores) {
            sum += s;
        }
        return sum;
    }

    public static void main(String[] args) {
        [[vtype]] scores = new ArrayList<>();
        scores.add(7);
        scores.add(9);
        System.out.println(total(scores));
    }
}
"""

LESSON = {
    "id": "coll-list",
    "title": "Programming to the List interface",
    "summary": "Declare variables and parameters as `List`, create an `ArrayList` or `LinkedList`, and your code works with either. The declared type decides which methods you can call; the object decides how they run.",
    "goals": [
        "Declare collections with interface types and create them with concrete classes",
        "Use the `Collection` methods and the extra position-based `List` methods",
        "Explain why a `Collection` variable has no `get`",
        "Choose between `ArrayList` and `LinkedList` from how a list is used",
    ],
    "cos225": "Exam 2 asks general questions about collections. Knowing which methods belong to `Collection` and which to `List`, and why you'd write `List<String> x = new ArrayList<>()`, covers most of them.",
    "blocks": [
        {"type": "h", "text": "Interface on the left, class on the right"},
        {"type": "p", "text": "The usual way to create a list is `List<String> names = new ArrayList<>();`. The variable's type is the interface; only the `new` names a concrete class. Methods that take a `List` parameter accept either implementation, and switching from `ArrayList` to `LinkedList` changes one word:"},
        {"type": "code", "files": {"Swap.java": SWAP}, "run": "Swap",
         "after": "Both lists hold the same elements in the same order, so `equals` says they're equal, even though they're different classes."},

        {"type": "h", "text": "The declared type decides the methods"},
        {"type": "p", "text": "You can only call methods that the **variable's type** has. `Collection` has no positions, so it has no `get`, even when the object is an `ArrayList`:"},
        {"type": "code", "files": {"NoGet.java": NOGET}, "expect": "compile"},
        {"type": "p", "text": "This is polymorphism, as in the inheritance units: the type of the variable says what you're allowed to ask for, and the object's class decides how it's done. Use the most general type that has the methods you need: `Collection` if you only add, check and loop; `List` if you need positions."},

        {"type": "h", "text": "Collection methods and List methods"},
        {"type": "list", "items": [
            "Every `Collection`: `add(x)`, `remove(x)`, `contains(x)`, `size()`, `isEmpty()`, `clear()`, and the for-each loop.",
            "Added by `List`: `get(i)`, `set(i, x)`, `add(i, x)`, `remove(i)`, `indexOf(x)`.",
        ]},
        {"type": "p", "text": "Watch out for `remove` on a list of `Integer`s: `remove(1)` matches `remove(int index)`, while `remove(Integer.valueOf(10))` matches `remove(Object)` and removes the value 10:"},
        {"type": "code", "files": {"RemoveCalls.java": REMOVE}, "run": "RemoveCalls"},

        {"type": "h", "text": "Looping, and which list to choose"},
        {"type": "code", "files": {"Loops.java": LOOPS}, "run": "Loops",
         "after": "Both loops print the same thing. On a `LinkedList`, the for-each loop walks the nodes once (O(n)), while each `get(i)` walks from an end, so the index loop is O(n²), as you measured in unit 17. Prefer for-each when you don't need the index."},
        {"type": "list", "items": [
            "**`ArrayList`**: fast `get` and `set` by index, fast adds at the end. The usual default.",
            "**`LinkedList`**: fast adds and removes at either end, and it also implements `Deque`, so it can serve as a stack or queue. Slow `get(i)`.",
        ]},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "list-types", "title": "Choose the types",
         "prompt": "Fill in the three types so `total` accepts any list of `Integer`s.",
         "files": {"Totals.java": BL}, "run": "Totals", "output": "16",
         "blanks": {
             "ptype": {"accept": ["List<Integer>"], "hint": "The interface type, with the element type in `< >`.",
                       "wrong": [{"answer": "ArrayList<Integer>", "why": "The variable passed in is declared as a `List<Integer>`, and the compiler only knows it's a `List`, so it won't pass it where an `ArrayList` is required. Use the interface for the parameter too."}]},
             "elem": {"accept": ["int", "Integer"], "hint": "Each element is an `Integer`; unboxing lets you use `int` too."},
             "vtype": {"accept": ["List<Integer>", "ArrayList<Integer>"], "hint": "Interface on the left, class on the right.",
                       "wrong": [{"answer": "List<int>", "why": "Generic types need object types, so it's `List<Integer>`, not `List<int>`."}]},
         },
         "explain": "`List<Integer>` as the parameter and variable type lets `total` work with any list of integers."},
        {"type": "quiz", "id": "list-which-methods",
         "question": "A variable is declared `Collection<String> c = new LinkedList<>();`. Which call does **not** compile?",
         "choices": ["`c.add(\"x\")`", "`c.size()`", "`c.contains(\"x\")`", "`c.get(0)`"],
         "answer": 3,
         "explain": "`get` belongs to `List`, not `Collection`. The object is a `LinkedList`, but the compiler only knows it as a `Collection`."},
        {"type": "quiz", "id": "list-why",
         "question": "Why write `List<String> names = new ArrayList<>();` rather than `ArrayList<String> names = new ArrayList<>();`?",
         "choices": ["It runs faster", "The rest of the code only depends on `List`, so you can switch to another `List` implementation by changing one line", "`ArrayList` variables can't hold strings", "It uses less memory"],
         "answer": 1,
         "explain": "Programming to the interface keeps the choice of implementation in one place."},
    ],
    "sources": [LIST_TUT, LIST_API, COLLECTION_API, ARRAYLIST_API, LINKEDLIST_API, DEV_LISTS],
}
