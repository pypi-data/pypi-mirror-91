import joblib
from .parallel_tqdm import parallel_tqdm_maybe


def map(function, iterable, num_jobs=8):
    '''
    Quite like functools.map, but works in parallel.
    '''
    if num_jobs <= 0:
        raise ValueError('Number of jobs must be positive')
    with parallel_tqdm_maybe(iterable):
        pool = joblib.Parallel(n_jobs=num_jobs)
        return pool(
            joblib.delayed(function)(item)
            for item in iterable
        )
