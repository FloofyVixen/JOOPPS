from sources import ALGS4_13, OPENDSA_STACK, EMPTYSTACK_API, GENERICS_TUT
from wshelp import step, guided, workshop, task
from ds_code import STACK_ADT

S1 = """public class ArrayStack<T> implements StackADT<T> {
    private Object[] stack;
    private int top;

    public ArrayStack() {
        stack = new Object[2];
        top = 0;
    }

    @Override
    public void push(T element) {
        stack[top] = element;
        top++;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T peek() {
        return (T) stack[top - 1];
    }

    @Override
    public T pop() {
        return null;
    }

    @Override
    public boolean isEmpty() {
        return top == 0;
    }

    @Override
    public int size() {
        return top;
    }
}
"""
S2 = "import java.util.EmptyStackException;\n\n" + S1.replace("""    @SuppressWarnings("unchecked")
    @Override
    public T peek() {
        return (T) stack[top - 1];
    }

    @Override
    public T pop() {
        return null;
    }
""", """    @SuppressWarnings("unchecked")
    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return (T) stack[top - 1];
    }

    @SuppressWarnings("unchecked")
    @Override
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        top--;
        T result = (T) stack[top];
        stack[top] = null;
        return result;
    }
""")
S3 = S2.replace("""    public void push(T element) {
        stack[top] = element;""", """    public void push(T element) {
        if (top == stack.length) {
            expandCapacity();
        }
        stack[top] = element;""").replace("""    @Override
    public int size() {
        return top;
    }
""", """    @Override
    public int size() {
        return top;
    }

    private void expandCapacity() {
        Object[] bigger = new Object[stack.length * 2];
        for (int i = 0; i < top; i++) {
            bigger[i] = stack[i];
        }
        stack = bigger;
    }

    @Override
    public String toString() {
        String result = "bottom [";
        for (int i = 0; i < top; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += stack[i];
        }
        return result + "] top";
    }
""")
ST1 = """public class StackTester {
    public static void main(String[] args) {
        StackADT<String> s = new ArrayStack<>();
        System.out.println(s.isEmpty());
        s.push("ant");
        s.push("bee");
        System.out.println(s.peek() + " " + s.size() + " " + s.isEmpty());
    }
}
"""
ST2 = """import java.util.EmptyStackException;

public class StackTester {
    public static void main(String[] args) {
        StackADT<String> s = new ArrayStack<>();
        s.push("ant");
        s.push("bee");
        System.out.println(s.pop() + " " + s.pop() + " " + s.size());
        try {
            s.pop();
        } catch (EmptyStackException e) {
            System.out.println("empty");
        }
    }
}
"""
ST3 = """public class StackTester {
    public static void main(String[] args) {
        StackADT<String> s = new ArrayStack<>();
        String[] bugs = {"ant", "bee", "cricket", "dragonfly", "earwig"};
        for (String bug : bugs) {
            s.push(bug);
        }
        System.out.println(s);
        s.pop();
        System.out.println(s + " " + s.size());
    }
}
"""

TW1 = """public class TwoStacks {
    private int[] data;
    private int left;
    private int right;

    public TwoStacks(int capacity) {
        data = new int[capacity];
        left = 0;
        right = capacity - 1;
    }

    public void pushLeft(int value) {
        data[left] = value;
        left++;
    }

    public void pushRight(int value) {
        data[right] = value;
        right--;
    }

    public int sizeLeft() {
        return left;
    }

    public int sizeRight() {
        return data.length - 1 - right;
    }
}
"""
TW2 = TW1.replace("""    public int sizeLeft() {""", """    public int popLeft() {
        if (left == 0) {
            throw new IllegalStateException("left stack is empty");
        }
        left--;
        return data[left];
    }

    public int popRight() {
        if (right == data.length - 1) {
            throw new IllegalStateException("right stack is empty");
        }
        right++;
        return data[right];
    }

    public int sizeLeft() {""")
TW3 = TW2.replace("""    public void pushLeft(int value) {
        data[left] = value;""", """    public boolean isFull() {
        return left > right;
    }

    public void pushLeft(int value) {
        if (isFull()) {
            throw new IllegalStateException("array is full");
        }
        data[left] = value;""").replace("""    public void pushRight(int value) {
        data[right] = value;""", """    public void pushRight(int value) {
        if (isFull()) {
            throw new IllegalStateException("array is full");
        }
        data[right] = value;""")
TT1 = """public class TwoTester {
    public static void main(String[] args) {
        TwoStacks t = new TwoStacks(5);
        t.pushLeft(1);
        t.pushLeft(2);
        t.pushRight(9);
        System.out.println(t.sizeLeft() + " " + t.sizeRight());
    }
}
"""
TT2 = """public class TwoTester {
    public static void main(String[] args) {
        TwoStacks t = new TwoStacks(5);
        t.pushLeft(1);
        t.pushLeft(2);
        t.pushRight(9);
        t.pushRight(8);
        System.out.println(t.popLeft() + " " + t.popRight() + " " + t.popRight());
        try {
            t.popRight();
        } catch (IllegalStateException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""
TT3 = """public class TwoTester {
    public static void main(String[] args) {
        TwoStacks t = new TwoStacks(4);
        t.pushLeft(1);
        t.pushRight(9);
        t.pushLeft(2);
        t.pushRight(8);
        System.out.println(t.isFull());
        try {
            t.pushLeft(3);
        } catch (IllegalStateException e) {
            System.out.println(e.getMessage());
        }
        t.popRight();
        t.pushLeft(3);
        System.out.println(t.sizeLeft() + " " + t.sizeRight() + " " + t.isFull());
    }
}
"""

LESSON = workshop(
    "ws-array-stack", "Workshop: array stacks",
    "Build an array stack from an empty file, then stretch the idea: two stacks sharing one array, a stack that forgets its oldest values, and a stack that always knows its minimum.",
    ["Write a generic array stack with push, pop, peek, expansion and toString",
     "Keep track of a top index precisely, from either end of an array",
     "Choose where to put the top so the common operations stay fast"],
    guided("ws-u14-arraystack", "ArrayStack from scratch", "Write the whole `ArrayStack<T>`, one piece at a time. Create `StackADT.java` too, with the five stack methods.", [
        step("Push and peek", "Create `StackADT<T>` and `ArrayStack<T>`, with an `Object[]` of 2 slots and `int top`. Write `push`, `peek`, `isEmpty` and `size`. For now `pop` can just `return null;` so the class compiles.",
             {"StackADT.java": STACK_ADT, "ArrayStack.java": S1, "StackTester.java": ST1}, "StackTester", "true\nbee 2 false",
             hint="`push` stores at `stack[top]`, then increments. The top value is at `top - 1`."),
        step("Pop, and empty stacks", "Write `pop`: move `top` down, take the value, clear the slot. `pop` and `peek` throw `EmptyStackException` (import it from `java.util`) when the stack is empty.",
             {"StackADT.java": STACK_ADT, "ArrayStack.java": S2, "StackTester.java": ST2}, "StackTester", "bee ant 0\nempty"),
        step("Growing and printing", "Add `expandCapacity()`, called by `push` when `top == stack.length`, and a `toString()` in the `bottom [ ... ] top` format. Push five values into the 2-slot array.",
             {"StackADT.java": STACK_ADT, "ArrayStack.java": S3, "StackTester.java": ST3}, "StackTester",
             "bottom [ant, bee, cricket, dragonfly, earwig] top\nbottom [ant, bee, cricket, dragonfly] top 4"),
    ]),
    guided("ws-u14-twostacks", "Two stacks in one array", "Two stacks can share one array: the left stack grows up from index 0, the right one grows down from the last index. The array is only full when they meet.", [
        step("Pushing from both ends", "Write `TwoStacks` with an `int[] data` (capacity from the constructor), `left` (next free slot from the left, starting at 0) and `right` (next free slot from the right, starting at the last index). Write `pushLeft`, `pushRight`, `sizeLeft()` and `sizeRight()`.",
             {"TwoStacks.java": TW1, "TwoTester.java": TT1}, "TwoTester", "2 1",
             hint="The right stack's size is how far `right` has moved down from the last index: `data.length - 1 - right`."),
        step("Popping", "Add `popLeft()` and `popRight()`. Each moves its index back toward its own end and returns the value there. An empty side throws `IllegalStateException` with the message `left stack is empty` or `right stack is empty`.",
             {"TwoStacks.java": TW2, "TwoTester.java": TT2}, "TwoTester", "2 8 9\nright stack is empty"),
        step("Full means they've met", "Add `isFull()`, true when `left > right` (no free slot between them). Both push methods throw `IllegalStateException(\"array is full\")` when it's full.",
             {"TwoStacks.java": TW3, "TwoTester.java": TT3}, "TwoTester", "true\narray is full\n3 1 true",
             hint="With capacity 4, after two pushes on each side `left` is 2 and `right` is 1."),
    ]),
    task("ws-u14-dropstack", "A stack that forgets",
         "Undo histories often keep only the most recent changes. Write `DropStack`, a `String` stack with a fixed capacity (from the constructor) and the top at the end. When `push` finds it full, it **drops the bottom value** (shift everything left one slot) to make room, instead of growing. Methods: `push`, `pop` (throw `IllegalStateException(\"empty\")` if empty), `size()`, and `toString()` in the `bottom [ ... ] top` format. `DropTester` makes a capacity-3 stack, pushes `a` to `e`, prints it, pops once and prints it again.",
         {"DropStack.java": """public class DropStack {
    private String[] stack;
    private int top;

    public DropStack(int capacity) {
        stack = new String[capacity];
        top = 0;
    }

    public void push(String value) {
        if (top == stack.length) {
            for (int i = 0; i < top - 1; i++) {
                stack[i] = stack[i + 1];
            }
            top--;
        }
        stack[top] = value;
        top++;
    }

    public String pop() {
        if (top == 0) {
            throw new IllegalStateException("empty");
        }
        top--;
        String result = stack[top];
        stack[top] = null;
        return result;
    }

    public int size() {
        return top;
    }

    @Override
    public String toString() {
        String result = "bottom [";
        for (int i = 0; i < top; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += stack[i];
        }
        return result + "] top";
    }
}
""", "DropTester.java": """public class DropTester {
    public static void main(String[] args) {
        DropStack s = new DropStack(3);
        for (String v : new String[] {"a", "b", "c", "d", "e"}) {
            s.push(v);
        }
        System.out.println(s);
        s.pop();
        System.out.println(s);
    }
}
"""}, "DropTester", "bottom [c, d, e] top\nbottom [c, d] top",
         tests={"CheckDrop.java": """public class CheckDrop {
    public static void main(String[] args) {
        DropStack s = new DropStack(2);
        s.push("x");
        System.out.println(s + " " + s.size());
        s.push("y");
        s.push("z");
        System.out.println(s.pop() + s.pop() + " " + s.size());
    }
}
"""}, tests_run="CheckDrop", tests_output="bottom [x] top 1\nzy 0",
         hints=["Shifting left is O(n), but it only happens when the stack is full."]),
    task("ws-u14-minstack", "A stack that knows its minimum",
         "Write `MinStack`, an `int` stack whose `min()` returns the smallest value in the stack in O(1): no loop. Keep two `int[]` arrays of the same capacity (4, doubling together) and one `top`: `values` holds the stack, and `mins[i]` holds the smallest of `values[0]` to `values[i]`. So `push` stores `Math.min(value, mins[top - 1])` (or just `value` when empty), and `min()` reads `mins[top - 1]`. Methods: `push`, `pop`, `min` and `size`; `pop` and `min` throw `java.util.EmptyStackException` when empty. `MinTester` pushes 5, 3, 7 and 2, then prints `min()`, pops, and prints `min()` again, all on one line.",
         {"MinStack.java": """import java.util.EmptyStackException;

public class MinStack {
    private int[] values = new int[4];
    private int[] mins = new int[4];
    private int top = 0;

    public void push(int value) {
        if (top == values.length) {
            int[] biggerValues = new int[values.length * 2];
            int[] biggerMins = new int[mins.length * 2];
            for (int i = 0; i < top; i++) {
                biggerValues[i] = values[i];
                biggerMins[i] = mins[i];
            }
            values = biggerValues;
            mins = biggerMins;
        }
        values[top] = value;
        if (top == 0) {
            mins[top] = value;
        } else {
            mins[top] = Math.min(value, mins[top - 1]);
        }
        top++;
    }

    public int pop() {
        if (top == 0) {
            throw new EmptyStackException();
        }
        top--;
        return values[top];
    }

    public int min() {
        if (top == 0) {
            throw new EmptyStackException();
        }
        return mins[top - 1];
    }

    public int size() {
        return top;
    }
}
""", "MinTester.java": """public class MinTester {
    public static void main(String[] args) {
        MinStack s = new MinStack();
        s.push(5);
        s.push(3);
        s.push(7);
        s.push(2);
        String line = s.min() + " ";
        s.pop();
        line += s.min();
        System.out.println(line);
    }
}
"""}, "MinTester", "2 3",
         tests={"CheckMin.java": """public class CheckMin {
    public static void main(String[] args) {
        MinStack s = new MinStack();
        int[] data = {9, 8, 10, 4, 6, 1, 12};
        for (int v : data) {
            s.push(v);
        }
        String out = "";
        while (s.size() > 0) {
            out += s.min() + " ";
            s.pop();
        }
        System.out.println(out.trim());
    }
}
"""}, tests_run="CheckMin", tests_output="1 1 4 4 8 8 9",
         checks=[{"pattern": r"mins\[top - 1\]|mins\[top-1\]", "message": "`min()` should read the saved minimum, `mins[top - 1]`, rather than searching."}]),
    [ALGS4_13, OPENDSA_STACK, EMPTYSTACK_API, GENERICS_TUT],
)
