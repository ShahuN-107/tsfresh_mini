import pandas as pd
from scipy.signal import savgol_filter
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.signal.savgol_filter.html
from matplotlib import pyplot as plt


def filter_df(dataframe):
    # Convert the dataframe into an numpy.ndarray
    # EXCLUDING the timestamp column
    headers = list(dataframe)
    del (headers[0])

    arr = dataframe.as_matrix(headers)

    # Apply filter in a loop over the Array columns
    arr_new = savgol_filter(arr, 11, 1, axis=0)

    return arr_new


def global_min(dataframe):
    return 1  # should be an array-like object with tag, minimum, timestamp


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

    test = filter_df(DF)

    plt.figure()
    subp_index = 330
    headers = list(DF)
    del (headers[0])

    for i in range(len(test[0])):
        subp = subp_index + i + 1
        plt.subplot(subp)
        plt.title(headers[i])
        plt.plot(T, DF[headers[i]], 'b-', label='Unfiltered')
        plt.plot(T, test[:, i], 'r-', label='Filtered')

    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    test_mini()
