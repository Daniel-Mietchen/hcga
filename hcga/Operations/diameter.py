
import networkx as nx
import numpy as np

class Diameter():
    """
    Diameter class
    """
    def __init__(self, G):
        self.G = G
        self.feature_names = []
        self.features = {}

    def feature_extraction(self):
        """
        Compute diameter and radius of graph
        
        Parameters
        ----------
        G : graph
          A networkx graph

        Returns
        -------
        feature_list : dict
           dictionary containing diameter and radius of graph.
           
        Notes
        -----
        Diameter/radius calculations using networkx:
            `Networkx_diameter/radius <https://networkx.github.io/documentation/stable/reference/algorithms/distance_measures.html>`_
        """
        

        
        G = self.G
        feature_list = {}
        if not nx.is_directed(G) or (nx.is_directed(G) and nx.is_strongly_connected(G)):
            #Adding diameter and radius 
            feature_list['diameter']=nx.diameter(G)
            feature_list['radius']=nx.radius(G)
        else:
            feature_list['diameter']=np.nan
            feature_list['radius']=np.nan

        self.features = feature_list
        
        
