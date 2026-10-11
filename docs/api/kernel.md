# Application and Runtime Lifecycle

## Application bootstrap

Application projects use `Tusk\Foundation\Application` as their entry point.
The skeleton's `bootstrap/app.php` composes the app and returns it to the
Engine-generated RoadRunner worker:

RoadRunner owns HTTP transport and the PHP worker pool; the Engine supervises
that runtime.

```php
use Tusk\Foundation\Application;

return Application::configure(dirname(__DIR__))
    ->withRouting(web: 'routes/web.php')
    ->withProviders(['bootstrap/providers.php'])
    ->create();
```

`Application::configure()` returns an `ApplicationBuilder`. The builder
supports routing, providers, controller and job directories, and custom
validators before `create()` returns the application.

## Application lifecycle

The application exposes these main runtime operations:

- `handle(ServerRequestInterface): ResponseInterface` handles one request.
- `runWorker(): void` runs the configured RoadRunner worker adapter.
- `start(): void` starts the application worker lifecycle.
- `shutdown(): void` shuts down the runtime lifecycle.

For ordinary projects, let the Tusk Engine start and supervise RoadRunner;
application code should return the configured application from
`bootstrap/app.php` instead of starting a server there. See
[Engine integration](../guides/engine-integration.md).

## Low-level runtime kernel

`Tusk\Runtime\Kernel` coordinates Framework lifecycle hooks with a supplied
`RuntimeAdapterInterface`. It is an integration-level runtime component, not
the project's HTTP server and not a replacement for the normal application
bootstrap. Its public lifecycle methods are `start()`, `run()`, `stop()`, and
`shutdown()`.
