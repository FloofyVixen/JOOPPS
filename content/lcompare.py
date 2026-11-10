from sources import ALGS4_13, ALGS4_14, ARRAYLIST_API, LINKEDLIST_API
from ds_code import NODE

INDEXED = """public class IndexLoop {
    public static long moves = 0;

    // get(index) on a chain of nodes: walk index steps from the head.
    public static int get(Node head, int index) {
        Node current = head;
        for (int i = 0; i < index; i++) {
            current = current.getNext();
            moves++;
        }
        return current.getData();
    }

    public static void main(String[] args) {
        int n = 1000;
        Node head = null;
        for (int i = n; i >= 1; i--) {
            Node node = new Node(i);
            node.setNext(head);
            head = node;
        }

        long total = 0;
        for (int i = 0; i < n; i++) {
            total += get(head, i);
        }
        System.out.println("by index: sum " + total + ", " + moves + " moves");

        moves = 0;
        total = 0;
        for (Node current = head; current != null; current = current.getNext()) {
            total += current.getData();
            moves++;
        }
        System.out.println("by walking: sum " + total + ", " + moves + " moves");
    }
}
"""

ITEMS = [
    ("`get(i)` on an `ArrayList`", "O(1)", "It reads `array[i]` directly."),
    ("`get(i)` on a linked list", "O(n)", "It walks `i` nodes from the head."),
    ("Adding at index 0 of an `ArrayList`", "O(n)", "Every value shifts one slot right."),
    ("Adding at index 0 of a linked list", "O(1)", "The new node becomes the head: one relink."),
    ("Adding at the end of an `ArrayList` (array not full)", "O(1)", "It writes the next free slot."),
    ("Adding at the end of a linked list with only a head reference", "O(n)", "It walks to the last node first."),
    ("Removing the first value of an `ArrayList`", "O(n)", "Every later value shifts one slot left."),
    ("Removing the first node of a linked list", "O(1)", "`head = head.getNext()`."),
    ("`push` on `ArrayStack` (array not full)", "O(1)", None),
    ("`pop` on `LinkedStack`", "O(1)", None),
]

LESSON = {
    "id": "lcompare",
    "title": "Array versus linked performance",
    "summary": "Arrays are fast at reaching any position; linked lists are fast at changing the front. Knowing which operations are O(1) and which are O(n) for each tells you which to use.",
    "goals": [
        "State the big O of get, add and remove at each end for array and linked lists",
        "Explain why looping with `get(i)` over a linked list is O(n²)",
        "Compare the memory each structure uses",
        "Say where the top of an array stack and a linked stack is, and why",
    ],
    "cos225": "The Exam 2 guide: contrast array and linked list implementations of stacks and queues, and where the top is located. Expect matching questions on which operations are O(1) and which are O(n).",
    "blocks": [
        {"type": "h", "text": "The cost of each operation"},
        {"type": "p", "text": "An array keeps values side by side, so it can jump straight to any index, but adding or removing anywhere except the end shifts the values after it. A linked list can only be entered at the head, so reaching index `i` means walking `i` nodes, but once you're at a node, linking in or out is one or two reference changes."},
        {"type": "list", "items": [
            "**Read by index**: array O(1); linked O(n).",
            "**Add or remove at the front**: array O(n); linked O(1).",
            "**Add at the end**: array O(1) (on average, counting the occasional doubling); linked O(n) with only a head reference.",
            "**Add or remove in the middle**: O(n) for both. The array shifts values; the linked list walks to the spot.",
            "**Size**: O(1) for both, as long as the class keeps a count.",
        ]},
        {"type": "p", "text": "Java's own `LinkedList` keeps references to both ends (it's doubly linked), so its documentation says operations that index into it traverse from whichever end is closer. The list you write for this course, with only a head, always starts from the front."},

        {"type": "h", "text": "The O(n²) loop"},
        {"type": "p", "text": "A loop that calls `get(i)` for every index is fine for an array, O(n) in total. On a linked list each `get(i)` walks from the head, so the loop does 0 + 1 + 2 + … + (n − 1) moves: O(n²). Walking the chain once does the same job in O(n):"},
        {"type": "code", "files": {"Node.java": NODE, "IndexLoop.java": INDEXED}, "run": "IndexLoop", "hide": ["Node.java"],
         "after": "Same sum, 500 times more moves. To visit every value of a linked list, traverse it with `getNext()` (or Java's for-each loop, which does that for you), not with `get(i)`."},

        {"type": "h", "text": "Memory"},
        {"type": "list", "items": [
            "An array is one block. A growable array usually has spare capacity: after doubling, up to half its slots can be empty.",
            "A linked list has no spare slots, but every value has its own node object, which costs an extra `next` reference plus the object's own overhead.",
        ]},

        {"type": "h", "text": "Where the top goes"},
        {"type": "p", "text": "Both stack implementations put the top where pushing and popping are O(1):"},
        {"type": "list", "items": [
            "**ArrayStack**: the top is at the **end** of the used part of the array, index `top - 1`. At index 0, every push and pop would shift the whole array.",
            "**LinkedStack**: the top is the **head**. At the last node, every pop would have to walk the list to find the node before it.",
        ]},
        {"type": "p", "text": "So both give O(1) push, pop and peek. The differences are elsewhere: the array occasionally pays O(n) to grow and may hold empty slots; the linked stack allocates a node per push and never fills up."},

        {"type": "h", "text": "Practice"},
        {"type": "match", "id": "cmp-match",
         "prompt": "Match each operation with its big O.",
         "options": ["O(1)", "O(n)"],
         "items": [{"text": t, "answer": a, **({"why": w} if w else {})} for t, a, w in ITEMS],
         "explain": "Arrays win at indexing and at the end; linked lists win at the front. Stacks use the fast end of each."},
        {"type": "quiz", "id": "cmp-choose",
         "question": "A program mostly reads values by position (`get(i)` with many different `i`s) and rarely adds or removes. Which list fits best?",
         "choices": ["A linked list, because it never runs out of room", "An array-based list such as `ArrayList`, because `get(i)` is O(1)", "Either: they have the same big O for everything", "A linked stack"],
         "answer": 1,
         "explain": "Reading by position is O(1) for an array and O(n) for a linked list."},
        {"type": "quiz", "id": "cmp-front",
         "question": "A program keeps adding and removing at the front of a long list. Which is the better fit?",
         "choices": ["An array-based list", "A linked list", "An array-based list with its top at index 0", "It makes no difference"],
         "answer": 1,
         "explain": "At the front, a linked list changes one reference (O(1)); an array shifts every value (O(n))."},
    ],
    "sources": [ALGS4_13, ALGS4_14, ARRAYLIST_API, LINKEDLIST_API],
}
