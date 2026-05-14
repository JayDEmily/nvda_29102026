from nvda_desk.vocabulary_builder import (
    build_canonical_payload as build_canonical_payload,
)
from nvda_desk.vocabulary_builder import (
    build_canonical_vocabulary as build_canonical_vocabulary,
)
from nvda_desk.vocabulary_builder import (
    build_document as build_document,
)
from nvda_desk.vocabulary_builder import (
    write_canonical_vocabulary as write_canonical_vocabulary,
)

__all__ = [
    "build_canonical_payload",
    "build_canonical_vocabulary",
    "build_document",
    "write_canonical_vocabulary",
]


def main() -> None:
    write_canonical_vocabulary()
