import math
import statistics


class Stopper:
    """
    Class responsible for checking stop condition in genetic algorithm

    Implemented conditions:
    maximum number of iterations

    In development:
    maximum number of iterations without improvement of best individual
    """

    def __init__(self, max_iter: int = 500,
                 n_iter_no_change: int = 100, early_stopping: bool = False,
                 **kwargs):
        self.max_iter: int = max_iter
        self.n_iter_no_change: int = n_iter_no_change
        self.early_stopping: bool = early_stopping

        #private variables
        self.reset_private_variables()

    def set_params(self, max_iter: int = None,
                   n_iter_no_change: int = None, early_stopping: bool = None,
                   **kwargs):
        if max_iter is not None:
            self.max_iter = max_iter
        if n_iter_no_change is not None:
            self.n_iter_no_change = n_iter_no_change
        if early_stopping is not None:
            self.early_stopping = early_stopping

    def reset_private_variables(self):
        self.current_iteration: int = 1
        self.best_result: float = -math.inf
        self.best_result_iteration: int = 1
        self.best_metric_hist: list = []

    def stop(self, metrics: list = None) -> bool:
        score = max(metrics)
        if self.current_iteration > self.max_iter:
            return True

        if self.early_stopping:
            if len(self.best_metric_hist) < self.n_iter_no_change:
                self.best_metric_hist.append(score)
            else:
                self.best_metric_hist.append(score)
                self.best_metric_hist.pop(0)
                if self.best_metric_hist[self.n_iter_no_change - 1] \
                        <= statistics.median(self.best_metric_hist[:self.n_iter_no_change - 1]):
                    return True

        self.current_iteration += 1
        return False
