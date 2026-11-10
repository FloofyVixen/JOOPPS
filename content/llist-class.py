from sources import ALGS4_13, ARRAYLIST_API, LIST_API, GENERICS_TUT
from ds_code import LINEAR_NODE, SIMPLE_LIST, LIST_FILES, main_class, lines

HIDE = ["LinearNode.java", "SimpleLinkedList.java"]

DEMO = main_class("ListDemo", lines(
    'SimpleLinkedList<String> names = new SimpleLinkedList<>();',
    'names.add("Ana");',
    'names.add("Ben");',
    'names.add("Cy");',
    'System.out.println(names + " size " + names.size());',
    'names.add(1, "Dee");',
    'System.out.println(names);',
    'System.out.println(names.get(2));',
    'System.out.println(names.remove(0) + " removed: " + names);',
))
SAME = """import java.util.ArrayList;

public class SameCalls {
    public static void main(String[] args) {
        ArrayList<String> array = new ArrayList<>();
        SimpleLinkedList<String> linked = new SimpleLinkedList<>();
        String[] words = {"red", "green", "blue"};
        for (String w : words) {
            array.add(w);
            linked.add(w);
        }
        array.add(0, "white");
        linked.add(0, "white");
        array.remove(2);
        linked.remove(2);
        for (int i = 0; i < array.size(); i++) {
            System.out.println(array.get(i) + " " + linked.get(i));
        }
    }
}
"""
BAD = main_class("BadIndex", lines(
    'SimpleLinkedList<Integer> list = new SimpleLinkedList<>();',
    'list.add(5);',
    'System.out.println(list.get(1));',
))
T1 = main_class("ListTrace", lines(
    'SimpleLinkedList<Integer> list = new SimpleLinkedList<>();',
    'list.add(10);',
    'list.add(20);',
    'list.add(0, 5);',
    'list.add(2, 15);',
    'list.remove(1);',
    'list.add(30);',
    'System.out.println(list);',
))
BL = SIMPLE_LIST.replace("""        if (index == 0) {
            node.setNext(head);
            head = node;
        } else {
            LinearNode<T> before = nodeAt(index - 1);
            node.setNext(before.getNext());
            before.setNext(node);
        }""", """        if (index == 0) {
            node.setNext(head);
            [[newhead]];
        } else {
            LinearNode<T> before = nodeAt([[beforeidx]]);
            node.setNext([[link]]);
            before.setNext(node);
        }""")
BLT = main_class("InsertTester", lines(
    'SimpleLinkedList<String> list = new SimpleLinkedList<>();',
    'list.add(0, "b");',
    'list.add(0, "a");',
    'list.add(2, "d");',
    'list.add(2, "c");',
    'System.out.println(list + " " + list.size());',
))

LESSON = {
    "id": "llist-class",
    "title": "A linked list with list operations",
    "summary": "Wrap the nodes in a class and you get a list with the same methods as `ArrayList` (add, get, remove, size), built on linked nodes instead of an array.",
    "goals": [
        "Keep `head` and `count` private inside a list class",
        "Use a generic node, `LinearNode<T>`, to store any type",
        "Implement add, add at an index, get, remove and size with nodes",
        "Compare the same calls on an `ArrayList` and a linked list",
    ],
    "cos225": "The Exam 2 guide asks you to compare array-based and linked lists. This lesson builds a linked list with the `ArrayList`-style operations; the next two use linked nodes for a stack and compare the costs.",
    "blocks": [
        {"type": "h", "text": "From loose nodes to a list class"},
        {"type": "p", "text": "In the last unit, the head was a local variable and every method had to return the new head. A list class keeps `head` (and a `count` of nodes) as private fields, so its methods can change them directly, and outside code just calls `add` and `get`, never touching a node."},
        {"type": "p", "text": "The node is now generic, so a list can hold any type. It's the same as `Node`, with `T element` in place of `int data`:"},
        {"type": "code", "files": {"LinearNode.java": LINEAR_NODE}, "show": False},

        {"type": "h", "text": "SimpleLinkedList"},
        {"type": "p", "text": "Every method here uses something from unit 16. `nodeAt(index)` walks `index` steps from the head; `add(index, ...)` and `remove(index)` use it to find the node **before** the position and relink around it. Position 0 is the special case, because there the head itself changes."},
        {"type": "code", "files": LIST_FILES, "hide": ["LinearNode.java"], "show": False},
        {"type": "code", "files": {**LIST_FILES, "ListDemo.java": DEMO}, "run": "ListDemo", "hide": HIDE},
        {"type": "list", "items": [
            "`count` is updated by every add and remove, so `size()` is O(1): it doesn't walk the list.",
            "`nodeAt` and `checkIndex` are `private` helpers. Outside code can't reach the nodes.",
            "`toString` prints the chain, so `System.out.println(names)` shows the nodes in order.",
        ]},

        {"type": "h", "text": "Same methods, different insides"},
        {"type": "p", "text": "Because the methods match, code that adds, gets and removes works with either an `ArrayList` or this class, and gets the same answers:"},
        {"type": "code", "files": {**LIST_FILES, "SameCalls.java": SAME}, "run": "SameCalls", "hide": HIDE},
        {"type": "p", "text": "What differs is the cost. `get(i)` on an `ArrayList` reads `array[i]` directly; on a linked list it walks `i` nodes. Adding at index 0 shifts every value in an `ArrayList`, but is one relink in a linked list. Lesson 3 of this unit puts the costs side by side."},
        {"type": "p", "text": "Bad indexes are refused the same way `ArrayList` refuses them:"},
        {"type": "code", "files": {**LIST_FILES, "BadIndex.java": BAD}, "run": "BadIndex", "hide": HIDE, "expect": "runtime"},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "ll-trace", "kind": "linked",
         "prompt": "Indexes count from the head, starting at 0. After each insert or removal, the indexes of later nodes change.",
         "files": {**LIST_FILES, "ListTrace.java": T1}, "run": "ListTrace", "hide": HIDE,
         "question": "Which diagram shows the list at the end?",
         "choices": ["head -> 5 -> 15 -> 20 -> 30 -> null", "head -> 5 -> 10 -> 20 -> 30 -> null", "head -> 10 -> 15 -> 20 -> 30 -> null", "head -> 5 -> 10 -> 15 -> 30 -> null"],
         "answer": 0,
         "explain": "10, 20; then 5 at index 0: 5, 10, 20; then 15 at index 2: 5, 10, 15, 20. Removing index 1 takes 10: 5, 15, 20. Adding 30 at the end: 5, 15, 20, 30."},
        {"type": "blanks", "id": "ll-insert", "title": "Insert at an index",
         "prompt": "Finish the middle of `add(int index, T element)`.",
         "files": {"LinearNode.java": LINEAR_NODE, "SimpleLinkedList.java": BL, "InsertTester.java": BLT}, "run": "InsertTester",
         "hide": ["LinearNode.java"],
         "output": "head -> a -> b -> c -> d -> null 4",
         "blanks": {
             "newhead": {"accept": ["head = node"], "hint": "At index 0 the new node becomes the head.",
                         "wrong": [{"answer": "node = head", "why": "That changes the local variable `node`, not the field: the list never gets its new first node."}]},
             "beforeidx": {"accept": ["index - 1"], "hint": "You need the node just before the new position.",
                           "wrong": [{"answer": "index", "why": "Then the new node goes in one place too late: `c` ends up after `d`."}]},
             "link": {"accept": ["before.getNext()"], "hint": "The new node takes over whatever came after `before`.",
                      "wrong": [{"answer": "null", "why": "That cuts off every node after the new one."}]},
         },
         "explain": "Find the node before the position, point the new node at what came after it, then point `before` at the new node."},
        {"type": "quiz", "id": "ll-size",
         "question": "Why is `size()` O(1) in `SimpleLinkedList`, when counting nodes takes a full traversal?",
         "choices": ["Because linked lists can't grow", "Because the class keeps a `count` field, updated by every add and remove", "Because Java caches method results", "Because `head` stores the size"],
         "answer": 1,
         "explain": "Updating `count` costs one step per add or remove, and saves walking the whole list every time someone asks for the size."},
    ],
    "sources": [ALGS4_13, ARRAYLIST_API, LIST_API, GENERICS_TUT],
}
