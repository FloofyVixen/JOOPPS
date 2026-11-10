from sources import ALGS4_13, OPENDSA_QUEUE, NOSUCH_API, LINKEDLIST_API
from ds_code import QUEUE_ADT, LINEAR_NODE, LINKED_QUEUE, LQUEUE_FILES, main_class, lines

HIDE = ["QueueADT.java", "LinearNode.java", "LinkedQueue.java"]

DEMO = main_class("LinkedQueueDemo", lines(
    'LinkedQueue<String> q = new LinkedQueue<>();',
    'q.enqueue("a");',
    'q.enqueue("b");',
    'q.enqueue("c");',
    'System.out.println(q.chainString());',
    'System.out.println(q.dequeue() + " " + q.chainString());',
    'q.enqueue("d");',
    'System.out.println(q.chainString());',
    'System.out.println(q);',
))
EMPTYING = main_class("Emptying", lines(
    'LinkedQueue<Integer> q = new LinkedQueue<>();',
    'q.enqueue(1);',
    'q.dequeue();',
    'q.enqueue(2);',
    'q.enqueue(3);',
    'System.out.println(q.chainString() + " size " + q.size());',
))
T1 = main_class("LQTrace", lines(
    'LinkedQueue<Integer> q = new LinkedQueue<>();',
    'q.enqueue(5);',
    'q.enqueue(6);',
    'q.enqueue(q.dequeue() * 10);',
    'q.enqueue(7);',
    'q.dequeue();',
    'System.out.println(q.chainString());',
))
BL = LINKED_QUEUE.replace("""        if (isEmpty()) {
            front = node;
        } else {
            rear.setNext(node);
        }
        rear = node;""", """        if (isEmpty()) {
            [[first]];
        } else {
            [[attach]];
        }
        [[newrear]];""").replace("""        T result = front.getElement();
        front = front.getNext();
        count--;
        if (isEmpty()) {
            rear = null;
        }""", """        T result = front.getElement();
        [[advance]];
        count--;
        if (isEmpty()) {
            rear = null;
        }""")
BLT = main_class("LQTester", lines(
    'LinkedQueue<String> q = new LinkedQueue<>();',
    'q.enqueue("x");',
    'q.enqueue("y");',
    'q.enqueue("z");',
    'System.out.println(q.dequeue() + " " + q.chainString());',
    'q.dequeue();',
    'q.dequeue();',
    'q.enqueue("w");',
    'System.out.println(q.chainString() + " " + q.getFront());',
))

ITEMS = [
    ("`enqueue` on the shifting `ArrayQueue` (array not full)", "O(1)", "It writes at `rear`, the next free slot."),
    ("`dequeue` on the shifting `ArrayQueue`", "O(n)", "Every remaining value shifts one slot left."),
    ("`enqueue` on `CircularArrayQueue` (array not full)", "O(1)", None),
    ("`dequeue` on `CircularArrayQueue`", "O(1)", "Only `front` moves."),
    ("`enqueue` on `LinkedQueue` (with a rear reference)", "O(1)", "Link after `rear`, then move `rear`."),
    ("`dequeue` on `LinkedQueue`", "O(1)", "`front = front.getNext()`."),
    ("`enqueue` on a linked queue with only a front reference", "O(n)", "It has to walk to the last node first."),
    ("`getFront` on any of these queues", "O(1)", None),
]

LESSON = {
    "id": "lqueue",
    "title": "Linked queues: front and rear",
    "summary": "A linked queue keeps two references: `front` (the head of the chain), where values leave, and `rear` (the last node), where they join. With both, every operation is O(1).",
    "goals": [
        "Implement enqueue and dequeue on linked nodes with `front` and `rear` references",
        "Handle the empty queue: the first enqueue sets both ends, the last dequeue clears both",
        "Explain why the front is the head and the rear is the last node, not the other way round",
        "Compare the big O of the array and linked queues",
    ],
    "cos225": "The Exam 2 guide asks about the challenges of the front and rear being at different points and array versus linked performance. This lesson is the linked half, and the comparison.",
    "blocks": [
        {"type": "h", "text": "Two ends, two references"},
        {"type": "p", "text": "A linked stack only needs its head. A queue works at both ends, so a linked queue keeps a reference to each: `front`, the head of the chain, and `rear`, the last node. Values join after `rear` and leave from `front`."},
        {"type": "note", "label": "Isn't that a tail?", "text": "Yes: `rear` is a reference to the last node. The exam guide says not to assume a tail for plain linked lists. A linked queue is the standard case where one is part of the design, and it's what makes `enqueue` O(1)."},
        {"type": "code", "files": {"QueueADT.java": QUEUE_ADT, "LinearNode.java": LINEAR_NODE, "LinkedQueue.java": LINKED_QUEUE},
         "hide": ["QueueADT.java", "LinearNode.java"], "show": False},
        {"type": "list", "items": [
            "`enqueue` makes a node. If the queue is empty, it's also the front; otherwise the old rear links to it. Either way it becomes the new `rear`.",
            "`dequeue` takes the front element and moves `front` to the next node. If that empties the queue, `rear` is cleared too, so it doesn't keep pointing at the removed node.",
            "`chainString` prints the nodes from the front; `toString` prints the queue in the `front [ ... ] rear` format.",
        ]},
        {"type": "code", "files": {**LQUEUE_FILES, "LinkedQueueDemo.java": DEMO}, "run": "LinkedQueueDemo", "hide": HIDE},
        {"type": "diagram", "kind": "linked", "state": "head -> b -> c -> d -> null",
         "files": {**LQUEUE_FILES, "LinkedQueueDemo.java": DEMO}, "run": "LinkedQueueDemo", "line": 2,
         "caption": "The chain after the demo: `front` refers to the head node (`b`) and `rear` to the last node (`d`)."},

        {"type": "h", "text": "Why the front is the head"},
        {"type": "p", "text": "Could the queue run the other way, with values joining at the head and leaving from the last node? Joining at the head is O(1), but leaving would mean removing the last node, and to do that you need the node **before** it, which only a full walk from the head can find. So that version's `dequeue` would be O(n). Removing is cheap at the head; adding is cheap at either end when you have a reference to it. Hence: remove at the head (front), add at the tail (rear)."},

        {"type": "h", "text": "The empty cases"},
        {"type": "p", "text": "The two ends meet when the queue has one node: `front` and `rear` refer to the same node. Getting the transitions between empty and one value right is where linked queues usually go wrong:"},
        {"type": "code", "files": {**LQUEUE_FILES, "Emptying.java": EMPTYING}, "run": "Emptying", "hide": HIDE,
         "after": "After the dequeue empties the queue, `enqueue(2)` sees `isEmpty()` and sets `front`; without that check it would call `rear.setNext` on `null`."},

        {"type": "h", "text": "Array or linked?"},
        {"type": "match", "id": "lq-match",
         "prompt": "Match each operation with its big O.",
         "options": ["O(1)", "O(n)"],
         "items": [{"text": t, "answer": a, **({"why": w} if w else {})} for t, a, w in ITEMS],
         "explain": "The circular array queue and the linked queue with both references are O(1) for every operation (the array occasionally pays O(n) to grow). The shifting array queue and the front-only linked queue each have one O(n) operation."},
        {"type": "p", "text": "Beyond big O, the trade-offs are the same as for stacks: an array queue may have unused capacity and must sometimes grow; a linked queue uses an extra reference per value but never fills up."},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "lq-trace", "kind": "linked",
         "prompt": "Draw the chain from `front` to `rear`.",
         "files": {**LQUEUE_FILES, "LQTrace.java": T1}, "run": "LQTrace", "hide": HIDE,
         "question": "Which diagram shows the queue's chain at the end?",
         "choices": ["head -> 50 -> 7 -> null", "head -> 6 -> 50 -> 7 -> null", "head -> 7 -> 50 -> null", "head -> 6 -> 7 -> 50 -> null"],
         "answer": 0,
         "explain": "5 and 6 join. `q.dequeue() * 10` removes 5 and enqueues 50: 6, 50. Then 7 joins: 6, 50, 7. The last dequeue removes 6."},
        {"type": "blanks", "id": "lq-blanks", "title": "Enqueue and dequeue",
         "prompt": "Fill in the four blanks in `LinkedQueue`.",
         "files": {"QueueADT.java": QUEUE_ADT, "LinearNode.java": LINEAR_NODE, "LinkedQueue.java": BL, "LQTester.java": BLT},
         "hide": ["QueueADT.java", "LinearNode.java"], "run": "LQTester",
         "output": "x head -> y -> z -> null\nhead -> w -> null w",
         "blanks": {
             "first": {"accept": ["front = node"], "hint": "In an empty queue, the new node is the front too.",
                       "wrong": [{"answer": "rear = node", "why": "`front` stays `null`, so the queue claims to have a value but `getFront` and `dequeue` crash."}]},
             "attach": {"accept": ["rear.setNext(node)"], "hint": "Link the new node after the current last node.",
                        "wrong": [{"answer": "node.setNext(rear)", "why": "That points the new node backwards at the old rear, and the old rear never links to it, so it's unreachable from the front."}]},
             "newrear": {"accept": ["rear = node"], "hint": "The new node is now last."},
             "advance": {"accept": ["front = front.getNext()"], "hint": "The second node becomes the front.",
                         "wrong": [{"answer": "front.setNext(null)", "why": "That cuts the chain after the front node, losing every other value, and the front itself never leaves."}]},
         },
         "explain": "Enqueue: an empty queue sets `front`, otherwise link after `rear`; then move `rear`. Dequeue: move `front` along."},
    ],
    "sources": [ALGS4_13, OPENDSA_QUEUE, NOSUCH_API, LINKEDLIST_API],
}
