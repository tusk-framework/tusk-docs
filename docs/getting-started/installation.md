# Installation

## Requirements

- PHP 8.2 or newer with the extensions required by your application.
- Composer 2 for creating the project and installing PHP dependencies.
- The Tusk Engine binary on your `PATH` as `tusk`.
- RoadRunner (`rr`) available to the Engine at runtime.

`tusk doctor` diagnoses the selected tools but does not install them. Install
and manage PHP and RoadRunner using your platform's package/release workflow,
or follow the Engine's explicit toolchain-provisioning documentation when a
verified catalog is configured.

## Install the Engine

Download the archive for your operating system and architecture from the
[Tusk Engine releases](https://github.com/tusk-framework/tusk-engine/releases),
then put the `tusk` executable on your `PATH`. Follow the release asset's
included instructions for your platform.

## Create an application

```sh
composer create-project tusk-framework/app catalog
cd catalog
```

Before starting the server, verify that the project bootstrap and required
tools are available:

```sh
tusk doctor
```

Continue to the [Quick Start](quickstart.md) to run the app.

## Contributing to the Framework

To work on the Framework source itself, clone
[tusk-framework/tusk-framework](https://github.com/tusk-framework/tusk-framework)
and follow its `CONTRIBUTING.md`. Cloning the Framework is not required to
create an application.
