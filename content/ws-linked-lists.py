from sources import ALGS4_13, OPENDSA_STACK, ARRAYLIST_API, EMPTYSTACK_API
from wshelp import step, guided, workshop, task
from tasks_stacks import given
from tasks_llists import extend
from ds_code import LINEAR_NODE, LIST_FILES

L1 = """public class SimpleLinkedList<T> {
    private LinearNode<T> head;
    private int count;

    public void add(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        if (head == null) {
            head = node;
        } else {
            LinearNode<T> current = head;
            while (current.getNext() != null) {
                current = current.getNext();
            }
            current.setNext(node);
        }
        count++;
    }

    public int size() {
        return count;
    }

    @Override
    public String toString() {
        String result = "head";
        LinearNode<T> current = head;
        while (current != null) {
            result += " -> " + current.getElement();
            current = current.getNext();
        }
        return result + " -> null";
    }
}
"""
L2 = L1.replace("""    public int size() {""", """    public T get(int index) {
        if (index < 0 || index >= count) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + count);
        }
        LinearNode<T> current = head;
        for (int i = 0; i < index; i++) {
            current = current.getNext();
        }
        return current.getElement();
    }

    public int size() {""")
L3 = L2.replace("""    public int size() {""", """    public T remove(int index) {
        if (index < 0 || index >= count) {
            throw new IndexOutOfBoundsException("Index " + index + ", size " + count);
        }
        T result;
        if (index == 0) {
            result = head.getElement();
            head = head.getNext();
        } else {
            LinearNode<T> before = head;
            for (int i = 0; i < index - 1; i++) {
                before = before.getNext();
            }
            result = before.getNext().getElement();
            before.setNext(before.getNext().getNext());
        }
        count--;
        return result;
    }

    public int size() {""")
LT1 = """public class ListTester {
    public static void main(String[] args) {
        SimpleLinkedList<String> list = new SimpleLinkedList<>();
        list.add("milk");
        list.add("eggs");
        list.add("rice");
        System.out.println(list + " " + list.size());
    }
}
"""
LT2 = """public class ListTester {
    public static void main(String[] args) {
        SimpleLinkedList<String> list = new SimpleLinkedList<>();
        list.add("milk");
        list.add("eggs");
        list.add("rice");
        for (int i = 0; i < list.size(); i++) {
            System.out.println(i + ": " + list.get(i));
        }
        try {
            list.get(3);
        } catch (IndexOutOfBoundsException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""
LT3 = """public class ListTester {
    public static void main(String[] args) {
        SimpleLinkedList<String> list = new SimpleLinkedList<>();
        list.add("milk");
        list.add("eggs");
        list.add("rice");
        list.add("tea");
        System.out.println(list.remove(2) + " " + list);
        System.out.println(list.remove(0) + " " + list);
        System.out.println(list.remove(1) + " " + list + " " + list.size());
    }
}
"""

S1 = """public class LinkedStack<T> {
    private LinearNode<T> top;
    private int count;

    public void push(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        node.setNext(top);
        top = node;
        count++;
    }

    public T peek() {
        return top.getElement();
    }

    public boolean isEmpty() {
        return top == null;
    }

    public int size() {
        return count;
    }
}
"""
S2 = "import java.util.EmptyStackException;\n\n" + S1.replace("""    public T peek() {
        return top.getElement();
    }""", """    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T result = top.getElement();
        top = top.getNext();
        count--;
        return result;
    }

    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return top.getElement();
    }""")
ST1 = """public class UndoTester {
    public static void main(String[] args) {
        LinkedStack<String> history = new LinkedStack<>();
        history.push("draw circle");
        history.push("fill red");
        System.out.println(history.peek() + " " + history.size() + " " + history.isEmpty());
    }
}
"""
ST2 = """public class UndoTester {
    public static void main(String[] args) {
        LinkedStack<String> history = new LinkedStack<>();
        history.push("draw circle");
        history.push("fill red");
        history.push("add border");
        while (!history.isEmpty()) {
            System.out.println("undo " + history.pop());
        }
    }
}
"""
SM = """public class Matcher {
    public static boolean matches(String html) {
        LinkedStack<String> open = new LinkedStack<>();
        for (String tag : html.split(" ")) {
            if (tag.startsWith("</")) {
                if (open.isEmpty()) {
                    return false;
                }
                String name = tag.substring(2, tag.length() - 1);
                if (!open.pop().equals(name)) {
                    return false;
                }
            } else {
                open.push(tag.substring(1, tag.length() - 1));
            }
        }
        return open.isEmpty();
    }

    public static void main(String[] args) {
        System.out.println(matches("<p> <b> </b> </p>"));
        System.out.println(matches("<p> <b> </p> </b>"));
        System.out.println(matches("<div> <p> </p>"));
    }
}
"""

LESSON = workshop(
    "ws-linked-lists", "Workshop: linked lists and stacks",
    "Write a linked list with list operations and a linked stack, use the stack to match HTML tags, and add the operations that show off what a singly linked list is bad at: removing the last node and reversing.",
    ["Write a generic linked list class with add, get, remove and toString",
     "Write a linked stack with its top at the head",
     "Explain which operations are O(1) and which are O(n) on each"],
    guided("ws-u17-list", "A linked list from scratch", "Write `SimpleLinkedList<T>` yourself, one group of operations at a time. Create `LinearNode<T>` too.", [
        step("Adding and printing", "Create `LinearNode<T>` (an element, a `next`, `getElement`, `getNext`, `setNext`). In `SimpleLinkedList<T>`, keep a private `head` and `count`. Write `add(T)` (at the end, walking from the head), `size()` and `toString()` in the `head -> ... -> null` format.",
             {"LinearNode.java": LINEAR_NODE, "SimpleLinkedList.java": L1, "ListTester.java": LT1}, "ListTester",
             "head -> milk -> eggs -> rice -> null 3"),
        step("Getting by index", "Add `get(int index)`: throw `IndexOutOfBoundsException(\"Index \" + index + \", size \" + count)` for a bad index, otherwise walk `index` steps from the head.",
             {"LinearNode.java": LINEAR_NODE, "SimpleLinkedList.java": L2, "ListTester.java": LT2}, "ListTester",
             "0: milk\n1: eggs\n2: rice\nIndex 3, size 3"),
        step("Removing by index", "Add `remove(int index)`, which returns the removed element. Index 0 moves the head; any other index walks to the node **before** it and links around. Update `count`.",
             {"LinearNode.java": LINEAR_NODE, "SimpleLinkedList.java": L3, "ListTester.java": LT3}, "ListTester",
             "rice head -> milk -> eggs -> tea -> null\nmilk head -> eggs -> tea -> null\ntea head -> eggs -> null 1"),
    ]),
    guided("ws-u17-stack", "A linked stack at work", "Write a `LinkedStack<T>`, use it as an undo history, then use it to check that HTML tags are properly nested.", [
        step("Push and peek", "Create `LinearNode<T>` and `LinkedStack<T>` with a `top` node and a `count`. Write `push` (at the head), `peek`, `isEmpty` and `size`.",
             {"LinearNode.java": LINEAR_NODE, "LinkedStack.java": S1, "UndoTester.java": ST1}, "UndoTester",
             "fill red 2 false"),
        step("Pop, and undo", "Add `pop`. `pop` and `peek` throw `EmptyStackException` on an empty stack. Undo every action, most recent first.",
             {"LinearNode.java": LINEAR_NODE, "LinkedStack.java": S2, "UndoTester.java": ST2}, "UndoTester",
             "undo add border\nundo fill red\nundo draw circle"),
        step("Matching tags", "In `Matcher`, write `matches(String html)` for tags separated by spaces, like `<p> <b> </b> </p>`. Push each opening tag's name; at each closing tag, the stack must be non-empty and its popped name must be equal. At the end, nothing may be left open.",
             {"LinearNode.java": LINEAR_NODE, "LinkedStack.java": S2, "Matcher.java": SM}, "Matcher",
             "true\nfalse\nfalse",
             hint="`tag.substring(1, tag.length() - 1)` turns `<p>` into `p`; for `</p>`, start at 2."),
    ]),
    given(task("ws-u17-removelast", "Remove the last element",
         "Add `public T removeLast()` to `SimpleLinkedList` (already in the editor with `LinearNode`). It throws a `NoSuchElementException` (import it from `java.util`) on an empty list. With only a head reference, you have to walk to the **second-to-last** node to cut off the last one, so it's O(n): this is why a linked stack doesn't keep its top at the end. A one-node list is a special case. `RemoveLastTester` adds 1, 2, 3, then prints two `removeLast()` results and the list.",
         {"SimpleLinkedList.java": "import java.util.NoSuchElementException;\n\n" + extend("""    public T removeLast() {
        if (head == null) {
            throw new NoSuchElementException();
        }
        T result;
        if (head.getNext() == null) {
            result = head.getElement();
            head = null;
        } else {
            LinearNode<T> current = head;
            while (current.getNext().getNext() != null) {
                current = current.getNext();
            }
            result = current.getNext().getElement();
            current.setNext(null);
        }
        count--;
        return result;
    }
"""), "RemoveLastTester.java": """public class RemoveLastTester {
    public static void main(String[] args) {
        SimpleLinkedList<Integer> list = new SimpleLinkedList<>();
        list.add(1);
        list.add(2);
        list.add(3);
        System.out.println(list.removeLast() + " " + list.removeLast() + " " + list);
    }
}
"""}, "RemoveLastTester", "3 2 head -> 1 -> null",
         tests={"CheckRemoveLast.java": """import java.util.NoSuchElementException;

public class CheckRemoveLast {
    public static void main(String[] args) {
        SimpleLinkedList<String> list = new SimpleLinkedList<>();
        list.add("only");
        System.out.println(list.removeLast() + " " + list + " " + list.size());
        try {
            list.removeLast();
        } catch (NoSuchElementException e) {
            System.out.println("empty");
        }
    }
}
"""}, tests_run="CheckRemoveLast", tests_output="only head -> null 0\nempty",
         hints=["Loop `while (current.getNext().getNext() != null)` stops on the second-to-last node."]), LIST_FILES),
    given(task("ws-u17-reverse", "Reverse the list",
         "Add `public void reverse()` to `SimpleLinkedList` (already in the editor with `LinearNode`), which reverses the list in place by turning every `next` reference around, then sets `head` to the old last node. No new nodes. `ReverseTester` adds `a` to `e`, reverses and prints the list, then prints `get(0)`.",
         {"SimpleLinkedList.java": extend("""    public void reverse() {
        LinearNode<T> previous = null;
        LinearNode<T> current = head;
        while (current != null) {
            LinearNode<T> next = current.getNext();
            current.setNext(previous);
            previous = current;
            current = next;
        }
        head = previous;
    }
"""), "ReverseTester.java": """public class ReverseTester {
    public static void main(String[] args) {
        SimpleLinkedList<String> list = new SimpleLinkedList<>();
        for (String s : new String[] {"a", "b", "c", "d", "e"}) {
            list.add(s);
        }
        list.reverse();
        System.out.println(list);
        System.out.println(list.get(0));
    }
}
"""}, "ReverseTester", "head -> e -> d -> c -> b -> a -> null\ne",
         tests={"CheckReverse.java": """public class CheckReverse {
    public static void main(String[] args) {
        SimpleLinkedList<Integer> empty = new SimpleLinkedList<>();
        empty.reverse();
        SimpleLinkedList<Integer> two = new SimpleLinkedList<>();
        two.add(1);
        two.add(2);
        two.reverse();
        two.add(3);
        System.out.println(empty + " | " + two + " " + two.size());
    }
}
"""}, tests_run="CheckReverse", tests_output="head -> null | head -> 2 -> 1 -> 3 -> null 3",
         hints=["Save `next` before you change `current`'s link, or you lose the rest of the list."]), LIST_FILES),
    [ALGS4_13, OPENDSA_STACK, ARRAYLIST_API, EMPTYSTACK_API],
)
