# Runtime Lifecycle

The Engine manages RoadRunner's lifecycle; it does not implement a separate
PHP request loop.

## Startup

1. `tusk doctor` reports project bootstrap and toolchain diagnostics.
2. `tusk start` validates `bootstrap/app.php` and project configuration.
3. The Engine generates RoadRunner configuration and private worker state
   under `.tusk/runtime/`.
4. The Engine starts RoadRunner and monitors runtime readiness and process
   health.

## Request handling

RoadRunner accepts HTTP traffic and dispatches requests to persistent PHP
workers. Each worker loads the Composer autoloader and application bootstrap;
the Framework handles each request. RoadRunner owns worker pooling, recycling,
and worker process shutdown. Application code should treat workers as
long-lived and avoid leaking request-specific state.

## Shutdown and diagnostics

The Engine supervises RoadRunner and coordinates shutdown when it receives a
termination signal. `tusk doctor` diagnoses the local project/toolchain;
Engine control and metrics endpoints, when enabled, report runtime operations.

The RoadRunner configuration is generated as part of `tusk start`.
