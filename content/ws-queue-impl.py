from sources import ALGS4_13, OPENDSA_QUEUE, NOSUCH_API, DEQUE_API
from wshelp import step, guided, workshop, task
from tasks_stacks import given
from ds_code import QUEUE_ADT, LQUEUE_FILES, LINKED_QUEUE

C1 = """public class CircularQueue<T> implements QueueADT<T> {
    private Object[] queue = new Object[4];
    private int front = 0;
    private int rear = 0;
    private int count = 0;

    @Override
    public void enqueue(T element) {
        queue[rear] = element;
        rear = (rear + 1) % queue.length;
        count++;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T getFront() {
        return (T) queue[front];
    }

    @Override
    public T dequeue() {
        return null;
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
"""
C2 = "import java.util.NoSuchElementException;\n\n" + C1.replace("""    @SuppressWarnings("unchecked")
    @Override
    public T getFront() {
        return (T) queue[front];
    }

    @Override
    public T dequeue() {
        return null;
    }
""", """    @SuppressWarnings("unchecked")
    @Override
    public T getFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        return (T) queue[front];
    }

    @SuppressWarnings("unchecked")
    @Override
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        T result = (T) queue[front];
        queue[front] = null;
        front = (front + 1) % queue.length;
        count--;
        return result;
    }
""").replace("""    @Override
    public int size() {
        return count;
    }
""", """    @Override
    public int size() {
        return count;
    }

    public String arrayString() {
        String result = "[";
        for (int i = 0; i < queue.length; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += (queue[i] == null) ? "_" : queue[i];
        }
        return result + "] front=" + front + " rear=" + rear;
    }
""")
C3 = C2.replace("""    public void enqueue(T element) {
        queue[rear] = element;""", """    public void enqueue(T element) {
        if (count == queue.length) {
            expandCapacity();
        }
        queue[rear] = element;""").replace("""    public String arrayString() {""", """    private void expandCapacity() {
        Object[] bigger = new Object[queue.length * 2];
        for (int i = 0; i < count; i++) {
            bigger[i] = queue[(front + i) % queue.length];
        }
        front = 0;
        rear = count;
        queue = bigger;
    }

    public String arrayString() {""")
CT1 = """public class CircularTester {
    public static void main(String[] args) {
        QueueADT<String> q = new CircularQueue<>();
        System.out.println(q.isEmpty());
        q.enqueue("a");
        q.enqueue("b");
        System.out.println(q.getFront() + " " + q.size());
    }
}
"""
CT2 = """public class CircularTester {
    public static void main(String[] args) {
        CircularQueue<String> q = new CircularQueue<>();
        for (String s : new String[] {"a", "b", "c", "d"}) {
            q.enqueue(s);
        }
        System.out.println(q.dequeue() + q.dequeue() + " " + q.arrayString());
        q.enqueue("e");
        System.out.println(q.getFront() + " " + q.arrayString());
    }
}
"""
CT3 = """public class CircularTester {
    public static void main(String[] args) {
        CircularQueue<String> q = new CircularQueue<>();
        for (String s : new String[] {"a", "b", "c", "d"}) {
            q.enqueue(s);
        }
        q.dequeue();
        q.enqueue("e");
        System.out.println(q.arrayString());
        q.enqueue("f");
        System.out.println(q.arrayString());
        String out = "";
        while (!q.isEmpty()) {
            out += q.dequeue();
        }
        System.out.println(out);
    }
}
"""

TS1 = """import java.util.ArrayDeque;
import java.util.Deque;

public class TwoStackQueue<T> implements QueueADT<T> {
    private Deque<T> in = new ArrayDeque<>();
    private Deque<T> out = new ArrayDeque<>();

    @Override
    public void enqueue(T element) {
        in.push(element);
    }

    @Override
    public T dequeue() {
        if (out.isEmpty()) {
            while (!in.isEmpty()) {
                out.push(in.pop());
            }
        }
        return out.pop();
    }

    @Override
    public T getFront() {
        return null;
    }

    @Override
    public boolean isEmpty() {
        return false;
    }

    @Override
    public int size() {
        return 0;
    }
}
"""
TS2 = "import java.util.NoSuchElementException;\n" + TS1.replace("""    @Override
    public T dequeue() {
        if (out.isEmpty()) {
            while (!in.isEmpty()) {
                out.push(in.pop());
            }
        }
        return out.pop();
    }

    @Override
    public T getFront() {
        return null;
    }

    @Override
    public boolean isEmpty() {
        return false;
    }

    @Override
    public int size() {
        return 0;
    }""", """    private void refill() {
        if (out.isEmpty()) {
            while (!in.isEmpty()) {
                out.push(in.pop());
            }
        }
    }

    @Override
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        refill();
        return out.pop();
    }

    @Override
    public T getFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        refill();
        return out.peek();
    }

    @Override
    public boolean isEmpty() {
        return in.isEmpty() && out.isEmpty();
    }

    @Override
    public int size() {
        return in.size() + out.size();
    }""")
TS3 = TS2.replace("""    private Deque<T> out = new ArrayDeque<>();
""", """    private Deque<T> out = new ArrayDeque<>();
    private int moves = 0;

    public int getMoves() {
        return moves;
    }
""").replace("""                out.push(in.pop());""", """                out.push(in.pop());
                moves++;""")
TT1 = """public class TwoStackTester {
    public static void main(String[] args) {
        QueueADT<Integer> q = new TwoStackQueue<>();
        q.enqueue(1);
        q.enqueue(2);
        q.enqueue(3);
        System.out.println(q.dequeue());
        q.enqueue(4);
        System.out.println(q.dequeue() + " " + q.dequeue() + " " + q.dequeue());
    }
}
"""
TT2 = """import java.util.NoSuchElementException;

public class TwoStackTester {
    public static void main(String[] args) {
        QueueADT<Integer> q = new TwoStackQueue<>();
        q.enqueue(1);
        q.enqueue(2);
        System.out.println(q.getFront() + " " + q.size() + " " + q.isEmpty());
        q.dequeue();
        q.dequeue();
        try {
            q.dequeue();
        } catch (NoSuchElementException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""
TT3 = """public class TwoStackTester {
    public static void main(String[] args) {
        TwoStackQueue<Integer> q = new TwoStackQueue<>();
        for (int round = 0; round < 1000; round++) {
            q.enqueue(round);
            q.enqueue(round);
            q.dequeue();
        }
        while (!q.isEmpty()) {
            q.dequeue();
        }
        System.out.println(q.getMoves() + " moves for 2000 values");
    }
}
"""

LESSON = workshop(
    "ws-queue-impl", "Workshop: queue implementations",
    "Write a circular array queue from scratch, build a queue out of two stacks, and add operations that show how the front and rear of each implementation work.",
    ["Wrap `front` and `rear` around an array with `%`, and unroll it when growing",
     "Keep a linked queue's `front` and `rear` correct, including the empty cases",
     "Measure that a queue made from two stacks does O(1) work per operation on average"],
    guided("ws-u19-circular", "A circular array queue", "Write `CircularQueue<T>` one piece at a time. Create `QueueADT.java` too.", [
        step("Enqueue around the circle", "Create `QueueADT<T>` and `CircularQueue<T>` with an `Object[]` of 4, `front`, `rear` and `count`. Write `enqueue` (wrap `rear` with `%`), `getFront`, `isEmpty` and `size`. For now `dequeue` can `return null;`.",
             {"QueueADT.java": QUEUE_ADT, "CircularQueue.java": C1, "CircularTester.java": CT1}, "CircularTester", "true\na 2"),
        step("Dequeue around the circle", "Write `dequeue`: take `queue[front]`, clear the slot, wrap `front` forward, and shrink `count`. `dequeue` and `getFront` throw `NoSuchElementException(\"queue is empty\")` when empty. Add `arrayString()` (each slot, `_` for empty, then ` front=... rear=...`) to see the wrap.",
             {"QueueADT.java": QUEUE_ADT, "CircularQueue.java": C2, "CircularTester.java": CT2}, "CircularTester",
             "ab [_, _, c, d] front=2 rear=0\nc [e, _, c, d] front=2 rear=1"),
        step("Growing in order", "Add `expandCapacity()`, called by `enqueue` when `count == queue.length`: copy the values in queue order, from `front` around, into slots 0, 1, 2, … of a double-size array, then set `front` to 0 and `rear` to `count`.",
             {"QueueADT.java": QUEUE_ADT, "CircularQueue.java": C3, "CircularTester.java": CT3}, "CircularTester",
             "[e, b, c, d] front=1 rear=1\n[b, c, d, e, f, _, _, _] front=0 rear=5\nbcdef",
             hint="The value `i` places behind the front is at `(front + i) % queue.length`."),
    ]),
    guided("ws-u19-twostacks", "A queue made of two stacks", "Two stacks can make a queue: push new values onto `in`; when you need the front, and `out` is empty, pop everything from `in` onto `out`, which reverses it into queue order.", [
        step("Enqueue and dequeue", "Create `QueueADT<T>` and `TwoStackQueue<T>` with two `Deque<T>` stacks, `in` and `out`. `enqueue` pushes onto `in`. `dequeue` refills `out` from `in` if `out` is empty, then pops `out`. Stub the other methods for now.",
             {"QueueADT.java": QUEUE_ADT, "TwoStackQueue.java": TS1, "TwoStackTester.java": TT1}, "TwoStackTester", "1\n2 3 4",
             hint="4 goes onto `in` while 2 and 3 are still in `out`. It only moves across once `out` is empty, so it comes out last, as it should."),
        step("The rest of the ADT", "Move the refill into a private `refill()` helper. `getFront` refills and peeks `out`; `isEmpty` is true when both stacks are empty; `size` adds their sizes. `dequeue` and `getFront` throw `NoSuchElementException(\"queue is empty\")`.",
             {"QueueADT.java": QUEUE_ADT, "TwoStackQueue.java": TS2, "TwoStackTester.java": TT2}, "TwoStackTester", "1 2 false\nqueue is empty"),
        step("Count the moves", "A single refill can move many values, which sounds O(n). Count every value moved from `in` to `out` (add a `moves` field and `getMoves()`), and run 2000 enqueues and 2000 dequeues.",
             {"QueueADT.java": QUEUE_ADT, "TwoStackQueue.java": TS3, "TwoStackTester.java": TT3}, "TwoStackTester", "2000 moves for 2000 values",
             hint="Each value is moved from `in` to `out` exactly once, so the total is n moves for n values: O(1) per operation on average."),
    ]),
    given(task("ws-u19-cutin", "Cutting in line",
         "Add `public void enqueueFront(T element)` to `LinkedQueue` (already in the editor), which puts a value at the **front** of the queue, in O(1). It's add-at-head: link the new node to `front` and make it the front. If the queue was empty, it's the rear too. `CutTester` enqueues `b` and `c`, calls `enqueueFront(\"a\")`, and prints the queue; then it uses `enqueueFront` on a new empty queue followed by `enqueue`, and prints that.",
         {"LinkedQueue.java": LINKED_QUEUE.replace("""    @Override
    public T dequeue() {""", """    public void enqueueFront(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        node.setNext(front);
        front = node;
        if (rear == null) {
            rear = node;
        }
        count++;
    }

    @Override
    public T dequeue() {"""), "CutTester.java": """public class CutTester {
    public static void main(String[] args) {
        LinkedQueue<String> q = new LinkedQueue<>();
        q.enqueue("b");
        q.enqueue("c");
        q.enqueueFront("a");
        System.out.println(q);
        LinkedQueue<String> e = new LinkedQueue<>();
        e.enqueueFront("x");
        e.enqueue("y");
        System.out.println(e + " " + e.size());
    }
}
"""}, "CutTester", "front [a, b, c] rear\nfront [x, y] rear 2",
         hints=["On an empty queue, `rear` is `null`. If you don't set it, the following `enqueue` calls `rear.setNext` on `null`."]), LQUEUE_FILES),
    given(task("ws-u19-mergesorted", "Merge two sorted queues",
         "Write `MergeQueues` with `public static QueueADT<Integer> merge(QueueADT<Integer> a, QueueADT<Integer> b)`: both queues are in increasing order from front to rear, and the result is a new `LinkedQueue` with all their values in increasing order. Compare the two fronts with `getFront()`, dequeue the smaller into the result, and when one queue runs out, move the rest of the other. `main` merges 1, 4, 9 with 2, 3, 10, 12 and prints the result. `QueueADT`, `LinearNode` and `LinkedQueue` are already in the editor.",
         {"MergeQueues.java": """public class MergeQueues {
    public static QueueADT<Integer> merge(QueueADT<Integer> a, QueueADT<Integer> b) {
        QueueADT<Integer> result = new LinkedQueue<>();
        while (!a.isEmpty() && !b.isEmpty()) {
            if (a.getFront() <= b.getFront()) {
                result.enqueue(a.dequeue());
            } else {
                result.enqueue(b.dequeue());
            }
        }
        while (!a.isEmpty()) {
            result.enqueue(a.dequeue());
        }
        while (!b.isEmpty()) {
            result.enqueue(b.dequeue());
        }
        return result;
    }

    public static void main(String[] args) {
        QueueADT<Integer> a = new LinkedQueue<>();
        QueueADT<Integer> b = new LinkedQueue<>();
        for (int v : new int[] {1, 4, 9}) {
            a.enqueue(v);
        }
        for (int v : new int[] {2, 3, 10, 12}) {
            b.enqueue(v);
        }
        System.out.println(merge(a, b));
    }
}
"""}, "MergeQueues", "front [1, 2, 3, 4, 9, 10, 12] rear",
         tests={"CheckMerge.java": """public class CheckMerge {
    public static void main(String[] args) {
        QueueADT<Integer> a = new LinkedQueue<>();
        QueueADT<Integer> b = new LinkedQueue<>();
        b.enqueue(5);
        b.enqueue(5);
        a.enqueue(5);
        System.out.println(MergeQueues.merge(a, b) + " " + MergeQueues.merge(new LinkedQueue<>(), new LinkedQueue<>()));
    }
}
"""}, tests_run="CheckMerge", tests_output="front [5, 5, 5] rear front [] rear",
         hints=["Each value is dequeued once, so merging is O(n + m)."]), LQUEUE_FILES),
    [ALGS4_13, OPENDSA_QUEUE, NOSUCH_API, DEQUE_API],
)
