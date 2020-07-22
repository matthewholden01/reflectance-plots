# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 22:02:17 2020

@author: Matthew
"""

from bokeh.plotting import figure
from bokeh.models import HoverTool, Label

def make_hovertool(x,x_label,y):
    hovertool = HoverTool(tooltips = [('Material: ', '$name'),
                                      (x_label, '@' + x),
                                      (y, '@$name')],
                          mode = 'mouse')
    return hovertool

def make_plot(x_label, y_label, title):
    fig = figure(plot_width = 650, plot_height = 350,
           title = title, 
           x_axis_label = x_label, y_axis_label = y_label,
           title_location = 'above', sizing_mode = "scale_both",
           toolbar_location = "below",
           tools = "box_zoom, pan, wheel_zoom, save", 
           border_fill_alpha = 0.6)
    fig.x_range.range_padding = 0
    fig.x_range.only_visible = True
    fig.y_range.only_visible = True
    
    return fig


def plot_spec(ds, myPalette, fig, index, visible, tags):
    renderers = []
    for name, color in zip(ds.data, myPalette):
        if name != index:
            r = fig.line(index, name, color = color, line_width = .7, 
                         source = ds, visible = visible, name = name, tags = tags)
            renderers.append(r)
    return renderers

def plot_lamb(ds, myPalette, fig, index, visible):
    renderers = []
    for name, color in zip(ds.data, myPalette):
        if name != index:
            r = fig.line(index, name, color = color, line_width = .7, 
                         source = ds, visible = visible, name = name, tags = ["white_lamb"])
            renderers.append(r)
    return renderers

def plot_lamb_pow(ds, myPalette, fig, index, visible):
    renderers = []
    for name, color in zip(ds.data, myPalette):
        if name != index:
            f = fig.line(index, name, color=color, line_width=1,
                         source=ds, visible=visible, line_dash='dotdash', name=name, tags=["white_lamb"])
            renderers.append(f)
    return renderers

def plot_resid(ds, myPalette, fig, index, visible):
    renderers = []
    for name, color in zip(ds.data, myPalette):
        if name != index:
            r = fig.line(index, name, line_width = 1, line_dash = 'dotdash',
                         color = color, source = ds, visible = visible, name = name, tags = ["white_res"])
            renderers.append(r)
    return renderers

def make_label(figure, visibility):
    new_label = Label(x = figure.plot_width / 2, y = figure.plot_height / 2,
                      x_units = 'screen', y_units = 'screen', 
                      text = 'No Data For this Material', visible = visibility)
    return new_label