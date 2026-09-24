# Architecture Decision Records

Architecture Decision Records (ADRs) capture the context, decision, and
consequences of choices that significantly shape Naven. They complement the
project roadmap: the README describes where the framework is going, while ADRs
explain why a direction was chosen.

## Statuses

- **Proposed**: under discussion and not yet part of the architecture contract.
- **Accepted**: approved and expected to guide implementation.
- **Deprecated**: retained for historical context but no longer recommended.
- **Superseded**: replaced by a newer ADR, which must be linked from the old
  record.

Because Naven is experimental, proposed decisions may change before they are
accepted. An accepted ADR is not rewritten to hide a later change; add a new
ADR and mark the old one as superseded instead.

## Records

| ADR | Status | Decision |
| --- | --- | --- |
| [0001](0001-record-architecture-decisions.md) | Accepted | Record significant architecture decisions |
| [0002](0002-use-asgi-as-the-server-interface.md) | Accepted | Use ASGI as the server interface |
| [0003](0003-model-endpoints-as-semantic-operations.md) | Proposed | Model endpoints as semantic operations |
| [0004](0004-propagate-request-deadlines.md) | Proposed | Propagate request deadlines |
| [0005](0005-unify-request-context-and-observability.md) | Proposed | Unify request context and observability |

## Adding an ADR

1. Copy [`template.md`](template.md) to the next zero-padded sequence number.
2. Use a short, action-oriented file name and set the initial status to
   `Proposed`.
3. Describe the constraints and alternatives, not only the preferred solution.
4. Open the ADR in the same pull request as the architecture change, or before
   implementation when early agreement is useful.
5. Add the record to the table above and link any ADR it supersedes.

Small implementation details and easily reversible local choices usually do
not need an ADR.
