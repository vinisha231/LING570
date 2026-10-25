#!/usr/bin/env python3
import sys, math
from collections import defaultdict

def main(train_file, out_file):
    trans= defaultdict(lambda: defaultdict(int)) #trans[prev][cur] = count
    emit= defaultdict(lambda: defaultdict(int)) #emit[state][word] = count

    with open(train_file) as f:
        for line in f:
            toks = line.split()
            if not toks:
                continue
            prev = "BOS"
            for tok in toks:
                word, tag = tok.rsplit("/", 1) #words keep their "\/" as-is
                trans[prev][tag] += 1
                emit[tag][word] += 1
                prev = tag
            trans[prev]["EOS"] += 1
            emit["EOS"]["</s>"] += 1
    trans_lines, emit_lines = [], []
    states, syms = {"BOS"}, set()
    for frm in sorted(trans):
        tot = sum(trans[frm].values())
        for to in sorted(trans[frm]):
            p = trans[frm][to] / tot
            trans_lines.append(f"{frm} {to} {p:.6f} {math.log10(p):.6f}")
            states.update([frm, to])
    for st in sorted(emit):
        tot = sum(emit[st].values())
        for w in sorted(emit[st]):
            p = emit[st][w] / tot
            emit_lines.append(f"{st} {w} {p:.6f} {math.log10(p):.6f}")
            syms.add(w)

    with open(out_file, "w") as out:
        out.write(f"state_num={len(states)}\nsym_num={len(syms)}\n")
        out.write(f"init_line_num=1\ntrans_line_num={len(trans_lines)}\n")
        out.write(f"emiss_line_num={len(emit_lines)}\n\n")
        out.write("\\init\nBOS 1.0 0.0\n\n\n\\transition\n")
        out.write("\n".join(trans_lines) + "\n\n")
        out.write("\\emission\n" + "\n".join(emit_lines) + "\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])