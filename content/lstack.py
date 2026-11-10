from sources import ALGS4_13, OPENDSA_STACK, EMPTYSTACK_API
from ds_code import STACK_ADT, LINEAR_NODE, LINKED_STACK, LSTACK_FILES, STACK_FILES, ARRAY_STACK, main_class, lines

HIDE = ["StackADT.java", "LinearNode.java", "LinkedStack.java"]

DEMO = main_class("LinkedDemo", lines(
    'StackADT<String> s = new LinkedStack<>();',
    's.push("red");',
    's.push("green");',
    's.push("blue");',
    'System.out.println(s);',
    'System.out.println(s.pop() + " " + s.peek() + " " + s.size());',
    'System.out.println(s);',
))
BOTH = main_class("BothStacks", lines(
    'StackADT<Integer> a = new ArrayStack<>();',
    'StackADT<Integer> b = new LinkedStack<>();',
    'for (int i = 1; i <= 3; i++) {',
    '    a.push(i * 10);',
    '    b.push(i * 10);',
    '}',
    'System.out.println(a);',
    'System.out.println(b);',
    'System.out.println(a.pop() + " " + b.pop());',
))
T1 = main_class("LTrace", lines(
    'LinkedStack<Character> s = new LinkedStack<>();',
    's.push(\'a\');',
    's.push(\'b\');',
    's.push(\'c\');',
    's.pop();',
    's.push(\'d\');',
    's.push(s.peek());',
    'System.out.println(s);',
))
BL = LINKED_STACK.replace("""        LinearNode<T> node = new LinearNode<>(element);
        node.setNext(top);
        top = node;""", """        LinearNode<T> node = new LinearNode<>(element);
        [[link]];
        [[move]];""").replace("""        T result = top.getElement();
        top = top.getNext();""", """        T result = top.getElement();
        [[popmove]];""")
BLT = main_class("LStackTester", lines(
    'StackADT<Integer> s = new LinkedStack<>();',
    'for (int i = 1; i <= 4; i++) {',
    '    s.push(i);',
    '}',
    'System.out.println(s.pop() + " " + s.pop() + " " + s.size());',
    'System.out.println(s);',
))

LESSON = {
    "id": "lstack",
    "title": "LinkedStack: the top at the head",
    "summary": "A stack built from linked nodes keeps its top at the head of the chain, where adding and removing are O(1). No array, so it never fills up.",
    "goals": [
        "Implement push, pop and peek on linked nodes",
        "Explain why the top of a linked stack is the head, not the last node",
        "Draw a linked stack and the same stack as an array",
    ],
    "cos225": "The Exam 2 guide asks you to contrast array and linked stacks and say where the top is located. For an array stack it's the end of the array; for a linked stack it's the head.",
    "blocks": [
        {"type": "h", "text": "Which end is the top?"},
        {"type": "p", "text": "A stack only works at one end, so pick the end of a linked list that's cheap to change. At the **head**, adding is `addFirst` and removing is `removeFirst`: both O(1). At the **last** node, adding means walking to the end, and removing is worse: you'd need the node **before** the last one, so you'd walk the whole list for every pop. So a linked stack's top is its head."},

        {"type": "h", "text": "LinkedStack"},
        {"type": "p", "text": "It implements the same `StackADT<T>` as `ArrayStack`, so code using one can use the other. `top` is the head node, and `count` keeps `size()` O(1)."},
        {"type": "code", "files": {"StackADT.java": STACK_ADT, "LinearNode.java": LINEAR_NODE, "LinkedStack.java": LINKED_STACK},
         "hide": ["StackADT.java", "LinearNode.java"], "show": False},
        {"type": "list", "items": [
            "`push` is add-at-front: the new node points at the old top, then becomes the top.",
            "`pop` saves the top's element, then moves `top` to the next node. The old top node is no longer referenced.",
            "`isEmpty` checks `top == null`. There's no capacity and no `expandCapacity`: every push makes exactly one new node.",
        ]},
        {"type": "code", "files": {**LSTACK_FILES, "LinkedDemo.java": DEMO}, "run": "LinkedDemo", "hide": HIDE,
         "after": "Its `toString` prints the chain from the top, so the most recent push comes first."},

        {"type": "h", "text": "One stack, two drawings"},
        {"type": "p", "text": "The same pushes into an `ArrayStack` and a `LinkedStack` give the same stack, drawn two ways. In the array, the top is the **last** used index. In the chain, the top is the **head**:"},
        {"type": "code", "files": {**STACK_FILES, **LSTACK_FILES, "BothStacks.java": BOTH}, "run": "BothStacks",
         "hide": ["StackADT.java", "ArrayStack.java", "LinearNode.java", "LinkedStack.java"]},
        {"type": "diagram", "kind": "stack", "state": "bottom [10, 20, 30] top",
         "files": {**STACK_FILES, **LSTACK_FILES, "BothStacks.java": BOTH}, "run": "BothStacks", "line": 0,
         "caption": "As a stack (and as `ArrayStack` stores it): 10 at the bottom, 30 on top."},
        {"type": "diagram", "kind": "linked", "state": "head -> 30 -> 20 -> 10 -> null",
         "files": {**STACK_FILES, **LSTACK_FILES, "BothStacks.java": BOTH}, "run": "BothStacks", "line": 1,
         "caption": "As `LinkedStack` stores it: the top, 30, is the head, and the bottom, 10, is the last node."},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "lstack-trace", "kind": "linked",
         "prompt": "Draw the chain of nodes, with the top as the head.",
         "files": {**LSTACK_FILES, "LTrace.java": T1}, "run": "LTrace", "hide": HIDE,
         "question": "Which diagram shows the stack's nodes at the end?",
         "choices": ["head -> a -> b -> d -> d -> null", "head -> d -> d -> b -> a -> null", "head -> d -> b -> a -> null", "head -> d -> c -> b -> a -> null"],
         "answer": 1,
         "explain": "After a, b, c the chain is c, b, a. Popping removes c. Pushing d gives d, b, a. `s.push(s.peek())` pushes a second d: d, d, b, a."},
        {"type": "blanks", "id": "lstack-blanks", "title": "Push and pop",
         "prompt": "Fill in `push` and `pop`.",
         "files": {"StackADT.java": STACK_ADT, "LinearNode.java": LINEAR_NODE, "LinkedStack.java": BL, "LStackTester.java": BLT},
         "hide": ["StackADT.java", "LinearNode.java"], "run": "LStackTester",
         "output": "4 3 2\nhead -> 2 -> 1 -> null",
         "blanks": {
             "link": {"accept": ["node.setNext(top)"], "hint": "The new node sits on top of the old top.",
                      "wrong": [{"answer": "top.setNext(node)", "why": "That attaches the new node **below** the old top, and on an empty stack `top` is `null`, so it crashes."}]},
             "move": {"accept": ["top = node"], "hint": "The new node is now the top.",
                      "wrong": [{"answer": "node = top", "why": "That changes the local variable, not the field, so `top` never moves and the push is lost."}]},
             "popmove": {"accept": ["top = top.getNext()"], "hint": "The node under the top becomes the top.",
                         "wrong": [{"answer": "top.setNext(null)", "why": "That cuts off everything under the top, and the top itself stays, so the next pop returns the same value."}]},
         },
         "explain": "Push: link the new node to the old top, then move `top` to it. Pop: move `top` to the next node."},
        {"type": "quiz", "id": "lstack-why",
         "question": "Why does `LinkedStack` keep its top at the head of the chain?",
         "choices": ["Because the head is the only node that can hold data", "Because adding and removing at the head are O(1), while removing the last node is O(n) with only a head reference", "Because the bottom must always be `null`", "So that `toString` prints in order"],
         "answer": 1,
         "explain": "At the head, push and pop just relink one node. To pop the last node you'd have to find the node before it by walking the whole list."},
        {"type": "quiz", "id": "lstack-full",
         "question": "What happens when you push onto a `LinkedStack` that already holds a million values?",
         "choices": ["It throws an exception because it's full", "It copies all the nodes into a bigger array", "It creates one new node and links it in, the same as any other push", "It walks to the end of the list first"],
         "answer": 2,
         "explain": "A linked stack has no capacity. Every push is one `new` and two reference changes."},
    ],
    "sources": [ALGS4_13, OPENDSA_STACK, EMPTYSTACK_API],
}
