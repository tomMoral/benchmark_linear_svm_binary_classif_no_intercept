import warnings


from benchopt.base import BaseSolver
from benchopt import safe_import_context


with safe_import_context() as import_ctx:
    from sklearn.exceptions import ConvergenceWarning
    from sklearn.svm import LinearSVC


class Solver(BaseSolver):
    name = 'sklearn'

    install_cmd = 'conda'
    requirements = ['scikit-learn']

    parameters = {
        'dual': [True, False],
    }
    parameter_template = "dual={dual}"

    def set_objective(self, X, y, C):
        self.X, self.y, self.C = X, y, C

        warnings.filterwarnings('ignore', category=ConvergenceWarning)

        self.clf = LinearSVC(C=self.C, penalty='l2',
                             fit_intercept=False, tol=1e-12)

    def run(self, n_iter):
        self.clf.max_iter = n_iter
        self.clf.fit(self.X, self.y)

    def get_result(self):
        return self.clf.coef_.flatten()