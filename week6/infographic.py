import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib import cm  # color map

f = open("titanic-db.csv")
data = list(csv.reader(f))
headers = data[0]
print(headers)
data = data[1:]

db = []
for item in data:
    # item is the row
    d = {h:val for h, val in zip(headers, item)}
    db.append(d)

figTotal = plt.figure( figsize=(15,10) )
grid = figTotal.add_gridspec(3,3)
figTotal.suptitle("Titanic Ship Tragedy (1912)", fontsize="x-large")

ax4 = figTotal.add_subplot( grid[0,:2]) # plot that uses the first row and 3 cols
ax2 = figTotal.add_subplot( grid[1:,0:2] )
ax3 = figTotal.add_subplot( grid[0:2,2] )
ax = figTotal.add_subplot( grid[2,2] )

s_men = 0
s_men_age = 0
s_women = 0
s_women_age = 0
d_men = 0
d_men_age = 0
d_women = 0
d_women_age = 0

for d in db:
    if int(d['Survived']) == 1 and d['Sex'] == 'male':

        if d['Age'] != '':
            s_men += 1
            s_men_age += float(d['Age'])
    if int(d['Survived']) == 0 and d['Sex'] == 'male':

        if d['Age'] != '':
            d_men += 1
            d_men_age += float(d['Age'])
    if int(d['Survived']) == 1 and d['Sex'] == 'female':

        if d['Age'] != '':
            s_women += 1
            s_women_age += float(d['Age'])
    if int(d['Survived']) == 0 and d['Sex'] == 'female':
        d_women += 1
        if d['Age'] != '':
            d_women_age += float(d['Age'])

# scatter
s_men_age = s_men_age / s_men
d_men_age = d_men_age / d_men
s_women_age = s_women_age / s_women
d_women_age = d_women_age / d_women

labels = ['Survived Men', 'Dead Men', 'Survived Women', 'Dead Women']
ys = [s_men_age, d_men_age, s_women_age, d_women_age]
radius = [s_men, d_men, s_women, d_women]
radius = [10 * r for r in radius]
xs = []
x = 0
xs.append(x)

for i in range(1, len(radius)):
    x += (radius[i - 1] + radius[i]) * 0.2
    xs.append(x)

gap = 1000
ax.set_xlim((min(xs) - gap, max(xs) + gap))
ax.set_ylim((0, max(ys) + 10))
ax.tick_params(
    axis='x',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    bottom=False,  # ticks along the bottom edge are off
    top=False,  # ticks along the top edge are off
    labelbottom=False)  # labels along the bottom edge are off

cmap = cm.get_cmap("cool")
color_n = np.array(ys) / max(ys)
color_n = [cmap(c) for c in color_n]

for r in range(len(radius)):
    ax.scatter(xs[r], ys[r], s=radius[r], label=labels[r], color=color_n[r])
    ax.annotate(labels[r], (xs[r], ys[r]))

ax.set_title("Gender Survival vs Average Age")
plt.ylabel("Age (Average)")

# bar
from matplotlib import cm # color map
cmap0 = cm.get_cmap("winter")
cmap1 = cm.get_cmap("cool")
class_data = [[0, 0, 0], [0, 0, 0]]

for d in db:
    class_data[int(d['Survived'])][int(d['Pclass']) - 1] += 1

width = 0.3
xs = list(np.arange(0, len(class_data)))
offset = [-1, 0, 1]

colors = [[cmap0(c) for c in np.array(class_data[0]) / max(class_data[0])],
          [cmap1(c) for c in np.array(class_data[0]) / max(class_data[1])]]
labels = ['1st class', '2nd class', '3rd class']

for s in range(len(class_data)):
    for c in range(len(class_data[s])):
        ax2.bar(np.array(xs[s]) + (width)*(offset[c]), class_data[s][c], width=width, color=colors[s][c], zorder=3)
        ax2.annotate(labels[c], (np.array(xs[s]) + (width)*(offset[c]) - (width/4.0),
                                 class_data[s][c] - class_data[s][c] * 0.5), fontsize=10)
ax2.set_xticks(xs)
ax2.set_xticklabels(['Deaths Per class', 'Survivals Per Class'])
ax2.grid(zorder=0, axis='y')
ax2.set_title("Death and Survival Per Class")
plt.ylabel("Number of People")

# pie
ports = ['Cherbourg', 'Queenstown', 'Southampton']
p = ['C', 'Q', 'S']
cmap3 = cm.get_cmap('cool')
size = 0.3

people = {port: 0 for port in p}
deaths = {port: 0 for port in p}
alive = {port: 0 for port in p}
for d in db:
    if d['Embarked'] in p:
        people[d['Embarked']] += 1
        if d['Survived'] == '0':
            deaths[d['Embarked']] += 1
pie2_data = []
for p in deaths.keys():
    alive[p] = people[p] - deaths[p]
    pie2_data.append(alive[p])
    pie2_data.append(deaths[p])
print(alive, deaths, pie2_data)


nums = list(people.values())
color_data = np.array(nums) / max(nums)
colors_out = [cmap3(c) for c in color_data]
colors_in = [cmap3((c % 2)/2.0) for c in range(len(pie2_data))] # 0 1 0 1 0 1

ax3.pie(nums, labels = ports, radius=1, colors=colors_out, wedgeprops=dict(width=size, edgecolor='w'))
ax3.set_title("Death and Survival Per Port Embarked")
ax3.pie(pie2_data, radius=1-(size), colors=colors_in,
        wedgeprops=dict(width=size, edgecolor='w'), labels = list('SD' * 3), labeldistance=0.7)

# stack
fares = [[], [], []] # 0 for 1st, 1 for 2nd, 3 for 3rd
labels = ['1st class', '2nd class', '3rd class']
cmap = cm.get_cmap("cool")
color_n = np.arange(0,3) * 100
color_n = [cmap(c) for c in color_n]
for d in db:
    fares[int(d['Pclass'])-1].append(float(d['Fare']))
lengths = [len(fares[0]), len(fares[1]), len(fares[2])]

xs = np.arange(0, max(lengths))
y1 = np.zeros(max(lengths))
y2 = np.zeros(max(lengths))
y3 = np.zeros(max(lengths))

y1[:len(fares[0])] = fares[0]
y2[:len(fares[1])] = fares[1]
y3[:len(fares[2])] = fares[2]

ax4.stackplot(xs, y3, y2, y1, labels=labels[::-1], colors=color_n)
ax4.set_title("Ticket Fare Per Class")
ax4.set_xlim(0, max(lengths)-1)
ax4.legend()
plt.show()