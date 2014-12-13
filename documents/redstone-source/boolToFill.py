import re, sys, math, os
from collections import deque

# the precedences for each logic symbol
op_dict = {}
op_dict["|"] = 2
op_dict["&"] = 3
op_dict["^"] = 3
op_dict["!"] = 4
op_dict["~"] = 4

# what each symbol corresponds to in boolean algebra
and_sym = "&^"
or_sym = "|"
not_sym = "~!"

# which are unary, which are binary
unary_sym = not_sym
binary_sym = and_sym+or_sym

# regex for finding the user's variable names
word = re.compile(r'\w+')

"""
Shunting yard algorithm for parsing boolean algebra
Input: Boolean algebra expression
Output: Queue representing the order of applying operators
"""
def shuntokenize(expr):
    output = deque([])
    op_stack = []

    # get tokens by splitting on non-letter characters
    tokens = deque(re.split('(\W)', expr))
    while (len(tokens) > 0):
        tok = tokens.popleft()
        # invalid token, so we try again from the top
        if (len(tok) == 0):
            continue
        # if it's a variable, enqueue it
        if (word.match(tok)):
            output.append(tok)
            
        # else, if it is an operator symbol
        elif (tok in op_dict):
            # get its precedence
            tok_prec = op_dict[tok]
            
            # while there is a valid operator at the top of the stack
            while (len(op_stack) != 0 and op_stack[-1] in op_dict):
                # if the current token's precedence is not greater than
                # that of the top of the stack, pop the token off the
                # stack and enqueue it into the output
                if tok_prec <= op_dict[op_stack[-1]]:
                    output.append(op_stack.pop())
                    continue
                break
            # this operator has higher precedence than the top of the
            # operator stack, so we push it on
            op_stack.append(tok)

        # push an open paren
        elif (tok == "("):
            op_stack.append(tok)
        # if we hit a closing paren...
        elif (tok == ")"):
            # ...keep enqueuing operators until we see an open paren
            while (op_stack[-1] != "("):
                output.append(op_stack.pop())
                # if there are no more operators then mismatched parens
                if (len(op_stack) == 0):
                    print "mismatched parentheses"
                    return
            # we found the matching paren, now pop it
            op_stack.pop()

        # no idea what this token is
        else:
            print "unrecognized token: "+tok
            return
        
    # now to take care of the remaining operators
    while (len(op_stack) > 0):
        op = op_stack.pop()
        # if one of these is a paren, then mismatched parens
        if (op in "()"):
            print "mismatched parentheses"
            return
        # enqueue the operator
        output.append(op)
    # and return the output queue
    return output

"""
Takes a Boolean expression and transforms it into a list of lists representing
    a tree of operators
Input: a Boolean expression
Output: A list of lists representing a tree of operators and variables
"""
def listify(expr):
    tokens = shuntokenize(expr)
    val_stack = []
    while (len(tokens) != 0):
        tok = tokens.popleft()
        if (word.match(tok)):
            val_stack.append(tok)
        else:
            if (tok in unary_sym):
                if (len(val_stack) == 0):
                    print "too few arguments for unary operator: "+tok
                    return
                r_val = val_stack.pop()
                if (tok in not_sym):
                    new_val = ["NOT", r_val]
                # how many levels lie below this operator on the tree
                nested = 0
                if (type(r_val) == type([])):
                    nested = r_val[-1]
                new_val.append(nested+1)
                val_stack.append(new_val)
            elif (tok in binary_sym):
                if (len(val_stack) < 2):
                    print "too few arguments for binary operator "+tok
                    return
                r_val = val_stack.pop()
                l_val = val_stack.pop()
                if (tok in or_sym):
                    new_val = ["OR", l_val, r_val]
                elif (tok in and_sym):
                    new_val = ["AND", l_val, r_val]
                nested = 0
                if (type(l_val) == type([])):
                    nested = l_val[-1]
                if (type(r_val) == type([])):
                    nested = max(nested, r_val[-1])
                new_val.append(nested+1)
                val_stack.append(new_val)
                
                    
    if (len(val_stack) != 1):
        print "too many values given"
        return
    return val_stack.pop()


"""
Write the text for creating an OR gate in Minecraft
Inputs:
    commands: the tree node (list of lists) representing the OR instruction
    xz_coords: where in the Minecraft world the center of the gate is
    f: the file to write the build commands in
Output: None
"""
def or_builder(commands, xz_coords, f):
    size = commands[-1]
    # the length of the gate increases exponentially based on how many gates
    # come before it
    num_blocks = int(math.pow(2, size) + 1)

    # start locations for the stone base of the gate, the wiring, and the output
    stoneline = str(xz_coords[0]-1) + " -1 " + str(xz_coords[1]-num_blocks/2)
    redstoneline = str(xz_coords[0]-1) + " 0 " + str(xz_coords[1]-num_blocks/2)
    outputSpot = str(xz_coords[0]) + " -1 " +str(xz_coords[1])

    # minecraft jargon to fill the areas with appropriate blocks
    # (1, 55, and 93:1 are data values of blocks in the game)
    f.write("fill 1 Player delta "+ stoneline +" 1 1 "+ str(num_blocks)+"\n")
    f.write("fill 55 Player delta "+ redstoneline +" 1 1 "+str(num_blocks)+"\n")
    f.write("fill 93:1 Player delta "+ outputSpot +" 1 1 1\n")

    # where to put the output of the left input for OR
    leadInList = [xz_coords[0]-2, xz_coords[1]-num_blocks/2]
    leadInSpot = str(leadInList[0]) + " -1 " +str(leadInList[1])

    # if the left input to the OR is a variable, put a lever down
    if (type(commands[1]) == type("")):
        f.write("fill 69:2 Player delta "+leadInSpot+" 1 1 1\n")
    # otherwise, call commandify to generate the other gates
    else:
        commandify(commands[1], leadInList, f)

    # similar function for the right input of OR
    leadInList = [xz_coords[0]-2, xz_coords[1]+num_blocks/2]
    leadInSpot = str(leadInList[0]) + " -1 " +str(leadInList[1])
    if (type(commands[2]) == type("")):
        f.write("fill 69:2 Player delta "+leadInSpot+" 1 1 1\n")
    else:
        commandify(commands[2], leadInList, f)

"""
Write the text for creating an AND gate in Minecraft
Inputs:
    commands: the tree node (list of lists) representing the AND instruction
    xz_coords: where in the Minecraft world the center of the gate is
    f: the file to write the build commands in
Output: None

Note: Much of this follows the template of the OR instruction
"""
def and_builder(commands, xz_coords, f):
    size = commands[-1]
    num_blocks = int(math.pow(2, size) + 1)

    stoneline = str(xz_coords[0]-2) + " -1 " + str(xz_coords[1]-num_blocks/2)
    redstoneline = str(xz_coords[0]-2) + " 0 " + str((xz_coords[1]-num_blocks/2)+1)
    t1Spot = str(xz_coords[0]-2) + " 0 " + str(xz_coords[1]-num_blocks/2)
    t2Spot = str(xz_coords[0]-2) + " 0 " + str(xz_coords[1] + num_blocks/2)
    t3Spot = str(xz_coords[0]-1) + " -1 " + str(xz_coords[1])
    outputSpot = str(xz_coords[0]) + " -1 " +str(xz_coords[1])

    f.write("fill 1 Player delta "+ stoneline +" 1 1 "+ str(num_blocks)+"\n")
    f.write("fill 55 Player delta "+ redstoneline +" 1 1 "+str(num_blocks-2)+"\n")
    f.write("fill 76:5 Player delta "+ t1Spot +" 1 1 1\n")
    f.write("fill 76:5 Player delta "+ t2Spot +" 1 1 1\n")
    f.write("fill 76:1 Player delta "+ t3Spot +" 1 1 1\n")
    f.write("fill 93:1 Player delta "+ outputSpot +" 1 1 1\n")

    leadInList = [xz_coords[0]-3, xz_coords[1]-num_blocks/2]
    leadInSpot = str(leadInList[0]) + " -1 " +str(leadInList[1])
    if (type(commands[1]) == type("")):
        f.write("fill 69:2 Player delta "+leadInSpot+" 1 1 1\n")
    else:
        commandify(commands[1], leadInList, f)
    leadInList = [xz_coords[0]-3, xz_coords[1]+num_blocks/2]
    leadInSpot = str(leadInList[0]) + " -1 " +str(leadInList[1])
    if (type(commands[2]) == type("")):
        f.write("fill 69:2 Player delta "+leadInSpot+" 1 1 1\n")
    else:
        commandify(commands[2], leadInList, f)

"""
Write the text for creating a NOT gate in Minecraft
Inputs:
    commands: the tree node (list of lists) representing the NOT instruction
    xz_coords: where in the Minecraft world the center of the gate is
    f: the file to write the build commands in
Output: None

Note: Much of this follows the template of the OR instruction
"""
def not_builder(commands, xz_coords, f):

    stoneSpot = str(xz_coords[0]-2) + " -1 " + str(xz_coords[1])
    torchSpot = str(xz_coords[0]-1) + " -1 " + str(xz_coords[1])
    outputSpot = str(xz_coords[0]) + " -1 " + str(xz_coords[1])
    f.write("fill 1 Player delta "+stoneSpot+" 1 1 1\n")
    f.write("fill 76:1 Player delta "+torchSpot+" 1 1 1\n")
    f.write("fill 93:1 Player delta "+outputSpot+" 1 1 1\n")

    # only one input
    right = commands[1]
    leadInList = [xz_coords[0]-3, xz_coords[1]]
    leadInSpot = str(leadInList[0]) + " -1 " +str(leadInList[1])
    if (type(commands[1]) == type("")):
        f.write("fill 69:2 Player delta "+leadInSpot+" 1 1 1\n")
    else:
        commandify(commands[1], leadInList, f)

    
"""
Calls the appropriate builders for the next gate
Inputs: Same as the builders
Output: None
"""
def commandify(commands, xz_coords, f):
    if (commands[0] == "OR"):
        or_builder(commands, xz_coords, f)
    elif (commands[0] == "AND"):
        and_builder(commands, xz_coords, f)
    else:
        not_builder(commands, xz_coords, f)


"""
Boilerplate text for the python-minecraft interface
Inputs: Same as the builders, plus the name of the Minecraft world holding
        the gate
Output: None
"""
def boilerplate(commands, xz_coords, world, filename):
    f = open(os.getcwd()+'/'+filename, 'w')
    f.write('load '+world+"\n")
    commandify(commands, xz_coords, f)
    f.write("save\nquit yes\n")
    f.close()

"""
Grabs the command line input, gets the tree for the expression and starts up
the writing.
Input: None
Output: None
"""
def main():
    if (len(sys.argv) != 4):
        print "Please provide 2 arguments"
        return
    filename = sys.argv[1]
    world = sys.argv[2]
    expr = sys.argv[3]
    boolList = listify(expr)
    if (type(boolList) != type([])):
        return
    boilerplate(boolList, [0,0], world, filename)

if __name__ == "__main__": main()
