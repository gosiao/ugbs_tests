# our aim:

* we want to create a set of exponents from a geometric progression (even-tempered, ET), 

```math
f_k = \alpha*\beta^k
```

* the aim is to optimize alpha and beta and find the optimal number of exponents


# how we do it:

* pick the "guiding" basis set, for which we know the range and the number of exponents
* choose a "start" exponent, which will be $\alpha_0$
  * here we test 4 starting exponents: 
    * the lowest exponent of the "guiding" basis set for a given element  (and then we move "upwards", so we will multiply with $\beta$)
    * the lowest exponent of the "guiding" basis set for all elements in that set  (and then we move "upwards", so we will multiply with $\beta$)
    * the largest exponent of the "guiding" basis set for a given element  (and then we move "downwards", so we will divide with $\beta$)
    * the largest exponent of the "guiding" basis set for all elements in that set  (and then we move "downwards", so we will divide with $\beta$)

* choose $\beta$: the rule of thumb is that:
  * to create sets of X-zeta quality, $\beta = 10^{(1/X)}$

* create a set of $f_k$ - that will be common to all angular momenta

* then to choose the number of exponents for every angular momentum we select these exponents of the generated sets, $f_k = [fmin, fmax]$, 
  so that $fmin <= fmin(guiding set)$ and $fmax >= fmax(guiding set)$

