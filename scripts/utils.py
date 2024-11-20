import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to load and summarize datasets
def load_and_summarize(file_path, name):
    data = pd.read_csv(file_path)
    print(f"\n---------- {name.upper()} DATA SUMMARY ----------")
    print(f"{name} Data Info:")
    print(data.info())
    print(f"\n{name} Data Statistics:")
    print(data.describe().round(2))
    print(f"\n{name} First Few Rows:")
    print(data.head())
    return data


# Function to visualize boxplots
def plot_boxplots(data, column, title, ax):
    sns.boxplot(x=data[column], ax=ax)
    ax.set_title(title)


# Function to resample and calculate totals
def resample_data(data, frequency, column, agg_func='sum'):
    if frequency == 'M':
        frequency = 'ME'
    return data.resample(frequency, on='tarih')[column].agg(agg_func)


# Function to plot time series
def plot_time_series(data, title, xlabel, ylabel, color):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data.values, marker='o', linestyle='-', color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


# Function to calculate and display grouped statistics
def analyze_grouped_data(data, group_by_column, target_column, stats=['sum', 'mean']):
    grouped_data = data.groupby(group_by_column)[target_column].agg(stats)
    print(f"\n---------- GROUPED DATA ({group_by_column.upper()}) ----------")
    print(grouped_data)
    return grouped_data


# Function to plot a pie chart
def plot_pie(data, labels, title):
    plt.figure(figsize=(8, 8))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(title)
    plt.show()


# Function to plot bar charts
def plot_bar(data, title, xlabel, ylabel, colors):
    plt.figure(figsize=(8, 6))
    data.plot(kind='bar', color=colors, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
