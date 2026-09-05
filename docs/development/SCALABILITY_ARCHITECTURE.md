# Scalability Architecture

Scalability is treated as an explicit architecture dimension rather than a framework choice.

The current repository profile records five dimensions:

- **Traffic:** low-to-medium expected repository/tooling activity.
- **Compute:** CPU-first; GPU acceleration is optional for domain-specific validation.
- **State:** stateless-preferred validation and tooling.
- **Async work:** optional and introduced only when it provides a clear benefit.
- **Observability:** CI results and deterministic validation output are the primary signals.

Growth should preserve deterministic validation, platform portability, and clear architectural boundaries. Scaling a component must not be used as a reason to bypass policy or dependency-direction contracts.
