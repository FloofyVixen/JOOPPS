"""Write-it-yourself tasks for unit 19, ArrayQueues vs Linked Queues. Compiled and run by build.py."""
from tasks_classes import task
from tasks_stacks import given
from ds_code import QUEUE_ADT, LINEAR_NODE, CQUEUE_FILES, CIRCULAR_QUEUE

QG = {"QueueADT.java": QUEUE_ADT}
QNG = {"QueueADT.java": QUEUE_ADT, "LinearNode.java": LINEAR_NODE}

ARRAY = [
    given(task("w-aq-shift", "A shifting array queue",
         "Write `ShiftQueue<T>`, implementing `QueueADT<T>` (already in the editor) with an `Object[]` of 4 slots that doubles when full and an `int rear`. The front is always index 0, so `dequeue` shifts the remaining values left and clears the old last slot. `dequeue` and `getFront` throw `java.util.NoSuchElementException(\"queue is empty\")`. `ShiftTester` enqueues 1 to 5, dequeues twice, and prints the two values, `getFront()` and `size()` on one line.",
         {"ShiftQueue.java": """import java.util.NoSuchElementException;

public class ShiftQueue<T> implements QueueADT<T> {
    private Object[] queue = new Object[4];
    private int rear = 0;

    @Override
    public void enqueue(T element) {
        if (rear == queue.length) {
            Object[] bigger = new Object[queue.length * 2];
            for (int i = 0; i < rear; i++) {
                bigger[i] = queue[i];
            }
            queue = bigger;
        }
        queue[rear] = element;
        rear++;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        T result = (T) queue[0];
        for (int i = 0; i < rear - 1; i++) {
            queue[i] = queue[i + 1];
        }
        rear--;
        queue[rear] = null;
        return result;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T getFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        return (T) queue[0];
    }

    @Override
    public boolean isEmpty() {
        return rear == 0;
    }

    @Override
    public int size() {
        return rear;
    }
}
""", "ShiftTester.java": """public class ShiftTester {
    public static void main(String[] args) {
        QueueADT<Integer> q = new ShiftQueue<>();
        for (int i = 1; i <= 5; i++) {
            q.enqueue(i);
        }
        int a = q.dequeue();
        int b = q.dequeue();
        System.out.println(a + " " + b + " " + q.getFront() + " " + q.size());
    }
}
"""}, "ShiftTester", "1 2 3 3",
         tests={"CheckShift.java": """import java.util.NoSuchElementException;

public class CheckShift {
    public static void main(String[] args) {
        QueueADT<String> q = new ShiftQueue<>();
        q.enqueue("a");
        System.out.println(q.dequeue() + " " + q.isEmpty());
        try {
            q.getFront();
        } catch (NoSuchElementException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""}, tests_run="CheckShift", tests_output="a true\nqueue is empty"), QG),

    task("w-aq-ring", "A fixed-size ring buffer",
         "Write `RingBuffer`, a circular queue of `int`s with a fixed capacity (from the constructor) that **never grows**: `front`, `rear` and `count` as in `CircularArrayQueue`. `isFull()` is `count == capacity`. `enqueue` on a full buffer throws `IllegalStateException(\"full\")`; `dequeue` on an empty one throws `IllegalStateException(\"empty\")`. `RingTester` makes a buffer of 3, enqueues 1, 2, 3, prints `isFull()`, dequeues once, enqueues 4 (which wraps to index 0), then dequeues everything onto one line.",
         {"RingBuffer.java": """public class RingBuffer {
    private int[] data;
    private int front;
    private int rear;
    private int count;

    public RingBuffer(int capacity) {
        data = new int[capacity];
    }

    public boolean isFull() {
        return count == data.length;
    }

    public boolean isEmpty() {
        return count == 0;
    }

    public void enqueue(int value) {
        if (isFull()) {
            throw new IllegalStateException("full");
        }
        data[rear] = value;
        rear = (rear + 1) % data.length;
        count++;
    }

    public int dequeue() {
        if (isEmpty()) {
            throw new IllegalStateException("empty");
        }
        int value = data[front];
        front = (front + 1) % data.length;
        count--;
        return value;
    }
}
""", "RingTester.java": """public class RingTester {
    public static void main(String[] args) {
        RingBuffer r = new RingBuffer(3);
        r.enqueue(1);
        r.enqueue(2);
        r.enqueue(3);
        System.out.println(r.isFull());
        r.dequeue();
        r.enqueue(4);
        String out = "";
        while (!r.isEmpty()) {
            out += r.dequeue() + " ";
        }
        System.out.println(out.trim());
    }
}
"""}, "RingTester", "true\n2 3 4",
         tests={"CheckRing.java": """public class CheckRing {
    public static void main(String[] args) {
        RingBuffer r = new RingBuffer(2);
        String out = "";
        for (int i = 0; i < 7; i++) {
            r.enqueue(i);
            out += r.dequeue();
        }
        System.out.println(out);
        r.enqueue(8);
        r.enqueue(9);
        try {
            r.enqueue(10);
        } catch (IllegalStateException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""}, tests_run="CheckRing", tests_output="0123456\nfull",
         checks=[{"pattern": r"%\s*data\.length", "message": "Wrap the indexes with `% data.length`."}]),

    given(task("w-aq-getat", "Look inside a circular queue",
         "Add `public T getAt(int i)` to `CircularArrayQueue` (already in the editor): the value `i` places behind the front (`getAt(0)` is the front), without changing anything. It's O(1): the slot is `(front + i) % queue.length`. Throw `IndexOutOfBoundsException(\"position \" + i)` unless `0 <= i < count`. `GetAtTester` enqueues `a` to `d`, dequeues twice, enqueues `e` and `f` (which wrap), and prints `getAt(0)` to `getAt(3)` on one line.",
         {"CircularArrayQueue.java": CIRCULAR_QUEUE.replace("""    @Override
    public boolean isEmpty() {""", """    @SuppressWarnings("unchecked")
    public T getAt(int i) {
        if (i < 0 || i >= count) {
            throw new IndexOutOfBoundsException("position " + i);
        }
        return (T) queue[(front + i) % queue.length];
    }

    @Override
    public boolean isEmpty() {"""), "GetAtTester.java": """public class GetAtTester {
    public static void main(String[] args) {
        CircularArrayQueue<String> q = new CircularArrayQueue<>();
        for (String s : new String[] {"a", "b", "c", "d"}) {
            q.enqueue(s);
        }
        q.dequeue();
        q.dequeue();
        q.enqueue("e");
        q.enqueue("f");
        System.out.println(q.getAt(0) + q.getAt(1) + q.getAt(2) + q.getAt(3));
    }
}
"""}, "GetAtTester", "cdef",
         tests={"CheckGetAt.java": """public class CheckGetAt {
    public static void main(String[] args) {
        CircularArrayQueue<Integer> q = new CircularArrayQueue<>();
        q.enqueue(1);
        try {
            q.getAt(1);
        } catch (IndexOutOfBoundsException e) {
            System.out.println(e.getMessage());
        }
        System.out.println(q.getAt(0));
    }
}
"""}, tests_run="CheckGetAt", tests_output="position 1\n1"), CQUEUE_FILES),
]

LINKED = [
    given(task("w-lq-scratch", "LinkedQueue from scratch",
         "Write `LinkedQueue<T>`, implementing `QueueADT<T>` with `LinearNode<T>` (both already in the editor): private `front`, `rear` and `count`. Enqueue after `rear`, dequeue from `front`, and handle the empty cases (the first enqueue sets both; the last dequeue clears `rear`). Throw `java.util.NoSuchElementException(\"queue is empty\")` from `dequeue` and `getFront` when empty. `LQTester` enqueues 1 to 3, dequeues them all onto one line, then enqueues 4 and prints `getFront()` and `size()`.",
         {"LinkedQueue.java": """import java.util.NoSuchElementException;

public class LinkedQueue<T> implements QueueADT<T> {
    private LinearNode<T> front;
    private LinearNode<T> rear;
    private int count;

    @Override
    public void enqueue(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        if (isEmpty()) {
            front = node;
        } else {
            rear.setNext(node);
        }
        rear = node;
        count++;
    }

    @Override
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        T result = front.getElement();
        front = front.getNext();
        count--;
        if (isEmpty()) {
            rear = null;
        }
        return result;
    }

    @Override
    public T getFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        return front.getElement();
    }

    @Override
    public boolean isEmpty() {
        return count == 0;
    }

    @Override
    public int size() {
        return count;
    }
}
""", "LQTester.java": """public class LQTester {
    public static void main(String[] args) {
        QueueADT<Integer> q = new LinkedQueue<>();
        for (int i = 1; i <= 3; i++) {
            q.enqueue(i);
        }
        String out = "";
        while (!q.isEmpty()) {
            out += q.dequeue() + " ";
        }
        System.out.println(out.trim());
        q.enqueue(4);
        System.out.println(q.getFront() + " " + q.size());
    }
}
"""}, "LQTester", "1 2 3\n4 1",
         tests={"CheckLQ.java": """import java.util.NoSuchElementException;

public class CheckLQ {
    public static void main(String[] args) {
        QueueADT<String> q = new LinkedQueue<>();
        try {
            q.dequeue();
        } catch (NoSuchElementException e) {
            System.out.println(e.getMessage());
        }
        q.enqueue("a");
        q.dequeue();
        q.enqueue("b");
        q.enqueue("c");
        System.out.println(q.dequeue() + q.dequeue() + " " + q.isEmpty());
    }
}
"""}, tests_run="CheckLQ", tests_output="queue is empty\nbc true"), QNG),

    given(task("w-lq-norear", "A linked queue without a rear",
         "Write `FrontOnlyQueue<T>`, implementing `QueueADT<T>` (already in the editor with `LinearNode<T>`) with **only** a `front` reference and a `count`. Without `rear`, `enqueue` has to walk to the last node: O(n). `dequeue` and `getFront` throw `java.util.NoSuchElementException` when empty. `FrontOnlyTester` enqueues `a`, `b`, `c`, dequeues once, enqueues `d`, and dequeues everything onto one line.",
         {"FrontOnlyQueue.java": """import java.util.NoSuchElementException;

public class FrontOnlyQueue<T> implements QueueADT<T> {
    private LinearNode<T> front;
    private int count;

    @Override
    public void enqueue(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        if (front == null) {
            front = node;
        } else {
            LinearNode<T> current = front;
            while (current.getNext() != null) {
                current = current.getNext();
            }
            current.setNext(node);
        }
        count++;
    }

    @Override
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException();
        }
        T result = front.getElement();
        front = front.getNext();
        count--;
        return result;
    }

    @Override
    public T getFront() {
        if (isEmpty()) {
            throw new NoSuchElementException();
        }
        return front.getElement();
    }

    @Override
    public boolean isEmpty() {
        return front == null;
    }

    @Override
    public int size() {
        return count;
    }
}
""", "FrontOnlyTester.java": """public class FrontOnlyTester {
    public static void main(String[] args) {
        QueueADT<String> q = new FrontOnlyQueue<>();
        q.enqueue("a");
        q.enqueue("b");
        q.enqueue("c");
        q.dequeue();
        q.enqueue("d");
        String out = "";
        while (!q.isEmpty()) {
            out += q.dequeue();
        }
        System.out.println(out);
    }
}
"""}, "FrontOnlyTester", "bcd",
         tests={"CheckFrontOnly.java": """public class CheckFrontOnly {
    public static void main(String[] args) {
        QueueADT<Integer> q = new FrontOnlyQueue<>();
        for (int i = 0; i < 50; i++) {
            q.enqueue(i);
        }
        System.out.println(q.getFront() + " " + q.size());
    }
}
"""}, tests_run="CheckFrontOnly", tests_output="0 50",
         checks=[{"pattern": r"^(?![\s\S]*\brear\b)", "file": "FrontOnlyQueue.java", "message": "There's no `rear` reference: `enqueue` walks from `front`."}]), QNG),
]

TASKS = {"aqueue": ARRAY, "lqueue": LINKED}
