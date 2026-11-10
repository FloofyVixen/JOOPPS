from sources import ALGS4_13, OPENDSA_STACK, OBJECTS_TUT, NPE
from ds_code import NODE, NODE_FILES, main_class, lines

HIDE = ["Node.java", "Show.java"]

THREE = main_class("ThreeNodes", lines(
    'Node first = new Node(7);',
    'Node second = new Node(3);',
    'Node third = new Node(9);',
    'first.setNext(second);',
    'second.setNext(third);',
    'Node head = first;',
    'System.out.println(head.getData());',
    'System.out.println(head.getNext().getData());',
    'System.out.println(head.getNext().getNext().getData());',
    'System.out.println(Show.chain(head));',
))
ONE = main_class("OneNode", lines(
    'Node head = new Node(42);',
    'System.out.println(Show.chain(head));',
    'Node empty = null;',
    'System.out.println(Show.chain(empty));',
))
FRONT = main_class("AddFront", lines(
    'Node head = null;',
    'for (int value = 1; value <= 3; value++) {',
    '    Node node = new Node(value);',
    '    node.setNext(head);',
    '    head = node;',
    '    System.out.println(Show.chain(head));',
    '}',
))
LOST = main_class("Lost", lines(
    'Node head = new Node(1);',
    'head.setNext(new Node(2));',
    'head.getNext().setNext(new Node(3));',
    'Node saved = head.getNext();',
    'head = null;',
    'System.out.println(Show.chain(head));',
    'System.out.println(Show.chain(saved));',
))
T1 = main_class("NodeTrace", lines(
    'Node a = new Node(4);',
    'Node b = new Node(8);',
    'Node c = new Node(6);',
    'b.setNext(a);',
    'a.setNext(c);',
    'Node head = b;',
    'System.out.println(Show.chain(head));',
))
T2 = main_class("FrontTrace", lines(
    'Node head = new Node(5);',
    'Node n = new Node(2);',
    'n.setNext(head);',
    'head = n;',
    'n = new Node(7);',
    'n.setNext(head.getNext());',
    'head.setNext(n);',
    'System.out.println(Show.chain(head));',
))
P1 = main_class("Follow", lines(
    'Node head = new Node(10);',
    'head.setNext(new Node(20));',
    'head.getNext().setNext(new Node(30));',
    'Node second = head.getNext();',
    'System.out.println(second.getData() + " " + second.getNext().getData());',
    'System.out.println(second.getNext().getNext());',
))

LESSON = {
    "id": "link-nodes",
    "title": "Nodes and the head",
    "summary": "A linked structure keeps each value in its own small object, a node, which holds a reference to the next node. You reach the whole chain from its first node, the head.",
    "goals": [
        "Describe a node: a data payload and a reference to the next node",
        "Create nodes with `new` and link them with `setNext`",
        "Explain the role of `head`, and why a single node is already a linked list",
        "Draw a chain of nodes from code",
    ],
    "cos225": "Straight from the Exam 2 guide: a node is typically called head, made with `new`, has a reference to `next` and a data payload, and every node on its own is a linked list. Linked-list problems are an exam favourite.",
    "blocks": [
        {"type": "h", "text": "Why not an array?"},
        {"type": "p", "text": "An array is one block of memory with a fixed size. Growing it means copying everything, and adding at the front means shifting everything. A **linked** structure avoids both: each value lives in its own object, and the objects are connected by references, like a chain."},

        {"type": "h", "text": "The node"},
        {"type": "p", "text": "Each link of the chain is a **node**. A node holds two things: its **data** (the payload, here an `int`) and **next**, a reference to the next node. The last node's `next` is `null`, meaning nothing comes after it."},
        {"type": "code", "files": {"Node.java": NODE}, "show": False},
        {"type": "p", "text": "Notice that `Node` has a field of type `Node`. That's allowed: the field doesn't hold a whole node inside it, only a reference to another node object."},

        {"type": "h", "text": "Linking nodes together"},
        {"type": "p", "text": "Create nodes with `new`, then link each one to the next with `setNext`. A variable that refers to the first node is traditionally called **head**: from it, `getNext()` reaches every other node."},
        {"type": "code", "files": {**NODE_FILES, "ThreeNodes.java": THREE}, "run": "ThreeNodes", "hide": HIDE,
         "after": "`Show.chain` (a helper you'll write yourself in the next lesson) prints the chain by following `getNext()` from the head until it reaches `null`."},
        {"type": "diagram", "kind": "linked", "state": "head -> 7 -> 3 -> 9 -> null",
         "files": {**NODE_FILES, "ThreeNodes.java": THREE}, "run": "ThreeNodes",
         "caption": "Each box is a node: its data, and its `next` reference pointing to the following node. The last `next` is `null`."},
        {"type": "p", "text": "`head.getNext().getData()` reads left to right: start at the head, follow its `next` to the second node, and read that node's data."},

        {"type": "h", "text": "Every node is a linked list"},
        {"type": "p", "text": "A single node whose `next` is `null` is a complete linked list of one value. And `head = null` is the **empty** list: there's no first node at all."},
        {"type": "code", "files": {**NODE_FILES, "OneNode.java": ONE}, "run": "OneNode", "hide": HIDE},
        {"type": "p", "text": "Look at it the other way, too: from any node, the nodes you can reach by following `next` form a linked list of their own. In `7 -> 3 -> 9`, the node holding 3 is the head of the list `3 -> 9`. Many linked-list methods use this idea."},

        {"type": "h", "text": "Adding at the front"},
        {"type": "p", "text": "The cheapest place to add is the front: make a new node, point its `next` at the current head, then make it the new head. Nothing else moves, so it's O(1) however long the list is."},
        {"type": "code", "files": {**NODE_FILES, "AddFront.java": FRONT}, "run": "AddFront", "hide": HIDE,
         "after": "Each new value goes in front, so the list ends up in the reverse of the order the values were added, just like a stack."},
        {"type": "p", "text": "The order of the two steps matters. If you wrote `head = node;` first, then `node.setNext(head)` would point the node at itself, and the rest of the list would be lost."},

        {"type": "h", "text": "Don't lose the head"},
        {"type": "p", "text": "The only way into the chain is through a reference to one of its nodes. If no variable refers to a node any more, you can't reach it, and Java eventually reclaims its memory:"},
        {"type": "code", "files": {**NODE_FILES, "Lost.java": LOST}, "run": "Lost", "hide": HIDE,
         "after": "After `head = null`, the node holding 1 is gone for good. The nodes holding 2 and 3 are still reachable, because `saved` refers to the second node."},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "node-trace1", "kind": "linked",
         "prompt": "The nodes are created in one order but linked in another. Follow the `setNext` calls.",
         "files": {**NODE_FILES, "NodeTrace.java": T1}, "run": "NodeTrace", "hide": HIDE,
         "question": "Which diagram shows the list starting at `head`?",
         "choices": ["head -> 4 -> 8 -> 6 -> null", "head -> 8 -> 4 -> 6 -> null", "head -> 8 -> 6 -> 4 -> null", "head -> 8 -> 4 -> null"],
         "answer": 1,
         "explain": "`head` is `b` (8). `b`'s next is `a` (4), and `a`'s next is `c` (6). `c`'s next was never set, so it's `null`."},
        {"type": "trace", "id": "node-trace2", "kind": "linked",
         "prompt": "Trace each assignment. `n` is reused for a second node halfway through.",
         "files": {**NODE_FILES, "FrontTrace.java": T2}, "run": "FrontTrace", "hide": HIDE,
         "question": "Which diagram shows the list at the end?",
         "choices": ["head -> 7 -> 2 -> 5 -> null", "head -> 2 -> 5 -> 7 -> null", "head -> 2 -> 7 -> 5 -> null", "head -> 2 -> 7 -> null"],
         "answer": 2,
         "explain": "Lines 4 to 6 put 2 in front of 5. Then the new node 7 points at `head.getNext()`, the 5, and `head.setNext(n)` makes the 2 point at 7. So 7 is inserted between 2 and 5."},
        {"type": "predict", "id": "node-follow",
         "prompt": "What does this print?",
         "files": {**NODE_FILES, "Follow.java": P1}, "run": "Follow", "hide": HIDE,
         "choices": ["20 30\nnull", "10 20\nnull", "20 30\n30", "20 30\n0"],
         "answer": 0,
         "explain": "`second` refers to the node holding 20, whose next holds 30. That node is last, so its `getNext()` is `null`, and printing a `null` reference prints `null`."},
        {"type": "quiz", "id": "node-one",
         "question": "Which statement about linked lists is true?",
         "choices": ["A linked list needs at least two nodes", "A single node whose `next` is `null` is a linked list of one value", "The head must always hold the smallest value", "Nodes must be created in the order they appear in the list"],
         "answer": 1,
         "explain": "Every node on its own is a linked list. Nodes can be created in any order; it's the `next` references that decide the order of the list."},
    ],
    "sources": [ALGS4_13, OPENDSA_STACK, OBJECTS_TUT, NPE],
}
