# Database Architecture

## Primary Database

The HelpDesk API uses MySQL as its primary relational database.

## Database Configuration

- Engine: MySQL
- Character set: utf8mb4
- Strict SQL mode enabled
- Transaction isolation: READ COMMITTED
- Django ORM used for data access

## Current Core Tables

### users

Stores application users.

Important fields:

- id
- email
- first_name
- last_name
- role
- is_active
- is_staff
- is_superuser
- created_at
- updated_at

## Database Design Principles

1. Business relationships are represented through relational foreign keys.
2. Frequently filtered fields receive appropriate indexes.
3. Sensitive credentials are supplied through environment variables.
4. Database constraints complement application-level validation.
5. Transactions are used for multi-step state-changing operations.
6. Public API identifiers use UUIDs where appropriate.