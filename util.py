import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from SETTINGS import *
from scipy.stats import spearmanr

def get_metrics_per_lp(path, lp):
        df = pd.DataFrame()
        for metric in metrics:
                tmp_df = pd.read_csv(path + f'sys_{metric}.csv')     
                df[metric] = tmp_df[lp]
       
        df = df.drop_duplicates(subset=metrics, keep='first')
        df = df.reset_index(drop=True)
        return df
def pearson(x):
    y = list(range(1, len(x)+1))
    return np.corrcoef(x, y)[0, 1]

def spearman(x):
    y = list(range(1, len(x)+1))
    return spearmanr(x, y)[0]

def acc(x, gap=1):
    y = list(range(1, len(x)+1))
    # for each pair in x, calculate the sign of their difference 
    diff_x, diff_y = [], []
    for i in range(len(x)-1):
        # only consider the pairs with a gap 
        for j in range(i+1, min(i+gap+1, len(x))):
            diff_x.append(np.sign(x[j] - x[i])) 
            diff_y.append(np.sign(y[j] - y[i]))
    # calculate the correlation between the signs
    # it should be the number of pairs with the same sign divided by the total number of pairs
    equals = np.equal(diff_x, diff_y)
    return equals
     
def plot_heatmap(correlations, corr_name):
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.heatmap(correlations, annot=True, ax=ax, cmap='Blues')

        metric_names = [metric_dict[metric] for metric in metrics]
        ax.set_yticklabels(metric_names, rotation=0)

        ax.set_xlabel(None)
        ax.set_ylabel(None)
        ax.set_xticklabels([lp.upper() for lp in lps])
        if corr_name == 'Spearman':
            plt.text(4.5, 4.5, '*', fontsize=24, ha='center', color='red')
        plt.title(f'Correlation between each metric and time for each language pair ({corr_name})')
        
        plt.show()
def generate_tex(correlations):
    sub_correlations = {}
    for subset in subsets:
            for metric in metrics:
                    equals = np.array([])
                    for lp in subsets[subset]:
                            equals = np.concatenate((equals, correlations[(lp, metric)]))
                    sub_correlations[(subset, metric)] = np.sum(equals) / len(equals)
    
    df = pd.DataFrame()
    for subset in subsets:
            df[subset] = [sub_correlations[(subset, metric)] for metric in metrics]
    subset_names = [subsets_dict[subset] for subset in subsets]
    df.columns = subset_names
    df.index = [metric_dict[metric] for metric in metrics]
    df = df.round(3)
    # refomat the vlaues to percentage
    df = df.map(lambda x: f'{x*100:.1f}')
    df.to_latex('result/sub_correlations.tex', escape=False, float_format="%.1f", label='tab:sub_correlations')
    print(df)

def draw_all(correlations, corr_name):
    # create a dataframe to store the correlations, the index is metric, the columns are language pairs
    df = pd.DataFrame()
    for metric in metrics:
            for lp in lps:
                    equals = correlations[(lp, metric)]
                    df.loc[metric, lp] = np.sum(equals) / len(equals)
    df.index = [metric_dict[metric] for metric in metrics]
    df = df.round(3)
    
    # draw the heatmap
    plt.figure(figsize=(20, 10))
    sns.heatmap(df, annot=True, fmt='.3f', cmap='Blues', linewidths=.5)
    # rotate the yticks
    plt.yticks(rotation=0)
    
    plt.title(f'Correlation between each metric and time for each language pair ({corr_name})')

    plt.savefig(f'result/{corr_name}_heatmap.png')
    plt.show()
    # save the figure
    
def all(gap=1):
    corr_dict = {'Accuracy': acc, 'Pearson': pearson, 'Spearman': spearman}
    corr_name = 'Accuracy'
    # assign the function to calculate the correlation
    corr = corr_dict[corr_name]

    correlations = {}

    for lp in lps:
            df = get_metrics_per_lp(lp)
            
            # calculate the correlation between each metric and time
            for metric in metrics:
                    correlations[(lp, metric)] = corr(df[metric], gap=gap)

    # draw the heatmap
    generate_tex(correlations)
    return correlations, corr_name

def rolling(gap=1, sample_size=10):
    corr_dict = {'Accuracy': acc, 'Pearson': pearson, 'Spearman': spearman}
    corr_name = 'Accuracy'
    # assign the function to calculate the correlation
    corr = corr_dict[corr_name]

    correlations = {}

    for lp in lps:
            df = get_metrics_per_lp(lp)
            
            # calculate the correlation between each metric and time
            for metric in metrics:
                corr_list = []
                # calculate the correlation between each metric and time with a rolling window
                for sample in df[metric].rolling(sample_size):
                        if len(sample) != sample_size:
                                continue
                        equals = corr(sample.values, gap=gap)
                        corr_list.append(np.sum(equals) / len(equals))
                correlations[(lp, metric)] = corr_list

    return correlations, corr_name

def draw_roll_subset(correlations, corr_name):
        subset_correlations = {}
        for metric in metrics:
                for subset in subsets:
                        subset_correlations[(subset, metric)] = pd.DataFrame(
                                        [correlations[(lp, metric)] for lp in subsets[subset]]).mean(axis=0)
        
        fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(20, 20))
        for i, ax in enumerate(axes.flatten()):
                subset = list(subsets.keys())[i+1]
                for metric in metrics:
                    ax.plot(subset_correlations[(subset, metric)], label=metric, color=colors[metric]) 
                ax.set_title(f'{subset.upper()}')
                ax.set_xlabel(None)
                ax.set_ylabel(None)
                ax.tick_params(axis='x', labelrotation=45)
                ax.legend()
        fig.suptitle(corr_name + ' between each metric and time', fontsize=20)
        fig.tight_layout()
        fig.subplots_adjust(top=0.95)

        # show the figure
        plt.show()

def draw_roll_mean(correlations, corr_name):
        all_correlations = {}
        for metric in metrics:
                all_correlations[metric] = pd.DataFrame([correlations[(lp, metric)] for lp in lps]).mean(axis=0)

        fig, ax = plt.subplots(figsize=(20, 10))
        for metric in metrics:
                ax.plot(all_correlations[metric], label=metric, color=colors[metric])
        ax.set_title(corr_name + ' between each metric and time', fontsize=20)
        ax.set_xlabel('Step')
        ax.set_ylabel(corr_name)
        ax.legend()
        plt.show()

def draw_roll(correlations, corr_name):
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(20, 20))
    for i, ax in enumerate(axes.flatten()):
            lp = lps[i]
            for metric in metrics:
                    ax.plot(correlations[(lp, metric)], label=metric, color=colors[metric]) 
            ax.set_title(f'{lp.upper()}')
            ax.set_xlabel(None)
            ax.set_ylabel(None)
            ax.tick_params(axis='x', labelrotation=45)
            ax.legend()
    # set the title of the figure
    fig.suptitle(corr_name + ' between each metric and time', fontsize=20)
    fig.tight_layout()
    fig.subplots_adjust(top=0.95)

    # show the figure
    plt.show()

def get_deep_lp(deep_lp, metric):
    human_df = pd.read_csv(f'result/sys_{metric}.csv')
    human_df = human_df[['date', 'en-de', 'en-zh', 'zh-en']]

    tmp_df = human_df[['date', deep_lp]]
    tmp_df.columns = ['date', 'human']
    deep_df = pd.read_csv(f'deepl/result/{metric}/sys_{deep_lp}.csv')
    deep_df.columns = ['date', 'deepl']
    
    merged_df = pd.merge(tmp_df, deep_df, on='date')
    merged_df = merged_df.drop_duplicates(subset=['human', 'deepl'], keep='first')
    merged_df = merged_df.sort_values(by=['date']).reset_index(drop=True)
    return merged_df
        

