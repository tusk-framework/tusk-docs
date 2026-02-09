# Tusk Framework

**Domain-first PHP Application Framework**

Tusk is a modern, lightweight PHP framework designed for building high-performance web applications and microservices. Built with PHP 8.2+, it emphasizes clean architecture, developer experience, and production readiness.

## Key Features

- **Zero-Dependency CLI**: Scaffold projects instantly with `tusk.phar`
- **Native HTTP Server**: Run without Nginx/Apache using pure PHP sockets
- **Dependency Injection**: Powerful container with attribute-based configuration
- **Repository Pattern**: Clean data access with PDO abstraction
- **Microservice Ready**: Built-in health checks, metrics, and RPC interfaces
- **Process Management**: Supervisor-based runtime for long-running workers

## Quick Start

```bash
# Download the CLI
wget https://github.com/tusk-framework/tusk/releases/latest/download/tusk.phar

# Create a new project
php tusk.phar init my-app

# Start the server
cd my-app
php tusk.phar run public/index.php
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

- [GitHub](https://github.com/tusk-framework/tusk)
- [Issues](https://github.com/tusk-framework/tusk/issues)
- [Discussions](https://github.com/tusk-framework/tusk/discussions)

## License

MIT License - see [LICENSE](https://github.com/tusk-framework/tusk/blob/main/LICENSE)
