# Tusk Framework

Tusk is a PHP application framework for building HTTP APIs and services with
an explicit application bootstrap and long-lived PHP workers.

The Tusk Engine is the Go control plane: it diagnoses project prerequisites,
generates the RoadRunner runtime configuration at startup, and supervises the
RoadRunner process. RoadRunner owns HTTP transport and the PHP worker pool. The
Framework owns application bootstrap, routing, dependency injection, and
request handling.

## Quick start

Requirements: PHP 8.2 or newer, Composer, the Tusk Engine, and a RoadRunner
binary available to the Engine. See [Installation](getting-started/installation.md)
for setup details.

```sh
composer create-project tusk-framework/app catalog
cd catalog
tusk doctor
tusk start
```

The sample app includes a small product API. Its data is in memory for
demonstration; use a database-backed repository for persistent or shared state.
See [Your First App](getting-started/first-app.md) to try the endpoint.

## Architecture

```text
Client → RoadRunner (HTTP + PHP workers) → Tusk Framework application
                    ↑
          supervised by Tusk Engine
```

The Engine manages runtime lifecycle; it is not a second HTTP server or worker
pool. Read the [architecture overview](architecture/overview.md) and
[Engine integration guide](guides/engine-integration.md) for the boundaries.

## Community

- [GitHub](https://github.com/tusk-framework/tusk-framework)
- [Issues](https://github.com/tusk-framework/tusk-framework/issues)
- [Discussions](https://github.com/tusk-framework/tusk-framework/discussions)

## License

MIT License — see the [Framework repository](https://github.com/tusk-framework/tusk-framework/blob/main/LICENSE).
