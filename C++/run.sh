#!/bin/bash
loads=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)

for load in ${loads[@]};
do
	echo $load
	./partitioned $load
done
