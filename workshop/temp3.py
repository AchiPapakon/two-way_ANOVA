from __future__ import division   # proper division 5/2 = 2.5
from math import sqrt
from scipy import stats

glb_split_groups_total_size = 0

# ~~~ the auto pilot method ~~~
def multiple_comparisons_with_bonferroni(list1, list2):
    groups = split_group(list1, list2)
    p_values = t_multiple_comparisons(groups)
    return bonferroni(p_values)

def split_group(m_c1, m_c2):
    # ~~~ m_c1 the depending variable
    # ~~~ m_c2 the categorical variable
    categories = []  # List of unique categorical values
    for y in m_c2:
        if not y in categories:
            categories.append(y)

    # ~~~ groups for the dependent variable (eg 3) ~~~
    from itertools import repeat
    groups = [[] for i in repeat(None, len(categories))]

    for x,y in zip(m_c1, m_c2):
        for i in range(0, len(categories)):
            if y == categories[i]:
                groups[i].append(x)
    # print(groups)
    return groups

def mean(m_lst):
    sum = 0
    for x in m_lst:
        sum += x
    return sum/len(m_lst)

def ms_within(m_groups):
    _size = 0
    # ~~~ SSwithin = Sigma(Y^2) - (1/n)*Sigma(Sigma(ai)^2) ~~~
    # ~~~ https://goo.gl/eh4h4k ~~~
    sum_y_squared = 0  # Sigma(Y^2)
    partial_sum = 0
    for x in m_groups:
        low_sum = 0  # sum the elements in each group
        for y in x:
            sum_y_squared += y ** 2
            low_sum += y
            _size += 1
        n = len(x)
        partial_sum += low_sum ** 2 / n
        global glb_split_groups_total_size
        glb_split_groups_total_size = _size
    SSwithin = sum_y_squared - partial_sum
    DFwithin = _size - len(m_groups)
    MSwithin = SSwithin / DFwithin
    return MSwithin

def t_multiple_comparisons(m_groups):
    p = []
    # ~~~ Calculate the modified t value for each pair
    s_res = sqrt(ms_within(m_groups))
    k = len(m_groups)  # number of conditions
    N = glb_split_groups_total_size  # conditions times participants
    DFwithin = N - k

    # ~~~ Test between groups ~~~
    for i in range(k-1):
        for j in range(i+1, k):
            numenator = mean(m_groups[i]) - mean(m_groups[j])
            denumenator = s_res * sqrt(1/len(m_groups[i]) + 1/len(m_groups[j]))
            t = numenator / denumenator
            # https://docs.scipy.org/doc/scipy/reference/tutorial/stats.html#t-test-and-ks-test
            p.append(stats.t.sf(abs(t), DFwithin) * 2)  # two-sided pvalue
    return p

def bonferroni(p_values):
    # ~~~ Bonferroni: Each p value is multiplied by the total number of comparisons made ~~~
    p_corrected = []
    k = len(p_values)
    for x in p_values:
        corrected = x * k
        if corrected > 1:
            p_corrected.append(1)
        else:
            p_corrected.append(x * k)
    return p_corrected


# groups = split_group([4.1, 5.4, 5.9, 3.8, 6.8, 9.3, 7.2, 2.3], [0.5, 0.5, 0.5, 1, 2, 1, 2, 2])

# print(ms_within([[243, 251, 275, 291, 347, 354, 380, 392],
#                  [206, 210, 226, 249, 255, 273, 285, 295, 309],
#                 [241, 258, 270, 293, 328]]))
#
# print(ms_within([[4.17, 5.58, 5.18, 6.11, 4.5, 4.61, 5.17, 4.53, 5.33, 5.14],
#                  [4.81, 4.17, 4.41, 3.59, 5.87, 3.83, 6.03, 4.89, 4.32, 4.69],
#                  [6.31, 5.12, 5.54, 5.5, 5.37, 5.29, 4.92, 6.15, 5.8, 5.26]]))

print(t_multiple_comparisons([[243, 251, 275, 291, 347, 354, 380, 392],
                              [206, 210, 226, 249, 255, 273, 285, 295, 309],
                              [241, 258, 270, 293, 328]]))
