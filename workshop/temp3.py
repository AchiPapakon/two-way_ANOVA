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


split_group([4.1, 5.4, 5.9, 3.8, 6.8, 9.3, 7.2, 2.3], [0.5, 0.5, 0.5, 1, 2, 1, 2, 2])