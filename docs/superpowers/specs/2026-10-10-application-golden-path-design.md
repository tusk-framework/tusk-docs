# Tusk Published Application Golden Path

**Status:** Design and implementation plan approved by the user; implementation in progress.

**Decision update:** The canonical flow does not include `tusk build`. The Engine has no built-in build command, and the App skeleton has no Composer `build` script. The Engine generates RoadRunner configuration as part of `tusk start`; the project currently has no compilation or package artifact that would justify a separate build step. Revisit a preparation command only when Tusk defines a concrete artifact or production-optimization contract.

## Goal

Make the supported path from a clean machine to a running Tusk PHP application discoverable, reproducible, and verifiable across the App skeleton, Framework package, Engine, and Docs repositories.

## User and success criteria

The target user is a PHP developer who has Composer and the Tusk Engine available, but has not cloned or edited Tusk's own repositories. They should be able to create a project from Packagist, understand which component owns each concern, validate the environment, start the application through RoadRunner, and receive an HTTP response from the sample endpoint.

Success means the public Composer command works from a clean temporary directory using stable published packages, the documented Engine commands match the released CLI, the sample endpoint is reachable, and the documentation build succeeds without stale descriptions of the removed native/NDJSON worker architecture.

## Canonical ownership and flow

| Component | Responsibility |
| --- | --- |
| Composer / `tusk-framework/app` | Creates an application project and installs its stable dependencies. |
| Tusk Framework | Owns application bootstrap, routes, dependency injection, validation, and request handling. |
| Tusk Engine | Validates project/runtime configuration, generates RoadRunner configuration at startup, starts and supervises RoadRunner, and reports readiness/health. |
| RoadRunner | Owns HTTP transport and PHP worker lifecycle. |

Canonical flow:

```text
composer create-project tusk-framework/app <directory>
cd <directory>
tusk doctor
tusk start
```

The application entry point remains `bootstrap/app.php`. RoadRunner serves requests and manages PHP workers; the Engine is a runtime manager, not an HTTP proxy or a second worker pool. The skeleton's `/api/products` route is an example only and stores data in memory.

## Public package identity and release order

- Keep the GitHub repository slug `tusk-framework/tusk-app`; set the Composer project package name to `tusk-framework/app`.
- Register `tusk-framework/app` on Packagist and configure/verify automatic updates from pushes to its GitHub repository. Do not commit Packagist credentials or webhook secrets.
- The Framework's current public stable release is `0.3.2`. The separately approved removal of its unfinished declarative HTTP/discovery proof of concept is a breaking API cleanup. Respect the repository's configured breaking-change → major release rule; do not silently ship the removal as a patch/minor release.
- Publish the Framework's resulting stable major release before changing the skeleton to require it. Then update the skeleton's Framework constraint to the new compatible stable major (currently expected to be `^1.0.0` from `0.3.2`; confirm the actual release tag before editing the manifest).
- Do not register/publish an App package while its manifest requires a Framework version that is not yet published.

## Scope

1. **App repository:** update the package identity, version constraint after the Framework major release, README/create-project examples, and manifest tests. Preserve the project type and application code; do not turn the skeleton into a reusable library.
2. **Engine repository:** run and, if necessary, strengthen a clean-consumer smoke test that starts from the published Composer skeleton and checks the documented `doctor` and `start` lifecycle. Keep RoadRunner as the transport/worker owner. The test must not rely on a local Framework path override or a `dev-*` dependency.
3. **Docs repository:** rewrite the current getting-started path, CLI usage, Engine integration, architecture, and deployment pages to match the canonical flow. Update navigation labels and remove obsolete examples that claim the Engine implements request pools/IPC, NDJSON, a root `worker.php`, a native HTTP server, or `tusk init <name>` scaffolding. Keep unrelated guides only where they remain accurate.
4. **Framework issue #9:** update its checklist with repository/PR evidence; close only after the clean consumer install, Engine smoke, and documentation build all pass.

## Out of scope

- Promoting TuskPress into a product; it remains an illustrative sample.
- Adding an Engine HTTP proxy/gateway, service mesh, native transport, or another worker pool.
- Reopening intentionally deferred Framework issues #7 or #8.
- Adding a new public Framework SDK or declarative outbound HTTP client as part of the golden path.
- Reworking application features unrelated to demonstrating the skeleton and RoadRunner lifecycle.

## Acceptance criteria

1. A clean Composer invocation can create `tusk-framework/app` without a local path repository, development branch, or copied Framework source.
2. The resulting project resolves a stable Framework release compatible with the skeleton constraint and passes its manifest validation and test suite.
3. A clean Engine smoke run can execute the documented CLI lifecycle and reach the sample HTTP endpoint through RoadRunner; failure output identifies the failing stage and preserves non-zero exit status.
4. The documentation presents one consistent create → diagnose → start → verify path, names the component that owns each step, and makes the Engine/RoadRunner/Framework boundary explicit. It does not advertise a `tusk build` step until that command has a concrete, separately designed artifact or optimization contract.
5. `mkdocs build --strict` succeeds, and a search of active user documentation finds no obsolete Native Engine/NDJSON/`worker.php` runtime claims or unsupported `tusk init <name>` project-generation examples.
6. Packagist contains the matching `tusk-framework/app` package and the GitHub push-update mechanism is verified with a successful package metadata refresh; an HTTP webhook acknowledgement alone is not considered proof of index refresh.
7. Framework issue #9 is closed only after links to the merged App/Engine/Docs PRs and the above verification evidence are recorded.

## Rollout and dependencies

The implementation is split into repository PRs. First merge and release the Framework breaking cleanup. Then update and register the App skeleton against that stable release. In parallel, update Docs and prepare the Engine clean-consumer smoke once the package is publicly resolvable. Run the final golden-path check from an empty directory, record evidence on issue #9, and close it last. If Packagist registration or indexing is blocked, keep the relevant PR open and report the external prerequisite rather than substituting a local path repository.

## Risks and mitigations

- **Packagist identity or indexing mismatch:** verify the exact Composer name and clean public install before treating the path as complete.
- **Breaking-version mismatch:** read the actual published Framework tag and test the App constraint against it before publishing the skeleton package.
- **Docs drift:** validate every command against Engine CLI behavior and the App README; require a strict MkDocs build.
- **Flaky end-to-end runtime checks:** bound startup/readiness time, collect Engine/RoadRunner logs on failure, and use deterministic cleanup in the smoke harness.
