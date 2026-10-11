# Deployment

Deploy the application, PHP runtime, Composer dependencies, Tusk Engine, and
RoadRunner as explicit parts of your runtime environment. The Engine supervises
RoadRunner; RoadRunner owns the public HTTP listener and PHP workers.

## Production checklist

1. Install a supported PHP version and the extensions required by your app.
2. Commit the application's `composer.lock`, then install its locked
   dependencies, for example with
   `composer install --no-dev --prefer-dist --no-interaction --optimize-autoloader`.
3. Install the Tusk Engine and RoadRunner versions selected for the deployment.
4. Provide production configuration and secrets through your platform's secret
   management; do not commit credentials.
5. Run `tusk doctor` as a deployment check, then start the app with `tusk
   start`.
6. Configure the platform's TLS termination, health checks, logging, and
   restart policy. Expose only the intended public listener.

The Engine generates RoadRunner configuration at startup from the project
configuration. The application is served from its Composer project; no
separate application artifact is produced by the current runtime workflow.

## Reverse proxy and TLS

When TLS termination or edge routing is required, place the deployment's
existing load balancer or reverse proxy in front of RoadRunner. This is an
infrastructure choice; the Engine does not proxy HTTP traffic.

## Long-lived workers

RoadRunner workers handle multiple requests over their lifetime. Avoid keeping
request-specific mutable state in long-lived services. Use a database or
shared cache for state shared between workers and instances, and follow the
Framework's request-scope lifecycle when adding application services.
