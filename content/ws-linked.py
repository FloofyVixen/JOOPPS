from sources import ALGS4_13, OPENDSA_STACK, NPE
from wshelp import step, guided, workshop, task
from tasks_stacks import given
from ds_code import NODE, NODE_FILES
from tasks_linked import BUILD

C1 = """public class Chain {
""" + BUILD + """
    public static String toText(Node head) {
        String result = "";
        for (Node current = head; current != null; current = current.getNext()) {
            result += current.getData() + " ";
        }
        return result.trim();
    }

    public static void main(String[] args) {
        Node head = build(3, 1, 4, 1, 5);
        System.out.println(toText(head));
        System.out.println("[" + toText(null) + "]");
    }
}
"""
C2 = C1.replace("""    public static void main""", """    public static int size(Node head) {
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

    public static void main""").replace("""        System.out.println("[" + toText(null) + "]");""", """        System.out.println(size(head) + " values, sum " + sum(head));""")
C3 = C2.replace("""    public static void main""", """    public static Node reverse(Node head) {
        Node previous = null;
        Node current = head;
        while (current != null) {
            Node next = current.getNext();
            current.setNext(previous);
            previous = current;
            current = next;
        }
        return previous;
    }

    public static void main""").replace("""        System.out.println(size(head) + " values, sum " + sum(head));""", """        head = reverse(head);
        System.out.println(toText(head));
        System.out.println("[" + toText(reverse(null)) + "] " + toText(reverse(new Node(8))));""")

D1 = """public class Dedupe {
""" + BUILD + """
    public static String toText(Node head) {
        String result = "";
        for (Node current = head; current != null; current = current.getNext()) {
            result += current.getData() + " ";
        }
        return result.trim();
    }

    public static int count(Node head, int value) {
        int count = 0;
        Node current = head;
        while (current != null) {
            if (current.getData() == value) {
                count++;
            }
            current = current.getNext();
        }
        return count;
    }

    public static void main(String[] args) {
        Node head = build(1, 1, 2, 3, 3, 3, 4);
        System.out.println(count(head, 3) + " " + count(head, 5));
    }
}
"""
D2 = D1.replace("""    public static void main""", """    public static void removeRepeats(Node head) {
        Node current = head;
        while (current != null && current.getNext() != null) {
            if (current.getNext().getData() == current.getData()) {
                current.setNext(current.getNext().getNext());
            } else {
                current = current.getNext();
            }
        }
    }

    public static void main""").replace("""        System.out.println(count(head, 3) + " " + count(head, 5));""", """        removeRepeats(head);
        System.out.println(toText(head));""")
D3 = D2.replace("""    public static void main""", """    public static Node removeAt(Node head, int index) {
        if (index == 0) {
            return head.getNext();
        }
        Node before = head;
        for (int i = 0; i < index - 1; i++) {
            before = before.getNext();
        }
        before.setNext(before.getNext().getNext());
        return head;
    }

    public static void main""").replace("""        removeRepeats(head);
        System.out.println(toText(head));""", """        removeRepeats(head);
        System.out.println(toText(head));
        head = removeAt(head, 2);
        System.out.println(toText(head));
        head = removeAt(head, 0);
        System.out.println(toText(head));""")

LESSON = workshop(
    "ws-linked", "Workshop: linked nodes",
    "Work directly with nodes: build and measure chains, reverse one in place, clean up repeated values, and join and thin out lists.",
    ["Traverse with `getNext()` using for and while loops",
     "Change `next` references in the right order so nothing is lost",
     "Handle the empty list and the head as special cases"],
    guided("ws-u16-reverse", "Reverse a chain", "Write your own `Node`, then build, measure and finally reverse a chain of nodes without creating any new nodes.", [
        step("Nodes and text", "Create `Node` (an `int` data and a `Node next`, with `getData`, `getNext` and `setNext`). In `Chain`, copy the `build` helper and write `toText(Node head)`, which returns the values separated by single spaces (empty string for an empty list).",
             {"Node.java": NODE, "Chain.java": C1}, "Chain", "3 1 4 1 5\n[]",
             hint="Add each value and a space, then `trim()` the end."),
        step("Size and sum", "Add `size(Node head)` and `sum(Node head)`, each with one traversal loop.",
             {"Node.java": NODE, "Chain.java": C2}, "Chain", "3 1 4 1 5\n5 values, sum 14"),
        step("Reverse in place", "Add `reverse(Node head)`, which returns the head of the reversed list by turning every `next` around. Walk with three references: `previous` (starts `null`), `current` (starts at head), and `next`, saved **before** you change `current`'s link. Each step: save `next`, point `current` back at `previous`, then move `previous` and `current` one step on.",
             {"Node.java": NODE, "Chain.java": C3}, "Chain", "3 1 4 1 5\n5 1 4 1 3\n[] 8",
             hint="At the end `current` is `null` and `previous` is the old last node, the new head. Saving `next` first matters: once you call `setNext(previous)`, the way forward is gone."),
    ]),
    guided("ws-u16-dedupe", "Clean up a sorted list", "Count values, remove repeats from a sorted list, and remove a node by position.", [
        step("Counting", "Create `Node`, then `Dedupe` with `build`, `toText` and `count(Node head, int value)`, which uses a `while` loop to count the nodes holding `value`.",
             {"Node.java": NODE, "Dedupe.java": D1}, "Dedupe", "3 0"),
        step("Removing repeats", "In a sorted list, repeats sit next to each other. Write `removeRepeats(Node head)`: whenever the next node holds the same value as `current`, link around it; otherwise move on. The head never changes, so it returns nothing.",
             {"Node.java": NODE, "Dedupe.java": D2}, "Dedupe", "1 2 3 4",
             hint="Only move `current` when the next node is different, or you'll miss the third 3."),
        step("Removing by position", "Add `removeAt(Node head, int index)`, which returns the new head. Index 0 removes the head; otherwise walk to the node **before** `index` (that's `index - 1` steps) and link around the next one.",
             {"Node.java": NODE, "Dedupe.java": D3}, "Dedupe", "1 2 3 4\n1 2 4\n2 4"),
    ]),
    given(task("ws-u16-concat", "Join two lists",
         "Write `Join` with `public static Node concat(Node a, Node b)`, which links the last node of `a` to the head of `b` and returns the head of the joined list. If `a` is empty, the result is just `b`. `main` joins 1 → 2 with 3 → 4 and prints the chain, then joins an empty list with 5. `Node` and `Show` are already in the editor.",
         {"Join.java": """public class Join {
    public static Node concat(Node a, Node b) {
        if (a == null) {
            return b;
        }
        Node current = a;
        while (current.getNext() != null) {
            current = current.getNext();
        }
        current.setNext(b);
        return a;
    }

    public static void main(String[] args) {
        Node a = new Node(1);
        a.setNext(new Node(2));
        Node b = new Node(3);
        b.setNext(new Node(4));
        System.out.println(Show.chain(concat(a, b)));
        System.out.println(Show.chain(concat(null, new Node(5))));
    }
}
"""}, "Join", "head -> 1 -> 2 -> 3 -> 4 -> null\nhead -> 5 -> null",
         tests={"CheckJoin.java": """public class CheckJoin {
    public static void main(String[] args) {
        Node a = new Node(7);
        System.out.println(Show.chain(Join.concat(a, null)) + " | " + Show.chain(Join.concat(null, null)));
    }
}
"""}, tests_run="CheckJoin", tests_output="head -> 7 -> null | head -> null"), NODE_FILES),
    given(task("ws-u16-everyother", "Keep every other node",
         "Write `Thin` with `public static void removeEveryOther(Node head)`, which removes the 2nd, 4th, 6th… nodes, keeping the 1st, 3rd, 5th… Walk with `current`: link it past its next node, then move to the node that is now next. `main` thins 1 to 7 and prints the chain. `Node` and `Show` are already in the editor.",
         {"Thin.java": """public class Thin {
    public static void removeEveryOther(Node head) {
        Node current = head;
        while (current != null && current.getNext() != null) {
            current.setNext(current.getNext().getNext());
            current = current.getNext();
        }
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        Node last = head;
        for (int i = 2; i <= 7; i++) {
            last.setNext(new Node(i));
            last = last.getNext();
        }
        removeEveryOther(head);
        System.out.println(Show.chain(head));
    }
}
"""}, "Thin", "head -> 1 -> 3 -> 5 -> 7 -> null",
         tests={"CheckThin.java": """public class CheckThin {
    public static void main(String[] args) {
        Thin.removeEveryOther(null);
        Node h = new Node(1);
        h.setNext(new Node(2));
        Thin.removeEveryOther(h);
        System.out.println(Show.chain(h));
    }
}
"""}, tests_run="CheckThin", tests_output="head -> 1 -> null"), NODE_FILES),
    [ALGS4_13, OPENDSA_STACK, NPE],
)
