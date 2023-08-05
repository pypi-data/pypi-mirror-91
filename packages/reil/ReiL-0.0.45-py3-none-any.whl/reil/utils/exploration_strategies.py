# -*- coding: utf-8 -*-
'''
exploration_strategies module
=============================

Contains classes that mimics exploration strategies in reinforcement learning.

Classes
-------
ExplorationStrategy:
    The base class for all exploration strategies.

ConstantEpsilonGreedy:
    An epsilon greedy object with constant epsilon

VariableEpsilonGreedy:
    An epsilon greedy object that accepts a uni-variate
    function to determine epsilon.
'''
import random
import warnings
from typing import Callable

from reil import reilbase


class ExplorationStrategy(reilbase.ReilBase):
    '''
    The base class for all exploration strategies.
    '''

    def __init__(self) -> None:
        pass

    def explore(self, epoch: int = 0) -> bool:
        '''
        Return `True` if the `agent` needs to explore.

        Arguments
        ---------
        epoch:
            The current epoch number.

        Returns
        -------
        :
            `True` if the caller should explore, otherwise `False`.
        '''
        return True


class ConstantEpsilonGreedy(ExplorationStrategy):
    '''
    An epsilon greedy object with constant epsilon.
    '''

    def __init__(self, epsilon: float) -> None:
        '''
        Arguments
        ---------
        epsilon:
            The value of epsilon

        Notes
        -----
        If epsilon is not in the range of [0, 1], a warning is being issued,
        but it does not raise an exception.
        '''
        if not (0.0 <= epsilon <= 1.0):
            warnings.warn('epsilon is not in the range of [0, 1].')
        self._epsilon = epsilon

    def explore(self, epoch: int = 0) -> bool:
        '''
        Return `True` if a randomly generated number is less than `epsilon`.

        Arguments
        ---------
        epoch:
            The current epoch number.

        Returns
        -------
        :
            `True` if the caller should explore, otherwise `False`.
        '''
        return random.random() < self._epsilon


class VariableEpsilonGreedy(ExplorationStrategy):
    '''
    An epsilon greedy object with constant epsilon.
    '''

    def __init__(self, epsilon: Callable[[int], float]) -> None:
        '''
        Arguments
        ---------
        epsilon:
            A uni-variate function that computes `epsilon` based on `epoch`.

        Raises
        ------
        TypeError:
            `epsilon` is not callable.
        '''
        if not callable(epsilon):
            raise TypeError('epsilon should be callable. '
                            'For constant epsilon, '
                            'use `ConstantEpsilonGreedy` class.')
        self._epsilon = epsilon

    def explore(self, epoch: int) -> bool:
        '''
        Return `True` if a randomly generated number is less than `epsilon`.

        Arguments
        ---------
        epoch:
            The current epoch number.

        Returns
        -------
        :
            `True` if the caller should explore, otherwise `False`.
        '''
        return random.random() < self._epsilon(epoch)
