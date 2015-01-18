#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt

VIDEO_TAG = """<video controls>
 <source src="data:video/x-webm;base64,{0}" type="video/webm">
 Your browser does not support the video tag.
</video>"""

def anim_to_html(anim, fps = 10):
    if not hasattr(anim, '_encoded_video'):
        with NamedTemporaryFile(suffix='.webm') as f:
            anim.save(f.name, fps=fps, extra_args=['-vcodec', 'libvpx'])
            video = open(f.name, "rb").read()
        anim._encoded_video = video.encode("base64")

    return VIDEO_TAG.format(anim._encoded_video)

from IPython.display import HTML

def display_animation(anim, fps = 10):
    plt.close(anim._fig)
    return HTML(anim_to_html(anim, fps))
