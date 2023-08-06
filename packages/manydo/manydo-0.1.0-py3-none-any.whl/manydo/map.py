import contextlib
import joblib
from tqdm.auto import tqdm


def map(function, iterable, num_jobs=8, loading_bar=True):
    '''
    Quite like functools.map, but works in parallel and comes with an optional loading bar.
    '''
    if num_jobs <= 0:
        raise ValueError('Number of jobs must be positive')
    context = tqdm_joblib(tqdm(iterable)) if loading_bar else contextlib.nullcontext()
    with context:
        pool = joblib.Parallel(n_jobs=num_jobs)
        return pool(
            joblib.delayed(function)(item)
            for item in iterable
        )


@contextlib.contextmanager
def tqdm_joblib(tqdm_object):    
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()
