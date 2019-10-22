import numpy as np
import networkx as nx

class ConnectedComponents():
    """
    Connected Components class
    """
    def __init__(self, G):
        self.G = G
        self.feature_names = []
        self.features = {}

    def feature_extraction(self):

        """ Calculating metrics about scale-free networks

        Parameters
        ----------
        G : graph
           A networkx graph

        Returns
        -------
        feature_list : dict
           Dictionary of features related to node connectivity.


        Notes
        -----
        Components calculations using networkx:
            `Networkx_connected_components <https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.connected_components.html#networkx.algorithms.components.connected_components>`_


        """
        


        G = self.G

        feature_list = {}

              
        if not nx.is_connected(G): 
            conn_components = list(nx.connected_components(G)) 
            feature_list['is_connected']=0
            feature_list['num_conncomp']=len(conn_components)
            feature_list['ratio_conncomp_size']=len(conn_components[0])/len(conn_components[1])
            feature_list['ratio_conncomp_size_max_min']=len(conn_components[0])/len(conn_components[-1])
        else:
            feature_list['is_connected']=1
            feature_list['num_conncomp']=np.nan   
            feature_list['ratio_conncomp_size']=np.nan
            feature_list['ratio_conncomp_size_max_min']=np.nan

        self.features = feature_list
