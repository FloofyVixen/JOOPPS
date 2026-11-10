from sources import ALGS4_13, OPENDSA_STACK
from ds_code import NODE, NODE_FILES

HIDE = ["Node.java", "Show.java"]

OPS = """public class ListOps {
    public static Node build(int... values) {
        Node head = null;
        for (int i = values.length - 1; i >= 0; i--) {
            Node node = new Node(values[i]);
            node.setNext(head);
            head = node;
        }
        return head;
    }

    // O(1): the new node becomes the head.
    public static Node addFirst(Node head, int value) {
        Node node = new Node(value);
        node.setNext(head);
        return node;
    }

    // O(n): walk to the last node, then attach after it.
    public static Node addLast(Node head, int value) {
        Node node = new Node(value);
        if (head == null) {
            return node;
        }
        Node current = head;
        while (current.getNext() != null) {
            current = current.getNext();
        }
        current.setNext(node);
        return head;
    }

    // O(1) once you have the node: link the new node in after it.
    public static void insertAfter(Node before, int value) {
        Node node = new Node(value);
        node.setNext(before.getNext());
        before.setNext(node);
    }

    // O(1): the second node becomes the head.
    public static Node removeFirst(Node head) {
        return head.getNext();
    }

    // O(1) once you have the node: skip over the node after it.
    public static void removeAfter(Node before) {
        before.setNext(before.getNext().getNext());
    }

    // O(n): find the node before the one to remove.
    public static Node removeValue(Node head, int value) {
        if (head == null) {
            return null;
        }
        if (head.getData() == value) {
            return head.getNext();
        }
        Node current = head;
        while (current.getNext() != null) {
            if (current.getNext().getData() == value) {
                current.setNext(current.getNext().getNext());
                return head;
            }
            current = current.getNext();
        }
        return head;
    }
}
"""
DEMO = """public class EditDemo {
    public static void main(String[] args) {
        Node head = ListOps.build(10, 20, 30);
        System.out.println(Show.chain(head));
        head = ListOps.addFirst(head, 5);
        System.out.println(Show.chain(head));
        head = ListOps.addLast(head, 40);
        System.out.println(Show.chain(head));
        ListOps.insertAfter(head.getNext(), 15);
        System.out.println(Show.chain(head));
        head = ListOps.removeFirst(head);
        System.out.println(Show.chain(head));
        ListOps.removeAfter(head);
        System.out.println(Show.chain(head));
        head = ListOps.removeValue(head, 30);
        System.out.println(Show.chain(head));
    }
}
"""
FILES = {**NODE_FILES, "ListOps.java": OPS, "EditDemo.java": DEMO}
T1 = """public class EditTrace {
    public static void main(String[] args) {
        Node head = ListOps.build(1, 2, 3, 4);
        head = ListOps.removeValue(head, 3);
        head = ListOps.addFirst(head, 9);
        ListOps.insertAfter(head.getNext().getNext(), 7);
        head = ListOps.removeFirst(head);
        System.out.println(Show.chain(head));
    }
}
"""
T2 = """public class LinkTrace {
    public static void main(String[] args) {
        Node head = ListOps.build(6, 7, 8);
        Node second = head.getNext();
        head.setNext(second.getNext());
        second.setNext(head);
        head = second;
        System.out.println(Show.chain(head));
    }
}
"""
BL = OPS.replace("""        if (head.getData() == value) {
            return head.getNext();
        }
        Node current = head;
        while (current.getNext() != null) {
            if (current.getNext().getData() == value) {
                current.setNext(current.getNext().getNext());""", """        if (head.getData() == value) {
            return [[newhead]];
        }
        Node current = head;
        while (current.getNext() != null) {
            if ([[found]] == value) {
                current.setNext([[skip]]);""")
BLT = """public class RemoveTester {
    public static void main(String[] args) {
        System.out.println(Show.chain(ListOps.removeValue(ListOps.build(4, 5, 6), 4)));
        System.out.println(Show.chain(ListOps.removeValue(ListOps.build(4, 5, 6), 6)));
        System.out.println(Show.chain(ListOps.removeValue(ListOps.build(4, 5, 6), 9)));
    }
}
"""

LESSON = {
    "id": "link-change",
    "title": "Adding and removing nodes",
    "summary": "Changing a linked list means changing `next` references: a node is added by linking it in, and removed by linking around it. Nothing else has to move.",
    "goals": [
        "Add a node at the front, at the end, and after a given node",
        "Remove the first node, the node after a given node, and a node by value",
        "Set references in the right order so no part of the list is lost",
        "Say which operations are O(1) and which are O(n), with only a head reference",
    ],
    "cos225": "The Exam 2 guide's linked-list problems ask you to draw the list after changes like these and to write a few lines that make them. The guide says not to assume a tail reference, so adding at the end walks the list.",
    "blocks": [
        {"type": "h", "text": "Changing links, not moving values"},
        {"type": "p", "text": "In an array, inserting in the middle shifts every later value. In a linked list, the nodes stay where they are in memory: you only change one or two `next` references. Here are the six basic changes as static methods. Methods that might change which node is first **return the new head**, and the caller writes `head = ...`."},
        {"type": "code", "files": {"Node.java": NODE, "ListOps.java": OPS}, "hide": ["Node.java"], "show": False},
        {"type": "code", "files": FILES, "run": "EditDemo", "hide": HIDE},

        {"type": "h", "text": "Adding"},
        {"type": "list", "items": [
            "**At the front** (`addFirst`): the new node's `next` is the old head, and it becomes the head. O(1).",
            "**At the end** (`addLast`): walk to the last node, the one whose `next` is `null`, and set its `next` to the new node. With only a head reference that walk is O(n). An empty list is a special case: the new node becomes the head.",
            "**After a node** (`insertAfter`): the new node takes over the old `next`, then the earlier node points at the new one. O(1), once you have the earlier node.",
        ]},
        {"type": "p", "text": "In `insertAfter`, the order of the two lines matters. If `before.setNext(node)` ran first, `before.getNext()` would already be the new node, so the new node would point at itself and the rest of the list would be cut off. **Link the new node in first, then redirect the old link.**"},
        {"type": "diagram", "kind": "linked", "state": "head -> 5 -> 10 -> 15 -> 20 -> 30 -> 40 -> null",
         "files": FILES, "run": "EditDemo", "line": 3,
         "caption": "After `addFirst(5)`, `addLast(40)` and `insertAfter(head.getNext(), 15)`, which puts 15 after the node holding 10."},

        {"type": "h", "text": "Removing"},
        {"type": "list", "items": [
            "**The first node** (`removeFirst`): the head becomes `head.getNext()`. O(1).",
            "**The node after a node** (`removeAfter`): point `before` at the node two along, skipping one. The skipped node is no longer reachable, so it's gone. O(1).",
            "**By value** (`removeValue`): you need the node **before** the one to remove, so the loop looks one ahead with `current.getNext().getData()`. If the head itself matches, return `head.getNext()` instead. O(n).",
        ]},
        {"type": "diagram", "kind": "linked", "state": "head -> 10 -> 20 -> 40 -> null",
         "files": FILES, "run": "EditDemo", "line": 6,
         "caption": "The end of the demo: `removeFirst` took 5, `removeAfter(head)` skipped 15, and `removeValue(head, 30)` linked 20 straight to 40."},
        {"type": "note", "label": "No tail", "text": "Some linked lists also keep a `tail` reference to the last node, which makes adding at the end O(1). The exam guide says not to assume one, so don't use a tail in your answers unless the question gives you one."},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "change-trace1", "kind": "linked",
         "prompt": "`ListOps` is the class above. Trace each call.",
         "files": {**FILES, "EditTrace.java": T1}, "run": "EditTrace", "hide": HIDE + ["ListOps.java", "EditDemo.java"],
         "question": "Which diagram shows the list at the end?",
         "choices": ["head -> 1 -> 2 -> 7 -> 4 -> null", "head -> 1 -> 7 -> 2 -> 4 -> null", "head -> 9 -> 1 -> 2 -> 7 -> 4 -> null", "head -> 1 -> 2 -> 4 -> 7 -> null"],
         "answer": 0,
         "explain": "Removing 3 gives 1, 2, 4. Adding 9 in front gives 9, 1, 2, 4. `head.getNext().getNext()` is the node holding 2, so 7 goes after it: 9, 1, 2, 7, 4. Removing the first node leaves 1, 2, 7, 4."},
        {"type": "trace", "id": "change-trace2", "kind": "linked",
         "prompt": "This code changes links directly. Draw the nodes and redraw an arrow at each `setNext`.",
         "files": {**FILES, "LinkTrace.java": T2}, "run": "LinkTrace", "hide": HIDE + ["ListOps.java", "EditDemo.java"],
         "question": "Which diagram shows the list at the end?",
         "choices": ["head -> 6 -> 7 -> 8 -> null", "head -> 7 -> 6 -> 8 -> null", "head -> 7 -> 8 -> 6 -> null", "head -> 7 -> 6 -> null"],
         "answer": 1,
         "explain": "Line 5 links 6 straight to 8, cutting 7 out. Line 6 points 7 at 6, and line 7 makes 7 the head. The first two nodes have swapped places: 7, 6, 8."},
        {"type": "blanks", "id": "change-remove", "title": "Remove by value",
         "prompt": "Finish `removeValue`. It removes the first node holding `value` and returns the head of the changed list.",
         "files": {**NODE_FILES, "ListOps.java": BL, "RemoveTester.java": BLT}, "run": "RemoveTester", "hide": HIDE,
         "output": "head -> 5 -> 6 -> null\nhead -> 4 -> 5 -> null\nhead -> 4 -> 5 -> 6 -> null",
         "blanks": {
             "newhead": {"accept": ["head.getNext()"], "hint": "If the head is the one to remove, the second node becomes the head.",
                         "wrong": [{"answer": "null", "why": "That throws away the whole list, not just its first node."}]},
             "found": {"accept": ["current.getNext().getData()"], "hint": "Look one node ahead, so `current` is the node **before** the match.",
                       "wrong": [{"answer": "current.getData()", "why": "By the time `current` holds the value, you've passed the node whose `next` needs changing, so the node **after** the match is removed instead."}]},
             "skip": {"accept": ["current.getNext().getNext()"], "hint": "Link around the matching node.",
                      "wrong": [{"answer": "current.getNext()", "why": "That sets `next` to what it already was, so nothing is removed."}]},
         },
         "explain": "Removing means linking the node before to the node after. Looking one node ahead keeps `current` on the node before."},
        {"type": "quiz", "id": "change-cost",
         "question": "A linked list has only a `head` reference. Which operation is O(n)?",
         "choices": ["Adding a value at the front", "Removing the first node", "Adding a value at the end", "Reading the first value"],
         "answer": 2,
         "explain": "Without a tail reference, adding at the end has to walk past every node to find the last one. The other three only touch the head."},
    ],
    "sources": [ALGS4_13, OPENDSA_STACK],
}
