First off, I have never played Minecraft. I have seen others play the 
game every once in awhile, but this is the limit of my expertise. 
With that out of the way, I've spent the last hour or so trying to 
familiarize myself with your project. I took a read through your
design documents and the last couple weeks of feedback. If I am 
understanding your progress properly for your notebook, 
you have reached a state where
you have a working parser and a defined AST. Cool! It would be nice 
however if that code was online somewhere that I could look at and
perhaps comment on. I haven't been able to find any code in this repo,
but maybe I missed something.

In terms of your scala/python integration, you will likely have a bad 
time. My team has dealt with this too over the past week. Take a look
at our code to see how we did it (it'll be in `taskerator.py`, 
search for `subprocess.Popen` to find the exact format that I have used).
Essentially, we are communicating with our scala parser/semantics as if
it is a unix utility. We pass it input as a string and retrieve output
as a string. This is probably the best you can do although it is definitely 
not fast or pretty. We are considering moving our scala component to 
a service model, but we have not implemented this yet.

For a format for inter-process communication, JSON likely would work great,
especially if you are trying to pass around the entire AST. If you have a 
more specific data structure to pass around, you might still look at something
like JSON given its wide adoption. 

However, with all of this said, I would still suggest caution when deciding
to attempt to integrate multiple languages. The only reason my team has decided
to do this is that it is a requirement for us to Python to interact with Sublime.
We also found python's language support to be lacking, so we wanted to use Scala.
You may come to the same conclusion, but be aware that using multiple languages
in a small project like this may add more complexity and ugliness
than you really want.

Regarding wire crossings, switches, and large boolean expressions, I have no 
idea what is reasonable in Minecraft. For wire crossings, 
a touch of googling reveals that the problem you are looking at is 
determining the [crossing number of a graph](http://en.wikipedia.org/wiki/Crossing_number_%28graph_theory%29).
That wikipedia article asserts the problem is NP-hard, but that efficient approximation algorithms 
exist. I would think some further research would turn out an algorithm 
or even a ready-made implementation for you to take advantage of.

Best,
Nick