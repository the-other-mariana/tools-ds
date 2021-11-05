import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
from scipy.interpolate import interp1d

common_names = ['Date', 'Severity', 'Problem', 'Company', 'Ranch']
names = ['Dew Point (°C)', 'Dew Max Point (°C)', 'Hour Max Wind Speed', 'Wind (km/h)', 'Wind Burst (km/h)', 'Avg Temp (°C)',
        'Avg Humidity (%)', 'ETO (mm)', 'Acc Joules', 'Cold Hours', 'Rain (mm)', 'Light Hours']
col_names = common_names + names
f = pd.read_csv('plague/temp.csv', low_memory=False, names=col_names, encoding='latin1', header=1)

f = f[f.isnull().sum(axis=1) < 1]

f[names] = f[names].add(0, fill_value=0)

prob = f.groupby('Problem').size()
sev = list(f.groupby('Severity').size().index)
prob_dicts = {}
sep = '-'
for p in list(prob.index):
    for s in sev:
        d = {n: [] for n in names}
        prob_dicts[p + sep + s] = d

eq = f[f['Severity'].str.contains('Equilibrio')]
eq_bees = eq[eq['Problem'].str.contains('Abejas')]
eq_prob1 = eq[eq['Problem'].str.contains('Agallas de la corona')]

problems = list(prob.index)
for s in sev:
    f_sev = f[f['Severity'].str.contains(s)]
    if len(list(f_sev.values)) == 0:
        continue
    for p in problems:
        f_sev_prob = f_sev[f_sev['Problem'].str.contains(p)]
        if len(list(f_sev_prob.values)) == 0:
            continue
        for col in names:
            #val = list(f_sev_prob.groupby(col).size().index)
            #freq = list(f_sev_prob.groupby(col).size().values)
            #prob_dicts[p+sep+s][col] = [val, freq]
            val = list(f_sev_prob[col].values)
            if len(val) == 0:
                continue
            prob_dicts[p+sep+s][col] = val
to_delete = []
for ps, v1 in list(prob_dicts.items()):
    for col, v2 in list(prob_dicts[ps].items()):
        if prob_dicts[ps][col] == 0:
            del prob_dicts[ps][col]
prob_dicts = {k: v for k,v in list(prob_dicts.items()) if len(list(prob_dicts[k].keys())) > 0}

prob_compact = {}
for p in problems:
    for s in sev:
        d = {n: [] for n in names}
        prob_compact[p] = d

for i in range(len(problems)):
    for k in range(len(names)):
        vals = []
        for j in range(len(sev)):
            vals = vals + prob_dicts[problems[i]+sep+sev[j]][names[k]]
        prob_compact[problems[i]][names[k]] = vals

bars = 10
problems = list(prob.index)
print(len(problems))
# problems = ['Alternaria spp.']
# fig1 = plt.figure(figsize=(14, 5))
colors = [(0, 0, 1, 0.5), (1, 0, 0, 0.5), (0, 1, 0, 0.5)]
labels = {"0": sev[0], "1": sev[1], "2": sev[2]}
offset = [-1, 0, 1]

fig1 = plt.figure(figsize=(20, 20))
counter = 1
for i in range(len(problems)):

        p = problems[i]
        col = 'Dew Point (°C)'
        tot_range = prob_compact[p][col]
        intervals = []
        if len(tot_range) == 0:
                continue
        if min(tot_range) == max(tot_range):
                intervals = np.linspace(min(tot_range) - max(tot_range), max(tot_range), bars)
        else:
                intervals = np.linspace(min(tot_range), max(tot_range), bars)

        intervals = list(intervals)
        intervals = [0.0] + intervals
        if max(intervals) == 0.0:
                continue

        for j in range(len(sev)):

                s = sev[j]
                # ax1 = fig1.add_subplot(len(problems), 3,(i*3) + (j+1))
                # ax1 = fig1.add_subplot(len(problems), 3, counter)
                key = p + sep + s
                if (key not in prob_dicts.keys()):
                        # ax1.set_title(p + sep + s)
                        # counter += 1
                        continue
                if (col not in prob_dicts[key].keys()):
                        continue
                if len(prob_dicts[p + sep + s][col]) == 0:
                        # ax1.set_title(p + sep + s)
                        # counter += 1
                        continue
                curr = prob_dicts[p + sep + s][col]

                heights = [0 for i in intervals[1:]]
                xs = list(range(len(heights)))
                xlabels = ["({:.2f}-{:.2f}]".format(intervals[h - 1], intervals[h]) for h in range(1, len(intervals))]

                for interval in range(len(intervals) - 1):
                        minVal = intervals[interval]
                        maxVal = intervals[interval + 1]
                        for c in curr:
                                if c > minVal and c <= maxVal:
                                        heights[interval] += 1
                width = 0.3
                ax1 = fig1.add_subplot(4, 3, counter)
                # ax1.bar(np.array(xs) + (width)*(offset[j]), heights, width=width, color=colors[j], label=labels[str(j)])
                xnew = np.linspace(min(xs), max(xs), 300)
                f = interp1d(xs, heights, kind='cubic')
                ax1.plot(xnew, f(xnew), color=colors[j], label=labels[str(j)], lw=5)
                # labels[str(j)] = "_nolegend_"
                ax1.legend()
                # ax1.bar(xs, heights, color=colors[0])
                # fig1.savefig('images/' + col + '.png', dpi=300)

        # fig1.suptitle(f"Attribute: ({col})\n", fontsize="x-large")

        ax1.set_xticks(xs)
        ax1.set_xticklabels(xlabels, rotation=90)
        ax1.set_title(p)
        plt.ylabel('Frequency')
        plt.xlabel(col)

        fig1.tight_layout()
        counter += 1
fig1.tight_layout()
plt.show()