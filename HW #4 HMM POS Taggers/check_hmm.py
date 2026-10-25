#!/usr/bin/env python3
import sys, math
from collections import OrderedDict

TOL = 1e-6

def fmt(x):
    return f"{round(x, 6):g}"

def main(in_file, out_file):
    header = {}
    section= None
    init, trans, emit = OrderedDict(), OrderedDict(), OrderedDict()
    counts = {"init": 0, "trans": 0, "emiss": 0}
    states = OrderedDict() #first-seen order
    syms = set()
    warns = []

    with open(in_file) as f:
        for line in f:
            s= line.strip()
            if not s:
                continue
            if s.startswith("\\"):
                section= s[1:]
                continue
            if section is None:
                k, v= s.split("=")
                header[k] = int(v)
                continue
            parts= s.split()
            try:
                if section == "init":
                    st, p= parts[0], float(parts[1])
                    init[st] = p
                    states[st] = 1
                    counts["init"] += 1
                    lg = parts[2:] and float(parts[2])
                elif section == "transition":
                    a, b, p= parts[0], parts[1], float(parts[2])
                    trans.setdefault(a, OrderedDict())[b] = p
                    states[a] = 1; states[b] = 1
                    counts["trans"] += 1
                    lg = parts[3:] and float(parts[3])
                elif section == "emission":
                    st, w, p= parts[0], parts[1], float(parts[2])
                    emit.setdefault(st, OrderedDict())[w] = p
                    states[st] = 1
                    syms.add(w)
                    counts["emiss"] += 1
                    lg= parts[3:] and float(parts[3])
            except (ValueError, IndexError):
                warns.append(f"warning: malformed line in {section}: {s}")
                continue
            if not (0< p <= 1):
                warns.append(f"warning: prob out of range in {section}: {s}")
            if lg and p > 0 and abs(lg - math.log10(p)) > 1e-3:
                warns.append(f"warning: lg_prob mismatch in {section}: {s}")
    out=[]
    def cmp(name, claimed, real):
        if claimed == real:
            out.append(f"{name}={real}")
        else:
            out.append(f"warning: different numbers of {name}: claimed={claimed}, real={real}")
    cmp("state_num", header.get("state_num"), len(states))
    cmp("sym_num", header.get("sym_num"), len(syms))
    cmp("init_line_num", header.get("init_line_num"), counts["init"])
    cmp("trans_line_num", header.get("trans_line_num"), counts["trans"])
    cmp("emission_line_num", header.get("emiss_line_num"), counts["emiss"])

    tot= sum(init.values())
    if abs(tot - 1) > TOL:
        out.append(f"warning: the init_prob_sum is {fmt(tot)}")
    for st in states:
        t= sum(trans.get(st, {}).values())
        if abs(t - 1) > TOL:
            out.append(f"warning: the trans_prob_sum for state {st} is {fmt(t)}")
    for st in states:
        e= sum(emit.get(st, {}).values())
        if abs(e - 1) > TOL:
            out.append(f"warning: the emiss_prob_sum for state {st} is {fmt(e)}")

    with open(out_file, "w") as o:
        o.write("\n".join(out + warns) + "\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])