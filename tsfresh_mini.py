import pandas as pd
from scipy.signal import savgol_filter
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.signal.savgol_filter.html
from matplotlib import pyplot as plt
import copy


def check_constant(lst):
    return all(x == lst[0] for x in lst)


def remove_constants(dataframe, headers):
    for i in headers:
        _lst = dataframe[i].as_matrix()
        if check_constant(_lst):
            del dataframe[i]
            del headers[headers.index(i)]
    return dataframe, headers


def filter_df(dataframe):
    # Convert the dataframe into an numpy.ndarray
    # EXCLUDING the timestamp column
    headers_ = list(dataframe)
    # Remove Constants
    arr_new__, headers = remove_constants(dataframe, headers_)
    # Apply filter over the Array columns
    arr_new_ = savgol_filter(arr_new__, 11, 1, axis=0)
    dataframe_new = arr_to_df(arr_new_, headers)
    return dataframe_new, headers


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


def extract_features(dataframe):  # Requires a dataframe with no timestamp, and no headers
    features = []
    return features  # should return a list of all features with tag, timestampINDEX, value


def test_mini():
    DF = pd.read_csv('CV_50_100.csv')

    tindex = [i for i in range(len(DF))]
    features = []
    headers = list(DF)
    DF_nostamp = copy.copy(DF)
    del DF_nostamp[headers[0]]
    del (headers[0])
    """
    I might have to add a function to remove the timestamp from data,
    since it could be the case that it is parsed through from Evert.
    """

    test, headers = filter_df(DF)
    testmin = global_min(test)
    features = features + testmin
    plt.figure()
    subp_index = 320

    for i, h in enumerate(headers):
        subp = subp_index + i + 1
        plt.subplot(subp)
        plt.title(h)
        plt.plot(tindex, DF[h], label='Unfiltered')
        plt.plot(tindex, test[h], label='Filtered')

        for j in features:
            if headers[i] == j[0]:
                plt.plot(j[1], j[2], '*', label='Glob_min')

    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    test_mini()
