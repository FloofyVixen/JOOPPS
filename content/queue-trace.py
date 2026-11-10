from sources import ALGS4_13, OPENDSA_QUEUE, JLS_EVAL_ORDER
from ds_code import LQUEUE_FILES, STACK_FILES, main_class, lines

HIDE = ["QueueADT.java", "LinearNode.java", "LinkedQueue.java"]
SHIDE = ["StackADT.java", "ArrayStack.java"]

ROTATE = main_class("Rotate", lines(
    'QueueADT<String> q = new LinkedQueue<>();',
    'q.enqueue("A");',
    'q.enqueue("B");',
    'q.enqueue("C");',
    'q.enqueue(q.dequeue());',
    'System.out.println(q);',
    'q.enqueue(q.dequeue());',
    'System.out.println(q);',
))
PIC = main_class("Picture", lines(
    'QueueADT<Integer> q = new LinkedQueue<>();',
    'for (int i = 1; i <= 5; i++) {',
    '    q.enqueue(i * 11);',
    '}',
    'System.out.println(q);',
))
T1 = main_class("SumQueue", lines(
    'QueueADT<Integer> q = new LinkedQueue<>();',
    'q.enqueue(3);',
    'q.enqueue(5);',
    'q.enqueue(2);',
    'q.enqueue(q.dequeue() + q.dequeue());',
    'q.enqueue(q.getFront());',
    'System.out.println(q);',
))
T2 = main_class("StackToQueue", lines(
    'StackADT<Character> s = new ArrayStack<>();',
    'QueueADT<Character> q = new LinkedQueue<>();',
    'for (char c : new char[] {\'x\', \'y\', \'z\'}) {',
    '    s.push(c);',
    '}',
    'q.enqueue(s.pop());',
    'q.enqueue(\'w\');',
    'q.enqueue(s.pop());',
    'q.dequeue();',
    'System.out.println(q);',
))
P1 = main_class("Mixed", lines(
    'QueueADT<Integer> q = new LinkedQueue<>();',
    'for (int i = 1; i <= 4; i++) {',
    '    q.enqueue(i * i);',
    '}',
    'System.out.println(q.dequeue() - q.dequeue());',
    'System.out.println(q.getFront() + " " + q.size());',
))
BUILD = main_class("MakeIt", lines(
    'QueueADT<Integer> q = new LinkedQueue<>();',
    'q.enqueue(1);',
    'q.enqueue(2);',
    'q.enqueue(3);',
    'q.enqueue(q.[[a]]);',
    'q.[[b]];',
    'q.enqueue(4);',
    'System.out.println(q);',
))

LESSON = {
    "id": "queue-trace",
    "title": "Tracing a queue on paper",
    "summary": "Queue questions on the exam give you operations to trace or a drawing to read. Keep the front on the left and the rear on the right, and redraw after every change.",
    "goals": [
        "Trace enqueue, dequeue and getFront one line at a time",
        "Follow values that move from the front to the rear, or between a stack and a queue",
        "Answer questions about a drawn queue",
    ],
    "cos225": "These are the Exam 2 guide's procedural problems for queues: interpret changes, draw the result, and answer questions about a drawing.",
    "blocks": [
        {"type": "h", "text": "Front on the left, rear on the right"},
        {"type": "p", "text": "Draw the queue as a row: values leave from the left and join on the right. `enqueue` adds a box on the right; `dequeue` crosses out the box on the left (write its value down if the code uses it). Unlike a stack, both ends of the drawing change."},
        {"type": "p", "text": "A common move is `q.enqueue(q.dequeue())`: take the front value and send it to the back of the line. The values rotate:"},
        {"type": "code", "files": {**LQUEUE_FILES, "Rotate.java": ROTATE}, "run": "Rotate", "hide": HIDE},
        {"type": "p", "text": "Doing this `size()` times brings the queue back to where it started, which is a handy way to visit every value without losing any."},

        {"type": "h", "text": "Questions about a picture"},
        {"type": "p", "text": "This queue was made by enqueueing 11, 22, 33, 44 and 55 in that order:"},
        {"type": "diagram", "kind": "queue", "state": "front [11, 22, 33, 44, 55] rear",
         "files": {**LQUEUE_FILES, "Picture.java": PIC}, "run": "Picture"},
        {"type": "quiz", "id": "qtrace-pic1",
         "question": "For the queue drawn above, what do two `dequeue()` calls return, in order?",
         "choices": ["55, then 44", "11, then 22", "11, then 11", "22, then 33"],
         "answer": 1,
         "explain": "`dequeue` takes the front each time: 11, then 22. (`getFront` twice would give 11 both times.)"},
        {"type": "quiz", "id": "qtrace-pic2",
         "question": "For the same queue, how many `dequeue` calls does it take before `getFront()` returns 44?",
         "choices": ["1", "2", "3", "4"],
         "answer": 2,
         "explain": "11, 22 and 33 are in front of 44, so three values have to leave first."},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "qtrace-sum", "kind": "queue",
         "prompt": "`q.dequeue() + q.dequeue()` removes the first two values. `getFront` only looks.",
         "files": {**LQUEUE_FILES, "SumQueue.java": T1}, "run": "SumQueue", "hide": HIDE,
         "question": "Which diagram shows the queue at the end?",
         "choices": ["front [2, 8, 2] rear", "front [3, 5, 2, 8, 3] rear", "front [2, 8] rear", "front [8, 2, 8] rear"],
         "answer": 0,
         "explain": "The queue is 3, 5, 2. The two dequeues remove 3 and 5, and their sum, 8, joins at the rear: 2, 8. `getFront()` returns 2 without removing it, and that 2 is enqueued too: 2, 8, 2."},
        {"type": "trace", "id": "qtrace-mix", "kind": "queue",
         "prompt": "A stack and a queue together. The stack's `pop` takes from its top.",
         "files": {**STACK_FILES, **LQUEUE_FILES, "StackToQueue.java": T2}, "run": "StackToQueue", "hide": SHIDE + HIDE,
         "question": "Which diagram shows the queue `q` at the end?",
         "choices": ["front [w, y] rear", "front [z, w, y] rear", "front [w, x] rear", "front [y, w] rear"],
         "answer": 0,
         "explain": "The stack holds x, y, z with z on top. The first pop gives z, then `w` is enqueued, then the second pop gives y: the queue is z, w, y. Dequeueing removes z, the front."},
        {"type": "predict", "id": "qtrace-mixed",
         "prompt": "The loop enqueues 1, 4, 9 and 16. What does the program print?",
         "files": {**LQUEUE_FILES, "Mixed.java": P1}, "run": "Mixed", "hide": HIDE,
         "choices": ["-3\n9 2", "3\n9 2", "-3\n4 3", "7\n1 2"],
         "answer": 0,
         "explain": "The left `dequeue` runs first and returns 1; the right one returns 4. 1 − 4 = −3. Then 9 is at the front, with 2 values left. (Compare the stack version in unit 13, where the same code gave 16 − 9.)"},
        {"type": "blanks", "id": "qtrace-build", "title": "Make the queue",
         "prompt": "Fill in the two blanks so the program ends with `front [3, 1, 4] rear`. Each blank is one queue method call.",
         "files": {**LQUEUE_FILES, "MakeIt.java": BUILD}, "run": "MakeIt", "hide": HIDE,
         "output": "front [3, 1, 4] rear",
         "blanks": {
             "a": {"accept": ["dequeue()"], "hint": "The 1 has to move from the front to the rear.",
                   "wrong": [{"answer": "getFront()", "why": "`getFront` copies the 1 to the rear but leaves the original at the front, so the queue becomes 1, 2, 3, 1."}]},
             "b": {"accept": ["dequeue()"], "hint": "Now the 2 is at the front, and it must go.",
                   "wrong": [{"answer": "getFront()", "why": "`getFront` only looks. The 2 stays in the queue."}]},
         },
         "explain": "`q.enqueue(q.dequeue())` rotates 1 to the rear (2, 3, 1); `dequeue()` removes 2 (3, 1); then 4 joins at the rear."},
    ],
    "sources": [ALGS4_13, OPENDSA_QUEUE, JLS_EVAL_ORDER],
}
