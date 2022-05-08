l = {('a',1):3,('b',2):2}

l = {key:l[key,1]/4 for key,_ in l }
print(l)
# print(l.values()/max(l.values()))