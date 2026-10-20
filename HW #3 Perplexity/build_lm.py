import sys
import math

def main(count_path, lm_path):
    counts = {1: {}, 2: {}, 3: {}} #n -> {tuple of words: count}

    with open(count_path) as f:
        for line in f:
            parts = line.split() 
            for n in (1, 2, 3):
                if len(parts) == n + 1:
                    count = int(parts[0])
                    ngram = tuple(parts[1:])
                    counts[n][ngram] = count

    with open(lm_path, "w") as out: 
        out.write("\\data\\\n")
        for n in (1, 2, 3):
            types = len(counts[n])
            tokens = sum(counts[n].values())
            out.write(f"ngram {n}: type = {types} tokens = {tokens}\n")   
            #unigram 
            for ngram, count in sorted(counts[1].items(), key=lambda x: (-x[1], x[0])):
                prob = count / sum(counts[1].values())
                log_prob = math.log10(prob)
                out.write(f"{prob:.4f}\t{log_prob:.4f}\t{' '.join(ngram)}\n")
            #bigram    
            for ngram, count in sorted(counts[2].items(), key=lambda x: (-x[1], x[0])):
                    prob = count / counts[1][(ngram[0],)]
                    log_prob = math.log10(prob)
                    out.write(f"{log_prob:.4f}\t{prob:.4f}\t{' '.join(ngram)}\n")
            #trigram
            for ngram, count in sorted(counts[3].items(), key=lambda x: (-x[1], x[0])):
                    prob = count / counts[2][(ngram[0], ngram[1])]
                    log_prob = math.log10(prob)
                    out.write(f"{log_prob:.4f}\t{prob:.4f}\t{' '.join(ngram)}\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])