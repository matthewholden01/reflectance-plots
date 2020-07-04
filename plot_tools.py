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


def plot_spec(ds, myPalette, fig, index, visible):
    renderers = []
    for name, color in zip(ds.data, myPalette):
        if name != index:
            r = fig.line(index, name, color = color, line_width = .7, 
                         source = ds, visible = visible, name = name)
            renderers.append(r)
    return renderers

def plot_lamb(ds, ds2, myPalette, fig, index, visible):
    renderers = []
    for name, name2, color in zip(ds.data, ds2.data, myPalette):
        if name != index:
            r = fig.line(index, name, color = color, line_width = .7, 
                         source = ds, visible = visible, name = name)
            f = fig.line(index, name2, color = color, line_width = .7, 
                         source = ds2, visible = visible, line_dash = 'dashed', name = name2)
            c = fig.circle(index, name2, color = color, source = ds2, visible = visible, 
                           name = name2)
            renderers.append(r)
            renderers.append(f)
            renderers.append(c)
    return renderers

def plot_dash_dots(ds, myPalette, fig, index, visible):
    renderers = []
    for name, color in zip(ds.data, myPalette):
        if name != index:
            r = fig.line(index, name, line_width = .7, line_dash = 'dashed', 
                         color = color, source = ds, visible = visible, name = name)
            f = fig.circle(index, name, color = color, source = ds, visible = visible,
                           name = name)
            renderers.append(r)
            renderers.append(f)
    return renderers

def make_label(figure, visibility):
    new_label = Label(x = figure.plot_width / 2, y = figure.plot_height / 2,
                      x_units = 'screen', y_units = 'screen', 
                      text = 'No Data For this Material', visible = visibility)
    return new_label