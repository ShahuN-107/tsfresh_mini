import pandas as pd
from scipy.signal import savgol_filter
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.signal.savgol_filter.html
import copy



def _check_constant_(_lst):
    return all(x == _lst[0] for x in _lst)


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


def _arr_to_df_(_arr, _headings):
    dfdict = {}
    for i, h in enumerate(_headings):
        dfdict[h] = _arr[:, i]
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
    mean_vals = _dataframe.mean()
    for i, h in enumerate(headers):
        points.append([h, 'line', mean_vals[h], 'Mean'])
    return points


def extract_features(__dataframe):
    tindex = [i for i in range(len(__dataframe))]
    features = []
    headers = list(__dataframe)
    DF_nostamp = copy.copy(__dataframe)
    del DF_nostamp[headers[0]]
    del (headers[0])

    """
    I might have to add a function to remove the timestamp from data,
    since it could be the case that it is parsed through from Evert.
    This is quick and easy (and essentially done above).
    
    Also, this library assumes a continuous dataframe is given as input.
    """

    __dataframe_filtered, headers = _filter_df_(__dataframe)
    features += _global_max_(__dataframe_filtered)
    features += _global_min_(__dataframe_filtered)
    features += _median_(__dataframe_filtered)
    features += _mean_(__dataframe_filtered)
    return features, headers, tindex, __dataframe_filtered


def _test_mini_():
    DF = pd.read_csv('CV_50_100.csv')
    features, headers, tindex, DF_filtered = extract_features(DF)

    from matplotlib import pyplot as plt

    plt.figure()
    subp_index = 320

    for i, h in enumerate(headers):
        subp = subp_index + i + 1
        plt.subplot(subp)
        plt.title(h)
        plt.plot(tindex, DF[h], label='Unfiltered')
        plt.plot(tindex, DF_filtered[h], label='Filtered')

        for j in features:
            if h == j[0]:
                if j[1] == 'line':
                    plt.plot([tindex[0], tindex[-1]], [j[2], j[2]], '-', label=j[3])
                else:
                    plt.plot(j[1], j[2], '*', label=j[3])
    plt.legend(loc='best')
    plt.show()


def _test_time_():
    DF = pd.read_csv('CV_50_100.csv')
    features, headers, tindex, DF_filtered = extract_features(DF)


if __name__ == '__main__':
    _test_mini_()

    time_it = False
    if time_it:
        import time
        start = time.clock()
        for k in range(1000):
            _test_time_()
        end = time.clock()
        time = (end - start) / 1000
        # note that this method may be inaccurate due to background processes occurring.
        # i.e. anything else that occupies the CPU will slow this down and produce an inaccurate result
        print(time)
