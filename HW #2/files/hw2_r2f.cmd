universe = vanilla
executable = reg_to_fsa.sh
arguments = "/mnt/dropbox/26-27/570/hw2/examples/reg_ex1 q3.out"
getenv = true
transfer_executable = true
should_transfer_files = YES
transfer_input_files = reg_to_fsa.py
when_to_transfer_output = ON_EXIT
output = hw2_r2f.stdout
error = hw2_r2f.error
log = hw2_r2f.log
notification = never
queue