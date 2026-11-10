from sources import ALGS4_13, OPENDSA_STACK, EMPTYSTACK_API, IFACE_TUT
from ds_code import STACK_ADT, ARRAY_STACK, STACK_FILES, main_class, lines

DEMO = main_class("StackDemo", lines(
    'StackADT<String> plates = new ArrayStack<>();',
    'plates.push("red");',
    'plates.push("green");',
    'plates.push("blue");',
    'System.out.println(plates);',
    'System.out.println("peek: " + plates.peek());',
    'System.out.println("pop: " + plates.pop());',
    'System.out.println(plates);',
    'System.out.println("size: " + plates.size());',
))
AFTER_PUSH = main_class("AfterPush", lines(
    'StackADT<String> plates = new ArrayStack<>();',
    'plates.push("red");',
    'plates.push("green");',
    'plates.push("blue");',
    'System.out.println(plates);',
))
AFTER_POP = main_class("AfterPop", lines(
    'StackADT<String> plates = new ArrayStack<>();',
    'plates.push("red");',
    'plates.push("green");',
    'plates.push("blue");',
    'plates.pop();',
    'System.out.println(plates);',
))
EMPTY = main_class("EmptyPop", lines(
    'StackADT<Integer> s = new ArrayStack<>();',
    's.push(5);',
    'System.out.println(s.pop());',
    'System.out.println(s.pop());',
))
SAFE = main_class("SafePop", lines(
    'StackADT<Integer> s = new ArrayStack<>();',
    's.push(5);',
    's.push(8);',
    'while (!s.isEmpty()) {',
    '    System.out.println(s.pop());',
    '}',
    'System.out.println("empty: " + s.isEmpty());',
))
T1 = main_class("Trace1", lines(
    'StackADT<Integer> s = new ArrayStack<>();',
    's.push(4);',
    's.push(9);',
    's.pop();',
    's.push(2);',
    's.push(7);',
    'System.out.println(s);',
))
P1 = main_class("Peeks", lines(
    'StackADT<String> s = new ArrayStack<>();',
    's.push("a");',
    's.push("b");',
    'System.out.println(s.peek());',
    'System.out.println(s.peek());',
    'System.out.println(s.pop());',
    'System.out.println(s.size());',
))

LESSON = {
    "id": "stack-lifo",
    "title": "The stack: last in, first out",
    "summary": "A stack lets you add and remove only at one end, the top. The last value pushed is the first one popped.",
    "goals": [
        "Describe a stack as LIFO: last in, first out",
        "Use the five stack operations: `push`, `pop`, `peek`, `isEmpty` and `size`",
        "Draw a stack after a sequence of operations",
        "Explain what happens when you pop an empty stack",
    ],
    "cos225": "The Exam 2 guide lists the stack as LIFO with push, pop and peek, and asks you to draw a stack and interpret changes to it. This unit covers using a stack; the next unit builds one on an array.",
    "blocks": [
        {"type": "h", "text": "One end only"},
        {"type": "p", "text": "A **stack** is a collection where you can only reach one end, called the **top**. Think of a stack of plates: you put a new plate on the top, and you take the top plate off. To reach a plate lower down, you have to remove every plate above it first."},
        {"type": "p", "text": "So the value you added **last** is the one you get back **first**. This rule is called **LIFO**: last in, first out."},
        {"type": "list", "items": [
            "`push(x)` puts `x` on the top.",
            "`pop()` removes the top value and returns it.",
            "`peek()` returns the top value without removing it.",
            "`isEmpty()` says whether the stack holds nothing.",
            "`size()` says how many values it holds.",
        ]},

        {"type": "h", "text": "The stack ADT"},
        {"type": "p", "text": "Those five operations are the stack's **abstract data type**: what a stack does, with nothing about how it stores values. In Java, an ADT is written as an interface. This one is generic, so a stack can hold any type `T`:"},
        {"type": "code", "files": {"StackADT.java": STACK_ADT}, "show": False},
        {"type": "p", "text": "`ArrayStack` implements this interface. You'll write it yourself in the next unit; for now it's given, and you only use it. Its `toString()` lists the values from the bottom to the top."},
        {"type": "code", "files": {**STACK_FILES, "StackDemo.java": DEMO}, "run": "StackDemo",
         "hide": ["StackADT.java", "ArrayStack.java"]},
        {"type": "code", "files": {"StackADT.java": STACK_ADT, "ArrayStack.java": ARRAY_STACK}, "hide": ["StackADT.java"],
         "collapsed": True, "show": False, "caption": "Show ArrayStack.java (you'll write it in the next unit)"},
        {"type": "list", "items": [
            "`blue` was pushed last, so it's on top: `peek` returns it and `pop` removes it.",
            "`peek` doesn't change the stack. `pop` does: afterwards, `green` is on top.",
            "The variable's type is the interface, `StackADT<String>`, and the object is an `ArrayStack`. Code that only uses the five operations works with any stack class.",
        ]},

        {"type": "h", "text": "Drawing a stack"},
        {"type": "p", "text": "On the exam you'll draw stacks and answer questions about them. Draw a stack as a column with the top at the top. After the three pushes, the stack looks like this:"},
        {"type": "diagram", "kind": "stack", "state": "bottom [red, green, blue] top",
         "files": {**STACK_FILES, "AfterPush.java": AFTER_PUSH}, "run": "AfterPush",
         "caption": "After `push(\"red\")`, `push(\"green\")`, `push(\"blue\")`."},
        {"type": "p", "text": "One `pop()` removes `blue`, and `green` becomes the top:"},
        {"type": "diagram", "kind": "stack", "state": "bottom [red, green] top",
         "files": {**STACK_FILES, "AfterPop.java": AFTER_POP}, "run": "AfterPop",
         "caption": "After one `pop()`."},
        {"type": "p", "text": "Each diagram on this site is checked against what the real program prints, so they always match the code."},

        {"type": "h", "text": "Popping an empty stack"},
        {"type": "p", "text": "An empty stack has no top, so `pop` and `peek` have nothing to return. `ArrayStack` throws Java's `EmptyStackException`, which crashes the program unless something catches it:"},
        {"type": "code", "files": {**STACK_FILES, "EmptyPop.java": EMPTY}, "run": "EmptyPop", "expect": "runtime",
         "hide": ["StackADT.java", "ArrayStack.java"],
         "after": "The first `pop` returns 5 and leaves the stack empty. The second has nothing to pop. The trace shows it was thrown in `ArrayStack.pop`, called from line 6 of `EmptyPop`."},
        {"type": "p", "text": "Check `isEmpty()` before you pop when you aren't sure. A common pattern is to pop until the stack is empty:"},
        {"type": "code", "files": {**STACK_FILES, "SafePop.java": SAFE}, "run": "SafePop",
         "hide": ["StackADT.java", "ArrayStack.java"]},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "lifo-trace1", "kind": "stack",
         "prompt": "Follow the operations one at a time and keep a drawing as you go.",
         "files": {**STACK_FILES, "Trace1.java": T1}, "run": "Trace1", "hide": ["StackADT.java", "ArrayStack.java"],
         "choices": ["bottom [4, 9, 2, 7] top", "bottom [4, 2, 7] top", "bottom [7, 2, 4] top", "bottom [9, 2, 7] top"],
         "answer": 1,
         "explain": "Push 4, push 9, then `pop` removes 9, the top. Pushing 2 and 7 puts them above 4, so the stack from bottom to top is 4, 2, 7."},
        {"type": "predict", "id": "lifo-peek",
         "prompt": "What does this print?",
         "files": {**STACK_FILES, "Peeks.java": P1}, "run": "Peeks", "hide": ["StackADT.java", "ArrayStack.java"],
         "choices": ["b\nb\nb\n1", "b\na\nb\n1", "b\nb\nb\n2", "a\na\na\n1"],
         "answer": 0,
         "explain": "`peek` looks at the top without removing it, so both peeks print `b`. Then `pop` removes and prints `b`, leaving one value."},
        {"type": "quiz", "id": "lifo-order",
         "question": "You push 1, 2 and 3 onto an empty stack, then pop three times. In what order do the values come out?",
         "choices": ["1, 2, 3", "3, 2, 1", "3, 1, 2", "1, 3, 2"],
         "answer": 1,
         "explain": "Last in, first out: 3 was pushed last, so it comes out first. A stack reverses the order of whatever you push."},
    ],
    "sources": [ALGS4_13, OPENDSA_STACK, EMPTYSTACK_API, IFACE_TUT],
}
