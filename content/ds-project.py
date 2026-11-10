from sources import ALGS4_13, OPENDSA_STACK, OPENDSA_QUEUE, STRING_API
from ds_code import LSTACK_FILES, LQUEUE_FILES

DOC = """public class Document {
    private String name;
    private String text;
    private StackADT<String> history;

    public Document(String name) {
        this.name = name;
        this.text = "";
        this.history = new LinkedStack<>();
    }

    public void append(String more) {
        history.push(text);
        text = text + more;
    }

    public void replace(String target, String replacement) {
        history.push(text);
        text = text.replace(target, replacement);
    }

    public boolean undo() {
        if (history.isEmpty()) {
            return false;
        }
        text = history.pop();
        return true;
    }

    public String getName() {
        return name;
    }

    public String getText() {
        return text;
    }
}
"""
SPOOL = """public class Spooler {
    private QueueADT<String> jobs;

    public Spooler() {
        jobs = new LinkedQueue<>();
    }

    public void submit(Document doc) {
        jobs.enqueue(doc.getName() + ": " + doc.getText());
    }

    public void printNext() {
        if (jobs.isEmpty()) {
            System.out.println("nothing to print");
        } else {
            System.out.println("printing " + jobs.dequeue());
        }
    }

    public int waiting() {
        return jobs.size();
    }
}
"""
OFFICE = """public class Office {
    public static void main(String[] args) {
        Document memo = new Document("memo");
        Spooler printer = new Spooler();

        memo.append("Lunch at 12.");
        memo.append(" Bring snacks.");
        printer.submit(memo);

        memo.replace("12", "1");
        System.out.println(memo.getText());
        memo.undo();
        memo.undo();
        System.out.println(memo.getText());
        printer.submit(memo);

        System.out.println(printer.waiting() + " jobs waiting");
        printer.printNext();
        printer.printNext();
        printer.printNext();
    }
}
"""
BASE = {**LSTACK_FILES, **LQUEUE_FILES}
FILES = {**BASE, "Document.java": DOC, "Spooler.java": SPOOL, "Office.java": OFFICE}
HIDE = list(BASE)
PRED = """public class Edits {
    public static void main(String[] args) {
        Document d = new Document("list");
        d.append("eggs");
        d.append(", milk");
        d.replace("milk", "tea");
        d.undo();
        d.append(", jam");
        System.out.println(d.getText());
        System.out.println(d.undo() + " " + d.undo() + " " + d.undo() + " " + d.undo());
    }
}
"""
BLDOC = DOC.replace("""    public void append(String more) {
        history.push(text);
        text = text + more;
    }""", """    public void append(String more) {
        [[save]];
        text = text + more;
    }""").replace("""        if (history.isEmpty()) {
            return false;
        }
        text = history.pop();""", """        if ([[check]]) {
            return false;
        }
        text = [[restore]];""")

LESSON = {
    "id": "ds-project",
    "title": "Project: an undo history and a print queue",
    "summary": "Put a stack and a queue to work in one small program: documents that remember their edits so they can be undone, and a printer that prints jobs in the order they were sent.",
    "goals": [
        "Use a stack field to give a class an undo history",
        "Use a queue field to process requests in arrival order",
        "Program to the `StackADT` and `QueueADT` interfaces, not to one implementation",
    ],
    "cos225": "Exam 2's code-writing questions give you classes like these with the scaffolding in place and ask for a few lines of a method. This project shows the kind of class a stack or queue usually lives inside.",
    "blocks": [
        {"type": "h", "text": "The design"},
        {"type": "list", "items": [
            "A `Document` has a name and some text. Before every change, it pushes the old text onto a **stack**. `undo` pops it back. The most recent change is undone first: LIFO.",
            "A `Spooler` holds print jobs in a **queue**. `submit` enqueues a copy of the document's text; `printNext` dequeues and prints the oldest job: FIFO.",
            "Both store their structure in a field whose type is the ADT interface (`StackADT<String>`, `QueueADT<String>`). Only the constructor names `LinkedStack` or `LinkedQueue`, so switching to an array version would change one line.",
        ]},

        {"type": "h", "text": "The classes"},
        {"type": "code", "files": {**BASE, "Document.java": DOC}, "hide": HIDE, "show": False},
        {"type": "code", "files": {**BASE, "Document.java": DOC, "Spooler.java": SPOOL}, "hide": HIDE + ["Document.java"], "show": False},
        {"type": "p", "text": "Now an office that writes a memo, prints it, changes its mind, and prints again:"},
        {"type": "code", "files": FILES, "run": "Office", "hide": HIDE + ["Document.java", "Spooler.java"]},
        {"type": "list", "items": [
            "The first job holds the memo's text **as it was when submitted**. Java `String`s can't change, so later edits make a new string and the queued one stays the same.",
            "Two `undo` calls step back through two changes: the `replace`, then the second `append`.",
            "The third `printNext` finds the queue empty and says so instead of crashing.",
        ]},

        {"type": "h", "text": "Practice"},
        {"type": "blanks", "id": "proj-undo", "title": "Saving and restoring",
         "prompt": "Fill in the blanks in `Document`'s `append` and `undo`.",
         "files": {**BASE, "Document.java": BLDOC, "Spooler.java": SPOOL, "Office.java": OFFICE}, "hide": HIDE + ["Spooler.java"],
         "run": "Office",
         "output": "Lunch at 1. Bring snacks.\nLunch at 12.\n2 jobs waiting\nprinting memo: Lunch at 12. Bring snacks.\nprinting memo: Lunch at 12.\nnothing to print",
         "blanks": {
             "save": {"accept": ["history.push(text)"], "hint": "Save the text as it is before the change.",
                      "wrong": [{"answer": "history.push(more)", "why": "That saves the added part, not the old text, so `undo` sets the text to `\" Bring snacks.\"`."}]},
             "check": {"accept": ["history.isEmpty()", "history.size() == 0"], "hint": "Nothing to undo when there's no saved version."},
             "restore": {"accept": ["history.pop()"], "hint": "Take the most recent saved version off the stack.",
                         "wrong": [{"answer": "history.peek()", "why": "`peek` leaves that version on the stack, so the second `undo` restores the same text again instead of going one step further back."}]},
         },
         "explain": "Push the old text before each change; `undo` pops the most recent one."},
        {"type": "predict", "id": "proj-edits",
         "prompt": "Each successful `undo` returns `true`. What does this print?",
         "files": {**BASE, "Document.java": DOC, "Edits.java": PRED}, "run": "Edits", "hide": HIDE + ["Document.java"],
         "choices": ["eggs, milk, jam\ntrue true true false", "eggs, tea, jam\ntrue true true false", "eggs, milk, jam\ntrue true true true", "eggs, jam\ntrue true false false"],
         "answer": 0,
         "explain": "The `replace` is undone straight away, so `, jam` is added to `eggs, milk`. The stack then holds three saved versions: the empty text from before `eggs`, the text before `, milk`, and the text before `, jam`. (The version the `replace` saved was popped by the undo.) So three undos succeed and the fourth finds the stack empty."},
    ],
    "sources": [ALGS4_13, OPENDSA_STACK, OPENDSA_QUEUE, STRING_API],
}
