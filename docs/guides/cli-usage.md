# CLI Usage

The Tusk CLI provides commands for scaffolding and running applications.

## Commands

### `init` - Create New Project

```bash
tusk init <name> [--type=api|micro]
```

**Arguments:**
- `name` - Project name (required)

**Options:**
- `--type` - Project type: `api` (default) or `micro`

**Example:**

```bash
tusk init my-api
cd my-api
composer install
```

### `start` - Boot the Runtime

```bash
tusk start [--port=8080] [--workers=4]
```

**Options:**
- `--port` - HTTP port to listen on (overrides `tusk.json`)
- `--workers` - Number of concurrent PHP workers (overrides `tusk.json`)

**Example:**

```bash
tusk start
```

### `setup` - Verify Environment

```bash
tusk setup
```

Checks project structure, PHP availability, and configuration validity.

### Script Proxying (npm-style)

Tusk can execute custom scripts defined in your `tusk.json`:

```json
"scripts": {
    "test": "phpunit",
    "db:migrate": "tusk migrate"
}
```

Run them via:
```bash
tusk test
tusk db:migrate
```

## Development Workflow

1. **Scaffold**: `tusk init my-app`
2. **Develop**: Edit controllers, services
3. **Test**: `tusk run public/index.php`
4. **Deploy**: Use Docker Compose or native server

## Tips

- Use `--type=micro` for microservice projects (includes health checks)
- The generated `docker-compose.yml` includes MySQL by default
- Edit `composer.json` to add dependencies
