from sources import ALGS4_13, ALGS4_14, OPENDSA_STACK, OPENDSA_QUEUE, COLL_IFACES, LIST_API
from tasks_classes import task
from tasks_stacks import given
from ds_code import (STACK_FILES, LSTACK_FILES, CQUEUE_FILES, LQUEUE_FILES, NODE, NODE_FILES, STACK_ADT, LINEAR_NODE,
                     QUEUE_ADT, LINKED_STACK, CIRCULAR_QUEUE, main_class, lines)

SH = ["StackADT.java", "ArrayStack.java"]
LSH = ["StackADT.java", "LinearNode.java", "LinkedStack.java"]
CQH = ["QueueADT.java", "CircularArrayQueue.java"]
LQH = ["QueueADT.java", "LinearNode.java", "LinkedQueue.java"]
NH = ["Node.java", "Show.java"]

A1 = main_class("A1", lines(
    'ArrayStack<Integer> s = new ArrayStack<>();',
    's.push(8);', 's.push(1);', 's.push(6);', 's.pop();', 's.push(3);', 's.push(s.pop() + s.peek());', 's.push(2);',
    'System.out.println(s.arrayString());'))
A2 = main_class("A2", lines(
    'CircularArrayQueue<String> q = new CircularArrayQueue<>();',
    'q.enqueue("A");', 'q.enqueue("B");', 'q.enqueue("C");', 'q.dequeue();', 'q.dequeue();',
    'q.enqueue("D");', 'q.enqueue("E");', 'q.enqueue(q.dequeue());',
    'System.out.println(q.arrayString());'))
A3 = main_class("A3", lines(
    'Node head = new Node(1);', 'head.setNext(new Node(2));', 'head.getNext().setNext(new Node(3));',
    'Node n = new Node(4);', 'n.setNext(head.getNext().getNext());', 'head.getNext().setNext(n);',
    'head = head.getNext();',
    'System.out.println(Show.chain(head));'))
A4 = main_class("A4", lines(
    'LinkedStack<String> s = new LinkedStack<>();',
    's.push("x");', 's.push("y");', 's.push("z");', 's.pop();', 's.push("w");',
    'System.out.println(s);'))
PIC = main_class("Pic", lines(
    'LinkedQueue<Integer> q = new LinkedQueue<>();',
    'for (int i = 5; i <= 25; i += 5) {', '    q.enqueue(i);', '}',
    'System.out.println(q);'))
PICS = main_class("PicStack", lines(
    'ArrayStack<Character> s = new ArrayStack<>();',
    'for (char c : "EXAM".toCharArray()) {', '    s.push(c);', '}',
    'System.out.println(s.arrayString());'))

PRED_LL = main_class("LL", lines(
    'Node head = null;',
    'for (int i = 1; i <= 4; i++) {', '    Node n = new Node(i * 3);', '    n.setNext(head);', '    head = n;', '}',
    'int total = 0;',
    'Node current = head;',
    'while (current.getNext() != null) {', '    total += current.getData();', '    current = current.getNext();', '}',
    'System.out.println(total + " " + current.getData());'))
PRED_LOOP = """public class Count {
    public static void main(String[] args) {
        int n = 6;
        int count = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                count++;
            }
        }
        System.out.println(count);
    }
}
"""

BIGO = [
    {"code": "static int middle(int[] a) {\n    return a[a.length / 2];\n}", "answer": "O(1)"},
    {"code": "static int countZeros(int[] a) {\n    int c = 0;\n    for (int x : a) {\n        if (x == 0) {\n            c++;\n        }\n    }\n    return c;\n}", "answer": "O(n)"},
    {"code": "static boolean anyPairSumsToZero(int[] a) {\n    for (int i = 0; i < a.length; i++) {\n        for (int j = 0; j < a.length; j++) {\n            if (i != j && a[i] + a[j] == 0) {\n                return true;\n            }\n        }\n    }\n    return false;\n}", "answer": "O(n²)"},
    {"code": "static int halvings(int n) {\n    int steps = 0;\n    for (int k = n; k > 1; k = k / 2) {\n        steps++;\n    }\n    return steps;\n}", "answer": "O(log n)"},
    {"code": "static int sumFirstHundred(int[] a) {\n    int s = 0;\n    for (int i = 0; i < 100 && i < a.length; i++) {\n        s += a[i];\n    }\n    return s;\n}", "answer": "O(1)", "why": "At most 100 iterations, whatever the length."},
]
OPS = [
    ("`push` on `ArrayStack` (not full)", "O(1)"),
    ("`dequeue` on a shifting `ArrayQueue`", "O(n)"),
    ("`dequeue` on `CircularArrayQueue`", "O(1)"),
    ("`get(i)` on a linked list", "O(n)"),
    ("`get(i)` on an `ArrayList`", "O(1)"),
    ("Adding at the end of a linked list with only `head`", "O(n)"),
    ("`pop` on `LinkedStack`", "O(1)"),
]

LS_PLACEHOLDER = LINKED_STACK.replace("""        LinearNode<T> node = new LinearNode<>(element);
        node.setNext(top);
        top = node;
        count++;""", """        // write push here""").replace("""        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T result = top.getElement();
        top = top.getNext();
        count--;
        return result;""", """        // write pop here
        return null;""")
LS_TEST = main_class("StackCheck", lines(
    'StackADT<Integer> s = new LinkedStack<>();',
    'for (int i = 1; i <= 3; i++) {', '    s.push(i * 10);', '}',
    'System.out.println(s.pop() + " " + s.pop() + " " + s.size() + " " + s.peek());',
    'try {', '    s.pop();', '    s.pop();', '} catch (java.util.EmptyStackException e) {', '    System.out.println("empty");', '}'))

CQ_PLACEHOLDER = CIRCULAR_QUEUE.replace("""        queue[rear] = element;
        rear = (rear + 1) % queue.length;
        count++;""", """        // store the element and move rear (wrap around!)""")
CQ_TEST = main_class("QueueCheck", lines(
    'CircularArrayQueue<String> q = new CircularArrayQueue<>();',
    'for (String s : new String[] {"a", "b", "c"}) {', '    q.enqueue(s);', '}',
    'q.dequeue();', 'q.dequeue();', 'q.enqueue("d");', 'q.enqueue("e");',
    'System.out.println(q.arrayString() + " " + q);'))

COUNT_PLACEHOLDER = """public class Nodes {
    // Returns how many nodes in the list hold a value greater than limit.
    public static int countGreater(Node head, int limit) {
        return 0;
    }
}
"""
COUNT_SOLUTION = """public class Nodes {
    // Returns how many nodes in the list hold a value greater than limit.
    public static int countGreater(Node head, int limit) {
        int count = 0;
        Node current = head;
        while (current != null) {
            if (current.getData() > limit) {
                count++;
            }
            current = current.getNext();
        }
        return count;
    }
}
"""
COUNT_TEST = main_class("NodesCheck", lines(
    'Node head = new Node(4);', 'head.setNext(new Node(9));', 'head.getNext().setNext(new Node(7));',
    'System.out.println(Nodes.countGreater(head, 5) + " " + Nodes.countGreater(head, 100) + " " + Nodes.countGreater(null, 0));'))

LESSON = {
    "id": "exam-practice-2",
    "title": "Exam practice 2",
    "summary": "A practice set in the Exam 2 format covering units 13 to 21: diagram problems on arrays, linked lists, stacks and queues; short answers and matching on algorithms and collections; and a few lines of code with the scaffolding given.",
    "goals": [
        "Draw and read diagrams of array and linked stacks and queues",
        "Match code and operations with their big O, and collection types with their kind",
        "Write a few lines of code inside given scaffolding",
    ],
    "cos225": "This page follows the Exam 2 guide's three question types: procedural problems (diagram an array or linked list, interpret changes to it as a stack or queue, and answer questions about drawings); short answers (matching, four-choice multiple choice, written math, with linked lists a favourite); and code writing, where imports and scaffolding are given and syntax errors are forgiven, but braces or indentation for control statements are required.",
    "blocks": [
        {"type": "h", "text": "How to use this page"},
        {"type": "list", "items": [
            "The exam is 50 minutes. Try to finish each part on paper before you check anything.",
            "For the diagram problems, draw every step, not just the end. Then pick the matching diagram.",
            "For code writing, write the lines on paper first, then type them in and run them. On the real exam, small syntax slips are ignored, but the structure of your loops and `if`s must be clear: use braces or indentation.",
            "Remember the guide's rules for linked lists: no tail and no doubly linked lists, unless a question gives you one.",
        ]},

        {"type": "h", "text": "Part A: procedural problems"},
        {"type": "trace", "id": "ex2-a-astack", "kind": "array",
         "prompt": "`ArrayStack` (from unit 14) starts with 4 slots. `top` is the next free index.",
         "files": {**STACK_FILES, "A1.java": A1}, "run": "A1", "hide": SH,
         "question": "Draw the array, then choose the matching diagram.",
         "choices": ["[8, 1, 4, 2] top=4", "[8, 1, 3, 4, 2, _, _, _] top=5", "[8, 1, 7, 2] top=4", "[8, 1, 3, 2] top=4"],
         "answer": 0,
         "explain": "8, 1, 6; pop removes 6; push 3 gives 8, 1, 3. `s.pop() + s.peek()` pops 3 and peeks 1 (the new top), pushing 4: 8, 1, 4. Push 2 fills the last slot, so no growth is needed."},
        {"type": "trace", "id": "ex2-a-cqueue", "kind": "array",
         "prompt": "`CircularArrayQueue` (from unit 19) starts with 4 slots. `rear` is the next free index; both indexes wrap.",
         "files": {**CQUEUE_FILES, "A2.java": A2}, "run": "A2", "hide": CQH,
         "question": "Draw the array, then choose the matching diagram.",
         "choices": ["[E, _, C, D] front=2 rear=1", "[E, C, _, D] front=3 rear=2", "[D, E, C, _] front=0 rear=3", "[C, D, E, _] front=0 rear=3"],
         "answer": 1,
         "explain": "A, B, C fill slots 0 to 2, and two dequeues clear slots 0 and 1 (front 2). D goes in slot 3 and E wraps into slot 0 (rear 1). Then `q.enqueue(q.dequeue())` takes C from slot 2 (clearing it, front 3) and stores it at the rear, slot 1 (rear 2). The queue is D, E, C. Nothing is unrolled: that only happens when the array grows."},
        {"type": "trace", "id": "ex2-a-linked", "kind": "linked",
         "prompt": "Nodes from unit 16. Trace the references carefully.",
         "files": {**NODE_FILES, "A3.java": A3}, "run": "A3", "hide": NH,
         "question": "Which diagram shows the list starting at `head` at the end?",
         "choices": ["head -> 2 -> 4 -> 3 -> null", "head -> 1 -> 2 -> 4 -> 3 -> null", "head -> 2 -> 3 -> 4 -> null", "head -> 4 -> 3 -> null"],
         "answer": 0,
         "explain": "The list is 1, 2, 3. The new node 4 points at the 3, and the 2 is redirected to 4: 1, 2, 4, 3. Then `head` moves to the second node, so the list seen from `head` is 2, 4, 3."},
        {"type": "trace", "id": "ex2-a-lstack", "kind": "linked",
         "prompt": "`LinkedStack` (from unit 17) keeps its top at the head of its chain.",
         "files": {**LSTACK_FILES, "A4.java": A4}, "run": "A4", "hide": LSH,
         "question": "Which diagram shows the stack's chain of nodes?",
         "choices": ["head -> x -> y -> w -> null", "head -> w -> y -> x -> null", "head -> w -> z -> y -> x -> null", "head -> z -> y -> w -> null"],
         "answer": 1,
         "explain": "Pushes put z on top of y on top of x; the pop removes z, and w becomes the new head."},
        {"type": "p", "text": "Questions about drawings. This queue was built by enqueueing 5, 10, 15, 20 and 25:"},
        {"type": "diagram", "kind": "queue", "state": "front [5, 10, 15, 20, 25] rear",
         "files": {**LQUEUE_FILES, "Pic.java": PIC}, "run": "Pic"},
        {"type": "quiz", "id": "ex2-a-pic1",
         "question": "If you call `dequeue()` twice and then `enqueue(30)`, what does `getFront()` return?",
         "choices": ["5", "15", "25", "30"],
         "answer": 1,
         "explain": "Two dequeues remove 5 and 10. Enqueueing adds at the rear, so the front is 15."},
        {"type": "p", "text": "And this is the array of an `ArrayStack` after pushing the letters of `EXAM`:"},
        {"type": "diagram", "kind": "array", "state": "[E, X, A, M] top=4",
         "files": {**STACK_FILES, "PicStack.java": PICS}, "run": "PicStack"},
        {"type": "quiz", "id": "ex2-a-pic2",
         "question": "Which statement about this stack is true?",
         "choices": ["`peek()` returns `E`, at index 0", "The next `push` must first expand the array", "`pop()` returns `A`", "`top` points at the top value"],
         "answer": 1,
         "explain": "`top` is 4, equal to the array's length: the array is full, so the next push expands it. The top value, `M`, is at index `top - 1`; `top` itself is the next free slot."},

        {"type": "h", "text": "Part B: short answers"},
        {"type": "match", "id": "ex2-b-bigo",
         "prompt": "Match each method with its big O (n is the array length, or `n` itself).",
         "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
         "items": BIGO},
        {"type": "match", "id": "ex2-b-ops",
         "prompt": "Match each operation with its big O.",
         "options": ["O(1)", "O(n)"],
         "items": [{"text": t, "answer": a} for t, a in OPS]},
        {"type": "match", "id": "ex2-b-order",
         "prompt": "Rank the big six from best (1) to worst (6).",
         "options": ["1", "2", "3", "4", "5", "6"],
         "items": [{"text": "O(n log n)", "answer": "4"}, {"text": "O(1)", "answer": "1"}, {"text": "O(2ⁿ)", "answer": "6"},
                   {"text": "O(n)", "answer": "3"}, {"text": "O(n²)", "answer": "5"}, {"text": "O(log n)", "answer": "2"}]},
        {"type": "match", "id": "ex2-b-kinds",
         "prompt": "Is each type an interface, an abstract class or a concrete class?",
         "options": ["Interface", "Abstract class", "Concrete class"],
         "items": [{"text": "`List`", "answer": "Interface"}, {"text": "`ArrayList`", "answer": "Concrete class"},
                   {"text": "`Collection`", "answer": "Interface"}, {"text": "`AbstractList`", "answer": "Abstract class"},
                   {"text": "`LinkedList`", "answer": "Concrete class"}]},
        {"type": "quiz", "id": "ex2-b-math",
         "question": "An O(n²) method takes 3 seconds for n = 1,000. About how long should it take for n = 3,000?",
         "choices": ["9 seconds", "27 seconds", "6 seconds", "3 seconds"],
         "answer": 1,
         "explain": "Tripling n multiplies n² by 3² = 9, so about 3 × 9 = 27 seconds."},
        {"type": "predict", "id": "ex2-b-count",
         "prompt": "How many times does `count++` run? (Written math: 0 + 1 + 2 + … + (n − 1).)",
         "files": {"Count.java": PRED_LOOP}, "run": "Count",
         "choices": ["15", "36", "21", "30"],
         "answer": 0,
         "explain": "The inner loop runs `i` times for each `i` from 0 to 5: 0 + 1 + 2 + 3 + 4 + 5 = 15, which is n(n − 1)/2 for n = 6. That's still O(n²)."},
        {"type": "predict", "id": "ex2-b-linked",
         "prompt": "A linked-list favourite. What does this print?",
         "files": {**NODE_FILES, "LL.java": PRED_LL}, "run": "LL", "hide": NH,
         "choices": ["27 3", "30 12", "18 12", "27 12"],
         "answer": 0,
         "explain": "Adding at the front builds 12, 9, 6, 3. The loop stops **on** the last node, so it adds 12 + 9 + 6 = 27 and `current` ends on the node holding 3."},
        {"type": "quiz", "id": "ex2-b-top",
         "question": "Where is the top of a stack in an array implementation and in a linked implementation, so that push and pop are O(1)?",
         "choices": ["Array: index 0. Linked: the last node", "Array: the end of the used part. Linked: the head", "Array: the end of the used part. Linked: the last node", "All of the above work equally well"],
         "answer": 1,
         "explain": "At the end of an array nothing has to shift; at the head of a chain nothing has to be searched for."},
        {"type": "quiz", "id": "ex2-b-pillars",
         "question": "Which of these are among the four pillars of OOP?",
         "choices": ["Encapsulation and inheritance only", "Abstraction and polymorphism only", "Encapsulation, abstraction, inheritance and polymorphism", "None of the above"],
         "answer": 2,
         "explain": "All four: encapsulation (hide the data), abstraction (show only what matters, like an ADT), inheritance (`extends`) and polymorphism (one interface, many forms, like `StackADT` with two classes)."},
        {"type": "quiz", "id": "ex2-b-node",
         "question": "Which statement about a linked node is **not** true?",
         "choices": ["It holds a data payload and a reference to the next node", "It is created with `new`", "On its own, it is a linked list of one element", "It must always have a non-null `next`"],
         "answer": 3,
         "explain": "The last node's `next` is `null`; a single node with `next` `null` is a whole list."},

        {"type": "h", "text": "Part C: code writing"},
        {"type": "p", "text": "Each task starts with the scaffolding already in the editor, as on the exam. Write only the missing lines, then run."},
        given(task("ex2-c-lstack", "LinkedStack push and pop",
             "`LinkedStack<T>` is in the editor with `push` and `pop` left empty. Write them: `push` adds at the head; `pop` throws `EmptyStackException` when empty, otherwise removes and returns the top element. Keep `count` up to date.",
             {"LinkedStack.java": LINKED_STACK, "StackCheck.java": LS_TEST}, "StackCheck", "30 20 1 10\nempty",
             hints=["push: new node, point it at `top`, move `top` to it. pop: save `top.getElement()`, move `top` to `top.getNext()`."]),
              {**{k: v for k, v in LSTACK_FILES.items() if k != "LinkedStack.java"}, "LinkedStack.java": LS_PLACEHOLDER, "StackCheck.java": LS_TEST}),
        given(task("ex2-c-count", "Traverse a linked list",
             "`Node` and the scaffolding of `Nodes.countGreater` are in the editor. Write the body: count the nodes whose data is greater than `limit`. An empty list (`null`) has none.",
             {"Nodes.java": COUNT_SOLUTION, "NodesCheck.java": COUNT_TEST}, "NodesCheck", "2 0 0",
             checks=[{"pattern": r"getNext\(\)", "message": "Move along the list with `getNext()`."}]),
              {"Node.java": NODE, "Nodes.java": COUNT_PLACEHOLDER, "NodesCheck.java": COUNT_TEST}),
        given(task("ex2-c-enqueue", "Circular enqueue",
             "`CircularArrayQueue` is in the editor with the end of `enqueue` missing (the capacity check is there). Store the element at `rear`, move `rear` forward with wrap-around, and update `count`.",
             {"CircularArrayQueue.java": CIRCULAR_QUEUE, "QueueCheck.java": CQ_TEST}, "QueueCheck",
             "[e, _, c, d] front=2 rear=1 front [c, d, e] rear",
             checks=[{"pattern": r"%\s*queue\.length", "message": "Wrap `rear` with `% queue.length`."}]),
              {"QueueADT.java": QUEUE_ADT, "CircularArrayQueue.java": CQ_PLACEHOLDER, "QueueCheck.java": CQ_TEST}),
        task("ex2-c-bigo", "Write it at a given big O",
             "Write `Given` with two methods: `public static boolean containsNegative(int[] data)`, which must be O(n), and `public static int countEqualPairs(int[] data)`, the number of pairs `i < j` with `data[i] == data[j]`, written as O(n²) with nested loops. `GivenTester` prints both for `{3, -1, 3, 3}`.",
             {"Given.java": """public class Given {
    public static boolean containsNegative(int[] data) {
        for (int value : data) {
            if (value < 0) {
                return true;
            }
        }
        return false;
    }

    public static int countEqualPairs(int[] data) {
        int count = 0;
        for (int i = 0; i < data.length; i++) {
            for (int j = i + 1; j < data.length; j++) {
                if (data[i] == data[j]) {
                    count++;
                }
            }
        }
        return count;
    }
}
""", "GivenTester.java": """public class GivenTester {
    public static void main(String[] args) {
        int[] data = {3, -1, 3, 3};
        System.out.println(Given.containsNegative(data) + " " + Given.countEqualPairs(data));
    }
}
"""}, "GivenTester", "true 3",
             tests={"CheckGiven.java": """public class CheckGiven {
    public static void main(String[] args) {
        System.out.println(Given.containsNegative(new int[] {}) + " " + Given.countEqualPairs(new int[] {1, 2}));
    }
}
"""}, tests_run="CheckGiven", tests_output="false 0"),
        task("ex2-c-list", "A method on any List",
             "Write `Lists` with `public static int sumEvens(List<Integer> values)`, the sum of the even values, using a for-each loop so it's O(n) for both `ArrayList` and `LinkedList`. `ListsTester` creates a `List<Integer>` as a `LinkedList`, adds 1 to 6 and prints `sumEvens`.",
             {"Lists.java": """import java.util.List;

public class Lists {
    public static int sumEvens(List<Integer> values) {
        int sum = 0;
        for (int v : values) {
            if (v % 2 == 0) {
                sum += v;
            }
        }
        return sum;
    }
}
""", "ListsTester.java": """import java.util.LinkedList;
import java.util.List;

public class ListsTester {
    public static void main(String[] args) {
        List<Integer> values = new LinkedList<>();
        for (int i = 1; i <= 6; i++) {
            values.add(i);
        }
        System.out.println(Lists.sumEvens(values));
    }
}
"""}, "ListsTester", "12",
             tests={"CheckLists.java": """import java.util.ArrayList;
import java.util.List;

public class CheckLists {
    public static void main(String[] args) {
        List<Integer> v = new ArrayList<>();
        v.add(-4);
        v.add(7);
        System.out.println(Lists.sumEvens(v) + " " + Lists.sumEvens(new ArrayList<>()));
    }
}
"""}, tests_run="CheckLists", tests_output="-4 0"),
    ],
    "sources": [ALGS4_13, ALGS4_14, OPENDSA_STACK, OPENDSA_QUEUE, COLL_IFACES, LIST_API],
}
