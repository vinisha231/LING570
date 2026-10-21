import sys
import math

def read_lm(lm_path):
    #Read the modified-ARPA LM file; return three dicts: ngram tuple -> probability.
    p1, p2, p3={}, {}, {}
    section=0
    with open(lm_path) as f:
        for line in f:
            line=line.strip()
            if line=="\\1-grams:":
                section=1
            elif line=="\\2-grams:":
                section=2
            elif line=="\\3-grams:":
                section=3
            elif section > 0 and line and not line.startswith("\\"):
                parts=line.split() #count prob logprob w1 ... wn
                prob=float(parts[1])
                ngram=tuple(parts[3:])
                if section==1:
                    p1[ngram]=prob
                elif section==2:
                    p2[ngram]=prob
                else:
                    p3[ngram]=prob
    return p1, p2, p3

def score(p1, p2, p3, l1, l2, l3, test_path, out_path):
    #Compute interpolated log-probs for the test data and write the ppl report.
    total_lg=0.0
    word_num = sent_num= oov_num = 0

    with open(test_path) as f, open(out_path, "w") as out:
        for line in f:
            words=line.split()
            tokens=["<s>"] + words + ["</s>"]
            sent_num += 1
            sent_lg=0.0
            sent_oov=0
            out.write(f"Sent #{sent_num}: {' '.join(tokens)}\n")

            for i in range(1, len(tokens)): #never score <s>
                w=tokens[i]
                history=" ".join(tokens[max(0, i - 2):i]) #1 token at i==1, else 2

                if (w,) not in p1: #if its an unknown word: skip + count
                    sent_oov += 1
                    out.write(f"{i}: lg P({w} | {history})=-inf (unknown word)\n")
                    continue

                #interpolate; a missing bigram/trigram counts as 0
                prob=l1 * p1[(w,)] + l2 * p2.get((tokens[i - 1], w), 0.0)
                if i >= 2:  # trigram needs two real history tokens
                    full=(tokens[i - 2], tokens[i - 1], w)
                    prob += l3 * p3.get(full, 0.0)
                    seen=full in p3
                else: #i==1: highest order available is the bigram
                    seen=(tokens[i - 1], w) in p2

                lg=math.log10(prob)
                sent_lg += lg
                suffix="" if seen else " (unseen ngrams)"
                out.write(f"{i}: lg P({w} | {history})={lg:.10f}{suffix}\n")

            #per-sentence summary
            sent_words=len(words) #includes OOVs, excludes <s> </s>
            sent_ct=sent_words + 1 - sent_oov
            sent_ppl=10 ** (-sent_lg / sent_ct)
            out.write(f"1 sentence, {sent_words} words, {sent_oov} OOVs\n")
            out.write(f"lgprob={sent_lg:.10f} ppl={sent_ppl:.10f}\n")
            out.write("%%\n")
            total_lg += sent_lg
            word_num += sent_words
            oov_num += sent_oov

        #overall summary
        ct=word_num + sent_num - oov_num
        ave_lg=total_lg / ct
        ppl=10 ** (-ave_lg)
        out.write(f"sent_num={sent_num} word_num={word_num} oov_num={oov_num}\n")
        out.write(f"lgprob={total_lg:.10f} ave_lgprob={ave_lg:.10f} ppl={ppl:.10f}\n")

def main(lm_path, l1, l2, l3, test_path, out_path):
    p1, p2, p3=read_lm(lm_path)
    score(p1, p2, p3, float(l1), float(l2), float(l3), test_path, out_path)

if __name__=="__main__":
    main(*sys.argv[1:7])