# 0002. Use ASGI as the server interface

- Status: Accepted
- Date: 2026-09-24
- Deciders: Naven maintainers

## Context

Naven needs an HTTP execution boundary but does not aim to implement TCP,
socket management, or its own production server. Its planned features include
async handlers, streaming, cancellation, deadlines, and application lifecycle
events.

The server interface must support those behaviors while allowing applications
to run on mature Python infrastructure.

## Decision

Naven applications will implement the ASGI application contract. Networking
and process management will be delegated to compatible servers such as
Uvicorn.

Naven will own behavior above the ASGI boundary, including routing, operation
execution, policies, request context, and observability. It will not depend on
features exclusive to one ASGI server for its core contract.

## Consequences

### Positive

- Naven can focus on application semantics instead of network server concerns.
- Async request handling, streaming, and lifecycle events have a standard
  integration point.
- Users can choose among compatible deployment servers and tools.

### Negative

- The framework must correctly implement and test the ASGI protocol boundary.
- Server-specific differences may still require compatibility testing and
  documentation.
- Synchronous handlers, if supported later, will need an explicit execution
  policy.

## Alternatives considered

### Implement a custom HTTP server

This would give Naven control over the entire stack, but it would greatly expand
the project scope into networking, protocol parsing, and process management.

### Use WSGI

WSGI has broad adoption but does not naturally model the async, streaming, and
lifecycle behavior central to Naven's direction.
