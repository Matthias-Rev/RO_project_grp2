#!/bin/bash 

NUM_ITER=50

for ((i=0; i<NUM_ITER; i++)); do
	echo "Instance $i is running..."
	output_file="$i.txt"
	python3 main.py > $output_file
done
