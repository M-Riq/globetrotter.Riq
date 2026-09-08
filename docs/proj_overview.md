# GlobeTrotter - Project Overview

## Introduction

GlobeTrotter is a travel assistance platform designed to help visitors discover the city of Yaoundé, Cameroon, based on their personal interests and travel preferences.

Unlike traditional travel applications, GlobeTrotter focuses on providing personalized recommendations for real places within Yaoundé. The platform is intended to simplify navigation, improve visitor experiences, and help newcomers quickly find locations that match their needs.

This project was initially provided as a monolithic Flask application as part of a university software engineering project. Since then, the application has been progressively redesigned following modern software engineering practices, with the objective of transforming it into a scalable microservices architecture.

---

# Project Objectives

The main objective of GlobeTrotter is to provide travelers with useful information about Yaoundé according to their personal interests.

The platform allows users to:

- Create an account
- Define personal preferences
- Discover destinations
- Receive personalized recommendations
- Build travel itineraries
- Prepare trips more efficiently

Future versions will include additional smart features such as navigation, notifications, favorites, analytics and location-aware services.

---

# Business Context

Many visitors arriving in Yaoundé are unfamiliar with the city.

Finding suitable places for shopping, restaurants, nightlife, tourism or administrative services often requires local knowledge.

GlobeTrotter aims to solve this problem by acting as a digital travel assistant capable of recommending locations based on each user's interests.

Instead of displaying every location available, the application prioritizes destinations that are relevant to the user's profile.

---

# Target Users

GlobeTrotter is primarily designed for:

- Visitors travelling to Yaoundé
- Students
- Tourists
- Business travelers
- People relocating to Yaoundé
- Residents looking to discover new places

The application can later be extended to cover additional cities across Cameroon.

---

# Core Features

The current version of GlobeTrotter provides the following features.

## User Authentication

Users can:

- Register
- Login securely
- Store personal preferences

Authentication is based on JSON Web Tokens (JWT).

---

## Destinations

The platform maintains a catalogue of destinations.

Each destination may contain information such as:

- Name
- Description
- Category
- District
- Address
- GPS coordinates
- Images
- Opening hours
- Estimated cost
- Contact information
- Tags
- Average rating

Examples include:

- Restaurants
- Shopping centers
- Hotels
- Administrative offices
- Tourist attractions
- Entertainment venues
- Cultural sites

---

## Recommendations

Recommendations are generated according to the user's preferences.

For example:

A user interested in:

- Shopping
- Restaurants

will receive destinations matching these interests before other categories.

Future versions may also include:

- popularity
- ratings
- visitor trends
- seasonal events

---

## Itineraries

Users can create personal itineraries.

Each itinerary stores:

- title
- destinations
- travel dates
- notes

Future versions will also provide:

- estimated distance
- estimated travel time
- transportation suggestions
- estimated transportation cost
- Google Maps integration

---

# Future Vision

The current application represents Version 1 of GlobeTrotter.

The long-term vision includes:

- Google Maps integration
- Real-time navigation
- Geolocation
- Favorites
- Reviews
- Notifications
- AI-powered recommendations
- Administrative assistance
- Offline mode
- Analytics Dashboard
- Mobile application
- Multi-city support

---

# Technical Evolution

The project originally started as a simple monolithic Flask application.

During development, the architecture has progressively evolved toward a modern layered architecture including:

- Routes
- Services
- Repositories
- Shared Utilities
- Base Repository
- JSON Storage Layer

The next major milestone consists of transforming the backend into independent microservices while preserving the current business logic.

---

# Current Technologies

Backend

- Python
- Flask
- JWT Authentication
- JSON Storage

Architecture

- Repository Pattern
- Service Layer
- Clean Architecture principles

Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Axios

DevOps

- Git
- GitHub
- Docker (planned)
- Kubernetes (planned)

---

# Development Philosophy

The project follows several software engineering principles.

- Separation of Concerns
- Single Responsibility Principle
- Layered Architecture
- Repository Pattern
- Service Layer Pattern
- Reusable Components
- Maintainable Code
- Incremental Refactoring

Every major refactoring is performed through dedicated Git branches before being merged into the main branch.

---

# Current Status

At the current stage, the project includes:

- Authentication module
- Destination management
- Recommendation engine
- Itinerary management
- Repository Layer
- Service Layer
- Standardized API responses
- JWT Authentication
- Modular project organization

The backend is now ready for the next phase of development:

- Microservices Architecture
- Docker containerization
- Kubernetes deployment
- Cloud deployment
- Frontend integration

---

# Project Roadmap

Completed

- Monolithic Flask application
- Authentication refactoring
- Repository Layer implementation
- Service Layer implementation
- Standardized API responses

In Progress

- Documentation
- Microservices migration

Planned

- Docker
- API Gateway
- Kubernetes
- PostgreSQL
- CI/CD
- Monitoring
- Cloud Deployment

---

# Conclusion

GlobeTrotter is evolving from an educational monolithic application into a modern, scalable travel platform following industry best practices.

The project demonstrates the progressive adoption of professional software engineering concepts including layered architecture, repository pattern, service layer, API standardization and future migration toward a cloud-native microservices ecosystem.