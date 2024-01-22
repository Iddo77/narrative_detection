from sentence_transformers import SentenceTransformer
from datasketch import MinHash, MinHashLSH
import numpy as np

from narrative import Narrative


class NarrativeClusterer:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the narrative clusterer with a Sentence Transformer model.

        Args:
        model_name (str): Name of the Sentence Transformer model to use.
        """
        self.model = SentenceTransformer(model_name)

    def cluster_narratives(self, narratives: set[Narrative],
                           threshold: float = 0.8,
                           num_perm: int = 128) -> list[set[Narrative]]:
        """
        Clusters narratives based on the similarity of their descriptions.

        Args:
        narratives (set[Narrative]): A set of Narrative objects to be clustered.
        threshold (float): The similarity threshold for LSH. Defaults to 0.8.
        num_perm (int): The number of permutations for MinHash. Defaults to 128.

        Returns:
        list[set[Narrative]]: A list of sets, each set containing similar Narrative objects.
        """
        # Convert narrative descriptions to embeddings
        descriptions = [narr.description for narr in narratives]
        embeddings = self.model.encode(descriptions)

        # Create LSH object
        lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
        narrative_minhashes = {}

        # Populate LSH with MinHashes of narratives
        for i, emb in enumerate(embeddings):
            minhash = MinHash(num_perm=num_perm)
            for d in np.nonzero(emb)[0]:
                minhash.update(d.to_bytes(8, byteorder='big'))
            lsh.insert(str(i), minhash)
            narrative_minhashes[i] = minhash

        # Group similar narratives
        clusters = {}
        for i, narrative in enumerate(narratives):
            result = lsh.query(narrative_minhashes[i])
            cluster_key = frozenset(result)
            if cluster_key not in clusters:
                clusters[cluster_key] = set()
            clusters[cluster_key].add(narrative)

        return list(clusters.values())
