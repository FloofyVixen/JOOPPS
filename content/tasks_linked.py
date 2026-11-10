"""Write-it-yourself tasks for unit 16, Linked Data Structures. Compiled and run by build.py."""
from tasks_classes import task
from tasks_stacks import given
from ds_code import NODE, NODE_FILES

NODE_ONLY = {"Node.java": NODE}
GIVEN = "`Node` and `Show` (with `Show.chain(head)`) are already in the editor."
GIVEN_NODE = "`Node` is already in the editor."

BUILD = """    public static Node build(int... values) {
        Node head = null;
        for (int i = values.length - 1; i >= 0; i--) {
            Node node = new Node(values[i]);
            node.setNext(head);
            head = node;
        }
        return head;
    }
"""
BUILD_NOTE = " Copy this `build` helper into your class to make test lists: it's the add-at-front loop from the lessons."

NODES = [
    given(task("w-link-byhand", "Build a list by hand",
         "Write `ByHand`. Its `main` creates three nodes holding 3, 1 and 4 with `new`, links them in that order with `setNext`, stores the first in a variable `head`, and prints `Show.chain(head)`. Then it prints the data of the last node, reached from `head` with `getNext()` calls. " + GIVEN,
         {"ByHand.java": """public class ByHand {
    public static void main(String[] args) {
        Node head = new Node(3);
        Node second = new Node(1);
        Node third = new Node(4);
        head.setNext(second);
        second.setNext(third);
        System.out.println(Show.chain(head));
        System.out.println(head.getNext().getNext().getData());
    }
}
"""}, "ByHand", "head -> 3 -> 1 -> 4 -> null\n4",
         checks=[{"pattern": r"getNext\(\)\s*\.\s*getNext\(\)", "message": "Reach the last node from `head` with `head.getNext().getNext()`."}]), NODE_FILES),

    given(task("w-link-addfront", "An add-at-front method",
         "Write `Front` with `public static Node addFront(Node head, int value)`, which puts a new node holding `value` in front and returns the new head. `main` starts with an empty list (`null`), adds 1, 2 and 3 with `head = addFront(head, ...)`, and prints the chain. " + GIVEN,
         {"Front.java": """public class Front {
    public static Node addFront(Node head, int value) {
        Node node = new Node(value);
        node.setNext(head);
        return node;
    }

    public static void main(String[] args) {
        Node head = null;
        head = addFront(head, 1);
        head = addFront(head, 2);
        head = addFront(head, 3);
        System.out.println(Show.chain(head));
    }
}
"""}, "Front", "head -> 3 -> 2 -> 1 -> null",
         tests={"CheckFront.java": """public class CheckFront {
    public static void main(String[] args) {
        Node one = Front.addFront(null, 8);
        System.out.println(Show.chain(one));
        Node two = Front.addFront(one, 9);
        System.out.println(Show.chain(two) + " " + (two.getNext() == one));
    }
}
"""}, tests_run="CheckFront", tests_output="head -> 8 -> null\nhead -> 9 -> 8 -> null true"), NODE_FILES),

    given(task("w-link-second", "The second value, safely",
         "Write `Second` with `public static int secondValue(Node head)`, which returns the data of the second node, or -1 if the list has fewer than two nodes. Don't let it throw a `NullPointerException`. `main` prints it for an empty list, a one-node list, and the list 5 → 6 → 7. " + GIVEN,
         {"Second.java": """public class Second {
    public static int secondValue(Node head) {
        if (head == null || head.getNext() == null) {
            return -1;
        }
        return head.getNext().getData();
    }

    public static void main(String[] args) {
        System.out.println(secondValue(null));
        System.out.println(secondValue(new Node(5)));
        Node head = new Node(5);
        head.setNext(new Node(6));
        head.getNext().setNext(new Node(7));
        System.out.println(secondValue(head));
    }
}
"""}, "Second", "-1\n-1\n6",
         hints=["`||` stops at the first `true`, so `head.getNext()` is only called when `head` isn't `null`."]), NODE_FILES),
]

TRAVERSE = [
    given(task("w-link-size", "Size with a while loop",
         "Write `Size` with `public static int size(Node head)` that counts the nodes using a `while` loop and a `current` reference. `main` prints the size of an empty list and of a list of 4 nodes." + BUILD_NOTE + " " + GIVEN_NODE,
         {"Size.java": """public class Size {
""" + BUILD + """
    public static int size(Node head) {
        int count = 0;
        Node current = head;
        while (current != null) {
            count++;
            current = current.getNext();
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(size(null));
        System.out.println(size(build(9, 8, 7, 6)));
    }
}
"""}, "Size", "0\n4",
         checks=[{"pattern": r"while\s*\(", "message": "Use a `while` loop."},
                 {"pattern": r"current\s*=\s*current\.getNext\(\)", "message": "Move along with `current = current.getNext()`."}]), NODE_ONLY),

    given(task("w-link-max", "Largest value with a for loop",
         "Write `Max` with `public static int max(Node head)` for a non-empty list, using a `for` loop over the nodes: `for (Node current = ...; ...; ...)`. `main` prints the max of 3, 17, -2, 9 and of -5, -1, -8." + BUILD_NOTE + " " + GIVEN_NODE,
         {"Max.java": """public class Max {
""" + BUILD + """
    public static int max(Node head) {
        int best = head.getData();
        for (Node current = head.getNext(); current != null; current = current.getNext()) {
            if (current.getData() > best) {
                best = current.getData();
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(max(build(3, 17, -2, 9)));
        System.out.println(max(build(-5, -1, -8)));
    }
}
"""}, "Max", "17\n-1",
         tests={"CheckMax.java": """public class CheckMax {
    public static void main(String[] args) {
        System.out.println(Max.max(new Node(4)));
        Node h = new Node(1);
        h.setNext(new Node(2));
        System.out.println(Max.max(h));
    }
}
"""}, tests_run="CheckMax", tests_output="4\n2",
         checks=[{"pattern": r"for\s*\(\s*Node\s+\w+\s*=", "message": "Traverse with `for (Node current = ...; ...; ...)`."}]), NODE_ONLY),

    given(task("w-link-get", "Get by index",
         "Write `Get` with `public static int get(Node head, int index)`, which steps `index` times from the head and returns that node's data. If `index` is negative or the list runs out first, throw `new IndexOutOfBoundsException(\"index \" + index)`. `main` prints `get` at 0 and 2 of the list 10, 20, 30, then catches the exception for index 3 and prints its message." + BUILD_NOTE + " " + GIVEN_NODE,
         {"Get.java": """public class Get {
""" + BUILD + """
    public static int get(Node head, int index) {
        if (index < 0) {
            throw new IndexOutOfBoundsException("index " + index);
        }
        Node current = head;
        for (int i = 0; i < index && current != null; i++) {
            current = current.getNext();
        }
        if (current == null) {
            throw new IndexOutOfBoundsException("index " + index);
        }
        return current.getData();
    }

    public static void main(String[] args) {
        Node head = build(10, 20, 30);
        System.out.println(get(head, 0) + " " + get(head, 2));
        try {
            get(head, 3);
        } catch (IndexOutOfBoundsException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""}, "Get", "10 30\nindex 3",
         tests={"CheckGet.java": """public class CheckGet {
    public static void main(String[] args) {
        String out = "";
        try {
            Get.get(null, 0);
        } catch (IndexOutOfBoundsException e) {
            out += e.getMessage() + "; ";
        }
        try {
            Get.get(new Node(1), -1);
        } catch (IndexOutOfBoundsException e) {
            out += e.getMessage();
        }
        System.out.println(out);
    }
}
"""}, tests_run="CheckGet", tests_output="index 0; index -1",
         hints=["Stop early if `current` becomes `null`, then check after the loop: if it's `null`, the index was past the end."]), NODE_ONLY),
]

CHANGE = [
    given(task("w-link-addlast", "Add at the end",
         "Write `AddLast` with `public static Node addLast(Node head, int value)`, which attaches a new node after the last node (no tail reference: walk there) and returns the head. Handle the empty list. `main` starts with `null`, adds 1, 2 and 3 at the end and prints the chain. " + GIVEN,
         {"AddLast.java": """public class AddLast {
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

    public static void main(String[] args) {
        Node head = null;
        head = addLast(head, 1);
        head = addLast(head, 2);
        head = addLast(head, 3);
        System.out.println(Show.chain(head));
    }
}
"""}, "AddLast", "head -> 1 -> 2 -> 3 -> null",
         tests={"CheckAddLast.java": """public class CheckAddLast {
    public static void main(String[] args) {
        Node head = new Node(5);
        Node same = AddLast.addLast(head, 6);
        System.out.println(Show.chain(same) + " " + (same == head));
    }
}
"""}, tests_run="CheckAddLast", tests_output="head -> 5 -> 6 -> null true"), NODE_FILES),

    given(task("w-link-removeall", "Remove every match",
         "Write `RemoveAll` with `public static Node removeAll(Node head, int value)`, which removes **every** node holding `value` and returns the new head. First drop matching nodes at the front (`while (head != null && head.getData() == value)`), then walk the rest looking one node ahead. `main` prints the result for 7, 7, 1, 7, 2, 7 with `value` 7." + BUILD_NOTE + " " + GIVEN,
         {"RemoveAll.java": """public class RemoveAll {
""" + BUILD + """
    public static Node removeAll(Node head, int value) {
        while (head != null && head.getData() == value) {
            head = head.getNext();
        }
        Node current = head;
        while (current != null && current.getNext() != null) {
            if (current.getNext().getData() == value) {
                current.setNext(current.getNext().getNext());
            } else {
                current = current.getNext();
            }
        }
        return head;
    }

    public static void main(String[] args) {
        System.out.println(Show.chain(removeAll(build(7, 7, 1, 7, 2, 7), 7)));
    }
}
"""}, "RemoveAll", "head -> 1 -> 2 -> null",
         tests={"CheckRemoveAll.java": """public class CheckRemoveAll {
    public static void main(String[] args) {
        Node all = new Node(3);
        all.setNext(new Node(3));
        System.out.println(Show.chain(RemoveAll.removeAll(all, 3)));
        Node h = new Node(1);
        h.setNext(new Node(2));
        h.getNext().setNext(new Node(2));
        System.out.println(Show.chain(RemoveAll.removeAll(h, 2)));
    }
}
"""}, tests_run="CheckRemoveAll", tests_output="head -> null\nhead -> 1 -> null",
         hints=["After removing the node ahead, **don't** move `current`: the new node ahead might match too."]), NODE_FILES),

    given(task("w-link-sorted", "Insert in order",
         "Write `Sorted` with `public static Node insertSorted(Node head, int value)`: the list is in increasing order, and the new node must go where it keeps it that way. Returns the head. Cases: empty list, new smallest value (new head), and somewhere after (find the last node whose data is less than `value`, then insert after it). `main` inserts 5, 1, 9 and 4 into an empty list and prints the chain. " + GIVEN,
         {"Sorted.java": """public class Sorted {
    public static Node insertSorted(Node head, int value) {
        Node node = new Node(value);
        if (head == null || value <= head.getData()) {
            node.setNext(head);
            return node;
        }
        Node current = head;
        while (current.getNext() != null && current.getNext().getData() < value) {
            current = current.getNext();
        }
        node.setNext(current.getNext());
        current.setNext(node);
        return head;
    }

    public static void main(String[] args) {
        Node head = null;
        head = insertSorted(head, 5);
        head = insertSorted(head, 1);
        head = insertSorted(head, 9);
        head = insertSorted(head, 4);
        System.out.println(Show.chain(head));
    }
}
"""}, "Sorted", "head -> 1 -> 4 -> 5 -> 9 -> null",
         tests={"CheckSorted.java": """public class CheckSorted {
    public static void main(String[] args) {
        Node head = null;
        int[] values = {3, 3, 0, 8, 6, -1};
        for (int v : values) {
            head = Sorted.insertSorted(head, v);
        }
        System.out.println(Show.chain(head));
    }
}
"""}, tests_run="CheckSorted", tests_output="head -> -1 -> 0 -> 3 -> 3 -> 6 -> 8 -> null"), NODE_FILES),
]

TASKS = {"link-nodes": NODES, "link-traverse": TRAVERSE, "link-change": CHANGE}
