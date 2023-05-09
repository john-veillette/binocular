from psychopy.core import getTime, wait
from psychopy import visual, event
import numpy as np
from psychopy.visual.filters import makeGrating


HOW_LONG_TO_PLAY = 10.

win = visual.Window(
    size = [400, 400],
    fullscr = False,
    units = "pix",
    winType = 'pyglet'
)

def make_gratings(win,
    red_cycles = 10, red_phase = 0.,
    blue_cycles = 3, blue_phase = 0.,
    grating_res = 256):

    red_grating = makeGrating(
        res = grating_res,
        ori = 45.,
        cycles = red_cycles,
        phase = red_phase,
        gratType = 'sqr'
        )
    blue_grating = makeGrating(
        res = grating_res,
        ori = 3*45.,
        cycles = blue_cycles,
        phase = blue_phase,
        gratType = 'sqr'
        )
    grating = np.ones((grating_res, grating_res, 3)) * -1.0 # black background
    grating[..., 0] = red_grating
    grating[..., -1] = blue_grating
    stim = visual.GratingStim(
        win = win,
        tex = grating,
        #mask = "circle",
        size = (grating_res, grating_res),
    )
    return stim

def draw_next_stims(win, period_red = .5, period_blue = .2):
    secs = getTime()
    deg_red = (secs % period_red)/period_red * 360
    deg_blue = (secs % period_blue)/period_blue * 360
    stim = make_gratings(
        win,
        red_cycles = 10, blue_cycles = 10,
        red_phase = deg_red, blue_phase = deg_blue,
        )
    stim.draw()
    fixation = visual.TextStim(win, text = '+', color = "white", pos = (0, 0))
    fixation.draw()


t0 = getTime()
done = False
secs_list = []
draw_next_stims(win)
while not done:
    secs = getTime()
    secs_list.append(secs)
    if secs - t0 > HOW_LONG_TO_PLAY:
        done = True
    win.callOnFlip(draw_next_stims, win)
    #draw_next_stims(win)
    win.getMovieFrame(buffer = 'back')
    win.flip()

win.saveMovieFrames(fileName = 'binocular-stim.mp4')
win.close()
arr = np.array(secs_list)
isi = np.diff(arr).mean()
print(1/isi)
