
import sys, statistics

import matplotlib
# matplotlib.use('TkAgg')
matplotlib.use("cairo")
import matplotlib.pyplot as plt

timeout = 4 * 3600

raw = []

with open("outputs/all-info.txt") as f:
    for row in f:
        parts = row.strip().split("\t")
        if len(parts) == 2:
            [a, b] = parts
            [model, param] = a.split("/")
            [param, _] = param.split(".")
            [_, param] = param.split("-")
            [key, value] = b.split(":")
            # print("model: " + model)
            # print("param: " + param)
            # print("key:   " + key)
            # print("value: " + value)
            # print()
            raw.append({ "model" : model
                       , "param" : param
                       , "key"   : key
                       , "value" : value
                       })
        else:
            sys.exit("What? -- " + row + " -- " + str(parts))


modelFace = {}
modelFace['Langford-direct']                         = 'Direct'
modelFace['Langford-direct-wdeg']                    = 'Direct wdeg'
modelFace['Langford-direct-domoverwdeg']             = 'Direct domoverwdeg'
modelFace['Langford-positional']                     = 'Positional'
modelFace['Langford-positional-wdeg']                = 'Positional wdeg'
modelFace['Langford-positional-domoverwdeg']         = 'Positional domoverwdeg'
modelFace['Langford-combined-symD-branchD-consD']    = 'branch:D sym:D cons:D'
modelFace['Langford-combined-symD-branchD-consFull'] = 'branch:D sym:D cons:Both'
modelFace['Langford-combined-symD-branchD-consP']    = 'branch:D sym:D cons:P'
modelFace['Langford-combined-symD-branchP-consD']    = 'branch:P sym:D cons:D'
modelFace['Langford-combined-symD-branchP-consFull'] = 'branch:P sym:D cons:Both'
modelFace['Langford-combined-symD-branchP-consP']    = 'branch:P sym:D cons:P'
modelFace['Langford-combined-symP-branchD-consD']    = 'branch:D sym:P cons:D'
modelFace['Langford-combined-symP-branchD-consFull'] = 'branch:D sym:P cons:Both'
modelFace['Langford-combined-symP-branchD-consP']    = 'branch:D sym:P cons:P'
modelFace['Langford-combined-symP-branchP-consD']    = 'branch:P sym:P cons:D'
modelFace['Langford-combined-symP-branchP-consFull'] = 'branch:P sym:P cons:Both'
modelFace['Langford-combined-symP-branchP-consP']    = 'branch:P sym:P cons:P'
modelFace['Langford-combined-symD-sdf']              = "SDF sym:D"
modelFace['Langford-combined-symP-sdf']              = "SDF sym:P"



# for point in raw:
#     print(point)

def isNumber(n):
    return type(n) == float or type(n) == int

def bool_(s):
    if type(s) == list:
        if len(s) == 0:
            return None
        else:
            return max([ bool_(i) for i in s])
    if s == "0" or s == "NA":
        return False
    elif s == "1":
        return True
    else:
        sys.exit(s)

def int_(s):
    if type(s) == list:
        if len(s) == 1:
            return int_(s[0])
        elif len(s) == 0:
            return None
        else:
            sys.exit("s: " + str(s))
    if s == "NA":
        return 0
    else:
        return int(s)

def float_(s):
    if type(s) == list:
        if len(s) == 1:
            return float_(s[0])
        elif len(s) == 0:
            return None
        else:
            sys.exit("s: " + str(s))
    if s == "NA":
        return 0
    else:
        return float(s)

cpmodels = [ "Langford-direct"
           , "Langford-direct-wdeg"
           , "Langford-direct-domoverwdeg"
           , "Langford-positional"
           , "Langford-positional-wdeg"
           , "Langford-positional-domoverwdeg"
           , "Langford-combined-symD-branchD-consD"
           , "Langford-combined-symD-branchD-consFull"
           , "Langford-combined-symD-branchD-consP"
           , "Langford-combined-symD-branchP-consD"
           , "Langford-combined-symD-branchP-consFull"
           , "Langford-combined-symD-branchP-consP"
           , "Langford-combined-symP-branchD-consD"
           , "Langford-combined-symP-branchD-consFull"
           , "Langford-combined-symP-branchD-consP"
           , "Langford-combined-symP-branchP-consD"
           , "Langford-combined-symP-branchP-consFull"
           , "Langford-combined-symP-branchP-consP"
           , "Langford-combined-symD-sdf"
           , "Langford-combined-symP-sdf"
           ]


def get(model, param):
    found = [ entry for entry in raw
                    if  entry["model"] == model
                    and entry["param"] == param ]

    point = {}

    point["SolverTime"]    = float_([entry["value"] for entry in found if entry["key"] == "SolverTotalTime"    ])

    # SR doesn't report SolverTotalTime for bc_minisat_all for "trivial" problems
    # Put 0
    if len(found) > 0 and model not in cpmodels and point["SolverTime"] == None:
        point["SolverTime"] = 0

    point["Nodes"]         = int_  ([entry["value"] for entry in found if entry["key"] == "SolverNodes"        ])
    point["Timeout"]       = bool_ ([entry["value"] for entry in found if entry["key"].endswith("Out")         ])
    point["Satisfiable"]   = bool_ ([entry["value"] for entry in found if entry["key"] == "SolverSatisfiable"  ])
    point["SavileRowTime"] = float_([entry["value"] for entry in found if entry["key"] == "SavileRowTotalTime" ])
    if point["SolverTime"] == None:
        point["Time"] = None
    else:
        point["Time"] = point["SolverTime"] + point["SavileRowTime"]


    if point["Timeout"]:
        point["SolverSolutionsFound"] = None
    elif point["Satisfiable"] == False:
        point["SolverSolutionsFound"] = 0
    else:
        point["SolverSolutionsFound"] = int_  ([entry["value"] for entry in found if entry["key"] == "SolverSolutionsFound"        ])

    # if model == "o-direct" and param == "langford_02_11":
    #     sys.exit("\n".join([str(x) for x in found])
    #             + "\n\n"
    #             + "\n".join([str(x) for x in point.items()]))

    return point

models = []
for x in raw:
    y = x["model"]
    if y not in models:
        models.append(y)

params = []
for x in raw:
    y = x["param"]
    if y not in params:
        params.append(y)

print("Models: " + str(len(models)))
print("Params: " + str(len(params)))

print("Models (" + str(len(models)) + "): " + str(models))
# print("Params (" + str(len(params)) + "): " + str(params))


# for m in models:
#     for p in params:
#         info = get(m, p)
#         print(m + " " + p + " " + str(info))


withlegend = True


def plotNodes(selectedModels, sortby, prefix, pyscale="symlog"):
    # for p in params:
    #     parts = []
    #     parts.append(p)
    #     for m in selectedModels:
    #         info = get(m, p)
    #         if info == {}:
    #             parts.append("NA")
    #         else:
    #             parts.append(str(info["Nodes"]))
    #     print("\t".join(parts))

    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":12}
    plt.rc("font", **font)
    # plt.rcParams["text.usetex"] = True

    # plt.title("Linkage Quality w.r.t. Threshold", fontsize=22)
    # plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Instances")
    plt.ylabel("Node count")

    allPoints = []
    for m in selectedModels:
        for p in params:
            x = get(m,p)
            if "Nodes" in x.keys() and isNumber(x["Nodes"]):
                allPoints.append(x["Nodes"])
            # else:
            #     sys.exit("What? -- " + str(x))

    order = []
    for p in params:
        x = get(sortby, p)
        if "Nodes" in x.keys() and isNumber(x["Nodes"]):
            if x["Nodes"] >= 0:
                order.append((x["Nodes"], p))
        else:
            print("Missing: %s -- %s" % (p, sortby))

    paramsOrdered = []
    for x in sorted(order):
        paramsOrdered.append(x[1])

    plt.xlim(1, len(paramsOrdered) + 1)
    plt.ylim(min(allPoints), max(allPoints) + 200000000)
    plt.grid()

    for m in selectedModels:
        ix = []
        vals = []
        for i, p in enumerate(paramsOrdered):
            x = get(m, p)
            if "Nodes" in x.keys() and isNumber(x["Nodes"]):
                if pyscale == "linear" and int(x["Nodes"]) <= 1000:
                    pass
                else:
                    # print(x["Nodes"])
                    ix.append(i)
                    vals.append(x["Nodes"])
            else:
                # print(x)
                # ix.append(i)
                # vals.append(300000000)
                pass
        plt.scatter( ix
                , vals
                # , color="blue"
                # , marker="o"
                # , linestyle="-."
                , label=modelFace[m]
                , linewidth=3.0
                )

    # if withlegend:
    #     plt.legend(bbox_to_anchor=(1,0), loc="lower right")
    #     # plt.legend(bbox_to_anchor=(1.5, 1), borderaxespad=0)
    #     # plt.margins(x=1, y=1)

    plt.ticklabel_format(useOffset=False, style='plain', axis='y')
    plt.yscale(pyscale)

    # plt.xticks( [ i for i,p in enumerate(paramsOrdered) ] , paramsOrdered )

    # plt.show()

    # plt.savefig("plots/plot-Nodes.png", bbox_inches="tight")
    plt.savefig("plots/plot-%s-Nodes.png" % prefix)
    plt.legend()
    plt.savefig("plots/plot-%s-Nodes-legend.png" % prefix)
    plt.close()


plotNodes(["Langford-direct", "Langford-positional"], "Langford-positional", "noch")
plotNodes(["Langford-direct-wdeg", "Langford-direct-domoverwdeg", "Langford-positional-wdeg", "Langford-positional-domoverwdeg"], "Langford-positional-domoverwdeg", "noch-wdeg")
plotNodes(["Langford-direct-domoverwdeg", "Langford-positional-domoverwdeg"], "Langford-positional-domoverwdeg", "noch-domoverwdeg")
plotNodes(["Langford-direct", "Langford-positional", "Langford-direct-domoverwdeg", "Langford-positional-domoverwdeg"], "Langford-positional-domoverwdeg", "noch-domoverwdegplus")
plotNodes(["Langford-positional-domoverwdeg", "Langford-combined-symD-sdf", "Langford-combined-symP-sdf"], "Langford-combined-symD-sdf", "SDF")
plotNodes(["Langford-combined-symD-sdf", "Langford-combined-symD-branchD-consFull"], "Langford-combined-symD-branchD-consFull", "FINAL")
plotNodes(["Langford-combined-symD-branchD-consFull", "Langford-combined-symP-branchD-consFull", "Langford-combined-symP-branchP-consFull", "Langford-combined-symD-branchP-consFull"], "Langford-combined-symD-branchD-consFull", "allchannelled")

plotNodes(["Langford-combined-symD-branchD-consFull", "Langford-combined-symP-branchP-consFull"], "Langford-combined-symD-branchD-consFull", "branchDvsP")

plotNodes(["Langford-combined-symD-branchD-consFull", "Langford-direct"], "Langford-combined-symD-branchD-consFull", "directs")
plotNodes(["Langford-combined-symP-branchP-consFull", "Langford-positional"], "Langford-combined-symP-branchP-consFull", "positionals")



plotNodes(cpmodels, "Langford-combined-symD-branchD-consFull", "all")




def plotSolverTime(selectedModels, sortby, prefix, timeField):
    # for p in params:
    #     parts = []
    #     parts.append(p)
    #     for m in selectedModels:
    #         info = get(m, p)
    #         if info == {}:
    #             parts.append("NA")
    #         else:
    #             parts.append(str(info[timeField]))
    #     print("\t".join(parts))

    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":12}
    plt.rc("font", **font)
    # plt.rcParams["text.usetex"] = True

    # plt.title("Linkage Quality w.r.t. Threshold", fontsize=22)
    # plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Instances")
    plt.ylabel("Time")

    allPoints = []
    for m in selectedModels:
        for p in params:
            x = get(m,p)
            if timeField in x.keys() and isNumber(x[timeField]):
                allPoints.append(x[timeField])
            # else:
            #     sys.exit("What? -- " + str(x))

    order = []
    for p in params:
        x = get(sortby, p)
        if timeField in x.keys() and isNumber(x[timeField]):
            if x[timeField] >= 5:
                order.append((x[timeField], p))
        else:
            print("Missing: %s -- %s" % (p, timeField))

    paramsOrdered = []
    for x in sorted(order):
        paramsOrdered.append(x[1])

    plt.xlim(1, len(paramsOrdered) + 1)
    if len(allPoints) > 0:
        plt.ylim(min(allPoints), max(allPoints))
    plt.grid()

    for m in selectedModels:
        ix = []
        vals = []
        for i, p in enumerate(paramsOrdered):
            x = get(m, p)
            if timeField in x.keys() and isNumber(x[timeField]):
                # print(x[timeField])
                ix.append(i)
                vals.append(x[timeField])
            else:
                # print(x)
                # ix.append(i)
                # vals.append(timeout)
                pass
        plt.scatter( ix
                   , vals
                   # , color="blue"
                   # , marker="o"
                   # , linestyle="-."
                   , label=m
                   , linewidth=3.0
                   )

    # if withlegend:
    #     plt.legend()

    plt.ticklabel_format(useOffset=False, style='plain', axis='y')
    # plt.yscale('symlog')

    # plt.xticks( [ i for i,p in enumerate(paramsOrdered) ] , paramsOrdered )

    # plt.show()

    # plt.savefig("plots/plot-SolverTime.png", bbox_inches="tight")
    plt.savefig("plots/plot-%s-%s.png" % (prefix, timeField))
    plt.legend()
    plt.savefig("plots/plot-%s-%s-legend.png" % (prefix, timeField))
    plt.close()

plotSolverTime(models, "Langford-combined-symD-branchD-consFull", "all", "Time")
plotSolverTime(models, "Langford-combined-symD-branchD-consFull", "all", "SolverTime")
plotSolverTime(models, "Langford-combined-symD-branchD-consFull", "all", "SavileRowTime")
plotSolverTime(models, "Langford-combined-symD-branchD-consFull", "all", "SolverSolutionsFound")

plotSolverTime(["Langford-direct", "Langford-positional"], "Langford-combined-symD-branchD-consFull", "noch", "Time")
plotSolverTime(["Langford-direct", "Langford-positional"], "Langford-combined-symD-branchD-consFull", "noch", "SolverTime")
plotSolverTime(["Langford-direct", "Langford-positional"], "Langford-combined-symD-branchD-consFull", "noch", "SavileRowTime")
plotSolverTime(["Langford-direct", "Langford-positional"], "Langford-combined-symD-branchD-consFull", "noch", "SolverSolutionsFound")







def paramFormat(s):
    [_, k, n] = s.split("_")
    return "%s_%s" % (k,n)

import locale
locale.setlocale(locale.LC_ALL, 'en_US')
    
def numberFormat(n):
    s = locale.format_string("%.2f", n, grouping=True)
    if s.endswith(".00"):
        s = s[:-3]
    return s

for timefield in ["Time", "SolverTime", "SavileRowTime", "Nodes", "SolverSolutionsFound"]:
    times = {}

    # only do cpmodels for Nodes
    selectModels = models
    if timefield == "Nodes":
        selectModels = cpmodels

    for m in selectModels:
        times[m] = []
        for p in params:
            x = get(m,p)
            if isNumber(x[timefield]):
                times[m].append(x[timefield])
            elif timefield == "Nodes" or timefield == "SolverSolutionsFound":
                # times[m].append(timeout)
                pass
            else:
                times[m].append(timeout)

    with open("plots/table-%s.tex" % timefield, "w") as f:

        print("\\begin{tabular}{r", file=f, end="")
        for m in selectModels:
            print("R{15mm}", file=f, end="")
        print("r}", file=f)

        print("Instance &", file=f, end="\t")
        for m in selectModels:
            print("%s &" % modelFace[m], file=f, end="\t")
        print("\\tabularnewline \\hline", file=f)

        if timefield != "SolverSolutionsFound":
            print("Sum &", file=f, end="\t")
            for m in selectModels:
                print("%s &" % numberFormat(sum(times[m])), file=f, end="\t")
            print("\\tabularnewline \\hline", file=f)

            print("Mean &", file=f, end="\t")
            for m in selectModels:
                if len(times[m]) > 0:
                    print("%s &" % numberFormat(statistics.mean(times[m])), file=f, end="\t")
                else:
                    print("- &", file=f, end="\t")
            print("\\tabularnewline \\hline", file=f)

        for p in params:
            print("%s &" % paramFormat(p), file=f, end="\t")
            for m in selectModels:
                x = get(m,p)
                if isNumber(x[timefield]):
                    print("%s &" % numberFormat(x[timefield]), file=f, end="\t")
                else:
                    print("- &", file=f, end="\t")
            print("\\tabularnewline \\hline", file=f)

        print("\\end{tabular}", file=f)


    with open("plots/table-%s.html" % timefield, "w") as f:

        print("<table>", file=f)

        print("<tr>", file=f)
        print("<th>Instance</th>", file=f)
        for m in selectModels:
            print("<th>%s</th>" % modelFace[m], file=f)
        print("</tr>", file=f)

        if timefield != "SolverSolutionsFound":
            print("<tr>", file=f)
            print("<th>Sum</th>", file=f)
            for m in selectModels:
                print("<td align=\"right\">%s</td>" % numberFormat(sum(times[m])), file=f)
            print("</tr>", file=f)

            print("<tr>", file=f)
            print("<th>Mean</th>", file=f)
            for m in selectModels:
                if len(times[m]) > 0:
                    print("<td align=\"right\">%s</td>" % numberFormat(statistics.mean(times[m])), file=f)
                else:
                    print("<td>-</td>", file=f)
            print("</tr>", file=f)

        for p in params:
            print("<tr>", file=f)
            print("<th>%s</th>" % paramFormat(p), file=f)
            for m in selectModels:
                x = get(m,p)
                if isNumber(x[timefield]):
                    print("<td align=\"right\">%s</td>" % numberFormat(x[timefield]), file=f)
                else:
                    print("<td>-</td>", file=f)
            print("</tr>", file=f)

        print("</table>", file=f)


    with open("plots/table-%s.tsv" % timefield, "w") as f:

        print("Instance", file=f, end="\t")
        for m in selectModels:
            print("%s" % modelFace[m], file=f, end="\t")
        print("", file=f)

        if timefield != "SolverSolutionsFound":
            print("Sum", file=f, end="\t")
            for m in selectModels:
                print("%s" % numberFormat(sum(times[m])), file=f, end="\t")
            print("", file=f)

            print("Mean", file=f, end="\t")
            for m in selectModels:
                if len(times[m]) > 0:
                    print("%s" % numberFormat(statistics.mean(times[m])), file=f, end="\t")
                else:
                    print("-", file=f, end="\t")
            print("", file=f)

        for p in params:
            print("%s" % paramFormat(p), file=f, end="\t")
            for m in selectModels:
                x = get(m,p)
                if isNumber(x[timefield]):
                    print("%s" % numberFormat(x[timefield]), file=f, end="\t")
                else:
                    print("-", file=f, end="\t")
            print("", file=f)
