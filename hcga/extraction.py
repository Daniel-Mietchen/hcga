"""functions to extract features from graphs."""
import logging
import time
from collections import defaultdict
from importlib import import_module
from pathlib import Path

import numpy as np
import pandas as pd

L = logging.getLogger(__name__)


def extract(
    graphs,
    n_workers,
    mode="fast",
    normalize_features=True,
    statistics_level="basic",
    with_runtimes=False,
    with_node_features=True,
    timeout=10,
    connected=False,
):
    """main function to extract features."""
    if not with_node_features:
        graphs.remove_node_features()
        n_node_features = 0
    else:
        n_node_features = graphs.get_n_node_features()

    if connected:
        graphs.maximal_subgraphs()

    feat_classes, features_info_df = get_list_feature_classes(
        mode,
        normalize_features=normalize_features,
        statistics_level=statistics_level,
        n_node_features=n_node_features,
        timeout=timeout,
    )

    if with_runtimes:
        L.info(
            "Runtime option enable, we will only use 10 graphs and one worker to estimate \
            the computational time of each feature class.",
        )
        selected_graphs = np.random.randint(0, len(graphs), 10)
        for graph in graphs.graphs:
            if graph.id not in selected_graphs:
                graph.disabled = True

    L.info(
        "Extracting features from %s graphs (we disabled %s graphs).",
        len(graphs),
        graphs.get_num_disabled_graphs(),
    )
    all_features_df = compute_all_features(
        graphs, feat_classes, n_workers=n_workers, with_runtimes=with_runtimes,
    )

    if with_runtimes:
        _print_runtimes(all_features_df)
        return 0.0, 0.0

    _set_graph_labels(all_features_df, graphs)

    L.info("%s feature extracted.", len(all_features_df.columns))
    return all_features_df, features_info_df


def _print_runtimes(all_features_df):
    """Print sorted runtimes."""
    runtimes = defaultdict(list)
    for raw_feature in all_features_df.values():
        for feat in raw_feature[1]:
            runtimes[feat].append(raw_feature[1][feat])
    feature_names, runtimes = list(runtimes.keys()), list(runtimes.values())
    runtime_sortid = np.argsort(np.mean(runtimes, axis=1))[::-1]
    for feat_id in runtime_sortid:
        L.info(
            "Runtime of %s is %s ( std = %s ) seconds per graph.",
            feature_names[feat_id],
            np.round(np.mean(runtimes[feat_id]), 3),
            np.round(np.std(runtimes[feat_id]), 3),
        )


def _set_graph_labels(features, graphs):
    """Set graph labels to features dataframe."""
    for graph in graphs:
        features.loc[graph.id, "label"] = graph.label


def _load_feature_class(feature_name):
    """load the feature class from feature name."""
    feature_module = import_module("hcga.features." + feature_name)
    return getattr(feature_module, feature_module.featureclass_name)


def get_list_feature_classes(
    mode="fast",
    normalize_features=True,
    statistics_level="basic",
    n_node_features=0,
    timeout=10,
):
    """Generates and returns the list of feature classes to compute for a given mode."""
    feature_path = Path(__file__).parent / "features"
    non_feature_files = ["__init__", "utils"]

    list_feature_classes = []
    column_indexes = pd.MultiIndex(
        levels=[[], []], codes=[[], []], names=["feature_class", "feature_name"]
    )
    feature_info_df = pd.DataFrame(columns=column_indexes)
    for f_name in feature_path.glob("*.py"):
        feature_name = f_name.stem
        if feature_name not in non_feature_files:
            feature_class = _load_feature_class(feature_name)
            if mode in feature_class.modes or mode == "all":
                list_feature_classes.append(feature_class)
                # runs once update_feature with trivial graph to create class variables
                features_info = feature_class.setup_class(
                    normalize_features=normalize_features,
                    statistics_level=statistics_level,
                    n_node_features=n_node_features,
                    timeout=timeout,
                )
                columns = [
                    (feature_class.shortname, col) for col in features_info.columns
                ]
                feature_info_df[columns] = features_info

    return list_feature_classes, feature_info_df


def feature_extraction(graph, list_feature_classes, with_runtimes=False):
    """extract features from a single graph."""
    if with_runtimes:
        runtimes = {}

    column_indexes = pd.MultiIndex(
        levels=[[], []], codes=[[], []], names=["feature_class", "feature_name"]
    )
    features_df = pd.DataFrame(columns=column_indexes)
    for feature_class in list_feature_classes:
        if with_runtimes:
            start_time = time.time()

        feat_class_inst = feature_class(graph)
        features = pd.DataFrame(feat_class_inst.get_features(), index=[graph.id])
        columns = [(feat_class_inst.shortname, col) for col in features.columns]
        features_df[columns] = features
        del feat_class_inst

        if with_runtimes:
            runtimes[feature_class.shortname] = time.time() - start_time

    if with_runtimes:
        return graph.id, [features_df, runtimes]

    return features_df


def compute_all_features(
    graphs, list_feature_classes, n_workers=1, with_runtimes=False,
):
    """compute the feature from all graphs."""
    L.info("Computing features for %s graphs:", len(graphs))
    if with_runtimes:
        n_workers = 1

    from joblib import Parallel, delayed

    results = Parallel(n_workers, verbose=10)(
        delayed(feature_extraction)(
            graph,
            list_feature_classes=list_feature_classes,
            with_runtimes=with_runtimes,
        )
        for graph in graphs
    )
    return pd.concat(results)
