---
name: quarkus
description: "Use this as the entrypoint skill for Quarkus work in any kind of project. Use decision tree below to find the right domain, then load detailed references."
---
# Quarkus

Use this as the entrypoint skill for Quarkus work in any kind of project.
Use decision tree below to find the right domain, then load detailed references.

## Decision Tree

```
What do you need?
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Dependency injection (CDI / ArC)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ dependency-injection
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Application configuration (.properties, profiles, config mapping)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ configuration
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ REST and HTTP APIs
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ web-rest
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Templates and server-side rendering (Qute)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ templates
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ OpenAPI and API contract documentation
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ openapi
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Databases, ORM, migrations, data access
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Standard JPA / Hibernate ORM usage
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ data-orm
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Panache entities and repositories for simpler CRUD/data access
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ data-panache
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Schema migrations and database evolution with Flyway
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ data-migrations
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Advanced Hibernate ORM features: multiple persistence units, multitenancy, caching, extension points
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ data-orm-advanced
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Event streaming and asynchronous messaging channels
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Is the event crossing a service/process boundary?
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ YES -> messaging
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ NO (in-process only)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need clustering or non-blocking event loop behavior
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ YES -> vertx-event-bus
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Want portability and type safety
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡        ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ YES -> cdi-events
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Communicating with external APIs, communication between services
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need asynchronous delivery, replay, or broker-managed fan-out
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ messaging
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need synchronous request/response calls
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ service-communication
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Shared protobuf contract and HTTP/2 streaming fit well
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ service-communication-grpc
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Standard HTTP/JSON or simpler interoperability matters more
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡        ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ service-communication-rest
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Authentication, authorization, identity providers
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need core Quarkus security concepts, RBAC, built-in auth mechanisms, or custom policies
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ security-core
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Protect endpoints with OpenID Connect
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Inbound bearer tokens, browser login redirects, or hybrid OIDC apps
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ security-oidc
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Outbound token acquisition, refresh, exchange, or propagation to downstream services
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ security-oidc-client
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need JWT verification or token building without full OIDC integration
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ security-jwt
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need username/password identity stores backed by JPA, JDBC, or LDAP
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ security-identity-providers
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need passkeys or WebAuthn flows
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ security-webauthn
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need to test secured applications
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ security-testing
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Logging, health, metrics, traces
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need help choosing signals, management exposure, or local observability stack
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ observability
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Logging configuration, JSON logs, MDC, and log shipping
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ observability-logging
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Liveness/readiness/startup probes and Health UI
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ observability-health
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Metrics, Micrometer registries, and Prometheus/OTLP export
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ observability-metrics
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Distributed tracing, propagation, and OpenTelemetry
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ observability-tracing
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Native image, jars, and container packaging
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ native-and-packaging
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need a native build, closed-world metadata, native SSL, or native-only runtime behavior
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ native-image
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need JVM artifact shape decisions: `fast-jar`, `uber-jar`, `mutable-jar`, layout, or re-augmentation
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ packaging-jars
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Need container image packaging: Jib, Docker, Podman, OpenShift, Buildpacks, tags, push, or base images
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡        ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ packaging-containers
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Testing 
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Start with the feature module you are testing (for example `security-testing` or `native-image`)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Dev mode, CLI, build plugins
   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ tooling
```

## General guidelines 

- Quarkus resolves much of its framework wiring at build time, so expect many integration mistakes to fail during build or startup rather than deep at runtime.
- Align all extension versions through the Quarkus platform BOM.
- Start with the smallest extension set, then add only what the feature needs.
- Never skip writing high-level integration tests and prefer them opposed to unit testing individual components. Only write unit tests when they are actually beneficial, e.g. implementing methods with complex logic
