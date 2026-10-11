# Web and Routing

The Framework's web layer matches routes, resolves controllers, applies
middleware, and handles PSR-7 server requests. RoadRunner provides the HTTP
listener and dispatches requests to the PHP worker; `Tusk\Web\HttpKernel` is
an application request handler, not a socket-based HTTP server.

RoadRunner owns the HTTP listener and PHP worker pool.

## Attribute routes

The router discovers controller methods marked with `#[Route]`. A controller
can return a PSR-7 response; arrays and objects are encoded as JSON by the
HTTP kernel.

```php
use Tusk\Web\Attribute\Route;

final class StatusController
{
    #[Route('/status', methods: ['GET'])]
    public function show(): array
    {
        return ['status' => 'ok'];
    }
}
```

The standard application skeleton registers controllers from `app/Controller`
and starts them through the Framework bootstrap and RoadRunner runtime. See
[Your First App](../getting-started/first-app.md) for a runnable example.
