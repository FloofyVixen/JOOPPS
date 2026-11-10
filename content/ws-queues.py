from sources import QUEUE_TUT, ARRAYDEQUE_API, ALGS4_13, OPENDSA_QUEUE
from wshelp import step, guided, workshop, task

CUST = """public class Customer {
    private String name;
    private int arrival;
    private int service;

    public Customer(String name, int arrival, int service) {
        this.name = name;
        this.arrival = arrival;
        this.service = service;
    }

    public String getName() {
        return name;
    }

    public int getArrival() {
        return arrival;
    }

    public int getService() {
        return service;
    }
}
"""
B1 = """import java.util.ArrayDeque;
import java.util.Queue;

public class Bank {
    public static void main(String[] args) {
        Queue<Customer> line = new ArrayDeque<>();
        line.add(new Customer("Ana", 0, 5));
        line.add(new Customer("Ben", 1, 3));
        line.add(new Customer("Cy", 9, 2));
        while (!line.isEmpty()) {
            Customer c = line.remove();
            System.out.println(c.getName() + " served");
        }
    }
}
"""
B2 = B1.replace("""        while (!line.isEmpty()) {
            Customer c = line.remove();
            System.out.println(c.getName() + " served");
        }""", """        int clock = 0;
        while (!line.isEmpty()) {
            Customer c = line.remove();
            int start = Math.max(clock, c.getArrival());
            int wait = start - c.getArrival();
            clock = start + c.getService();
            System.out.println(c.getName() + ": waited " + wait + ", done at " + clock);
        }""")
B3 = B2.replace("""        int clock = 0;""", """        int clock = 0;
        int totalWait = 0;
        int served = 0;""").replace("""            clock = start + c.getService();""", """            clock = start + c.getService();
            totalWait += wait;
            served++;""").replace("""            System.out.println(c.getName() + ": waited " + wait + ", done at " + clock);
        }""", """            System.out.println(c.getName() + ": waited " + wait + ", done at " + clock);
        }
        System.out.println("average wait " + (double) totalWait / served);""")

TASKC = """public class Job {
    private String name;
    private int remaining;

    public Job(String name, int time) {
        this.name = name;
        this.remaining = time;
    }

    public String getName() {
        return name;
    }

    public int getRemaining() {
        return remaining;
    }

    // Runs for up to `slice` units and returns how long it actually ran.
    public int run(int slice) {
        int used = Math.min(slice, remaining);
        remaining -= used;
        return used;
    }
}
"""
R1 = """import java.util.ArrayDeque;
import java.util.Queue;

public class Scheduler {
    public static void main(String[] args) {
        Queue<Job> ready = new ArrayDeque<>();
        ready.add(new Job("A", 5));
        ready.add(new Job("B", 2));
        ready.add(new Job("C", 3));
        int size = ready.size();
        for (int i = 0; i < size; i++) {
            Job job = ready.remove();
            int used = job.run(2);
            System.out.println(job.getName() + " ran " + used + ", " + job.getRemaining() + " left");
        }
    }
}
"""
R2 = R1.replace("""        int size = ready.size();
        for (int i = 0; i < size; i++) {
            Job job = ready.remove();
            int used = job.run(2);
            System.out.println(job.getName() + " ran " + used + ", " + job.getRemaining() + " left");
        }""", """        while (!ready.isEmpty()) {
            Job job = ready.remove();
            int used = job.run(2);
            System.out.println(job.getName() + " ran " + used + ", " + job.getRemaining() + " left");
            if (job.getRemaining() > 0) {
                ready.add(job);
            }
        }""")
R3 = R2.replace("""        while (!ready.isEmpty()) {""", """        int clock = 0;
        while (!ready.isEmpty()) {""").replace("""            int used = job.run(2);
            System.out.println(job.getName() + " ran " + used + ", " + job.getRemaining() + " left");
            if (job.getRemaining() > 0) {
                ready.add(job);
            }""", """            clock += job.run(2);
            if (job.getRemaining() > 0) {
                ready.add(job);
            } else {
                System.out.println(job.getName() + " finished at " + clock);
            }""")

LESSON = workshop(
    "ws-queues", "Workshop: queues",
    "Simulate a bank line and a processor sharing its time, then use queues for a counting-out game and, together with a stack, for palindromes.",
    ["Process objects in arrival order with Java's `Queue`",
     "Re-enqueue unfinished work to share turns fairly",
     "Combine a queue and a stack to compare an order with its reverse"],
    guided("ws-u18-bank", "A bank line", "Simulate customers waiting for one teller. Each `Customer` has a name, an arrival minute and how many minutes they need.", [
        step("Serve in order", "Create `Customer` (private `name`, `arrival`, `service`, a constructor and getters). In `Bank`, add three customers to a `Queue<Customer>` (an `ArrayDeque`) and remove them one by one, printing `<name> served`.",
             {"Customer.java": CUST, "Bank.java": B1}, "Bank", "Ana served\nBen served\nCy served"),
        step("Keep the clock", "Track a `clock`. Each customer starts at whichever is later, the clock or their arrival, waits `start - arrival` minutes, and leaves at `start + service`, which becomes the new clock. Print `<name>: waited <w>, done at <clock>`.",
             {"Customer.java": CUST, "Bank.java": B2}, "Bank",
             "Ana: waited 0, done at 5\nBen: waited 4, done at 8\nCy: waited 0, done at 11",
             hint="Cy arrives at minute 9, after the teller is free at 8, so the teller waits for Cy, not the other way round: `Math.max`."),
        step("Average wait", "Add up the waits and count the customers, then print `average wait <value>` as a `double`.",
             {"Customer.java": CUST, "Bank.java": B3}, "Bank",
             "Ana: waited 0, done at 5\nBen: waited 4, done at 8\nCy: waited 0, done at 11\naverage wait 1.3333333333333333"),
    ]),
    guided("ws-u18-roundrobin", "Round-robin scheduling", "A processor runs several jobs by giving each a short time slice in turn. Unfinished jobs go to the back of the queue.", [
        step("One round", "Create `Job` (name, remaining time, and `run(int slice)`, which runs for up to `slice` units and returns how long it ran). In `Scheduler`, give each of three jobs one turn of 2 units, printing `<name> ran <used>, <remaining> left`.",
             {"Job.java": TASKC, "Scheduler.java": R1}, "Scheduler", "A ran 2, 3 left\nB ran 2, 0 left\nC ran 2, 1 left"),
        step("Back of the line", "Keep going until the queue is empty: after its turn, a job with time left is added back at the rear.",
             {"Job.java": TASKC, "Scheduler.java": R2}, "Scheduler",
             "A ran 2, 3 left\nB ran 2, 0 left\nC ran 2, 1 left\nA ran 2, 1 left\nC ran 1, 0 left\nA ran 1, 0 left"),
        step("Finishing times", "Track a clock (add the time each turn used) and print only `<name> finished at <clock>` when a job completes.",
             {"Job.java": TASKC, "Scheduler.java": R3}, "Scheduler", "B finished at 4\nC finished at 9\nA finished at 10"),
    ]),
    task("ws-u18-survivor", "Last one standing",
         "`n` people stand in a circle, numbered 1 to `n`. Counting starts at person 1; every `k`-th person is out, and counting continues from the next person. Write `Circle` with `public static int survivor(int n, int k)` using a `Queue<Integer>`: rotate `k - 1` people to the rear, then remove the next one. Return the last person left. `main` prints `survivor(7, 3)` and `survivor(5, 2)`.",
         {"Circle.java": """import java.util.ArrayDeque;
import java.util.Queue;

public class Circle {
    public static int survivor(int n, int k) {
        Queue<Integer> circle = new ArrayDeque<>();
        for (int i = 1; i <= n; i++) {
            circle.add(i);
        }
        while (circle.size() > 1) {
            for (int i = 0; i < k - 1; i++) {
                circle.add(circle.remove());
            }
            circle.remove();
        }
        return circle.remove();
    }

    public static void main(String[] args) {
        System.out.println(survivor(7, 3));
        System.out.println(survivor(5, 2));
    }
}
"""}, "Circle", "4\n3",
         tests={"CheckCircle.java": """public class CheckCircle {
    public static void main(String[] args) {
        System.out.println(Circle.survivor(1, 5) + " " + Circle.survivor(6, 1) + " " + Circle.survivor(10, 2));
    }
}
"""}, tests_run="CheckCircle", tests_output="1 6 5"),
    task("ws-u18-palindrome", "Palindromes with a stack and a queue",
         "A queue gives the letters back in order; a stack gives them back reversed. Write `Mirror` with `public static boolean isPalindrome(String text)`: put every **letter** of the text (skip other characters with `Character.isLetter`, and compare in lower case) into both a `Queue<Character>` and a `Deque<Character>` stack, then remove from both and compare. `main` prints the result for `Never odd or even`, `Java` and `A`.",
         {"Mirror.java": """import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Queue;

public class Mirror {
    public static boolean isPalindrome(String text) {
        Queue<Character> queue = new ArrayDeque<>();
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < text.length(); i++) {
            char c = Character.toLowerCase(text.charAt(i));
            if (Character.isLetter(c)) {
                queue.add(c);
                stack.push(c);
            }
        }
        while (!queue.isEmpty()) {
            if (!queue.remove().equals(stack.pop())) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("Never odd or even"));
        System.out.println(isPalindrome("Java"));
        System.out.println(isPalindrome("A"));
    }
}
"""}, "Mirror", "true\nfalse\ntrue",
         tests={"CheckMirror.java": """public class CheckMirror {
    public static void main(String[] args) {
        System.out.println(Mirror.isPalindrome("") + " " + Mirror.isPalindrome("Was it a car or a cat I saw?") + " " + Mirror.isPalindrome("ab"));
    }
}
"""}, tests_run="CheckMirror", tests_output="true true false",
         hints=["`queue.remove()` and `stack.pop()` return `Character` objects: compare them with `equals`."]),
    [QUEUE_TUT, ARRAYDEQUE_API, ALGS4_13, OPENDSA_QUEUE],
)
