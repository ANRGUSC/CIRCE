The code in this heft folder is a modified version of the open source code implementation of HEFT 
by Ouyang Liduo at https://github.com/oyld/heft

We have modified the following parts of the code:

- Original implementation displayed the output on the screen. We added a function called output_file to heft_dup.py, which writes an output to a file, in a format that corresponds to the input of our centralized scheduler.
- Computation matrix was fixed in the original implementation. We obtain the matrix values from the application execution profiler - namely from task execution times.
- Egde TYPE in our imeplementation represents the size of the task output data, also obtained from the application execution profiler.
