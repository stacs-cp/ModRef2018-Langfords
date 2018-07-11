
mkdir -p outputs
mkdir -p logs
mkdir -p plots


# SAT
parallel \
    --joblog  logs/joblog-sat \
    --results logs/results-sat \
    --timeout 4h \
    --eta \
    "conjure solve {2} {1} --number-of-solutions all -o outputs/{2/.}-{3} --copy-solutions=no --solutions-in-one-file --solver {3}" \
    ::: params/*.param \
    ::: models/Langford-direct.essence models/Langford-positional.essence models/Langford-combined-symD-sdf.essence models/Langford-combined-symP-sdf.essence \
    ::: bc_minisat_all nbc_minisat_all

# Minion-static
parallel \
    --joblog  logs/joblog-Minion \
    --results logs/results-Minion \
    --timeout 4h \
    --eta \
    "conjure solve {2} {1} --number-of-solutions all -o outputs/{2/.} --copy-solutions=no --solutions-in-one-file" \
    ::: params/*.param \
    ::: models/*.essence

# Minion-wdeg
parallel \
    --joblog  logs/joblog-Minion-wdegs \
    --results logs/results-Minion-wdegs \
    --timeout 4h \
    --eta \
    "conjure solve {2} {1} --number-of-solutions all -o outputs/{2/.}-{3} --copy-solutions=no --solutions-in-one-file --solver-options='-varorder {3}'" \
    ::: params/*.param \
    ::: models/Langford-direct.essence models/Langford-positional.essence \
    ::: wdeg domoverwdeg

# and following to generate the "all-info.txt" file
(cd outputs ; parallel -j1 --tag cat ::: */*info > all-info.txt)


# this script will produce the tables and the plots
# python3 plot.py
# bash append.sh >> ../Nugget034.md

