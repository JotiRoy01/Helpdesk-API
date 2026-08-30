## Dashboard

### Summary

```http
GET /api/v1/dashboard/summary/
Authorization: Bearer <token>

## Audit Logs

Audit logs record important state-changing operations.

Examples include:

- ticket creation;
- ticket assignment;
- ticket reassignment;
- ticket status changes;
- ticket priority changes;
- comment creation;
- category changes.

### List Audit Logs

```http
GET /api/v1/audit-logs/
Authorization: Bearer <admin-token>


---

# 15.43 Run migrations/checks

Run:

```bash
python manage.py check
```
