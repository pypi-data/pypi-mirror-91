# Scierra

Scierra [_see-eh-rah_] is a **S**imulated **C**++ **I**nt**er**preter with **R**ecurrent **A**daptation.

In human words, it's a interactive interpreter for C++, which allows you to run and debug your program immediately as you type. Well, basically. But the implementation is slightly trickier.

To get a quick start, simply launch Scierra on the terminal and type `cout << "Hello, World!";`. Yes, that's a complete C++ program in Scierra!

**WARNING:** Scierra is still under development. Even though many vital aspects of C++ (e.g. function definition, templates, classes) are already supported, Scierra does not handle input statements very well. This is unfortunately keeping Scierra in Beta...

## Navigation

* [Example](#Example)

* [Installation](#Installation)

   * [Prerequisites](#Prerequisites)

   * [Install with PIP](#Install-with-PIP)

* [Usage](#Usage)

   * [Quick Start](#Quick-Start)
   
   * [Keywords](#Keywords)

* [Docs](#Docs)

   * [Anatomy of a C++ Program in Scierra](#Anatomy-of-a-C-Program-in-Scierra)
   
   * [Unsupported features](#Unsupported-features)

* [LICENSE](#LICENSE)

## Example

***An sample program running on the Scierra interpreter:***

```c++
++> cout << "Hello, World!";
Hello, World!
++> int factorial(int n){

-->     if (n==1 || n==0)

-->         return 1;

-->     else return n * factorial(n-1);

--> }

++> cout << "10 factorial is: " << factorial(10);
10 factorial is: 3628800
```

## Installation

### Prerequisites:

* **Python** must be **installed** and **added to PATH**.
   
   The key ideas of Scierra and it's CLI have been implemented in Python.

* **GCC** (GNU Compiler Collection) must be **installed** and **added to PATH**.
   
   This allows Python to access G++ through the command line. If you're a Linux user, there's a good chance that GCC tools are already included in your distro. Users of other operating systems like Windows or MacOS may need to make additional installations. MinGW has been tested to work with Scierra on Windows.

### Install with PIP

Install Scierra with PIP using:

    $ pip install scierra
  
After installation, run Scierra on your terminal using:

    $ scierra

## Usage

### Quick Start

Launch `scierra` in your terminal, and try pasting in the full sample program below.

Note Scierra's ability to automatically categorise whether the block of code you've just typed belongs to the `main` function section, global declarations section, or preprocessors section (refer to the [anatomy of a C++ program in Scierra](#Anatomy-of-a-C-Program-in-Scierra)). The `<esc>` command closes the interpreter.

```c++
cout << "Hello, World!\n";
#define CYAN "\033[36m"
#define GREEN "\033[32m"
#define DEFAULT "\033[0m"
cout << GREEN << "I am SCIERRA" << DEFAULT << endl;

int factorial(int n){
    if (n==1 || n==0)
        return 1;
    else return n * factorial(n-1);
}
cout << CYAN << "10 factorial is: " << factorial(10) << DEFAULT << endl;

<esc>
```

Below is a demo of the above program running in a terminal with Scierra:

![Basic Scierra Demo](static/basic_demo.png "Scierra Basic Demo")

### Keywords

Type these special keywords at any stage when writing your code to perform special functions.

* `<print>`: Prints out the code you've written so far.

* `<restart>`: Restarts another interpreter session and forgets all local variables.

* `<esc>`: Terminates Scierra.

#### Code keywords

Put the following keywords at the start of each block of your code for special operations.

* `<`: Using this keyword before a single-lined statement without any semicolons (e.g. `<10+23` or `<"Hey!"`) makes Scierra automatically output the evaluated value of the statement. It works with all data types, variables and classes that supports `cout` statements. You can even join multiple outputs together! E.g.

    ```c++
    ++> int x = 132;
    
    ++> < x*7
    924
    ++> < x%127 << x%12 << "COOL!"
    50COOL!
    ++> 
    ```
   
* `<prep>`: Forcefully specifies that the block of code that you type belongs to the 'preprocessor' section of the program. E.g.
   
    ```c++
    ++> <prep>
    
    --> const int Answer_to_Ultimate_Question_of_Life = 42;
    
    ++> 
    ```
    
   This puts `const int Answer_to_Ultimate_Question_of_Life = 42;` in the 'preprocessors' section. Without the `<prep>` keyword, this statement would be automatically placed in the `main` function by Scierra.
      
   Refer to: [Anatomy of a C++ Program in Scierra](#Anatomy-of-a-C-Program-in-Scierra).
   
* `<glob>`: Forcefully specifies that the block of code that you type belongs to the 'globals' section of the program.
      
   Refer to: [Anatomy of a C++ Program in Scierra](#Anatomy-of-a-C-Program-in-Scierra).
   
* `<main>`: Forcefully specifies that the block of code that you type belongs to the `main` function in the program.
   
   Refer to: [Anatomy of a C++ Program in Scierra](#Anatomy-of-a-C-Program-in-Scierra).

## Docs

### Anatomy of a C++ Program in Scierra

Scierra divides a C++ program into three distinct sections: the 'preprocessor' section, the 'globals' section, and the 'main' section. Please refer to the [keywords and expressions table](#Keywords-and-Expressions-Table) for the full list of keywords and expressions that Scierra uses to categorise a block of code. However, here is a quick overview:

The 'preprocessor' section comes at the top of the program. This is where libraries are imported and namespaces are defined. By default in Scierra, the libraries `iostream`, `sstream`, `fstream`, `vector` and `string` are already imported, and the namespace `std` is under use. The 'globals' section is reserved for global class and function declarations, while the 'main' section goes into the `main` function of your C++ program.

When you enter a block of code in Scierra, it automatically categorises it into one of these three sections based on syntactical keywords and expressions. You can override this automatic behaviour by using one of the [code keywords](#Code-Keywords).

#### Keywords and Expressions Table

Here is a table showing the different keywords and expressions that Scierra uses to categorise your block of code.

| Preprocessor Section | Globals Section | Main Section |
| :---: | :---: | :---: |
| `#include` statement | `class` keyword | _Anything that doesn't fit into the former two sections_ |
| `#define` statement | `struct` keyword |  |
| `typedef` keyword | `return` keyword |  |
| `using` keyword | `void` keyword |  |
|  | `template` keyword |  |
|  | `typename` keyword |  |

### Unsupported features

Scierra supports most features that come with your installed version of GCC.

However, unfortunately the following features are not yet supported by Scierra:

* any expression involving inputs

* lambda expressions

* range-based for loops

## LICENSE
[Apache License 2.0](LICENSE)
