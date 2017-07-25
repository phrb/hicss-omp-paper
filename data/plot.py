#! /usr/bin/python

import re
import os
import matplotlib as mpl

import math
import numpy

import csv

mpl.use('agg')

import matplotlib.pyplot as plt
import numpy as np

def config_matplotlib():
    plt.rc('text', usetex = True)
    plt.rc('font', family = 'serif')

    font = {'family' : 'serif',
            'size'   : 28}

    mpl.rc('font', **font)

def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., height + .03,
                '%.2f' % height,
                ha = 'center', va = 'bottom', rotation = '0')

def plot_bar_stacks(data,
                    xlabel,
                    ylabel,
                    index_range,
                    width,
                    tick_labels,
                    file_title,
                    title,
                    ymin,
                    ymax,
                    color_map):

    indexes = np.arange(index_range)
    fig     = plt.figure(1, figsize=(18, 10))
    ax      = fig.add_subplot(111)

    rects   = []

    legend_names = []
    legend_rects = []

    previous_bottom = np.zeros(len(list(data.values())[0]))

    cmap = mpl.cm.get_cmap(color_map)
    colors = len(list(data.keys()))
    c_index = 0

    for key, value in data.items():
        rect = ax.bar(indexes, value, width, color = cmap(1. * (c_index / colors)), edgecolor = 'lightgrey', bottom = previous_bottom)

        c_index += 1

        previous_bottom += value

        legend_rects.append(rect[0])
        legend_names.append(key)

        rects.append(rects)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xticks(indexes)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(tick_labels, rotation = '15', ha = 'right')

    ax.set_ylim([ymin, ymax])

    legend = ax.legend(tuple(legend_rects), tuple(legend_names),
                        loc = 9, bbox_to_anchor = [0.5, 1.15], ncol = len(list(data.keys())), shadow = True,
                        title = "", fancybox = True)

    #autolabel(rects, ax)

    plt.tight_layout()

    fig.savefig("{0}.eps".format(file_title), format = 'eps', dpi = 2000,
                bbox_extra_artists=(legend,), bbox_inches = 'tight')

    plt.clf()

def plot_bar(data,
             xlabel,
             ylabel,
             index_range,
             width,
             tick_labels,
             file_title,
             title,
             ymin,
             ymax,
             line,
             color_map):

    indexes = np.arange(index_range)
    fig     = plt.figure(1, figsize=(18, 10))
    ax      = fig.add_subplot(111)

    cmap = mpl.cm.get_cmap(color_map)
    colors = len(data)
    c_index = 0

    color = [cmap(1. * (c_index / colors)) for c_index in range(len(data))]

    rects   = ax.bar(indexes, data, width, color = color, edgecolor = 'black')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xticks(indexes)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(tick_labels, rotation = '0')

    ax.set_ylim([ymin, ymax])

    if line:
        ax.axhline(y=1., color='r')

    #legend = ax.legend((rects1[0], rects2[0]), ('Default Start', 'Random Start'),
    #                    loc = 9, bbox_to_anchor = [0.5, -0.1], ncol = 4, shadow = True,
    #                    title = "", fancybox = True)

    autolabel(rects, ax)

    plt.tight_layout()

    fig.savefig("{0}.eps".format(file_title), format = 'eps', dpi = 2000, bbox_inches = 'tight')

    plt.clf()

def plot_heatmap(data,
                 ylabels,
                 xlabels,
                 ylabel,
                 xlabel,
                 file_title,
                 title):

    #print(data.shape)

    fig     = plt.figure(1, figsize=(18, 10))
    ax      = fig.add_subplot(111)

#    aux = data[-1]
#
#    data[-1] = data[-2]
#
#    data[-2] = aux

    heatmap = plt.pcolor(data, cmap = plt.cm.RdBu_r, vmin = 0.5, vmax = 1.5, edgecolors='gray')
    #plt.colorbar()

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if data[y, x] <= 0.65 or data[y, x] >= 1.45:
                cell_color = 'white'
            else:
                cell_color = 'black'

            plt.text(x + 0.5, y + 0.5, '%.2f' % data[y, x],
                    horizontalalignment='center',
                    verticalalignment='center',
                    color=cell_color,
                    usetex=True
                    )

    xlabels = ["FMax", "DSP", "Cycles", "Blocks", "Regs", "BRAM", "Pins", "LUTs", "\\textbf{WNS}"]
    xlabels.reverse()

    ax.set_yticks(np.arange(len(ylabels)) + 0.5, minor = False)
    ax.set_xticks(np.arange(len(xlabels)) + 0.5, minor = False)

    ax.set_title(title)
    #ax.set_xlabel(xlabel)
    ax.set_xticklabels(xlabels, minor=False)
    #ax.set_ylabel(ylabel)
    ax.set_yticklabels(ylabels, minor=False)

    #plt.xticks(rotation = 45)
    #plt.yticks(rotation = 45)

    plt.tight_layout()

    fig.savefig("{0}.eps".format(file_title), format = 'eps', dpi = 2000, bbox_inches = 'tight')

    plt.clf()

if __name__ == '__main__':
    config_matplotlib()

    datafile = "student_responses.csv"
    data = {}

    with open(datafile, 'rU') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]

    background = ['cpp', 'java', 'python', 'ruby', 'c', 'openmp', 'pthreads']
    classes    = ['had_concepts', 'knew_apis', 'helped_openmp_class', 'helped_pthreads_class']
    learning   = ['learn_openmp', 'learn_pthreads']
    using      = ['par_loop_openmp', 'par_loop_pthreads', 'par_nested_loop_openmp', 'par_nested_loops_pthreads', 'improve_seq_openmp', 'improve_seq_pthreads']
    comparing  = ['harder_learn', 'simpler_tech', 'easier_tech', 'easier_par_loop', 'easier_nested_par_loop', 'easier_improve_seq']

    background_mean_data = []

    for tech in background:
        background_mean_data.append(np.mean([float(i) for i in data[tech]]))

    print(background_mean_data)

    plot_bar(background_mean_data,
             "Technology",
             "Previous Knowledge",
             len(background_mean_data),
             .9,
             [i.title() for i in background],
             "background_mean_knowledge",
             "",
             1,
             5,
             False,
             "viridis")

    classes_norm_data = []

    for topic in classes:
        ratio = 0

        for answer in data[topic]:
            if answer == "Sim":
                ratio += 1

        ratio /= len(data[topic])
        classes_norm_data.append(ratio * 100)

    print(classes_norm_data)

    plot_bar(classes_norm_data,
             "",
             "Percentage of Students",
             len(classes_norm_data),
             .9,
             [i.replace("_", "\\_") for i in classes],
             "yes_no_questions",
             "",
             0,
             100,
             False,
             "viridis")

    using_data = {}

    levels = {"Concordo fortemente": "SA",
              "Concordo": "A",
              "Não concordo nem discordo": "N",
              "Discordo": "D",
              "Discordo fortemente": "SD"}

    for subject in using:
        sub_data = data[subject]
        using_data[subject] = {}

        for response in sub_data:
            try:
                using_data[subject][levels[response]] += 1
            except KeyError:
                using_data[subject][levels[response]] = 1

        for key in using_data[subject].keys():
            using_data[subject][key] *= 100 / len(sub_data)

    print(using_data)

    stacked_using_data = {}

    for value in levels.values():
        for key in using_data.keys():
            if value not in using_data[key].keys():
                using_data[key][value] = 0
            try:
                stacked_using_data[value].append(using_data[key][value])
            except KeyError:
                stacked_using_data[value] = [using_data[key][value]]


    plot_bar_stacks(stacked_using_data,
                    "",
                    "Percentage of Likert Scale Values",
                    len(stacked_using_data["SA"]),
                    1.,
                    [i.replace("_", "\\_") for i in using],
                    "likert_questions",
                    "",
                    0,
                    100,
                    "viridis")

    print(stacked_using_data)

    comparing_data = {}

    levels = {"OpenMP": "OpenMP",
              "POSIX Threads": "Pthreads"}

    for subject in comparing:
        sub_data = data[subject]
        comparing_data[subject] = {}

        for response in sub_data:
            try:
                comparing_data[subject][levels[response]] += 1
            except KeyError:
                comparing_data[subject][levels[response]] = 1

        for key in comparing_data[subject].keys():
            comparing_data[subject][key] *= 100 / len(sub_data)

    print(comparing_data)

    stacked_comparing_data = {}

    for value in levels.values():
        for key in comparing_data.keys():
            if value not in comparing_data[key].keys():
                comparing_data[key][value] = 0
            try:
                stacked_comparing_data[value].append(comparing_data[key][value])
            except KeyError:
                stacked_comparing_data[value] = [comparing_data[key][value]]


    plot_bar_stacks(stacked_comparing_data,
                    "",
                    "Percentage",
                    len(stacked_comparing_data["OpenMP"]),
                    1.,
                    [i.replace("_", "\\_") for i in comparing],
                    "comparisons",
                    "",
                    0,
                    100,
                    "viridis")

    print(stacked_comparing_data)
