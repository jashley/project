# Preliminary evaluation

#### What works well? What are you particularly pleased with

The code I have successfully takes in a Bollean expression and translates it into a Minecraft circuit. The input expression
can contain and, or, and not expressions, as well as any amount of whitepace and parentheses. I spent a while trying to use
parsing libraries, but ended up writing my own parser, using the shunting yard algorithm. That was really fun to write, as
was the translation from its output (in reverse polish notation) to a tree of gates (ie [AND [OR x y] z]). Also, this was
my first python project that heavily involved moving things from the command line to python, and I am pleased with how
seamless I have made it, though there is still more work to do.

#### What could be improved? For example, how could the user's experience be better? How might your implementation be simpler or more cohesive?

Right now, the circuitry is gigantic, as I make the gates large enough such that no two circuits overlap. However, most
circuits do not need this amount of space, so I am planning on changing the sizes of each side of the gate to only use
as much space as actually needed. The biggest challenge on the Minecraft side will be getting the inputs all in one place. To
do this, I must implement a way for wires to bridge over each other, which is possible, but will be a lot of work. On the
UX side, the user currently has to enter the directory of a python package, the name of the file to hold the Minecraft 
commands, the name of their Minecraft world, and the Boolean expression to evaluate. I do not think the user should have
to name the file to hold commands they won't even see, so I need some way to make a new text file in the current directory
having a name different than anything currently in the directory. Then, I can do away with that bit. Aside from that, I like
the state of the UI and UX.


#### Re-visit your evaluation plan from the beginning of the project. Which tools have you used to evaluate the quality of your design? What have you learned from these evaluations? Have you made any significant changes as a result of these tools, the critiques, or user tests?

Much of the work for this project was done over Thanksgiving break, so I currently have not had a chance to evaluate it.
When I wrote my Evaluation plan, I also had no idea how I would test it. The easiest way would be to have friends use the
program and get their feedback, which I will likely do this week.

#### Where did you run into trouble and why? For example, did you come up with some syntax that you found difficult to implement, given your host language choice? Did you want to support multiple features, but you had trouble getting them to play well together?

The largest trouble was with parsing packages. Alejandro found success with pyPEG, so I decided to try and use it. 4 hours
later, and I realized that there was no easy way to implement a recursive parser (ie OR -> EXPR OR EXPR). Thus, I scrapped
this and went with building my own parser, which worked wonderfully. The other big issue was getting the whole thing easy
to run. I have a shell script that handles all the calls, but this was the 3rd script I had ever written, and understanding
all the syntax and error messages was tough (pro tip: don't name your variables PATH). The big issues may come up later,
but this is the extent of my troubles so far.

#### What's left to accomplish before the end of the project?

Shrinking the circuitry and having the user only provide three commands are the two features that need to be implemented.
Aside from that, time permitting, I want to have the inputs grouped together for easy toggling, but, as stated above,
that involves crossing wires, which is tough. The DSLs part of the project is done, though, as I have my parser taking
user input and turning it into the language that Minecraft wants to see (ie fill 1 Player delta 0 0 0 1 1 3).
