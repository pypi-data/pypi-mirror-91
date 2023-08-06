"""
For Tabular_ML Predictions.

This serves to simulate the data and API of the tabular_prediction_analyzer.

For now, it is the main module for the tabular ML analyzer and just
serves as an example of what is possible.

Should inherit a Base Class Analyzer in the future that users can
use with real numpy or pandas data.

"""
from tqdm import tqdm

import sklearn.datasets
import sklearn.linear_model
import sklearn.tree
import sklearn.ensemble
import sklearn.metrics
import sklearn.naive_bayes
import sklearn.neighbors

import pandas as pd
from predictions_analyzer.analyze import Analyzer

def get_classification(random_state = 42):
    """
    Creates a classification dataset.
    Wrapper for sklearn's make_classification.

    :param random_state: Specifies a random seed
    :return: A tuple of X,y values.
    """
    X, y = sklearn.datasets.make_classification(
        n_samples = 1000,
        n_classes = 5,
        n_features = 20,
        n_informative = 5,
        n_redundant = 15,
        n_clusters_per_class = 3,
        random_state = random_state
    )

    # For logging
    print(X.shape)
    print(y.shape)

    return X, y

class BaseClassificationAnalyzer:
    pass

class BaseRegressionAnalyzer:
    pass

class ClassificationAnalyzer():
    """
    FITTING
    PREDICTING
    ANALYZING should be clearly differentiated and encapsulated things.

    """



    def __init__(self,
                 random_state = 42,
                 max_depth = 7,
                 simulate_data = False):


        self.random_state = random_state
        self.max_depth = max_depth
        self.is_fit = False

        self._initialize_models()
        self._initialize_metrics()
        self._initialize_preds()

        if simulate_data:
            self.generate_data()

    def _initialize_models(self):

        # Set random state / seeds for these
        self.logistic_reg = sklearn.linear_model.LogisticRegression()
        self.ridge = sklearn.linear_model.RidgeClassifier()
        self.svc = sklearn.svm.SVC()
        self.nb = sklearn.naive_bayes.GaussianNB()
        self.knn = sklearn.neighbors.KNeighborsClassifier()
        self.dec_tree = sklearn.tree.DecisionTreeClassifier(max_depth=self.max_depth)
        self.extr_tree = sklearn.ensemble.ExtraTreesClassifier(max_depth=self.max_depth)
        self.random_forest = sklearn.ensemble.RandomForestClassifier(max_depth=self.max_depth)
        self.bagging_clf = sklearn.ensemble.BaggingClassifier(max_features=0.4,
                                                              max_samples=0.4)
        # A list of named tuples of all models to loop through.
        self.models = [
            (self.logistic_reg, "logistic_reg"),
            (self.ridge, "ridge"),
            (self.knn, "knn"),
            (self.nb, "nb"),
#            (self.svc, "SVC"),
            (self.dec_tree, "dec_tree"),
            (self.random_forest, "random_forest"),
            (self.extr_tree, "extr_tree"),
            (self.bagging_clf, "bagging_clf")
        ]

    def show_models(self):
        print(self.models)

    def remove_model(self):
        """

        :return:
        """
        pass

    def update_model(self):
        pass

    def add_model(self, model_name:str, model_object):
        """
        Adds a model
        :param model_name: classifier_name
        :param model_obj: classifier object with .fit and .predict methods
        :return:

        """

        # Is this possible?
        # self.model_name = model_object

        self.models.append((model_object, model_name))

    def add_models(self):
        """
        Plural version of add_model
        Eventually refactor into one function

        :return:

        """
        pass

    def remove_all_models(self):
        pass

    def restore_baseline_models(self):
        self._initialize_models()

    def _initialize_metrics(self):

        self.metrics_df = pd.DataFrame()
        self.accuracy = []  # List of accuracy scores?

        self.binary_metrics = [
            (sklearn.metrics.accuracy_score, "accuracy_score"),
            (sklearn.metrics.roc_auc_score, "roc_auc_score")
        ]

        self.binary_or_multiclass_metrics = [
            (sklearn.metrics.precision_score, "precision_score"),
            (sklearn.metrics.recall_score, "recall_score"),
            (sklearn.metrics.f1_score, "f1_score"),
            (sklearn.metrics.log_loss, "log_loss")

        ]

    def _initialize_preds(self):
        self.ensembled_preds_df = pd.DataFrame()

        # This will be the original_preds & ensembled_preds
        self.all_preds_df = pd.DataFrame()


    def _set_is_fit(self, is_it_fit: bool):
        """
        Sets if the estimators are fit_models or not
        :return:
        """

        self.is_fit = is_it_fit

    def _is_fit(self):
        """
        TO DO - Make This Private

        find if the models are fit_models or not.
        This can be updated if there is a better method.
        :return:
        """

        if self.is_fit == False:
            return False
        if self.is_fit == True:
            return True


    def load_unsplit_data(self, X, y):
        self.X = X
        self.y = y

    def load_split_data(self, X_train, y_train,
                        X_valid, y_valid):

        self.X_train = X_train
        self.y_train = y_train
        self.X_valid = X_valid
        self.y_valid = y_valid

    def split_val_train(self, verbose = True):
        """
        Splits data into train and validation splits.
        Useful for quick processing.

        :param X:
        :param y:
        :return:
        """
        X = self.X
        y = self.y

        length_of_X = len(X)
        split_at_id = (length_of_X * 2) // 3

        self.X_train = X.iloc[0:split_at_id, :]
        self.y_train = y.iloc[0:split_at_id]

        self.X_valid = X.iloc[split_at_id:, :]
        self.y_valid = y.iloc[split_at_id:]

        self.y_true = self.y_valid



    def generate_data(self):
        X, y = get_classification(random_state=self.random_state)
        X = pd.DataFrame(X)
        y = pd.DataFrame(y)

        # TODO: Delete this to not duplicate data.  Just deal with train/val splits.
        self.X = X
        self.y = y

        # Creates validations plits and stores in instance variables.
        # Simple validation split at 66.6% train / 33.3%
        # TODO: make any percent possible.
        self.split_val_train()


    def load_preds(self):
        pass



    def fit_models(self, verbose = True):
        """
        Fit all models on the self.X and self.y data.
        Should only be used if you don't already have
        offline predictions done already.

        :return:
        """

        for model, model_name in tqdm(self.models):
            if verbose:
                print("fitting: ", model_name)

            model.fit(self.X_train, self.y_train)

        self.is_fit = self._set_is_fit(True)

    def predict(self, verbose = True):


        # Here or in the __init__?
        self.preds_df = pd.DataFrame(self.y_true, columns = ["y_true"])

        # TODO: Check if model split_val_train has been called
        # Here

        for model, model_name in tqdm(self.models):
            if verbose:
                print("Predicting with: ", model_name)

            # TODO: Add Exception handling to predict doesn't stop.

            self.preds_df[model_name] = model.predict(self.X_valid)

            # If verbose - Print Time it took.  Add to "speed_df"

        # Drop y_true.  Just keep it in self.y_true
        self.preds_df = self.preds_df.drop("y_true", axis = 1)

        return self.preds_df

    def within_threshold(self, threshold: float):
        """
        Finds all
        :param threshold: float - Find all outputs that are within a threshold.

        :return:
        """

        # Validate that the model is fit_models already.

    def apply_ytrue(self,
                       func,
                       df: pd.DataFrame = None,
                       func_name: str = None,):
        """
        TO UPDATE: Should be private function

        Applies func(y_true, col in cols...) across dataframe df

        Helper function to use df.apply with
        self.preds_df and self.y_true

        func - the function being passed to apply
        across columns.  func should take self.y_true
        as its first argument.

        df - the df to apply the func to.

        :return: a df or series with the result.
        """

        # How to get this to work with pd.apply when there is varying
        # positional arguments?  args = () ?

        if df is None:
            df = self.preds_df

        applied_df = pd.DataFrame(columns = df.columns,
                                  index = [func_name])

        for col in df.columns:
            applied_df[col] = func(self.y_true, df[col])

        return applied_df


    def add_to_metrics_from_ytrue_and_preds_df(self,
                                               func,
                                               func_name: str = None):
        """

        Helper wrapper function to apply_ytrue
        encapsulate any future
        changes to apply_ytrue or the
        preds_df structure

        :return:
        """

        # FIX: apply_ytrue should be private function
        # Modularize this.
        ### DRY Violated

        new_metric = self.apply_ytrue(func = func,
                                      df = self.preds_df,
                                      func_name = func_name)

        assert new_metric.empty != True  # Was the new_metric created?

        # Encapsulate this in a new private function
        self.metrics_df = pd.concat([self.metrics_df, new_metric])
        assert self.metrics_df.empty != True  # Has metric been added to self.metrics_df?


        ########### Do the same for Ensembled Preds ###################
        # Modularize this
        # If ensembled predictions have been created...
        if self.ensembled_preds_df.empty != True:
            new_ensembled_metric = self.apply_ytrue(func = func,
                                                    df=self.ensembled_preds_df,
                                                    func_name=func_name)

            self.metrics_df = pd.concat([self.metrics_df, new_ensembled_metric])

            assert self.metrics_df.empty != True  # Has metric been added to self.metrics_df?



    def show_preds_report(self, save = False):
        """
        Show pandas styled dataframe with reds -> incorrect, greens -> correct.

        Sort by number incorrect. / TODO: customize show features.

        Classification Report for Each Classifier.

        :param save: Save outputs to a filepath.

        :return:
        """
        pass

    def do_binary_metrics(self):
        pass


    def get_num_wrong_right(self):
        """

        :return: a df of number right, wrong, and proportions
        """

        num_rightwrong_df = pd.DataFrame()


    def fit_accuracy_scores(self):
        """
        Redundant function now?
        Remove?

        :return:
        """

        self.add_to_metrics_from_ytrue_and_preds_df(
            func=sklearn.metrics.accuracy_score,
            func_name="accuracy_score")


    def get_classification_metrics(self):

        """
        ANALYZE: assumes fit_predicted data already
        and just needs self.preds_df.

        Get classification_metrics for each of the classifiers

        :return:
        """
        # Call helper function to find if this is a multi-class problem
        # or a binary classification problem.

        # Make this configurable
        multiclass_kwargs = {"average":"micro"}

        metric_names = ["accuracy", "recall_score", "precision_score", "f1_score"]

        self.metrics_df = pd.DataFrame(index = metric_names)

        # Need a better way to do this!!!!!!!!!
        # Nested for loop?  Apply?

    def analyze(self):
        pass

    def find_hardest_samples(self):
        """
        ANALYZE:

        These are the samples that were the hardest to
        get correct.

        For each sample, find total "correct" and "wrong"
        Sort these results by the most wrong.

        FOLLOW UP:
        Then do a cluster / correlation / dependency analysis
        in the X field on these samples to find out
        if they have something in common.

        :return:
        """

        trues_df = self.preds_df.copy()

        # Set all to the trues for easy comparison.
        for col in trues_df.columns:
            trues_df[col] = self.y_true

        correct_mask = trues_df == self.preds_df

        self.correct_mask = correct_mask

        n_correct = correct_mask.sum(axis = 1).sort_values()

        self.n_correct = n_correct

        print("\nSorted Hardest Samples: retrievable with the ._hardest_samples attribute")
        print("Key is row index of sample, Value is the number of correct from all predictors")
        print(n_correct)

        print("\nNumber of correct: retrievable with the ._n_correct attribute")
        print("Index is the number of correct predictions, value is how many samples had that number of correct")
        print(n_correct.value_counts().sort_values())

        return n_correct


    def cluster_wrong_answers(self):
        """
        Find out if wrong answers have anything in common.

        :return:
        """
        pass

    def find_most_variance(self):
        """
        This function finds the samples that had
        the most variance across them.

        Highest std / variance.

        What does this mean in terms of Classification?
        Most different guesses.


        :return:
        """
        pass

    def analyze_ensemble(self):
        pass

    def add_to_ensembled_preds_df_with_ensemble_func(self):
        """
        Generalize the below to deal with any aggregation function.

        :return:
        """

    def add_metric_to_metric_df(self,
                                func,
                                func_name):
        """
        I've been concatenating but this leaves double rows
        of the same metric.

        Solve this problem by calling this function when adding
        another metric to a DF that already has other metrics
        OR is blank.

        :return:
        """
        new_preds = func(axis=1)

        # TODO: Check for Rounding Bias
        new_preds_df = pd.DataFrame(new_preds, columns=[func_name]).round(decimals = 0).astype(int)

        # ADD: IF THERE IS ALREADY A MEAN ROW, DROP IT.
        # Code here

        # Add Here
        self.ensembled_preds_df = pd.concat([self.ensembled_preds_df, new_preds_df], axis = 1)


    def fit_mean_ensemble(self):
        self.add_metric_to_metric_df(self.preds_df.mean,
                                     "mean_ensemble")


    def fit_median_ensemble(self):
        self.add_metric_to_metric_df(self.preds_df.median,
                                     "median_ensemble")

    def fit_mode_ensemble(self):

        # This doesn't work.
        # Gives ValueError: Cannot convert non-finite values (NA or inf) to integer

        #self.add_metric_to_metric_df(self.preds_df.mode,
        #                             "mode_ensemble")
        pass

    def fit_all_stats_ensembles(self):

        self.fit_mean_ensemble()
        self.fit_median_ensemble()


    def fit_best_ensemble(self):
        """

        :return:
        """
        pass

    def fit_null_test(self):
        """
        Create random predictions in a certain range
        and see how that compares with your other
        models.

        :return:
        """
        pass

    def fit_random_seed_variance(self):
        """
        How much variance is there in just changing the random seed
        :return:
        """
        pass

    def correlated_predictions(self):
        """
        Get diverse predictors by finding uncorrelated predictions.

        :return:
        """
        pass

    def bootstrap(self):
        pass

