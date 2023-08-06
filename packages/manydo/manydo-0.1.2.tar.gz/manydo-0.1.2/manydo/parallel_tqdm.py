import contextlib
import joblib
from tqdm import tqdm
from tqdm.notebook import tqdm as tqdm_notebook


def parallel_tqdm_maybe(iterable):
    '''Check if an iterable is wrapped in tqdm - if yes, make sure it works with joblib.'''
    use_tqdm = isinstance(iterable, tqdm) or isinstance(iterable, tqdm_notebook)
    return tqdm_joblib(iterable) if use_tqdm else contextlib.nullcontext()


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
