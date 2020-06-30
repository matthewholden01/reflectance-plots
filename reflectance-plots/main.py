# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 21:29:49 2020

@author: Matthew
"""
from bokeh.palettes import turbo
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select, MultiChoice
from custom_extensions import IonRangeSlider
from bokeh.layouts import layout, row, column
from bokeh.io import curdoc
import pandas as pd
import itertools
import plot_tools #custom functions for saving time and space

doc = curdoc()
#handle specular data
black_spec_mat = pd.read_csv('reflectance-plots/data/Specular_Reflect_Data/Specular_material.csv').set_index('Angle (Deg)')

initial_intensity = 10.4629235
for name in black_spec_mat:
    black_spec_mat[name] = black_spec_mat[name] / initial_intensity
#Specular data sources
black_spec_ref_ds = ColumnDataSource(black_spec_mat)
black_spec_ratio_ds = ColumnDataSource(pd.read_csv('reflectance-plots/data/Specular_Reflect_Data/Spec_Ratio.csv').set_index('Angle (Deg)'))
#Total data sources
black_tot_df = ColumnDataSource(pd.read_csv('reflectance-plots/data/Total_Reflect_Data/Black_Materials_total_reflecatance.csv').set_index('nm'))
white_tot_df = ColumnDataSource(pd.read_csv('reflectance-plots/data/Total_Reflect_Data/SPIE18_white_all.csv').set_index('nm'))
#lamb data sources
white_lamb_pow_ds = ColumnDataSource(pd.read_csv('reflectance-plots/data/Lambertian_Reflect_Data/Lamb_Reflect_Power.csv').set_index('Angle (Deg)'))
white_lamb_scaled_ds = ColumnDataSource(pd.read_csv('reflectance-plots/data/Lambertian_Reflect_Data/Lamb_Reflect_Scaled.csv').set_index('Angle (Deg)'))
white_lamb_res_ds = ColumnDataSource(pd.read_csv('reflectance-plots/data/Lambertian_Reflect_Data/Lamb_Resid.csv').set_index('Angle (Deg)'))
#create figures plots 
total_fig = plot_tools.make_plot('Wavelength (nm)', 'Total Reflectance (%)', 'Total')
total_fig.x_range.start = 250
total_fig.x_range.end = 2500

spec_fig = plot_tools.make_plot('Angle', 'Specular Reflectance', 'Specular')
lamb_fig = plot_tools.make_plot('Angle', 'Power (uW)', 'Lambertian')
lamb_resid_fig = plot_tools.make_plot('Angle', 'Power (uW)', 'Lambertian-Residual')
lamb_resid_fig.plot_width = 650
lamb_resid_fig.plot_height = 250
#palette for total reflecatance
total_palette = turbo(len(black_tot_df.data) + len(white_tot_df.data))
#palette for specular reflectance
colors = itertools.cycle(palette)

def plot_lines(df, color_offset, visible):
    renderers = []
    for name, color in zip(df.data, total_palette[color_offset:]):
        if name != 'nm':
            r = total_fig.line('nm', name, line_width = .7, color = color,
                               source = df, visible = visible, name = name)
            renderers.append(r)
    return renderers

#total renderers
black_tot_renderers = plot_lines(black_tot_df, 0, False)
white_tot_renderers = plot_lines(white_tot_df, len(black_tot_df.data), False)

#specular renderers
black_spec_ref_renderers = plot_tools.plot_spec(black_spec_ref_ds, colors, spec_fig,'Angle (Deg)', False)
black_spec_ratio_renderers = plot_tools.plot_spec(black_spec_ratio_ds, colors, spec_fig,'Angle (Deg)', False)

#lambertian renderers
white_lamb_renderers = plot_tools.plot_lamb(white_lamb_scaled_ds, white_lamb_pow_ds, colors, lamb_fig, 'Angle (Deg)', False)
white_lamb_resid_renderers = plot_tools.plot_dash_dots(white_lamb_res_ds, colors, lamb_resid_fig, 'Angle (Deg)', False)

all_black_renderers = black_tot_renderers + black_spec_ref_renderers
all_white_renderers = white_tot_renderers + white_lamb_renderers + white_lamb_resid_renderers
all_renderers = all_black_renderers + all_white_renderers

multiChoiceList = []
for rnds in black_tot_renderers+white_tot_renderers:
    multiChoiceList.append(rnds.name)

multiChoice = MultiChoice(title = "Show/Hide Materials", options = multiChoiceList)
#Select Widgets
mat_color_select = Select(title="Filter Material Color", options=['Select Material','Black', 'White', 'All'], value = 'Select Material')
spec_select = Select(title = "Variable Type", options = ['Reflectance', 'Ratio'])

tot_slider = IonRangeSlider(start = 250, end = 2500, step = 1, range = (250, 2500), title = 'Total Reflectance Range')
spec_slider = IonRangeSlider(start = 10, end = 160, step = 1, range = (10, 160), title = 'Specular Reflectance Range')
lamb_slider = IonRangeSlider(start = 10, end = 90, step = 1, range = (10, 90), title = 'Lambertian Reflectance Range')
resid_slider = IonRangeSlider(start = 10, end = 90, step = 1, range = (10, 90), title = 'Lambertian Residual Range')

tot_fig_label = plot_tools.make_label(True)
spec_fig_label = plot_tools.make_label(True)
lamb_fig_label = plot_tools.make_label(True)

#update callback for total reflectance select widget
def update_mat_color(attr, old, new):
    if new == 'Select Material':
        for all_rnd in all_renderers:
            all_rnd.visible = False
        tot_fig_label.visible, spec_fig_label.visible, lamb_fig_label.visible = True, True, True
        spec_select.disabled = True
    elif new == 'All':
        for all_rnd in all_renderers:
            all_rnd.visible = True
        tot_fig_label.visible, spec_fig_label.visible, lamb_fig_label.visible = False, False, False
        spec_select.disabled = False
    else:
        wv = new == 'White'
        for blk_rnd in all_black_renderers:
            blk_rnd.visible = not wv
        for wht_rnd in all_white_renderers:
            wht_rnd.visible = wv
        spec_select.disabled, spec_fig_label.visible = wv, wv
        tot_fig_label.visible = False
        lamb_fig_label.visible = not wv

#update callback for specular reflectance select widget
#will probably be removed once specular data is fixed
def update_spec(attr, old, new):
    wv = new == 'Ratio'
    if wv:
        spec_fig.yaxis.axis_label = 'Specular Ratio (%)'
    else:
        spec_fig.yaxis.axis_label = 'Specular Reflectance'
    for r in black_spec_ratio_renderers:
        r.visible = wv
    for r in black_spec_ref_renderers:
        r.visible = not wv

def update_tot_slider(attr, old, new):
    low, high = new
    total_fig.x_range.start = low
    total_fig.x_range.end = high

def update_spec_slider(attr, old, new):
    low, high = new
    spec_fig.x_range.start = low
    spec_fig.x_range.end = high

def update_lamb_slider(attr, old, new):
    low, high = new
    lamb_fig.x_range.start = low
    lamb_fig.x_range.end = high

def update_resid_slider(attr, old, new):
    low, high = new
    lamb_resid_fig.x_range.start = low
    lamb_resid_fig.x_range.end = high

def update_multi_choice(attr, old, new):
    for x in all_renderers:
        if x.name in multiChoice.value:
            x.visible = True
        else:
            x.visible = False
    tot_fig_label.visible = check_for_data(black_tot_renderers+white_tot_renderers)
    spec_fig_label.visible = check_for_data(black_spec_ref_renderers)
    lamb_fig_label.visible = check_for_data(white_lamb_renderers)
def check_for_data(renderers):
    for x in renderers:
        if x.visible:
            return False
    return True

tot_slider.on_change('range', update_tot_slider)
spec_slider.on_change('range', update_spec_slider)
lamb_slider.on_change('range', update_lamb_slider)
resid_slider.on_change('range', update_resid_slider)

mat_color_select.on_change('value', update_mat_color)
spec_select.on_change('value', update_spec)

multiChoice.on_change('value', update_multi_choice)
total_fig.add_tools(plot_tools.make_hovertool('nm','nm', 'Total Reflectance %'))
spec_fig.add_tools(plot_tools.make_hovertool('{Angle (Deg)}','Angle', 'Specular Reflectance %'))
lamb_fig.add_tools(plot_tools.make_hovertool('{Angle (Deg)}','Angle', 'Lambertian Reflectance %'))
lamb_resid_fig.add_tools(plot_tools.make_hovertool('{Angle (Deg)}', 'Angle', 'Residual Reflect'))


total_fig.add_layout(tot_fig_label)
spec_fig.add_layout(spec_fig_label)
lamb_fig.add_layout(lamb_fig_label)
lamb_resid_fig.add_layout(lamb_fig_label)

widgets = column(row(mat_color_select, spec_select, multiChoice),tot_slider, spec_slider,
                 lamb_slider, resid_slider)
plots = column(total_fig, spec_fig, lamb_fig, lamb_resid_fig)
doc_layout = row(plots, widgets, name = "rows")

doc.add_root(doc_layout)