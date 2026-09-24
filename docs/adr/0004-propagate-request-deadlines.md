# 0004. Propagate request deadlines

- Status: Proposed
- Date: 2026-09-24
- Deciders: Naven maintainers

## Context

Independent timeout values at each application layer can allow a request to run
longer than its caller's total budget. Retries make this worse because each
attempt may reset the same timeout.

Naven needs one execution constraint that handlers, dependencies, and
resilience policies can share without accidentally extending the request's
lifetime.

## Decision

Naven will represent the request time budget as a deadline in its execution
context. Internal work and Naven-managed dependency calls will derive their
remaining timeout from that deadline instead of restarting the original
duration.

Retries and other policies must not schedule work beyond the remaining budget.
If the deadline expires, the runtime will stop or cancel managed work where the
underlying execution boundary permits it.

The format used to propagate a deadline across network boundaries is outside
this ADR and requires a separate decision.

## Consequences

### Positive

- Nested calls share one bounded end-to-end execution budget.
- Retry behavior cannot silently multiply the request timeout.
- Runtime introspection and telemetry can report the remaining budget.

### Negative

- Cancellation must be coordinated across handlers, policies, and adapters.
- Code that blocks outside runtime control may continue after expiration.
- Deadline calculations need monotonic local time and careful conversion at
  integration boundaries.

## Alternatives considered

### Configure independent timeouts per layer

This is simple locally but does not enforce the caller's end-to-end budget and
can produce unexpectedly long requests.

### Use only server-level request timeouts

This bounds the outer request but gives internal dependencies and retries no
information about the remaining execution time.
