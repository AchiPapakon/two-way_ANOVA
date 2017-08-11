import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt

from scipy import stats

datafile = "../data/test_output.csv"
data = pd.read_csv(datafile)

fig = interaction_plot(data.dose, data.supp, data.len,
                       colors=['red', 'blue'], markers=['D', '^'], ms=10)
print(data.dose)

N = len(data.len)
df_a = len(data.supp.unique()) - 1
df_b = len(data.dose.unique()) - 1
df_axb = df_a * df_b
df_w = N - (len(data.supp.unique()) * len(data.dose.unique()))

grand_mean = data['len'].mean()
ssq_a = sum([(data[data.supp == l].len.mean() - grand_mean) ** 2 for l in data.supp])
ssq_b = sum([(data[data.dose == l].len.mean() - grand_mean) ** 2 for l in data.dose])
ssq_t = sum((data.len - grand_mean) ** 2)

vc = data[data.supp == 'VC']
oj = data[data.supp == 'OJ']
vc_dose_means = [vc[vc.dose == d].len.mean() for d in vc.dose]
oj_dose_means = [oj[oj.dose == d].len.mean() for d in oj.dose]
ssq_w = sum((oj.len - oj_dose_means) ** 2) + sum((vc.len - vc_dose_means) ** 2)

ssq_axb = ssq_t - ssq_a - ssq_b - ssq_w
ms_a = ssq_a / df_a
ms_b = ssq_b / df_b
ms_axb = ssq_axb / df_axb
ms_w = ssq_w / df_w
f_a = ms_a / ms_w
f_b = ms_b / ms_w

p_a = stats.f.sf(f_a, df_a, df_w)
p_b = stats.f.sf(f_b, df_b, df_w)
p_axb = stats.f.sf(df_axb, df_axb, df_w)

results = {'sum_sq': [ssq_a, ssq_b, ssq_axb, ssq_w],
           'df': [df_a, df_b, df_axb, df_w],
           'F': [f_a, f_b, df_axb, 'NaN'],
           'PR(>F)': [p_a, p_b, p_axb, 'NaN']}
columns = ['sum_sq', 'df', 'F', 'PR(>F)']

aov_table1 = pd.DataFrame(results, columns=columns,
                          index=['supp', 'dose',
                                 'supp:dose', 'Residual'])

# def eta_squared(aov):
#     aov['eta_sq'] = 'NaN'
#     aov['eta_sq'] = aov[:-1]['sum_sq'] / sum(aov['sum_sq'])
#     return aov


# def omega_squared(aov):
#     mse = aov['sum_sq'][-1] / aov['df'][-1]
#     aov['omega_sq'] = 'NaN'
#     aov['omega_sq'] = (aov[:-1]['sum_sq'] - (aov[:-1]['df'] * mse)) / (sum(aov['sum_sq']) + mse)
#     return aov


# eta_squared(aov_table1)
# omega_squared(aov_table1)
print(aov_table1)
plt.show()
