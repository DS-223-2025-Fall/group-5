# Services & Architecture (Milestone 2)

This document describes the technical services created in Milestone 2 and how they work together.

## Database Service

- Database service/container created.
- Database and required tables implemented based on the ERD.
- Data loaded from flat files into the database.
- Helper DB methods implemented for later usage (for backend and DS).

## Backend Service

- Backend service/container created.
- Dummy CRUD endpoints (GET, POST, PUT, DELETE) implemented.
- Backend connects to the database using the helper methods.
- These endpoints will later be used by the frontend and DS service.

## Frontend Service

- Frontend service/container created.
- Initial UI skeleton implemented (basic layout and navigation).
- The frontend will later consume backend endpoints once the full API is ready.

## Data Science (DS) Service

- DS service/container created.
- Configured to access data either via DB helper methods or backend API.
- Used in this milestone to experiment with simple baseline models.
