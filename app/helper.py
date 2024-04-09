STATES_MEAN = 1
STATE_MEAN = 2
BEST5 = 3
WORST5 = 4
GLOBAL_MEAN = 5
DIFF_FROM_MEAN = 6
STATE_DIFF_FROM_MEAN = 7
MEAN_BY_CATEGORY = 8
STATE_MEAN_BY_CATEGORY = 9
GRACEFUL_SHUTDOWN = 10
JOBS = 11
NUM_JOBS = 12


def compute_location_mean(data, location, data_value_index, question_values):
    """
        Returns the mean value for the given location
    """
    sum = 0
    
    for field in question_values[location]:
        sum += float(field[data_value_index])

    return sum / question_values[location].__len__()