# 0003. Model endpoints as semantic operations

- Status: Proposed
- Date: 2026-09-24
- Deciders: Naven maintainers

## Context

An HTTP method and path describe how a request reaches a handler, but not the
handler's application semantics. Reliability policies often need to know
whether work is read-oriented, changes state, or produces a long-lived stream.

Treating every endpoint as an undifferentiated route forces applications to
repeat policy configuration and makes safe defaults difficult to define.

## Decision

Naven will model an endpoint as an operation with one of three initial semantic
types:

- **Query** for read-oriented work;
- **Command** for work that changes state; and
- **Stream** for long-lived or streaming work.

Routing will remain responsible for HTTP matching. The operation model will
describe execution semantics and provide the attachment point for deadlines,
idempotency, resilience, rate limits, and telemetry. Explicit configuration on
an operation will take precedence over defaults derived from its type.

## Consequences

### Positive

- Policies and safe defaults can reflect the kind of work being performed.
- Operation semantics become visible in application code and runtime
  introspection.
- Telemetry can group behavior by operation rather than only by raw routes.

### Negative

- Authors must choose a semantic type in addition to an HTTP method.
- Some endpoints may not fit cleanly into the initial three types.
- Incorrect classification could apply unsuitable defaults, so those defaults
  must remain visible and overridable.

## Alternatives considered

### Model only HTTP routes

This is familiar and simple, but leaves higher-level semantics implicit and
weakens the framework's ability to provide policy-aware defaults.

### Infer semantics only from HTTP methods

HTTP methods provide useful signals but do not fully express application intent
or distinguish all execution behaviors, especially streaming.
