# RAG Skill

Use for retrieval-augmented generation systems and document-grounded LLM workflows.

## Lineage

Keep these revisions traceable:

```text
corpus/document revision
→ cleaning / extraction revision
→ chunking configuration
→ embedding model revision
→ vector/index revision
→ retrieval configuration
→ reranking configuration when used
→ generation model + prompt/template revision
```

## Evaluation

Evaluate retrieval and generation as separate stages before evaluating the end-to-end system.

```text
retrieval recall / hit rate / ranking quality
→ retrieved-context relevance
→ grounded generation quality
→ end-to-end task metric
```

Use a frozen evaluation set and explicit protocol. Do not tune retrieval or prompts on the final test set.

## Rules

- Record chunk size/overlap, filters, top-k, score thresholds, reranker, embedding model, and generation settings.
- Make corpus updates explicit; never silently mix corpus revisions in a comparison.
- Preserve retrieved-document identifiers in evaluation artifacts when privacy permits so failures are diagnosable.
- Distinguish retrieval failures from generation/grounding failures in error analysis.
- Run a small representative retrieval + generation smoke test before expensive indexing or benchmarking.
- For Colab or other ephemeral runtimes, persist the index/build metadata and experiment artifacts durably when they are required for recovery.