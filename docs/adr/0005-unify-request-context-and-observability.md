# 0005. Unify request context and observability

- Status: Proposed
- Date: 2026-09-24
- Deciders: Naven maintainers

## Context

Logs, metrics, traces, deadlines, cancellation, and dependency calls all need
consistent information about the operation currently executing. If each
subsystem builds its own context, identifiers and lifecycle boundaries can
diverge, making production behavior difficult to correlate and explain.

## Decision

Each operation execution will have one Naven request context. At minimum, the
context will identify the request, trace, operation, and deadline when one is
configured.

The runtime will make this context available throughout the managed execution
lifecycle. Framework-provided logging, metrics, tracing, policies, and clients
will derive correlation data from it. Telemetry will cover the whole operation
lifecycle rather than being added independently by individual handlers.

The concrete telemetry backend and the mechanism used to carry context through
Python execution are outside this ADR.

## Consequences

### Positive

- Logs, metrics, and traces can be correlated around the same execution.
- Policies and dependency clients can participate without duplicating context
  plumbing in application handlers.
- Runtime inspection can explain an operation using the same data that governs
  its execution.

### Negative

- Context creation and cleanup must be correct across concurrency, exceptions,
  cancellation, and streaming lifetimes.
- Integrations must avoid leaking request data between concurrent operations.
- Supporting multiple telemetry backends will require stable abstraction
  boundaries.

## Alternatives considered

### Let each subsystem manage its own context

This reduces coordination inside the framework but risks inconsistent
identifiers, duplicated propagation logic, and incomplete lifecycle coverage.

### Require handlers to pass context explicitly everywhere

Explicit parameters are easy to reason about, but forcing them through every
application layer would add significant plumbing and make framework-managed
instrumentation harder to adopt.
