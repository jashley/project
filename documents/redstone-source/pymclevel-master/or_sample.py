import mclevel

while True:
    try:
        world = raw_input("Please enter world name or path to world folder: ")
        level = mclevel.loadWorld(world)
    except EOFError, e:
        print "End of input."
        raise SystemExit
    except Exception, e:
        print "Cannot open {0}: {1}".format(world, e)
    else:
        break

print level
