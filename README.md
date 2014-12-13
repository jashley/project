# LogiCraft

The code for this project is located in documents/redstone-source.

The writer.sh and builder.sh are helper scripts to generate the minecraft world.

Example programs are provided in sample1.sh (creates a^~b^~c) and uselessMachine.sh (a^~a :}).

To run this yourself, you must first install pymclevel using these two commands in the terminal
  pip install -U numpy PyYaml Cython
  pip install git+https://github.com/jashley/pymclevel
The first command installs required libraries. The second installs the minecraft-python interface. 
My fork of the code fixes an issue with the .yaml files.

Next, create a .sh file of the form of sample1.sh or uselessMachine.sh.
Valid symbols are:
  Not: ~!
  Or: |
  And: ^&
Make sure the level name provided is a superflat world and has already been created
  (it doesn't HAVE to be superflat, but your circuit might end up embedded in a mountain, otherwise)
  
After that, just run:
  sh myscriptname.sh
and load up minecraft. You may have to toggle the levers to force the blocks to update.
