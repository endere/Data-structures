"""Quick Sort Data Structure."""


def quick_sort(array):
    """."""
    if len(array) == 1:
        if not isinstance(array[0], int):
            raise TypeError('Must be an integer, please try again.')
        return array
    if len(array) == 0:
        return array
    pivot_point = array[0]
    stored_index = 0
    for i in range(len(array)):
        if pivot_point > array[i]:
            stored_index += 1
            array[stored_index], array[i] = array[i], array[stored_index]
    array[stored_index], array[0] = array[0], array[stored_index]
    return quick_sort(array[:stored_index]) + [array[stored_index]] + quick_sort(array[stored_index + 1:])


if __name__ == '__main__':
    import random
    import datetime
    from functools import reduce
    import sys
    times = []
    num_runs = 500
    string_length = 5
    for i in range(num_runs):
        data = random.sample(range(string_length), string_length)
        timeA = datetime.datetime.now()
        print(quick_sort(data))
        timeB = datetime.datetime.now()
        times.append(timeB - timeA)
    average_time = reduce(lambda x, y: x + y, times) / len(times)
    print(' ')
    print('Number of runs: ', num_runs)
    print('Length of lists to sort: ', string_length)
    print('Average time: ', str(average_time)[-8:], 'seconds')