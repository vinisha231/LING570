universe = vanilla
executable = ./ppl.sh
arguments = "./wsj_sec0_19.lm 0.05 0.15 0.8 /mnt/dropbox/26-27/570/hw3/examples/wsj_sec22.word ./ppl_0.05_0.15_0.8"
getenv = true
request_memory = 4*1024
output = ppl.out
error = ppl.error
log = ppl.log
notification = never
queue
