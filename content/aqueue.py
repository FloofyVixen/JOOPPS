from sources import ALGS4_13, OPENDSA_QUEUE, NOSUCH_API, JLS_REM
from ds_code import QUEUE_ADT, ARRAY_QUEUE, CIRCULAR_QUEUE, QUEUE_FILES, CQUEUE_FILES, main_class, lines

AHIDE = ["QueueADT.java", "ArrayQueue.java"]
CHIDE = ["QueueADT.java", "CircularArrayQueue.java"]


def prog(name, cls, *stmts, t="String"):
    return main_class(name, lines(f"{cls}<{t}> q = new {cls}<>();", *stmts))


SHIFT = prog("ShiftDemo", "ArrayQueue", 'q.enqueue("a");', 'q.enqueue("b");', 'q.enqueue("c");',
             'System.out.println(q.arrayString());', 'q.dequeue();', 'System.out.println(q.arrayString());')
CIRC = prog("CircleDemo", "CircularArrayQueue", 'q.enqueue("a");', 'q.enqueue("b");', 'q.enqueue("c");',
            'System.out.println(q.arrayString());', 'q.dequeue();', 'q.dequeue();', 'System.out.println(q.arrayString());',
            'q.enqueue("d");', 'q.enqueue("e");', 'System.out.println(q.arrayString());', 'System.out.println(q);')
GROW = prog("GrowDemo", "CircularArrayQueue", 'for (String s : new String[] {"a", "b", "c", "d"}) {', '    q.enqueue(s);', '}',
            'q.dequeue();', 'q.dequeue();', 'q.enqueue("e");', 'q.enqueue("f");', 'System.out.println(q.arrayString());',
            'q.enqueue("g");', 'System.out.println(q.arrayString());')
T1 = prog("CircleTrace", "CircularArrayQueue", 'q.enqueue("p");', 'q.enqueue("q");', 'q.enqueue("r");', 'q.dequeue();',
          'q.enqueue("s");', 'q.enqueue("t");', 'q.dequeue();', 'System.out.println(q.arrayString());')
T2 = prog("ShiftTrace", "ArrayQueue", 'q.enqueue("x");', 'q.enqueue("y");', 'q.enqueue("z");', 'q.dequeue();', 'q.enqueue("w");',
          'System.out.println(q.arrayString());')
MOD = main_class("Wrap", lines(
    'int length = 4;',
    'int rear = 0;',
    'for (int i = 0; i < 6; i++) {',
    '    System.out.print(rear + " ");',
    '    rear = (rear + 1) % length;',
    '}',
    'System.out.println();',
))
BL = CIRCULAR_QUEUE.replace("""        queue[rear] = element;
        rear = (rear + 1) % queue.length;""", """        queue[rear] = element;
        rear = [[rearstep]];""").replace("""        queue[front] = null;
        front = (front + 1) % queue.length;""", """        queue[front] = null;
        front = [[frontstep]];""").replace("""    public boolean isEmpty() {
        return count == 0;""", """    public boolean isEmpty() {
        return [[empty]];""")
BLT = main_class("CircleTester", lines(
    'CircularArrayQueue<Integer> q = new CircularArrayQueue<>();',
    'for (int i = 1; i <= 4; i++) {',
    '    q.enqueue(i);',
    '}',
    'q.dequeue();',
    'q.dequeue();',
    'q.dequeue();',
    'q.dequeue();',
    'System.out.println(q.isEmpty() + " " + q.arrayString());',
    'q.enqueue(5);',
    'q.enqueue(6);',
    'System.out.println(q + " " + q.arrayString());',
))

LESSON = {
    "id": "aqueue",
    "title": "Array queues: shifting versus circular",
    "summary": "A queue changes at both ends, which is awkward for an array. Keeping the front at index 0 makes every dequeue shift the array; letting front and rear both move, and wrap around, makes both operations O(1).",
    "goals": [
        "Implement an array queue whose dequeue shifts the values left, and say why it's O(n)",
        "Implement a circular array queue with `front`, `rear` and `count`",
        "Use `%` to wrap an index around the end of the array",
        "Draw a circular queue's array, including after it wraps and after it grows",
    ],
    "cos225": "The Exam 2 guide lists the challenge of having the front and rear at different points, and array versus linked performance. This lesson is the array half.",
    "blocks": [
        {"type": "h", "text": "Front fixed at index 0"},
        {"type": "p", "text": "The simplest array queue copies the array stack: values fill the array from index 0, and `rear` is the next free slot, so `enqueue` is O(1). But the front must also stay at index 0, so `dequeue` takes `queue[0]` and then shifts every remaining value one slot left:"},
        {"type": "code", "files": QUEUE_FILES, "hide": ["QueueADT.java"], "show": False},
        {"type": "code", "files": {**QUEUE_FILES, "ShiftDemo.java": SHIFT}, "run": "ShiftDemo", "hide": AHIDE},
        {"type": "diagram", "kind": "array", "state": "[b, c, _, _] front=0 rear=2",
         "files": {**QUEUE_FILES, "ShiftDemo.java": SHIFT}, "run": "ShiftDemo", "line": 1,
         "caption": "After one dequeue, `b` and `c` have both moved left. With n values, a dequeue moves n − 1 of them: O(n)."},

        {"type": "h", "text": "Let the front move"},
        {"type": "p", "text": "Instead of shifting, let `front` move too: `dequeue` takes `queue[front]` and adds 1 to `front`. Now both operations are O(1). The catch is that both indexes only ever move right, so the queue creeps toward the end of the array, leaving unused slots behind it at the start."},
        {"type": "p", "text": "The fix is to treat the array as a circle: after the last index comes index 0 again. The remainder operator `%` does the wrapping. `(i + 1) % length` counts 0, 1, 2, 3, 0, 1, …:"},
        {"type": "code", "files": {"Wrap.java": MOD}, "run": "Wrap"},

        {"type": "h", "text": "CircularArrayQueue"},
        {"type": "p", "text": "The circular queue keeps three ints: `front` (index of the front value), `rear` (index of the next free slot) and `count`. Both `enqueue` and `dequeue` move their index with `% queue.length`."},
        {"type": "code", "files": CQUEUE_FILES, "hide": ["QueueADT.java"], "show": False},
        {"type": "p", "text": "Here the queue fills up, empties from the front, and then wraps: `d` goes into the last slot and `e` wraps around into index 0."},
        {"type": "code", "files": {**CQUEUE_FILES, "CircleDemo.java": CIRC}, "run": "CircleDemo", "hide": CHIDE},
        {"type": "diagram", "kind": "array", "state": "[e, _, c, d] front=2 rear=1",
         "files": {**CQUEUE_FILES, "CircleDemo.java": CIRC}, "run": "CircleDemo", "line": 2,
         "caption": "The queue is `c, d, e`: start at `front` and go right, wrapping from the last index to 0. `rear` is now **before** `front` in the array."},
        {"type": "p", "text": "Why keep `count`? When the array is full, `rear` has wrapped all the way round to `front`, and when it's empty, `front` has caught up with `rear`. Either way `front == rear`, so the indexes alone can't tell full from empty. The count can."},

        {"type": "h", "text": "Growing a circular queue"},
        {"type": "p", "text": "When `count` reaches the capacity, `expandCapacity` can't just copy slot `i` to slot `i`: the queue might wrap, with its front in the middle of the array. It copies the values **in queue order**, starting at `front`, into slots 0, 1, 2, … of the new array, then resets `front` to 0 and `rear` to `count`."},
        {"type": "code", "files": {**CQUEUE_FILES, "GrowDemo.java": GROW}, "run": "GrowDemo", "hide": CHIDE},
        {"type": "diagram", "kind": "array", "state": "[c, d, e, f, g, _, _, _] front=0 rear=5",
         "files": {**CQUEUE_FILES, "GrowDemo.java": GROW}, "run": "GrowDemo", "line": 1,
         "caption": "Before growing, the queue `c, d, e, f` was wrapped (`e` and `f` in slots 0 and 1). After growing, it's unrolled in order."},

        {"type": "h", "text": "Practice"},
        {"type": "trace", "id": "aq-trace-circle", "kind": "array",
         "prompt": "A `CircularArrayQueue` with 4 slots. Track `front`, `rear` and the slots as you go.",
         "files": {**CQUEUE_FILES, "CircleTrace.java": T1}, "run": "CircleTrace", "hide": CHIDE,
         "question": "Which diagram shows the array at the end?",
         "choices": ["[t, _, r, s] front=2 rear=1", "[r, s, t, _] front=0 rear=3", "[_, q, r, s] front=1 rear=0", "[t, q, r, s] front=2 rear=1"],
         "answer": 0,
         "explain": "p, q, r fill slots 0 to 2. The first dequeue clears slot 0 (front 1). `s` fills slot 3 and `t` wraps into slot 0, so `rear` is 1. The second dequeue clears slot 1 (front 2). The queue is r, s, t."},
        {"type": "trace", "id": "aq-trace-shift", "kind": "array",
         "prompt": "This is the shifting `ArrayQueue`, whose front stays at index 0.",
         "files": {**QUEUE_FILES, "ShiftTrace.java": T2}, "run": "ShiftTrace", "hide": AHIDE,
         "question": "Which diagram shows the array at the end?",
         "choices": ["[_, y, z, w] front=0 rear=4", "[y, z, w, _] front=0 rear=3", "[w, y, z, _] front=0 rear=3", "[y, z, _, w] front=0 rear=4"],
         "answer": 1,
         "explain": "After x, y, z, the dequeue removes x and shifts y and z left: `[y, z, _, _]`, rear 2. Then w goes in slot 2."},
        {"type": "blanks", "id": "aq-blanks", "title": "The circular steps",
         "prompt": "Fill in the three blanks in `CircularArrayQueue`.",
         "files": {"QueueADT.java": QUEUE_ADT, "CircularArrayQueue.java": BL, "CircleTester.java": BLT}, "run": "CircleTester",
         "hide": ["QueueADT.java"],
         "output": "true [_, _, _, _] front=0 rear=0\nfront [5, 6] rear [5, 6, _, _] front=0 rear=2",
         "blanks": {
             "rearstep": {"accept": ["(rear + 1) % queue.length"], "hint": "Move one slot right, wrapping to 0 after the last slot.",
                          "wrong": [{"answer": "rear + 1", "why": "Without wrapping, `rear` runs off the end: after four enqueues it's 4, so the fifth enqueue writes past the array."}]},
             "frontstep": {"accept": ["(front + 1) % queue.length"], "hint": "Same as `rear`.",
                           "wrong": [{"answer": "front + 1", "why": "After four dequeues `front` is 4, past the end of the array, so the queue's values are no longer where `front` says."}]},
             "empty": {"accept": ["count == 0"], "hint": "Indexes alone can't tell full from empty.",
                       "wrong": [{"answer": "front == rear", "why": "That's also true when the queue is full. Here it happens to give the right answers, but a full queue would claim to be empty."}]},
         },
         "explain": "Both indexes step with `% queue.length`, and `count` decides empty versus full."},
        {"type": "quiz", "id": "aq-cost",
         "question": "Which statement is true about the two array queues?",
         "choices": ["Both have O(1) dequeue", "The shifting queue has O(n) dequeue; the circular queue has O(1) dequeue", "The circular queue has O(n) enqueue because of the `%`", "The shifting queue never needs to grow"],
         "answer": 1,
         "explain": "The shifting queue moves every value on each dequeue. The circular queue just moves `front`; `%` is a single arithmetic step."},
    ],
    "sources": [ALGS4_13, OPENDSA_QUEUE, NOSUCH_API, JLS_REM],
}
