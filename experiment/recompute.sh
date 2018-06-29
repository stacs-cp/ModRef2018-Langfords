
mkdir -p outputs

# run the following command for the Minion
parallel \
    --joblog  gnuparallel/joblog-Minion \
    --results gnuparallel/results-Minion \
    --timeout 4h \
    --eta \
    "conjure solve {2} {1} --number-of-solutions all -o outputs/{2/.} --copy-solutions=no --solutions-in-one-file" ::: params/*.param ::: models/*.essence

# and the following for the SAT
# parallel --joblog joblog-sat --results results-sat --timeout 4h --eta -j16 "conjure solve Langford-{2}.essence {1} --solver bc_minisat_all --number-of-solutions all -o o-sat-{2} --copy-solutions=no --solutions-in-one-file" ::: params/*.param ::: direct positional combinedDirect

# and following to generate the "all-info.txt" file
# parallel -j1 --tag cat ::: o-*/*info > all-info.txt


# this script will produce the tables and the plots
# python3 plot.py && bash append.sh >> ../Nugget034.md

