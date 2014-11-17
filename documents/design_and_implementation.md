# Language design and implementation overview

## Language design
1. To write a program, the user types out Boolean logic statements (ie xvy^z)
2. The language takes this string, parses it into logical functions, then translates it to Minecraft circuitry.
3. There is no major data structure. The input is a string, the output is a function, translated into a Minecraft map.
4. The user has little control over the language. Aside from specifying the input string, the rest is handled behind the scenes.
5. As said above, the input is a string, the output is a .dat file containing the Minecraft map.
6. The only point of error is if the input string is not properly formatted. There will be nice error messages, though I have not implemented these yet.
7. There may be a gui, but it will likely be a program run through the command line or an ide like Eclipse.
8. There is a DSL, which allows users to graphically represent Minecraft circuitry, which is then translated into a .dat file. This is somewhat different, as it does not require knowledge of how Minecraft circuitry works. If you can type in Boolean logic, you are all set.

## Language implementation
1. This is an external DSL. External DSLs make it very easy to abstract away the details of the implementation, and I believe it is very similar to the external-lab we did in class.
2. I chose Scala for the reasoning above. It seemed to mesh with the previous Scala projects.
3. I don't believe so. The most significant is using {v,^,!} for logical operators, as they are the common symbols.
4. Ideally, the program takes, as input, a string, which is a Boolean logic statement. The program then parses said input into functions, such that "xvy^z" becomes Or(Var(x), And(Var(y),Var(z))). This will then be translated into Minecraft circuitry, where these logical functions will already have a hard-coded design. This will be saved as a .dat file and will be produced as output.

## Note
I forgot this was due last night, but better late than never.
