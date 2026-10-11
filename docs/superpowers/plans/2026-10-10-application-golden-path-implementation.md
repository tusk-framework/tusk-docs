# Tusk Application Golden Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Keep each repository change in its own PR/worktree and verify every acceptance criterion before reporting completion.

**Goal:** Deliver and verify one public, stable path from a clean Composer install to a Tusk application served by RoadRunner, consistently across the App skeleton, Engine, and Docs.

**Architecture:** Composer creates the project; the Framework owns application bootstrap and request handling; the Engine validates/configures and supervises RoadRunner; RoadRunner owns HTTP transport and PHP workers. No Engine proxy or second worker pool is introduced. Framework's separately reviewed breaking cleanup and major release is a prerequisite to publishing the App skeleton against that API.

**Tech Stack:** PHP 8.2+, Composer/Packagist, Go CLI, RoadRunner, PowerShell smoke harness (Linux CI), MkDocs Material.

**Spec:** `docs/superpowers/specs/2026-10-10-application-golden-path-design.md` (merged in Docs PR #3).

## Global Constraints

- Update each repository's local `main` from `origin/main` and verify its tracked baseline before creating implementation branches/worktrees.
- Never use `codex/` in branch names. Use conventional repository prefixes and lowercase kebab-case.
- Preserve existing user worktrees and untracked files; all repository work is delivered through separate PRs.
- Do not begin the Framework mock/discovery removal from this plan. Framework PR #61 is a separate draft design-review gate; only after its spec is approved should that work receive its own implementation plan and approval. Publish the resulting Framework major before changing/registering the App package.
- Confirm the actual published Framework tag before setting the App constraint (expected `^1.0.0`, not an assumption).
- Never use a local path repository or `dev-*` Framework dependency to prove the public consumer path.
- Keep `tuskpress` an example, not a product requirement. Do not add a gateway, native server, service mesh, duplicate worker pool, or unrelated app features.
- Do not commit Packagist credentials or webhook secrets. If account-level package registration is unavailable, stop at the external prerequisite and report it.
- Issue #9 is closed only after all public-package/runtime/docs evidence is recorded.

## Dependency Order

```text
Framework PR #61 spec review → separately planned implementation → breaking major release
                                                        ↓
                                      App identity + Packagist publication
                                      ↙                       ↘
                         Engine public-consumer smoke       Docs rewrite/build
                                      ↘                       ↙
                                  clean end-to-end proof → Framework issue #9
```

Docs may be implemented independently after this plan is approved. Engine harness work can be prepared independently, but its public-package run is gated on App registration and stable indexing. Framework PR #61 must not be treated as implementation approval merely because its checks are green.

## PR 1 — App package identity and public installation

**Repository:** `tusk-app`  
**Branch:** `chore/packagist-app-identity`  
**Prerequisite:** Framework breaking cleanup merged and its compatible stable major is available from Packagist.

### Files / behavior

- `composer.json`: set package name to `tusk-framework/app`; retain `type: project`; require the actually published compatible stable Framework major.
- `README.md`: canonical `composer create-project tusk-framework/app <directory>` flow, then `tusk doctor` and `tusk start`; explain the sample `/api/products` route is in-memory and not persistence. Do not include `tusk build`.
- Existing manifest/package identity tests (locate current test path before editing): assert the exact vendor/package name and project type; reject old `tusk/app` identity and local/dev dependencies.
- Any metadata or install instructions in the skeleton must use the Composer package name while keeping GitHub repository slug `tusk-framework/tusk-app`.

### TDD / verification

1. Add/update manifest tests first; run the focused test and confirm it fails on the old name/constraint.
2. Change manifest and README; run the focused test and full App test suite.
3. Run `composer validate --strict` and `composer install --no-interaction --prefer-dist` from a clean temporary copy.
4. Verify the installed `composer.lock` resolves a stable Framework tag satisfying the new constraint, with no path repository and no `dev-*` package version.
5. Verify CI's supported PHP matrix (currently 8.2–8.5) and open a PR with the standard summary, rationale, verification, and release-impact sections.

### Packagist release gate (external account action)

1. Register `tusk-framework/app` from the `tusk-framework/tusk-app` GitHub repository only after the manifest points at the published Framework major.
2. Configure Packagist's GitHub auto-update hook using Packagist/GitHub UI or authorized tooling; keep credentials out of source and logs.
3. Verify a package metadata refresh and then run `composer create-project tusk-framework/app <empty-temp-directory> --no-interaction --prefer-dist` from outside all Tusk checkouts.
4. Confirm package metadata/version and installed Framework version from Composer output/lockfile. A webhook HTTP 2xx alone is insufficient proof of indexing.

## PR 2 — Docs canonical getting-started path

**Repository:** `tusk-docs`  
**Branch:** `docs/published-app-golden-path`

### Files / behavior

Rewrite only pages that contradict the merged spec/current CLI; inspect each page before editing:

- `docs/index.md`
- `docs/getting-started/installation.md`
- `docs/getting-started/quickstart.md`
- `docs/getting-started/first-app.md`
- `docs/guides/cli-usage.md`
- `docs/guides/deployment.md`
- `docs/guides/engine-integration.md`
- `docs/architecture/engine.md`
- `docs/architecture/overview.md`
- `docs/architecture/runtime.md`
- `docs/architecture/web.md` (currently advertises a removed PHP socket server).
- `docs/api/kernel.md` (currently documents removed Kernel methods and a removed HTTP server).
- `mkdocs.yml` navigation labels where they describe removed Native Engine behavior.

Present one verified path: install Engine prerequisites, `composer create-project tusk-framework/app <directory>`, `cd <directory>`, `tusk doctor`, `tusk start`, then request the sample endpoint. Explain which component owns each action; distinguish Engine lifecycle supervision from RoadRunner's HTTP/worker ownership; state the in-memory sample limitation. Do not document `tusk build`: the CLI has no such built-in command, configuration generation happens during `tusk start`, and no build artifact is currently defined. Revisit only alongside a concrete build/optimization design. Remove active user-doc claims about Engine-owned request pools/IPC, NDJSON, root `worker.php`, native HTTP transport, or `tusk init <name>` scaffolding. Preserve unrelated guides only after verifying their examples against current code.

### TDD / verification

1. Add `tests/test_golden_path_docs.py` before the rewrite. Assert the public create-project command plus `tusk doctor` and `tusk start`; assert active onboarding pages do not show an unsupported `tusk build` command; verify RoadRunner owns HTTP/workers; reject obsolete runtime claims in active pages. Keep historical specs/archives outside the active-page scan.
2. Rewrite pages/navigation; run that focused check and search active docs for `worker.php`, `NDJSON`, `tusk init <name>`, and claims that Engine owns HTTP/worker pools. Review each hit rather than blindly deleting valid API references.
3. Install dependencies using the repository's documented MkDocs setup and run `mkdocs build --strict`.
4. Add `.github/workflows/validate.yml` to install MkDocs and its Material theme, run `python -m unittest discover -s tests -v`, and run `mkdocs build --strict` on pull requests and pushes to `main`; use a supported Python version and read-only repository permissions. Verify workflow syntax and commands before opening the PR.
5. Open the PR with rendered navigation/page list and exact build evidence. If package installation/network is unavailable, do not claim strict-build success; leave that check pending and report the environmental blocker.

## PR 3 — Engine clean public-consumer smoke

**Repository:** `tusk-engine`  
**Branch:** `test/public-app-golden-path`
**Prerequisite for public run:** App package registered and `composer create-project` succeeds from Packagist.

### Files / behavior

- Add a dedicated `test/skeleton/public-app.ps1` (or equivalent isolated test harness) and focused Go contract tests for its invocation/acceptance behavior where practical.
- Extend `.github/workflows/test.yml` to run this consumer smoke in addition to, not instead of, the existing comprehensive generated-skeleton/local-Framework smoke.
- Use a fresh temporary directory, public `composer create-project`, the built Engine binary, CI's actual RoadRunner binary, and no local Framework checkout/path repository/dev package.
- Exercise the documented sequence `tusk doctor`, `tusk start`; verify startup generates the RoadRunner configuration and use a bounded readiness loop to request `POST /api/products`, asserting HTTP 201 and the expected response shape. Verify Engine exits non-zero on failed stages, preserve useful logs, and always terminate/reap Engine, RoadRunner, and PHP children on success/failure/timeout.
- Use dynamically allocated loopback ports where supported; avoid races from probe-then-bind if the CLI can accept a port through generated config. Confirm actual generated config and CLI behavior before choosing the port injection mechanism.
- Keep existing `test/skeleton/smoke.ps1` semantics and its local Framework path override intact; this new smoke is separate specifically to cover published-consumer behavior.

### TDD / verification

1. Add harness contract tests first for the command sequence, no local/path/dev dependency, non-zero failures, bounded startup, HTTP assertion, and cleanup path; demonstrate failure before implementation.
2. Implement the isolated script and workflow invocation. Exercise on Linux with PHP, Composer, Go, RoadRunner, and a real published App package.
3. Run `go test ./...`, `go vet ./...`, existing skeleton smoke, and the new public smoke. Confirm the new test runs in CI rather than silently returning a skipped success when a required public prerequisite is absent.
4. Capture Engine/RoadRunner logs on failure and verify the harness cleans all child processes. Keep credentials/secrets out of logs and test artifacts.
5. Open a separate PR with explicit public package/version and smoke evidence.

## Final acceptance and issue #9

After the App package is indexed and all three PRs are merged:

1. From an empty temporary directory not nested under any repository, run the exact documented `composer create-project tusk-framework/app ...` command.
2. Verify the installed Framework is a stable published major and run the skeleton's test suite/manifest validation.
3. Run `tusk doctor`, `tusk start`; send the documented HTTP request and assert the response through RoadRunner.
4. Run `mkdocs build --strict` and the active-doc obsolete-claim scan.
5. Record exact versions, commands/results, and links to the App/Engine/Docs PRs on Framework issue #9; close it only if every acceptance criterion passes. If Packagist account/indexing is blocked, keep #9 open and report precisely which external step remains.

## Review Focus

- Does the public Composer package use exactly `tusk-framework/app`, retain `type: project`, and resolve a stable compatible Framework release?
- Does any proof accidentally depend on a local checkout, `path` repository, or `dev-*` release?
- Does documentation assign HTTP transport and PHP worker lifecycle to RoadRunner, not Engine?
- Are sample state limitations clear, without promoting TuskPress or claiming persistence?
- Can a failing or hung smoke stage be diagnosed, return non-zero, and clean up its entire child-process tree?
- Does CI actually execute both the existing development smoke and the new public-consumer smoke?
- Are Packagist registration, webhook refresh, and successful clean install verified as distinct steps?
- Is Framework issue #9 left open until release, public install, runtime, docs build, and evidence are all complete?
