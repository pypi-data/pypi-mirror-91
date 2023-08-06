from typing import List

from robustnessgym.core.cachedops import SingleColumnCachedOperation

try:
    import flair  # noqa
    from flair.data import Sentence
    from flair.models import SequenceTagger
except ImportError:
    _flair_available = False
else:
    _flair_available = True


class FlairSentenceTagger(SingleColumnCachedOperation):
    """Class for running the Flair sentence tagger using a CachedOperation."""

    def __init__(self, model: str):
        if not _flair_available:
            raise ImportError(
                "Flair not available for import. Install using " "\npip install flair"
            )
        super(FlairSentenceTagger, self).__init__()

        self.tagger = SequenceTagger.load(model)

    # @classmethod
    # def encode(cls, obj: stanza.Document) -> str:
    #     # Dump the Stanza Document to a string
    #     return obj.to_serialized()
    #
    # @classmethod
    # def decode(cls, s: str):
    #     # Load the Stanza Document from the string
    #     return stanza.Document.from_serialized(s)

    def single_column_apply(self, column_batch: List, *args, **kwargs) -> List:
        # Create a prediction for each example
        return [self.tagger.predict(Sentence(sentence)) for sentence in column_batch]
