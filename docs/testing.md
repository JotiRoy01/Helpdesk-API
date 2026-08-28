# Testing Strategy

## Test Layers

### Unit

Tests isolated business rules such as:

- SLA calculations;
- overdue logic;
- workflow transitions;
- serializer validation;
- permission rules.

### Integration

Tests interactions between:

- authentication;
- tickets;
- assignment;
- comments;
- dashboard;
- audit logs.

### Security

Tests:

- IDOR protection;
- role escalation;
- authentication bypass;
- authorization boundaries;
- sensitive-data leakage;
- rate limiting;
- safe error handling.

### Performance

Tests:

- query count;
- N+1 regressions;
- pagination limits;
- dashboard aggregation;
- workload aggregation.

## Commands

Run all tests:

```bash
pytest -v