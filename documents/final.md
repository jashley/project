# Final write-up

## Introduction
This is LogiCraft. It is a language for automatically constructing logic gates in Minecraft. For those Minecrafters who cannot
be bothered to build their own circuitry and would rather download code to do it for them, this is the code for you! Honestly,
though, this code could be very useful for Minecrafters who, while working on homework in a logic class, want to make sure their
expression does what they think it should do. The main drive behind this language is to hide as much as possible from the user.
When I use a program, I do not want to specify more than I need to, and neither should users of my language. It is automating
a very narrow task, and thus should be very quick and easy to run, which I think it is.

## Language Design Details
To write a program in this language, the user first must install a few required libraries, then write a shell script. The script
simply runs another script with two additional arguments: the world in which to put the circuit, and the logic expression. 
That's it. A program is a header and an sh command. 

Because it is so straightforward to write a program, users need have little-
to-no programming knowledge. Instead of having to use the interface language themselves or, godforbid, place blocks in minecraft,
they just need to write a few lines in a text file. 

The computation is made up of two parts: the first is getting the user input into an AST of expressions and operators. The second
takes this AST and transforms it into commands to fill certain regions of the world with certain blocks to make a working circuit.

The only major data structure is the list of lists representing my AST halfway through my program's execution. The user can
create data at the start by specifying their expression. Beyond that, there is no manipulation of the data.

There really is no major control structure. The language takes data from a shell script, sends it to python, writes to a text
file, then builds in Minecraft. The user does not manipulate the control flow.

As illustrated by the previous two statements, the user has very little control of what goes on in the language. This is an
intentional decision on my part. I wanted to create a language as easy to use as possible, and did not want to require my users
to go mucking about and actually code anything. Simple input to complex output.

On the note of input/output, the input to the program is a shell script written by the user. In it, the user specifies the name
of their Minecraft world and their Boolean circuit (a^    ~b |   ~ x, for example). The output of the program is a new structure
in their Minecraft world representing the expression they typed in.

The only point of failure is in parsing the user's input. Beyond that, everything is hidden. Thus, the only issues arise in the
shuntokenize method of boolToFill.py. Because the shunting yard algorithm is well-described, I know exactly where the parsing
could fail and why. Thus, I can provide accurate error reporting to the user, telling them that they have mismatched parentheses
or that I do not recognize the symbol *. These errors are all sent through python print statements.

No tool support or error-handling support is provided, nor is any needed. The interaction is limited to the point that, in my
opinion, those features would be useless.

The only other DSL is actually a superset of my DSL: MCEdit. MCEdit provides a whole assortment of ways t interact with and
control your minecraft worlds. Theoretically, everything my code does is possible in MCEdit. However, where MCEdit has many
features and a steep learning curve, LogiCraft has one basic task and is incredibly streamlined as a result.

#### Example Program

As an example, say you wanted to build a circuit representing x and y or z in your world called Testara. 
To get this in Minecraft, you create a shell script of the form:

\#!/SHELL

sh writer.sh Testara x^y|z

And that is it. After saving, run sh [NameOfTheShellScript].sh and, in a few moments, the circuit will be built.

## Language Implementation

The host language I chose is Python. Aside from being very easy to code in (in my opinion, at least), the available code
for interfacing programmatically with Minecraft is in Python, which made the choice quite easy.

This is very much an external DSL. The user does not come close to executing python code, aside from downloading required
packages. It provides a window into a small subset of a single python package. I did not want the users to have to have coding
knowledge, meaning I wanted the user to not use python. This made an external DSL a requirement.

The front-end of this language is very raw. The user has to create a shell script and execute it through the command line. The
middle-end is probably the scripts I have that handle getting command line arguments and running the appropriate python files.
The back end is certainly boolToFill.py, which handles all the nitty gritty of parsing the language, creatig an AST, and writing
very convoluted syntax for building in Minecraft. The only technologies I used were the command line and python packages.

The parsing is handled by an algorithm called <a href="http://en.wikipedia.org/wiki/Shunting-yard_algorithm">Shunting Yard</a>.
It takes input made up of symbols and operators and organizes them according to precedence rules. If you are curious, check the
Wikipedia link above for a detailed description. After that, I take the output and parse it into Reverse Polish Notation for
easier evaluation later.

This parsed product is the internal representation: a list of lists representing precedence order for the various operators and
their arguments. This is a pseudo-AST, as each list is made up of an operator and two branches, each of which could be more
operator lists.

From their, the AST is translated into text instructions for building in Minecraft. The structure of this part is a recursive
function commandify that calls the appropriate builders for AND, OR, and NOT gates. These builders handle the writing of the
build instructions, then call commandify on their children. As I am writing this, I realize I implemented a type of mutual
recursion, where each subsequent call reduces the size of the input until we reach a base case. I haven't thought about mutual
recursion since CS60. As far as differing semantics, the user is simply not writing in Python. The semantics are that of a
shell script, not valid python code at all.

## Evaluation





