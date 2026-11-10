from sources import ALGS4_13, OPENDSA_QUEUE, NOSUCH_API, IFACE_TUT
from ds_code import QUEUE_ADT, LQUEUE_FILES, STACK_FILES, main_class, lines

HIDE = ["QueueADT.java", "LinearNode.java", "LinkedQueue.java"]

DEMO = main_class("QueueDemo", lines(
    'QueueADT<String> line = new LinkedQueue<>();',
    'line.enqueue("Ana");',
    'line.enqueue("Ben");',
    'line.enqueue("Cy");',
    'System.out.println(line);',
    'System.out.println("front: " + line.getFront());',
    'System.out.println("served: " + line.dequeue());',
    'System.out.println(line + " size " + line.size());',
))
AFTER = main_class("AfterOps", lines(
    'QueueADT<String> line = new LinkedQueue<>();',
    'line.enqueue("Ana");',
    'line.enqueue("Ben");',
    'line.enqueue("Cy");',
    'System.out.println(line);',
    'line.dequeue();',
    'line.enqueue("Dee");',
    'System.out.println(line);',
))
VERSUS = main_class("Versus", lines(
    'StackADT<Integer> stack = new ArrayStack<>();',
    'QueueADT<Integer> queue = new LinkedQueue<>();',
    'for (int i = 1; i <= 4; i++) {',
    '    stack.push(i);',
    '    queue.enqueue(i);',
    '}',
    'String fromStack = "";',
    'String fromQueue = "";',
    'while (!stack.isEmpty()) {',
    '    fromStack += stack.pop() + " ";',
    '    fromQueue += queue.dequeue() + " ";',
    '}',
    'System.out.println("stack: " + fromStack);',
    'System.out.println("queue: " + fromQueue);',
))
EMPTY = main_class("EmptyQueue", lines(
    'QueueADT<Integer> q = new LinkedQueue<>();',
    'q.enqueue(1);',
    'q.dequeue();',
    'q.dequeue();',
))
T1 = main_class("QTrace", lines(
    'QueueADT<Integer> q = new LinkedQueue<>();',
    'q.enqueue(4);',
    'q.enqueue(9);',
    'q.dequeue();',
    'q.enqueue(2);',
    'q.enqueue(7);',
    'System.out.println(q);',
))

LESSON = {
    "id": "queue-fifo",
    "title": "The queue: first in, first out",
    "summary": "A queue adds at one end, the rear, and removes from the other, the front. The first value in is the first one out, like a line at a shop.",
    "goals": [
        "Describe a queue as FIFO: first in, first out",
        "Use the queue operations `enqueue`, `dequeue`, `getFront`, `isEmpty` and `size`",
        "Draw a queue after a sequence of operations",
        "Contrast a queue with a stack",
    ],
    "cos225": "The Exam 2 guide lists the queue as FIFO with enqueue, dequeue and getFront. This unit covers using a queue; the next builds one with an array and with linked nodes.",
    "blocks": [
        {"type": "h", "text": "Two ends"},
        {"type": "p", "text": "A **queue** is a line. New values join at the back, called the **rear**, and values leave from the **front**. Whoever has waited longest is served first. This rule is **FIFO**: first in, first out."},
        {"type": "list", "items": [
            "`enqueue(x)` adds `x` at the rear.",
            "`dequeue()` removes the front value and returns it.",
            "`getFront()` returns the front value without removing it.",
            "`isEmpty()` and `size()` work as they do for stacks.",
        ]},
        {"type": "p", "text": "As with stacks, the operations form an ADT, written as an interface:"},
        {"type": "code", "files": {"QueueADT.java": QUEUE_ADT}, "show": False},
        {"type": "p", "text": "`LinkedQueue` implements it (you'll build it in the next unit). Its `toString` lists the values from front to rear."},
        {"type": "code", "files": {**LQUEUE_FILES, "QueueDemo.java": DEMO}, "run": "QueueDemo", "hide": HIDE},

        {"type": "h", "text": "Drawing a queue"},
        {"type": "p", "text": "Draw a queue as a row, with the front on the left and the rear on the right. After the three enqueues:"},
        {"type": "diagram", "kind": "queue", "state": "front [Ana, Ben, Cy] rear",
         "files": {**LQUEUE_FILES, "AfterOps.java": AFTER}, "run": "AfterOps", "line": 0},
        {"type": "p", "text": "`dequeue` takes `Ana` from the front, and `enqueue(\"Dee\")` joins at the rear. The queue's contents slide along: both ends move."},
        {"type": "diagram", "kind": "queue", "state": "front [Ben, Cy, Dee] rear",
         "files": {**LQUEUE_FILES, "AfterOps.java": AFTER}, "run": "AfterOps", "line": 1},

        {"type": "h", "text": "Stack or queue?"},
        {"type": "p", "text": "Put the same values into a stack and a queue and take them all out. The stack reverses them; the queue keeps their order:"},
        {"type": "code", "files": {**STACK_FILES, **LQUEUE_FILES, "Versus.java": VERSUS}, "run": "Versus",
         "hide": ["StackADT.java", "ArrayStack.java"] + HIDE},
        {"type": "list", "items": [
            "**Stack**: one end does everything. LIFO. Good for undo, matching brackets, reversing, backtracking.",
            "**Queue**: in at one end, out at the other. FIFO. Good for anything that must be handled in arrival order: print jobs, customers, messages, tasks waiting for a turn.",
        ]},

        {"type": "h", "text": "An empty queue"},
        {"type": "p", "text": "`dequeue` and `getFront` have nothing to return on an empty queue. Here they throw Java's `NoSuchElementException`:"},
        {"type": "code", "files": {**LQUEUE_FILES, "EmptyQueue.java": EMPTY}, "run": "EmptyQueue", "hide": HIDE, "expect": "runtime"},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "fifo-trace", "kind": "queue",
         "prompt": "Follow the operations one at a time. Values join at the rear and leave from the front.",
         "files": {**LQUEUE_FILES, "QTrace.java": T1}, "run": "QTrace", "hide": HIDE,
         "question": "Which diagram shows the queue at the end?",
         "choices": ["front [9, 2, 7] rear", "front [4, 2, 7] rear", "front [7, 2, 9] rear", "front [4, 9, 2, 7] rear"],
         "answer": 0,
         "explain": "Enqueue 4 and 9. `dequeue` removes 4, the front. Then 2 and 7 join at the rear behind 9."},
        {"type": "quiz", "id": "fifo-order",
         "question": "You enqueue 1, 2 and 3 into an empty queue, then dequeue three times. In what order do the values come out?",
         "choices": ["1, 2, 3", "3, 2, 1", "2, 3, 1", "1, 3, 2"],
         "answer": 0,
         "explain": "First in, first out: the order they went in."},
        {"type": "quiz", "id": "fifo-which",
         "question": "A printer handles documents in the order they were sent. Which structure fits?",
         "choices": ["A stack", "A queue", "An array sorted by size", "Either; they behave the same"],
         "answer": 1,
         "explain": "Arrival order means FIFO: a queue. A stack would print the most recently sent document first."},
    ],
    "sources": [ALGS4_13, OPENDSA_QUEUE, NOSUCH_API, IFACE_TUT],
}
