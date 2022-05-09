import numpy as np

l = {3:110,1:14}
l = sorted(l.items(),key=lambda kv:kv[1],reverse=True)

# n = np.linalg.norm(list(l.values()))

print(l[:10])

