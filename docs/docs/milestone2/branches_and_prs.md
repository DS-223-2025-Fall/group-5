# Branches & Pull Request Workflow (Milestone 2)

This document summarizes how the team uses Git branches and pull requests in Milestone 2.

## Branch Naming

For this milestone, each role uses a dedicated branch:

- `db` – database-related work
- `back` – backend-related work
- `front` – frontend-related work
- `ds` – data science–related work

Each branch is created from the main project branch.

## Workflow

1. Developer creates their role-specific branch (e.g. `db`, `back`, `front`, `ds`).
2. Developer commits and pushes their changes to the corresponding branch.
3. A pull request (PR) is opened from that branch into the main branch.
4. The PM reviews the PR:
   - Checks that the Milestone 2 task is completed.
   - Ensures code structure and naming are consistent.
5. After review, the PR is approved and merged.

## Purpose

- Keeps work separated by responsibility (DB, backend, frontend, DS).
- Makes code review easier for the PM.
- Reduces the risk of conflicts on the main branch.
- Documents progress per role for Milestone 2.
