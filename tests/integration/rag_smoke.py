"""Deterministic, network-independent RAG integration smoke test."""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Iterable


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    text: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    text: str


def normalize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def chunk_documents(documents: Iterable[Document], max_words: int = 18) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        words = document.text.split()
        for index in range(0, len(words), max_words):
            text = " ".join(words[index : index + max_words])
            chunks.append(
                Chunk(
                    chunk_id=f"{document.doc_id}:chunk-{index // max_words:03d}",
                    doc_id=document.doc_id,
                    title=document.title,
                    text=text,
                )
            )
    return chunks


def tfidf_vectors(chunks: list[Chunk]) -> tuple[list[dict[str, float]], dict[str, float]]:
    tokenized = [normalize(chunk.text) for chunk in chunks]
    vocabulary = sorted({token for tokens in tokenized for token in tokens})
    idf: dict[str, float] = {}
    for term in vocabulary:
        document_frequency = sum(term in tokens for tokens in tokenized)
        idf[term] = math.log((1 + len(chunks)) / (1 + document_frequency)) + 1.0

    vectors: list[dict[str, float]] = []
    for tokens in tokenized:
        length = max(len(tokens), 1)
        counts = {term: tokens.count(term) for term in set(tokens)}
        vectors.append({term: (count / length) * idf[term] for term, count in counts.items()})
    return vectors, idf


def vectorize_query(query: str, idf: dict[str, float]) -> dict[str, float]:
    tokens = normalize(query)
    length = max(len(tokens), 1)
    return {term: (tokens.count(term) / length) * idf[term] for term in set(tokens) if term in idf}


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    keys = set(left) | set(right)
    numerator = sum(left.get(key, 0.0) * right.get(key, 0.0) for key in keys)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0


def retrieve(
    query: str,
    chunks: list[Chunk],
    vectors: list[dict[str, float]],
    idf: dict[str, float],
    top_k: int = 2,
) -> list[tuple[Chunk, float]]:
    query_vector = vectorize_query(query, idf)
    ranked = [(chunk, cosine(query_vector, vector)) for chunk, vector in zip(chunks, vectors)]
    return sorted(ranked, key=lambda item: (-item[1], item[0].chunk_id))[:top_k]


def assemble_prompt(question: str, retrieved: list[tuple[Chunk, float]]) -> str:
    evidence = "\n".join(f"[{chunk.chunk_id}] {chunk.text}" for chunk, _ in retrieved)
    return (
        "Answer using only the evidence below. Cite chunk IDs. "
        "If the evidence is insufficient, say so.\n\n"
        f"Question: {question}\n\nEvidence:\n{evidence}"
    )


def recall_at_k(results: list[tuple[Chunk, float]], relevant_ids: set[str]) -> float:
    retrieved_ids = {chunk.chunk_id for chunk, _ in results}
    return float(bool(retrieved_ids & relevant_ids))


def main() -> None:
    documents = [
        Document(
            "python",
            "Python",
            "Python is a programming language. Python uses indentation to delimit blocks. Python supports virtual environments.",
        ),
        Document(
            "git",
            "Git",
            "Git is a distributed version control system. Git commits record project history. Branches isolate lines of development.",
        ),
        Document(
            "colab",
            "Colab",
            "Google Colab provides hosted notebook runtimes. Colab runtimes are ephemeral, so checkpoints and artifacts should be persisted.",
        ),
    ]
    chunks = chunk_documents(documents)
    assert [chunk.chunk_id for chunk in chunks] == [
        "python:chunk-000", "git:chunk-000", "colab:chunk-000"
    ]

    vectors, idf = tfidf_vectors(chunks)
    results = retrieve("How should Colab handle ephemeral runtimes?", chunks, vectors, idf, top_k=2)
    assert recall_at_k(results, {"colab:chunk-000"}) == 1.0

    prompt = assemble_prompt("How should Colab handle ephemeral runtimes?", results)
    assert "colab:chunk-000" in prompt
    assert "persisted" in prompt
    assert "database" not in prompt.lower()

    unknown = retrieve("What orbital quasar calibration protocol does this corpus define?", chunks, vectors, idf, top_k=2)
    assert unknown[0][1] == 0.0
    assert "insufficient" in assemble_prompt(
        "What orbital quasar calibration protocol does this corpus define?", unknown
    ).lower()
    print("RAG integration smoke test passed")


if __name__ == "__main__":
    main()
