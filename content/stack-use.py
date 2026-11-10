from sources import DEQUE_API, ARRAYDEQUE_API, ALGS4_13, EXCEPTIONS_TUT

DEQ = """import java.util.ArrayDeque;
import java.util.Deque;

public class DequeStack {
    public static void main(String[] args) {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(10);
        stack.push(20);
        stack.push(30);
        System.out.println(stack);
        System.out.println(stack.pop());
        System.out.println(stack.peek());
        System.out.println(stack.size() + " " + stack.isEmpty());
    }
}
"""
EMPTY = """import java.util.ArrayDeque;
import java.util.Deque;

public class EmptyDeque {
    public static void main(String[] args) {
        Deque<String> stack = new ArrayDeque<>();
        System.out.println(stack.peek());
        System.out.println(stack.pop());
    }
}
"""
REVERSE = """import java.util.ArrayDeque;
import java.util.Deque;

public class Reverse {
    public static String reverse(String word) {
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < word.length(); i++) {
            stack.push(word.charAt(i));
        }
        String result = "";
        while (!stack.isEmpty()) {
            result += stack.pop();
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(reverse("stack"));
        System.out.println(reverse("level"));
    }
}
"""
BRACKETS = """import java.util.ArrayDeque;
import java.util.Deque;

public class Brackets {
    public static boolean isBalanced(String text) {
        Deque<Character> open = new ArrayDeque<>();
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c == '(' || c == '[') {
                open.push(c);
            } else if (c == ')' || c == ']') {
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
            }
        }
        return open.isEmpty();
    }

    public static void main(String[] args) {
        System.out.println(isBalanced("a[i] = (b + c) * d[(j)]"));
        System.out.println(isBalanced("(a[0)]"));
        System.out.println(isBalanced("((x)"));
        System.out.println(isBalanced("x)"));
    }
}
"""
CALLS = """public class Calls {
    public static void main(String[] args) {
        first();
    }

    public static void first() {
        second();
    }

    public static void second() {
        int[] numbers = new int[2];
        numbers[5] = 1;
    }
}
"""
BLANKS = BRACKETS.replace("                open.push(c);", "                [[push]];").replace(
    "                if (open.isEmpty()) {\n                    return false;",
    "                if ([[empty]]) {\n                    return false;").replace(
    "        return open.isEmpty();", "        return [[end]];")

LESSON = {
    "id": "stack-use",
    "title": "Using a stack",
    "summary": "Stacks reverse things and match things up. Java has a ready-made stack, and you've been reading one in every crash report.",
    "goals": [
        "Use Java's `Deque` and `ArrayDeque` as a stack",
        "Reverse a sequence with a stack",
        "Check that brackets are balanced with a stack",
        "Read a stack trace as the call stack, most recent call first",
    ],
    "cos225": "The Exam 2 guide asks what stacks are for, and code-writing questions give you the imports and scaffolding. This lesson uses `java.util`'s stack so you can focus on the logic.",
    "blocks": [
        {"type": "h", "text": "Java's own stack"},
        {"type": "p", "text": "You don't have to write a stack class every time. Java's `Deque` interface (pronounced \"deck\") has `push`, `pop` and `peek`, and `ArrayDeque` implements it with an array. The Java documentation recommends `Deque` over the older `Stack` class, so that's what this course uses."},
        {"type": "code", "files": {"DequeStack.java": DEQ}, "run": "DequeStack",
         "after": "When you print an `ArrayDeque` used as a stack, it lists the values **top first**, the reverse of the `bottom [ ... ] top` format this course uses for its own stacks."},
        {"type": "p", "text": "One difference from `ArrayStack`: on an empty `ArrayDeque`, `peek()` returns `null` instead of throwing. `pop()` still throws, but a `NoSuchElementException`:"},
        {"type": "code", "files": {"EmptyDeque.java": EMPTY}, "run": "EmptyDeque", "expect": "runtime",
         "after": "The trace starts inside Java's own code: `pop` calls `removeFirst`, which throws. The last line points at your code, line 8."},

        {"type": "h", "text": "Reversing"},
        {"type": "p", "text": "Push every value, then pop them all, and they come out in the opposite order. That's LIFO at work:"},
        {"type": "code", "files": {"Reverse.java": REVERSE}, "run": "Reverse",
         "after": "`level` reads the same both ways, so reversing it gives `level` again. That's how a palindrome checker works."},

        {"type": "h", "text": "Matching brackets"},
        {"type": "p", "text": "In code, every `(` needs a matching `)`, and pairs can nest but not cross: `([])` is fine, `([)]` is not. A stack checks this in one pass. Push each opening bracket. At each closing bracket, pop and check the popped opening bracket is the right kind. The most recently opened bracket must close first: last in, first out."},
        {"type": "code", "files": {"Brackets.java": BRACKETS}, "run": "Brackets"},
        {"type": "list", "items": [
            "`(a[0)]`: at `)`, the top of the stack is `[`, the wrong kind, so it returns `false`.",
            "`((x)`: every closing bracket matches, but one `(` is still on the stack at the end. That's why the last line checks `open.isEmpty()`.",
            "`x)`: a closing bracket with nothing open. Without the `isEmpty` check, `pop` would throw.",
        ]},

        {"type": "h", "text": "The call stack"},
        {"type": "p", "text": "Java itself uses a stack to keep track of method calls. Calling a method pushes it; returning pops it. When a program crashes, the stack trace lists that **call stack** from the top: the method that was running, then the one that called it, down to `main`."},
        {"type": "code", "files": {"Calls.java": CALLS}, "run": "Calls", "expect": "runtime",
         "after": "`main` called `first`, which called `second`, where the crash happened. The trace prints them top first: `second`, `first`, `main`."},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "use-brackets", "title": "Finish the bracket checker",
         "prompt": "Fill in the three blanks so `isBalanced` works.",
         "files": {"Brackets.java": BLANKS}, "run": "Brackets",
         "output": "true\nfalse\nfalse\nfalse",
         "blanks": {
             "push": {"accept": ["open.push(c)"], "hint": "An opening bracket goes on the stack.",
                      "wrong": [{"answer": "open.pop()", "why": "An opening bracket has to be saved for later, so it's pushed, not popped."}]},
             "empty": {"accept": ["open.isEmpty()", "open.size() == 0"], "hint": "A closing bracket with nothing open is an error.",
                       "wrong": [{"answer": "!open.isEmpty()", "why": "That rejects every closing bracket that does have a match, so even `(b + c)` is unbalanced."}]},
             "end": {"accept": ["open.isEmpty()", "open.size() == 0"], "hint": "At the end, nothing should be left open.",
                     "wrong": [{"answer": "true", "why": "Then `((x)` passes, though one `(` was never closed."}]},
         },
         "explain": "Push openers, pop at each closer, and at the end the stack must be empty."},
        {"type": "quiz", "id": "use-which",
         "question": "Which task is a stack the natural fit for?",
         "choices": ["Serving customers in the order they arrived", "Undoing the most recent edits first", "Finding the largest value in a list", "Printing a list in its original order"],
         "answer": 1,
         "explain": "Undo reverses the most recent change first: last in, first out. Serving customers in arrival order is first in, first out, which is a queue (unit 18)."},
    ],
    "sources": [DEQUE_API, ARRAYDEQUE_API, ALGS4_13, EXCEPTIONS_TUT],
}
