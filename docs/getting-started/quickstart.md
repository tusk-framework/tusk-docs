# Quick Start

This guide will walk you through creating your first Tusk application in under 5 minutes.

## Create a Project

```bash
php tusk.phar init my-api
cd my-api
```

This generates:
- `composer.json` - Dependency configuration
- `docker-compose.yml` - Local development environment
- `public/index.php` - Application entry point
- `src/Controller/HomeController.php` - Sample controller

## Install Dependencies

```bash
composer install
```

## Run the Server

### Option 1: Native Server (Development)

```bash
php ../tusk.phar run public/index.php
```

Visit `http://localhost:8080`

### Option 2: Docker (Production-like)

```bash
docker-compose up
```

Visit `http://localhost:8000`

## Your First Endpoint

The generated project includes a sample controller:

```php
<?php
namespace App\Controller;

use Tusk\Web\Attribute\Route;
use Tusk\Web\Http\Request;
use Tusk\Web\Http\Response;

class HomeController
{
    #[Route('/', methods: ['GET'])]
    public function index(Request $request): Response
    {
        return new Response(200, ['Content-Type' => 'application/json'], json_encode([
            'message' => 'Welcome to Tusk!',
            'version' => '0.7.0'
        ]));
    }
}
```

## Add a New Route

Create `src/Controller/UserController.php`:

```php
<?php
namespace App\Controller;

use Tusk\Web\Attribute\Route;
use Tusk\Web\Http\Request;
use Tusk\Web\Http\Response;

class UserController
{
    #[Route('/users', methods: ['GET'])]
    public function list(Request $request): Response
    {
        $users = [
            ['id' => 1, 'name' => 'Alice'],
            ['id' => 2, 'name' => 'Bob'],
        ];
        
        return new Response(200, ['Content-Type' => 'application/json'], 
            json_encode($users));
    }
}
```

Register it in `public/index.php`:

```php
$router->registerControllers([
    \App\Controller\HomeController::class,
    \App\Controller\UserController::class, // Add this
]);
```

Visit `http://localhost:8080/users` to see your new endpoint!

## Next Steps

- Learn about [Your First App](first-app.md) with database integration
- Explore the [Architecture](../architecture/overview.md)
- Read the [CLI Usage Guide](../guides/cli-usage.md)
