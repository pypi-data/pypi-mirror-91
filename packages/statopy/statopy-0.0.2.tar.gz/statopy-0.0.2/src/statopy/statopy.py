""" Online statistics
Credit for scalar algorithms to John D. Cook:

    https://www.johndcook.com/blog/skewness_kurtosis/

    https://www.johndcook.com/blog/running_regression/

"""
import math,cmath
try:
    #numpy optional - not necessary for scalar statistics, only used for vector statistics and probability model
    import numpy as np 
except:
    pass

try:
    #scipy optional - not necessary for scalar statistics or vector statistics, only used for probability model
    #from scipy.interpolate import UnivariateSpline
    from scipy.interpolate import PchipInterpolator
    #import scipy.interpolate
    #from scipy.optimize import root
    from scipy.signal import savgol_filter
    from scipy.optimize import newton
except:
    pass
try:
    #matplotlib optional - not necessary for scalar statistics or vector statistics, only used for probability model
    import matplotlib.pyplot as plt
except:
    pass


class ScalarStats():
    """
    Streaming/running/online calculation of min, max, mean, std dev/variance, skewness, kurtosis for an iterable

    >>> stats=ScalarStats([1,2,3,4,5])
    >>> stats.kurtosis
    -1.3
    >>> stats.update(10)
    >>> stats.kurtosis
    -0.021349099704380592
    >>> stats.skewness
    1.0513280892320203
    >>> stats.stdev
    3.188521078284832
    >>> stats.var
    10.166666666666668
    >>> stats.mean
    4.166666666666667
    >>> stats.max
    10
    >>> stats.min
    1
    """
    __slots__ = ['mx','mx2','mx3','mx4','n','min','max','n_limit','use_cmath']
    def __init__(self,scalars=None,n_limit=float('inf'),use_cmath=False):
        object.__setattr__(self,'mx',0)
        object.__setattr__(self,'mx2',0)
        object.__setattr__(self,'mx3',0)
        object.__setattr__(self,'mx4',0)
        object.__setattr__(self,'min',None)
        object.__setattr__(self,'max',None)
        object.__setattr__(self,'n',0)
        object.__setattr__(self,'n_limit',n_limit)
        object.__setattr__(self,'use_cmath',use_cmath)
        if scalars is not None:
            self.consume(scalars)

    def consume(self,scalars):
        for x in scalars:
            self.update(x)

    def update(self,x):
            n1 = self.n #n1 = n as it was before this sample
            n = n1 + 1 #n = including this sample
            d = x - self.mx #d = delta of sample from mean as mean was before this sample
            dn = d/n #dn = delta scaled down by new n
            dn2 = dn*dn # dn2 = square dn
            t1 = d*dn*n1 # t1 = square delta times (n-1)/n
            mx = self.mx + dn #mean update

            minimum = self.min
            if minimum is None or x < minimum:
                object.__setattr__(self,'min',x)
            maximum = self.max
            if maximum is None or x > maximum:
                object.__setattr__(self,'max',x)


                #m2 = m1 + dn = m1 + d/n = m1 + (x-m1)/n = m1*(1-1/n) + x/n = m1*(n-1)/n + x/n = (m*(n-1)+x)/n
                #m*(n-1) is the sum of all the previous samples

            mx4 = self.mx4 + t1*dn2*(n*n-3*n+3) + 6 * dn2*self.mx2 - 4 *dn * self.mx3 #4th moment update
            mx3 = self.mx3 + t1*dn*(n-2)-3*dn*self.mx2 #3rd moment update
            mx2 = self.mx2 + t1 #2nd moment update


            object.__setattr__(self,'n',min(n,self.n_limit))
            object.__setattr__(self,'mx',mx)
            object.__setattr__(self,'mx2',mx2)
            object.__setattr__(self,'mx3',mx3)
            object.__setattr__(self,'mx4',mx4)

    def __setattr__(self,attr_name,attr_value):
        raise Exception('OnlineStatistics properties are only changeable via the consume() or add() methods')

    @property
    def mean(self):
        if self.n > 0:
            return self.mx
        else:
            return None

    @property
    def var(self):
        if self.n > 1:
            return self.mx2/(self.n-1)
        else:
            return None

    @property
    def stdev(self):
        mm = cmath if self.use_cmath else math
        if self.n > 1:
            return mm.sqrt(self.var)
        else:
            return None

    @property
    def skewness(self):
        mm = cmath if self.use_cmath else math
        if self.n > 2:
            return mm.sqrt(self.n) * self.mx3/(self.mx2**1.5)
        else:
            return None

    @property
    def kurtosis(self):
        if self.n > 3:
            return self.n*self.mx4/(self.mx2**2) - 3
        else:
            return None

    def __add__(self,other):
        """
        Combines the two ScalarStats objects as if all the data points were included in one.
        Whichever n_limit value is larger will be used.
        """
        if isinstance(other,ScalarStats):
            result = ScalarStats()
            object.__setattr__(result,'n',self.n+other.n)
            d = other.mx - self.mx
            d2 = d*d
            d3 = d*d2
            d4 = d2*d2
            object.__setattr__(result,'mx',self.mx*(self.n/result.n)+other.mx*(other.n/result.n))
            object.__setattr__(result,'mx2',self.mx2 + other.mx2 + d2*self.n*other.n/result.n)
            object.__setattr__(result,'mx3',self.mx3+other.mx3+d3*self.n*other.n*(self.n-other.n)/(result.n**2) + 3*d*(self.n*other.mx2-other.n*self.mx2)/result.n)
            object.__setattr__(result,'mx4',self.mx4 + other.mx4 + d4*self.n*other.n * (self.n**2 - self.n*other.n + other.n**2)/(result.n**3) + 6*d2*(self.n*self.n*other.mx2 + other.n*other.n*self.mx2)/(result.n**2) + 4*d*(self.n*other.mx3-other.n*self.mx3)/result.n)
            if self.min is not None:
                if other.min is not None:
                    minimum = min(self.min,other.min)
                else:
                    minimum = self.min
            else:
                if other.min is not None:
                    minimum = other.min
                else:
                    minimum = None
            if self.max is not None:
                if other.max is not None:
                    maximum = max(self.max,other.max)
                else:
                    maximum = self.max
            else:
                if other.max is not None:
                    maximum = other.max
                else:
                    maximum = None
            object.__setattr__(result,'min',minimum)
            object.__setattr__(result,'max',maximum)
            object.__setattr__(result,'max',maximum)
            object.__setattr__(result,'n_limit',max(self.n_limit,other.n_limit))
        else:
            raise Exception('ScalarStats objects can only be added to other ScalarStats objects')

class ScalarRegression():
    """
    Streaming/running/online calculation of a linear regression between two sequences of scalars

    >>> x = np.arange(0,100)
    >>> y = x + np.cos(np.linspace(0,4*np.pi,100))
    >>> sr = ScalarRegression(zip(x,y))
    >>> sr.corr
    0.9996971673199834
    >>> sr.cov
    841.6666666666665
    >>> sr.xs.mean
    49.5
    >>> sr.xs.max
    99
    >>> sr.xs.min
    0
    >>> sr.ys.stdev
    29.020280265129536
    >>> sr.ys.kurtosis
    -1.1986082973172405
    """
    __slots__ = ['xs','ys','sxy','n','n_limit','use_cmath']
    def __init__(self,pair_source=None,n_limit=float('inf'),use_cmath=False):
        object.__setattr__(self,'xs',ScalarStats(n_limit=n_limit,use_cmath=use_cmath))
        object.__setattr__(self,'ys',ScalarStats(n_limit=n_limit,use_cmath=use_cmath))
        object.__setattr__(self,'n',0)
        object.__setattr__(self,'n_limit',n_limit)
        object.__setattr__(self,'use_cmath',use_cmath)
        if pair_source is not None:
            self.consume(pair_source)
    def __setattr__(self,attr_name,attr_value):
        raise Exception('ScalarRegression properties are only changeable via the consume() or add() methods')
    def update(self,x,y):
        if self.n == 0:
            xm = ym = 0
            object.__setattr__(self,'sxy',0)
        else:
            xm = self.xs.mean
            ym = self.ys.mean
            object.__setattr__(self,'sxy',self.sxy*(self.n-1)/self.n + (xm-x)*(ym-y)/(self.n+1))
        self.xs.update(x)
        self.ys.update(y)
        object.__setattr__(self,'n',self.n+1)
    def consume(self,pair_source):
        for x,y in pair_source:
            self.update(x,y)
    @property
    def slope(self):
        sxx = self.xs.var*(self.n-1)
        return self.sxy/sxx

    @property
    def intercept(self):
        return self.ys.mean - self.slope*self.xs.mean

    @property
    def cov(self):
        return self.sxy
    @property
    def corr(self):
        t = self.xs.stdev * self.ys.stdev
        return self.sxy/t

    def __add__(self,other):
        if isinstance(other,ScalarRegression):
            result = ScalarRegression(n_limit=self.n_limit,use_cmath=self.use_cmath)
            object.__setattr__(result,'xs',self.xs+other.xs)
            object.__setattr__(result,'ys',self.ys+other.ys)
        else:
            raise Exception('ScalarRegression objects can only be added to other ScalarRegression objects')


class VectorStats():
    """
    Streaming/running/online calculation of mean and covariance matrix for vectors

    Configure dimensions using one sample with the configure() method.
    Incorporate subsequent samples with the update() method
    Requires numpy

    >>> from pydataset import data
    >>> iris = data('iris')
    >>> iris.cov()
                  Sepal.Length  Sepal.Width  Petal.Length  Petal.Width
    Sepal.Length      0.685694    -0.042434      1.274315     0.516271
    Sepal.Width      -0.042434     0.189979     -0.329656    -0.121639
    Petal.Length      1.274315    -0.329656      3.116278     1.295609
    Petal.Width       0.516271    -0.121639      1.295609     0.581006
    >>> vecs = iris.to_numpy()[:,:-1].astype('float64')
    >>> vs = VectorStats()
    >>> vs.configure(vecs[0])
    >>> for x in vecs[1:]:
    ...  vs.update(x)
    ... 

    >>> vs.cov
    array([[ 0.68569351, -0.042434  ,  1.27431544,  0.51627069],
           [-0.042434  ,  0.18997942, -0.32965638, -0.12163937],
           [ 1.27431544, -0.32965638,  3.11627785,  1.2956094 ],
           [ 0.51627069, -0.12163937,  1.2956094 ,  0.58100626]])
    """
    def __init__(self,x_0=None,n_limit=None,default_cov=1):
        if x_0 is None:
            self.make_empty()
        else:
            self.configure(x_0)
        self.n_limit = np.inf
        self.default_cov = default_cov
    def make_empty(self,n_limit=None):
        self.mean = self.cov = self.dim_x = None
        self.n = 0
        if n_limit is not None:
            self.n_limit=n_limit #otherwise preserve previous value
    @property
    def is_empty(self):
        return self.mean is None
    def configure(self,x_0):
        self.mean = x_0
        self.dim_x = dim_x = x_0.shape[0]
        self.cov = np.ones((dim_x,dim_x))*self.default_cov
        self.n = 1
    def update(self,x):
        deviation = x - self.mean
        plasticity = 1.0/(1+self.n)
        rigidity = (self.n-1.0)/self.n
        self.mean += deviation * plasticity
        self.cov = self.cov * rigidity + (deviation * deviation.reshape((self.dim_x,1))) * plasticity
        if self.n_limit is None:
            self.n += 1
        else:
            self.n = min(self.n+1,self.n_limit)
    def consume(self,vectors):
        for x in vectors:
            self.update(x)

class ScalarProbModel():
    """
    Given a set of random data, produce a CDF and PDF model that can be used to generate more data with the same approximate distribution.
    Requires numpy and scipy

    Example:
        ```python
from scipy.stats import expon
import matplotlib.pyplot as plt
x = expon().rvs(1000)
spm = ScalarProbModel(x)
fig = plt.figure()
spm.plot_cdf()
spm.plot_scatter()
fig = plt.figure()
spm.plot_pdf()
plt.show()
        ```
    """
    def __init__(self,xs,resolution=1000,smoothing=.1):
        n = len(xs)
        xs,cdf_vals = np.unique(xs,return_counts=True)
        cdf_vals = np.cumsum(cdf_vals) / float(n) 
        self.min_x = xs[0]
        self.max_x = xs[-1]
        rng = self.max_x - self.min_x 
        dev = rng*1e-9
        #xs = np.r_[self.min_x-rng,self.min_x-dev,xs,self.max_x+dev,self.max_x+rng]
        #cdf_vals = np.r_[0,0,cdf_vals,1,1]
        xs = np.r_[self.min_x-dev,xs,self.max_x+dev]
        cdf_vals = np.r_[0,cdf_vals,1]
        self.xs = xs
        self.cdf_vals = cdf_vals
        #cdf = UnivariateSpline(xs,cdf_vals,s=smoothing,ext=use_boundary_value)
        cdf_interp = PchipInterpolator(xs,cdf_vals,extrapolate=True)
        if smoothing is None:
            cdf = cdf_interp
        else:
            xl = np.linspace(self.min_x,self.max_x,resolution)
            cdf_l = cdf_interp(xl)
            w = int(resolution*smoothing)
            w = w + 1 - (w%2);
            cdf_f = savgol_filter(cdf_l,w,3,mode='nearest')
            cdf= PchipInterpolator(xl,cdf_f,extrapolate=True)
        base_cdf = cdf
        cdf = lambda x,base_cdf=base_cdf: np.clip(base_cdf(x),0,1)
        #w = 31
        #mask = np.ones((1,w))/w
        #mask = mask[0,:]
        #cdf_ma = np.convolve(cdf_l,mask,'valid')
        #cdf = scipy.interpolate.CubicSpline(xl,cdf_ma,bc_type=((1,0.0),(1,0.0)))
        #cdf = scipy.interpolate.PchipInterpolator(xl,cdf_l)
        #cdf = scipy.interpolate.PchipInterpolator(xl,cdf_l)
        #cdf = scipy.interpolate.Akima1DInterpolator(xs,cdf_vals)
        #use_boundary_value = 3
        #cdf = scipy.interpolate.UnivariateSpline(xs,cdf_vals,s=smoothing,ext=use_boundary_value)
        #cdf = scipy.interpolate.CubicSpline(xl,cdf_l,bc_type=((1,0.0),(1,0.0)))
        base_pdf = base_cdf.derivative(1)
        pdf = lambda x,base_pdf=base_pdf: np.clip(base_pdf(x),0,None)
        self.n = n
        self.cdf = cdf
        self.pdf = pdf
        self.base_cdf = base_cdf
        self.base_pdf = base_pdf
    def plot_cdf(self,num_points=100):
        x_lin = np.linspace(self.min_x,self.max_x,num_points)
        cdf_lin = self.cdf(x_lin)
        plt.plot(x_lin,cdf_lin)
    def plot_pdf(self,num_points=500):
        x_lin = np.linspace(self.min_x,self.max_x,num_points)
        pdf_lin = self.pdf(x_lin)
        plt.plot(x_lin,pdf_lin)
    def plot_scatter(self):
        plt.scatter(self.xs,self.cdf_vals)
    def rvs(self,num_points=1):
        u = np.random.uniform(size=num_points)
        #u# = np.array([0.5])
        #F(x) = u
        #x = inv_F(u)
        #F(x)-u=0

        func = lambda xs,u=u: self.cdf(xs) - u
        guess_values = self.base_cdf.solve(0.5,extrapolate=False)
        guess_value = np.mean(guess_values[guess_values>=0][guess_values<=1])
        guess = np.ones(num_points)*guess_value
        #result = root(func,guess,tol=1e-4)
        result = newton(func,guess,fprime=self.pdf,maxiter=1000,tol=1e-9)
        return np.clip(result,self.min_x,self.max_x)

if __name__ == '__main__':
    from scipy.stats import norm,expon,uniform
    import matplotlib.pyplot as plt
    x = norm().rvs(1000)
    spm = ScalarProbModel(x)
    fig = plt.figure()
    spm.plot_cdf()
    spm.plot_scatter()
    fig = plt.figure()
    spm.plot_pdf()
    import os
    os.environ['PYTHONINSPECT']= '1'
    x2 = spm.rvs(1000)
    spm2 = ScalarProbModel(x2)
    fig = plt.figure()
    spm2.plot_cdf()
    spm2.plot_scatter()
    fig = plt.figure()
    spm2.plot_pdf()
    plt.show()

