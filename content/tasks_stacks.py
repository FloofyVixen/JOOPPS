"""Write-it-yourself tasks for unit 13, Arrays and Stacks. Compiled and run by build.py."""
from tasks_classes import task
from ds_code import STACK_FILES


def given(t, files):
    """Files the learner starts with (already in the editor), e.g. the stack class."""
    t["solution"] = {**files, **t["solution"]}
    t["files"] = list(t["solution"])
    t["starter"] = dict(files)
    return t


GIVEN_NOTE = "`StackADT` and `ArrayStack` are already in the editor."

LIFO = [
    given(task("w-stack-countdown", "Pop them all",
         "Write `Countdown`. Its `main` pushes the strings `one`, `two`, `three` and `four` onto an `ArrayStack<String>`, then pops until the stack is empty, printing each value on its own line. " + GIVEN_NOTE,
         {"Countdown.java": """public class Countdown {
    public static void main(String[] args) {
        StackADT<String> words = new ArrayStack<>();
        words.push("one");
        words.push("two");
        words.push("three");
        words.push("four");
        while (!words.isEmpty()) {
            System.out.println(words.pop());
        }
    }
}
"""}, "Countdown", "four\nthree\ntwo\none",
         checks=[{"pattern": r"\.pop\(\)", "message": "Use `pop()` to take the values off the stack."},
                 {"pattern": r"isEmpty\(\)", "message": "Loop until `isEmpty()` is true, rather than counting to 4."}]), STACK_FILES),

    given(task("w-stack-toporsentinel", "A safe peek",
         "Write `SafeTop` with a method `public static String topOrNone(StackADT<String> s)` that returns the top value without removing it, or `\"none\"` if the stack is empty. `main` prints `topOrNone` of an empty stack, then pushes `a` and `b` and prints it again, then prints the stack's size. " + GIVEN_NOTE,
         {"SafeTop.java": """public class SafeTop {
    public static String topOrNone(StackADT<String> s) {
        if (s.isEmpty()) {
            return "none";
        }
        return s.peek();
    }

    public static void main(String[] args) {
        StackADT<String> s = new ArrayStack<>();
        System.out.println(topOrNone(s));
        s.push("a");
        s.push("b");
        System.out.println(topOrNone(s));
        System.out.println(s.size());
    }
}
"""}, "SafeTop", "none\nb\n2",
         tests={"CheckSafeTop.java": """public class CheckSafeTop {
    public static void main(String[] args) {
        StackADT<String> s = new ArrayStack<>();
        s.push("x");
        System.out.println(SafeTop.topOrNone(s) + " " + s.size());
        s.pop();
        System.out.println(SafeTop.topOrNone(s));
    }
}
"""}, tests_run="CheckSafeTop", tests_output="x 1\nnone",
         hints=["Check `isEmpty()` first. If you use `pop`, the size check in the test will catch it."]), STACK_FILES),

    given(task("w-stack-sum", "Add up a stack",
         "Write `StackSum` with `public static int sumAndEmpty(StackADT<Integer> s)`, which pops every value, adds them up and returns the total (the stack ends up empty). `main` pushes 3, 1, 4, 1 and 5, then prints `sum 14, empty true`. " + GIVEN_NOTE,
         {"StackSum.java": """public class StackSum {
    public static int sumAndEmpty(StackADT<Integer> s) {
        int total = 0;
        while (!s.isEmpty()) {
            total += s.pop();
        }
        return total;
    }

    public static void main(String[] args) {
        StackADT<Integer> s = new ArrayStack<>();
        s.push(3);
        s.push(1);
        s.push(4);
        s.push(1);
        s.push(5);
        int sum = sumAndEmpty(s);
        System.out.println("sum " + sum + ", empty " + s.isEmpty());
    }
}
"""}, "StackSum", "sum 14, empty true",
         tests={"CheckSum.java": """public class CheckSum {
    public static void main(String[] args) {
        StackADT<Integer> s = new ArrayStack<>();
        System.out.println(StackSum.sumAndEmpty(s));
        s.push(-2);
        s.push(10);
        System.out.println(StackSum.sumAndEmpty(s) + " " + s.size());
    }
}
"""}, tests_run="CheckSum", tests_output="0\n8 0"), STACK_FILES),
]

TRACE = [
    given(task("w-stack-addtop", "Combine the top two",
         "Write `TopTwo` with `public static void addTopTwo(StackADT<Integer> s)`: pop two values and push their sum, so the stack shrinks by one. `main` pushes 6, 2 and 5, calls `addTopTwo` once and prints the stack. " + GIVEN_NOTE,
         {"TopTwo.java": """public class TopTwo {
    public static void addTopTwo(StackADT<Integer> s) {
        int first = s.pop();
        int second = s.pop();
        s.push(first + second);
    }

    public static void main(String[] args) {
        StackADT<Integer> s = new ArrayStack<>();
        s.push(6);
        s.push(2);
        s.push(5);
        addTopTwo(s);
        System.out.println(s);
    }
}
"""}, "TopTwo", "bottom [6, 7] top",
         tests={"CheckTopTwo.java": """public class CheckTopTwo {
    public static void main(String[] args) {
        StackADT<Integer> s = new ArrayStack<>();
        s.push(1);
        s.push(2);
        s.push(3);
        s.push(4);
        TopTwo.addTopTwo(s);
        TopTwo.addTopTwo(s);
        System.out.println(s);
    }
}
"""}, tests_run="CheckTopTwo", tests_output="bottom [1, 9] top"), STACK_FILES),

    given(task("w-stack-under", "Look under the top",
         "Write `Under` with `public static int underTop(StackADT<Integer> s)`, which returns the value just below the top **and leaves the stack exactly as it was**. Pop the top, peek, then push the top back. `main` pushes 8, 3 and 5, prints `underTop`, then prints the stack. " + GIVEN_NOTE,
         {"Under.java": """public class Under {
    public static int underTop(StackADT<Integer> s) {
        int top = s.pop();
        int below = s.peek();
        s.push(top);
        return below;
    }

    public static void main(String[] args) {
        StackADT<Integer> s = new ArrayStack<>();
        s.push(8);
        s.push(3);
        s.push(5);
        System.out.println(underTop(s));
        System.out.println(s);
    }
}
"""}, "Under", "3\nbottom [8, 3, 5] top",
         tests={"CheckUnder.java": """public class CheckUnder {
    public static void main(String[] args) {
        StackADT<Integer> s = new ArrayStack<>();
        s.push(1);
        s.push(2);
        System.out.println(Under.underTop(s) + " " + s.peek() + " " + s.size());
    }
}
"""}, tests_run="CheckUnder", tests_output="1 2 2"), STACK_FILES),

    given(task("w-stack-transfer", "Move one stack onto another",
         "Write `Transfer` with `public static void moveAll(StackADT<String> from, StackADT<String> to)`, which pops every value from `from` and pushes it onto `to`. `main` pushes `a`, `b`, `c` onto one stack, moves them all onto an empty second stack, and prints both stacks. Notice the order flips. " + GIVEN_NOTE,
         {"Transfer.java": """public class Transfer {
    public static void moveAll(StackADT<String> from, StackADT<String> to) {
        while (!from.isEmpty()) {
            to.push(from.pop());
        }
    }

    public static void main(String[] args) {
        StackADT<String> first = new ArrayStack<>();
        StackADT<String> second = new ArrayStack<>();
        first.push("a");
        first.push("b");
        first.push("c");
        moveAll(first, second);
        System.out.println(first);
        System.out.println(second);
    }
}
"""}, "Transfer", "bottom [] top\nbottom [c, b, a] top",
         tests={"CheckTransfer.java": """public class CheckTransfer {
    public static void main(String[] args) {
        StackADT<String> x = new ArrayStack<>();
        StackADT<String> y = new ArrayStack<>();
        y.push("base");
        x.push("1");
        x.push("2");
        Transfer.moveAll(x, y);
        System.out.println(y);
    }
}
"""}, tests_run="CheckTransfer", tests_output="bottom [base, 2, 1] top"), STACK_FILES),
]

USE = [
    task("w-deque-reverse-words", "Reverse a sentence",
         "Write `ReverseWords` with `public static String reverseWords(String sentence)`, which returns the words in reverse order, separated by single spaces. Split with `sentence.split(\" \")`, push each word onto a `Deque<String>`, then pop them into the result. `main` prints `reverseWords(\"to be or not\")`.",
         {"ReverseWords.java": """import java.util.ArrayDeque;
import java.util.Deque;

public class ReverseWords {
    public static String reverseWords(String sentence) {
        Deque<String> stack = new ArrayDeque<>();
        for (String word : sentence.split(" ")) {
            stack.push(word);
        }
        String result = stack.pop();
        while (!stack.isEmpty()) {
            result += " " + stack.pop();
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(reverseWords("to be or not"));
    }
}
"""}, "ReverseWords", "not or be to",
         tests={"CheckWords.java": """public class CheckWords {
    public static void main(String[] args) {
        System.out.println("[" + ReverseWords.reverseWords("one") + "]");
        System.out.println("[" + ReverseWords.reverseWords("a b c") + "]");
    }
}
"""}, tests_run="CheckWords", tests_output="[one]\n[c b a]",
         checks=[{"pattern": r"Deque<String>", "message": "Use a `Deque<String>` as the stack."}],
         hints=["Popping the first word before the loop avoids an extra space at the start or end."]),

    task("w-deque-curly", "Check curly braces too",
         "Write `Balance` with `public static boolean isBalanced(String code)` that checks `()`, `[]` **and** `{}`, using a `Deque<Character>`. `main` prints the result for `{ a[0] = (1); }`, `{ ( }` and `}{`.",
         {"Balance.java": """import java.util.ArrayDeque;
import java.util.Deque;

public class Balance {
    public static boolean isBalanced(String code) {
        Deque<Character> open = new ArrayDeque<>();
        for (int i = 0; i < code.length(); i++) {
            char c = code.charAt(i);
            if (c == '(' || c == '[' || c == '{') {
                open.push(c);
            } else if (c == ')' || c == ']' || c == '}') {
                if (open.isEmpty()) {
                    return false;
                }
                char last = open.pop();
                if (c == ')' && last != '(') {
                    return false;
                }
                if (c == ']' && last != '[') {
                    return false;
                }
                if (c == '}' && last != '{') {
                    return false;
                }
            }
        }
        return open.isEmpty();
    }

    public static void main(String[] args) {
        System.out.println(isBalanced("{ a[0] = (1); }"));
        System.out.println(isBalanced("{ ( }"));
        System.out.println(isBalanced("}{"));
    }
}
"""}, "Balance", "true\nfalse\nfalse",
         tests={"CheckBalance.java": """public class CheckBalance {
    public static void main(String[] args) {
        System.out.println(Balance.isBalanced(""));
        System.out.println(Balance.isBalanced("{[()]}"));
        System.out.println(Balance.isBalanced("{[(])}"));
        System.out.println(Balance.isBalanced("(("));
    }
}
"""}, tests_run="CheckBalance", tests_output="true\ntrue\nfalse\nfalse"),

    task("w-deque-undo", "An undo button",
         "Write `Editor` with a private `String text` (starting empty), a private `Deque<String>` of earlier versions, and three methods: `type(String s)` saves the current text on the stack, then adds `s` to the end; `undo()` restores the most recent saved version, or does nothing if there is none; `getText()` returns the text. `EditorTester` (write it too) types `Hello`, `, world` and `!`, undoes twice, and prints the text after each step.",
         {"Editor.java": """import java.util.ArrayDeque;
import java.util.Deque;

public class Editor {
    private String text = "";
    private Deque<String> history = new ArrayDeque<>();

    public void type(String s) {
        history.push(text);
        text = text + s;
    }

    public void undo() {
        if (!history.isEmpty()) {
            text = history.pop();
        }
    }

    public String getText() {
        return text;
    }
}
""", "EditorTester.java": """public class EditorTester {
    public static void main(String[] args) {
        Editor e = new Editor();
        e.type("Hello");
        System.out.println(e.getText());
        e.type(", world");
        System.out.println(e.getText());
        e.type("!");
        System.out.println(e.getText());
        e.undo();
        System.out.println(e.getText());
        e.undo();
        System.out.println(e.getText());
    }
}
"""}, "EditorTester", "Hello\nHello, world\nHello, world!\nHello, world\nHello",
         tests={"CheckEditor.java": """public class CheckEditor {
    public static void main(String[] args) {
        Editor e = new Editor();
        e.undo();
        System.out.println("[" + e.getText() + "]");
        e.type("a");
        e.undo();
        e.undo();
        System.out.println("[" + e.getText() + "]");
    }
}
"""}, tests_run="CheckEditor", tests_output="[]\n[]"),
]

TASKS = {"stack-lifo": LIFO, "stack-trace": TRACE, "stack-use": USE}
