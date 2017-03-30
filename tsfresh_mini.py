import pandas as pd
from scipy.signal import savgol_filter
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.signal.savgol_filter.html
from matplotlib import pyplot as plt
import copy


def _check_constant_(lst):
    return all(x == lst[0] for x in lst)


def _remove_constants_(_dataframe, _headers):
    for i, h in enumerate(_headers):
        _lst = _dataframe[h].as_matrix()
        if _check_constant_(_lst):
            del _dataframe[h]
            del _headers[i]
    return _dataframe, _headers


def _filter_df_(_dataframe):
    __headers = list(_dataframe)
    arr_new__, _headers = _remove_constants_(_dataframe, __headers)
    arr_new_ = savgol_filter(arr_new__, 11, 1, axis=0)
    dataframe_new = _arr_to_df_(arr_new_, _headers)
    return dataframe_new, _headers


def _arr_to_df_(arr, headings):
    dfdict = {}
    for i, h in enumerate(headings):
        dfdict[h] = arr[:, i]
    # dfdict = dict(zip(headings, arr)) found this method, but having issues slicing arr in one liner
    DF = pd.DataFrame(dfdict)
    return DF


def _global_min_(_dataframe):
    points = []
    headers = list(_dataframe)
    min_vals = _dataframe.min()
    min_index = _dataframe.idxmin(0)

    for i, h in enumerate(headers):
        points.append([h, min_index[h], min_vals[h], 'Global Minimum'])

    return points


def _global_max_(_dataframe):
    points = []
    headers = list(_dataframe)
    max_vals = _dataframe.max()
    max_index = _dataframe.idxmax(0)

    for i, h in enumerate(headers):
        points.append([h, max_index[h], max_vals[h], 'Global Maximum'])

    return points


def _local_minima_(_dataframe):
    return 1


def _local_maxima_(_dataframe):
    return 1


def _median_(_dataframe):
    points = []
    headers = list(_dataframe)
    median_vals = _dataframe.median()
    for i, h in enumerate(headers):
        points.append([h, 'line', median_vals[h], 'Median'])
    return points


def _mean_(_dataframe):
    points = []
    headers = list(_dataframe)
    mean_vals = _dataframe.median()
    for i, h in enumerate(headers):
        points.append([h, 'line', mean_vals[h], 'Median'])
    return points


def extract_features(_dataframe):
    features = []
    return features


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

    test, headers = _filter_df_(DF)
    testmin = _global_min_(test)
    testmax = _global_max_(test)
    testmedian = _median_(test)
    features = features + testmin + testmax
    plt.figure()
    subp_index = 320

    for i, h in enumerate(headers):
        subp = subp_index + i + 1
        plt.subplot(subp)
        plt.title(h)
        plt.plot(tindex, DF[h], label='Unfiltered')
        plt.plot(tindex, test[h], label='Filtered')

        for j in features:
            if h == j[0]:
                plt.plot(j[1], j[2], '*', label=j[3])
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    test_mini()
