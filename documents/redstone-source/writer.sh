#!/SHELL

FILE=fillCommands.txt
WORLD=$1
LOGIC=$(echo $2 | tr -d ' ')
touch $FILE

python boolToFill.py $FILE $WORLD $LOGIC
python builder.sh