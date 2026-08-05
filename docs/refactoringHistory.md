# GlobeTrotter - Refactoring History

> **Purpose:** Document the complete evolution of the GlobeTrotter backend from the original monolithic architecture to the current layered architecture.

---

# Introduction

This document records every major architectural decision made during the refactoring of GlobeTrotter.

The project initially started as a simple monolithic Flask application provided as the starting point for a software engineering project.

The objective of the refactoring was **not to change the business logic**, but to progressively transform the project into a clean, maintainable and scalable architecture that can later evolve into independent microservices.

Every important modification has been implemented inside a dedicated Git branch before being merged into the main branch.

---

# Initial State

## Original Architecture

The original project contained a classic Flask monolith.

```
app/

__init__.py

auth.py

destinations.py

recommendations.py

itineraries.py

models.py

main.py
```

Business logic, data access and HTTP handling were tightly coupled.

Routes were directly reading and writing JSON files.

---

# Problems Identified

Several limitations were observed.

## Tight Coupling

Routes directly manipulated JSON storage.

Example

```
Route

↓

read_json()

↓

Business Logic

↓

HTTP Response
```

Every endpoint mixed several responsibilities.

---

## Code Duplication

Repeated logic appeared throughout the project.

Examples included:

- JSON reading
- JSON writing
- password verification
- JWT validation
- response formatting

---

## Poor Scalability

As the application grows:

- maintenance becomes difficult
- testing becomes complicated
- introducing new features requires modifications across multiple files

---

# Refactoring Strategy

The refactoring was divided into multiple incremental sprints.

Each sprint focused on one architectural improvement while preserving application functionality.

---

# Sprint 1 — Authentication Refactoring

## Objective

Separate authentication logic from HTTP routes.

---

## Achievements

Created:

```
services/

AuthenticationService
```

Authentication responsibilities moved into the service layer.

Routes now delegate authentication operations.

Example

Before

```
Route

↓

Validation

↓

Password Verification

↓

JWT Generation

↓

JSON Response
```

After

```
Route

↓

Authentication Service

↓

Response
```

---

## Benefits

- cleaner routes
- reusable authentication logic
- easier testing

---

# Sprint 2 — Repository Layer

## Objective

Separate data access from business logic.

---

## New Structure

Created

```
repositories/

base_repository.py

user_repository.py

destination_repository.py

itinerary_repository.py
```

Repositories became responsible only for persistence.

---

## Base Repository

A generic BaseRepository was introduced.

Responsibilities:

- read all records
- save collections
- append new records

Every repository now inherits these common operations.

---

## Example

Before

```
UserRepository

↓

read_json()

↓

write_json()
```

After

```
UserRepository

↓

BaseRepository

↓

JSON Storage
```

---

## Benefits

- no duplicated persistence code
- reusable storage layer
- centralized file operations

---

# Sprint 3 — Service Layer

## Objective

Move business logic outside Flask routes.

---

## Services Created

```
services/

auth_service.py

destination_service.py

recommendation_service.py

itinerary_service.py
```

---

## Responsibilities

Authentication Service

- registration
- login
- credential validation

Destination Service

- search
- filtering

Recommendation Service

- recommendation scoring
- preference matching

Itinerary Service

- itinerary creation
- itinerary retrieval

---

## Benefits

Business logic became independent from HTTP requests.

Services can now be reused by:

- REST APIs
- CLI applications
- scheduled jobs
- future microservices

---

# Sprint 4 — Shared Utilities

Several reusable utilities were introduced.

Created:

```
utils/

responses.py

jwt.py

password_utils.py
```

---

## responses.py

Introduced standardized API responses.

Before

```
return jsonify(...)
```

After

```
return success(...)

return error(...)
```

Advantages

- consistent API responses
- less duplicated code
- easier frontend integration

---

## password_utils.py

Password operations became centralized.

Before

```
generate_password_hash()

check_password_hash()
```

After

```
hash_password()

verify_password()
```

---

## jwt.py

JWT operations became reusable.

Centralized

- token creation
- token decoding
- authenticated user extraction

---

# Current Backend Architecture

The backend now follows a layered architecture.

```
Client

↓

Routes

↓

Services

↓

Repositories

↓

Base Repository

↓

JSON Storage
```

Every layer has one responsibility.

---

# Git Workflow

Development follows a feature branch strategy.

Example

```
main

│

├── feature/auth-refactor

├── feature/repository-layer

├── feature/service-layer

├── feature/microservices

└── feature/docker
```

Each feature is:

implemented

↓

tested

↓

reviewed

↓

merged into main

---

# Files Added During Refactoring

## Services

- auth_service.py
- destination_service.py
- recommendation_service.py
- itinerary_service.py

---

## Repositories

- base_repository.py
- user_repository.py
- destination_repository.py
- itinerary_repository.py

---

## Utilities

- responses.py
- jwt.py
- password_utils.py

---

## Documentation

Created

```
docs/

PROJECT_OVERVIEW.md

ARCHITECTURE.md

REFACTORING_HISTORY.md

API.md

CHANGELOG.md
```

---

# Architectural Improvements

The refactoring introduced several software engineering concepts.

- Layered Architecture
- Repository Pattern
- Service Layer Pattern
- Base Repository
- Shared Utilities
- API Standardization
- Modular Design

---

# Current Status

Completed

- Authentication Refactoring
- Repository Layer
- Service Layer
- Base Repository
- Shared Utilities
- Standardized API Responses
- JWT Authentication
- Git Feature Workflow

---

# Next Phase

The next architectural evolution consists of transforming the application into independent microservices.

The future architecture will include:

```
Frontend

↓

API Gateway

↓

Authentication Service

↓

Destination Service

↓

Recommendation Service

↓

Itinerary Service

↓

PostgreSQL

↓

Docker

↓

Kubernetes

↓

Cloud Deployment
```

Each service will:

- own its business logic
- own its database
- expose REST APIs
- communicate through HTTP
- be independently deployable

---

# Conclusion

The GlobeTrotter backend has undergone a complete architectural transformation while preserving its original business requirements.

Instead of rewriting the application from scratch, the project evolved incrementally through carefully planned refactoring sprints.

This approach reduced technical debt, improved maintainability, and established a solid foundation for the upcoming migration toward a Docker-based microservices architecture.

The project now follows software engineering practices commonly used in professional backend development and is ready for its next evolution toward cloud-native deployment.