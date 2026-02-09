# Web (HTTP)

The `tusk-web` component provides HTTP server, routing, and request handling.

## Native HTTP Server

Pure PHP socket-based server (no Nginx/Apache required):

```php
use Tusk\Web\Server\HttpServer;

$server = new HttpServer('127.0.0.1', 8080, $kernel);
$server->start();
```

## Router

Attribute-based routing:

```php
use Tusk\Web\Attribute\Route;

class UserController
{
    #[Route('/users/{id}', methods: ['GET'])]
    public function show(int $id): Response
    {
        // ...
    }
}
```

## Request/Response

PSR-7 compatible request and response objects.

*Full documentation coming soon.*
