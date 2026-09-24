# 0001. Record significant architecture decisions

- Status: Accepted
- Date: 2026-09-24
- Deciders: Naven maintainers

## Context

Naven intends to make reliability, operation semantics, policies, and
observability part of one framework contract. Decisions in any of these areas
affect several layers and may be difficult to reverse after applications depend
on them.

The README communicates the vision and roadmap, but it is not intended to
preserve the context and trade-offs behind individual architecture choices.

## Decision

We will record architecture decisions with meaningful, long-term impact as
versioned Markdown files in `docs/adr`.

Each record will have a sequential number, a status, a date, context, the
decision, its consequences, and the alternatives considered. Accepted records
will remain in the repository. A later decision will supersede an earlier one
instead of rewriting its history.

## Consequences

### Positive

- Contributors can understand why the architecture has its current shape.
- Proposed decisions can be reviewed independently of a large implementation.
- Reversals retain the context needed to avoid repeating earlier discussions.

### Negative

- Maintainers must keep record statuses and the ADR index current.
- Minor choices may require judgment about whether they are significant enough
  to document.

## Alternatives considered

### Keep decisions only in issues and pull requests

Discussion remains useful in those tools, but it becomes fragmented and harder
to discover from a checkout of the source code.

### Document only the resulting architecture

This explains what exists but loses the constraints, alternatives, and reasons
behind it.
