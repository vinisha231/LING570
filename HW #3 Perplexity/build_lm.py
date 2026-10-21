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

    #compute the unigram total once (not inside the loop)
    total_unigrams = sum(counts[1].values())
    with open(lm_path, "w") as out:
        out.write("\\data\\\n\n")
        for n in (1, 2, 3):
            types = len(counts[n])
            tokens = sum(counts[n].values())
            out.write(f"ngram {n}: type = {types} tokens = {tokens}\n\n")

        #unigram
        out.write("\\1-grams:\n")
        for ngram, count in sorted(counts[1].items(), key=lambda x: (-x[1], x[0])):
            prob = count / total_unigrams
            log_prob = math.log10(prob)
            out.write(f"{count} {prob:.10f} {log_prob:.10f} {' '.join(ngram)}\n")

        #bigram
        out.write("\n\\2-grams:\n")
        for ngram, count in sorted(counts[2].items(), key=lambda x: (-x[1], x[0])):
            prob = count / counts[1][(ngram[0],)]
            log_prob = math.log10(prob)
            out.write(f"{count} {prob:.10f} {log_prob:.10f} {' '.join(ngram)}\n")

        #trigram
        out.write("\n\\3-grams:\n")
        for ngram, count in sorted(counts[3].items(), key=lambda x: (-x[1], x[0])):
            prob = count / counts[2][(ngram[0], ngram[1])]
            log_prob = math.log10(prob)
            out.write(f"{count} {prob:.10f} {log_prob:.10f} {' '.join(ngram)}\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])