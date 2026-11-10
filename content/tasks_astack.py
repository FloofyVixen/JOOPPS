"""Write-it-yourself tasks for unit 14, Array Stack implementations. Compiled and run by build.py."""
from tasks_classes import task
from tasks_stacks import given
from ds_code import STACK_ADT

INTSTACK = """import java.util.EmptyStackException;

public class IntStack {
    private int[] stack;
    private int top;

    public IntStack() {
        stack = new int[4];
        top = 0;
    }

    public void push(int value) {
        if (top == stack.length) {
            int[] bigger = new int[stack.length * 2];
            for (int i = 0; i < top; i++) {
                bigger[i] = stack[i];
            }
            stack = bigger;
        }
        stack[top] = value;
        top++;
    }

    public int pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        top--;
        return stack[top];
    }

    public int peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return stack[top - 1];
    }

    public boolean isEmpty() {
        return top == 0;
    }

    public int size() {
        return top;
    }
}
"""

BUILD = [
    task("w-intstack", "A stack of ints",
         "Write `IntStack`, an array stack of `int` values (no generics needed). Use a private `int[]` that starts with 4 slots and doubles when full, and a private `int top`. Methods: `push(int)`, `pop()`, `peek()` (both throw `java.util.EmptyStackException` when empty), `isEmpty()` and `size()`. `IntStackTester` pushes 1 to 6, prints `size()` and `peek()`, then pops everything onto one line separated by spaces.",
         {"IntStack.java": INTSTACK, "IntStackTester.java": """public class IntStackTester {
    public static void main(String[] args) {
        IntStack s = new IntStack();
        for (int i = 1; i <= 6; i++) {
            s.push(i);
        }
        System.out.println(s.size() + " " + s.peek());
        while (!s.isEmpty()) {
            System.out.print(s.pop() + " ");
        }
        System.out.println();
    }
}
"""}, "IntStackTester", "6 6\n6 5 4 3 2 1",
         tests={"CheckIntStack.java": """import java.util.EmptyStackException;

public class CheckIntStack {
    public static void main(String[] args) {
        IntStack s = new IntStack();
        for (int i = 0; i < 20; i++) {
            s.push(i * i);
        }
        System.out.println(s.pop() + " " + s.size());
        IntStack e = new IntStack();
        try {
            e.peek();
            System.out.println("no exception");
        } catch (EmptyStackException ex) {
            System.out.println("EmptyStackException");
        }
    }
}
"""}, tests_run="CheckIntStack", tests_output="361 19\nEmptyStackException",
         hints=["`top` is the next free index: push stores at `stack[top]` then increments; pop decrements first."]),

    given(task("w-boundedstack", "A stack with a size limit",
         "Write `BoundedStack<T>`, which implements `StackADT<T>` (already in the editor) with an `Object[]` whose capacity comes from the constructor and **never grows**. Add `isFull()`. `push` on a full stack throws `new IllegalStateException(\"stack is full\")`; `pop` and `peek` on an empty one throw `EmptyStackException`. `BoundedTester` makes a stack of capacity 2, pushes `x` and `y`, prints `isFull()`, then tries to push `z` and prints the exception's message.",
         {"BoundedStack.java": """import java.util.EmptyStackException;

public class BoundedStack<T> implements StackADT<T> {
    private Object[] stack;
    private int top;

    public BoundedStack(int capacity) {
        stack = new Object[capacity];
        top = 0;
    }

    public boolean isFull() {
        return top == stack.length;
    }

    @Override
    public void push(T element) {
        if (isFull()) {
            throw new IllegalStateException("stack is full");
        }
        stack[top] = element;
        top++;
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

    @SuppressWarnings("unchecked")
    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return (T) stack[top - 1];
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
""", "BoundedTester.java": """public class BoundedTester {
    public static void main(String[] args) {
        BoundedStack<String> s = new BoundedStack<>(2);
        s.push("x");
        s.push("y");
        System.out.println(s.isFull());
        try {
            s.push("z");
        } catch (IllegalStateException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""}, "BoundedTester", "true\nstack is full",
         tests={"CheckBounded.java": """public class CheckBounded {
    public static void main(String[] args) {
        BoundedStack<Integer> s = new BoundedStack<>(3);
        s.push(1);
        s.push(2);
        s.pop();
        s.push(3);
        s.push(4);
        System.out.println(s.isFull() + " " + s.peek() + " " + s.size());
        s.pop();
        System.out.println(s.isFull());
    }
}
"""}, tests_run="CheckBounded", tests_output="true 4 3\nfalse"), {"StackADT.java": STACK_ADT}),
]

TOP = [
    given(task("w-frontstack", "Top at index 0",
         "Write `FrontStack<T>`, which implements `StackADT<T>` (already in the editor) with its top **at index 0**: `push` shifts every value right before storing at index 0, and `pop` shifts them left after taking index 0. Use an `Object[]` of capacity 4 that doubles when full, and a `count`. Its `toString()` returns the usual `bottom [ ... ] top` format, so the bottom is the **last** used index. `FrontTester` pushes 1, 2 and 3, pops once, pushes 4 and prints the stack.",
         {"FrontStack.java": """import java.util.EmptyStackException;

public class FrontStack<T> implements StackADT<T> {
    private Object[] stack = new Object[4];
    private int count = 0;

    @Override
    public void push(T element) {
        if (count == stack.length) {
            Object[] bigger = new Object[stack.length * 2];
            for (int i = 0; i < count; i++) {
                bigger[i] = stack[i];
            }
            stack = bigger;
        }
        for (int i = count; i > 0; i--) {
            stack[i] = stack[i - 1];
        }
        stack[0] = element;
        count++;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T result = (T) stack[0];
        for (int i = 0; i < count - 1; i++) {
            stack[i] = stack[i + 1];
        }
        count--;
        stack[count] = null;
        return result;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return (T) stack[0];
    }

    @Override
    public boolean isEmpty() {
        return count == 0;
    }

    @Override
    public int size() {
        return count;
    }

    @Override
    public String toString() {
        String result = "bottom [";
        for (int i = count - 1; i >= 0; i--) {
            result += stack[i];
            if (i > 0) {
                result += ", ";
            }
        }
        return result + "] top";
    }
}
""", "FrontTester.java": """public class FrontTester {
    public static void main(String[] args) {
        StackADT<Integer> s = new FrontStack<>();
        s.push(1);
        s.push(2);
        s.push(3);
        s.pop();
        s.push(4);
        System.out.println(s);
    }
}
"""}, "FrontTester", "bottom [1, 2, 4] top",
         tests={"CheckFront.java": """public class CheckFront {
    public static void main(String[] args) {
        StackADT<String> s = new FrontStack<>();
        for (int i = 0; i < 9; i++) {
            s.push("v" + i);
        }
        System.out.println(s.pop() + " " + s.peek() + " " + s.size());
        System.out.println(new FrontStack<String>());
    }
}
"""}, tests_run="CheckFront", tests_output="v8 v7 8\nbottom [] top",
         checks=[{"pattern": r"stack\[0\]\s*=", "message": "`push` should store the new value at index 0."}]), {"StackADT.java": STACK_ADT}),

    task("w-peekat", "Look anywhere in an array stack",
         "Because an array stack keeps its values in an array, it can read any of them directly. Write `DeepStack`, an `int` stack like `IntStack` (an `int[]` of 4 that doubles, and `top`), with `push`, `pop`, `size` and one extra method: `peekAt(int depth)`, which returns the value `depth` places below the top (`peekAt(0)` is the top) without changing anything. If `depth` is negative or at least `size()`, throw `new IndexOutOfBoundsException(\"depth \" + depth)`. `DeepTester` pushes 10, 20, 30 and prints `peekAt(0)`, `peekAt(2)` and `size()` on one line.",
         {"DeepStack.java": """import java.util.EmptyStackException;

public class DeepStack {
    private int[] stack = new int[4];
    private int top = 0;

    public void push(int value) {
        if (top == stack.length) {
            int[] bigger = new int[stack.length * 2];
            for (int i = 0; i < top; i++) {
                bigger[i] = stack[i];
            }
            stack = bigger;
        }
        stack[top] = value;
        top++;
    }

    public int pop() {
        if (top == 0) {
            throw new EmptyStackException();
        }
        top--;
        return stack[top];
    }

    public int peekAt(int depth) {
        if (depth < 0 || depth >= top) {
            throw new IndexOutOfBoundsException("depth " + depth);
        }
        return stack[top - 1 - depth];
    }

    public int size() {
        return top;
    }
}
""", "DeepTester.java": """public class DeepTester {
    public static void main(String[] args) {
        DeepStack s = new DeepStack();
        s.push(10);
        s.push(20);
        s.push(30);
        System.out.println(s.peekAt(0) + " " + s.peekAt(2) + " " + s.size());
    }
}
"""}, "DeepTester", "30 10 3",
         tests={"CheckDeep.java": """public class CheckDeep {
    public static void main(String[] args) {
        DeepStack s = new DeepStack();
        for (int i = 1; i <= 6; i++) {
            s.push(i);
        }
        s.pop();
        System.out.println(s.peekAt(1) + " " + s.peekAt(4));
        try {
            s.peekAt(5);
        } catch (IndexOutOfBoundsException e) {
            System.out.println(e.getMessage());
        }
    }
}
"""}, tests_run="CheckDeep", tests_output="4 1\ndepth 5",
         hints=["The top value is at `top - 1`, so the one `depth` below it is at `top - 1 - depth`."]),
]

TASKS = {"astack-build": BUILD, "astack-top": TOP}
