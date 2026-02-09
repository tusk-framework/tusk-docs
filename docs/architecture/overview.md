# Architecture Overview

Tusk is built on a modular, layered architecture that separates concerns and promotes clean code.

## Core Principles

1. **Dependency Injection First**: All components use constructor injection
2. **Attribute-Based Configuration**: Routes, services, and more via PHP 8 attributes
3. **Repository Pattern**: Clean separation between domain and data access
4. **Process Supervision**: Long-running workers with automatic restart

## Component Layers

```
┌─────────────────────────────────────┐
│          External Traffic           │
│        (HTTP/TCP, Port 8080)        │
├─────────────────────────────────────┤
│         Tusk Engine (Go)            │
│  (Master, Listener, NDJSON Proxy)   │
├─────────────────────────────────────┤
│         Framework Layer             │
│  ┌──────────┐  ┌──────────────────┐ │
│  │ tusk-web │  │   tusk-micro     │ │
│  │ (Logic)  │  │ (Resilience)     │ │
│  └──────────┘  └──────────────────┘ │
│  ┌──────────┐  ┌──────────────────┐ │
│  │tusk-data │  │   tusk-cli       │ │
│  │ (Repos)  │  │ (Command Logic)  │ │
│  └──────────┘  └──────────────────┘ │
├─────────────────────────────────────┤
│         Runtime Layer               │
│  ┌──────────────────────────────┐   │
│  │      tusk-runtime            │   │
│  │  (IPC Loop, Runner, Kernel)  │   │
│  └──────────────────────────────┘   │
├─────────────────────────────────────┤
│          Core Layer                 │
│  ┌──────────────────────────────┐   │
│  │       tusk-core              │   │
│  │  (Container, Contracts)      │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Request Lifecycle

### HTTP Request Flow

1. **Tusk Engine (Go)** receives the HTTP request.
2. **IPC Bridge** forwards the request to a PHP worker over NDJSON.
3. **Runtime Runner** (PHP) parses the NDJSON into a `Request` object.
4. **Kernel** dispatches to the `Router`.
5. **Router** matches the route and resolves the `Controller`.
6. **Container** injects dependencies into the controller.
7. **Controller** returns a `Response`.
8. **Runner** sends the response back to Go over NDJSON to be served.

### CLI Command Flow

1. **Tusk Binary (Go)** receives a command (e.g., `init` or `migrate`).
2. **Command Proxy** determines if it's a native command or framework command.
3. **PHP Worker** is spawned to execute the logic for framework-aware commands.
4. **Generator** (for `init`) scaffolds project files.
4. Exit with status code

## Component Details

- [Core (DI)](core.md) - Dependency injection container
- [Runtime (Supervisor)](runtime.md) - Process management
- [Web (HTTP)](web.md) - Server, router, request handling
- [Data (Repository)](data.md) - Database abstraction
- [Micro (Services)](micro.md) - Microservice utilities
