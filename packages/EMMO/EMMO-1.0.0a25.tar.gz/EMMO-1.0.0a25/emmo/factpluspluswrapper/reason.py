from .owlapi_interface import OwlApiInterface


class FaCTPP:
    """Class for running the FaCT++ reasoner (using OwlApiInterface) and
    postprocessing the resulting inferred ontology.

    Parameters
    ----------
    graph : owlapi.Graph instance
        The graph to be inferred.
    """
    def __init__(self, graph):
        self.graph = graph
        self._inferred = None

    @property
    def inferred(self):
        "The current inferred graph."
        if self._inferred is None:
            self._inferred = self.raw_inferred_graph()
        return self._inferred

    def raw_inferred_graph(self):
        """Returns the raw non-postprocessed inferred ontology as a rdflib
        graph."""
        return OwlApiInterface().reason(self.graph)

    def inferred_graph(self):
        """Returns the postprocessed inferred graph."""

        return self.inferred
