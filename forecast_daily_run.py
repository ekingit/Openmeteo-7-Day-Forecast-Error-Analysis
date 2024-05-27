import my_functions as mf


ds = mf.dataset()

dfl = []
for a_tuple in ds:
    dfl.append(mf.forecast(a_tuple[2],a_tuple[3]))

mf.update(ds,dfl)