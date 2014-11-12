I like the idea you've translated into --- it's something pretty unique, and a
lot easier to use for someone familiar with Boolean logic but not Minecraft.  I
can also see how it would be easier to build large structures using your DSL,
or using the DSL as a tool for learning/visualizing Boolean logic.

As for the IR -> Minecraft side, if you make your AST something like a tree:

    a v (b ^ c) => expr a
                    operator OR
                    operand (expr b
                              operator AND
                              operand c)

then you can probably wrangle something where you have preset Minecraft circuit
parts for OR and AND, which have a set spot for left and right operands.  So it
would look like this:

    expr a
     operator OR
     operand (expr b
               operator AND
               operand c)

     ||
     ||
     \/

     OR ---- a
          |
           --- (expr b
                 operator AND
                 operand c)

     ||
     ||
     \/

     OR ---- a
          |
           --- AND --- b
                    |
                    --- c

This would be not too bad (maybe?) if you had the Minecraft API calls to build
gates, or at least API calls that you could compose into sevaral gate-building
function with two arguments (something like `expr OR(expr left, expr right)`).
