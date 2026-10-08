import sys

def main():
    in_name = sys.argv[1]
    out_name = sys.argv[2]

    counts = {}

    with open(in_name, "r") as fin:
        for line in fin:
            for token in line.split(): 
                if token not in counts:
                    counts[token] = 1
                else:
                    counts[token] += 1

    with open(out_name, "w") as fout:
        for token, freq in counts.items():
            fout.write(f"{token}\t{freq}\n")

if __name__ == "__main__":
    main()