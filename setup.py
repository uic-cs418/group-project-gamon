import os

current_dir = os.getcwd()

dirs = [
         'datasets/Jan-25-Feb-8-2021-Core-Trends-Survey',
         'datasets/January-8-February-7-2019-Core-Trends-Survey-SPS',
         'datasets/January 3-10, 2018 - Core Trends Survey',
         'datasets/National Survey on Drug Use and Health 2018',
         'datasets/National Survey on Drug Use and Health 2019',
         'datasets/National Survey on Drug Use and Health 2021',
         'datasets/National Survey on Drug Use and Health 2022',
         ]

for dir in dirs:
    os.makedirs(dir)

