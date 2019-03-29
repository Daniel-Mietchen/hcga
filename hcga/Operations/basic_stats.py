# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


class BasicStats():
    """
    Basic stats class
    """
    def __init__(self, G):
        self.G = G
        self.feature_names = []
        self.features = []

    def feature_extraction(self):

        """Compute some basic stats of the network


        Parameters
        ----------
        G : graph
          A networkx graph

        Returns
        -------
        feature_list : list
           List of features related to basic stats.


        """


        self.feature_names = ['num_nodes','num_edges','degree_mean','degree_median','degree_std']

        G = self.G

        feature_list = []

        # basic normalisation parameters
        N = G.number_of_nodes()
        E = G.number_of_edges()

        # Adding basic node and edge numbers
        feature_list.append(N)
        feature_list.append(E)

        # Degree stats
        degree_vals = np.asarray(list(dict(G.degree())))

        feature_list.append(degree_vals.mean())
        feature_list.append(np.median(degree_vals))
        feature_list.append(degree_vals.std())

        self.features = feature_list



"""
def basic_stats(G):

    feature_names = ['num_nodes','num_edges','degree_mean','degree_median','degree_std']
    feature_list = []


    # basic normalisation parameters
    N = G.number_of_nodes()
    E = G.number_of_edges()

    # Adding basic node and edge numbers
    feature_list.append(N)
    feature_list.append(E)

    # Degree stats
    degree_vals = np.asarray(list(dict(G.degree())))

    feature_list.append(degree_vals.mean())
    feature_list.append(np.median(degree_vals))
    feature_list.append(degree_vals.std())

    return (feature_names,feature_list)
"""
