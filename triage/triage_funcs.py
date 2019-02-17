# Define patient arrival rate function
def lam(time, c, a):
    t = time/60
    out = c / 60 * (t)**(a-1)*np.exp(-t)/(gamma(a))
    return out
