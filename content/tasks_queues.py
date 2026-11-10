"""Write-it-yourself tasks for unit 18, Introduction to Queues. Compiled and run by build.py."""
from tasks_classes import task
from tasks_stacks import given
from ds_code import LQUEUE_FILES, STACK_FILES

GIVEN = "`QueueADT` and `LinkedQueue` are already in the editor."

FIFO = [
    given(task("w-q-serve", "Serve everyone",
         "Write `Serve`. Its `main` enqueues `Ana`, `Ben`, `Cy` and `Dee` into a `LinkedQueue<String>`, then dequeues until the queue is empty, printing `Serving <name>` for each. " + GIVEN,
         {"Serve.java": """public class Serve {
    public static void main(String[] args) {
        QueueADT<String> line = new LinkedQueue<>();
        line.enqueue("Ana");
        line.enqueue("Ben");
        line.enqueue("Cy");
        line.enqueue("Dee");
        while (!line.isEmpty()) {
            System.out.println("Serving " + line.dequeue());
        }
    }
}
"""}, "Serve", "Serving Ana\nServing Ben\nServing Cy\nServing Dee",
         checks=[{"pattern": r"isEmpty\(\)", "message": "Loop until `isEmpty()` is true."}]), LQUEUE_FILES),

    given(task("w-q-frontornone", "A safe getFront",
         "Write `SafeFront` with `public static String frontOrNone(QueueADT<String> q)`: the front value, or `\"none\"` for an empty queue, without changing the queue. `main` prints it for an empty queue, then enqueues `x` and `y` and prints it again, then prints the size. " + GIVEN,
         {"SafeFront.java": """public class SafeFront {
    public static String frontOrNone(QueueADT<String> q) {
        if (q.isEmpty()) {
            return "none";
        }
        return q.getFront();
    }

    public static void main(String[] args) {
        QueueADT<String> q = new LinkedQueue<>();
        System.out.println(frontOrNone(q));
        q.enqueue("x");
        q.enqueue("y");
        System.out.println(frontOrNone(q));
        System.out.println(q.size());
    }
}
"""}, "SafeFront", "none\nx\n2",
         tests={"CheckSafeFront.java": """public class CheckSafeFront {
    public static void main(String[] args) {
        QueueADT<String> q = new LinkedQueue<>();
        q.enqueue("only");
        System.out.println(SafeFront.frontOrNone(q) + " " + q.size());
    }
}
"""}, tests_run="CheckSafeFront", tests_output="only 1"), LQUEUE_FILES),
]

TRACE = [
    given(task("w-q-rotate", "Rotate a queue",
         "Write `Rotate` with `public static void rotate(QueueADT<Integer> q, int k)`, which moves the front value to the rear `k` times. `main` enqueues 1 to 5, rotates by 2 and prints the queue. " + GIVEN,
         {"Rotate.java": """public class Rotate {
    public static void rotate(QueueADT<Integer> q, int k) {
        for (int i = 0; i < k; i++) {
            q.enqueue(q.dequeue());
        }
    }

    public static void main(String[] args) {
        QueueADT<Integer> q = new LinkedQueue<>();
        for (int i = 1; i <= 5; i++) {
            q.enqueue(i);
        }
        rotate(q, 2);
        System.out.println(q);
    }
}
"""}, "Rotate", "front [3, 4, 5, 1, 2] rear",
         tests={"CheckRotate.java": """public class CheckRotate {
    public static void main(String[] args) {
        QueueADT<Integer> q = new LinkedQueue<>();
        q.enqueue(7);
        q.enqueue(8);
        Rotate.rotate(q, 0);
        System.out.println(q);
        Rotate.rotate(q, 3);
        System.out.println(q);
    }
}
"""}, tests_run="CheckRotate", tests_output="front [7, 8] rear\nfront [8, 7] rear"), LQUEUE_FILES),

    given(task("w-q-sum-keep", "Add up a queue and keep it",
         "Write `QueueSum` with `public static int sum(QueueADT<Integer> q)`, which returns the total of the values **and leaves the queue exactly as it was**. Rotate each value through once: dequeue it, add it, enqueue it again, `size()` times. `main` enqueues 4, 6 and 10, prints the sum, then prints the queue. " + GIVEN,
         {"QueueSum.java": """public class QueueSum {
    public static int sum(QueueADT<Integer> q) {
        int total = 0;
        int n = q.size();
        for (int i = 0; i < n; i++) {
            int value = q.dequeue();
            total += value;
            q.enqueue(value);
        }
        return total;
    }

    public static void main(String[] args) {
        QueueADT<Integer> q = new LinkedQueue<>();
        q.enqueue(4);
        q.enqueue(6);
        q.enqueue(10);
        System.out.println(sum(q));
        System.out.println(q);
    }
}
"""}, "QueueSum", "20\nfront [4, 6, 10] rear",
         tests={"CheckQueueSum.java": """public class CheckQueueSum {
    public static void main(String[] args) {
        QueueADT<Integer> q = new LinkedQueue<>();
        System.out.println(QueueSum.sum(q));
        q.enqueue(-3);
        System.out.println(QueueSum.sum(q) + " " + q);
    }
}
"""}, tests_run="CheckQueueSum", tests_output="0\n-3 front [-3] rear",
         hints=["Save `q.size()` before the loop. It doesn't change here, but it's a good habit when a loop adds and removes."]), LQUEUE_FILES),
]

USE = [
    task("w-q-reverse", "Reverse a queue with a stack",
         "Write `ReverseQueue` with `public static void reverse(Queue<Integer> q)` that reverses a `java.util.Queue` using a `Deque<Integer>` as a stack: dequeue everything onto the stack, then pop everything back into the queue. `main` puts 1 to 4 into an `ArrayDeque` queue, reverses it and prints it.",
         {"ReverseQueue.java": """import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Queue;

public class ReverseQueue {
    public static void reverse(Queue<Integer> q) {
        Deque<Integer> stack = new ArrayDeque<>();
        while (!q.isEmpty()) {
            stack.push(q.remove());
        }
        while (!stack.isEmpty()) {
            q.add(stack.pop());
        }
    }

    public static void main(String[] args) {
        Queue<Integer> q = new ArrayDeque<>();
        for (int i = 1; i <= 4; i++) {
            q.add(i);
        }
        reverse(q);
        System.out.println(q);
    }
}
"""}, "ReverseQueue", "[4, 3, 2, 1]",
         tests={"CheckReverseQueue.java": """import java.util.ArrayDeque;
import java.util.Queue;

public class CheckReverseQueue {
    public static void main(String[] args) {
        Queue<Integer> q = new ArrayDeque<>();
        ReverseQueue.reverse(q);
        q.add(5);
        ReverseQueue.reverse(q);
        q.add(6);
        ReverseQueue.reverse(q);
        System.out.println(q);
    }
}
"""}, tests_run="CheckReverseQueue", tests_output="[6, 5]"),

    task("w-q-interleave", "Merge two lines",
         "Write `Merge` with `public static Queue<String> interleave(Queue<String> a, Queue<String> b)`, which returns a new queue taking one value from `a`, then one from `b`, and so on; when one runs out, the rest of the other follows. Use `poll` and `isEmpty`. `main` interleaves `[a1, a2, a3]` with `[b1]` and prints the result.",
         {"Merge.java": """import java.util.ArrayDeque;
import java.util.Queue;

public class Merge {
    public static Queue<String> interleave(Queue<String> a, Queue<String> b) {
        Queue<String> result = new ArrayDeque<>();
        while (!a.isEmpty() || !b.isEmpty()) {
            if (!a.isEmpty()) {
                result.add(a.poll());
            }
            if (!b.isEmpty()) {
                result.add(b.poll());
            }
        }
        return result;
    }

    public static void main(String[] args) {
        Queue<String> a = new ArrayDeque<>();
        Queue<String> b = new ArrayDeque<>();
        a.add("a1");
        a.add("a2");
        a.add("a3");
        b.add("b1");
        System.out.println(interleave(a, b));
    }
}
"""}, "Merge", "[a1, b1, a2, a3]",
         tests={"CheckMerge.java": """import java.util.ArrayDeque;
import java.util.Queue;

public class CheckMerge {
    public static void main(String[] args) {
        Queue<String> a = new ArrayDeque<>();
        Queue<String> b = new ArrayDeque<>();
        b.add("x");
        b.add("y");
        System.out.println(Merge.interleave(a, b) + " " + Merge.interleave(new ArrayDeque<>(), new ArrayDeque<>()));
    }
}
"""}, tests_run="CheckMerge", tests_output="[x, y] []"),
]

TASKS = {"queue-fifo": FIFO, "queue-trace": TRACE, "queue-use": USE}
