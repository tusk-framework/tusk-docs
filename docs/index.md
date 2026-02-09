# Tusk Framework

**Domain-first PHP Application Framework**

Tusk is a modern, lightweight PHP framework designed for building high-performance web applications and microservices. Built with PHP 8.2+, it emphasizes clean architecture, developer experience, and production readiness.

## Key Features

- **Native Go Engine**: Replaces Nginx and PHP-FPM with a single, high-performance Go binary.
- **Unified CLI**: One tool (`tusk`) for server management, scaffolding, and custom scripts.
- **Persistent Runtime**: Applications stay in memory, drastically reducing latency.
- **Sidecar PHP**: Automatic management of a portable PHP runtime for zero-dependency deployment.
- **Domain-First Framework**: Clean architecture patterns (DI, Repository, Events) built for performance.

## Quick Start

```bash
# Install Tusk globally
curl -sSL https://tusk.sh/install.sh | bash

# Create a project
tusk init my-app

# Start the runtime
cd my-app
tusk start
```

Visit `http://localhost:8080` to see your app running!

## Philosophy

Tusk follows these core principles:

1. **Domain-First**: Your business logic comes first, not the framework
2. **Explicit over Magic**: Clear, readable code over hidden conventions
3. **Performance**: Native implementations, minimal overhead
4. **Developer Experience**: Fast scaffolding, clear errors, great tooling

## Components

- **tusk/core**: Dependency injection and kernel contracts
- **tusk/runtime**: Process manager and supervisor
- **tusk/web**: HTTP server, router, and request handling
- **tusk/data**: Database abstraction and repository pattern
- **tusk/micro**: Microservice utilities (health, metrics, RPC)
- **tusk/cli**: Command-line tools and scaffolding

## Community

- [GitHub](https://github.com/tusk-framework/tusk-framework)
- [Issues](https://github.com/tusk-framework/tusk-framework/issues)
- [Discussions](https://github.com/tusk-framework/tusk-framework/discussions)

## License

MIT License - see [LICENSE](https://github.com/tusk-framework/tusk-framework/blob/main/LICENSE)
