import pandas as pd
from scipy.signal import savgol_filter
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.signal.savgol_filter.html
from matplotlib import pyplot as plt
import copy


def filter_df(dataframe):
    # Convert the dataframe into an numpy.ndarray
    # EXCLUDING the timestamp column
    headers = list(dataframe)
    arr = dataframe.as_matrix(headers)

    # Apply filter over the Array columns
    arr_new = savgol_filter(arr, 11, 1, axis=0)

    return arr_new


def arr_to_df(arr, headings):

    dfdict = {}

    for i, h in enumerate(headings):
        dfdict[h] = arr[:, i]

    DF = pd.DataFrame(dfdict)

    return DF

def global_min(dataframe):
    points = []
    headers = list(dataframe)
    min_vals = dataframe.min()
    min_index = dataframe.idxmin(0)

    for i, h in enumerate(headers):
        points.append([h, min_index[h], min_vals[h]])

    return points  # should be an array-like object with tag, minimum, timestamp


def global_max(dataframe):
    return 1  # should be an array-like object with tag, maximum, timestamp


def local_minima(dataframe):
    return 1  # should be an array-like object with tag, local minima, timestamp


def local_maxima(dataframe):
    return 1  # should be an array-like object with tag, local maxima, timestamp


def median(dataframe):
    return 1  # should be an array-like object with tag, median


def ari_mean(dataframe):
    return 1  # should be an array-like object with tag, arithmetic mean


def geo_mean(dataframe):
    return 1  # should be an array-like object with tag, geometric mean


def variance(dataframe):
    return 1  # should be an array-like object with tag, standard deviation


def std_dev(dataframe):
    return 1  # should be an array-like object with tag, variance


def test_mini():
    DF = pd.read_csv('CV_50_100.csv')

    T = [i for i in range(len(DF))]
    features = []
    headers = list(DF)
    DF_nostamp = copy.copy(DF)
    del DF_nostamp[headers[0]]
    del (headers[0])

    test = filter_df(DF)
    newDF = arr_to_df(test, headers)
    print(newDF)
    testmin = global_min(newDF)
    """
    This bit isn't completely accurate yet.
    If the values in a list doesn't change, by default no features should occur (i.e. set point values)
    Since for a constant thing all things are constant
    Also, the functions should be written to use the Filtered data, 
    NOT the original pd.DataFrame
    """
    features = features + testmin
    print(testmin)
    plt.figure()
    subp_index = 330

    for i in range(len(headers)):
        subp = subp_index + i + 1
        plt.subplot(subp)
        plt.title(headers[i])
        plt.plot(T, DF[headers[i]], label='Unfiltered')
        plt.plot(T, test[:, i], label='Filtered')

        for j in features:
            if headers[i] == j[0]:
                plt.plot(j[1], j[2], '*', label='Glob_min')

    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    test_mini()
