"""Write-it-yourself tasks for unit 17, Linked Lists as ArrayLists and Stacks. Compiled and run by build.py."""
from tasks_classes import task
from tasks_stacks import given
from ds_code import LIST_FILES, SIMPLE_LIST, LINEAR_NODE, STACK_ADT

ANCHOR = "    public int size() {"


def extend(method):
    """SimpleLinkedList with one more method, inserted before size()."""
    return SIMPLE_LIST.replace(ANCHOR, method + "\n" + ANCHOR)


LIST_NOTE = "`LinearNode` and `SimpleLinkedList` (from the lesson) are already in the editor; add the method to `SimpleLinkedList`."

LIST = [
    given(task("w-ll-indexof", "indexOf",
         "Add `public int indexOf(T target)` to `SimpleLinkedList`: the index of the first element that `equals` the target, or -1. Traverse with `getNext()`, counting as you go. `IndexTester` adds `x`, `y`, `z`, `y` and prints `indexOf(\"y\")`, `indexOf(\"z\")` and `indexOf(\"w\")` on one line. " + LIST_NOTE,
         {"SimpleLinkedList.java": extend("""    public int indexOf(T target) {
        int index = 0;
        LinearNode<T> current = head;
        while (current != null) {
            if (current.getElement().equals(target)) {
                return index;
            }
            index++;
            current = current.getNext();
        }
        return -1;
    }
"""), "IndexTester.java": """public class IndexTester {
    public static void main(String[] args) {
        SimpleLinkedList<String> list = new SimpleLinkedList<>();
        list.add("x");
        list.add("y");
        list.add("z");
        list.add("y");
        System.out.println(list.indexOf("y") + " " + list.indexOf("z") + " " + list.indexOf("w"));
    }
}
"""}, "IndexTester", "1 2 -1",
         tests={"CheckIndexOf.java": """public class CheckIndexOf {
    public static void main(String[] args) {
        SimpleLinkedList<Integer> list = new SimpleLinkedList<>();
        System.out.println(list.indexOf(3));
        list.add(1000);
        list.add(3);
        System.out.println(list.indexOf(1000) + " " + list.indexOf(3));
    }
}
"""}, tests_run="CheckIndexOf", tests_output="-1\n0 1",
         hints=["Compare with `equals`, not `==`: two `Integer` objects holding 1000 aren't necessarily the same object."]), LIST_FILES),

    given(task("w-ll-set", "set",
         "Add `public T set(int index, T element)` to `SimpleLinkedList`, which replaces the element at `index` and returns the old one, like `ArrayList.set`. Use the private helpers `checkIndex` and `nodeAt`. You'll also need a `setElement` method in `LinearNode`: add it. `SetTester` adds `a`, `b`, `c`, sets index 1 to `B`, and prints the returned value and the list. " + LIST_NOTE,
         {"LinearNode.java": LINEAR_NODE.replace("""    public LinearNode<T> getNext() {""", """    public void setElement(T element) {
        this.element = element;
    }

    public LinearNode<T> getNext() {"""), "SimpleLinkedList.java": extend("""    public T set(int index, T element) {
        checkIndex(index);
        LinearNode<T> node = nodeAt(index);
        T old = node.getElement();
        node.setElement(element);
        return old;
    }
"""), "SetTester.java": """public class SetTester {
    public static void main(String[] args) {
        SimpleLinkedList<String> list = new SimpleLinkedList<>();
        list.add("a");
        list.add("b");
        list.add("c");
        System.out.println(list.set(1, "B"));
        System.out.println(list);
    }
}
"""}, "SetTester", "b\nhead -> a -> B -> c -> null",
         tests={"CheckSet.java": """public class CheckSet {
    public static void main(String[] args) {
        SimpleLinkedList<Integer> list = new SimpleLinkedList<>();
        list.add(1);
        System.out.println(list.set(0, 9) + " " + list + " " + list.size());
        try {
            list.set(1, 5);
        } catch (IndexOutOfBoundsException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""}, tests_run="CheckSet", tests_output="1 head -> 9 -> null 1\nIndex 1, size 1"), LIST_FILES),

    given(task("w-ll-removeelement", "Remove by value",
         "Add `public boolean removeElement(T target)` to `SimpleLinkedList`: remove the first element that `equals` the target and return `true`, or return `false` if there is none. Handle the head separately, and remember to update `count`. `RemoveTester` adds 1, 2, 3, 2, removes 2 twice and 7 once (printing each result on one line), then prints the list and its size. " + LIST_NOTE,
         {"SimpleLinkedList.java": extend("""    public boolean removeElement(T target) {
        if (head == null) {
            return false;
        }
        if (head.getElement().equals(target)) {
            head = head.getNext();
            count--;
            return true;
        }
        LinearNode<T> current = head;
        while (current.getNext() != null) {
            if (current.getNext().getElement().equals(target)) {
                current.setNext(current.getNext().getNext());
                count--;
                return true;
            }
            current = current.getNext();
        }
        return false;
    }
"""), "RemoveTester.java": """public class RemoveTester {
    public static void main(String[] args) {
        SimpleLinkedList<Integer> list = new SimpleLinkedList<>();
        list.add(1);
        list.add(2);
        list.add(3);
        list.add(2);
        System.out.println(list.removeElement(2) + " " + list.removeElement(2) + " " + list.removeElement(7));
        System.out.println(list + " " + list.size());
    }
}
"""}, "RemoveTester", "true true false\nhead -> 1 -> 3 -> null 2",
         tests={"CheckRemoveElement.java": """public class CheckRemoveElement {
    public static void main(String[] args) {
        SimpleLinkedList<String> list = new SimpleLinkedList<>();
        System.out.println(list.removeElement("a"));
        list.add("a");
        System.out.println(list.removeElement("a") + " " + list + " " + list.size());
    }
}
"""}, tests_run="CheckRemoveElement", tests_output="false\ntrue head -> null 0"), LIST_FILES),
]

LINKED_STACK_SOLUTION = """import java.util.EmptyStackException;

public class LinkedStack<T> implements StackADT<T> {
    private LinearNode<T> top;
    private int count;

    @Override
    public void push(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        node.setNext(top);
        top = node;
        count++;
    }

    @Override
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T result = top.getElement();
        top = top.getNext();
        count--;
        return result;
    }

    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return top.getElement();
    }

    @Override
    public boolean isEmpty() {
        return top == null;
    }

    @Override
    public int size() {
        return count;
    }
}
"""
STACK_GIVEN = {"StackADT.java": STACK_ADT, "LinearNode.java": LINEAR_NODE}

STACKS = [
    given(task("w-lstack-scratch", "LinkedStack from scratch",
         "Write `LinkedStack<T>`, which implements `StackADT<T>` with `LinearNode<T>`s (both already in the editor): a private `top` node and a `count`. Push and pop at the head; `pop` and `peek` throw `EmptyStackException` when empty. `LinkedTester` pushes 1 to 5, then pops three times and prints the popped values and the size on one line.",
         {"LinkedStack.java": LINKED_STACK_SOLUTION, "LinkedTester.java": """public class LinkedTester {
    public static void main(String[] args) {
        StackADT<Integer> s = new LinkedStack<>();
        for (int i = 1; i <= 5; i++) {
            s.push(i);
        }
        System.out.println(s.pop() + " " + s.pop() + " " + s.pop() + " " + s.size());
    }
}
"""}, "LinkedTester", "5 4 3 2",
         tests={"CheckLinked.java": """import java.util.EmptyStackException;

public class CheckLinked {
    public static void main(String[] args) {
        StackADT<String> s = new LinkedStack<>();
        System.out.println(s.isEmpty() + " " + s.size());
        s.push("only");
        System.out.println(s.peek() + " " + s.pop() + " " + s.isEmpty());
        try {
            s.peek();
        } catch (EmptyStackException e) {
            System.out.println("empty");
        }
    }
}
"""}, tests_run="CheckLinked", tests_output="true 0\nonly only true\nempty",
         checks=[{"pattern": r"LinearNode<T>", "message": "Store the stack in `LinearNode<T>` nodes."}]), STACK_GIVEN),

    given(task("w-lstack-nocount", "A stack without a count",
         "Write `NoCountStack<T>`, a linked stack (implementing `StackADT<T>`, already in the editor with `LinearNode<T>`) with **only** a `top` field: no `count`. Its `size()` has to traverse the nodes to count them, which makes it O(n) instead of O(1). `NoCountTester` pushes `a`, `b`, `c`, prints `size()`, pops once and prints `size()` again.",
         {"NoCountStack.java": """import java.util.EmptyStackException;

public class NoCountStack<T> implements StackADT<T> {
    private LinearNode<T> top;

    @Override
    public void push(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        node.setNext(top);
        top = node;
    }

    @Override
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T result = top.getElement();
        top = top.getNext();
        return result;
    }

    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return top.getElement();
    }

    @Override
    public boolean isEmpty() {
        return top == null;
    }

    @Override
    public int size() {
        int count = 0;
        for (LinearNode<T> current = top; current != null; current = current.getNext()) {
            count++;
        }
        return count;
    }
}
""", "NoCountTester.java": """public class NoCountTester {
    public static void main(String[] args) {
        StackADT<String> s = new NoCountStack<>();
        s.push("a");
        s.push("b");
        s.push("c");
        System.out.println(s.size());
        s.pop();
        System.out.println(s.size());
    }
}
"""}, "NoCountTester", "3\n2",
         tests={"CheckNoCount.java": """public class CheckNoCount {
    public static void main(String[] args) {
        StackADT<Integer> s = new NoCountStack<>();
        System.out.println(s.size() + " " + s.isEmpty());
        for (int i = 0; i < 100; i++) {
            s.push(i);
        }
        System.out.println(s.size() + " " + s.peek());
    }
}
"""}, tests_run="CheckNoCount", tests_output="0 true\n100 99",
         checks=[{"pattern": r"^(?![\s\S]*private\s+int\b)", "file": "NoCountStack.java",
                  "message": "There's no `int` field keeping a count: `size()` counts the nodes each time."}]), STACK_GIVEN),
]

COMPARE = [
    given(task("w-cmp-arraylist-stack", "A stack on an ArrayList",
         "Write `ArrayListStack<T>`, implementing `StackADT<T>` (already in the editor) with a private `java.util.ArrayList<T>`. Put the top at the **end** of the list, so `push` is `add(element)` and `pop` is `remove(size() - 1)`, both O(1). `pop` and `peek` throw `EmptyStackException` when empty. `ALStackTester` pushes `x`, `y`, `z`, then prints `pop()`, `peek()` and `size()` on one line.",
         {"ArrayListStack.java": """import java.util.ArrayList;
import java.util.EmptyStackException;

public class ArrayListStack<T> implements StackADT<T> {
    private ArrayList<T> items = new ArrayList<>();

    @Override
    public void push(T element) {
        items.add(element);
    }

    @Override
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return items.remove(items.size() - 1);
    }

    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return items.get(items.size() - 1);
    }

    @Override
    public boolean isEmpty() {
        return items.isEmpty();
    }

    @Override
    public int size() {
        return items.size();
    }
}
""", "ALStackTester.java": """public class ALStackTester {
    public static void main(String[] args) {
        StackADT<String> s = new ArrayListStack<>();
        s.push("x");
        s.push("y");
        s.push("z");
        System.out.println(s.pop() + " " + s.peek() + " " + s.size());
    }
}
"""}, "ALStackTester", "z y 2",
         tests={"CheckALStack.java": """import java.util.EmptyStackException;

public class CheckALStack {
    public static void main(String[] args) {
        StackADT<Integer> s = new ArrayListStack<>();
        try {
            s.pop();
        } catch (EmptyStackException e) {
            System.out.println("empty");
        }
        s.push(4);
        s.push(5);
        System.out.println(s.pop() + s.pop() + " " + s.isEmpty());
    }
}
"""}, tests_run="CheckALStack", tests_output="empty\n9 true",
         checks=[{"pattern": r"size\(\)\s*-\s*1", "message": "The top is the last index, `size() - 1`."}]), {"StackADT.java": STACK_ADT}),

    given(task("w-cmp-linkedlist-stack", "A stack on Java's LinkedList",
         "Write `LinkedListStack<T>`, implementing `StackADT<T>` (already in the editor) with a private `java.util.LinkedList<T>`. This time the top is the **front**: `push` is `addFirst`, `pop` is `removeFirst`, and `peek` is `getFirst`, all O(1) for a linked list. Check `isEmpty()` first and throw `EmptyStackException`, since `LinkedList` would throw a different exception. `LLStackTester` pushes 1, 2, 3, then prints `pop()`, `peek()` and `size()` on one line.",
         {"LinkedListStack.java": """import java.util.EmptyStackException;
import java.util.LinkedList;

public class LinkedListStack<T> implements StackADT<T> {
    private LinkedList<T> items = new LinkedList<>();

    @Override
    public void push(T element) {
        items.addFirst(element);
    }

    @Override
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return items.removeFirst();
    }

    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return items.getFirst();
    }

    @Override
    public boolean isEmpty() {
        return items.isEmpty();
    }

    @Override
    public int size() {
        return items.size();
    }
}
""", "LLStackTester.java": """public class LLStackTester {
    public static void main(String[] args) {
        StackADT<Integer> s = new LinkedListStack<>();
        s.push(1);
        s.push(2);
        s.push(3);
        System.out.println(s.pop() + " " + s.peek() + " " + s.size());
    }
}
"""}, "LLStackTester", "3 2 2",
         tests={"CheckLLStack.java": """import java.util.EmptyStackException;

public class CheckLLStack {
    public static void main(String[] args) {
        StackADT<String> s = new LinkedListStack<>();
        try {
            s.peek();
        } catch (EmptyStackException e) {
            System.out.println("empty");
        }
        s.push("a");
        s.push("b");
        System.out.println(s.pop() + s.pop() + " " + s.size());
    }
}
"""}, tests_run="CheckLLStack", tests_output="empty\nba 0",
         checks=[{"pattern": r"addFirst", "message": "Push at the front with `addFirst`."}]), {"StackADT.java": STACK_ADT}),
]

TASKS = {"llist-class": LIST, "lstack": STACKS, "lcompare": COMPARE}
