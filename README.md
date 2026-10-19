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

- **Priority sorting — `Scheduler.sort_tasks()`**: Orders tasks by priority
  (high, medium, low), then by shorter duration. It sorts a copy and leaves the
  source list unchanged.
- **Chronological sorting — `Scheduler.sort_tasks_by_time()`**: Orders tasks by
  scheduled start time and places tasks without a start time at the end.
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

## Demo Walkthrough

### What you can do in the Streamlit app

- Set the owner's name and available care time.
- Add multiple pets and choose each pet's species.
- Add tasks to a selected pet with a description, duration, frequency, priority, and optional scheduled start time.
- Browse tasks in a table, filter by pet and completion status, and see tasks ordered by scheduled time. Unscheduled tasks appear after timed tasks.
- Mark an unfinished task complete. Daily and weekly tasks create a new occurrence with the next due date.
- Generate a time-limited plan and see conflict warnings for overlapping scheduled task intervals.

### Example workflow

1. Run `streamlit run app.py` and enter the owner's available care time.
2. Use **Add a Pet** to add a dog named Mochi and a cat named Miso.
3. Use **Schedule a Task** to add Mochi's 25-minute morning walk at 8:00 and Miso's 20-minute playtime at 8:00, plus other care tasks.
4. Review the task table. Use the status and pet filters to narrow the displayed tasks; the scheduler reports that the walk and playtime overlap.
5. Select **Generate schedule** to see incomplete tasks prioritized by priority and duration and fitted within the available time. Use a task's **Mark complete** button to complete it; a daily or weekly task will get a fresh occurrence.

### CLI example

Run `python main.py` to see sorting, filtering, the conflict warning, and the generated time-limited plan:

```text
Tasks sorted by priority, then duration:
- Breakfast (10 min, high, incomplete)
- Morning walk (25 min, high, incomplete)
- Playtime (20 min, medium, incomplete)
- Brush coat (5 min, low, complete)

Incomplete tasks:
- Morning walk
- Playtime
- Breakfast

Tasks for Miso:
- Playtime
- Breakfast

Schedule conflict check:
Warning: Morning walk for Mochi (08:00-08:25) overlaps with Playtime for Miso (08:00-08:20).

Today's Schedule
Owner: Jordan | Available time: 50 minutes
- Miso (cat): Breakfast (10 min, high priority)
- Mochi (dog): Morning walk (25 min, high priority)
```

### Testing PawPal+

```
=================== test session starts ===================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\gmasg\Downloads\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 16 items                                         

test_pawpal_system.py ..............                 [ 87%]
tests\test_pawpal.py ..                              [100%]

=================== 16 passed in 0.06s ====================
```



**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
