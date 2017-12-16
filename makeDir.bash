#!/bin/bash

# PROBLEM: BASH CANNOT DO FLOATING POINTS!! ONLY INTEGERS... use zsh instead

## declare an array of layers
declare -a arr=("element1" "element2" "element3")

## loop through the array
for i in "${arr[@]}"
do
	echo "$i"
	# or do whatever
done

# You can access them using echo "${arr[0]}", "${arr[1]}" also

## having a list of number from integers

END=5
for i in $(seq 1 $END)
do
	echo $i
done



