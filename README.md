# Naven

> A production-first HTTP framework for Python where reliability is part of the application contract.

Naven is an experimental HTTP framework for Python designed around a simple idea:

**Reliability should be part of the framework contract, not something added later through disconnected libraries and middleware.**

Instead of treating endpoints only as HTTP routes, Naven models them as **operations with explicit semantics and operational guarantees**.

```python
from naven import Naven

app = Naven()

@app.query("/users/{id}")
async def get_user(id: str):
    return {
        "id": id,
    }
```

As the framework evolves, operations will be able to declare guarantees such as:

```python
@app.command(
    "/payments",
    deadline="2s",
    idempotent=True,
    rate_limit="20/min",
)
async def create_payment(
    payment: PaymentRequest,
) -> Payment:

    return await payments.create(payment)
```

These guarantees are enforced by the Naven runtime.

---

# Why Naven?

Modern HTTP frameworks are already very good at handling:

- routing;
- request parsing;
- validation;
- dependency injection;
- middleware;
- serialization;
- OpenAPI.

But production applications usually require much more.

A typical backend also needs:

- request deadlines;
- timeout propagation;
- idempotency;
- retries;
- circuit breakers;
- rate limiting;
- structured logging;
- distributed tracing;
- metrics;
- request correlation;
- graceful shutdown;
- dependency health checks;
- resilience policies.

These concerns are commonly assembled using multiple libraries and custom infrastructure.

Naven explores a different approach:

> **What if operational guarantees were part of the endpoint definition itself?**

Instead of:

```python
@app.post("/payments")
async def create_payment(...):
    ...
```

Naven aims to make it possible to express:

```python
@app.command(
    "/payments",
    deadline="2s",
    idempotent=True,
)
async def create_payment(...):
    ...
```

The framework understands not only **where** the request goes, but also **how the operation must behave**.

---

# Core Idea

Traditional HTTP frameworks usually model:

```text
HTTP Request
    │
    ▼
Route
    │
    ▼
Handler
    │
    ▼
Response
```

Naven evolves this model into:

```text
HTTP Request
      │
      ▼
┌─────────────────┐
│ Request Context │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Operation       │
│                 │
│ Query           │
│ Command         │
│ Stream          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Policies        │
│                 │
│ Deadline        │
│ Idempotency     │
│ Rate Limiting   │
│ Resilience      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Handler         │
└────────┬────────┘
         │
         ▼
     Response
```

Observability surrounds the entire lifecycle.

---

# Design Principles

## Production-first

Production concerns should exist from the beginning of the application lifecycle.

Naven should make production-safe patterns easy to adopt without forcing every application to assemble its own infrastructure stack.

---

## Reliability as code

Operational guarantees should be visible directly in the operation definition.

```python
@app.command(
    "/orders",
    deadline="3s",
    idempotent=True,
)
async def create_order(...):
    ...
```

Instead of being hidden across:

```text
middleware/
config/
terraform/
observability/
custom libraries/
```

---

## Explicit semantics

Naven distinguishes between different operation types.

### Query

Represents a read-oriented operation.

```python
@app.query("/users/{id}")
async def get_user(id: str):
    ...
```

### Command

Represents an operation that changes state.

```python
@app.command("/payments")
async def create_payment(...):
    ...
```

### Stream

Represents a long-lived or streaming operation.

```python
@app.stream("/events")
async def events():
    ...
```

These operation types may have different runtime guarantees and default policies.

---

## Safe defaults

Applications should have sensible production behavior by default.

Developers should explicitly opt out of important guarantees instead of having to discover them individually.

---

## Observable by default

Naven should automatically generate useful telemetry for every operation.

```text
Request
   │
   ├── Logs
   │
   ├── Metrics
   │
   └── Traces
```

All telemetry should share the same execution context.

---

## Context propagation

Each request executes inside a Naven context.

```python
ctx.request_id
ctx.trace_id
ctx.operation
ctx.deadline
```

The same context can propagate across internal layers and external dependencies.

---

## Deadline-aware execution

Naven uses deadlines instead of isolated timeout values whenever possible.

Example:

```text
Request deadline: 2000 ms

Service A
████████████████████

Service B
      ██████████████

Database
             ███████
```

Each dependency receives the remaining execution budget instead of resetting the timeout at every layer.

---

## Introspection

Naven should understand enough about the application to explain how it behaves.

```bash
naven inspect POST /payments
```

Future output:

```text
POST /payments

Operation
└── Command

Deadline
└── 2s

Idempotency
└── enabled

Rate Limit
└── 20/min

Dependencies
└── payment-provider
    ├── timeout: 700ms
    ├── retries: 2
    └── circuit breaker: enabled

Observability
├── traces
├── metrics
└── structured logs
```

---

# Goals

Naven aims to explore better abstractions for building production HTTP services.

Main areas of focus:

- HTTP routing;
- typed request handling;
- semantic operations;
- request context propagation;
- request deadlines;
- cancellation;
- idempotency;
- resilience policies;
- retries;
- circuit breakers;
- rate limiting;
- dependency-aware HTTP clients;
- structured errors;
- observability;
- runtime introspection;
- production diagnostics.

---

# Non-goals

Naven does not initially aim to:

- implement TCP networking from scratch;
- implement its own HTTP server;
- replace ASGI;
- provide an ORM;
- provide frontend functionality;
- replace mature HTTP client implementations;
- compete with FastAPI on ecosystem size;
- support every possible Python web use case.

Naven will initially run as an **ASGI application**.

This allows mature servers such as Uvicorn to handle networking while Naven focuses on application semantics and runtime guarantees.

```text
Client
  │
  ▼
Uvicorn
  │
  ▼
ASGI
  │
  ▼
Naven
  │
  ├── Router
  ├── Runtime
  ├── Context
  ├── Policies
  ├── Observability
  └── Handler
```

---

# Proposed API

> The following examples represent the intended API and may not be implemented yet.

## Basic application

```python
from naven import Naven

app = Naven()
```

---

## Query

```python
@app.query(
    "/users/{id}",
    deadline="1s",
)
async def get_user(
    id: str,
) -> User:

    return await users.find(id)
```

---

## Command

```python
@app.command(
    "/payments",
    deadline="2s",
    idempotent=True,
)
async def create_payment(
    payment: PaymentRequest,
) -> Payment:

    return await payments.create(payment)
```

---

## Streaming

```python
@app.stream("/events")
async def events():
    async for event in event_bus.subscribe():
        yield event
```

---

# Request Context

Each operation executes inside a runtime context.

```python
from naven import current_context

ctx = current_context()

ctx.request_id
ctx.trace_id
ctx.operation
ctx.deadline
```

This context becomes the foundation for:

- correlation;
- tracing;
- cancellation;
- deadlines;
- observability;
- dependency calls.

---

# Deadlines

Instead of isolated timeouts, Naven aims to propagate an execution deadline.

```python
@app.query(
    "/portfolio",
    deadline="2s",
)
async def portfolio():
    ...
```

Example:

```text
GET /portfolio
deadline = 2000ms

0ms
 │
 ├── user-service
 │      300ms
 │
 ├── database
 │      450ms
 │
 └── investment-service
        remaining budget ≈ 1250ms
```

External calls should respect the remaining deadline automatically.

---

# Idempotency

Commands may declare themselves idempotent.

```python
@app.command(
    "/payments",
    idempotent=True,
)
async def create_payment(...):
    ...
```

The request:

```http
POST /payments
Idempotency-Key: 7e2ef...
```

may execute through:

```text
Request
   │
   ▼
Idempotency Key
   │
   ▼
Storage
  / \
 /   \
Hit   Miss
 │      │
 │     Lock
 │      │
 │    Handler
 │      │
 │    Persist
 │      │
 └──── Response
```

Possible storage adapters:

```text
Memory
Redis
PostgreSQL
```

---

# Resilience

External dependencies can be declared explicitly.

```python
payments = app.client(
    "payment-provider",
    base_url="https://example.com",
    timeout="700ms",
    retry=2,
    circuit_breaker=True,
)
```

Calls made using this client automatically participate in the current request context.

```python
await payments.post(
    "/payments",
    json=payload,
)
```

The runtime may automatically propagate:

```text
request_id
trace context
deadline
retry budget
metrics
logging context
```

---

# Structured Errors

Application errors should be semantic rather than HTTP-specific.

Instead of:

```python
raise HTTPException(
    status_code=404,
    detail="User not found",
)
```

Naven may expose:

```python
raise ResourceNotFound(
    resource="user",
    key=user_id,
)
```

The runtime converts the error into:

```json
{
  "type": "resource_not_found",
  "title": "User not found",
  "status": 404,
  "request_id": "req_01...",
  "error_id": "err_01..."
}
```

The same error can also feed:

```text
                   Error
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      HTTP API      Logs       Trace
```

---

# Observability

Naven aims to provide automatic instrumentation.

Example trace:

```text
POST /payments                          824ms
│
├── validation                           2ms
│
├── PostgreSQL                          31ms
│
└── payment-provider                   761ms
    │
    ├── attempt #1                    timeout
    │
    └── attempt #2                     318ms
```

Possible automatic metrics:

```text
http.requests
http.duration
http.errors

operation.duration

dependency.requests
dependency.duration
dependency.errors

retry.count

circuit_breaker.state

idempotency.hit
idempotency.miss
```

---

# Architecture

The initial architecture is expected to evolve toward:

```text
naven/
│
├── app.py
│
├── routing/
│   ├── router.py
│   ├── route.py
│   └── matcher.py
│
├── operations/
│   ├── operation.py
│   ├── query.py
│   ├── command.py
│   └── stream.py
│
├── http/
│   ├── request.py
│   ├── response.py
│   └── errors.py
│
├── runtime/
│   ├── context.py
│   ├── deadline.py
│   ├── cancellation.py
│   └── lifecycle.py
│
├── policies/
│   ├── idempotency.py
│   ├── retry.py
│   ├── rate_limit.py
│   └── circuit_breaker.py
│
├── clients/
│   └── http.py
│
├── observability/
│   ├── logging.py
│   ├── metrics.py
│   └── tracing.py
│
├── validation/
│
├── openapi/
│
├── adapters/
│   ├── memory.py
│   ├── redis.py
│   └── postgres.py
│
└── cli/
    ├── run.py
    ├── routes.py
    ├── inspect.py
    └── doctor.py
```

---

# Roadmap

Naven will be built incrementally.

Each milestone should leave the framework in a working and demonstrable state.

---

## Milestone 0 — Foundation

- [X] Define minimum supported Python version
- [X] Create package structure
- [X] Configure `pyproject.toml`
- [X] Configure linting
- [X] Configure formatting
- [X] Configure type checking
- [X] Configure `pytest`
- [ ] Configure CI
- [ ] Add license

- [ ] Add contributing guidelines
- [ ] Create initial Architecture Decision Records
formatting
### Deliverable

An installable Naven package with CI and a working test suite.

---

## Milestone 1 — ASGI Core

- [ ] Implement ASGI callable
- [ ] Handle HTTP scope
- [ ] Read HTTP request body
- [ ] Implement `Request`
- [ ] Implement `Response`
- [ ] Implement JSON responses
- [ ] Implement text responses
- [ ] Implement startup lifecycle
- [ ] Implement shutdown lifecycle
- [ ] Run Naven using Uvicorn

Target:

```python
from naven import Naven

app = Naven()

@app.route("/")
async def hello(request):
    return {
        "message": "Hello, Naven!",
    }
```

### Deliverable

Naven can receive and respond to real HTTP requests.

---

## Milestone 2 — Router

- [ ] Route registry
- [ ] HTTP method matching
- [ ] Static routes
- [ ] Path parameters
- [ ] Query parameters
- [ ] Duplicate route detection
- [ ] `404 Not Found`
- [ ] `405 Method Not Allowed`
- [ ] Decorator API
- [ ] Router tests

Target:

```python
@app.get("/users/{id}")
async def get_user(id: str):
    ...
```

### Deliverable

A usable HTTP router.

---

## Milestone 3 — Operations

The first major Naven-specific abstraction.

- [ ] Define `Operation`
- [ ] Define `Query`
- [ ] Define `Command`
- [ ] Define `Stream`
- [ ] Implement `@app.query`
- [ ] Implement `@app.command`
- [ ] Implement `@app.stream`
- [ ] Store operation metadata
- [ ] Create operation registry
- [ ] Define lifecycle semantics

Target:

```python
@app.query("/users/{id}")
async def get_user(id: str):
    ...
```

### Deliverable

Routes become semantic operations.

---

## Milestone 4 — Typed HTTP

- [ ] Inspect handler signatures
- [ ] Parse typed path parameters
- [ ] Parse typed query parameters
- [ ] Parse request bodies
- [ ] Schema validation
- [ ] Response validation
- [ ] Validation errors
- [ ] Initial OpenAPI schema generation

Target:

```python
@app.command("/users")
async def create_user(
    user: CreateUser,
) -> User:
    ...
```

### Deliverable

Typed operations with runtime validation.

---

## Milestone 5 — Request Context

- [ ] Implement `Context`
- [ ] Generate request IDs
- [ ] Implement `contextvars`
- [ ] Expose current operation
- [ ] Expose request metadata
- [ ] Add correlation IDs
- [ ] Propagate context internally

Target:

```python
ctx = current_context()

ctx.request_id
ctx.operation
```

### Deliverable

Every operation executes inside a Naven runtime context.

---

## Milestone 6 — Deadlines

First major production-first capability.

- [ ] Define `Deadline`
- [ ] Add operation deadline
- [ ] Track remaining execution budget
- [ ] Cancel expired handlers
- [ ] Expose deadline through context
- [ ] Map expiration to HTTP response
- [ ] Deadline tests
- [ ] Deadline metrics

Target:

```python
@app.query(
    "/portfolio",
    deadline="2s",
)
async def portfolio():
    ...
```

### Deliverable

Deadlines become part of operation contracts.

---

## Milestone 7 — Structured Errors

- [ ] Define `NavenError`
- [ ] Define error codes
- [ ] HTTP error mapping
- [ ] Validation errors
- [ ] `ResourceNotFound`
- [ ] `Conflict`
- [ ] `Unauthorized`
- [ ] `Forbidden`
- [ ] Deadline errors
- [ ] Error IDs
- [ ] Error/request correlation

### Deliverable

Errors become structured operational events.

---

## Milestone 8 — Observability

- [ ] Structured logging
- [ ] Automatic request logs
- [ ] Request counters
- [ ] Latency metrics
- [ ] Error metrics
- [ ] OpenTelemetry integration
- [ ] Automatic request spans
- [ ] Operation metadata in traces
- [ ] Correlate logs and traces
- [ ] OTLP exporters

### Deliverable

Naven applications are observable without manually instrumenting every handler.

---

## Milestone 9 — Dependency-aware HTTP Client

- [ ] Implement Naven HTTP client abstraction
- [ ] Propagate request context
- [ ] Propagate correlation IDs
- [ ] Propagate tracing
- [ ] Respect remaining deadline
- [ ] Dependency metrics
- [ ] Dependency tracing
- [ ] External latency tracking

Target:

```python
github = app.client(
    "github",
    base_url="https://api.github.com",
)
```

### Deliverable

Outbound HTTP calls participate in the Naven runtime.

---

## Milestone 10 — Retry Policies

- [ ] Retry policy abstraction
- [ ] Maximum attempts
- [ ] Fixed backoff
- [ ] Exponential backoff
- [ ] Jitter
- [ ] Safe retry defaults
- [ ] Deadline-aware retries
- [ ] Retry metrics
- [ ] Retry tracing

### Deliverable

Retries become framework primitives.

---

## Milestone 11 — Circuit Breaker

- [ ] State machine
- [ ] Closed state
- [ ] Open state
- [ ] Half-open state
- [ ] Failure thresholds
- [ ] Recovery timeout
- [ ] Per-dependency configuration
- [ ] Metrics
- [ ] Tracing

### Deliverable

Naven can prevent dependency failures from propagating uncontrollably.

---

## Milestone 12 — Idempotency

A flagship Naven capability.

- [ ] Define idempotency contract
- [ ] Parse `Idempotency-Key`
- [ ] Storage abstraction
- [ ] In-memory adapter
- [ ] Duplicate detection
- [ ] Response replay
- [ ] Concurrent request locking
- [ ] TTL
- [ ] Redis adapter
- [ ] PostgreSQL adapter
- [ ] Metrics
- [ ] Tracing

Target:

```python
@app.command(
    "/payments",
    idempotent=True,
)
async def payment(...):
    ...
```

### Deliverable

Reliable idempotent commands.

---

## Milestone 13 — Rate Limiting

- [ ] Rate-limit policy
- [ ] Per-operation limits
- [ ] Per-client limits
- [ ] In-memory implementation
- [ ] Redis implementation
- [ ] Rate-limit response headers
- [ ] `429 Too Many Requests`
- [ ] Metrics

### Deliverable

Rate limiting becomes part of the operation contract.

---

## Milestone 14 — CLI

Target:

```bash
naven run app:app
```

Commands:

- [ ] `naven run`
- [ ] `naven routes`
- [ ] `naven inspect`
- [ ] `naven doctor`
- [ ] development reload
- [ ] human-readable output
- [ ] JSON output

Example:

```bash
naven inspect POST /payments
```

```text
POST /payments

Operation
└── Command

Deadline
└── 2s

Idempotency
└── Redis

Dependencies
└── payment-provider
    ├── timeout: 700ms
    ├── retries: 2
    └── circuit breaker: enabled
```

### Deliverable

Naven can explain its own runtime model.

---

## Milestone 15 — Naven Doctor

```bash
naven doctor
```

- [ ] Analyze registered operations
- [ ] Detect invalid deadlines
- [ ] Detect unsafe retry configurations
- [ ] Detect missing recommended policies
- [ ] Verify external dependencies
- [ ] Verify telemetry exporters
- [ ] Verify idempotency storage
- [ ] Human-readable warnings
- [ ] Machine-readable diagnostics

Example:

```text
Naven Doctor

✓ 18 operations registered
✓ OpenTelemetry configured
✓ Redis reachable

Warnings

⚠ POST /payments

  Dependency timeout: 5s
  Operation deadline: 2s

  Dependency timeout exceeds the operation deadline.

⚠ POST /orders

  Retries are enabled but the operation
  has no idempotency strategy.
```

### Deliverable

Naven proactively identifies operational design problems.

---

## Milestone 16 — OpenAPI & Developer Experience

- [ ] Full OpenAPI generation
- [ ] Swagger UI
- [ ] ReDoc
- [ ] Operation metadata
- [ ] Structured error schemas
- [ ] Idempotency documentation
- [ ] Rate-limit documentation
- [ ] Authentication metadata

### Deliverable

Naven applications become self-documenting.

---

## Milestone 17 — Performance

- [ ] Benchmark suite
- [ ] Routing benchmarks
- [ ] Runtime context benchmarks
- [ ] Policy overhead benchmarks
- [ ] Load tests
- [ ] Memory profiling
- [ ] Hot-path optimization
- [ ] Publish benchmark methodology
- [ ] Performance regression thresholds

### Deliverable

Naven has measurable and reproducible performance characteristics.

---

## Milestone 18 — Production Hardening

- [ ] Graceful shutdown validation
- [ ] Liveness endpoint
- [ ] Readiness endpoint
- [ ] Dependency health model
- [ ] Configuration validation
- [ ] Security review
- [ ] Concurrency stress tests
- [ ] Failure injection tests
- [ ] Production documentation
- [ ] Example production application

### Deliverable

First Naven release candidate.

---

# Release Strategy

Naven will evolve through small releases.

```text
v0.1
 │
 ├── ASGI
 ├── Request / Response
 └── Router
      │
      ▼
v0.2
 │
 ├── Operations
 ├── Typed HTTP
 └── Context
      │
      ▼
v0.3
 │
 ├── Deadlines
 ├── Structured Errors
 └── Observability
      │
      ▼
v0.4
 │
 ├── HTTP Client
 ├── Retry
 └── Circuit Breaker
      │
      ▼
v0.5
 │
 ├── Idempotency
 └── Rate Limiting
      │
      ▼
v0.6
 │
 ├── CLI
 ├── Inspect
 └── Doctor
      │
      ▼
v1.0
```

---

# Current Focus

The first implementation target is intentionally small.

The following should work:

```bash
pip install -e .

uvicorn example:app
```

Then:

```bash
curl http://localhost:8000/hello
```

Response:

```json
{
  "message": "Hello, Naven!"
}
```

At this stage, Naven only needs:

```text
ASGI
  │
  ▼
Router
  │
  ▼
Handler
  │
  ▼
Response
```

No OpenTelemetry.

No idempotency.

No retries.

No circuit breaker.

No dependency injection.

The first objective is to create a solid runtime foundation before introducing the production-first capabilities.

---

# Project Status

> 🚧 Naven is currently experimental and under active development.

The public API may change significantly before the first stable release.

---

# Contributing

Naven is currently in its early architecture and implementation phase.

Contributions, discussions and design proposals will be welcome as the core runtime stabilizes.

---

# License

To be defined.