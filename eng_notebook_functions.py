# This file contains functions from eng.ipynb for use in final_report.ipynb
# Imports for these functions
import numpy as np
import pandas as pd
import seaborn as sns

# diffSocialPlot
# Input
# DataFrame: The NSDUH DataFrame containing the data to be plotted.
# ax: The axis object for plotting the data.
# label: A string label representing the year for the plot.
# Optional Inputs
# color: String specifying the color of the plotted line. Default is 'blue'.
# linestyle: String specifying the style of the plotted line. Default is '-'.
# Graph Type
# Line plot displaying the percentage of people whose social life is impacted by their mental health by age group across years. 
# It illustrates how mental health affects social life across different age groups over time.
def diffSocialPlot(df, ax, label, color='blue', linestyle='-'):
    genMap = {'18-25': 'Gen Z', '26-34': 'Millennials', '35-49': 'Gen X', '50-64': 'Young Boomers', '65+': 'Older Boomers'}
    df['generation'] = df['age'].map(genMap)
    df['diff_social_high'] = (df['diff_social']) >= 3
    group_counts = df.groupby('generation')['diff_social_high'].sum()
    total_counts = df.groupby('generation').size()
    percentages = (group_counts / total_counts) * 100
    plot_data = pd.DataFrame({'Age Group': percentages.index, 'Percentage': percentages.values})
    plot_data['Moving Avg'] = plot_data['Percentage'].rolling(window=3, min_periods=1).mean()
    sns.lineplot(data=plot_data, x='Age Group', y='Moving Avg', ax=ax, label=f"Social Life impacted\nby Mental Health\n{label}", color=color, linestyle=linestyle)

# snsPlot
# Input
# DataFrame: The coreTrends DataFrame containing the data to be plotted.
# label: A string label representing the year for the plot.
# ax: The axis object for plotting the data.
# Optional Inputs
# color: String specifying the color of the plotted line. Default is 'blue'.
# linestyle: String specifying the style of the plotted line. Default is '--'.
# Graph Type
# Line plot showing the percentage of people with daily social media usage by age group across years. 
# It helps visualize the trend of social media usage across different age groups over time.
def snsPlot(df, label, ax, color='blue', linestyle='--'):
    sns_columns = df.filter(like='Sns_').columns
    df['sns_use'] = df[sns_columns].min(axis=1)
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 34, 49, 64, float('inf')], labels=['Gen Z', 'Millennials', 'Gen X', 'Young Boomers', 'Older Boomers'])
    high_sns = df[df['sns_use'] <= 2.0].groupby('age_group').size().reset_index(name='high_sns_count')
    total_counts = df.groupby('age_group').size().reset_index(name='total')
    high_sns = pd.merge(high_sns, total_counts, on='age_group', how='right')
    high_sns['percentage'] = (high_sns['high_sns_count'] / high_sns['total']) * 100
    high_sns['smoothed_percentage'] = high_sns['percentage'].rolling(window=3, min_periods=1).mean()
    sns.lineplot(data=high_sns, x='age_group', y='smoothed_percentage', ax=ax, label=f"Daily Social Media\n{label}", color=color, linestyle=linestyle)
