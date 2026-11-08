from sources import GENERICS_TUT, GENERICS_WHY, ARRAYLIST_API, HEL_12_1

BOX = """public class Box<T> {
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
}
"""
BOXT = """public class BoxTester {
    public static void main(String[] args) {
        Box<String> note = new Box<>();
        System.out.println(note.isEmpty());
        note.put("Buy milk");
        String text = note.get();
        System.out.println(text.length() + " characters: " + text);

        Box<Integer> count = new Box<>();
        count.put(42);
        int n = count.get();
        System.out.println(n + 1);
    }
}
"""
GLIST = """public class GrowList<T> {
    private Object[] data;
    private int size;

    public GrowList() {
        data = new Object[2];
        size = 0;
    }

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
}
"""
GLT = """public class GrowListTester {
    public static void main(String[] args) {
        GrowList<String> words = new GrowList<>();
        words.add("stack");
        words.add("queue");
        words.add("tree");
        for (int i = 0; i < words.size(); i++) {
            System.out.println(words.get(i).toUpperCase());
        }

        GrowList<Double> prices = new GrowList<>();
        prices.add(2.5);
        prices.add(4.0);
        System.out.println(prices.get(0) + prices.get(1));
    }
}
"""

LESSON = {
    "id": "ds-generics",
    "title": "Generic classes with <T>",
    "summary": "Write a data structure once and use it for any type of item, with the compiler checking that the types match.",
    "goals": [
        "Write a generic class with a type parameter `<T>`",
        "Create objects of a generic class for different types, using wrapper types like `Integer` for numbers",
        "Build a growable list that works for any type",
    ],
    "blocks": [
        {"type": "h", "text": "One class, any type"},
        {"type": "p", "text": "`IntList` from the previous lesson only holds `int`s. A list of names or songs would need another copy of the same code. A **generic class** takes a **type parameter**, a placeholder written in angle brackets like `<T>`, and the code uses `T` wherever the item type goes. Each time you create an object, you say what `T` is."},
        {"type": "code", "files": {"Box.java": BOX, "BoxTester.java": BOXT}, "run": "BoxTester"},
        {"type": "list", "items": [
            "`public class Box<T>` declares the type parameter. `T` is just a name; single capital letters are the convention.",
            "`Box<String> note` is a box of `String`s, so `note.get()` returns a `String` and you can call `length()` on it without a cast.",
            "`new Box<>()` lets Java fill in the type from the variable. The empty `<>` is called the diamond.",
            "Type parameters must be classes, not primitives, so a box of numbers is `Box<Integer>`. Java converts between `int` and `Integer` automatically (this is called **autoboxing**), which is why `count.put(42)` and `int n = count.get()` work.",
        ]},
        {"type": "p", "text": "The compiler holds every box to its type. Putting a number in a box of strings is caught before the program ever runs:"},
        {"type": "code", "files": {"Box.java": BOX, "WrongType.java": """public class WrongType {
    public static void main(String[] args) {
        Box<String> note = new Box<>();
        note.put(42);
    }
}
"""}, "run": "WrongType", "expect": "compile"},

        {"type": "h", "text": "A generic growable list"},
        {"type": "p", "text": "Here is `IntList` turned into `GrowList<T>`. One wrinkle: Java doesn't allow `new T[...]`, because at run time it no longer knows what `T` is. The standard workaround, used in many textbooks and similar to what `ArrayList` does inside, is to store the items in an `Object[]` and cast each one back to `T` in `get`."},
        {"type": "code", "files": {"GrowList.java": GLIST, "GrowListTester.java": GLT}, "run": "GrowListTester"},
        {"type": "list", "items": [
            "`(T) data[index]` is safe here because `add` only accepts `T`s. But the compiler can't prove it, so it would print a warning note. `@SuppressWarnings(\"unchecked\")` tells it this cast was checked by hand.",
            "`GrowList<String>` and `GrowList<Double>` are the same code, used for two types. This is how `ArrayList<E>` works.",
        ]},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "gen-pair", "title": "A generic pair",
         "prompt": "`Pair` holds two values of the same type. Fill in the type parameter's uses.",
         "files": {"Pair.java": """public class Pair[[decl]] {
    private T first;
    private T second;

    public Pair(T first, T second) {
        this.first = first;
        this.second = second;
    }

    public [[rtype]] getFirst() {
        return first;
    }

    public T getSecond() {
        return second;
    }
}
""", "PairTester.java": """public class PairTester {
    public static void main(String[] args) {
        Pair<String> names = new Pair<>("Ana", "Sam");
        System.out.println(names.getFirst() + " & " + names.getSecond());
        [[use]] scores = new Pair<>(90, 85);
        System.out.println(scores.getFirst() + scores.getSecond());
    }
}
"""},
         "run": "PairTester", "output": "Ana & Sam\n175",
         "blanks": {
             "decl": {"accept": ["<T>"], "hint": "Declare the type parameter after the class name.",
                      "wrong": [{"answer": "", "why": "Without `<T>` on the class, Java doesn't know what `T` is: \"cannot find symbol: class T\"."}]},
             "rtype": {"accept": ["T"], "hint": "`first` has type `T`.",
                       "wrong": [{"answer": "Object", "why": "This compiles, but then `getFirst()` returns `Object`, so `scores.getFirst() + scores.getSecond()` can't add an `Object` to an `Integer`. Returning `T` keeps the real type."}]},
             "use": {"accept": ["Pair<Integer>"], "hint": "A pair of whole numbers. Remember: type parameters need a class, not a primitive.",
                     "wrong": [{"answer": "Pair<int>", "why": "Type arguments must be reference types. Use the wrapper class `Integer`."}]},
         },
         "explain": "`Pair<Integer>` makes both getters return `Integer`, so adding them gives 175."},
        {"type": "quiz", "id": "gen-why",
         "question": "What's the main benefit of `GrowList<String>` over a list that stores plain `Object`s?",
         "choices": ["It runs faster", "The compiler rejects non-`String` items, and `get` returns a `String` with no cast", "It can hold primitives directly", "It never needs to grow"],
         "answer": 1,
         "explain": "Generics move type mistakes from run time (a crash when you cast) to compile time (an error before the program runs), and remove casts from the code that uses the list."},
    ],
    "sources": [GENERICS_TUT, GENERICS_WHY, ARRAYLIST_API, HEL_12_1],
}
