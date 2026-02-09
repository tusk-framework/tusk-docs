# Router API Reference

The Router component handles HTTP request routing and controller resolution.

## Class: `Tusk\Web\Router\Router`

### Basic Usage

```php
use Tusk\Web\Router\Router;
use Tusk\Core\Container\Container;

$container = new Container();
$router = new Router($container);

// Register controllers
$router->registerControllers([
    \App\Controller\UserController::class,
    \App\Controller\ProductController::class,
]);

// Dispatch request
$request = Request::fromGlobals();
$response = $router->dispatch($request);
```

---

## Route Definition

### Using Attributes

```php
use Tusk\Web\Attribute\Route;
use Tusk\Web\Http\Request;
use Tusk\Web\Http\Response;

class UserController
{
    #[Route('/users', methods: ['GET'])]
    public function list(Request $request): Response
    {
        // List all users
    }
    
    #[Route('/users/{id}', methods: ['GET'])]
    public function show(Request $request, int $id): Response
    {
        // Show user by ID
    }
    
    #[Route('/users', methods: ['POST'])]
    public function create(Request $request): Response
    {
        // Create new user
    }
    
    #[Route('/users/{id}', methods: ['PUT', 'PATCH'])]
    public function update(Request $request, int $id): Response
    {
        // Update user
    }
    
    #[Route('/users/{id}', methods: ['DELETE'])]
    public function delete(Request $request, int $id): Response
    {
        // Delete user
    }
}
```

---

## Route Parameters

### Path Parameters

```php
#[Route('/posts/{id}/comments/{commentId}')]
public function showComment(Request $request, int $id, int $commentId): Response
{
    // $id = post ID
    // $commentId = comment ID
    return new Response(200, [], "Post $id, Comment $commentId");
}
```

### Optional Parameters

```php
#[Route('/search/{query?}')]
public function search(Request $request, ?string $query = null): Response
{
    $query = $query ?? $request->getQueryParam('q', '');
    // Search logic
}
```

### Type Constraints

```php
#[Route('/users/{id:\d+}')]  // Only numeric IDs
public function show(Request $request, int $id): Response
{
    // ...
}

#[Route('/posts/{slug:[a-z0-9-]+}')]  // Alphanumeric slugs
public function showBySlug(Request $request, string $slug): Response
{
    // ...
}
```

---

## Request Methods

### Method Restrictions

```php
#[Route('/api/data', methods: ['GET', 'POST'])]
public function handleData(Request $request): Response
{
    if ($request->getMethod() === 'GET') {
        // Return data
    } else {
        // Create data
    }
}
```

### RESTful Routes

```php
class ProductController
{
    #[Route('/products', methods: ['GET'])]
    public function index(Request $request): Response { }
    
    #[Route('/products', methods: ['POST'])]
    public function store(Request $request): Response { }
    
    #[Route('/products/{id}', methods: ['GET'])]
    public function show(Request $request, int $id): Response { }
    
    #[Route('/products/{id}', methods: ['PUT'])]
    public function update(Request $request, int $id): Response { }
    
    #[Route('/products/{id}', methods: ['DELETE'])]
    public function destroy(Request $request, int $id): Response { }
}
```

---

## Middleware (Future Feature)

```php
use Tusk\Web\Attribute\Middleware;

#[Middleware(AuthMiddleware::class)]
class AdminController
{
    #[Route('/admin/users')]
    public function users(Request $request): Response
    {
        // Only accessible after AuthMiddleware
    }
}
```

---

## Route Groups (Future Feature)

```php
// Planned API for route grouping
$router->group('/api/v1', function(Router $router) {
    $router->registerControllers([
        \App\Api\V1\UserController::class,
        \App\Api\V1\ProductController::class,
    ]);
});
```

---

## Error Handling

### 404 Not Found

```php
try {
    $response = $router->dispatch($request);
} catch (\Tusk\Web\Exception\RouteNotFoundException $e) {
    $response = new Response(404, [], json_encode([
        'error' => 'Route not found',
        'path' => $request->getPath()
    ]));
}
```

### 405 Method Not Allowed

```php
try {
    $response = $router->dispatch($request);
} catch (\Tusk\Web\Exception\MethodNotAllowedException $e) {
    $response = new Response(405, [
        'Allow' => implode(', ', $e->getAllowedMethods())
    ], json_encode([
        'error' => 'Method not allowed',
        'allowed' => $e->getAllowedMethods()
    ]));
}
```

---

## Advanced Patterns

### API Versioning

```php
namespace App\Api\V1;

#[Route('/api/v1/users')]
class UserController { }

namespace App\Api\V2;

#[Route('/api/v2/users')]
class UserController { }
```

### Content Negotiation

```php
#[Route('/users/{id}', methods: ['GET'])]
public function show(Request $request, int $id): Response
{
    $user = $this->userRepo->find($id);
    
    $accept = $request->getHeader('Accept');
    
    if (str_contains($accept, 'application/json')) {
        return new Response(200, 
            ['Content-Type' => 'application/json'],
            json_encode($user)
        );
    }
    
    if (str_contains($accept, 'application/xml')) {
        return new Response(200,
            ['Content-Type' => 'application/xml'],
            $this->toXml($user)
        );
    }
    
    return new Response(406, [], 'Not Acceptable');
}
```

---

## Complete Example

```php
<?php
// public/index.php

use Tusk\Core\Container\Container;
use Tusk\Web\Router\Router;
use Tusk\Web\Http\Request;

// Bootstrap
$container = require __DIR__ . '/../bootstrap.php';

// Create router
$router = new Router($container);

// Register all controllers
$router->registerControllers([
    \App\Controller\HomeController::class,
    \App\Controller\UserController::class,
    \App\Controller\ProductController::class,
    \App\Controller\OrderController::class,
]);

// Handle request
$request = Request::fromGlobals();

try {
    $response = $router->dispatch($request);
} catch (\Tusk\Web\Exception\RouteNotFoundException $e) {
    $response = new Response(404, [], 'Not Found');
} catch (\Tusk\Web\Exception\MethodNotAllowedException $e) {
    $response = new Response(405, ['Allow' => implode(', ', $e->getAllowedMethods())]);
} catch (\Throwable $e) {
    error_log($e->getMessage());
    $response = new Response(500, [], 'Internal Server Error');
}

// Send response
$response->send();
```
