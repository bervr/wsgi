test_data = [{"key1": "value1"}, {"k1": "v1", "k2": "v2", "k3": "v3"}, {}, {}, {"key1": "value1"}, {"key1": "value1"},
             {"key2": "value2"}]
new_data = test_data*10000

import pandas as pd
from timeit import timeit
from memory_profiler import profile, memory_usage

# @profile
def clear_list_pandas(data):
    # вариант с pandas и удалением дубликатов
    sr = pd.Series(data)
    filtered = sr.drop_duplicates()
    return filtered.tolist()

def clear_list_pandas_unique(data):
    # вариант с pandas и фильтром уникальных
    sr = pd.Series(data)
    filtered = sr.unique()
    return filtered.tolist()

# @profile
def clear_list(data):
    # вариант с перебором листа
    exit_data = []
    while len(data) > 0:
        element = data.pop()
        if element not in exit_data:
            exit_data.append(element)
    return exit_data


if __name__ == "__main__":

    print(clear_list_pandas(new_data))
    print(clear_list(new_data))

    # print(
    #     timeit(
    #         'clear_list_pandas(test_data)',
    #         setup='from __main__ import clear_list_pandas, test_data',
    #         number=100000))
    # # 8.663440300006187 -  test_data данные из задачи. number=100000
    # # 0.8613347999926191 -  test_data*10000. number=1000
    # # 0.8679558000003453 -  test_data*1000000. number=1000

    # print(
    #     timeit(
    #         'clear_list(test_data)',
    #         setup='from __main__ import clear_list, test_data',
    #         number=100000))
    # # 0.007110500009730458  -  test_data данные из задачи. number=100000
    # # 0.000673100003041327- test_data*10000. number=1000
    # # 0.0007060999923851341 -  test_data*1000000. number=1000
