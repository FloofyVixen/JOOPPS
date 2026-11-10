from sources import ALGS4_14, OPENDSA_ANAL

STEPS = """public class StepCount {
    // Each method returns how many basic steps it takes for input size n.
    public static long constant(int n) {
        long steps = 0;
        steps++;  // look at one value
        return steps;
    }

    public static long linear(int n) {
        long steps = 0;
        for (int i = 0; i < n; i++) {
            steps++;
        }
        return steps;
    }

    public static long quadratic(int n) {
        long steps = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                steps++;
            }
        }
        return steps;
    }

    public static void main(String[] args) {
        for (int n = 10; n <= 10000; n *= 10) {
            System.out.println("n = " + n + ": " + constant(n) + ", " + linear(n) + ", " + quadratic(n));
        }
    }
}
"""
TERMS = """public class Terms {
    public static void main(String[] args) {
        for (long n = 10; n <= 100000; n *= 10) {
            long total = 3 * n * n + 5 * n + 2;
            long biggest = 3 * n * n;
            System.out.println("n = " + n + ": total " + total + ", the 3n^2 term is "
                    + (100 * biggest / total) + "% of it");
        }
    }
}
"""
TABLE = """public class Growth {
    // How many times n can be halved before reaching 1: log base 2 of n.
    public static int log2(int n) {
        int count = 0;
        while (n > 1) {
            n = n / 2;
            count++;
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println("n\\tlog n\\tn log n\\tn^2\\t2^n");
        for (int n = 2; n <= 32; n *= 2) {
            long twoToN = 1;
            for (int k = 0; k < n; k++) {
                twoToN *= 2;
            }
            System.out.println(n + "\\t" + log2(n) + "\\t" + (n * log2(n)) + "\\t" + (n * n) + "\\t" + twoToN);
        }
    }
}
"""

LESSON = {
    "id": "bigo-growth",
    "title": "Growth rates and the big six",
    "summary": "Big O describes how an algorithm's work grows as its input grows. Six growth rates cover almost everything in this course, and they always rank in the same order.",
    "goals": [
        "Explain that big O is about growth rate, not exact speed",
        "Drop constants and smaller terms to find an algorithm's big O",
        "Name the six common growth rates and rank them from best to worst",
    ],
    "cos225": "The Exam 2 guide says the point of big O is **growth rate**, asks for the \"big six\" categories and their order from best to worst, and loves matching problems. This lesson covers all three.",
    "blocks": [
        {"type": "h", "text": "Counting steps, not seconds"},
        {"type": "p", "text": "The same program runs faster on a fast computer, so seconds don't tell you much about an algorithm. Instead, count its basic steps (comparisons, assignments, array reads) as a function of the input size, `n`. Then ask: when `n` gets bigger, how fast does the count grow?"},
        {"type": "p", "text": "These three methods do one step, `n` steps and `n × n` steps:"},
        {"type": "code", "files": {"StepCount.java": STEPS}, "run": "StepCount"},
        {"type": "p", "text": "Multiply `n` by 10 and the constant method doesn't change, the linear one does 10 times more work, and the quadratic one does 100 times more. That pattern of growth is what **big O** describes. It's the point of big O: not how long something takes, but how its cost **grows** as the input grows."},

        {"type": "h", "text": "Only the biggest term matters"},
        {"type": "p", "text": "Suppose you count the steps of an algorithm exactly and get 3n² + 5n + 2. For small `n`, every part counts. As `n` grows, the n² term takes over:"},
        {"type": "code", "files": {"Terms.java": TERMS}, "run": "Terms"},
        {"type": "p", "text": "So big O keeps only the fastest-growing term and drops its constant: 3n² + 5n + 2 is **O(n²)**. The constant 3 is dropped too, because it doesn't change the shape of the growth: double `n` and 3n² still quadruples, just as n² does."},
        {"type": "list", "items": [
            "5n + 100 is O(n).",
            "n²/2 + n is O(n²).",
            "1000 is O(1): it doesn't grow at all.",
        ]},

        {"type": "h", "text": "The big six"},
        {"type": "p", "text": "Most algorithms you'll meet fall into one of six growth rates. From best (slowest growing) to worst:"},
        {"type": "list", "items": [
            "**O(1), constant**: the same work at any size. Reading `array[i]`, pushing onto an array stack.",
            "**O(log n), logarithmic**: the work grows by one step each time `n` doubles. Anything that halves the problem each step, such as binary search.",
            "**O(n), linear**: work in step with `n`. One loop over the data: summing an array, finding the largest value.",
            "**O(n log n), linearithmic**: a little more than linear. Fast sorting algorithms, such as merge sort.",
            "**O(n²), quadratic**: a loop inside a loop over the data. Comparing every pair of values.",
            "**O(2ⁿ), exponential**: the work doubles each time `n` grows by one. Trying every possible subset of `n` items.",
        ]},
        {"type": "p", "text": "This program prints each growth rate for a few sizes. `log2` counts how many times `n` can be halved before it reaches 1, which is what log base 2 means:"},
        {"type": "code", "files": {"Growth.java": TABLE}, "run": "Growth"},
        {"type": "p", "text": "By n = 32, the exponential column is already in the billions, while log n has only reached 5. The order never changes once `n` is big enough:"},
        {"type": "note", "label": "Best to worst", "text": "O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)"},
        {"type": "p", "text": "Princeton's *Algorithms* table also lists **cubic**, O(n³), three nested loops, which sits between quadratic and exponential. The exam guide's three main categories are constant, linear and quadratic; the next lesson shows how each looks in code."},

        {"type": "h", "text": "Practice"},
        {"type": "match", "id": "bigo-names",
         "prompt": "Match each growth rate with its name.",
         "options": ["constant", "logarithmic", "linear", "linearithmic", "quadratic", "exponential"],
         "items": [
             {"text": "O(n²)", "answer": "quadratic"},
             {"text": "O(1)", "answer": "constant"},
             {"text": "O(2ⁿ)", "answer": "exponential"},
             {"text": "O(n)", "answer": "linear"},
             {"text": "O(log n)", "answer": "logarithmic"},
             {"text": "O(n log n)", "answer": "linearithmic"},
         ]},
        {"type": "match", "id": "bigo-simplify",
         "prompt": "Each expression counts an algorithm's steps. Match it with its big O.",
         "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"],
         "items": [
             {"text": "4n + 7", "answer": "O(n)", "why": "Drop the constant 7 and the factor 4."},
             {"text": "n² + 1000n", "answer": "O(n²)", "why": "n² eventually outgrows 1000n (once n is over 1000)."},
             {"text": "500", "answer": "O(1)", "why": "It doesn't depend on n at all."},
             {"text": "2ⁿ + n³", "answer": "O(2ⁿ)", "why": "Exponential outgrows any power of n."},
             {"text": "3 log n + 2", "answer": "O(log n)"},
             {"text": "n log n + n", "answer": "O(n log n)", "why": "n log n grows faster than n, since log n keeps growing."},
         ]},
        {"type": "quiz", "id": "bigo-double",
         "question": "An O(n²) method takes 2 seconds when n is 1,000. Roughly how long would you expect it to take when n is 2,000?",
         "choices": ["2 seconds", "4 seconds", "8 seconds", "4,000 seconds"],
         "answer": 2,
         "explain": "Doubling n multiplies n² by 4, so 2 seconds becomes about 8. An O(n) method would take about 4 seconds; an O(1) method, still 2."},
        {"type": "quiz", "id": "bigo-point",
         "question": "What does big O tell you about an algorithm?",
         "choices": ["Exactly how many seconds it takes", "How its work grows as the input gets larger", "How much memory the computer has", "The number of lines of code"],
         "answer": 1,
         "explain": "Big O is about growth rate: how the cost changes as `n` grows, ignoring constants that depend on the computer."},
    ],
    "sources": [ALGS4_14, OPENDSA_ANAL],
}
