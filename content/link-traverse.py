from sources import ALGS4_13, NPE, WHILE_TUT, FOR_TUT
from ds_code import NODE, NODE_FILES, main_class

HIDE = ["Node.java", "Show.java"]

BUILD = """    // Builds head -> values[0] -> values[1] -> ... by adding at the front, last value first.
    public static Node build(int... values) {
        Node head = null;
        for (int i = values.length - 1; i >= 0; i--) {
            Node node = new Node(values[i]);
            node.setNext(head);
            head = node;
        }
        return head;
    }
"""


def cls(name, methods, body):
    return f"public class {name} {{\n{BUILD}\n{methods}    public static void main(String[] args) {{\n{body}    }}\n}}\n"


WALK = cls("Walk", """    public static void printAll(Node head) {
        Node current = head;
        while (current != null) {
            System.out.println(current.getData());
            current = current.getNext();
        }
    }

""", """        Node head = build(4, 8, 15);
        printAll(head);
""")
SIZE_SUM = cls("Measure", """    public static int size(Node head) {
        int count = 0;
        for (Node current = head; current != null; current = current.getNext()) {
            count++;
        }
        return count;
    }

    public static int sum(Node head) {
        int total = 0;
        for (Node current = head; current != null; current = current.getNext()) {
            total += current.getData();
        }
        return total;
    }

    public static boolean contains(Node head, int target) {
        Node current = head;
        while (current != null) {
            if (current.getData() == target) {
                return true;
            }
            current = current.getNext();
        }
        return false;
    }

""", """        Node head = build(4, 8, 15, 16);
        System.out.println(size(head) + " " + sum(head));
        System.out.println(contains(head, 15) + " " + contains(head, 5));
        System.out.println(size(null) + " " + sum(null));
""")
LAST = cls("LastNode", """    public static int lastValue(Node head) {
        Node current = head;
        while (current.getNext() != null) {
            current = current.getNext();
        }
        return current.getData();
    }

""", """        System.out.println(lastValue(build(4, 8, 15)));
        System.out.println(lastValue(build(23)));
        System.out.println(lastValue(null));
""")
GET = cls("GetAt", """    public static int get(Node head, int index) {
        Node current = head;
        for (int i = 0; i < index; i++) {
            current = current.getNext();
        }
        return current.getData();
    }

""", """        Node head = build(4, 8, 15, 16, 23);
        System.out.println(get(head, 0) + " " + get(head, 3));
""")
BLANK = cls("CountAbove", """    public static int countAbove(Node head, int limit) {
        int count = 0;
        Node current = [[start]];
        while ([[cond]]) {
            if (current.getData() > limit) {
                count++;
            }
            [[step]];
        }
        return count;
    }

""", """        Node head = build(3, 12, 7, 20, 9);
        System.out.println(countAbove(head, 8));
        System.out.println(countAbove(null, 8));
""")
PRED = cls("Skip", """    public static void everyOther(Node head) {
        Node current = head;
        while (current != null) {
            System.out.print(current.getData() + " ");
            if (current.getNext() == null) {
                current = null;
            } else {
                current = current.getNext().getNext();
            }
        }
        System.out.println();
    }

""", """        everyOther(build(1, 2, 3, 4, 5));
        everyOther(build(1, 2, 3, 4));
""")
SHOWCODE = """public class Show {
    // Prints a chain of nodes in the form head -> 7 -> 3 -> null.
    public static String chain(Node head) {
        String result = "head";
        Node current = head;
        while (current != null) {
            result += " -> " + current.getData();
            current = current.getNext();
        }
        return result + " -> null";
    }
}
"""

LESSON = {
    "id": "link-traverse",
    "title": "Traversing with getNext()",
    "summary": "To visit every node, start a reference at the head and keep moving it to `getNext()` until it becomes `null`. That one loop is the base of almost every linked-list method.",
    "goals": [
        "Traverse a linked list with a `while` loop and with a `for` loop",
        "Write size, sum, contains and get by traversal",
        "Choose between `current != null` and `current.getNext() != null`",
        "Avoid `NullPointerException` at the end of the list and on an empty list",
    ],
    "cos225": "The Exam 2 guide lists traversal with `.getNext()`, a for loop and a while loop. Expect to write a few lines like these, with the node class given.",
    "blocks": [
        {"type": "h", "text": "The traversal loop"},
        {"type": "p", "text": "You can't jump to the third node of a linked list the way you jump to `array[2]`: the only way there is to follow `next` from the head, one node at a time. Use a second reference, usually called `current`, so the `head` variable stays pointing at the start:"},
        {"type": "code", "files": {"Node.java": NODE, "Walk.java": WALK}, "run": "Walk", "hide": ["Node.java"]},
        {"type": "list", "items": [
            "`current` starts at the head.",
            "`current != null` means there's still a node to visit. When `current` moves past the last node, it becomes `null` and the loop ends.",
            "`current = current.getNext();` is the step that moves along the chain. Forget it and the loop never ends.",
            "`build` makes a list from the values you pass it, using add-at-front from the last value back. The `int...` parameter lets you pass any number of values.",
        ]},
        {"type": "p", "text": "The `Show.chain` helper from the last lesson is exactly this loop, building a string instead of printing:"},
        {"type": "code", "files": {"Node.java": NODE, "Show.java": SHOWCODE}, "hide": ["Node.java"], "show": False},

        {"type": "h", "text": "The for-loop version"},
        {"type": "p", "text": "The same three parts (start, condition, step) fit in a `for` loop header. Use whichever you find clearer; both are common on exams. Here the traversal counts, adds and searches:"},
        {"type": "code", "files": {"Node.java": NODE, "Measure.java": SIZE_SUM}, "run": "Measure", "hide": ["Node.java"],
         "after": "An empty list is `null`, so the loop body never runs: size 0, sum 0. No special case needed. `contains` can stop as soon as it finds the value."},
        {"type": "p", "text": "Each of these visits every node once, so they're O(n). Even `size` is O(n) here, because nothing stores the count: you have to walk the list to find out."},

        {"type": "h", "text": "Stopping at the last node"},
        {"type": "p", "text": "Sometimes you need the last node itself, to read it or to attach something after it. Then the condition is `current.getNext() != null`: stop **on** the last node instead of after it. But that condition calls a method on `current`, so `current` must not be `null`:"},
        {"type": "code", "files": {"Node.java": NODE, "LastNode.java": LAST}, "run": "LastNode", "hide": ["Node.java"], "expect": "runtime",
         "after": "For the empty list, `current` is `null`, and calling `getNext()` on `null` throws a `NullPointerException`. (`<local1>` stands for the local variable `current`: as in the lesson on arrays of objects, javac leaves out local variable names unless you compile with `-g`.) Check for an empty list first whenever your loop condition uses `current.getNext()`."},

        {"type": "h", "text": "Getting the value at an index"},
        {"type": "p", "text": "To reach index `i`, step `i` times from the head. That's O(n), where an array is O(1): the price of a linked structure."},
        {"type": "code", "files": {"Node.java": NODE, "GetAt.java": GET}, "run": "GetAt", "hide": ["Node.java"]},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "trav-count", "title": "Count values above a limit",
         "prompt": "Fill in the traversal so `countAbove` visits every node, including for an empty list.",
         "files": {"Node.java": NODE, "CountAbove.java": BLANK}, "run": "CountAbove", "hide": ["Node.java"],
         "output": "3\n0",
         "blanks": {
             "start": {"accept": ["head"], "hint": "Start at the first node.",
                       "wrong": [{"answer": "head.getNext()", "why": "That skips the first node, and for an empty list it calls `getNext()` on `null` and crashes."}]},
             "cond": {"accept": ["current != null", "null != current"], "hint": "Keep going while there's a node to look at.",
                      "wrong": [{"answer": "current.getNext() != null", "why": "That stops on the last node without counting it (20 is missed), and crashes on an empty list."}]},
             "step": {"accept": ["current = current.getNext()"], "hint": "Move `current` to the next node. Just calling `current.getNext()` reads the next node without moving, and the loop never ends."},
         },
         "explain": "Start at the head, loop while `current != null`, and move with `current = current.getNext()`."},
        {"type": "predict", "id": "trav-skip",
         "prompt": "This loop jumps two nodes at a time. What does it print?",
         "files": {"Node.java": NODE, "Skip.java": PRED}, "run": "Skip", "hide": ["Node.java"],
         "choices": ["1 3 5 \n1 3 ", "1 3 5 \n1 3 4 ", "2 4 \n2 4 ", "1 2 3 4 5 \n1 2 3 4 "],
         "answer": 0,
         "explain": "It prints the node it's on, then jumps to the node after next: 1, 3, 5, then 5 has no next and the loop ends. For four values, it prints 1 and 3, then jumps from 3 past 4 to `null`."},
        {"type": "quiz", "id": "trav-cond",
         "question": "Your loop is `while (current.getNext() != null) { current = current.getNext(); }`. After it ends (on a non-empty list), what does `current` refer to?",
         "choices": ["`null`", "The head", "The last node", "The second-to-last node"],
         "answer": 2,
         "explain": "The loop stops when `current`'s next is `null`, which is only true of the last node."},
    ],
    "sources": [ALGS4_13, NPE, WHILE_TUT, FOR_TUT],
}
