import numpy as np

x = np.zeros(2)
x[1] = 2
x[0] = 100

z = [None]*4
z[1] = "abel"
z[2] = "lorena"
z[1] = "pepe"

v = {'feliz':{'gordo':2,'flaco':100}}
s = sorted(v['feliz'].items(),key=lambda kv:kv[1],reverse=True)[:2]
f = filter(lambda t: t[1],[('flaco', 100), ('gordo', 2)])
print(list(f))

print('a' in ' ab c')
# print(filter(lambda t:t[1], ))