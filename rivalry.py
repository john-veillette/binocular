from psychopy.core import getTime, wait
from psychopy import visual, event
from psychopy.visual import filters
import numpy as np

HOW_LONG_TO_PLAY = 10.

win = visual.Window(
    size=[800, 800],
    fullscr=False,
    units="pix"
)

def make_gratings(win,
    red_cycles = 10, red_phase = 0.,
    blue_cycles = 3, blue_phase = 0.,
    grating_res = 2*256):

    red_grating = filters.makeGrating(
        res = grating_res,
        ori = 45.,
        cycles = red_cycles,
        phase = red_phase
        )
    blue_grating = filters.makeGrating(
        res = grating_res,
        ori = 3*45.,
        cycles = blue_cycles,
        phase = blue_phase
        )
    grating = np.ones((grating_res, grating_res, 3)) * -1.0 # black background
    grating[..., 0] = red_grating
    grating[..., -1] = blue_grating
    stim = visual.GratingStim(
        win = win,
        tex = grating,
        mask = "circle",
        size = (grating_res, grating_res)
    )
    return stim

t0 = getTime()
done = False
while not done:
    secs = getTime()
    if secs - t0 > HOW_LONG_TO_PLAY:
        done = True
    deg = (secs % 1.) * 360
    stim = make_gratings(
        win,
        red_cycles = 5, blue_cycles = 5,
        red_phase = deg, blue_phase = deg,
        )
    stim.draw()
    fixation = visual.TextStim(win, text = '+', color = "white", pos = (0, 0))
    fixation.draw()
    win.getMovieFrame(buffer = 'back')
    win.flip()
    wait(1/60)

win.saveMovieFrames(fileName = 'binocular-stim.mp4')
win.close()
