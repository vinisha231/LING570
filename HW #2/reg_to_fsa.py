#!/usr/bin/env python3
# usage: python3 reg_to_fsa.py <input_filename> <output_filename>
import sys
def read_grammar(gram_fname):
    """returns the start symbol and a list of rules, each rule = (lhs, terminal, rhs_nonterm or None)"""
    f_in = open(gram_fname, "r")
    rule_list = []
    start_sym = None
    for one_line in f_in:
        parts = one_line.split()
        if len(parts) == 0:
            continue
        if start_sym is None:
            start_sym = parts[0] #lhs of 1st line is the start symbol
        if len(parts) == 3:
            rule_list.append((parts[0], parts[1], parts[2])) #A t B
        elif len(parts) == 2:
            rule_list.append((parts[0], parts[1], None)) #A t
    f_in.close()
    return start_sym, rule_list

def main():
    if len(sys.argv) != 3:
        print("Usage: reg_to_fsa.sh <input_filename> <output_filename>")
        sys.exit(1)
    in_fname = sys.argv[1]
    out_fname = sys.argv[2]
    start_sym, rule_list = read_grammar(in_fname)

    #all non-terminals, so we need to make sure the new final state name is not one of them
    nonterm_set = set()
    for (lhs, term, rhs) in rule_list:
        nonterm_set.add(lhs)
        if rhs is not None:
            nonterm_set.add(rhs)

    final_state = "qf"
    count = 1
    while final_state in nonterm_set:
        final_state = "qf" + str(count) #qf1, qf2, ...
        count += 1

    f_out = open(out_fname, "w")
    f_out.write(final_state + "\n")
    for (lhs, term, rhs) in rule_list:
        if term == "*e*":
            sym_str = "*e*"
        else:
            sym_str = '"' + term + '"'
        if rhs is None:
            dst_state = final_state #A => t  goes to the final state
        else:
            dst_state = rhs #A => t B
        f_out.write("(" + lhs + " (" + dst_state + " " + sym_str + "))\n")
    f_out.close()

if __name__ == "__main__":
    main()