from scipy.stats import norm


def N(x):
    return norm.cdf(x)


def n(x):
    return norm.pdf(x)



