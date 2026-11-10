from sources import ALGS4_13, OPENDSA_STACK, JLS_EVAL_ORDER
from ds_code import STACK_FILES, main_class, lines

HIDE = ["StackADT.java", "ArrayStack.java"]

STEPS = main_class("Steps", lines(
    'StackADT<Integer> s = new ArrayStack<>();',
    's.push(6);',
    's.push(1);',
    'System.out.println(s);',
    's.push(s.pop() + 10);',
    'System.out.println(s);',
    's.push(s.peek() * 2);',
    'System.out.println(s);',
))
PICTURE = main_class("Picture", lines(
    'StackADT<String> s = new ArrayStack<>();',
    's.push("M");',
    's.push("A");',
    's.push("P");',
    's.push("S");',
    'System.out.println(s);',
))
T_SUM = main_class("SumTrace", lines(
    'StackADT<Integer> s = new ArrayStack<>();',
    's.push(3);',
    's.push(5);',
    's.push(2);',
    's.push(s.pop() + s.pop());',
    's.push(4);',
    'System.out.println(s);',
))
T_MOVE = main_class("MoveTrace", lines(
    'StackADT<Character> a = new ArrayStack<>();',
    'StackADT<Character> b = new ArrayStack<>();',
    'a.push(\'x\');',
    'a.push(\'y\');',
    'a.push(\'z\');',
    'b.push(a.pop());',
    'b.push(a.pop());',
    'a.push(b.pop());',
    'System.out.println(a);',
))
P_MIX = main_class("Mix", lines(
    'StackADT<Integer> s = new ArrayStack<>();',
    'for (int i = 1; i <= 4; i++) {',
    '    s.push(i * i);',
    '}',
    'System.out.println(s.pop() - s.pop());',
    'System.out.println(s.peek() + " " + s.size());',
))
BUILD = main_class("BuildIt", lines(
    'StackADT<Integer> s = new ArrayStack<>();',
    's.push(1);',
    's.push(2);',
    's.[[a]];',
    's.push(3);',
    's.[[b]];',
    's.push(4);',
    'System.out.println(s);',
))

LESSON = {
    "id": "stack-trace",
    "title": "Tracing a stack on paper",
    "summary": "Exam questions give you a sequence of stack operations and ask you to draw the result or say what a call returns. Here's a method that works every time.",
    "goals": [
        "Trace push, pop and peek one line at a time, redrawing after each change",
        "Work out what an expression like `s.pop() + s.pop()` does",
        "Answer questions about a drawn stack",
    ],
    "cos225": "These are the Exam 2 guide's \"procedural problems\": interpret changes to a stack, draw it, and answer questions about a drawing.",
    "blocks": [
        {"type": "h", "text": "One line, one drawing"},
        {"type": "p", "text": "To trace stack code, go through it one line at a time. Whenever a line pushes or pops, redraw the stack, and write down any value a `pop` or `peek` returns. Only the top changes, so each new drawing copies the old one with one value added or removed at the top."},
        {"type": "p", "text": "Watch for lines that do two things. `s.push(s.pop() + 10)` first pops the top value, then adds 10, then pushes the result. The stack ends up with the same size but a new value on top:"},
        {"type": "code", "files": {**STACK_FILES, "Steps.java": STEPS}, "run": "Steps", "hide": HIDE},
        {"type": "list", "items": [
            "After the two pushes: 6, then 1 on top.",
            "`s.pop()` returns 1. Adding 10 gives 11, which is pushed back.",
            "`s.peek()` returns 11 without removing it, so `s.push(s.peek() * 2)` adds 22 on top and the stack grows to three values.",
        ]},
        {"type": "diagram", "kind": "stack", "state": "bottom [6, 11, 22] top",
         "files": {**STACK_FILES, "Steps.java": STEPS}, "run": "Steps",
         "caption": "The final stack of `Steps`."},

        {"type": "h", "text": "Two pops in one expression"},
        {"type": "p", "text": "Java evaluates the operands of `+` and `-` from left to right. In `s.pop() - s.pop()`, the left `pop` runs first and gets the top value; the right one gets the value that was underneath. That order matters for `-` and `/`, where swapping the operands changes the answer."},

        {"type": "h", "text": "Questions about a picture"},
        {"type": "p", "text": "Sometimes the exam gives you the drawing and asks about it. Here is a stack built by pushing `M`, `A`, `P` and `S`, in that order:"},
        {"type": "diagram", "kind": "stack", "state": "bottom [M, A, P, S] top",
         "files": {**STACK_FILES, "Picture.java": PICTURE}, "run": "Picture"},
        {"type": "quiz", "id": "trace-picture",
         "question": "For the stack drawn above, what do two calls to `pop()` return, in order?",
         "choices": ["`M`, then `A`", "`S`, then `P`", "`S`, then `S`", "`P`, then `S`"],
         "answer": 1,
         "explain": "`pop` always takes the top. `S` is on top; once it's gone, `P` is on top. (Two `peek` calls would give `S` twice.)"},
        {"type": "quiz", "id": "trace-picture-2",
         "question": "For the same stack, how many `pop` calls does it take before `peek()` returns `A`?",
         "choices": ["1", "2", "3", "4"],
         "answer": 1,
         "explain": "Two values, `S` and `P`, sit above `A`. After popping both, `A` is on top."},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "trace-sum", "kind": "stack",
         "prompt": "Trace the code. Remember that `s.pop() + s.pop()` removes two values.",
         "files": {**STACK_FILES, "SumTrace.java": T_SUM}, "run": "SumTrace", "hide": HIDE,
         "choices": ["bottom [3, 5, 2, 4] top", "bottom [3, 7, 4] top", "bottom [7, 4] top", "bottom [3, 4, 7] top"],
         "answer": 1,
         "explain": "The stack is 3, 5, 2 before line 7. The two pops return 2 and 5, and their sum, 7, is pushed back on top of 3. Then 4 goes on top."},
        {"type": "trace", "id": "trace-move", "kind": "stack",
         "prompt": "Two stacks this time. Which diagram shows stack `a` at the end?",
         "files": {**STACK_FILES, "MoveTrace.java": T_MOVE}, "run": "MoveTrace", "hide": HIDE,
         "question": "Which diagram shows stack `a` at the end?",
         "choices": ["bottom [x, y] top", "bottom [x, z] top", "bottom [x] top", "bottom [x, y, z] top"],
         "answer": 0,
         "explain": "Popping `a` twice moves `z`, then `y`, onto `b`, so `b` holds `z` with `y` on top. Popping `b` returns `y`, which goes back onto `a` on top of `x`."},
        {"type": "predict", "id": "trace-mix",
         "prompt": "The loop pushes 1, 4, 9 and 16. What does the program print?",
         "files": {**STACK_FILES, "Mix.java": P_MIX}, "run": "Mix", "hide": HIDE,
         "choices": ["7\n4 2", "-7\n4 2", "7\n9 3", "15\n1 2"],
         "answer": 0,
         "explain": "The left `pop` runs first and returns 16; the right one returns 9. 16 − 9 = 7. That leaves 1 and 4, with 4 on top and size 2."},
        {"type": "blanks", "id": "trace-build", "title": "Make the stack",
         "prompt": "Fill in the two missing operations so the program ends with the stack `bottom [1, 4] top`. Each blank is one call: a `push` with a value, or a `pop`.",
         "files": {**STACK_FILES, "BuildIt.java": BUILD}, "run": "BuildIt", "hide": HIDE,
         "output": "bottom [1, 4] top",
         "blanks": {
             "a": {"accept": ["pop()"], "hint": "After pushing 1 and 2, the 2 has to go.",
                   "wrong": [{"answer": "push(4)", "why": "That leaves 2 in the stack, under the 3 and the 4."}]},
             "b": {"accept": ["pop()"], "hint": "The 3 that was just pushed has to go too.",
                   "wrong": [{"answer": "peek()", "why": "`peek` only looks at the top. The 3 stays in the stack."}]},
         },
         "explain": "Each value you don't want has to be popped while it's on top: the 2 before the 3 goes on, and the 3 before the 4 goes on."},
    ],
    "sources": [ALGS4_13, OPENDSA_STACK, JLS_EVAL_ORDER],
}
