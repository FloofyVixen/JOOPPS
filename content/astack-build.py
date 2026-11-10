from sources import ALGS4_13, OPENDSA_STACK, EMPTYSTACK_API, GENERICS_TUT
from ds_code import STACK_ADT, ARRAY_STACK, STACK_FILES, main_class, lines

HIDE = ["StackADT.java", "ArrayStack.java"]


def prog(name, *stmts, t="Integer"):
    return main_class(name, lines(f"ArrayStack<{t}> s = new ArrayStack<>();", *stmts))


EMPTY = prog("Empty", "System.out.println(s.arrayString());")
PUSHED = prog("Pushed", "s.push(5);", "s.push(8);", "System.out.println(s.arrayString());")
POPPED = prog("Popped", "s.push(5);", "s.push(8);", "System.out.println(s.pop());", "System.out.println(s.arrayString());")
FULL = prog("Full", "for (int i = 1; i <= 5; i++) {", "    s.push(i * 10);", "}", "System.out.println(s.arrayString());")
DEMO = main_class("StackTester", lines(
    'StackADT<String> s = new ArrayStack<>();',
    'for (String word : new String[] {"a", "b", "c", "d", "e"}) {',
    '    s.push(word);',
    '}',
    'System.out.println(s + " size " + s.size());',
    'System.out.println(s.pop() + s.pop());',
    'System.out.println(s.peek() + " " + s);',
))
T1 = prog("ArrayTrace", "s.push(3);", "s.push(6);", "s.push(9);", "s.pop();", "s.push(1);", "s.pop();", "System.out.println(s.arrayString());")
T2 = prog("GrowTrace", "s.push(1);", "s.push(2);", "s.push(3);", "s.push(4);", "s.pop();", "s.push(5);", "s.push(6);", "System.out.println(s.arrayString());")

BLANK_STACK = ARRAY_STACK.replace("""        stack[top] = element;
        top++;""", """        [[store]];
        [[inc]];""").replace("""        top--;
        T result = (T) stack[top];
        stack[top] = null;""", """        [[dec]];
        T result = (T) stack[top];
        stack[top] = null;""").replace("""        return (T) stack[top - 1];""", """        return (T) stack[[[peekat]]];""")

LESSON = {
    "id": "astack-build",
    "title": "ArrayStack: the top at the end",
    "summary": "Build the stack you've been using. An array holds the values from the bottom up, and one int, `top`, tells you where the next value goes.",
    "goals": [
        "Store a stack in an array with the bottom at index 0",
        "Use `top` as both the count and the next free index",
        "Write `push`, `pop` and `peek`, and grow the array when it's full",
        "Draw the array behind a stack after a sequence of operations",
    ],
    "cos225": "The Exam 2 guide asks you to diagram an array as a stack and to say where the top is. Here the top is at the end of the used part of the array; the next lesson tries the other end.",
    "blocks": [
        {"type": "h", "text": "Two fields"},
        {"type": "p", "text": "An `ArrayStack` needs an array for the values and one `int`, `top`. The bottom of the stack is index 0, and values fill the array upward. `top` counts the values, which also makes it the index of the **next free slot**: with 2 values in slots 0 and 1, `top` is 2."},
        {"type": "p", "text": "An empty stack with room for four. The arrow shows where `top` points:"},
        {"type": "diagram", "kind": "array", "state": "[_, _, _, _] top=0",
         "files": {**STACK_FILES, "Empty.java": EMPTY}, "run": "Empty"},
        {"type": "p", "text": "The array is an `Object[]`, as in the generics lesson, because Java can't create a `T[]`. `pop` and `peek` cast values back to `T`."},

        {"type": "h", "text": "push"},
        {"type": "p", "text": "Store the value at `stack[top]`, then add 1 to `top`. Nothing else moves, so `push` takes the same time however big the stack is."},
        {"type": "snippet", "code": """        stack[top] = element;
        top++;"""},
        {"type": "diagram", "kind": "array", "state": "[5, 8, _, _] top=2",
         "files": {**STACK_FILES, "Pushed.java": PUSHED}, "run": "Pushed",
         "caption": "After `push(5)` and `push(8)`. The top value, 8, is at index `top - 1`."},

        {"type": "h", "text": "pop and peek"},
        {"type": "p", "text": "`pop` goes the other way: subtract 1 from `top`, so it points at the top value, take that value, and clear the slot. `peek` reads `stack[top - 1]` without changing anything. Both throw `EmptyStackException` when `top` is 0."},
        {"type": "snippet", "code": """        top--;
        T result = (T) stack[top];
        stack[top] = null;
        return result;"""},
        {"type": "diagram", "kind": "array", "state": "[5, _, _, _] top=1",
         "files": {**STACK_FILES, "Popped.java": POPPED}, "run": "Popped", "line": 1,
         "caption": "After one `pop()`, which returned 8."},
        {"type": "p", "text": "Setting the slot to `null` isn't strictly needed: `top` already says the slot is free, and the next `push` overwrites it. But leaving the old reference there would keep that object in memory for as long as the stack exists, so clearing it is good practice (Princeton's *Algorithms* calls this avoiding loitering)."},

        {"type": "h", "text": "When the array is full"},
        {"type": "p", "text": "When `top` equals the array's length, there's no free slot. `push` first calls `expandCapacity`, which makes an array twice as big and copies the values across, exactly like the growable list in unit 12:"},
        {"type": "diagram", "kind": "array", "state": "[10, 20, 30, 40, 50, _, _, _] top=5",
         "files": {**STACK_FILES, "Full.java": FULL}, "run": "Full",
         "caption": "Five pushes into a stack that started with four slots."},

        {"type": "h", "text": "The whole class"},
        {"type": "code", "files": {"StackADT.java": STACK_ADT, "ArrayStack.java": ARRAY_STACK, "StackTester.java": DEMO},
         "run": "StackTester", "hide": ["StackADT.java"]},
        {"type": "list", "items": [
            "`toString` and `arrayString` are only for printing. `toString` shows the stack (bottom to top); `arrayString` shows every slot of the array, which is what you draw on the exam.",
            "`s.pop() + s.pop()` with strings joins them: `e` then `d`, so it prints `ed`.",
        ]},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "astack-trace1", "kind": "array",
         "prompt": "Each `pop` clears the slot it takes from. Trace the array, not just the stack.",
         "files": {**STACK_FILES, "ArrayTrace.java": T1}, "run": "ArrayTrace", "hide": HIDE,
         "question": "Which diagram shows the array at the end?",
         "choices": ["[3, 6, 1, _] top=3", "[3, 6, _, _] top=2", "[3, 6, _, _] top=3", "[3, _, _, _] top=1"],
         "answer": 1,
         "explain": "After 3, 6, 9 and a pop, the array is `[3, 6, _, _]`. Pushing 1 fills index 2; popping it clears index 2 again. `top` is 2, the next free slot."},
        {"type": "trace", "id": "astack-trace2", "kind": "array",
         "prompt": "The array starts with four slots. Watch for the moment it fills up.",
         "files": {**STACK_FILES, "GrowTrace.java": T2}, "run": "GrowTrace", "hide": HIDE,
         "question": "Which diagram shows the array at the end?",
         "choices": ["[1, 2, 3, 5, 6, _, _, _] top=5", "[1, 2, 3, 4, 5, 6, _, _] top=6", "[1, 2, 3, 5] top=4", "[1, 2, 3, 5, 6] top=5"],
         "answer": 0,
         "explain": "Four pushes fill the array, but the `pop` frees index 3 before it ever has to grow. `push(5)` reuses index 3. Only `push(6)` finds the array full, so the array doubles to 8 and 6 goes in index 4."},
        {"type": "blanks", "id": "astack-blanks", "title": "Write the core of ArrayStack",
         "prompt": "Fill in the four blanks.",
         "files": {"StackADT.java": STACK_ADT, "ArrayStack.java": BLANK_STACK, "StackTester.java": DEMO},
         "hide": ["StackADT.java"], "run": "StackTester",
         "output": "bottom [a, b, c, d, e] top size 5\ned\nc bottom [a, b, c] top",
         "blanks": {
             "store": {"accept": ["stack[top] = element"], "hint": "`top` is the next free slot.",
                       "wrong": [{"answer": "stack[top + 1] = element", "why": "That skips a slot: the first push lands in index 1, and on a full array it runs past the end."}]},
             "inc": {"accept": ["top++", "top += 1", "top = top + 1"], "hint": "One more value.",
                     "wrong": [{"answer": "top--", "why": "`top` must grow with each push. Going down, the next push writes to index -1 and crashes."}]},
             "dec": {"accept": ["top--", "top -= 1", "top = top - 1"], "hint": "Move `top` back to the last filled slot.",
                     "wrong": [{"answer": "top++", "why": "That moves away from the values: it reads an empty slot and returns `null`."}]},
             "peekat": {"accept": ["top - 1"], "hint": "The top value is just below the next free slot.",
                        "wrong": [{"answer": "top", "why": "`stack[top]` is the next free slot, which is empty, so `peek` returns `null`."}]},
         },
         "explain": "`top` is the next free slot, so push stores at `top` and then moves it up, and pop moves it down first. The top value lives at `top - 1`."},
        {"type": "quiz", "id": "astack-where",
         "question": "An `ArrayStack` has `top` equal to 3. Which index holds the value `peek()` returns?",
         "choices": ["0", "2", "3", "4"],
         "answer": 1,
         "explain": "`top` counts the values (3, in indexes 0, 1 and 2) and is the next free slot. The top value is at `top - 1`, index 2."},
    ],
    "sources": [ALGS4_13, OPENDSA_STACK, EMPTYSTACK_API, GENERICS_TUT],
}
