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

This language is so DSL-y that I fell bad calling it a language at all. I realize that almost anything could be a DSL, but this
is essentially a program that takes a shell script and returns a structure in Minecraft. The user, in my mind at least, is not
coding at all. Just adjusting a template to suit their needs. In that sense, it is about as far away as possible from a general
purpose language. Technically, you can create a circuit such that, when executed, runs a Turing machine, but that is very much
not the intended use of the language. All you can do is build a circuit.

The user input is so straightforward. I am so pleased that I got the input down to creating a single shell script with two
inputs. I take real enjoyment out of using programs like pip or brew, as they seem to have reduced their user input to the
barest possible form. I like to think that I have taken on this philosophy successfully. Additionally, I like how little the
user has to do as far as downloading requirements. In a future version, I may just include a script that installs the necessary
files, but, aside from that, the user has very little to do. If you haven't caught on, I am really happy at how lazy the user
can be and still run my code.

SO MANY THINGS could be improved. I mentioned one above, how there could be a script that simply installs the necessary
packages. Going from there, I could make my program a small python package, where you could essentially type

pip install logicraft

Then run logicraft.generateCircuit(world, expr) inside python. That would be the ultimate ease of use and I'd love to have
that work. As far as the generated structure goes, it could use a lot of refining. First off, the circuit is built way too
big, with long expressions taking up WAY more space than they need to. I thought of a fix, but it requires redesigning the
control flow to build the circuit "bottom-up" so that I know how much space I need for my circuitry. Another issue is the
fact that users have to toggle the levers to initialize the circuit. There is a way to do this automatically, but it requires
me knowing the area that the circuit covers. This is possible to do, but I ran out of time to implement it. Next, the levers
could have signs next to them to indicate which variable they represent. Similar to the previous issue, this is fairly
easy to implement, but I ran out of time. Finally, I would love to be able to combine input lines together so that the
circuit

x^~x

has exactly one lever, not two. This, however, requires building bridges between inputs, meaning I have to extend the build
into the 3rd dimension. This is possible and I have a vague idea of how to do it, but it would take a solid day to work out
the kinks, and I already had kinks that needed ironing that were much easier to smooth out. All of that aside, the final
version of this does not differ to wildly from my initial vision. At the VERY beginning I wanted a GUI to let people design
circuits and place said circuits into Minecraft. In that sense, this is very different, but that was my idea for no more than
a day before I realized that had already been created.

I never created an evaluation plan... :(

About half of this project was running into trouble. The first issue was in finding a way to programmatically place blocks
in Minecraft. There were plenty of ways for placing blocks with an external program and its GUI, but programmatically doing
so was absent. The first solution I found was in something called an MCEdit filter. This is a piece of python code that, when
applied to a specified region of the world, will generate a design. This would have been very easy for me, as I would just
create the code and tell the user to download MCEdit, navigate to the appropriate section, select the region themselves, then
run my code themselves. I felt that was too much work to put on the user. The second idea I had was using a command block, an
item in the game itself. This is incredibly easy for the user to use, as they simply cut and paste code from my program into
the block to build the circuit. However, putting this all in one command block requires nested commands of stone riding
pressure plates riding command blocks, which themselves have nested layers of stone riding...I decided this was too much work
for me, even if it made the user experience much nicer.

After about 4 hours more of searching, I finally found this small part of MCEdit called pymclevel. It is a programmatic
interface between python and Minecraft and even has an 'execute' command that will run a text file of commands. This means
I can just create a text file and be done, while the user simply has to download a package. Great success for all!

After that, I moved onto the problem of parsing. After spending an hour or two wrestling with Scala, I decided, from
Alejandro's advice, to switch to python packages for parsing. After Thanksgiving dinner, I sat down to write the parser. The
following night, I had made 0 progress and had gotten a parser stuck in an infinite loop. Turns out python parsers have
issues with defining and Expr in terms of Expr's. Basically, 12 hours of work down the drain. I came back from break ready to
spend another 12 hours wrestling with the parsers. I asked one of my friends if he had any advice, and he mentioned the
Shunting Yard algorithm. An hour later, and I had a fully functioning parser. An hour after that, I had an AST as a list of
lists in reverse polish notation. 

Finally, I moved on to the non-DSL stage: converting the AST into Minecraft commands. As it turns out, the pymclevel package
does not install correctly, and reports an error about missing minecraft.yaml. However, I could run it from the command line.
This meant the user had to specify the path to their pymclevel folder, which felt so unnecessary. After getting it working
as well as I could, I decided to look into this issue. Turns out that I had to fork the code from github and change setup.py
to get it to work. But, it did, and I managed to get it working in python itself. This was about 10pm tonight. From
10:30-11:30, I was desperately trying to figure out why none of the circuits were showing up in Minecraft. As it turns out,
if you save by quitting from pymclevel and saying you'd like to save, it does not save. You have to save the world, then quit
and say you would like to save. I'd be upset if I had not had 10 times the issues with a python package for another class.

Sorry for the wall of issues here. This had a lot of bumps along the way, but I am so happy I got it working.

## Th-th-th-that's all folks



