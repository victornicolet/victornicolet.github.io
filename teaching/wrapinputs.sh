#!/bin/sh

for project_no in 1 2 3 4 5
do
    tar -cvf "project"$project_no"inputs.tar" -T "p"$project_no"inputs"
done
