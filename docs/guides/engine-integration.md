# Integration: Engine and Framework

The **Tusk Engine** and **Tusk Framework** were designed to work in perfect harmony. The Engine provides an ultra-high performance web server in Go, while the Framework builds the business logic through a robust container in PHP.

Unlike the classic ecosystem (Apache + mod_php or Nginx + PHP-FPM), Tusk works with the concept of **Long-Lived Process**.

## The "Boot-and-Die" Problem

In a traditional server like Apache, on every new HTTP request:
1. A new PHP process is created.
2. The framework is entirely loaded into memory (autoloader, configurations, dependency injection container).
3. The route is resolved and the response is generated.
4. The PHP process is destroyed.

This cycle (known as *boot-and-die*) consumes a massive amount of resources and adds latency just to "boot" the application.

## The Tusk Solution

With Tusk, your application "boots" **only once**.

The `tusk-engine` (in Go) manages one or more PHP processes in the background. When an HTTP request arrives at the server, Go converts the request data to **NDJSON** (Newline Delimited JSON) and injects it directly into the `STDIN` of the PHP process that is already running. The framework processes the request and returns the response via `STDOUT`.

This means that database connections, containers, and routes are already ready in memory!

## How It Works in Practice

When starting a project using the Tusk Framework, you will have a file named `worker.php` in the root of your project. It acts as the bridge between the Engine and the Framework.

### The `worker.php` File

A basic Tusk worker has the following structure:

```php
<?php

// Require the Composer autoloader
require 'vendor/autoload.php';

use Tusk\Core\Container\Container;
use Tusk\Runtime\Kernel;
use Tusk\Runtime\Adapters\NativeLoopAdapter;

// Initialize the Dependency Injection Container
$container = new Container();

// Initialize the Kernel stating that we will use the NativeLoopAdapter (NDJSON Communication)
$kernel = new Kernel($container, new NativeLoopAdapter());

// The start() method is blocking! It creates the infinite loop that will wait for requests from the Engine.
$kernel->start();
```

By running the `tusk start` command in the terminal, the Engine detects `tusk.json` (or `composer.json`) and automatically starts this `worker.php`.

## Running in Production (Docker)

Because it is a self-contained architecture (where `tusk-engine` replaces Apache/Nginx and PHP-FPM), putting Tusk in production with Docker is extremely simple and results in very lightweight images.

### Dockerfile Example

Here is a functional example using the Alpine PHP CLI image:

```dockerfile
# We use only the CLI version of PHP (no FPM, no Apache)
FROM php:8.2-cli-alpine

# Install the latest version of the Tusk Engine in Go
RUN curl -L https://github.com/tusk-framework/tusk-engine/releases/latest/download/tusk_Linux_x86_64.tar.gz | tar xz \
    && mv tusk /usr/local/bin/tusk \
    && chmod +x /usr/local/bin/tusk

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install the Framework's production dependencies
RUN composer install --no-dev --optimize-autoloader

# Expose the default port used by tusk-engine
EXPOSE 8080

# Start the application server
CMD ["tusk", "start", "worker.php"]
```

With this Dockerfile, you have a production-ready web server in a single container, consuming minimum RAM and delivering exceptional speed thanks to the NDJSON communication between Go and PHP.
