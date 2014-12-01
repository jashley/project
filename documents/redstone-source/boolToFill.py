import re, sys, math
from collections import deque

op_dict = {}
op_dict["|"] = 2
op_dict["&"] = 3
op_dict["^"] = 3
op_dict["!"] = 4
op_dict["~"] = 4

and_sym = "&^"
or_sym = "|"
not_sym = "~!"

unary_sym = not_sym
binary_sym = and_sym+or_sym

word = re.compile(r'\w+')

def shuntokenize(expr):
    output = deque([])
    op_stack = []

    tokens = deque(re.split('(\W)', expr))
    while (len(tokens) > 0):
        tok = tokens.popleft()
        if (len(tok) == 0):
            continue
        if (word.match(tok)):
            output.append(tok)
        elif (tok in op_dict):
            tok_prec = op_dict[tok]
            while (len(op_stack) != 0 and op_stack[-1] in op_dict):
                if tok_prec <= op_dict[op_stack[-1]]:
                    output.append(op_stack.pop())
                    continue
                break
            op_stack.append(tok)
        elif (tok == "("):
            op_stack.append(tok)
        elif (tok == ")"):
            while (op_stack[-1] != "("):
                output.append(op_stack.pop())
                if (len(op_stack) == 0):
                    print "mismatched parentheses"
                    return
            op_stack.pop()
        else:
            print "unrecognized token: "+tok
            return
    while (len(op_stack) > 0):
        op = op_stack.pop()
        if (op in "()"):
            print "mismatched parentheses"
            return
        output.append(op)
    return output

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

def or_builder(commands, xz_coords, f):
    size = commands[-1]
    num_blocks = int(math.pow(2, size) + 1)

    stoneline = str(xz_coords[0]-1) + " -1 " + str(xz_coords[1]-num_blocks/2)
    redstoneline = str(xz_coords[0]-1) + " 0 " + str(xz_coords[1]-num_blocks/2)
    outputSpot = str(xz_coords[0]) + " -1 " +str(xz_coords[1])

    f.write("fill 1 Player delta "+ stoneline +" 1 1 "+ str(num_blocks)+"\n")
    f.write("fill 55 Player delta "+ redstoneline +" 1 1 "+str(num_blocks)+"\n")
    f.write("fill 93:1 Player delta "+ outputSpot +" 1 1 1\n")

    left = commands[1]
    right = commands[2]
    leadInList = [xz_coords[0]-2, xz_coords[1]-num_blocks/2]
    leadInSpot = str(leadInList[0]) + " -1 " +str(leadInList[1])
    if (type(commands[1]) == type("")):
        f.write("fill 69:2 Player delta "+leadInSpot+" 1 1 1\n")
    else:
        commandify(commands[1], leadInList, f)
    leadInList = [xz_coords[0]-2, xz_coords[1]+num_blocks/2]
    leadInSpot = str(leadInList[0]) + " -1 " +str(leadInList[1])
    if (type(commands[2]) == type("")):
        f.write("fill 69:2 Player delta "+leadInSpot+" 1 1 1\n")
    else:
        commandify(commands[2], leadInList, f)

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

    left = commands[1]
    right = commands[2]
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

def not_builder(commands, xz_coords, f):

    stoneSpot = str(xz_coords[0]-2) + " -1 " + str(xz_coords[1])
    torchSpot = str(xz_coords[0]-1) + " -1 " + str(xz_coords[1])
    outputSpot = str(xz_coords[0]) + " -1 " + str(xz_coords[1])
    f.write("fill 1 Player delta "+stoneSpot+" 1 1 1\n")
    f.write("fill 76:1 Player delta "+torchSpot+" 1 1 1\n")
    f.write("fill 93:1 Player delta "+outputSpot+" 1 1 1\n")

    right = commands[1]
    leadInList = [xz_coords[0]-3, xz_coords[1]]
    leadInSpot = str(leadInList[0]) + " -1 " +str(leadInList[1])
    if (type(commands[1]) == type("")):
        f.write("fill 69:2 Player delta "+leadInSpot+" 1 1 1\n")
    else:
        commandify(commands[1], leadInList, f)
    
    

def commandify(commands, xz_coords, f):
    if (commands[0] == "OR"):
        or_builder(commands, xz_coords, f)
    elif (commands[0] == "AND"):
        and_builder(commands, xz_coords, f)
    else:
        not_builder(commands, xz_coords, f)
        
    

def boilerplate(commands, xz_coords, world, filename):
    f = open(filename, 'w')
    f.write(world+"\n")
    commandify(commands, xz_coords, f)
    f.write("quit\nyes\n")
    f.close()

def main():
    if (len(sys.argv) != 4):
        print "Please provide 4 commands"
        return
    filename = sys.argv[1]
    world = sys.argv[2]
    expr = re.sub(r"\s", "", sys.argv[3])
    boolList = listify(expr)
    if (type(boolList) != type([])):
        return
    boilerplate(boolList, [0,0], world, filename)

if __name__ == "__main__": main()
    
    
    
    


            
            
        
