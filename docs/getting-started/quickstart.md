# Quick Start

Create a project, check its prerequisites, and start it under RoadRunner.

## Create the project

```sh
composer create-project tusk-framework/app catalog
cd catalog
```

Composer creates the application and installs its dependencies. The app entry
point is `bootstrap/app.php`; you do not need to create a root `worker.php`.

## Diagnose and start

```sh
tusk doctor
tusk start
```

`tusk doctor` reports the project and toolchain status. `tusk start` validates
the application bootstrap, generates the RoadRunner configuration, and
supervises RoadRunner. RoadRunner listens for HTTP requests and manages the PHP
workers. The default application address is `http://127.0.0.1:8080` unless
changed in `tusk.json`.

Try the sample endpoint with
[Your First App](first-app.md), or read about [CLI commands](../guides/cli-usage.md).
