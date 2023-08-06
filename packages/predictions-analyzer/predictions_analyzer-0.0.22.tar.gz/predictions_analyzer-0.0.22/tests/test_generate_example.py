
from src.generate_example import *
from sklearn.metrics import accuracy_score

def get_ExClfObj():
    ex = ExampleClassificationAnalyzer()

    ex.fit()
    ex.predict()

    return ex

def test_apply_ytrue():
    ex = get_ExClfObj()

    accuracy = ex.apply_ytrue(func = accuracy_score,
                                 func_name = "accuracy_score",
                                 df = ex.preds_df)
    print(accuracy)
    print(accuracy.shape)

def test_add_to_metrics_from_ytrue_and_preds_df():
    ex = get_ExClfObj()
    ex.add_to_metrics_from_ytrue_and_preds_df(func = accuracy_score,
                                              func_name = "accuracy_score")

    print(ex.metrics_df)

    assert ex.metrics_df.empty != True  # Assert dataframe is not empty.


def test_fit_accuracy_scores():
    ex = get_ExClfObj()
    ex.fit_accuracy_scores()

    accuracy_score_df = ex.metrics_df.loc["accuracy_score"]

    print(accuracy_score_df)
    print(accuracy_score_df.shape)

    # Assert accuracy_score is only one row.
    # assert accuracy_score_df.shape == tuple(len(ex.models), )


def test_validate_classification_constructor():

    X, y = get_classification()

    assert 1 + 1 == 2

def test_ExampleAnalyzerConstructor():
    assert ExampleClassificationAnalyzer()

def test_fit_predict():
    ex = get_ExClfObj()

    print(ex.preds_df)
    print(ex.preds_df.shape)

def test_fit_class_metrics():
    ex = get_ExClfObj()

    ex.get_classification_metrics()

    print(ex.metrics_df)


def test_mean_ensemble():
    ex = get_ExClfObj()

    ex.fit_mean_ensemble()

    print(ex.ensembled_preds_df)

    assert ex.ensembled_preds_df.empty != True

    # Assert there is only one mean column!

def test_median_ensemble():
    ex = get_ExClfObj()

    ex.fit_median_ensemble()

    print(ex.ensembled_preds_df)

    assert ex.ensembled_preds_df.empty != True

    # Assert there is only one mean column!

def test_mode_ensemble():
    ex = get_ExClfObj()

    ex.fit_mode_ensemble()

    print(ex.ensembled_preds_df)

    assert ex.ensembled_preds_df.empty != True

    # Assert there is only one mean column!

def test_all_stat_ensembled_pred_metrics():
    ex = get_ExClfObj()

    ex.fit_all_stats_ensembles()

    print(ex.ensembled_preds_df)

    # Assert it is not an empty dataframe.
    assert ex.ensembled_preds_df.empty != True

    # Assert no NaNs are in the predictions.
    assert ex.ensembled_preds_df.isna().sum().sum() == 0

def test_ensembled_preds_metrics_exist():
    ex = get_ExClfObj()
    ex.fit_mean_ensemble()

    print(ex.ensembled_preds_df)

    ex.add_to_metrics_from_ytrue_and_preds_df(
        func = accuracy_score,
        func_name = "accuracy_score"
    )

    print(ex.metrics_df)

    assert ex.metrics_df.empty != True

    # BUG: when adding ensembles, it adds another row.
    # TO DO:
    # assert accuracy_score is in one row.

def test_find_hardest_samples():
    ex = get_ExClfObj()

    ex.find_hardest_samples()

    # Assert all values in self.trues_df?


