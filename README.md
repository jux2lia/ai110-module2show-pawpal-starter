# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

```
# Today's Schedule
# Owner: Jordan | Available time: 45 minutes
# - Mochi (dog): Breakfast (10 min, high priority)
# - Mochi (dog): Morning walk (25 min, high priority)
```


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
================== test session starts ==================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\gmasg\Downloads\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 6 items                                        

test_pawpal_system.py ....                         [ 66%]
tests\test_pawpal.py ..                            [100%]

=================== 6 passed in 0.05s ===================
```

## 📐 Smarter Scheduling

PawPal+ includes these scheduling behaviors:

- **Sorting — `Scheduler.sort_tasks()`**: Orders tasks by priority (high, medium,
  low), then by shorter duration. It sorts a copy and leaves the source list
  unchanged.
- **Filtering — `Scheduler.filter_tasks()`**: Selects tasks by completion
  status, pet name, or both. Pet-name matching ignores capitalization.
- **Conflict detection — `Scheduler.detect_conflicts()`**: Compares scheduled
  time intervals for incomplete tasks and returns warning messages for
  overlaps, including overlaps across different pets. Tasks without a scheduled
  start time are ignored; conflicts do not stop the program.
- **Recurring tasks — `Task.mark_complete()`, `Pet.mark_task_complete()`, and
  `Scheduler.mark_task_complete()`**: Completing a daily or weekly task creates
  a fresh, incomplete task due one or seven days after the completion date. The
  Pet and Scheduler methods append it to the pet's task list; the scheduler
  method also invalidates its cached plan.
- **Time-limited plan — `Scheduler.generate_plan()`**: Builds a plan from all
  pets' incomplete tasks, ordered by priority and duration, fitting tasks within
  the owner's available minutes and recording tasks that do not fit.

## 📸 Demo Walkthrough

### Implementation summary

PawPal+ models care activities as Task dataclasses, including a description, duration, frequency, priority, completion status, due date, and optional scheduled start time. The Scheduler can warn when scheduled intervals overlap. When a daily or weekly task is marked complete, its Pet keeps the completed task and adds a new task due one or seven days after completion. Each Pet stores its own tasks, while an Owner manages multiple pets and provides get_all_tasks() to collect their tasks together. The Scheduler uses that owner-wide task list to skip completed tasks, order remaining tasks by priority and then duration, and fit as many as possible into the owner's available minutes.

### Run the demo

1. Create the owner with the amount of time available for pet care.
2. Add the owner's pets and give each pet its care tasks.
3. Create a Scheduler for the owner; it retrieves tasks from every pet through Owner.get_all_tasks()
4. Generate the plan. The scheduler prioritizes high-priority tasks, sorts ties by shorter duration, and skips tasks that do not fit the remaining time.
5. Run python main.py to print today's schedule, including the pet associated with each selected task, and a warning if scheduled tasks overlap.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
