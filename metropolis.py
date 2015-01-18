#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from numpy.random import random_sample, random_integers

class two_spheres_metropolis:
    """Metropolis-Hastings for two hard spheres in a box system

    This class implements Metropolis-Hastings method for a simple
    system of two hard spheres in a box

    Parameters
    ----------
    L : float
        Length of the box
    R : float
        Radius of the spheres
    n_walkers : int
        Number of systems (i.e. walkers) to consider
    w_centers : [float, float, float, float] (optional)
        Initial center positions for all the walkers, if used
        each walker will be randomly started in a valid position

    """
    def __init__(self, L, R, n_walkers, w_centres = None):
        self.L = L
        self.R = R
        self.n_walkers = n_walkers
        if w_centres:
            self.w_c = np.tile(w_centres, (self.n_walkers,1))
        else:
            self.w_c = self.random_walkers()

    def random_walkers(self):
        """Return an array of valid random sphere centres"""
        # sample uniform random (no wall overlap)
        shift = -self.L/2+self.R # center box
        factor = self.L-2*self.R # remove space near wall
        w_c = shift+factor*random_sample((self.n_walkers,4))
        # check overlap and sample again  if required
        overlap = self.overlap(w_c[:,0:2], w_c[:,2:4])
        while np.sum(overlap) > 0:
            w_c[overlap,2:4] = shift+factor*random_sample((np.sum(overlap),2))
            overlap = self.overlap(w_c[:,0:2], w_c[:,2:4])
        return w_c

    def overlap(self,s1_c, s2_c):
        """Return a boolean array True if spheres will overlap (False if not)"""
        dist = np.sqrt((s1_c[:,0]-s2_c[:,0])**2 + (s1_c[:,1]-s2_c[:,1])**2)
        return (dist < 2*self.R)

    def is_wall(self,s_c):
        """Return a boolean array True if sphere will collide with wall"""
        return (np.abs(s_c) > (self.L/2-self.R)).any(axis = 1)

    def inter_distance(self):
        """Return an array with distance between spheres for all walkers"""
        s1_c, s2_c = self.w_c[:,0:2], self.w_c[:,2:4]
        return np.sqrt((s1_c[:,0]-s2_c[:,0])**2 + (s1_c[:,1]-s2_c[:,1])**2)

    def wall_distance(self):
        """Return an array with minimum distance to wall for all walkers"""
        return np.min(self.L/2 - np.abs(self.w_c), axis=1)

    def step(self, n_steps= 1, step_max = None):
        """Perform one or several Metropolis-Hastings steps

        This method will update all the walkers with several
        Metropolis-Hastings steps.

        Parameters
        ----------
        n_steps : int (optional)
            Number of steps to iterate (one is default)
        step_max : float
            Maximum step_size in x or y direction, step size will
            be uniformly sampled from 0 to step_max

        Returns
        -------
        n_steps : int
            The number of steps will be returned.

        """
        if not step_max:
            step_max = self.R/np.pi
        for i in xrange(n_steps):
            # choose a random sphere for each walker
            sp = random_integers(0,1,size=(self.n_walkers,1)) == 1
            # get a random step size
            step = -step_max + 2*step_max*random_sample((self.n_walkers,2))
            # check if sphere will overlap or collide with wall
            overlap = self.overlap(self.w_c[:,0:2] + sp*step,
                                   self.w_c[:,2:4] + (-sp)*step)
            wall = self.is_wall(np.where(sp, self.w_c[:,0:2],
                                         self.w_c[:,2:4]) + step)
            # only perform step if probability is not null
            mv = - np.logical_or(overlap,wall)
            self.w_c[mv,0:2] = self.w_c[mv,0:2] + sp[mv]*step[mv]
            self.w_c[mv,2:4] = self.w_c[mv,2:4] + (-sp[mv])*step[mv]
        return n_steps
