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
│         Application Layer           │
│    (Your Controllers, Services)     │
├─────────────────────────────────────┤
│         Framework Layer             │
│  ┌──────────┐  ┌──────────────────┐ │
│  │ tusk-web │  │   tusk-micro     │ │
│  │ (HTTP)   │  │ (Health/Metrics) │ │
│  └──────────┘  └──────────────────┘ │
│  ┌──────────┐  ┌──────────────────┐ │
│  │tusk-data │  │   tusk-cli       │ │
│  │ (Repos)  │  │ (Commands)       │ │
│  └──────────┘  └──────────────────┘ │
├─────────────────────────────────────┤
│         Runtime Layer               │
│  ┌──────────────────────────────┐   │
│  │      tusk-runtime            │   │
│  │  (Kernel, Supervisor, Pool)  │   │
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

1. **Server** receives TCP connection (`HttpServer`)
2. **Parser** converts raw data to `Request` object
3. **Kernel** dispatches to `Router`
4. **Router** matches route and resolves `Controller`
5. **Container** injects dependencies into controller
6. **Controller** returns `Response`
7. **Server** sends response back to client

### CLI Command Flow

1. **Dispatcher** parses `argv` and selects command
2. **Command** executes with injected services
3. **Generator** (for `init`) scaffolds project files
4. Exit with status code

## Component Details

- [Core (DI)](core.md) - Dependency injection container
- [Runtime (Supervisor)](runtime.md) - Process management
- [Web (HTTP)](web.md) - Server, router, request handling
- [Data (Repository)](data.md) - Database abstraction
- [Micro (Services)](micro.md) - Microservice utilities
