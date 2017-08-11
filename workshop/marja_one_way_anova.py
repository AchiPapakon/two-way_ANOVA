import pandas as pd

datafile = "../data/PlantGrowth.csv"
data = pd.read_csv(datafile)

# Create a boxplot
data.boxplot('weight', by='group', figsize=(12, 8))

ctrl = data['weight'][data.group == 'ctrl']

grps = pd.unique(data.group.values)
d_data = {grp: data['weight'][data.group == grp] for grp in grps}

k = len(pd.unique(data.group))  # number of conditions
N = len(data.values)  # conditions times participants
n = data.groupby('group').size()[0]  # Participants in each condition

DFbetween = k - 1
DFwithin = N - k
DFtotal = N - 1

# ~~~ Sum of Squares Within ~~~
sum_y_squared = sum([value**2 for value in data['weight'].values])
partial_sum = sum(data.groupby('group').sum()['weight']**2)
SSwithin = sum_y_squared - partial_sum/n

# ~~~ Mean square within ~~~
MSwithin = SSwithin/DFwithin

print('SSwithin:', SSwithin)
print('MSwithin', MSwithin)

# ~~~ Calculate the F value ~~~
from scipy import stats
p = stats.f.sf(F, DFbetween, DFwithin)
print()