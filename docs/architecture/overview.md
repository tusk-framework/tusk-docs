# Architecture Overview

Tusk separates application behavior from process/runtime management.

```text
HTTP client
    ↓
RoadRunner — HTTP transport and PHP worker lifecycle
    ↓
PHP worker — Tusk Framework application
                  ├─ bootstrap and dependency injection
                  ├─ routing and middleware
                  └─ application services and persistence

Tusk Engine — validates configuration and supervises RoadRunner
```

## Responsibilities

- **Tusk Framework:** application bootstrap, dependency injection, routing,
  request handling, validation, and application-level components.
- **Tusk Engine:** CLI, project diagnostics, generated runtime configuration,
  process supervision, and operational health/metrics.
- **RoadRunner:** owns HTTP transport and PHP worker processes, including
  worker pooling and recycling.
- **Composer:** package resolution, lockfile, autoloading, and PHP scripts.

The Engine manages the runtime but is not in the public request path. This
avoids implementing a second HTTP server, worker pool, or request transport.
See [Engine integration](../guides/engine-integration.md) for the lifecycle.
