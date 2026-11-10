"""Write-it-yourself tasks for unit 20, Queues/Stacks/Linked List use cases. Compiled and run by build.py."""
from tasks_classes import task
from tasks_stacks import given
from ds_code import LSTACK_FILES, LQUEUE_FILES
import importlib.util
import os

_spec = importlib.util.spec_from_file_location("ds_project", os.path.join(os.path.dirname(__file__), "ds-project.py"))
_proj = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_proj)
DOC, SPOOL = _proj.DOC, _proj.SPOOL
BASE = {**LSTACK_FILES, **LQUEUE_FILES}

CHOOSE = [
    task("w-choose-distance", "How many doors away?",
         "Using the same `doors` layout idea as the lesson, write `Distance` with `public static int[] distances(int[][] doors, int start)`: a breadth-first search with a `Queue<Integer>` that records, for every room, how many doors it is from `start` (-1 if it can't be reached). Set a room's distance when you first add it to the queue: one more than the room you reached it from. `main` uses the layout below and prints `Arrays.toString(distances(doors, 0))` for the layout `{{1, 2}, {3}, {3, 4}, {5}, {}, {}, {0}}` (room 6 has a door to room 0, but nothing leads to room 6).",
         {"Distance.java": """import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Queue;

public class Distance {
    public static int[] distances(int[][] doors, int start) {
        int[] dist = new int[doors.length];
        Arrays.fill(dist, -1);
        Queue<Integer> toVisit = new ArrayDeque<>();
        dist[start] = 0;
        toVisit.add(start);
        while (!toVisit.isEmpty()) {
            int room = toVisit.remove();
            for (int next : doors[room]) {
                if (dist[next] == -1) {
                    dist[next] = dist[room] + 1;
                    toVisit.add(next);
                }
            }
        }
        return dist;
    }

    public static void main(String[] args) {
        int[][] doors = {{1, 2}, {3}, {3, 4}, {5}, {}, {}, {0}};
        System.out.println(Arrays.toString(distances(doors, 0)));
    }
}
"""}, "Distance", "[0, 1, 1, 2, 2, 3, -1]",
         tests={"CheckDistance.java": """import java.util.Arrays;

public class CheckDistance {
    public static void main(String[] args) {
        int[][] ring = {{1}, {2}, {0}};
        System.out.println(Arrays.toString(Distance.distances(ring, 1)));
    }
}
"""}, tests_run="CheckDistance", tests_output="[2, 0, 1]",
         hints=["Using -1 for \"not reached yet\" means you don't need a separate `seen` array."]),

    task("w-choose-reachable", "Count reachable rooms with a stack",
         "Write `Reach` with `public static int countReachable(int[][] doors, int start)`, a depth-first search with a `Deque<Integer>` stack and a `boolean[] seen`, returning how many rooms (including `start`) can be reached. `main` prints the count from room 0 and from room 4 for `{{1}, {2}, {0}, {0}, {3}}`.",
         {"Reach.java": """import java.util.ArrayDeque;
import java.util.Deque;

public class Reach {
    public static int countReachable(int[][] doors, int start) {
        boolean[] seen = new boolean[doors.length];
        Deque<Integer> toVisit = new ArrayDeque<>();
        toVisit.push(start);
        seen[start] = true;
        int count = 0;
        while (!toVisit.isEmpty()) {
            int room = toVisit.pop();
            count++;
            for (int next : doors[room]) {
                if (!seen[next]) {
                    seen[next] = true;
                    toVisit.push(next);
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        int[][] doors = {{1}, {2}, {0}, {0}, {3}};
        System.out.println(countReachable(doors, 0));
        System.out.println(countReachable(doors, 4));
    }
}
"""}, "Reach", "3\n5",
         tests={"CheckReach.java": """public class CheckReach {
    public static void main(String[] args) {
        int[][] alone = {{}, {0}};
        System.out.println(Reach.countReachable(alone, 0) + " " + Reach.countReachable(alone, 1));
    }
}
"""}, tests_run="CheckReach", tests_output="1 2",
         checks=[{"pattern": r"\.push\(", "message": "Use the `Deque` as a stack with `push` and `pop`."}]),
]

PROJECT_NOTE = "The project's classes are already in the editor."

PROJECT = [
    given(task("w-proj-redo", "Add redo",
         "Give `Document` a second stack, `future`, and a method `public boolean redo()`. `undo` now pushes the current text onto `future` before restoring the old text; `redo` does the reverse (push the current text onto `history`, pop `future`), returning `false` if there's nothing to redo. Any new edit (`append` or `replace`) makes redo impossible: set `future` to a new empty `LinkedStack`. `RedoTester` appends `a`, `b`, `c`, undoes twice, redoes once, prints the text, then appends `z`, prints `redo()` and the text. " + PROJECT_NOTE,
         {"Document.java": DOC.replace("""    private StackADT<String> history;
""", """    private StackADT<String> history;
    private StackADT<String> future;
""").replace("""        this.history = new LinkedStack<>();
""", """        this.history = new LinkedStack<>();
        this.future = new LinkedStack<>();
""").replace("""        history.push(text);
        text = text + more;""", """        history.push(text);
        future = new LinkedStack<>();
        text = text + more;""").replace("""        history.push(text);
        text = text.replace(target, replacement);""", """        history.push(text);
        future = new LinkedStack<>();
        text = text.replace(target, replacement);""").replace("""        text = history.pop();
        return true;
    }
""", """        future.push(text);
        text = history.pop();
        return true;
    }

    public boolean redo() {
        if (future.isEmpty()) {
            return false;
        }
        history.push(text);
        text = future.pop();
        return true;
    }
"""), "RedoTester.java": """public class RedoTester {
    public static void main(String[] args) {
        Document d = new Document("d");
        d.append("a");
        d.append("b");
        d.append("c");
        d.undo();
        d.undo();
        d.redo();
        System.out.println(d.getText());
        d.append("z");
        System.out.println(d.redo() + " " + d.getText());
    }
}
"""}, "RedoTester", "ab\nfalse abz",
         tests={"CheckRedo.java": """public class CheckRedo {
    public static void main(String[] args) {
        Document d = new Document("d");
        System.out.println(d.redo() + " " + d.undo());
        d.append("x");
        d.undo();
        d.redo();
        d.undo();
        System.out.println("[" + d.getText() + "] " + d.redo() + " " + d.getText());
    }
}
"""}, tests_run="CheckRedo", tests_output="false false\n[] true x"), {**BASE, "Document.java": DOC, "Spooler.java": SPOOL}),

    given(task("w-proj-cancel", "Cancel a document's jobs",
         "Add `public int cancel(String docName)` to `Spooler`: remove every waiting job for that document (a job's text starts with `docName + \": \"`) and return how many were removed, keeping the other jobs in their order. Rotate through the queue once: dequeue each of the `size()` jobs, and enqueue it again only if it should stay. `CancelTester` submits `memo`, `plan`, `memo` again (after an edit), then cancels `memo`, prints the count and `waiting()`, and prints the next job. " + PROJECT_NOTE,
         {"Spooler.java": SPOOL.replace("""    public int waiting() {""", """    public int cancel(String docName) {
        int removed = 0;
        int n = jobs.size();
        for (int i = 0; i < n; i++) {
            String job = jobs.dequeue();
            if (job.startsWith(docName + ": ")) {
                removed++;
            } else {
                jobs.enqueue(job);
            }
        }
        return removed;
    }

    public int waiting() {"""), "CancelTester.java": """public class CancelTester {
    public static void main(String[] args) {
        Spooler s = new Spooler();
        Document memo = new Document("memo");
        Document plan = new Document("plan");
        memo.append("v1");
        plan.append("steps");
        s.submit(memo);
        s.submit(plan);
        memo.append(" v2");
        s.submit(memo);
        System.out.println(s.cancel("memo") + " " + s.waiting());
        s.printNext();
    }
}
"""}, "CancelTester", "2 1\nprinting plan: steps",
         tests={"CheckCancel.java": """public class CheckCancel {
    public static void main(String[] args) {
        Spooler s = new Spooler();
        Document a = new Document("a");
        Document ab = new Document("ab");
        s.submit(ab);
        s.submit(a);
        s.submit(ab);
        System.out.println(s.cancel("a") + " " + s.cancel("zzz") + " " + s.waiting());
        s.printNext();
        s.printNext();
    }
}
"""}, tests_run="CheckCancel", tests_output="1 0 2\nprinting ab: \nprinting ab: ",
         hints=["Save `jobs.size()` before the loop: re-enqueued jobs would otherwise keep the loop going.", "Checking `docName + \": \"` stops `cancel(\"a\")` from also removing jobs for `ab`."]), {**BASE, "Document.java": DOC, "Spooler.java": SPOOL}),
]

TASKS = {"ds-choose": CHOOSE, "ds-project": PROJECT}
