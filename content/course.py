TITLE = "Java Objects, Step by Step"

# Section order follows UMaine COS 225 (Object-Oriented Design, Programming and
# Data Structures), using the University of Helsinki Java MOOC and similar
# university courses where COS 225 materials aren't public.
SECTIONS = [
    {
        "id": "intro",
        "title": "Introduction",
        "blurb": "Write, compile and run Java programs, and learn to read what the compiler tells you.",
        "lessons": ["intro-first-program", "intro-variables", "intro-decisions-loops",
                    "intro-methods", "intro-errors", "intro-workshop"],
    },
    {
        "id": "classes",
        "title": "Classes and objects",
        "blurb": "Design your own types: fields, constructors, toString, private data and arrays of objects.",
        "lessons": ["classes-first-class", "classes-constructors", "classes-tostring",
                    "classes-encapsulation", "classes-arrays", "classes-project-parking"],
    },
    {
        "id": "inheritance",
        "title": "Inheritance",
        "blurb": "Build new classes on top of existing ones with extends and super.",
        "planned": ["Subclasses with extends", "Calling the parent with super",
                    "Overriding methods", "Abstract classes",
                    "Polymorphism and the Object class", "Project: a clothing store"],
    },
    {
        "id": "interfaces",
        "title": "Interfaces",
        "blurb": "Promise what a class can do, and let one class keep several promises.",
        "planned": ["What an interface is", "Implementing more than one interface",
                    "Using an interface as a type", "The Comparable interface",
                    "Project: a smart-home controller"],
    },
    {
        "id": "data-structures",
        "title": "Data structures",
        "blurb": "Abstract data types, generics, and choosing the right structure.",
        "planned": ["Abstract data types", "Interface versus implementation",
                    "Generic classes with <T>", "Measuring cost with Big-O"],
    },
    {
        "id": "arraylist",
        "title": "ArrayList",
        "blurb": "Lists that grow: using ArrayList, then building your own.",
        "planned": ["Using ArrayList", "Removing while you loop",
                    "Wrapper classes and autoboxing", "Building your own ArrayList",
                    "Project: a manager class with a list"],
    },
    {
        "id": "array-stack",
        "title": "Array stack",
        "blurb": "Last in, first out: push, pop and peek on top of an array.",
        "planned": ["The stack ADT", "An array-based stack", "Growing the array",
                    "Project: checking balanced brackets"],
    },
    {
        "id": "algorithms",
        "title": "Algorithms",
        "blurb": "Searching and sorting, and how to reason about their cost.",
        "planned": ["Linear search", "Binary search", "Selection sort", "Insertion sort",
                    "Recursion"],
    },
    {
        "id": "queues",
        "title": "Queues",
        "blurb": "First in, first out: a circular-array queue and Java's own Queue.",
        "planned": ["The queue ADT", "A circular-array queue", "Java's Queue and ArrayDeque",
                    "Project: a print-job line"],
    },
]
