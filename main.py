import os
import numpy as np
import pandas as pd


def compute_max_temp(df):
    return [0, 1, 3, 5]


if __name__ == "__main__":
    # load your dataframe from data/melbourne.18_08_2020.22_08_2020.csv

    # compute max temperature for each day
    list_max_temps = compute_max_temp(df)

    print('Max temp for each day: {}'.format(','.join([str(t) for t in list_max_temps])))
