.. module:: cellrank.estimators

Estimators
==========
Estimators enable quantitative analysis of Markov transition matrices computed using CellRank
:doc:`kernels <kernels>`, including automatic detection of initial and terminal states, and computation
of fate probabilities. Our recommended estimator is the :class:`~cellrank.estimators.GPCCA` estimator.

.. currentmodule:: cellrank

.. autosummary::
    :toctree: _autosummary/estimators

    estimators.GPCCA
    estimators.CFLARE
