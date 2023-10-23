import numpy as np

a = [941,1336]

b = [1721.7406769943166, 578.9942543553803, 1128.9306524863418]

for v in a:
    for p in b:
        print(f'{v} & {p}, {np.isclose(v, p, rtol=.1)}')