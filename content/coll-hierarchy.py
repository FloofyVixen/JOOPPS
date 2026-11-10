from sources import COLL_IFACES, COLL_SUMMARY, COLLECTION_API, LIST_API, ABSTRACTLIST_API, ARRAYLIST_API, LINKEDLIST_API, ABSTRACT_TUT, JLS_IFACES

KINDS = """import java.util.AbstractList;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;
import java.util.List;

public class Kinds {
    public static void main(String[] args) {
        ArrayList<String> array = new ArrayList<>();
        LinkedList<String> linked = new LinkedList<>();

        System.out.println(array instanceof List);
        System.out.println(array instanceof Collection);
        System.out.println(linked instanceof List);
        System.out.println(array instanceof AbstractList);
        System.out.println(array.getClass().getSuperclass());
    }
}
"""
NEWLIST = """import java.util.List;

public class NewList {
    public static void main(String[] args) {
        List<String> names = new List<>();
    }
}
"""
NEWABS = """import java.util.AbstractList;

public class NewAbstract {
    public static void main(String[] args) {
        AbstractList<String> names = new AbstractList<>();
    }
}
"""
COLL = """import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;

public class AnyCollection {
    public static int countLonger(Collection<String> words, int length) {
        int count = 0;
        for (String w : words) {
            if (w.length() > length) {
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        Collection<String> a = new ArrayList<>();
        Collection<String> b = new LinkedList<>();
        for (String w : new String[] {"queue", "list", "stack", "node"}) {
            a.add(w);
            b.add(w);
        }
        System.out.println(countLonger(a, 4) + " " + countLonger(b, 4));
        System.out.println(a.contains("node") + " " + a.size() + " " + a.isEmpty());
    }
}
"""

ITEMS = [
    ("`Collection`", "Interface"),
    ("`List`", "Interface"),
    ("`ArrayList`", "Concrete class"),
    ("`LinkedList`", "Concrete class"),
    ("`AbstractList`", "Abstract class"),
    ("`QueueADT`, from this course", "Interface"),
    ("`ArrayStack`, from this course", "Concrete class"),
]

LESSON = {
    "id": "coll-hierarchy",
    "title": "The Collection hierarchy",
    "summary": "Java's collection classes fit into a hierarchy of interfaces and classes. At the top is the `Collection` interface; `List` extends it; `ArrayList` and `LinkedList` are the concrete classes you actually create.",
    "goals": [
        "Draw the hierarchy Collection → List → ArrayList and LinkedList",
        "Tell an interface, an abstract class and a concrete class apart, and say which can be instantiated",
        "Place `AbstractList` in the hierarchy and say what it's for",
    ],
    "cos225": "The Exam 2 guide keeps collections to general questions: the hierarchy Collection → List → ArrayList/LinkedList, and the difference between an interface (Collection, List), an abstract class and a concrete class (ArrayList). Sets and Maps aren't on it, so they aren't here either.",
    "blocks": [
        {"type": "h", "text": "One family of types"},
        {"type": "p", "text": "Everything you've built in this half of the course (lists, stacks, queues) holds a group of values. Java's own versions are organised as the **Collections Framework**: a set of interfaces that say what each kind of collection can do, and classes that implement them."},
        {"type": "list", "items": [
            "**`Collection<E>`** (interface): any group of elements. Methods such as `add`, `remove`, `contains`, `size`, `isEmpty`, and looping with for-each.",
            "**`List<E>`** (interface, extends `Collection`): an ordered collection with positions. Adds `get(i)`, `set(i, x)`, `add(i, x)`, `remove(i)`, `indexOf`.",
            "**`ArrayList<E>`** and **`LinkedList<E>`** (concrete classes): two implementations of `List`, one on a resizable array, one on linked nodes.",
        ]},
        {"type": "p", "text": "Between `List` and `ArrayList` sits **`AbstractList<E>`**, an abstract class. It implements most of `List` on top of a few methods it leaves abstract (`get` and `size`), so a concrete list class only has to fill those in. `ArrayList` extends it."},
        {"type": "code", "files": {"Kinds.java": KINDS}, "run": "Kinds",
         "after": "An `ArrayList` **is a** `List` and **is a** `Collection`, because `List` extends `Collection`. Its superclass is `AbstractList`."},

        {"type": "h", "text": "Interface, abstract class, concrete class"},
        {"type": "p", "text": "These are the three kinds of type you met in the inheritance units, and the collections use all three:"},
        {"type": "list", "items": [
            "An **interface** (`Collection`, `List`) lists methods a type must have. It can't be instantiated with `new`.",
            "An **abstract class** (`AbstractList`) is a partly written class: it can have fields and finished methods, but some methods are abstract. It can't be instantiated either; it exists to be extended.",
            "A **concrete class** (`ArrayList`, `LinkedList`) has every method written. It's the only kind you can create with `new`.",
        ]},
        {"type": "error", "id": "coll-new-list", "expect": "compile",
         "prompt": "This tries to create a `List` directly.",
         "files": {"NewList.java": NEWLIST},
         "question": "Why won't it compile?",
         "choices": ["`List` needs a size, like `new List<>(10)`", "`List` is an interface, so it can't be instantiated; create a concrete class such as `ArrayList`", "The variable should be called `list`", "`List` must be imported as `java.util.List.*`"],
         "answer": 1,
         "explain": "Interfaces describe a type but have no constructor. The compiler calls `List` abstract because every interface is implicitly abstract. Keep the variable's type as `List<String>` and create an `ArrayList` (or `LinkedList`).",
         "fix": [["NewList.java", "new List<>()", "new ArrayList<>()"], ["NewList.java", "import java.util.List;", "import java.util.ArrayList;\nimport java.util.List;"]],
         "fixed_output": ""},
        {"type": "error", "id": "coll-new-abstract", "expect": "compile",
         "prompt": "And this tries to create an `AbstractList`.",
         "files": {"NewAbstract.java": NEWABS},
         "question": "What does the compiler say?",
         "choices": ["Nothing; abstract classes can be instantiated", "That `AbstractList` is abstract and cannot be instantiated", "That `AbstractList` is a final class", "That generics aren't allowed with abstract classes"],
         "answer": 1,
         "explain": "An abstract class can't be created with `new`. A variable of type `AbstractList` can still refer to an `ArrayList`, because `ArrayList` extends it. (In this unit's tasks, you'll extend `AbstractList` yourself.)",
         "fix": [["NewAbstract.java", "new AbstractList<>()", "new ArrayList<>()"], ["NewAbstract.java", "import java.util.AbstractList;", "import java.util.AbstractList;\nimport java.util.ArrayList;"]],
         "fixed_output": ""},

        {"type": "h", "text": "Code that takes any collection"},
        {"type": "p", "text": "A method whose parameter is `Collection<String>` accepts an `ArrayList`, a `LinkedList`, or any other collection of strings, because it only uses methods every `Collection` has:"},
        {"type": "code", "files": {"AnyCollection.java": COLL}, "run": "AnyCollection"},
        {"type": "p", "text": "The `Queue` and `Deque` you used in units 13 to 20 are also interfaces that extend `Collection`, and `ArrayDeque` and `LinkedList` implement them. That's why a `Queue` has `size()` and `isEmpty()` too."},

        {"type": "h", "text": "Practice"},
        {"type": "match", "id": "coll-kinds",
         "prompt": "Is each type an interface, an abstract class or a concrete class?",
         "options": ["Interface", "Abstract class", "Concrete class"],
         "items": [{"text": t, "answer": a} for t, a in ITEMS],
         "explain": "Only concrete classes can be instantiated. Interfaces and abstract classes are used as variable and parameter types, and as things to implement or extend."},
        {"type": "quiz", "id": "coll-order",
         "question": "Which line shows the hierarchy from most general to most specific?",
         "choices": ["ArrayList → List → Collection", "Collection → List → ArrayList", "List → Collection → ArrayList", "Collection → ArrayList → List"],
         "answer": 1,
         "explain": "`Collection` is the most general; `List` extends it; `ArrayList` implements `List` (by way of `AbstractList`)."},
        {"type": "quiz", "id": "coll-which-new",
         "question": "Which of these compiles?",
         "choices": ["`Collection<Integer> c = new Collection<>();`", "`List<Integer> c = new List<>();`", "`List<Integer> c = new LinkedList<>();`", "`AbstractList<Integer> c = new AbstractList<>();`"],
         "answer": 2,
         "explain": "Only `LinkedList` is a concrete class. The variable can still have an interface type."},
    ],
    "sources": [COLL_IFACES, COLL_SUMMARY, COLLECTION_API, LIST_API, ABSTRACTLIST_API, ARRAYLIST_API, LINKEDLIST_API, ABSTRACT_TUT, JLS_IFACES],
}
