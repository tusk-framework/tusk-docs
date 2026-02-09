# CLI Usage

The Tusk CLI provides commands for scaffolding and running applications.

## Commands

### `init` - Create New Project

```bash
php tusk.phar init <name> [--type=api|micro]
```

**Arguments:**
- `name` - Project name (required)

**Options:**
- `--type` - Project type: `api` (default) or `micro`

**Example:**

```bash
php tusk.phar init my-api
cd my-api
composer install
```

### `run` - Run Application

```bash
php tusk.phar run <file>
```

**Arguments:**
- `file` - Entry point file (e.g., `public/index.php`)

**Example:**

```bash
php tusk.phar run public/index.php
```

Server starts on `http://localhost:8080`

## Building the PHAR

To build `tusk.phar` from source:

```bash
cd tusk-framework
php -d phar.readonly=0 tusk-framework/scripts/build_cli.php
```

Output: `build/tusk.phar`

## Development Workflow

1. **Scaffold**: `tusk init my-app`
2. **Develop**: Edit controllers, services
3. **Test**: `tusk run public/index.php`
4. **Deploy**: Use Docker Compose or native server

## Tips

- Use `--type=micro` for microservice projects (includes health checks)
- The generated `docker-compose.yml` includes MySQL by default
- Edit `composer.json` to add dependencies
