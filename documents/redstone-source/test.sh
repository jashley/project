#!/bin/sh

echo "Please provide the path to the folder containing mce.py: "
read PATHTO
echo "Please provide the name of a file where the commands will be housed: "
read FILE
echo "Please provide the name of the world which will house the circuit (must be an existing world): "
read WORLD
echo "Please type in a Boolean expression to evaluate"
read EXPR

python boolToFill.py $FILE $WORLD $EXPR
python "$PATHTO"mce.py < $FILE