AUTHENTICATION

POST /api/v1/auth/register/
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/
GET  /api/v1/auth/me/


CATEGORIES

GET   /api/v1/categories/
POST  /api/v1/categories/
GET   /api/v1/categories/{id}/
PATCH /api/v1/categories/{id}/


TICKETS

GET   /api/v1/tickets/
POST  /api/v1/tickets/
GET   /api/v1/tickets/{id}/
PATCH /api/v1/tickets/{id}/


TICKET ACTIONS

POST /api/v1/tickets/{id}/assign/
POST /api/v1/tickets/{id}/transition/


COMMENTS

GET  /api/v1/tickets/{id}/comments/
POST /api/v1/tickets/{id}/comments/


DASHBOARD

GET /api/v1/dashboard/summary/
GET /api/v1/dashboard/workload/


AUDIT

GET /api/v1/audit-logs/


SYSTEM

GET /api/v1/health/