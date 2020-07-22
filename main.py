# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 21:29:49 2020

@author: Matthew
"""
from os.path import dirname, join
from bokeh.palettes import turbo
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import (ColumnDataSource, Select, MultiChoice, Div, Panel, Tabs,
                          Paragraph, Button, CustomJS,  CheckboxGroup, Text)
from custom_extensions import IonRangeSlider
from bokeh.layouts import row, layout, column
from bokeh.io import curdoc
import pandas as pd
import itertools
import plot_tools #custom functions for saving time and space
import time
import csv



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
total_fig = plot_tools.make_plot('Wavelength (nm)', 'Total Reflectance (%)', 'Total Reflectance vs nm')
total_fig.x_range.start = 250
total_fig.x_range.end = 2500

spec_fig = plot_tools.make_plot('Angle', 'Specular Reflectance', 'Specular Reflectance vs Angle')
lamb_fig = plot_tools.make_plot('Angle', 'Power (uW)', 'Lambertian Reflectance vs Angle')
lamb_resid_fig = plot_tools.make_plot('Angle', 'Power (uW)', 'Lambertian-Residual Reflectance vs Angle')
#palette for total reflecatance
total_palette = turbo(len(black_tot_df.data) + len(white_tot_df.data))
#palette for specular reflectance
colors = itertools.cycle(palette)

def plot_lines(df, color_offset, visible, tags):
    renderers = []
    for name, color in zip(df.data, total_palette[color_offset:]):
        if name != 'nm':
            r = total_fig.line('nm', name, line_width = .7, color = color,
                               source = df, visible = visible, name = name, tags = tags)
            renderers.append(r)
    return renderers

#total renderers
black_tot_renderers = plot_lines(black_tot_df, 0, False, ["black_tot"])
white_tot_renderers = plot_lines(white_tot_df, len(black_tot_df.data), False, ["white_tot"])

#specular renderers
black_spec_ref_renderers = plot_tools.plot_spec(black_spec_ref_ds, colors, spec_fig,'Angle (Deg)', False, ["black_spec"])
black_spec_ratio_renderers = plot_tools.plot_spec(black_spec_ratio_ds, colors, spec_fig,'Angle (Deg)', False, ["black_ref"])

#lambertian renderers
white_lamb_renderers = plot_tools.plot_lamb(white_lamb_scaled_ds, colors, lamb_fig, 'Angle (Deg)', False)
white_lamb_pow_renderers = plot_tools.plot_lamb_pow(white_lamb_pow_ds, colors, lamb_fig, 'Angle (Deg)', False)
white_lamb_resid_renderers = plot_tools.plot_resid(white_lamb_res_ds, colors, lamb_resid_fig, 'Angle (Deg)', False)

all_black_renderers = black_tot_renderers + black_spec_ref_renderers
all_white_renderers = white_tot_renderers + white_lamb_renderers + white_lamb_pow_renderers + white_lamb_resid_renderers
all_renderers = black_tot_renderers + white_tot_renderers + black_spec_ref_renderers + black_spec_ratio_renderers + white_lamb_renderers + white_lamb_pow_renderers + white_lamb_resid_renderers


multiChoiceList = []
for rnds in all_renderers:
    if rnds.name not in multiChoiceList:
        multiChoiceList.append(rnds.name)

checkbox_groups = []
checkbox_groups.append(CheckboxGroup(labels = black_tot_df.column_names[1:], width = 215))
btk_text = Div(text="Black Total Data:")
checkbox_groups.append(CheckboxGroup(labels = white_tot_df.column_names[1:]))
wtk_text = Div(text="White Total Data:")
checkbox_groups.append(CheckboxGroup(labels = black_spec_ref_ds.column_names[1:], width = 125))
bsk_text = Div(text="Black Specular Data:")
checkbox_groups.append(CheckboxGroup(labels = black_spec_ratio_ds.column_names[1:], width = 125))
bsrk_text = Div(text="Black Specular Ratio Data:")
checkbox_groups.append(CheckboxGroup(labels = white_lamb_scaled_ds.column_names[1:], width = 125))
wls_text = Div(text="White Lambertian Data:")
checkbox_groups.append(CheckboxGroup(labels = white_lamb_pow_ds.column_names[1:], width = 125))
wlss_text = Div(text="White Lambertian Scaled Data:")
checkbox_groups.append(CheckboxGroup(labels = white_lamb_res_ds.column_names[1:], width = 125))
wrs_text = Div(text="White Lambertian Residual Data:")

multiChoice = MultiChoice(title = "Show/Hide Materials", options = multiChoiceList, name = "multi")
#Select Widgets
mat_color_select = Select(title="Filter Material Color", options=['Select Material','Black', 'White', 'All'], value = 'Select Material', name = "color")
spec_select = Select(title = "Variable Type", options = ['Reflectance', 'Ratio'], name = "spec_select")


tot_slider = IonRangeSlider(start = 250, end = 2500, step = 1, range = (250, 2500), sizing_mode = "scale_both", visible = False, title = 'Total Reflectance Range')
spec_slider = IonRangeSlider(start = 10, end = 160, step = 1, range = (10, 160), sizing_mode = "scale_both", visible = False, title = 'Specular Reflectance Range')
lamb_slider = IonRangeSlider(start = 10, end = 90, step = 1, range = (10, 90), sizing_mode = "scale_both", visible = False, title = 'Lambertian Reflectance Range')
resid_slider = IonRangeSlider(start = 10, end = 90, step = 1, range = (10, 90), sizing_mode = "scale_both", visible = False, title = 'Lambertian Residual Range')

totb_button = Button(label = "Download Black Total Reflectance Data", button_type = "success")
totw_button = Button(label = "Download White Total Reflectance Data", button_type = "success")
spec_button = Button(label = "Download Specular Reflectance Data", button_type = "success")
spec_rat_button = Button(label = "Download Specular Reflectance Ratio Data", button_type = "success")
lamb_button = Button(label = "Download Lambertian Reflectance Data", button_type = "success")
resid_button = Button(label = "Download Lambertian Residual Reflectance Data", button_type = "success")
selec_button = Button(label = "Download Selected Materials Data", button_type = "success")

tot_fig_label = plot_tools.make_label(total_fig, True)
spec_fig_label = plot_tools.make_label(spec_fig, True)
lamb_fig_label = plot_tools.make_label(lamb_fig, True)

#update callback for total reflectance select widget
def update_mat_color(attr, old, new):
    if new == 'Select Material':
        for all_rnd in all_renderers:
            all_rnd.visible = False
        tot_fig_label.visible, spec_fig_label.visible, lamb_fig_label.visible = True, True, True
        spec_select.disabled = True
    elif new == 'All':
        start = time.time()
        for all_rnd in all_renderers:
            all_rnd.visible = True
        tot_fig_label.visible, spec_fig_label.visible, lamb_fig_label.visible = False, False, False
        spec_select.disabled = False
        end = time.time()
        print(end - start)
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

def update_tabs(attr, old, new):
    wv = new == 2
    tot_slider.visible, spec_slider.visible, lamb_slider.visible, resid_slider.visible = wv, wv, wv, wv

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

selec_button.js_on_click(CustomJS(args=dict(groups = checkbox_groups, rnds = all_renderers),
                                     code=open(join(dirname(__file__), "selec_download.js")).read()))
totb_button.js_on_click(CustomJS(args=dict(source= black_tot_df),
                                     code=open(join(dirname(__file__), "download.js")).read()))
totw_button.js_on_click(CustomJS(args=dict(source= white_tot_df),
                                     code=open(join(dirname(__file__), "download.js")).read()))
spec_button.js_on_click(CustomJS(args=dict(source= black_spec_ref_ds),
                                     code=open(join(dirname(__file__), "download.js")).read()))
spec_rat_button.js_on_click(CustomJS(args=dict(source= black_spec_ratio_ds),
                                     code=open(join(dirname(__file__), "download.js")).read()))
lamb_button.js_on_click(CustomJS(args=dict(source=white_lamb_scaled_ds),
                                     code=open(join(dirname(__file__), "download.js")).read()))
resid_button.js_on_click(CustomJS(args=dict(source=white_lamb_res_ds),
                                     code=open(join(dirname(__file__), "download.js")).read()))

total_fig.add_tools(plot_tools.make_hovertool('nm','nm', 'Total Reflectance %'))
spec_fig.add_tools(plot_tools.make_hovertool('{Angle (Deg)}','Angle', 'Specular Reflectance %'))
lamb_fig.add_tools(plot_tools.make_hovertool('{Angle (Deg)}','Angle', 'Lambertian Reflectance %'))
lamb_resid_fig.add_tools(plot_tools.make_hovertool('{Angle (Deg)}', 'Angle', 'Residual Reflect'))


total_fig.add_layout(tot_fig_label)
spec_fig.add_layout(spec_fig_label)
lamb_fig.add_layout(lamb_fig_label)
lamb_resid_fig.add_layout(lamb_fig_label)

spacer = Div(text = "", width = 200)
instructions = Div(text = """<h6><b>Welcome to the Black and White materials data application. In order to interact with the plots, please use the navigation tabs above.</b></h6>""")
filter_instr = Div(text = """<blockquote><p class="my-text"><b>Filters:</b> <i>Material Color</i>, <i>Specific Material</i>, or <i>Specular Reflectance Display</i>. Use the 'Filter Material Color' dropdown menu to see data for black materials, white materials, or even all of them but if you choose to see them all the graphs may get cluttered. Use the 'Show/Hide Material' menu to view specific materials; you can either type in a material name in order to find it or scroll through the list of options.</p></blockquote><blockquote><p class="my-text"><b>Range Sliders:</b> You can use the range sliders in order to narrow down the range x range of nano-meters or degrees that you would like to view, just slide the the minimum value and maximum value bars to your liking.</p></blockquote><blockquote><p class="my-text"><b>Download Data:</b> If you are interested in downloading the data shown in these plots to see for yourself, navigate to the "Select Data to Download" tab. Here the data is categorically sorted in the manner that it is displayed in the graphs below. Once you have decided what data you would like to download, select the materials by clicking on the checkbox next to its name and then proceed over to the "Downloads" tab. Once here click the "Downlaod Selected Materials" button and your download should immediately begin. If you want entire sets of data or are not quite sure what you would prefer, select from any other of the possible downloadable options and the download will automatically begin for your chosen category.</p></blockquote><blockquote><p class="my-text"><b>Other Tools:</b> There are a variety of ways to interact with the data in the different plots and more to come! At the bottom of each graph you will find a toolbar with different symbols. The 'Pan' option will allow you to click and drag the graph to shift the displayed data, the 'box zoom' tool allows you to click and drag a specific box area to zoom in on while the 'Wheel Zoom' tool allows you to zoom using your mouse wheel or your trackpad, and the save button will download a screenshot of the current status of the plot you are viewing. If you are curious about what material you are viewing or what its exact data is, hover over the line with your mouse and its information will be displayed.</p></blockquote>""", height = 300)

total_fig.name = "total"
spec_fig.name = "spec"
lamb_fig.name = "lamb"
lamb_resid_fig.name = "resid"

instr_layout = column(instructions, filter_instr, sizing_mode = 'scale_width', height = 200, css_classes = ['scrollable'])
filter_layout = row(mat_color_select, spec_select, multiChoice, sizing_mode = 'scale_width')
slider_layout = row(tot_slider, spec_slider, lamb_slider, resid_slider)
download_layout = row(column(btk_text, checkbox_groups[0]), column(wtk_text, checkbox_groups[1]), column(bsk_text, checkbox_groups[2], bsrk_text, checkbox_groups[3]),
                      column(wls_text, checkbox_groups[4], wlss_text, checkbox_groups[5]), column(wrs_text, checkbox_groups[6]), height = 400, sizing_mode = 'fixed', css_classes = ['scrollable'])
lay = row(column(totb_button, totw_button), column(spec_button, spec_rat_button), column(lamb_button, resid_button, selec_button))

intro_tab = Panel(child = instr_layout, title = "Instructions")
filter_tab = Panel(child = filter_layout, title = "Filters")
slider_tab = Panel(child = slider_layout, title = "Range Sliders")
download_tab = Panel(child = download_layout, title = "Select Data to Download")
download_tab2 = Panel(child = lay, title = "Download")

tabs = Tabs(tabs = [intro_tab, filter_tab, slider_tab, download_tab, download_tab2], active = 0, name = "tabs", css_classes = ["white"])

tabs.on_change('active', update_tabs)

spec_fig.plot_height = 250
lamb_fig.plot_height = 400
lamb_resid_fig.plot_height = 400
total_fig.plot_height = 250

curdoc().add_root(total_fig)
curdoc().add_root(spec_fig)
curdoc().add_root(lamb_fig)
curdoc().add_root(lamb_resid_fig)
curdoc().add_root(tabs)

curdoc().title = "B/W Materials Reflectance"