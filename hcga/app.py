""" hcga app with click module """
import click

import numpy
import warnings

numpy.seterr(all="ignore")
warnings.simplefilter("ignore")


@click.group()
def cli():
    """init app"""


@cli.command("extract_features")
@click.argument("dataset", type=str)
@click.option(
    "-n", "--n-workers", default=1, help="Number of workers for multiprocessing"
)
@click.option("-m", "--mode", default="fast", help="Mode of features to extract")
@click.option(
    "-df", "--dataset-folder", default="./datasets", help="Location of dataset"
)
@click.option("-of", "--output-folder", default="./results", help="Location of results")
@click.option("-on", "--output-name", default="features", help="name of feature file")
def extract_features(
    dataset, n_workers, mode, dataset_folder, output_folder, output_name
):
    """Extract features from dataset of graphs and save the feature matrix, info and labels"""
    from .io import load_dataset, save_features
    from .feature_extraction import extract

    graphs = load_dataset(dataset, dataset_folder)
    feature_matrix, features_info = extract(graphs, n_workers=int(n_workers), mode=mode)
    labels = [graph.label for graph in graphs]
    save_features(
        feature_matrix,
        features_info,
        labels,
        filename=output_name,
        folder=output_folder,
    )


@cli.command("feature_analysis")
@click.argument("feature_file", type=str)
def feature_analysis(feature_file):
    """Extract features from dataset of graphs"""
    from .io import load_features
    from .feature_analysis import analysis

    feature_matrix, features_info, labels = load_features(feature_file)
    analysis(feature_matrix, features_info, labels)


@cli.command("get_data")
@click.argument("dataset_name", type=str)
@click.option("-f", "--folder", default="./datasets", help="Location to save dataset")
def generate_data(dataset_name, folder):
    """Generate the benchmark or test data"""
    if dataset_name == "TESTDATA":
        print("--- Building test dataset and creating pickle ---")
        from .dataset_creation import make_test_dataset

        make_test_dataset(folder=folder)
    else:
        print("---Downloading and creating pickle for {}---".format(dataset_name))
        from .dataset_creation import make_benchmark_dataset

        make_benchmark_dataset(dataset_name=dataset_name, folder=folder)