#%%
import sympy as sy
import math as math
from sympy.core import evaluate
import os
import sys
sys.path.insert(1, os.path.dirname(sys.path[0])) # need to import 1 directories up (so spp is a subfolder)
import scipyPaperPrinter as spp
g = 9.80665 #m/sec

spp.printMarkdown(r'# Scipy Paper Printer Demo {-}')
spp.printMarkdown(r'## Solution to Chapter 01 Problem 05 of Optimal Control with Aerospace Applications @LonguskiGuzmanAndPrussing {-}')
spp.printMarkdown(r'This back-of-the-chapter problem is all about Hohmann and bi-parabolic satellite transfers.  In addition to being an interesting study in orbital maneuvers, this problem shows many tips and tricks to solving problems like this symbolically and numerically, and how to transition between the two.')
spp.printMarkdown(r'### 5-a {-}')
spp.printMarkdown(r'First, we are asked to describe a Hohmann Transfer and derive a formula for the total velocity change.')
spp.printMarkdown(r'A Hohmann transfer is a co-planer transfer between 2 circular orbits (although it extends easily to 2 coelliptic elliptical orbits when the burns are only at periapsis and apoapsis). There are 2 burns, the first to get onto the transfer orbit between the 2 circles, and the second happens 180 degrees of anomaly later.  The burns are always along the velocity vector of both the pre and post orbits, and on the elliptical transfer orbit the burns are always at 0 and 180 degrees anomaly.  I say anomaly because everything said before is correct for mean, true and eccentric anomalies.')
spp.printMarkdown(r'We could spend more time talking about Hohmann Transfers, but lets get to evaluating values.  We will start with taking the two expression the problem asked us to put our problem in, but we are going to solve for $r_o$ and $r_f$ in terms of those expressions.  Then we add equations 1.36 and 1.41 together and do the substitution.')
    # define a bunch of parameters up front
mu = sy.Symbol(r'\mu', positive=True, real=True)
dv1 = sy.Symbol(r'\Delta{V_{1}}', positive=True, real=True)
dv2 = sy.Symbol(r'\Delta{V_{2}}', positive=True, real=True)
ro = sy.Symbol(r'r_o', positive=True, real=True)
rf = sy.Symbol(r'r_f', positive=True, real=True)
vo = sy.Symbol(r'f_o', positive=True, real=True)
vf = sy.Symbol(r'v_f', positive=True, real=True)
dvTol = sy.Symbol(r'\Delta{V_{tol}}', positive=True, real=True)

with (evaluate(False)) : # setting evaluate to false here helps prevent some of the simplification and rearrangement of terms that scipy will do by default
    # equation 1.36 and 1.41
    dv1 = sy.sqrt(mu/ro)*(sy.sqrt(2*rf/(rf+ro))-1)
    dv2 = sy.sqrt(mu/rf)*(1-sy.sqrt(2*ro/(rf+ro)))

alpha = sy.Symbol(r'\alpha', real=True, positive=True) 
alphaEq = sy.Eq(alpha, rf/ro)
rfITOalpha = sy.solve(alphaEq, rf)[0]
spp.showEquation(rf, rfITOalpha)

    # note that I am calling this expression beta in code, but notice how it is a Dummy.  This is a trick to help keep various terms together when solving equations
beta = sy.Dummy(r'\frac{\Delta{V_{tol}}}{\sqrt{(\frac{\mu}{r_o}})}', real=True, positive=True)
betaEq = sy.Eq(beta, dvTol/(sy.sqrt(mu/ro)))
roITObeta = sy.solve(betaEq, ro)[0].subs(rf, rfITOalpha) # standard substitution and printing the output as we go...
spp.showEquation(ro, roITObeta)
rfFull = rfITOalpha.subs(ro, roITObeta) 
spp.showEquation(rf, rfFull)
dvTolEq = sy.Eq(dvTol, dv1+dv2)
spp.showEquation(dvTol, dvTolEq)
dvTotEqSubs = dvTolEq.subs(rf, rfFull).subs(ro, roITObeta).simplify()
spp.showEquation(dvTotEqSubs)
dvTotSmplified = sy.solve(dvTotEqSubs, beta)[0]

spp.showEquation(beta, dvTotSmplified)
spp.printMarkdown(r'The problem explicitaly states that we should simplify this into the most compact form.  I tried various techniques in sympy to do that, but this may not be exactly what the author is looking for.')

#%%
spp.printMarkdown(r'### 5-b {-}')
spp.printMarkdown(r'We do the same thing, but this time we sum the circular speed with the parabolic speeds.')
with evaluate(False) :
    vTotParaEq = sy.Eq(dvTol, sy.sqrt(2*mu/rf) - sy.sqrt(mu/rf) +  sy.sqrt(2*mu/ro) - sy.sqrt(mu/ro))
spp.showEquation(vTotParaEq, cleanEqu=False)
dvTotParaSubed = vTotParaEq.subs(rf, rfFull).subs(ro, roITObeta)
dvParSubs = sy.solve(dvTotParaSubed, beta)[0]
spp.showEquation(dvTol, dvParSubs)

#%%
spp.printMarkdown(r'### 5-c {-}')
spp.printMarkdown(r'We make the plot comparing the two transfer types.  Note that since the problem assumes $r_f > r_o$, the lower bound of the plot must be $>= 1$ as the problem says.')

import matplotlib.pyplot as plt
import numpy as np

t = np.arange(1, 40.0, 0.01)
    # here is one of the most powerful features of scipy!  Eventually, you want to 
    # evaluate some numbers.  If you are doing it once or twice, you can just substitute in values
    # and evaluate it.  But if you need to evaluate the expression many many times, that will be 
    # too slow.  But lambdify will convert the expression to a callback using python's default 
    # math library, numpy, scipy, or others.  That will be MUCH faster.  
dvHoh = sy.lambdify(alpha, dvTotSmplified)(t)
dvPar = sy.lambdify(alpha, dvParSubs)(t)

fig, ax = plt.subplots()
ax.plot(t, dvHoh, label="Hohman")
ax.plot(t, dvPar, label="BiParabolic")
ax.legend()
ax.grid()
# if we don't capture (and ignore) the output of the set function, it will write cruff to the final file
ignoreOutput = ax.set(xlabel=r'$\alpha$', ylabel=r'$\frac{dv}{r}$',
       title=r'$\frac{\Delta{V}}{r_f}$ for different orbit ratios')
plt.show()

spp.printMarkdown(r'We can see that the cutoff is about a ratio of 12, likely the 11.94 value quoted earlier in the chapter.')

#%%
spp.printMarkdown(r'### 5-d {-}')
spp.printMarkdown(r'Here we will use a numerical root-finder to find when the two transfer techniqes equal each other.  Attempts to solve it symbolically failed.')
eqForAlpha = sy.Eq(dvTotSmplified, dvParSubs)
spp.showEquation(eqForAlpha)
spp.showEquation(0, eqForAlpha.lhs - eqForAlpha.rhs)

    # again, using lambdify (making it a more stand-alone example instead of refactoring to use the similar expressions in part C)
aplhaEqLhs = sy.lambdify(alpha, dvTotSmplified)
aplhaEqRhs = sy.lambdify(alpha, dvParSubs)
def EqToSolve(alp) :
    return aplhaEqLhs(alp) - aplhaEqRhs(alp)

from scipy import optimize
ans = optimize.root_scalar(EqToSolve, bracket=[1, 40], method='brentq') # and doing root-finding with the lambdified function
# spp.showEquation(r'\alpha', ans)
spp.showEquation(r'\alpha', ans.root)

spp.printMarkdown("This matches the values a few pages earlier in the textbook.")

#%%
spp.printMarkdown(r'### Acknowlegments {-}')

spp.printMarkdown("Many thanks for the Citation Style Language website for making citations so easy and simple @CslDefinition.  Also thanks to the AIAA for publishing their csl file @AiaaCslDef.  Also, this sample of the Scipy Paper Printer is made with the Scipy Paper Printer and is in the public domain as specified on its github page @SppRepo. Please forgive, but also point out, any mistakes or problems or potential improvements.  Especally with how citations are handled.")

spp.printMarkdown(r'### References {-}')
if '__file__' in globals() or '__file__' in locals():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    thisFile = os.path.join(dir_path, "SppDemo-OptimalControlWithAerospaceApplications-01-05.py")
    spp.ReportGeneratorFromPythonFileWithCells.WriteIpynbToDesiredFormatWithPandoc(thisFile, extension="pdf")
    spp.printMarkdown("done")
