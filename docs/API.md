# GlobeTrotter - REST API Documentation

> **API Version:** v1.0  
> **Architecture:** Layered Architecture (Routes → Services → Repositories)  
> **Authentication:** JSON Web Token (JWT)

---

# Introduction

This document describes every REST API endpoint currently implemented in the GlobeTrotter backend.

The API allows clients to:

- Register users
- Authenticate users
- Search destinations
- Retrieve personalized recommendations
- Create itineraries
- Retrieve user itineraries

All responses are returned in JSON format.

---

# Base URL

During local development:

```

http://localhost:5000

```

or

```

http://127.0.0.1:5000

```

---

# Authentication

Authentication uses JSON Web Tokens (JWT).

Protected endpoints require the following HTTP header:

```

Authorization: Bearer <JWT_TOKEN>

```

The token is obtained after a successful login.

---

# Standard API Responses

The project uses standardized API responses through `responses.py`.

## Success Response

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {}
}
```

---

## Error Response

```json
{
    "success": false,
    "message": "Description of the error."
}
```

---

# Endpoints

---

# Register User

Create a new user account.

## Endpoint

```

POST /register

```

---

## Request Body

```json
{
    "username": "rick",
    "password": "123456",
    "preferences": [
        "shopping",
        "food",
        "nightlife"
    ]
}
```

---

## Success Response

Status Code

```

201 Created

```

Example

```json
{
    "success": true,
    "message": "User registered successfully",
    "data": {
        "username": "rick"
    }
}
```

---

## Possible Errors

| Status | Description |
|---------|-------------|
|400|Username or password missing|
|409|Username already exists|

---

# Login

Authenticate an existing user.

## Endpoint

```

POST /login

```

---

## Request Body

```json
{
    "username": "rick",
    "password": "123456"
}
```

---

## Success Response

Status Code

```

200 OK

```

Example

```json
{
    "token": "eyJhbGciOi..."
}
```

---

## Possible Errors

| Status | Description |
|---------|-------------|
|400|Missing credentials|
|401|Invalid credentials|

---

# Search Destinations

Search destinations according to user criteria.

## Endpoint

```

GET /destinations

```

---

## Query Parameters

| Parameter | Description |
|------------|-------------|
|q|Search keyword|
|tag|Destination category|
|continent|Destination continent|
|max_cost|Maximum daily budget|

Example

```

GET /destinations?tag=shopping

```

---

## Success Response

```json
[
    {
        "id": 1,
        "name": "Marché Central",
        "description": "...",
        "tags": [
            "shopping"
        ]
    }
]
```

---

## Possible Errors

| Status | Description |
|---------|-------------|
|400|Invalid max_cost value|

---

# Recommendations

Return personalized destination recommendations.

Authentication required.

## Endpoint

```

GET /recommendations

```

---

## Headers

```

Authorization: Bearer JWT_TOKEN

```

---

## Query Parameters

| Parameter | Description |
|------------|-------------|
|limit|Maximum number of recommendations|

Default

```

limit=5

```

---

## Success Response

```json
[
    {
        "name": "Marché Central",
        "match_score": 3
    }
]
```

---

## Possible Errors

| Status | Description |
|---------|-------------|
|401|Authentication required|
|404|User not found|

---

# Create Itinerary

Create a new itinerary.

Authentication required.

## Endpoint

```

POST /itineraries

```

---

## Request Body

```json
{
    "title": "Weekend Shopping",
    "destinations": [
        "Marché Central"
    ],
    "start_date": "2026-08-01",
    "end_date": "2026-08-02",
    "notes": "Buy clothes"
}
```

---

## Success Response

Status Code

```

201 Created

```

Example

```json
{
    "id": "...",
    "title": "Weekend Shopping",
    "destinations": [
        "Marché Central"
    ]
}
```

---

## Possible Errors

| Status | Description |
|---------|-------------|
|400|Missing title|
|400|Invalid destinations|
|401|Authentication required|

---

# Get User Itineraries

Retrieve all itineraries belonging to the authenticated user.

Authentication required.

## Endpoint

```

GET /itineraries

```

---

## Headers

```

Authorization: Bearer JWT_TOKEN

```

---

## Success Response

```json
[
    {
        "title": "Weekend Shopping",
        "destinations": [
            "Marché Central"
        ]
    }
]
```

---

## Possible Errors

| Status | Description |
|---------|-------------|
|401|Authentication required|

---

# HTTP Status Codes

| Code | Meaning |
|------|---------|
|200|Request successful|
|201|Resource created|
|400|Bad request|
|401|Unauthorized|
|404|Resource not found|
|409|Conflict|

---

# Current API Workflow

The current backend follows the architecture below.

```
Client

↓

HTTP Request

↓

Route

↓

Service

↓

Repository

↓

JSON Storage

↓

Response

↓

Client
```

---

# Future API Evolution

The current REST API represents Version 1 of GlobeTrotter.

Future versions will include:

- API Gateway
- Microservices
- Docker deployment
- PostgreSQL
- Google Maps integration
- Geolocation
- Favorites
- Reviews
- Notifications
- Analytics
- OpenAPI / Swagger documentation

---

# Testing

The API has been validated using:

- Postman
- cURL

All implemented endpoints have been successfully tested.

---

# Conclusion

The GlobeTrotter REST API provides a clean and modular interface for interacting with the application.

The current implementation is built on a layered architecture using Routes, Services and Repositories, making it ready for future migration to Docker-based microservices and cloud-native deployment.