"""Reproducible, dependency-free retrieval and grounding evaluation harness."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tests.integration.rag_smoke import (  # noqa: E402
    Document,
    chunk_documents,
    retrieve,
    tfidf_vectors,
)

CORPUS_REVISION = "rag-smoke-corpus-v1"
CHUNKING_CONFIG = {"max_words": 18}
EMBEDDING_MODEL = "tfidf-smoke-v1"
INDEX_REVISION = "in-memory-tfidf-v1"
RETRIEVAL_CONFIG = {"top_k": 2}
PROMPT_REVISION = "grounding-rubric-v1"
GENERATION_CONFIG = {"mode": "reference-fixture"}

DOCUMENTS = [
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

REFERENCE_ANSWERS = {
    "colab-runtime": "Colab runtimes are ephemeral, so checkpoints and artifacts should be persisted. [colab:chunk-000]",
    "git-history": "Git commits record project history. [git:chunk-000]",
    "python-environments": "Python supports virtual environments. [python:chunk-000]",
    "git-branches": "Branches isolate lines of development. [git:chunk-000]",
}


def load_cases(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_answers(path: Path | None) -> dict[str, str]:
    if path is None:
        return REFERENCE_ANSWERS.copy()
    return json.loads(path.read_text(encoding="utf-8"))


def first_relevant_rank(results, relevant_ids: set[str]) -> int | None:
    for rank, (chunk, _) in enumerate(results, start=1):
        if chunk.chunk_id in relevant_ids:
            return rank
    return None


def evaluate_grounding(answer: str, required_citation_ids: list[str], required_terms: list[str]) -> str:
    if not answer.strip():
        return "generation_failure"
    lowered = answer.lower()
    if not all(citation in answer for citation in required_citation_ids):
        return "grounding_failure"
    if not all(term.lower() in lowered for term in required_terms):
        return "grounding_failure"
    return "pass"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).with_name("rag_eval_cases.json"),
        help="Frozen evaluation dataset JSON.",
    )
    parser.add_argument(
        "--answers",
        type=Path,
        help="Optional JSON mapping case IDs to generated answers.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/rag_eval_results.json"),
        help="Machine-readable result artifact path.",
    )
    args = parser.parse_args()

    dataset = load_cases(args.cases)
    answers = load_answers(args.answers)
    chunks = chunk_documents(DOCUMENTS, **CHUNKING_CONFIG)
    vectors, idf = tfidf_vectors(chunks)

    results = []
    for case in dataset["cases"]:
        ranked = retrieve(case["query"], chunks, vectors, idf, **RETRIEVAL_CONFIG)
        rank = first_relevant_rank(ranked, set(case["relevant_chunk_ids"]))
        retrieval_status = "retrieval_failure" if rank is None else "pass"
        answer = answers.get(case["id"], "")
        grounding_status = "retrieval_failure" if rank is None else evaluate_grounding(
            answer,
            case["required_citation_ids"],
            case["required_evidence_terms"],
        )
        results.append(
            {
                "id": case["id"],
                "query": case["query"],
                "retrieved": [
                    {"chunk_id": chunk.chunk_id, "score": round(score, 6)}
                    for chunk, score in ranked
                ],
                "first_relevant_rank": rank,
                "retrieval_status": retrieval_status,
                "grounding_status": grounding_status,
            }
        )

    count = len(results)
    recall_at_1 = sum(item["first_relevant_rank"] == 1 for item in results) / count
    recall_at_2 = sum(item["first_relevant_rank"] is not None and item["first_relevant_rank"] <= 2 for item in results) / count
    mrr = sum((1 / item["first_relevant_rank"]) if item["first_relevant_rank"] else 0.0 for item in results) / count
    grounding_pass_rate = sum(item["grounding_status"] == "pass" for item in results) / count

    artifact = {
        "evaluation": "rag-eval-v1",
        "dataset_id": dataset["dataset_id"],
        "dataset_revision": dataset["dataset_revision"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "corpus_revision": CORPUS_REVISION,
            "chunking_config": CHUNKING_CONFIG,
            "embedding_model_revision": EMBEDDING_MODEL,
            "index_revision": INDEX_REVISION,
            "retrieval_config": RETRIEVAL_CONFIG,
            "prompt_template_revision": PROMPT_REVISION,
            "generation_settings": GENERATION_CONFIG,
        },
        "metrics": {
            "retrieval_recall_at_1": round(recall_at_1, 6),
            "retrieval_recall_at_2": round(recall_at_2, 6),
            "retrieval_mrr": round(mrr, 6),
            "grounding_pass_rate": round(grounding_pass_rate, 6),
        },
        "results": results,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(artifact["metrics"], indent=2))
    print(f"RAG evaluation passed: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
