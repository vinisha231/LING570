import sys
from collections import Counter

def main(train_path, out_path):
    counts = {1: Counter(), 2: Counter(), 3: Counter()}

    with open(train_path) as f:
        for line in f:
            tokens = ["<s>"] + line.split() + ["</s>"] 
            for n in (1, 2, 3):
                for i in range(len(tokens) - n + 1):
                    key = tuple(tokens[i : i + n])
                    counts[n][key] += 1

    with open(out_path, "w") as out:
        for n in (1, 2, 3):
            for ngram, count in sorted(counts[n].items(), key=lambda x: (-x[1], x[0])):
                out.write(f"{count}\t{' '.join(ngram)}\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
