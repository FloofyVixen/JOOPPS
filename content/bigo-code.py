from sources import ALGS4_14, OPENDSA_ANAL, ARRAYLIST_API

PATTERNS = """public class Patterns {
    public static long fixedLoop(int n) {
        long steps = 0;
        for (int i = 0; i < 10; i++) {
            steps++;
        }
        return steps;
    }

    public static long twoLoops(int n) {
        long steps = 0;
        for (int i = 0; i < n; i++) {
            steps++;
        }
        for (int i = 0; i < n; i++) {
            steps++;
        }
        return steps;
    }

    public static long nestedLoops(int n) {
        long steps = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                steps++;
            }
        }
        return steps;
    }

    public static long halving(int n) {
        long steps = 0;
        while (n > 1) {
            n = n / 2;
            steps++;
        }
        return steps;
    }

    public static void main(String[] args) {
        for (int n = 1000; n <= 1000000; n *= 1000) {
            System.out.println("n = " + n);
            System.out.println("  fixed loop:   " + fixedLoop(n));
            System.out.println("  two loops:    " + twoLoops(n));
            System.out.println("  halving:      " + halving(n));
        }
        System.out.println("nested loops, n = 1000: " + nestedLoops(1000));
    }
}
"""
HIDDEN = """import java.util.ArrayList;

public class Hidden {
    public static int countShared(ArrayList<Integer> a, ArrayList<Integer> b) {
        int shared = 0;
        for (int value : a) {
            if (b.contains(value)) {
                shared++;
            }
        }
        return shared;
    }

    public static void main(String[] args) {
        ArrayList<Integer> a = new ArrayList<>();
        ArrayList<Integer> b = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            a.add(i);
            b.add(i * 2);
        }
        System.out.println(countShared(a, b));
    }
}
"""
TRI = """public class Triangle {
    public static void main(String[] args) {
        int n = 5;
        int steps = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                steps++;
            }
        }
        System.out.println(steps);
    }
}
"""

ITEMS = [
    {"code": "static int first(int[] data) {\n    return data[0];\n}", "answer": "O(1)",
     "why": "One array read, however long the array is."},
    {"code": "static int sum(int[] data) {\n    int total = 0;\n    for (int i = 0; i < data.length; i++) {\n        total += data[i];\n    }\n    return total;\n}",
     "answer": "O(n)", "why": "One loop that visits each value once."},
    {"code": "static boolean hasDuplicate(int[] data) {\n    for (int i = 0; i < data.length; i++) {\n        for (int j = i + 1; j < data.length; j++) {\n            if (data[i] == data[j]) {\n                return true;\n            }\n        }\n    }\n    return false;\n}",
     "answer": "O(n²)", "why": "A loop inside a loop: every pair is compared. Starting `j` at `i + 1` halves the work, but n²/2 is still O(n²)."},
    {"code": "static int digitsInBinary(int n) {\n    int count = 1;\n    while (n > 1) {\n        n = n / 2;\n        count++;\n    }\n    return count;\n}",
     "answer": "O(log n)", "why": "`n` is halved each time round, so doubling `n` adds only one more step."},
    {"code": "static int firstTenSum(int[] data) {\n    int total = 0;\n    for (int i = 0; i < 10 && i < data.length; i++) {\n        total += data[i];\n    }\n    return total;\n}",
     "answer": "O(1)", "why": "The loop runs at most 10 times, however long the array is. A loop isn't automatically O(n): it depends on what it counts up to."},
    {"code": "static int range(int[] data) {\n    int min = data[0];\n    for (int value : data) {\n        min = Math.min(min, value);\n    }\n    int max = data[0];\n    for (int value : data) {\n        max = Math.max(max, value);\n    }\n    return max - min;\n}",
     "answer": "O(n)", "why": "Two loops one after the other: n + n = 2n steps, which is O(n). Only loops **inside** loops multiply."},
]

LESSON = {
    "id": "bigo-code",
    "title": "Reading big O from code",
    "summary": "You can usually see an algorithm's big O from the shape of its loops: no loop, one loop, a loop inside a loop.",
    "goals": [
        "Recognise O(1), O(n) and O(n²) code by its loops",
        "Tell loops in sequence (add) from nested loops (multiply)",
        "Spot a halving loop (O(log n)) and a fixed-size loop (O(1))",
        "Count the cost of method calls inside a loop",
    ],
    "cos225": "The Exam 2 guide asks how O(1), O(n) and O(n²) look in code (no loop, one loop, nested loops), and how they compare. Expect a matching question pairing code with its big O.",
    "blocks": [
        {"type": "h", "text": "Look at the loops"},
        {"type": "p", "text": "Big O counts how the work grows with `n`, the size of the input. Most of the work in a method happens in its loops, so start there:"},
        {"type": "list", "items": [
            "**No loop** over the input: **O(1)**. A fixed number of steps.",
            "**One loop** over the input: **O(n)**. Each value is visited once.",
            "**A loop inside a loop**, both over the input: **O(n²)**. For each of the n values, the inner loop does n more steps.",
        ]},
        {"type": "p", "text": "Three more patterns need a closer look. This program counts the steps of each:"},
        {"type": "code", "files": {"Patterns.java": PATTERNS}, "run": "Patterns"},
        {"type": "list", "items": [
            "**A loop with a fixed limit** (`i < 10`) does the same work at any size: **O(1)**. Check what a loop counts up to, not just that there is one.",
            "**Two loops one after the other** add: n + n = 2n, still **O(n)**. A thousand times more input means a thousand times more steps.",
            "**A loop that halves** `n` grows by one step each time `n` doubles: **O(log n)**. A million needs only 19 halvings.",
            "**Nested loops** multiply: 1000 × 1000 is a million steps.",
        ]},

        {"type": "h", "text": "Triangles are still quadratic"},
        {"type": "p", "text": "A common nested loop starts the inner loop at `i + 1`, so it compares each pair only once. That does about half the work of a full square:"},
        {"type": "code", "files": {"Triangle.java": TRI}, "run": "Triangle",
         "after": "For n = 5 that's 4 + 3 + 2 + 1 + 0 = 10 steps, which is n(n − 1)/2. Dropping the constant ½ and the smaller term leaves **O(n²)**."},

        {"type": "h", "text": "Hidden loops in method calls"},
        {"type": "p", "text": "A method call costs whatever that method does. `ArrayList.contains` has to search the list, which the Java documentation says takes linear time. Calling it inside a loop puts a loop inside a loop:"},
        {"type": "code", "files": {"Hidden.java": HIDDEN}, "run": "Hidden",
         "after": "The `for` loop runs n times, and each `contains` can look at all n values of `b`. So `countShared` is **O(n²)**, though you only see one loop."},
        {"type": "p", "text": "By contrast, `get(i)`, `size()` and `add` at the end of an `ArrayList` are O(1) (adding is O(1) on average, since growing is rare), so a loop that calls only those stays O(n)."},

        {"type": "h", "text": "Practice"},
        {"type": "match", "id": "bigo-code-match",
         "prompt": "Match each method with its big O, where n is the length of the array (or the value of `n`).",
         "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
         "items": ITEMS,
         "explain": "No loop or a fixed loop: O(1). A halving loop: O(log n). Loops over the data in sequence: O(n). Nested loops over the data: O(n²)."},
        {"type": "quiz", "id": "bigo-code-index",
         "question": "A method loops `for (int i = 0; i < n; i++)` and inside calls `list.indexOf(x)` on an `ArrayList` of n values. What is its big O?",
         "choices": ["O(1)", "O(n)", "O(n log n)", "O(n²)"],
         "answer": 3,
         "explain": "`indexOf` searches the list, which is O(n). Doing that n times is n × n: O(n²)."},
        {"type": "quiz", "id": "bigo-code-compare",
         "question": "Method A is O(n) and method B is O(n²). For a large input, which statement is true?",
         "choices": ["A is always faster, at every size", "B will eventually take much longer than A as n grows", "They take the same time, since both have loops", "B is faster, because n² is a smaller number"],
         "answer": 1,
         "explain": "Big O describes growth. For small n, B might even be faster, but as n grows, n² outgrows n and B falls further and further behind."},
    ],
    "sources": [ALGS4_14, OPENDSA_ANAL, ARRAYLIST_API],
}
