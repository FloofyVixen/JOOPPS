from sources import ALGS4_13, ALGS4_41, QUEUE_TUT, DEQUE_API, LINKEDLIST_API
from wshelp import step, guided, workshop, task

M1 = """public class Maze {
    public static void main(String[] args) {
        String[] grid = {
            "S.#.....",
            ".##.###.",
            "....#E#.",
            ".##.....",
        };
        int open = 0;
        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[r].length(); c++) {
                char ch = grid[r].charAt(c);
                if (ch != '#') {
                    open++;
                }
                if (ch == 'S') {
                    System.out.println("start at row " + r + ", column " + c);
                }
            }
        }
        System.out.println(open + " open squares");
    }
}
"""
M2 = """import java.util.ArrayDeque;
import java.util.Queue;

public class Maze {
    public static void main(String[] args) {
        String[] grid = {
            "S.#.....",
            ".##.###.",
            "....#E#.",
            ".##.....",
        };
        int rows = grid.length;
        int cols = grid[0].length();
        boolean[][] seen = new boolean[rows][cols];
        Queue<int[]> toVisit = new ArrayDeque<>();
        toVisit.add(new int[] {0, 0});
        seen[0][0] = true;
        int[][] moves = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        int reached = 0;
        while (!toVisit.isEmpty()) {
            int[] square = toVisit.remove();
            reached++;
            for (int[] m : moves) {
                int r = square[0] + m[0];
                int c = square[1] + m[1];
                if (r >= 0 && r < rows && c >= 0 && c < cols && !seen[r][c] && grid[r].charAt(c) != '#') {
                    seen[r][c] = true;
                    toVisit.add(new int[] {r, c});
                }
            }
        }
        System.out.println(reached + " squares reachable");
    }
}
"""
M3 = M2.replace("""        boolean[][] seen = new boolean[rows][cols];""", """        int[][] dist = new int[rows][cols];
        for (int[] row : dist) {
            java.util.Arrays.fill(row, -1);
        }""").replace("""        seen[0][0] = true;""", """        dist[0][0] = 0;""").replace("""        int reached = 0;
        while (!toVisit.isEmpty()) {
            int[] square = toVisit.remove();
            reached++;""", """        while (!toVisit.isEmpty()) {
            int[] square = toVisit.remove();
            if (grid[square[0]].charAt(square[1]) == 'E') {
                System.out.println("exit in " + dist[square[0]][square[1]] + " steps");
                return;
            }""").replace("""!seen[r][c] && grid[r].charAt(c) != '#') {
                    seen[r][c] = true;""", """dist[r][c] == -1 && grid[r].charAt(c) != '#') {
                    dist[r][c] = dist[square[0]][square[1]] + 1;""").replace("""        System.out.println(reached + " squares reachable");""", """        System.out.println("no way out");""")
M3 = M3.replace("import java.util.ArrayDeque;\n", "import java.util.ArrayDeque;\nimport java.util.Arrays;\n").replace("java.util.Arrays.fill", "Arrays.fill")

P1 = """import java.util.ArrayDeque;
import java.util.Deque;

public class ToPostfix {
    public static String convert(String infix) {
        String output = "";
        Deque<Character> ops = new ArrayDeque<>();
        for (char c : infix.toCharArray()) {
            if (Character.isDigit(c)) {
                output += c + " ";
            } else if (c == '+' || c == '-') {
                while (!ops.isEmpty()) {
                    output += ops.pop() + " ";
                }
                ops.push(c);
            }
        }
        while (!ops.isEmpty()) {
            output += ops.pop() + " ";
        }
        return output.trim();
    }

    public static void main(String[] args) {
        System.out.println(convert("3+4"));
        System.out.println(convert("9-2+1"));
    }
}
"""
P2 = P1.replace("""            } else if (c == '+' || c == '-') {
                while (!ops.isEmpty()) {
                    output += ops.pop() + " ";
                }
                ops.push(c);
            }""", """            } else if (c == '+' || c == '-' || c == '*' || c == '/') {
                while (!ops.isEmpty() && rank(ops.peek()) >= rank(c)) {
                    output += ops.pop() + " ";
                }
                ops.push(c);
            }""").replace("""    public static String convert""", """    public static int rank(char op) {
        if (op == '*' || op == '/') {
            return 2;
        }
        return 1;
    }

    public static String convert""").replace("""        System.out.println(convert("3+4"));
        System.out.println(convert("9-2+1"));""", """        System.out.println(convert("3+4*2"));
        System.out.println(convert("8/4-1"));
        System.out.println(convert("1+2*3-4"));""")
P3 = P2.replace("""        if (op == '*' || op == '/') {
            return 2;
        }
        return 1;""", """        if (op == '*' || op == '/') {
            return 2;
        }
        if (op == '+' || op == '-') {
            return 1;
        }
        return 0;""").replace("""            } else if (c == '+' || c == '-' || c == '*' || c == '/') {""", """            } else if (c == '(') {
                ops.push(c);
            } else if (c == ')') {
                while (ops.peek() != '(') {
                    output += ops.pop() + " ";
                }
                ops.pop();
            } else if (c == '+' || c == '-' || c == '*' || c == '/') {""").replace("""        System.out.println(convert("3+4*2"));
        System.out.println(convert("8/4-1"));
        System.out.println(convert("1+2*3-4"));""", """        System.out.println(convert("(3+4)*2"));
        System.out.println(convert("2*(5-(1+1))"));""")

LESSON = workshop(
    "ws-ds-use-cases", "Workshop: choosing structures",
    "Solve four problems where the choice of structure is the solution: a maze, an expression converter, a recent-files list and a moving average.",
    ["Use a queue for breadth-first search and shortest paths",
     "Use a stack to hold operators until it's their turn",
     "Pick a linked list or a queue for problems that work at the ends"],
    guided("ws-u20-maze", "Escape the maze", "Find the shortest way out of a grid maze. `#` is a wall, `S` the start (top left), `E` the exit. Each step moves up, down, left or right.", [
        step("Read the grid", "In `Maze`, store the grid as a `String[]`. Loop over every square: count the ones that aren't walls, and print where `S` is.",
             {"Maze.java": M1}, "Maze", "start at row 0, column 0\n22 open squares"),
        step("Explore with a queue", "Breadth-first search from the start. Each queue entry is an `int[] {row, column}`. Take a square, count it, and add each neighbour that's inside the grid, not a wall and not seen yet (mark it seen when you add it). Print how many squares are reachable.",
             {"Maze.java": M2}, "Maze", "22 squares reachable",
             hint="Keeping the four moves in an array, `{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}`, saves writing the neighbour check four times."),
        step("Shortest path", "Replace `seen` with `int[][] dist` filled with -1. The start's distance is 0; a neighbour's is one more than the square it was reached from. When you take the exit off the queue, print `exit in <d> steps` and stop.",
             {"Maze.java": M3}, "Maze", "exit in 9 steps",
             hint="Because a queue explores squares in order of distance, the first time the exit comes off the queue is by a shortest route."),
    ]),
    guided("ws-u20-postfix", "From infix to postfix", "Unit 13's workshop evaluated postfix like `3 4 +`. People write infix, `3+4`. A stack of operators converts one to the other (single-digit numbers only).", [
        step("Plus and minus", "In `ToPostfix`, write `convert(String infix)`. Digits go straight to the output. For `+` or `-`, first pop every waiting operator to the output, then push this one. At the end, pop the rest. Separate output tokens with spaces.",
             {"ToPostfix.java": P1}, "ToPostfix", "3 4 +\n9 2 - 1 +",
             hint="Popping first makes `9-2+1` mean (9 − 2) + 1, which is how Java reads it."),
        step("Times and divide first", "Add `rank(char op)`: 2 for `*` and `/`, 1 for `+` and `-`. Before pushing an operator, pop only the waiting operators whose rank is **at least** as high.",
             {"ToPostfix.java": P2}, "ToPostfix", "3 4 2 * +\n8 4 / 1 -\n1 2 3 * + 4 -"),
        step("Brackets", "Push `(` as it comes (give it rank 0 so no operator pops it). At `)`, pop operators to the output until you reach the `(`, then pop and discard the `(`.",
             {"ToPostfix.java": P3}, "ToPostfix", "3 4 + 2 *\n2 5 1 1 + - *"),
    ]),
    task("ws-u20-recent", "Recent files",
         "An editor's File menu shows the 3 most recently opened files, newest first, with no repeats. Write `Recent` using a `java.util.LinkedList<String>`: `open(String name)` removes `name` if it's already there, adds it at the front with `addFirst`, and if there are now more than 3, removes the last with `removeLast`. `toString()` returns the list. `RecentTester` opens `a`, `b`, `c`, `a`, `d` and prints after each.",
         {"Recent.java": """import java.util.LinkedList;

public class Recent {
    private LinkedList<String> files = new LinkedList<>();

    public void open(String name) {
        files.remove(name);
        files.addFirst(name);
        if (files.size() > 3) {
            files.removeLast();
        }
    }

    @Override
    public String toString() {
        return files.toString();
    }
}
""", "RecentTester.java": """public class RecentTester {
    public static void main(String[] args) {
        Recent r = new Recent();
        for (String f : new String[] {"a", "b", "c", "a", "d"}) {
            r.open(f);
            System.out.println(r);
        }
    }
}
"""}, "RecentTester", "[a]\n[b, a]\n[c, b, a]\n[a, c, b]\n[d, a, c]",
         hints=["`remove(Object)` removes the first match and does nothing if there is none."]),
    task("ws-u20-average", "Moving average",
         "A moving average is the average of the last `k` values seen. Write `MovingAverage` with a constructor taking `k`, a `Queue<Integer>` of the recent values and a running `sum`. `next(int value)` adds the value; if the queue now holds more than `k`, it removes the oldest (and subtracts it from the sum). It returns the average of the values in the queue as a `double`. Each call is O(1): no loop over the queue. `AverageTester` uses `k = 3` and prints `next` of 2, 4, 6 and 10.",
         {"MovingAverage.java": """import java.util.ArrayDeque;
import java.util.Queue;

public class MovingAverage {
    private Queue<Integer> window = new ArrayDeque<>();
    private int k;
    private int sum = 0;

    public MovingAverage(int k) {
        this.k = k;
    }

    public double next(int value) {
        window.add(value);
        sum += value;
        if (window.size() > k) {
            sum -= window.remove();
        }
        return (double) sum / window.size();
    }
}
""", "AverageTester.java": """public class AverageTester {
    public static void main(String[] args) {
        MovingAverage m = new MovingAverage(3);
        System.out.println(m.next(2));
        System.out.println(m.next(4));
        System.out.println(m.next(6));
        System.out.println(m.next(10));
    }
}
"""}, "AverageTester", "2.0\n3.0\n4.0\n6.666666666666667",
         tests={"CheckAverage.java": """public class CheckAverage {
    public static void main(String[] args) {
        MovingAverage m = new MovingAverage(1);
        System.out.println(m.next(5) + " " + m.next(-5));
    }
}
"""}, tests_run="CheckAverage", tests_output="5.0 -5.0",
         checks=[{"pattern": r"^(?![\s\S]*\bfor\b)", "file": "MovingAverage.java", "message": "`MovingAverage` keeps a running sum instead of looping over the queue."}]),
    [ALGS4_13, ALGS4_41, QUEUE_TUT, DEQUE_API, LINKEDLIST_API],
)
