# RAG Colab validation

`rag_validation.ipynb` is an optional hardware/runtime validation notebook for a fresh Google Colab session.

It validates:

1. runtime and CUDA visibility
2. dense embeddings with Sentence Transformers
3. cosine-similarity retrieval over a small corpus
4. evidence-bearing prompt assembly
5. text generation with a small causal language model
6. retrieval-hit and non-empty-generation assertions
7. experiment metadata for model/corpus/retrieval traceability

The notebook is intentionally separate from required CI. CI validates notebook JSON and runs the dependency-free `tests/integration/rag_smoke.py`; Colab validates the real embedding and generation path.
