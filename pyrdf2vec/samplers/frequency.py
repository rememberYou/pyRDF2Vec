from collections import defaultdict
from typing import Any, DefaultDict

from pyrdf2vec.graphs import KnowledgeGraph
from pyrdf2vec.samplers import Sampler


class ObjFreqSampler(Sampler):
    """Defines the Object Frequency Weight sampling strategy.

    This sampling strategy is a node-centric object frequency approach. With
    this strategy, entities which have a high in degree get visisted more
    often.

    Attributes:
        inverse: True if Inverse Object Frequency Weight sampling strategy
            must be used, False otherwise. Default to False.
        split: True if Split Object Frequency Weight sampling strategy must
            be used, False otherwise. Default to False.

    """

    def __init__(self, inverse=False, split=False):
        super().__init__(inverse, split)

    def fit(self, kg: KnowledgeGraph) -> None:
        """Fits the embedding network based on provided knowledge graph.

        Args:
            kg: The knowledge graph.

        """
        super().fit(kg)
        self.counts = {}
        for vertex in kg._vertices:
            if not vertex.predicate:
                self.counts[str(vertex)] = len(kg.get_inv_neighbors(vertex))

    def get_weight(self, hop) -> int:
        """Gets the weights to the edge of the Knowledge Graph.

        Args:
            hop: The depth of the Knowledge Graph.

                A depth of eight means four hops in the graph, as each hop adds
                two elements to the sequence (i.e., the predicate and the
                object).

        Returns:
            The weights to the edge of the Knowledge Graph.

        """
        return self.counts[str(hop[1])]


class PredFreqSampler(Sampler):
    """Defines the Predicate Frequency Weight sampling strategy.

    This sampling strategy is an edge-centric approach. With this strategy,
    edges with predicates which are commonly used in the dataset are more often
    followed.

    Attributes:
        inverse: True if Inverse Predicate Frequency Weight sampling strategy
            must be used, False otherwise. Default to False.
        split: True if Split Predicate Frequency Weight sampling strategy
            must be used, False otherwise. Default to False.

    """

    def __init__(self, inverse: bool = False, split: bool = False):
        super().__init__(inverse, split)

    def fit(self, kg: KnowledgeGraph) -> None:
        """Fits the embedding network based on provided knowledge graph.

        Args:
            kg: The knowledge graph.

        """
        super().fit(kg)
        self.counts: DefaultDict[Any, Any] = defaultdict(int)
        for vertex in kg._vertices:
            if vertex.predicate:
                self.counts[str(vertex)] += 1

    def get_weight(self, hop) -> int:
        """Gets the weights to the edge of the Knowledge Graph.

        Args:
            hop: The depth of the Knowledge Graph.

                A depth of eight means four hops in the graph, as each hop adds
                two elements to the sequence (i.e., the predicate and the
                object).

        Returns:
            The weights to the edge of the Knowledge Graph.

        """
        return self.counts[str(hop[0])]


class ObjPredFreqSampler(Sampler):
    """Defines the Predicate-Object Frequency Weight sampling strategy.

    This sampling strategy is a edge-centric approach. This strategy is similar
    to the Predicate Frequency Weigh sampling strategy, but differentiates
    between the objects as well.

    Args:
        inverse: True if Inverse Predicate-Object Frequency Weight sampling
            strategy must be used, False otherwise. Default to False.
         split: True if Split Predicate-Object Frequency Weight sampling
            strategy must be used, False otherwise. Default to False.

    """

    def __init__(self, inverse: bool = False, split: bool = False):
        super().__init__(inverse, split)

    def fit(self, kg: KnowledgeGraph) -> None:
        """Fits the embedding network based on provided knowledge graph.

        Args:
            kg: The knowledge graph.

        """
        super().fit(kg)
        self.counts: DefaultDict[Any, Any] = defaultdict(int)
        for vertex in kg._vertices:
            if vertex.predicate:
                # Always one object associated with this predicate
                obj = list(kg.get_neighbors(vertex))[0]
                self.counts[(str(vertex), str(obj))] += 1

    def get_weight(self, hop) -> int:
        """Gets the weights to the edge of the Knowledge Graph.

        Args:
            hop: The depth of the Knowledge Graph.

                A depth of eight means four hops in the graph, as each hop adds
                two elements to the sequence (i.e., the predicate and the
                object).

        Returns:
            The weights to the edge of the Knowledge Graph.

        """
        return self.counts[(str(hop[0]), str(hop[1]))]
