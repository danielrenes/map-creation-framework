#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./paths_to_list.sh <filepath>"
    exit 1
fi

FILE=$1

sed 's/Path/\nPath/gI' $FILE |\
sed 's/Point/\nPoint/gI' |\
sed 's/^.*latitude\=\(.*\),\slongitude\=\(.*\)),\sheading.*$/\t[\1, \2],/gI' |\
sed 's/Points=\[/[/gI' |\
sed 's/Path(/],/gI' |\
sed '$s/$/\n]/' |\
sed -n '3,$p' > $FILE
