"""Every source the lessons cite. Only official documentation (Oracle / OpenJDK),
the Java Language Specification, and university courses."""

ORACLE = "Oracle, The Java Tutorials"
DEVJAVA = "Oracle, dev.java"
API = "Oracle, Java SE 21 API docs"
JLS = "Oracle, Java Language Specification (Java SE 21)"
HEL = "University of Helsinki, Java Programming MOOC"


def s(title, url, org, note=None):
    d = {"title": title, "url": url, "org": org}
    if note:
        d["note"] = note
    return d


HELLO_TUT = s("A Closer Look at the \"Hello World!\" Application",
              "https://docs.oracle.com/javase/tutorial/getStarted/application/index.html", ORACLE)
DEV_FIRST = s("Your first Java code", "https://dev.java/learn/first-steps/first-java-code/", DEVJAVA)
JAVAC_MAN = s("The javac command", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html",
              "Oracle, JDK 21 tool docs")
JAVA_MAN = s("The java command", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html",
             "Oracle, JDK 21 tool docs")
HEL_1_1 = s("Part 1.1: Getting started with programming",
            "https://java-programming.mooc.fi/part-1/1-starting-programming", HEL)
HEL_1_2 = s("Part 1.2: Printing", "https://java-programming.mooc.fi/part-1/2-printing", HEL)

VARIABLES = s("Variables", "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/variables.html", ORACLE)
DATATYPES = s("Primitive Data Types",
              "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html", ORACLE)
ARITH = s("Assignment, Arithmetic, and Unary Operators",
          "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/op1.html", ORACLE)
EQUALITY = s("Equality, Relational, and Conditional Operators",
             "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/op2.html", ORACLE)
HEL_1_4 = s("Part 1.4: Variables", "https://java-programming.mooc.fi/part-1/4-variables", HEL)
HEL_1_5 = s("Part 1.5: Calculating with numbers", "https://java-programming.mooc.fi/part-1/5-calculating", HEL)
JLS_DIV = s("15.17.2 Division Operator /",
            "https://docs.oracle.com/javase/specs/jls/se21/html/jls-15.html#jls-15.17.2", JLS)

IF_TUT = s("The if-then and if-then-else Statements",
           "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/if.html", ORACLE)
FOR_TUT = s("The for Statement", "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/for.html", ORACLE)
WHILE_TUT = s("The while and do-while Statements",
              "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/while.html", ORACLE)
HEL_1_6 = s("Part 1.6: Conditional statements",
            "https://java-programming.mooc.fi/part-1/6-conditional-statements", HEL)
HEL_2_2 = s("Part 2.2: Repeating functionality", "https://java-programming.mooc.fi/part-2/2-repeating", HEL)

METHODS_TUT = s("Defining Methods", "https://docs.oracle.com/javase/tutorial/java/javaOO/methods.html", ORACLE)
RETURN_TUT = s("Returning a Value from a Method",
               "https://docs.oracle.com/javase/tutorial/java/javaOO/returnvalue.html", ORACLE)
ARGS_TUT = s("Passing Information to a Method or a Constructor",
             "https://docs.oracle.com/javase/tutorial/java/javaOO/arguments.html", ORACLE)
HEL_2_4 = s("Part 2.4: Methods and dividing the program into smaller parts",
            "https://java-programming.mooc.fi/part-2/4-methods", HEL)

HEL_3_1 = s("Part 3.1: Discovering errors", "https://java-programming.mooc.fi/part-3/1-discovering-errors", HEL)
AIOOBE = s("ArrayIndexOutOfBoundsException",
           "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ArrayIndexOutOfBoundsException.html",
           API)
EXCEPTIONS_TUT = s("What Is an Exception?",
                   "https://docs.oracle.com/javase/tutorial/essential/exceptions/definition.html", ORACLE)
VSCODE_JAVA = s("Language Support for Java by Red Hat (README)",
                "https://github.com/redhat-developer/vscode-java", "Red Hat, VS Code Java extension",
                "Says the extension runs on the Eclipse JDT Language Server, which is why its messages are worded differently from javac's.")

CLASSES_TUT = s("Classes", "https://docs.oracle.com/javase/tutorial/java/javaOO/classes.html", ORACLE)
OBJECTS_TUT = s("Objects", "https://docs.oracle.com/javase/tutorial/java/javaOO/objects.html", ORACLE)
FIELDS_TUT = s("Declaring Member Variables",
               "https://docs.oracle.com/javase/tutorial/java/javaOO/variables.html", ORACLE)
DEV_CLASSES = s("Classes and Objects", "https://dev.java/learn/language/oop/classes-objects/", DEVJAVA)
HEL_4_1 = s("Part 4.1: Introduction to object-oriented programming",
            "https://java-programming.mooc.fi/part-4/1-introduction-to-object-oriented-programming", HEL)
JLS_DEFAULTS = s("4.12.5 Initial Values of Variables",
                 "https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.12.5", JLS)

CONSTRUCTORS_TUT = s("Providing Constructors for Your Classes",
                     "https://docs.oracle.com/javase/tutorial/java/javaOO/constructors.html", ORACLE)
THIS_TUT = s("Using the this Keyword", "https://docs.oracle.com/javase/tutorial/java/javaOO/thiskey.html", ORACLE)
JLS_DEFAULT_CTOR = s("8.8.9 Default Constructor",
                     "https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.8.9", JLS)
HEL_5_2 = s("Part 5.2: Overloading methods and constructors",
            "https://java-programming.mooc.fi/part-5/2-method-and-constructor-overloading", HEL)

OBJECT_TOSTRING = s("Object.toString()",
                    "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#toString()",
                    API)
OBJECT_TUT = s("Object as a Superclass",
               "https://docs.oracle.com/javase/tutorial/java/IandI/objectclass.html", ORACLE)
OVERRIDE_TUT = s("Predefined Annotation Types (@Override)",
                 "https://docs.oracle.com/javase/tutorial/java/annotations/predefined.html", ORACLE)

ACCESS_TUT = s("Controlling Access to Members of a Class",
               "https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html", ORACLE)
NAMING = s("Code Conventions: Naming Conventions",
           "https://www.oracle.com/java/technologies/javase/codeconventions-namingconventions.html",
           "Oracle, Code Conventions for Java")

ARRAYS_TUT = s("Arrays", "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/arrays.html", ORACLE)
JLS_ARRAY_CREATE = s("15.10.2 Run-Time Evaluation of Array Creation Expressions",
                     "https://docs.oracle.com/javase/specs/jls/se21/html/jls-15.html#jls-15.10.2", JLS)
NPE = s("NullPointerException",
        "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/NullPointerException.html", API)
JEP358 = s("JEP 358: Helpful NullPointerExceptions", "https://openjdk.org/jeps/358", "OpenJDK")
STRING_EQUALS = s("String.equals(Object)",
                  "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html#equals(java.lang.Object)",
                  API)
HEL_3_3 = s("Part 3.3: Arrays", "https://java-programming.mooc.fi/part-3/3-arrays", HEL)
HEL_4_2 = s("Part 4.2: Objects in a list", "https://java-programming.mooc.fi/part-4/2-objects-in-a-list", HEL)
