# Security Architecture

## Authentication

The API uses JWT-based authentication.

Access tokens are short-lived.
Refresh tokens have a longer lifetime and support blacklist-based logout.

## Authorization

Authorization is enforced through:

- role-based permissions;
- object-level permissions;
- role-aware querysets;
- explicit domain validation.

## Roles

- Customer
- Support Agent
- Admin

## Data Protection

Sensitive configuration is stored in environment variables.

The application does not expose:

- passwords;
- password hashes;
- JWT secrets;
- database passwords;
- internal stack traces;
- SQL statements.

## Request Protection

The API uses:

- authentication;
- role-based authorization;
- rate throttling;
- request-size limits;
- JSON-only API parsing;
- explicit CORS origins.

## Production Security

Production configuration uses:

- `DEBUG=False`;
- HTTPS redirect;
- secure cookies;
- HSTS;
- `nosniff`;
- `X-Frame-Options`;
- controlled `ALLOWED_HOSTS`.

## Information Leakage

Private resources are hidden where appropriate.

For example, access to another user's ticket does not reveal whether the ticket exists.

## Logging

Unexpected server errors are logged internally while clients receive safe generic error responses.

Request IDs are used for correlation.
