#!/usr/bin/env python3 
#python3 fsa_acceptor.py <fsa_filename> <input_filename> <output_filename>
import re
import sys

#to match a line like:  (q0 (q1 "a"))
edge_pat = re.compile(r'^\(\s*(\S+)\s+\(\s*(\S+)\s+(.+?)\s*\)\s*\)\s*$')

def read_fsa(fsa_fname):
    """reads the fsa file, returns (start_state, final_state, trans_table, is_dfa)"""
    f_in = open(fsa_fname, "r")
    all_lines = []
    for one_line in f_in:
        one_line = one_line.strip()
        if one_line != "":
            all_lines.append(one_line)
    f_in.close()

    #the 1st line is the (only) final state
    final_state = all_lines[0].strip("()").strip()
    trans_table = {} #(state, symbol) -> next state
    start_state = None
    is_dfa = True

    for one_line in all_lines[1:]:
        m = edge_pat.match(one_line)
        if m is None:
            continue
        src_state = m.group(1)
        dst_state = m.group(2)
        sym = m.group(3)

        #first edge tells us the start state
        if start_state is None:
            start_state = src_state

        if sym == "*e*":
            #epsilon arc -> not a DFA
            is_dfa = False
            continue

        #if the symbols are in quotation marks, take them off
        if len(sym) >= 2 and sym[0] == '"' and sym[-1] == '"':
            sym = sym[1:-1]

        key = (src_state, sym)
        if key in trans_table and trans_table[key] != dst_state:
            #same state + same symbol goes to 2 places -> NFA
            is_dfa = False
        trans_table[key] = dst_state
    return start_state, final_state, trans_table, is_dfa

def get_tokens(one_line, alphabet):
    """splits an input line into symbols"""
    tokens = []
    for raw_tok in one_line.split():
        # input symbols can be in quotation marks like "a", take them off
        if len(raw_tok) >= 2 and raw_tok[0] == '"' and raw_tok[-1] == '"':
            raw_tok = raw_tok[1:-1]
        tokens.append(raw_tok)
    # if the string is written without spaces (like aabb) split it into chars
    if len(tokens) == 1 and tokens[0] not in alphabet:
        tokens = list(tokens[0])
    return tokens

def is_accepted(tokens, start_state, final_state, trans_table):
    cur_state = start_state
    for tok in tokens:
        key = (cur_state, tok)
        if key not in trans_table:
            return False #no arc to follow -> reject
        cur_state = trans_table[key]
    return cur_state == final_state

def main():
    if len(sys.argv) != 4:
        print("Usage: fsa_acceptor.sh <fsa_filename> <input_filename> <output_filename>")
        sys.exit(1)
    fsa_fname = sys.argv[1]
    in_fname = sys.argv[2]
    out_fname = sys.argv[3]
    start_state, final_state, trans_table, is_dfa = read_fsa(fsa_fname)

    if not is_dfa:
        print("Error: the input FSA is not a DFA")
        sys.exit(1)

    alphabet = set()
    for (st, sym) in trans_table:
        alphabet.add(sym)

    f_in = open(in_fname, "r")
    f_out = open(out_fname, "w")
    for one_line in f_in:
        one_line = one_line.rstrip("\r\n")
        tokens = get_tokens(one_line, alphabet)
        if is_accepted(tokens, start_state, final_state, trans_table):
            ans = "yes"
        else:
            ans = "no"
        f_out.write(one_line + " => " + ans + "\n")
    f_in.close()
    f_out.close()

if __name__ == "__main__":
    main()