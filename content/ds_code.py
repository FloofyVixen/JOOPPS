"""Shared Java classes for units 13-21 (stacks, linked structures, queues).
Every lesson that uses one of these compiles and runs it through build.py.

Conventions (from the COS 225 Exam 2 guide):
  stacks: push, pop, peek, isEmpty, size; empty pops throw java.util.EmptyStackException
  queues: enqueue, dequeue, getFront, isEmpty, size; empty dequeues throw NoSuchElementException
  nodes:  a data payload and a reference to the next node; getNext()/setNext()
toString() prints the state in the text format the site draws as a diagram:
  "bottom [a, b] top", "front [a, b] rear", "head -> a -> b -> null", "[a, b, _, _] top=2"
"""

STACK_ADT = """public interface StackADT<T> {
    void push(T element);

    T pop();

    T peek();

    boolean isEmpty();

    int size();
}
"""

ARRAY_STACK = """import java.util.EmptyStackException;

public class ArrayStack<T> implements StackADT<T> {
    private Object[] stack;
    private int top;

    public ArrayStack() {
        stack = new Object[4];
        top = 0;
    }

    @Override
    public void push(T element) {
        if (top == stack.length) {
            expandCapacity();
        }
        stack[top] = element;
        top++;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        top--;
        T result = (T) stack[top];
        stack[top] = null;
        return result;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return (T) stack[top - 1];
    }

    @Override
    public boolean isEmpty() {
        return top == 0;
    }

    @Override
    public int size() {
        return top;
    }

    private void expandCapacity() {
        Object[] bigger = new Object[stack.length * 2];
        for (int i = 0; i < top; i++) {
            bigger[i] = stack[i];
        }
        stack = bigger;
    }

    @Override
    public String toString() {
        String result = "bottom [";
        for (int i = 0; i < top; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += stack[i];
        }
        return result + "] top";
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
        return result + "] top=" + top;
    }
}
"""

# ---- unit 16: a node with an int payload ----
NODE = """public class Node {
    private int data;
    private Node next;

    public Node(int data) {
        this.data = data;
        this.next = null;
    }

    public int getData() {
        return data;
    }

    public Node getNext() {
        return next;
    }

    public void setNext(Node next) {
        this.next = next;
    }
}
"""

# ---- unit 17 onward: a generic node ----
LINEAR_NODE = """public class LinearNode<T> {
    private T element;
    private LinearNode<T> next;

    public LinearNode(T element) {
        this.element = element;
        this.next = null;
    }

    public T getElement() {
        return element;
    }

    public LinearNode<T> getNext() {
        return next;
    }

    public void setNext(LinearNode<T> next) {
        this.next = next;
    }
}
"""

LINKED_STACK = """import java.util.EmptyStackException;

public class LinkedStack<T> implements StackADT<T> {
    private LinearNode<T> top;
    private int count;

    public LinkedStack() {
        top = null;
        count = 0;
    }

    @Override
    public void push(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        node.setNext(top);
        top = node;
        count++;
    }

    @Override
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T result = top.getElement();
        top = top.getNext();
        count--;
        return result;
    }

    @Override
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return top.getElement();
    }

    @Override
    public boolean isEmpty() {
        return top == null;
    }

    @Override
    public int size() {
        return count;
    }

    // The chain of nodes from the top: the head of the list is the top of the stack.
    @Override
    public String toString() {
        String result = "head";
        LinearNode<T> current = top;
        while (current != null) {
            result += " -> " + current.getElement();
            current = current.getNext();
        }
        return result + " -> null";
    }
}
"""

QUEUE_ADT = """public interface QueueADT<T> {
    void enqueue(T element);

    T dequeue();

    T getFront();

    boolean isEmpty();

    int size();
}
"""

# Front always at index 0: dequeue shifts everything left.
ARRAY_QUEUE = """import java.util.NoSuchElementException;

public class ArrayQueue<T> implements QueueADT<T> {
    private Object[] queue;
    private int rear;

    public ArrayQueue() {
        queue = new Object[4];
        rear = 0;
    }

    @Override
    public void enqueue(T element) {
        if (rear == queue.length) {
            expandCapacity();
        }
        queue[rear] = element;
        rear++;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        T result = (T) queue[0];
        for (int i = 0; i < rear - 1; i++) {
            queue[i] = queue[i + 1];
        }
        rear--;
        queue[rear] = null;
        return result;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T getFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        return (T) queue[0];
    }

    @Override
    public boolean isEmpty() {
        return rear == 0;
    }

    @Override
    public int size() {
        return rear;
    }

    private void expandCapacity() {
        Object[] bigger = new Object[queue.length * 2];
        for (int i = 0; i < rear; i++) {
            bigger[i] = queue[i];
        }
        queue = bigger;
    }

    @Override
    public String toString() {
        String result = "front [";
        for (int i = 0; i < rear; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += queue[i];
        }
        return result + "] rear";
    }

    // Every slot of the array, for drawing it: _ marks an empty slot.
    public String arrayString() {
        String result = "[";
        for (int i = 0; i < queue.length; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += (queue[i] == null) ? "_" : queue[i];
        }
        return result + "] front=0 rear=" + rear;
    }
}
"""

# Front and rear both move and wrap around: no shifting.
CIRCULAR_QUEUE = """import java.util.NoSuchElementException;

public class CircularArrayQueue<T> implements QueueADT<T> {
    private Object[] queue;
    private int front;
    private int rear;
    private int count;

    public CircularArrayQueue() {
        queue = new Object[4];
        front = 0;
        rear = 0;
        count = 0;
    }

    @Override
    public void enqueue(T element) {
        if (count == queue.length) {
            expandCapacity();
        }
        queue[rear] = element;
        rear = (rear + 1) % queue.length;
        count++;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        T result = (T) queue[front];
        queue[front] = null;
        front = (front + 1) % queue.length;
        count--;
        return result;
    }

    @SuppressWarnings("unchecked")
    @Override
    public T getFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        return (T) queue[front];
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
        Object[] bigger = new Object[queue.length * 2];
        for (int i = 0; i < count; i++) {
            bigger[i] = queue[(front + i) % queue.length];
        }
        front = 0;
        rear = count;
        queue = bigger;
    }

    @Override
    public String toString() {
        String result = "front [";
        for (int i = 0; i < count; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += queue[(front + i) % queue.length];
        }
        return result + "] rear";
    }

    // Every slot of the array, for drawing it: _ marks an empty slot.
    public String arrayString() {
        String result = "[";
        for (int i = 0; i < queue.length; i++) {
            if (i > 0) {
                result += ", ";
            }
            result += (queue[i] == null) ? "_" : queue[i];
        }
        return result + "] front=" + front + " rear=" + rear;
    }
}
"""

LINKED_QUEUE = """import java.util.NoSuchElementException;

public class LinkedQueue<T> implements QueueADT<T> {
    private LinearNode<T> front;
    private LinearNode<T> rear;
    private int count;

    public LinkedQueue() {
        front = null;
        rear = null;
        count = 0;
    }

    @Override
    public void enqueue(T element) {
        LinearNode<T> node = new LinearNode<>(element);
        if (isEmpty()) {
            front = node;
        } else {
            rear.setNext(node);
        }
        rear = node;
        count++;
    }

    @Override
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        T result = front.getElement();
        front = front.getNext();
        count--;
        if (isEmpty()) {
            rear = null;
        }
        return result;
    }

    @Override
    public T getFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("queue is empty");
        }
        return front.getElement();
    }

    @Override
    public boolean isEmpty() {
        return count == 0;
    }

    @Override
    public int size() {
        return count;
    }

    @Override
    public String toString() {
        String result = "front [";
        LinearNode<T> current = front;
        while (current != null) {
            result += current.getElement();
            if (current.getNext() != null) {
                result += ", ";
            }
            current = current.getNext();
        }
        return result + "] rear";
    }
}
"""

STACK_FILES = {"StackADT.java": STACK_ADT, "ArrayStack.java": ARRAY_STACK}
LSTACK_FILES = {"StackADT.java": STACK_ADT, "LinearNode.java": LINEAR_NODE, "LinkedStack.java": LINKED_STACK}
QUEUE_FILES = {"QueueADT.java": QUEUE_ADT, "ArrayQueue.java": ARRAY_QUEUE}
CQUEUE_FILES = {"QueueADT.java": QUEUE_ADT, "CircularArrayQueue.java": CIRCULAR_QUEUE}
LQUEUE_FILES = {"QueueADT.java": QUEUE_ADT, "LinearNode.java": LINEAR_NODE, "LinkedQueue.java": LINKED_QUEUE}


def main_class(name, body, imports=""):
    """A tester class whose main method is `body` (already indented 8 spaces)."""
    return (imports + "\n" if imports else "") + f"public class {name} {{\n    public static void main(String[] args) {{\n{body}    }}\n}}\n"


def lines(*stmts):
    return "".join("        " + s + "\n" for s in stmts)
