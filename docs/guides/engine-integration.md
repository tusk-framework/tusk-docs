# Engine and Framework Integration

The Engine and Framework have separate responsibilities. The Framework
composes and handles the PHP application; the Engine validates the project,
generates RoadRunner configuration, and supervises the runtime; RoadRunner
serves HTTP and manages PHP workers.

## Request lifecycle

1. A client sends an HTTP request to RoadRunner.
2. RoadRunner dispatches the request to an available PHP worker.
3. The worker loads `bootstrap/app.php` and handles requests through the Tusk
   Framework application lifecycle.
4. RoadRunner returns the application's response to the client.

The PHP application is long-lived within each worker, so its bootstrap is not
repeated for every request. Request-specific state must not leak across
requests; use the Framework's request lifecycle and shared infrastructure for
persistent data.

## Start the managed runtime

From the project root:

```sh
tusk doctor
tusk start
```

The Engine checks the bootstrap and toolchain, generates private runtime state
under `.tusk/runtime/`, and starts RoadRunner. Do not edit or commit the
generated worker. The application entry point remains `bootstrap/app.php`;
there is no root-level `worker.php` contract.

## Responsibility boundary

| Concern | Owner |
| --- | --- |
| Project bootstrap, routes, middleware, request handling | Tusk Framework |
| Project diagnostics, runtime configuration, process supervision | Tusk Engine |
| HTTP transport, PHP workers, worker pool and recycling | RoadRunner |

The default request path is direct:

```text
client → RoadRunner → PHP worker → Tusk Framework
                    ↑
             supervised by Engine
```

RoadRunner owns the HTTP transport and PHP worker pool. The Engine is not an
HTTP proxy and does not implement a second worker pool or an application-level
request protocol.
