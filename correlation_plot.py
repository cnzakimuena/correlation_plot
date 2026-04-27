"""
This code generates a correlation plot. The plot uses systolic blood pressure measurements 
from the arm and finger for demonstration. The appearance of the plot is customized and the final 
figure is saved.
"""
import os
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import seaborn as sns

# suppress pandas warning
pd.options.mode.chained_assignment = None


def generate_plot(measure1,
                  measure2,
                  x_range_array,
                  y_range_array,
                  independent_variable_label=None,
                  dependent_variable_label=None,
                  specified_colors='mediumblue',
                  super_title=None):
    """
    Calls function to generate a correlation plot for two sets of measurements and provides 
    customized aesthetics.
    """

    sns.set(style="whitegrid", font_scale=1.6)

    with plt.rc_context({'axes.edgecolor': 'black'}):

        fig, ax = plt.subplots(figsize=(6, 6))

        # correlation plot
        # generate basic scatterplot
        ax.plot(measure1, measure2, 'o',
                markerfacecolor=specified_colors,
                markeredgecolor=specified_colors,
                markersize=7)
        # obtain m (slope) and b(intercept) of linear regression line
        m, b = np.polyfit(measure1, measure2, 1)
        # add linear regression line to scatterplot
        ax.plot(measure1, m * measure1 + b, linewidth=2, color='black')

        r, _ = scipy.stats.pearsonr(measure1, measure2)
        annotation_size = 18
        ax.text(x_range_array[0] + 0.1 * (x_range_array[1] - x_range_array[0]),
                y_range_array[1] - 0.3 * (y_range_array[1] - y_range_array[0]),
                f"r = {r:.2f}\ns = {m:.2f}",
                size=annotation_size, color='black')

        # set x and y ranges
        ax.set(xlim=(x_range_array[0] - 0.1 * (x_range_array[1] - x_range_array[0]),
                     x_range_array[1] + 0.1 * (x_range_array[1] - x_range_array[0])))
        ax.set(ylim=(y_range_array[0] - 0.1 * (y_range_array[1] - y_range_array[0]),
                     y_range_array[1] + 0.1 * (y_range_array[1] - y_range_array[0])))

        # set x and y labels
        if independent_variable_label is not None:
            ax.set_xlabel(independent_variable_label)
        if dependent_variable_label is not None:
            ax.set_ylabel(dependent_variable_label)

        # alter axis line size
        # change all spines
        for axis in ['top', 'bottom', 'right', 'left']:
            ax.spines[axis].set_linewidth(2)

        # only show ticks on the left and bottom spines
        ax.get_yaxis().tick_left()
        ax.get_xaxis().tick_bottom()

        # specify ticks
        ax.set_xticks(np.linspace(x_range_array[0], x_range_array[1], num=5).tolist())
        ax.set_yticks(np.linspace(y_range_array[0], y_range_array[1], num=5).tolist())
        ax.tick_params(axis='both', colors='black', direction='in', width=2)

        # set the color of the axis labels
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')

        # remove grid lines
        ax.grid(False)

        # adjust subplots spacing
        # if subplots are added, can include, for e.g., 'wspace=0.4, hspace=0.4'
        # to control padding between subplots
        plt.subplots_adjust(bottom=0.3, top=0.8, left=0.25, right=0.8)

        # add global title
        if super_title is not None:
            fig.suptitle(super_title, fontsize="large", color="k")


if __name__ == '__main__':

    # --- read data ---
    EXAMPLE_DATA_PATH = r'.\systolic blood pressure.csv'
    example_data_df = pd.read_csv(EXAMPLE_DATA_PATH)

    # --- variables setup ---
    m1_array = example_data_df.iloc[:, 0].to_numpy()
    m2_array = example_data_df.iloc[:, 1].to_numpy()

    # --- plot data ---
    generate_plot(m1_array,
                  m2_array,
                  [50, 250],
                  [50, 250],
                  independent_variable_label=r'SBP$_{\rm arm}$ $\mathregular{[mmHg]}$',
                  dependent_variable_label=r'SBP$_{\rm finger}$ $\mathregular{[mmHg]}$',
                  specified_colors='cornflowerblue')

    # save figure
    FILE_DESTINATION = r'.\figure'
    plt.savefig(os.path.join(FILE_DESTINATION + '.pdf').replace("\\", "/"), format="pdf")
    plt.savefig(os.path.join(FILE_DESTINATION + '.png').replace("\\", "/"), dpi=300)
    plt.close()
