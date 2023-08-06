from genetic_tree.genetic_tree import GeneticTree
import pandas as pd
import numpy as np
from genetic_tree.genetic.initializer import Initialization
from genetic_tree.genetic.selector import Selection
from genetic_tree.genetic.evaluator import Metric
import json
import mnist
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import openml


def test_over_params(X_train: list, y_train: list, X_test: list, y_test: list, dataset: list,
                     iterate_over_1: str, iterate_params_1: list, json_path,
                     n_trees: int = 400,
                     n_iters: int = 500,
                     cross_prob: float = 0.6,
                     mutation_prob: float = 0.4,
                     initialization: Initialization = Initialization.Full,
                     metric: Metric = Metric.AccuracyMinusDepth,
                     selection: Selection = Selection.StochasticUniform,
                     n_elitism: int = 3,
                     n_thresholds: int = 10,
                     cross_both: bool = True,
                     mutations_additional: list = None,
                     mutation_replace: bool = False,
                     initial_depth: int = 1,
                     split_prob: float = 0.7,
                     n_leaves_factor: float = 0.0001,
                     depth_factor: float = 0.01,
                     tournament_size: int = 3,
                     leave_selected_parents: bool = False,
                     n_iters_without_improvement: int = 100,
                     use_without_improvement: bool = False,
                     random_state: int = None,
                     save_metrics: bool = True,
                     keep_last_population: bool = False,
                     remove_variables: bool = True,
                     verbose: bool = True,
                     n_jobs: int = -1):
    test_records = []
    for iter_1 in iterate_params_1:
        parms = {
            "n_trees": int(n_trees),
            "n_iters": int(n_iters),
            "cross_prob": float(cross_prob),
            "mutation_prob": float(mutation_prob),
            "initialization": initialization.name,
            "metric": metric.name,
            "selection": selection.name,
            "n_elitism": int(n_elitism),
            "n_thresholds": int(n_thresholds),
            "cross_both": cross_both,
            "mutations_additional": mutations_additional,
            "mutation_replace": mutation_replace,
            "initial_depth": int(initial_depth),
            "split_prob": float(split_prob),
            "n_leaves_factor": float(n_leaves_factor),
            "depth_factor": float(depth_factor),
            "tournament_size": int(tournament_size),
            "leave_selected_parents": leave_selected_parents,
            "n_iters_without_improvement": int(n_iters_without_improvement),
            "use_without_improvement": use_without_improvement,
            "random_state": random_state,
            "save_metrics": save_metrics,
            "keep_last_population": keep_last_population,
            "remove_variables": remove_variables,
            "verbose": verbose,
            "n_jobs": int(n_jobs)
        }
        if iterate_over_1 in ["initialization", "selection", "metric"]:
            parms[iterate_over_1] = iter_1.name
        else:
            parms[iterate_over_1] = iter_1

        kwargs = {"n_trees": int(n_trees),
                  "n_iters": int(n_iters),
                  "cross_prob": float(cross_prob),
                  "mutation_prob": float(mutation_prob),
                  "initialization": initialization,
                  "metric": metric,
                  "selection": selection,
                  "n_elitism": int(n_elitism),
                  "n_thresholds": int(n_thresholds),
                  "cross_both": cross_both,
                  "mutations_additional": mutations_additional,
                  "mutation_replace": mutation_replace,
                  "initial_depth": int(initial_depth),
                  "split_prob": float(split_prob),
                  "n_leaves_factor": float(n_leaves_factor),
                  "depth_factor": float(depth_factor),
                  "tournament_size": int(tournament_size),
                  "leave_selected_parents": leave_selected_parents,
                  "n_iters_without_improvement": int(n_iters_without_improvement),
                  "use_without_improvement": use_without_improvement,
                  "random_state": random_state,
                  "save_metrics": save_metrics,
                  "keep_last_population": keep_last_population,
                  "remove_variables": remove_variables,
                  "verbose": verbose,
                  "n_jobs": int(n_jobs),
                  iterate_over_1: iter_1}

        dataset_records = []
        for X_train_i, y_train_i, X_test_i, y_test_i, dataset_i in zip(X_train, y_train, X_test, y_test, dataset):
            print(dataset_i + ":")
            gt = GeneticTree(**kwargs)
            gt.fit(X=X_train_i, y=y_train_i)
            print(sum(gt.predict(X_test_i) == y_test_i) / len(y_test_i))

            dataset_record = {
                "dataset": dataset_i,
                "acc_best": [float(k) for k in gt.acc_best],
                "acc_mean": [float(k) for k in gt.acc_mean],
                "depth_best": [float(k) for k in gt.depth_best],
                "depth_mean": [float(k) for k in gt.depth_mean],
                "n_leaves_best": [float(k) for k in gt.n_leaves_best],
                "n_leaves_mean": [float(k) for k in gt.n_leaves_mean]
            }
            dataset_records.append(dataset_record)

        test_record = {
            "parms": parms,
            "dataset_records": dataset_records
        }
        test_records.append(test_record)

    json_out = {
        "iter_over": iterate_over_1,
        "test_records": test_records
    }
    out_file = open(json_path, "w")
    json.dump(json_out, out_file, indent=4)
    out_file.close()
    return json_out


if __name__ == "__main__":

    diabetes = pd.read_csv("https://www.openml.org/data/get_csv/37/dataset_37_diabetes.csv").sample(frac=1,
                                                                                                    random_state=123)
    print("diabetes: " + str(diabetes.shape))
    diabetes["class"] = LabelEncoder().fit_transform(diabetes["class"])
    diabetes_X_train = np.array(diabetes.iloc[diabetes.shape[0] // 7:, :diabetes.shape[1] - 1])
    diabetes_y_train = np.array(diabetes["class"])[diabetes.shape[0] // 7:]
    diabetes_X_test = np.array(diabetes.iloc[:diabetes.shape[0] // 7, :diabetes.shape[1] - 1])
    diabetes_y_test = np.array(diabetes["class"])[:diabetes.shape[0] // 7]

    print("diabetes: " + str(len(diabetes_y_train)) + ", " + str(len(diabetes_y_test)))

    ozone = pd.read_csv("https://www.openml.org/data/get_csv/1592279/phpdReP6S.csv").sample(frac=1,
                                                                                            random_state=123)
    print("ozone: " + str(ozone.shape))
    ozone_X_train = np.array(ozone.iloc[ozone.shape[0] // 7:, :ozone.shape[1] - 1])
    ozone_y_train = np.array(ozone["Class"])[ozone.shape[0] // 7:] - 1
    ozone_X_test = np.array(ozone.iloc[:ozone.shape[0] // 7, :ozone.shape[1] - 1])
    ozone_y_test = np.array(ozone["Class"])[:ozone.shape[0] // 7] - 1

    print("ozone: " + str(len(ozone_y_train)) + ", " + str(len(ozone_y_test)))

    banknote = pd.read_csv("https://www.openml.org/data/get_csv/1586223/php50jXam.csv").sample(frac=1,
                                                                                               random_state=123)
    print("banknote: " + str(banknote.shape))
    banknote_X_train = np.array(banknote.iloc[banknote.shape[0] // 7:, :banknote.shape[1] - 1])
    banknote_y_train = np.array(banknote["Class"])[banknote.shape[0] // 7:] - 1
    banknote_X_test = np.array(banknote.iloc[:banknote.shape[0] // 7, :banknote.shape[1] - 1])
    banknote_y_test = np.array(banknote["Class"])[:banknote.shape[0] // 7] - 1

    print("banknote: " + str(len(banknote_y_train)) + ", " + str(len(banknote_y_test)))

    plants = pd.read_csv("https://www.openml.org/data/get_csv/1592285/phpoOxxNn.csv").sample(frac=1,
                                                                                             random_state=123)
    print("plants: " + str(plants.shape))
    plants["Class"] = LabelEncoder().fit_transform(plants["Class"])
    # print(plants)
    plants_X_train = np.array(plants.iloc[plants.shape[0] // 7:, :plants.shape[1] - 1])
    plants_y_train = np.array(plants["Class"])[plants.shape[0] // 7:] - 1
    plants_X_test = np.array(plants.iloc[:plants.shape[0] // 7, :plants.shape[1] - 1])
    plants_y_test = np.array(plants["Class"])[:plants.shape[0] // 7] - 1

    print("plants: " + str(len(plants_y_train)) + ", " + str(len(plants_y_test)))

    madelon = pd.read_csv("https://www.openml.org/data/get_csv/1590986/phpfLuQE4.csv").sample(frac=1,
                                                                                             random_state=123)
    print("madelon: " + str(madelon.shape))
    madelon["Class"] = LabelEncoder().fit_transform(madelon["Class"])
    madelon_X_train = np.array(madelon.iloc[madelon.shape[0] // 7:, :madelon.shape[1] - 1])
    madelon_y_train = np.array(madelon["Class"])[madelon.shape[0] // 7:] - 1
    madelon_X_test = np.array(madelon.iloc[:madelon.shape[0] // 7, :madelon.shape[1] - 1])
    madelon_y_test = np.array(madelon["Class"])[:madelon.shape[0] // 7] - 1

    print("madelon: " + str(len(madelon_y_train)) + ", " + str(len(madelon_y_test)))

    abalone = pd.read_csv("https://www.openml.org/data/get_csv/3620/dataset_187_abalone.csv").sample(frac=1,
                                                                                                     random_state=123)
    print("abalone: " + str(abalone.shape))
    abalone_X = abalone.iloc[:, :abalone.shape[1] - 1]
    abalone_y = abalone["Class_number_of_rings"]
    abalone_X = OneHotEncoder().fit_transform(abalone_X).toarray()
    abalone_X_train = np.array(abalone_X[abalone_X.shape[0] // 7:, :])
    abalone_y_train = np.array(abalone_y)[abalone_y.shape[0] // 7:] - 1
    abalone_X_test = np.array(abalone_X[:abalone_X.shape[0] // 7, :])
    abalone_y_test = np.array(abalone_y)[:abalone_y.shape[0] // 7] - 1
    print(abalone_X)

    print("abalone: " + str(len(abalone_y_train)) + ", " + str(len(abalone_y_test)))

    print("mnist: (70000, 785)")
    mnist_X_train = mnist.train_images().reshape((60000, 784))
    mnist_y_train = mnist.train_labels()
    mnist_X_test = mnist.test_images().reshape((10000, 784))
    mnist_y_test = mnist.test_labels()

    print("mnist: " + str(60000) + ", " + str(10000))

    train_X_list = [diabetes_X_train, ozone_X_train, banknote_X_train, plants_X_train,
                    madelon_X_train, abalone_X_train,
                    mnist_X_train]
    train_y_list = [diabetes_y_train, ozone_y_train, banknote_y_train, plants_y_train,
                    madelon_y_train, abalone_y_train,
                    mnist_y_train]
    test_X_list = [diabetes_X_test, ozone_X_test, banknote_X_test, plants_X_test,
                   madelon_X_test, abalone_X_test,
                   mnist_X_test]
    test_y_list = [diabetes_y_test, ozone_y_test, banknote_y_test, plants_y_test,
                   madelon_y_test, abalone_y_test,
                   mnist_y_test]
    dataset_list = ["diabetes", "ozone", "banknote", "plants",
                     "madelon", "abalone", "mnist"]


    #
    # cross_prob = test_over_params([madelon_X_train], [madelon_y_train], [madelon_X_test], [madelon_y_test], ["plants"],
    #                               "cross_prob", [0.2, 0.4, 0.6, 0.8, 1],
    #                               "quality_tests/cross_prob_1.json")

    cross_prob = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                  "cross_prob", [0.2, 0.4, 0.6, 0.8, 1],
                                  "quality_tests/cross_prob_1.json")

    mut_prob = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                "mutation_prob", [0.2, 0.4, 0.6, 0.8, 1],
                                "quality_tests/mut_prob_1.json")

    n_trees = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                               "n_trees", [10, 50, 150, 400, 1000],
                               "quality_tests/n_trees_1.json")

    n_thresholds = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                    "n_thresholds", [3, 10, 30, 100, 300],
                                    "quality_tests/n_thresholds_1.json")

    metrics = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                               "metric", [Metric.Accuracy, Metric.AccuracyMinusDepth, Metric.AccuracyMinusLeavesNumber],
                               "quality_tests/metrics_1.json")

    selection = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                 "selection", [Selection.StochasticUniform, Selection.Tournament, Selection.Roulette,
                                               Selection.Rank],
                                 "quality_tests/selection_1.json")

    initialization = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                      "initialization",
                                      [Initialization.Full, Initialization.Half, Initialization.Split],
                                      "quality_tests/initialization_1.json")

    n_elitism = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                 "n_elitism", [1, 3, 5, 8, 13],
                                 "quality_tests/elitism_1.json")

    n_leaves_factor = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                       "n_leaves_factor", [0.000001, 0.00001, 0.0001, 0.001, 0.01],
                                       "quality_tests/n_leaves_factor_1.json",
                                       metric=Metric.AccuracyMinusLeavesNumber)

    depth_factor = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                    "depth_factor", [0.00001, 0.0001, 0.001, 0.01, 0.1],
                                    "quality_tests/depth_factor_1.json",
                                    metric=Metric.AccuracyMinusDepth)

    initial_depth = test_over_params(train_X_list, train_y_list, test_X_list, test_y_list, dataset_list,
                                     "initial_depth", [1, 3, 5, 8, 13],
                                     "quality_tests/initial_depth_1.json",
                                     metric=Metric.AccuracyMinusDepth)
