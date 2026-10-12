universe = vanilla
executable = fsa_acceptor.sh
arguments = "/mnt/dropbox/26-27/570/hw2/examples/fsa1 /mnt/dropbox/26-27/570/hw2/examples/ex q2.out"
getenv = true
transfer_executable = true
should_transfer_files = YES
transfer_input_files = fsa_acceptor.py
when_to_transfer_output = ON_EXIT
output = hw2_fsa.stdout
error = hw2_fsa.error
log = hw2_fsa.log
notification = never
queue