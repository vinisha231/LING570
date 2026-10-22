universe = vanilla
executable = ./build_lm.sh
arguments = "./wsj_sec0_19.ngram_count ./wsj_sec0_19.lm"
getenv = true
output = build_lm.out
error = build_lm.error
log = build_lm.log
notification = never
queue
