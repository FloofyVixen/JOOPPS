from sources import QUEUE_TUT, ARRAYDEQUE_API, LINKEDLIST_API, ALGS4_13

JAVAQ = """import java.util.ArrayDeque;
import java.util.Queue;

public class JavaQueue {
    public static void main(String[] args) {
        Queue<String> q = new ArrayDeque<>();
        q.add("first");
        q.add("second");
        q.offer("third");
        System.out.println(q);
        System.out.println(q.peek());
        System.out.println(q.remove());
        System.out.println(q.poll());
        System.out.println(q + " " + q.size());
    }
}
"""
EMPTYQ = """import java.util.ArrayDeque;
import java.util.Queue;

public class EmptyJavaQueue {
    public static void main(String[] args) {
        Queue<Integer> q = new ArrayDeque<>();
        System.out.println(q.peek());
        System.out.println(q.poll());
        System.out.println(q.remove());
    }
}
"""
POTATO = """import java.util.ArrayDeque;
import java.util.Queue;

public class HotPotato {
    public static String play(String[] names, int passes) {
        Queue<String> circle = new ArrayDeque<>();
        for (String name : names) {
            circle.add(name);
        }
        while (circle.size() > 1) {
            for (int i = 0; i < passes; i++) {
                circle.add(circle.remove());
            }
            System.out.println(circle.remove() + " is out");
        }
        return circle.remove();
    }

    public static void main(String[] args) {
        String[] names = {"Ana", "Ben", "Cy", "Dee", "Eli"};
        System.out.println("Winner: " + play(names, 2));
    }
}
"""
PRINTER = """import java.util.ArrayDeque;
import java.util.Queue;

public class PrintQueue {
    public static void main(String[] args) {
        Queue<String> jobs = new ArrayDeque<>();
        int[] pages = {3, 1, 4};
        String[] names = {"essay.pdf", "ticket.pdf", "notes.pdf"};
        for (int i = 0; i < names.length; i++) {
            jobs.add(names[i] + ":" + pages[i]);
        }
        int minute = 0;
        while (!jobs.isEmpty()) {
            String job = jobs.remove();
            String[] parts = job.split(":");
            minute += Integer.parseInt(parts[1]);
            System.out.println(parts[0] + " done at minute " + minute);
        }
    }
}
"""
BL = POTATO.replace("""            for (int i = 0; i < passes; i++) {
                circle.add(circle.remove());
            }
            System.out.println(circle.remove() + " is out");""", """            for (int i = 0; i < passes; i++) {
                [[pass]];
            }
            System.out.println([[out]] + " is out");""")

LESSON = {
    "id": "queue-use",
    "title": "Using a queue",
    "summary": "Java's `Queue` interface gives you a ready-made queue. Queues handle anything that must happen in arrival order, and rotating one models taking turns.",
    "goals": [
        "Use Java's `Queue` with `ArrayDeque`, and tell `add`/`remove`/`element` from `offer`/`poll`/`peek`",
        "Process jobs in arrival order",
        "Model taking turns by rotating a queue",
    ],
    "cos225": "The Exam 2 guide asks where queues are used and how they differ from stacks. Code questions give you the imports and scaffolding; these are the patterns to fill in.",
    "blocks": [
        {"type": "h", "text": "Java's Queue"},
        {"type": "p", "text": "Java has a `Queue` interface in `java.util`, implemented by `ArrayDeque` and `LinkedList`. Its methods have different names from our `QueueADT`, and they come in pairs: one throws an exception when it can't do its job, the other returns a special value (`null` or `false`) instead."},
        {"type": "list", "items": [
            "Enqueue: `add(x)` (throws if it can't) or `offer(x)` (returns `false`).",
            "Dequeue: `remove()` (throws on an empty queue) or `poll()` (returns `null`).",
            "Get front: `element()` (throws) or `peek()` (returns `null`).",
        ]},
        {"type": "code", "files": {"JavaQueue.java": JAVAQ}, "run": "JavaQueue",
         "after": "An `ArrayDeque` used as a queue prints from front to rear."},
        {"type": "code", "files": {"EmptyJavaQueue.java": EMPTYQ}, "run": "EmptyJavaQueue", "expect": "runtime",
         "after": "`peek` and `poll` return `null` on an empty queue; `remove` throws. Pick the one whose behaviour you want, and check `isEmpty()` when you're not sure."},

        {"type": "h", "text": "Serving in arrival order"},
        {"type": "p", "text": "A printer prints jobs in the order they were sent. Each job here is a string `name:pages`, and each page takes a minute:"},
        {"type": "code", "files": {"PrintQueue.java": PRINTER}, "run": "PrintQueue"},

        {"type": "h", "text": "Taking turns"},
        {"type": "p", "text": "Rotating a queue (`remove` from the front, `add` at the rear) passes the turn to the next value, and the value that just had its turn waits at the back. In the game hot potato, players pass the potato a set number of times, and whoever holds it then is out:"},
        {"type": "code", "files": {"HotPotato.java": POTATO}, "run": "HotPotato"},
        {"type": "p", "text": "Operating systems use the same idea to share a processor between programs: each gets a short turn, then goes to the back of the queue. This is called round-robin scheduling."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "use-potato", "title": "Pass the potato",
         "prompt": "Fill in the two blanks in `play`.",
         "files": {"HotPotato.java": BL}, "run": "HotPotato",
         "output": "Cy is out\nAna is out\nEli is out\nBen is out\nWinner: Dee",
         "blanks": {
             "pass": {"accept": ["circle.add(circle.remove())", "circle.offer(circle.poll())", "circle.add(circle.poll())", "circle.offer(circle.remove())"],
                      "hint": "The front player passes and goes to the back of the line: remove them from the front, add them at the rear. (`peek` would leave them at the front too, and the circle would grow forever.)"},
             "out": {"accept": ["circle.remove()", "circle.poll()"], "hint": "Whoever is at the front now is out, so they must leave the queue. `peek` would name them but leave them in, and the game would never end."},
         },
         "explain": "Rotate with `add(remove())` for each pass, then `remove()` the player at the front."},
        {"type": "quiz", "id": "use-poll",
         "question": "On an empty `Queue<String>`, what does `poll()` do?",
         "choices": ["Throws a `NoSuchElementException`", "Returns `null`", "Returns an empty string", "Waits until something is added"],
         "answer": 1,
         "explain": "`poll` and `peek` return `null` for an empty queue; `remove` and `element` throw `NoSuchElementException`."},
    ],
    "sources": [QUEUE_TUT, ARRAYDEQUE_API, LINKEDLIST_API, ALGS4_13],
}
