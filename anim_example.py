#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as no
from JSAnimation.IPython_display import anim_to_html

def animation_metropolis(metropolis, woi = 0, frames = 1000, interval = 1 ,
                         fps = 5, step_max = 0.1):
    # set up the figure and axis
    L = metropolis.L
    R = metropolis.R
    fig = plt.figure()
    ax = plt.axes(xlim=(-L/2, L/2), ylim=(-L/2, L/2), aspect='equal')

    # create spheres and add to axis
    sphere_one = plt.Circle(metropolis.w_c[woi,0:2],R, color='b')
    sphere_two = plt.Circle(metropolis.w_c[woi,2:4],R, color='b')
    patch_one = ax.add_patch(sphere_one)
    patch_two = ax.add_patch(sphere_two)

    # function to execute between animations
    def animate(i):
        metropolis.step(n_steps=1, step_max = step_max)
        patch_one.center = metropolis.w_c[woi,0:2]
        patch_two.center = metropolis.w_c[woi,2:4]
        return (patch_one, patch_two)

    # create and return html animation
    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=interval)
    return anim_to_html(anim, fps=fps, default_mode = "reflect")
