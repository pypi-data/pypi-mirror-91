# Tess

Manage your algorithms' implementations to be run against prepared and 
auto-generated test cases. Apply Stress Testing to detect issues when 
implementing new algorithms. Compare algorithms written in different languages 
with ease.

## Installation
Tess hasn't been tested on _Windows_, so if you are on a _Windows_ machine, we 
recommend you to use a _Linux_ distribution. You can access this 
[link](https://docs.microsoft.com/en-us/windows/wsl/install-win10) 
to learn how to install it.

### Dependencies
Before installing Tess, please make sure you have installed these dependencies:

* [Python](https://www.python.org/downloads/) >= 3.7 
* [Pip](https://pip.pypa.io/en/stable/installing/)
* [GCC](https://gcc.gnu.org/install/) (with support for C++14)
* [OpenJDK](https://openjdk.java.net/install/)

### Download
Run the next command from your terminal to download and install Tess:

    pip install tess-cli
    
## Setup
After installing Tess and all its dependencies, it is recommended to enable
the auto-completion feature for your terminal. Tess supports auto-completion
for _**bash**_, _**zsh**_, and _**fish**_ shells. Run the next command to create
a shell script that will be used by your terminal to recognize Tess commands.

    tess auto-complete /location/where/you/want/to/store/the/script.sh

A file named _**tess-completion.sh**_ will be created at your specified 
location. Now, you need to add the next line to your `.bashrc` or `.zshrc` file.

    . /location/tess-completion.sh
    
>Remember to replace the path with the one where the file was created in the
>previous step.

If you are using _MacOSX_ you might have issues with the _**zsh**_ terminal. If,
after sourcing from your `.zshrc` the auto-completion script you see an error,
or the Tess commands are not being auto-completed, you can add two extra lines
on top of the previous one to enable the auto-completion for the shell. Your
`.zshrc` file should look like this:

    autoload -Uz compinit
    compinit
    . /location/tess-completion.sh

Now, you should be able to start using Tess with its auto-completion feature on.

## Getting Started
After completing the installation and setup of the auto-completion feature, 
you're ready to go. Now, let's create your first Tess project for a very simple
algorithmic problem, computing the sum of an array of numbers.

### Project Initialization
The first step is to initialize a Tess project; for that, you have this command: 

    tess init -e
    
That command will create the required project structure for Tess to work. By 
default, Tess will create a couple of sample files for you to test the tool but, 
we want an empty project to work with, that's why the `-e` option.

>If you want the sample files from one of the supported languages run this
>command:

    tess init -l [py|cpp|java]

Now, you should see three directories (`solutions`, `cases`, `build`) and one
file named `generator.py`.

### Project Structure
Any Tess project will have the next structure:

* **Solutions:** Here you have to save all your source files containing the
implementations for a given algorithm. Avoid creating new sub-directories here,
otherwise Tess won't be able to find your source files.
* **Cases:** This directory will contain files containing the test cases needed to
test manually our algorithms, this files usually are `.txt` files but, you can
use any valid input file extension.
* **Build:** All the compiled files will be here.

>This project structure is created by default, do not modify the location or
>name of any of the directories or the `generator.py` file.

### Running an Algorithm
To run an algorithm from the `solutions` directory you have to type the next
command:

    tess run FILENAME [TESTCASE]
    
Where the *FILENAME* is the name of the source file of your algorithm, i.e.
*sum.cpp* and the *TESTCASE* is an optional argument, where you can specify the
name of one of the test cases that you have in you `cases` directory. Let's say
you have a *sum.cpp* file in your `solutions` directory and two test cases in
your `cases` directory (*sample-1.in*, *sample-2.in*); if you want to run all
your test cases you simply call the run command like this:

    tess run sum.cpp 
    
Without passing the *TESTCASE* argument, otherwise if you want to run the 
*sample-1.in* test case, you should pass it as the *TESTCASE* argument, like
this:

    tess run sum.cpp sample-1.in
    
>***Important:*** It's highly recommended to use the auto-completion script to 
>find the available files for every command quick and easy. If you are not using
>this feature, remember to use the file names as arguments, not its absolute or
>relative paths.

### Debug Mode
Tess has a simple yet, useful feature to allow you to debug your algorithms
using native comments. To use this feature you need to append the `@log` 
annotation to your comments; this annotation will tell Tess to uncomment those
lines of code whenever you run the algorithm in debug mode, which can be done 
using this option:

    tess run --debug sum.cpp

#### Log Annotation Rules
For this annotation to work properly, please always append the annotation next
to the open comment symbol used by the programming language of your preference.
For single line comments you have to leave just **one** white space between the
annotation and the actual code you want to be executed when the comments are
removed; for block comments the annotation should be alone in the opening line.

Here you can see examples of how to use the annotation properly:

##### Python
````python
def fn():
    #@log print('This is a single line debug comment.')

    """@log
    print('This is a block debug comment.')
    """
    pass
```` 

>Always try to keep the indentation correct when working with Python.

##### C++/Java
````c++
void fn() {
    //@log std::cout << "This is a single line debug comment.\n";

    /*@log
    std::cout << "This is a block debug comment.\n";
    */
}
````

### Stress Testing
To execute a stress testing you need at least two algorithms; one that will work
as a ***Model*** and another one that will be the ***Solution*** to be tested. 
The model is usually a naive implementation to solve an algorithmic problem, 
this model could be very inefficient and slow but, will give us the right answer 
to the problem. On the other hand, we have the solution, which is the new,
efficient and optimized algorithm that we've created. Often times, things does
not work as expected and we are not going to have infinite number of prepared
test cases to find bugs, here's where stress testing and Tess come in. 

To execute the stress testing you can type in your terminal this command:

    tess stress MODEL SOLUTION 

Passing the names of the files that you want to treat as the model and the 
solution.

>***Important:*** When working with C++ or Java, remember to compile the source
>files before executing the stress testing. You can use this command to do so:

    tess build [FILENAME]
    
#### The Generator
When you press `<ENTER>`, a prompt will ask you for some arguments:

    Arguments (separated by spaces):
    
You can think of them like the arguments you pass to a console program, i.e. 
`./myprogram arg1 arg2`. These arguments are used by the `generator.py` sitting
in the root of your Tess project. This generator file is the one responsible for
the creation of the auto-generated test cases that will be executed during the 
stress testing process.

For instance, if you pass the next arguments to the stress testing command:

    Arguments (separtaed by spaces): 10 Hello

You can access them from the generator file like this:

````python
def test_case(args, random) -> str:
    num = int(args[0]) # 10
    greet = args[1] # Hello
    pass
````

>The arguments array is zero-indexed.

You can use those arguments to modify the behaviour of your randomly generated
test cases.

The generator have a second parameter called ***random***, this is just a
reference of the random object used by Python to generate pseudo-random numbers.

>You can change the seed of this random instance using the `--seed` option 
>available from the `stress` command.

Finally, after you implement the logic needed to generate your desired test
case, you have to return a ***string*** containing the test case with the
required format to be read by your algorithms from the standard I/O.

>If you initialize the project with the sample files, you can see a simple
>implementation of the generator that produces random test cases.

#### The Execution
At this point you should have these things ready:

1. A model or naive (but correct) algorithm.
2. A solution that you want to test for correctness.
3. A generator that will produce strings following the input format needed by
your algorithms.

Now, you can run the stress testing and hope that your new algorithm is correct.
The stress testing will run infinitely, you have to abort the process to stop 
it by typing `CTLR+C`; or you can pass the `--number` option to the stress 
command letting Tess know how many test cases do you want to created before 
stopping the process.

One last option that you can pass to the stress command is the `--line` one.
This option is useful when some algorithms output does not need to be evaluated
completely. For example, you have an algorithms that outputs these two lines:

    8
    4 2
    
If you want to compare just the first line, you can use the command above
telling Tess to just compare the first line when is executing the stress testing
and ignore the second one. For this you can run the stress command like this:

    tess stress model.py solution.cpp --line 1
    
### Usage
For a complete list of the commands, options, and usage of Tess, please use
the help command:

    tess --help
    tess COMMAND --help
    
## Contribute
Tess is the result of the testing practices learned from the 
[Algorithmic Toolbox](https://www.coursera.org/learn/algorithmic-toolbox?specialization=data-structures-algorithms)
course offered by [Coursera](https://www.coursera.org/). It is a work in 
progress, aiming to help other students like me enrolled in the [Data Structures 
and Algorithms Specialization](https://www.coursera.org/specializations/data-structures-algorithms) 
to test their algorithms using the stress testing 
approach suggested in the course easing the process and allowing the students to 
use different programming languages to create their models and solutions.

### How can I contribute?
Tess is a new tool looking to grow and help more students and anyone who is 
interested and needs to test algorithms in an efficient and simple way, without 
restricting you to use a particular programming language or IDE. Currently, Tess 
is supporting three programming languages, **Python**, **C++**, and **Java**; 
one of the main goals of Tess is to give support to more programming languages 
but,  as the code base grows and more features are added, the need for a more 
reliable and flexible code is critical to achieving this. Here you can find a 
list of tasks that would help the project to grow and improve the user's 
experience:

* **Unit testing:** This is the top priority at this point.
* **Testing and reporting issues:** You can contribute using the tool and 
reporting any bugs to my [email](mailto:andressbox90@gmail.com).
* **Documentation:** This documentation could be incomplete. Any contributions
to improve it would be very helpful. The code is not documented, this is 
critical to make it easier for more developers to join in, task that I have to
begin as soon as possible.
* **OOP migration:** Any contributions refactoring code to make it more 
object-oriented would be very appreciated. 

Please feel free to [contact me](mailto:andressbox90@gmail.com) to report 
something else that is not part of this documentation or if you want more 
information about the project and how to contribute.