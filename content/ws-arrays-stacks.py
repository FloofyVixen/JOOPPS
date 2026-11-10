from sources import DEQUE_API, ARRAYDEQUE_API, ALGS4_13, OPENDSA_STACK
from wshelp import step, guided, workshop, task

IMPORTS = "import java.util.ArrayDeque;\nimport java.util.Deque;\n\n"

B1 = IMPORTS + """public class Browser {
    private String current;
    private Deque<String> back = new ArrayDeque<>();

    public Browser(String home) {
        current = home;
    }

    public void visit(String page) {
        back.push(current);
        current = page;
    }

    public String getCurrent() {
        return current;
    }
}
"""
B2 = B1.replace("""    public String getCurrent() {""", """    public void back() {
        if (back.isEmpty()) {
            System.out.println("Can't go back");
        } else {
            current = back.pop();
        }
    }

    public String getCurrent() {""")
B3 = B2.replace("""    private Deque<String> back = new ArrayDeque<>();
""", """    private Deque<String> back = new ArrayDeque<>();
    private Deque<String> forward = new ArrayDeque<>();
""").replace("""        back.push(current);
        current = page;
    }""", """        back.push(current);
        current = page;
        forward.clear();
    }""").replace("""            current = back.pop();
        }
    }
""", """            forward.push(current);
            current = back.pop();
        }
    }

    public void forward() {
        if (forward.isEmpty()) {
            System.out.println("Can't go forward");
        } else {
            back.push(current);
            current = forward.pop();
        }
    }
""")
BT1 = """public class BrowserTester {
    public static void main(String[] args) {
        Browser b = new Browser("home");
        b.visit("news");
        b.visit("sports");
        System.out.println(b.getCurrent());
    }
}
"""
BT2 = """public class BrowserTester {
    public static void main(String[] args) {
        Browser b = new Browser("home");
        b.visit("news");
        b.visit("sports");
        b.back();
        System.out.println(b.getCurrent());
        b.back();
        System.out.println(b.getCurrent());
        b.back();
        System.out.println(b.getCurrent());
    }
}
"""
BT3 = """public class BrowserTester {
    public static void main(String[] args) {
        Browser b = new Browser("home");
        b.visit("news");
        b.visit("sports");
        b.back();
        b.back();
        b.forward();
        System.out.println(b.getCurrent());
        b.visit("weather");
        b.forward();
        b.back();
        System.out.println(b.getCurrent());
    }
}
"""

P1 = IMPORTS + """public class Postfix {
    public static int evaluate(String expression) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String token : expression.split(" ")) {
            stack.push(Integer.parseInt(token));
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        System.out.println(evaluate("42"));
        System.out.println(evaluate("1 2 3"));
    }
}
"""
P2 = IMPORTS + """public class Postfix {
    public static int evaluate(String expression) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String token : expression.split(" ")) {
            if (token.equals("+") || token.equals("-")) {
                int right = stack.pop();
                int left = stack.pop();
                if (token.equals("+")) {
                    stack.push(left + right);
                } else {
                    stack.push(left - right);
                }
            } else {
                stack.push(Integer.parseInt(token));
            }
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        System.out.println(evaluate("3 4 +"));
        System.out.println(evaluate("10 4 -"));
        System.out.println(evaluate("1 2 + 5 -"));
    }
}
"""
P3 = IMPORTS + """public class Postfix {
    public static int evaluate(String expression) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String token : expression.split(" ")) {
            if (token.equals("+") || token.equals("-") || token.equals("*") || token.equals("/")) {
                int right = stack.pop();
                int left = stack.pop();
                if (token.equals("+")) {
                    stack.push(left + right);
                } else if (token.equals("-")) {
                    stack.push(left - right);
                } else if (token.equals("*")) {
                    stack.push(left * right);
                } else {
                    stack.push(left / right);
                }
            } else {
                stack.push(Integer.parseInt(token));
            }
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        System.out.println(evaluate("2 3 4 * +"));
        System.out.println(evaluate("20 4 /"));
        System.out.println(evaluate("5 1 2 + 4 * + 3 -"));
    }
}
"""

LESSON = workshop(
    "ws-arrays-stacks", "Workshop: stacks",
    "Use stacks to solve problems: a browser's back and forward buttons, a postfix calculator, a palindrome checker and a binary converter.",
    ["Keep history with a stack, and undo it in reverse order",
     "Evaluate postfix expressions by pushing operands and popping them for each operator",
     "Reverse a sequence by pushing it and popping it back"],
    guided("ws-u13-browser", "Back and forward buttons", "Build a browser history: the back button returns to the most recent page, which is exactly what a stack gives you.", [
        step("Visiting pages", "Create `Browser` with a private `String current` (set by the constructor) and a private `Deque<String> back`. `visit(page)` pushes the current page onto `back`, then makes `page` current. Add `getCurrent()`. In `BrowserTester`, start at `home`, visit `news` and `sports`, and print the current page.",
             {"Browser.java": B1, "BrowserTester.java": BT1}, "BrowserTester", "sports",
             checks=[{"pattern": r"Deque<String>", "message": "Keep the history in a `Deque<String>`."}]),
        step("The back button", "Add `back()`: if `back` is empty, print `Can't go back`; otherwise pop it into `current`. Go back three times, printing the page after each.",
             {"Browser.java": B2, "BrowserTester.java": BT2}, "BrowserTester", "news\nhome\nCan't go back\nhome",
             hint="On the third `back()`, the stack is empty, so the message prints and the page stays `home`."),
        step("The forward button", "Add a second stack, `forward`. `back()` now pushes the current page onto `forward` before popping `back`. Add `forward()`, the mirror image (message `Can't go forward`). Visiting a new page clears `forward` with `forward.clear()`, as real browsers do.",
             {"Browser.java": B3, "BrowserTester.java": BT3}, "BrowserTester", "news\nCan't go forward\nnews",
             hint="Trace it: back twice reaches `home`, forward returns to `news`. Visiting `weather` clears `forward`, so `forward()` fails, and `back()` returns to `news`."),
    ]),
    guided("ws-u13-postfix", "A postfix calculator", "In postfix notation the operator comes after its operands: `3 4 +` means 3 + 4. No brackets are needed, and a stack evaluates it in one pass.", [
        step("Numbers only", "In `Postfix`, write `evaluate(String expression)`: split it on spaces, push each token as an `int` (`Integer.parseInt`), and return the top of the stack at the end.",
             {"Postfix.java": P1}, "Postfix", "42\n3"),
        step("Adding and subtracting", "When the token is `+` or `-`, pop the **right** operand first, then the left, and push the result. Order matters for `-`: `10 4 -` is 10 − 4.",
             {"Postfix.java": P2}, "Postfix", "7\n6\n-2",
             hint="Compare strings with `equals`, not `==`."),
        step("All four operators", "Add `*` and `/` (integer division). `5 1 2 + 4 * + 3 -` is 5 + (1 + 2) × 4 − 3.",
             {"Postfix.java": P3}, "Postfix", "14\n5\n14"),
    ]),
    task("ws-u13-palindrome", "Palindrome checker",
         "Write `Palindrome` with `public static boolean isPalindrome(String word)`: push every character onto a `Deque<Character>`, then pop them to build the reversed word, and compare it with the original using `equals`. `main` prints the result for `racecar`, `stack` and `a`.",
         {"Palindrome.java": IMPORTS + """public class Palindrome {
    public static boolean isPalindrome(String word) {
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < word.length(); i++) {
            stack.push(word.charAt(i));
        }
        String reversed = "";
        while (!stack.isEmpty()) {
            reversed += stack.pop();
        }
        return reversed.equals(word);
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("racecar"));
        System.out.println(isPalindrome("stack"));
        System.out.println(isPalindrome("a"));
    }
}
"""}, "Palindrome", "true\nfalse\ntrue",
         tests={"CheckPalindrome.java": """public class CheckPalindrome {
    public static void main(String[] args) {
        System.out.println(Palindrome.isPalindrome("") + " " + Palindrome.isPalindrome("abba") + " " + Palindrome.isPalindrome("abca"));
    }
}
"""}, tests_run="CheckPalindrome", tests_output="true true false",
         checks=[{"pattern": r"\.push\(", "message": "Use the stack: push each character."}]),
    task("ws-u13-binary", "Decimal to binary",
         "To write a number in binary, divide by 2 repeatedly: the remainders, read from last to first, are the binary digits. Write `Binary` with `public static String toBinary(int n)` for `n >= 0`: push each `n % 2` onto a `Deque<Integer>` while dividing `n` by 2, then pop them into a string. `0` gives `\"0\"`. `main` prints `toBinary` of 6, 13 and 0.",
         {"Binary.java": IMPORTS + """public class Binary {
    public static String toBinary(int n) {
        if (n == 0) {
            return "0";
        }
        Deque<Integer> digits = new ArrayDeque<>();
        while (n > 0) {
            digits.push(n % 2);
            n = n / 2;
        }
        String result = "";
        while (!digits.isEmpty()) {
            result += digits.pop();
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(toBinary(6));
        System.out.println(toBinary(13));
        System.out.println(toBinary(0));
    }
}
"""}, "Binary", "110\n1101\n0",
         tests={"CheckBinary.java": """public class CheckBinary {
    public static void main(String[] args) {
        System.out.println(Binary.toBinary(1) + " " + Binary.toBinary(8) + " " + Binary.toBinary(255));
    }
}
"""}, tests_run="CheckBinary", tests_output="1 1000 11111111",
         hints=["13 % 2 is 1, 6 % 2 is 0, 3 % 2 is 1, 1 % 2 is 1. Popping gives them in reverse: 1101."]),
    [DEQUE_API, ARRAYDEQUE_API, ALGS4_13, OPENDSA_STACK],
)
