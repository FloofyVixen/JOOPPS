from sources import ALGS4_14, OPENDSA_ANAL

THREE = """public class ThreeWays {
    // O(1): one array read, no loop.
    public static int last(int[] data) {
        return data[data.length - 1];
    }

    // O(n): one pass, keeping a running total.
    public static double average(int[] data) {
        int total = 0;
        for (int i = 0; i < data.length; i++) {
            total += data[i];
        }
        return (double) total / data.length;
    }

    // O(n^2): try every pair i < j.
    public static int pairsWithSum(int[] data, int target) {
        int count = 0;
        for (int i = 0; i < data.length; i++) {
            for (int j = i + 1; j < data.length; j++) {
                if (data[i] + data[j] == target) {
                    count++;
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        int[] data = {4, 9, 1, 6, 5};
        System.out.println(last(data));
        System.out.println(average(data));
        System.out.println(pairsWithSum(data, 10));
    }
}
"""
SUMS = """public class SumTo {
    // O(n): add 1 + 2 + ... + n one at a time.
    public static long loopSum(int n) {
        long total = 0;
        for (int i = 1; i <= n; i++) {
            total += i;
        }
        return total;
    }

    // O(1): the same answer from a formula.
    public static long formulaSum(int n) {
        return (long) n * (n + 1) / 2;
    }

    public static void main(String[] args) {
        System.out.println(loopSum(100) + " " + formulaSum(100));
        System.out.println(loopSum(1000000) + " " + formulaSum(1000000));
    }
}
"""
MAXB = """public class Largest {
    public static int largest(int[] data) {
        int best = [[start]];
        for (int i = [[from]]; i < data.length; i++) {
            if ([[test]]) {
                best = data[i];
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(largest(new int[] {3, 8, 2, 8, 5}));
        System.out.println(largest(new int[] {-4, -9, -1}));
    }
}
"""

LESSON = {
    "id": "bigo-write",
    "title": "Writing constant, linear and quadratic code",
    "summary": "Exam questions ask you to write a method with a given big O. Each of the three main growth rates has a recognisable shape you can reach for.",
    "goals": [
        "Write an O(1) method: direct access or a formula, no loop over the data",
        "Write an O(n) method: one pass with a running result",
        "Write an O(n²) method: every pair, with a loop inside a loop",
        "Solve one problem at two different growth rates",
    ],
    "cos225": "The Exam 2 guide: \"write functions of a given big O (constant, linear, quadratic)\". Code questions give you the scaffolding and ask for a few lines.",
    "blocks": [
        {"type": "h", "text": "Three shapes"},
        {"type": "p", "text": "When a question asks for a method of a particular big O, start from its shape:"},
        {"type": "list", "items": [
            "**O(1)**: no loop over the input. Read a value by index, do arithmetic, compare, return.",
            "**O(n)**: one loop over the input, keeping a running result: a total, a count, the best value so far.",
            "**O(n²)**: a loop inside a loop, typically to look at every pair of values.",
        ]},
        {"type": "code", "files": {"ThreeWays.java": THREE}, "run": "ThreeWays",
         "after": "The pairs that add to 10 are 4 + 6 and 9 + 1. The 5 can't pair with itself, because `j` always starts after `i`."},

        {"type": "h", "text": "One problem, two growth rates"},
        {"type": "p", "text": "Big O belongs to an algorithm, not to a problem. The sum 1 + 2 + … + n can be added up in a loop (O(n)), or worked out with Gauss's formula n(n + 1)/2 (O(1)):"},
        {"type": "code", "files": {"SumTo.java": SUMS}, "run": "SumTo",
         "after": "Both give the same answers, but for a million, the loop does a million additions while the formula does one multiplication and one division. The `(long)` cast stops `n * (n + 1)` overflowing an `int`."},
        {"type": "p", "text": "So when you're asked for O(1), look for a way to compute the answer directly instead of visiting the values; when you're asked for O(n), look for a way to finish in one pass instead of comparing pairs."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "bigo-largest", "title": "An O(n) largest value",
         "prompt": "Finish `largest` so it finds the largest value in one pass. It must work for all-negative arrays too.",
         "files": {"Largest.java": MAXB}, "run": "Largest", "output": "8\n-1",
         "blanks": {
             "start": {"accept": ["data[0]"], "hint": "Start with a value that's really in the array.",
                       "wrong": [{"answer": "0", "why": "For `{-4, -9, -1}`, nothing beats 0, so it returns 0, which isn't in the array."}]},
             "from": {"accept": ["1", "0"], "hint": "`data[0]` is already in `best`."},
             "test": {"accept": ["data[i] > best", "best < data[i]"], "hint": "Replace `best` when you find something bigger.",
                      "wrong": [{"answer": "data[i] < best", "why": "That keeps the smallest value instead."}]},
         },
         "explain": "Start with the first value, then one loop compares each value with the best so far. One pass: O(n)."},
        {"type": "quiz", "id": "bigo-write-which",
         "question": "You're asked to write an O(1) method that returns the middle value of an array. Which body fits?",
         "choices": ["`return data[data.length / 2];`", "A loop that counts to `data.length / 2`, then returns that value", "A loop that finds the median by comparing every pair", "Sorting the array first, then returning the middle"],
         "answer": 0,
         "explain": "Arrays allow direct access by index, so one read is enough. Any loop that depends on the length makes it O(n) or worse."},
        {"type": "quiz", "id": "bigo-write-pairs",
         "question": "Which method has to be at least O(n²) the way it's described?",
         "choices": ["Return the first value", "Count how many values are even", "Print every pair of values (all n × n combinations)", "Return the length of the array"],
         "answer": 2,
         "explain": "Printing n × n pairs means doing n² things, so no algorithm can do it in less. Counting evens is one pass; the others are single steps."},
    ],
    "sources": [ALGS4_14, OPENDSA_ANAL],
}
