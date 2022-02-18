#!/bin/bash
STARTROW=5
ENDROW=7
STARTCOL=4
ENDCOL=10

for ((ROW=$STARTROW;ROW<=$ENDROW;ROW++));
do
	for ((COL=$STARTCOL;COL<=$ENDCOL;COL++));
	do
		python3 main.py 2 $ROW $COL
	done
done
