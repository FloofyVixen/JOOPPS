from sources import ALGS4_13, OPENDSA_STACK, ALGS4_14
from ds_code import STACK_ADT, ARRAY_STACK, STACK_FILES, main_class, lines

FRONT = """import java.util.EmptyStackException;

public class FrontArrayStack<T> implements StackADT<T> {
    private Object[] stack;
    private int count;

    public FrontArrayStack() {
        stack = new Object[4];
        count = 0;
    }

    @Override
    public void push(T element) {
        if (count == stack.length) {
            expandCapacity();
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

    private void expandCapacity() {
        Object[] bigger = new Object[stack.length * 2];
        for (int i = 0; i < count; i++) {
            bigger[i] = stack[i];
        }
        stack = bigger;
    }

    // Every slot of the array, for drawing it: _ marks an empty slot.
    public String arrayString() {
        String result = "[";
        for (int i = 0; i < stack.length; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += (stack[i] == null) ? "_" : stack[i];
        }
        return result + "] top=0";
    }
}
"""
FFILES = {"StackADT.java": STACK_ADT, "FrontArrayStack.java": FRONT}
BOTH = main_class("BothEnds", lines(
    'ArrayStack<Integer> atEnd = new ArrayStack<>();',
    'FrontArrayStack<Integer> atFront = new FrontArrayStack<>();',
    'for (int value : new int[] {5, 8, 2}) {',
    '    atEnd.push(value);',
    '    atFront.push(value);',
    '}',
    'System.out.println(atEnd.arrayString());',
    'System.out.println(atFront.arrayString());',
    'System.out.println(atEnd.pop() + " " + atFront.pop());',
))
MOVES = """public class MoveCount {
    // With the top at index 0, each push shifts every value already
    // in the stack one slot right. Count those moves for n pushes.
    public static long movesForPushes(int n) {
        long moves = 0;
        for (int count = 0; count < n; count++) {
            for (int i = count; i > 0; i--) {
                moves++;
            }
        }
        return moves;
    }

    public static void main(String[] args) {
        for (int n = 10; n <= 10000; n *= 10) {
            System.out.println(n + " pushes: " + movesForPushes(n) + " values moved");
        }
    }
}
"""
TF = main_class("FrontTrace", lines(
    'FrontArrayStack<String> s = new FrontArrayStack<>();',
    's.push("p");',
    's.push("q");',
    's.push("r");',
    's.pop();',
    's.push("t");',
    'System.out.println(s.arrayString());',
))

LESSON = {
    "id": "astack-top",
    "title": "Where the top goes: end versus front",
    "summary": "An array stack could keep its top at index 0 instead of at the end. It works, but every push and pop has to shift the whole array. Here's why the end is the right choice.",
    "goals": [
        "Implement a stack with its top at index 0",
        "Count the values each operation has to move",
        "Explain why an array stack keeps its top at the end",
    ],
    "cos225": "The Exam 2 guide asks you to contrast stack implementations and say where the top is located. For arrays, the answer is the end of the used part, and this lesson shows the cost of the alternative.",
    "blocks": [
        {"type": "h", "text": "The other end"},
        {"type": "p", "text": "Nothing says the top has to be at the end of the array. Here is a stack that keeps its top at index 0. To make room for a new top, `push` first shifts every value one slot to the right; `pop` shifts them all back left."},
        {"type": "code", "files": FFILES, "show": False},
        {"type": "p", "text": "Both classes behave the same as stacks, but their arrays look like mirror images:"},
        {"type": "code", "files": {**STACK_FILES, **FFILES, "BothEnds.java": BOTH}, "run": "BothEnds",
         "hide": ["StackADT.java", "ArrayStack.java", "FrontArrayStack.java"]},
        {"type": "diagram", "kind": "array", "state": "[5, 8, 2, _] top=3",
         "files": {**STACK_FILES, **FFILES, "BothEnds.java": BOTH}, "run": "BothEnds", "line": 0,
         "caption": "`ArrayStack` after pushing 5, 8 and 2: the top value is at index `top - 1`."},
        {"type": "diagram", "kind": "array", "state": "[2, 8, 5, _] top=0",
         "files": {**STACK_FILES, **FFILES, "BothEnds.java": BOTH}, "run": "BothEnds", "line": 1,
         "caption": "`FrontArrayStack` after the same pushes: the top value is always at index 0."},

        {"type": "h", "text": "Counting the work"},
        {"type": "p", "text": "With the top at the end, a push writes one slot and moves nothing, however many pushes you do. With the top at the front, a push into a stack of `count` values moves all `count` of them first. This program counts those moves for `n` pushes in a row:"},
        {"type": "code", "files": {"MoveCount.java": MOVES}, "run": "MoveCount"},
        {"type": "p", "text": "Ten times more pushes means about a hundred times more moves, because each push costs more than the one before. For a single operation, the difference is:"},
        {"type": "list", "items": [
            "**Top at the end**: `push`, `pop` and `peek` take the same time at any size. This is called **constant time**, written **O(1)**.",
            "**Top at the front**: `push` and `pop` move every value, so their time grows in step with the size. This is **linear time**, written **O(n)**. (`peek` is still O(1): it only reads index 0.)",
        ]},
        {"type": "p", "text": "Unit 15 covers this notation properly. For now: an array stack keeps its top at the end, because that's the end where adding and removing don't disturb anything else."},
        {"type": "note", "label": "What about growing?", "text": "A `push` that finds the array full copies every value into the bigger array, so that one push is O(n). Because the capacity doubles, this happens rarely, and spread over all the pushes it adds only a constant amount of work to each (Princeton's *Algorithms* shows this in section 1.4)."},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "atop-trace", "kind": "array",
         "prompt": "This stack keeps its top at index 0.",
         "files": {**FFILES, "FrontTrace.java": TF}, "run": "FrontTrace", "hide": ["StackADT.java", "FrontArrayStack.java"],
         "question": "Which diagram shows the array at the end?",
         "choices": ["[p, q, t, _] top=0", "[t, q, p, _] top=0", "[t, r, q, p] top=0", "[q, p, t, _] top=0"],
         "answer": 1,
         "explain": "After p, q and r, the array is `[r, q, p, _]`. `pop` removes `r` from index 0 and shifts the rest left: `[q, p, _, _]`. Pushing `t` shifts them right again and puts `t` at index 0."},
        {"type": "match", "id": "atop-match",
         "prompt": "Match each operation with how its time grows as the stack holds more values. Assume the array isn't full.",
         "options": ["O(1): the same at any size", "O(n): grows with the size"],
         "items": [
             {"text": "`push` with the top at the end", "answer": "O(1): the same at any size"},
             {"text": "`pop` with the top at the end", "answer": "O(1): the same at any size"},
             {"text": "`push` with the top at index 0", "answer": "O(n): grows with the size",
              "why": "Every existing value shifts one slot right first."},
             {"text": "`pop` with the top at index 0", "answer": "O(n): grows with the size",
              "why": "Every remaining value shifts one slot left."},
             {"text": "`peek` with the top at index 0", "answer": "O(1): the same at any size",
              "why": "`peek` only reads `stack[0]`. Nothing moves."},
             {"text": "A `push` that finds the array full and expands it", "answer": "O(n): grows with the size",
              "why": "That one push copies every value into the new array."},
         ],
         "explain": "Adding or removing at the end of an array touches one slot. Adding or removing at the front moves everything after it."},
        {"type": "quiz", "id": "atop-why",
         "question": "Why does `ArrayStack` keep its top at the end of the used part of the array?",
         "choices": ["Because index 0 can't hold a value", "So push and pop don't have to shift the other values", "So the array never has to grow", "Because `peek` would be slower at index 0"],
         "answer": 1,
         "explain": "At the end, push and pop change one slot and `top`. At index 0 they shift every value. `peek` is fast either way, and the array still grows when full."},
    ],
    "sources": [ALGS4_13, ALGS4_14, OPENDSA_STACK],
}
