from sources import ALGS4_13, ALGS4_41, QUEUE_TUT, DEQUE_API, ARRAYLIST_API, LINKEDLIST_API

EXPLORE = """import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Queue;

public class Explore {
    // Room i has doors to the rooms listed in doors[i].
    static int[][] doors = {
        {1, 2},     // room 0
        {3, 4},     // room 1
        {5},        // room 2
        {},         // room 3
        {},         // room 4
        {}          // room 5
    };

    public static void withQueue() {
        boolean[] seen = new boolean[doors.length];
        Queue<Integer> toVisit = new ArrayDeque<>();
        toVisit.add(0);
        seen[0] = true;
        String order = "";
        while (!toVisit.isEmpty()) {
            int room = toVisit.remove();
            order += room + " ";
            for (int next : doors[room]) {
                if (!seen[next]) {
                    seen[next] = true;
                    toVisit.add(next);
                }
            }
        }
        System.out.println("queue: " + order);
    }

    public static void withStack() {
        boolean[] seen = new boolean[doors.length];
        Deque<Integer> toVisit = new ArrayDeque<>();
        toVisit.push(0);
        seen[0] = true;
        String order = "";
        while (!toVisit.isEmpty()) {
            int room = toVisit.pop();
            order += room + " ";
            for (int next : doors[room]) {
                if (!seen[next]) {
                    seen[next] = true;
                    toVisit.push(next);
                }
            }
        }
        System.out.println("stack: " + order);
    }

    public static void main(String[] args) {
        withQueue();
        withStack();
    }
}
"""

SCENARIOS = [
    ("A browser's back button", "Stack", "The most recent page is the one you go back to: LIFO."),
    ("Customers waiting for the next available agent", "Queue", "First come, first served: FIFO."),
    ("Reading the 500th of a million stored values, often", "Array-based list", "Direct access by index is O(1)."),
    ("A playlist where songs are often inserted and removed right after the one playing", "Linked list", "With a reference to the current node, linking in or out after it is O(1)."),
    ("Checking that every `{` in a file has a matching `}`", "Stack", "The most recently opened brace must close first."),
    ("Jobs sent to a shared printer", "Queue", "Printed in the order they arrived."),
    ("Undoing edits in a text editor", "Stack", None),
    ("Taking turns in a game, round after round", "Queue", "Rotate: the player who just went goes to the back."),
]

LESSON = {
    "id": "ds-choose",
    "title": "Choosing a structure",
    "summary": "Stacks, queues, array lists and linked lists can all hold the same values. What decides between them is the order you need things back in and which operations you'll do most.",
    "goals": [
        "Pick a stack, queue, array list or linked list for a described problem",
        "See how swapping a queue for a stack changes the order of an exploration",
        "Justify a choice with the big O of the operations it needs",
    ],
    "cos225": "The Exam 2 guide asks what each structure is for and how array and linked versions compare. Short-answer questions often describe a situation and ask which structure fits.",
    "blocks": [
        {"type": "h", "text": "Three questions"},
        {"type": "list", "items": [
            "**What order do you need values back in?** Most recent first: a stack. Oldest first: a queue. Any position, by index: a list.",
            "**Where do you add and remove?** Only at one end: a stack. One end in, the other out: a queue. Anywhere: a list.",
            "**Which operation happens most?** Reading by index favours an array-based list (O(1)). Adding and removing at the front, or next to a node you already have, favours a linked list (O(1)).",
        ]},

        {"type": "h", "text": "Same code, different order"},
        {"type": "p", "text": "Here's a building where each room has doors to other rooms. Both methods explore from room 0 the same way: take a room from the to-visit collection, then add the rooms it leads to. The only difference is whether that collection is a queue or a stack:"},
        {"type": "code", "files": {"Explore.java": EXPLORE}, "run": "Explore"},
        {"type": "list", "items": [
            "**With a queue**, rooms are visited in the order they were discovered: first everything one door from room 0 (1 and 2), then everything two doors away (3, 4 and 5). This is **breadth-first search**, and it finds the shortest route to every room.",
            "**With a stack**, the most recently discovered room is explored next, so the search runs as deep as it can down one branch before backing up. This is **depth-first search**.",
        ]},
        {"type": "p", "text": "Princeton's *Algorithms* (section 4.1) covers both searches; its breadth-first search uses a queue just like this one. You'll meet the same ideas again with trees."},

        {"type": "h", "text": "Practice"},
        {"type": "match", "id": "choose-match",
         "prompt": "Match each situation with the structure that fits it best.",
         "options": ["Stack", "Queue", "Array-based list", "Linked list"],
         "items": [{"text": t, "answer": a, **({"why": w} if w else {})} for t, a, w in SCENARIOS]},
        {"type": "quiz", "id": "choose-bfs",
         "question": "In the exploration above, what would change if `withQueue` used a stack instead?",
         "choices": ["Nothing; both visit rooms in the same order", "It would visit rooms deep down one branch before rooms closer to the start", "It would visit fewer rooms", "It would crash on the empty rooms"],
         "answer": 1,
         "explain": "Swapping the queue for a stack turns breadth-first into depth-first: same rooms, different order."},
    ],
    "sources": [ALGS4_13, ALGS4_41, QUEUE_TUT, DEQUE_API, ARRAYLIST_API, LINKEDLIST_API],
}
