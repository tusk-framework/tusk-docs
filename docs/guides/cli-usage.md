# CLI Usage

Run the `tusk` CLI from the application directory. Use `tusk --help` in the
installed Engine version for the complete command list.

## Diagnose the project

```sh
tusk doctor
tusk doctor --json
```

The diagnostic report helps identify the application bootstrap and toolchain
executables used by the project. It does not install tools or change the
machine.

## Start the application

```sh
tusk start
```

The Engine validates the application bootstrap, generates RoadRunner's
configuration, and supervises the runtime. `tusk dev` is an alias for `tusk
start`.

## Configure the project

`tusk init` initializes Engine configuration (`tusk.json`) in an existing
project; it does not scaffold a PHP application. To create a new app, use
Composer's `create-project` command with `tusk-framework/app`.

The Engine reads platform settings from `tusk.json`. Composer owns package
dependencies, the lockfile, and Composer scripts in `composer.json`.

## Toolchain commands

```sh
tusk toolchain list
tusk toolchain pin php@8.3
```

Toolchain setup is explicit. Read the Engine's
[offline documentation](https://github.com/tusk-framework/tusk-engine/blob/main/docs/user-guide/index.md)
before provisioning managed tools.

## Offline documentation

```sh
tusk docs
tusk docs runtime
```

The installed Engine includes version-matched documentation, so these pages
remain available without opening the website.
