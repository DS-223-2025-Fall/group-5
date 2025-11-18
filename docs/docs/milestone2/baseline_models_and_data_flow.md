# Baseline Models & Data Flow (Milestone 2)

This document explains how data flows through the system in Milestone 2 and how simple baseline models are used.

## Data Flow

- Data is stored in the database created from the ERD.
- Flat files are loaded into the database using the DB service.
- The backend exposes CRUD endpoints to access and modify the data.
- The DS service accesses the data:
  - either directly through DB helper methods, or
  - via the backend CRUD endpoints (depending on the final design).

## Simulated Data (If Needed)

If the real data is not fully available or complete:

- Additional simulated data is generated to unblock development.
- The structure of the simulated data matches the target database schema.
- Simulated data is used only for testing the pipeline and baseline models and will later be replaced by real data.

## Baseline Models

- Simple baseline models are implemented to:
  - verify that the DS service can read data,
  - test the integration with the database/backend,
  - provide a first reference point for later, more complex models.

Examples of baseline approaches (depending on the final problem definition):

- Constant or average-based predictions.
- Very simple rules or heuristics.
- Minimal models used only to ensure the pipeline works end-to-end.

## Role in Later Milestones

These baseline models are not final.  
They are used to:

- Validate the infrastructure built in Milestone 2.
- Provide a comparison point for more advanced models to be developed in later milestones.
