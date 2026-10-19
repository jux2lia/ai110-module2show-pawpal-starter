# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

    My UML design has four classes:
        1. An Owner has one or more Pets
        2. Each Pet has a list of Tasks
        3. And lastly a Scheduler that takes in the pets and tasks to build a daily plan

- What classes did you include, and what responsibilities did you assign to each?
    Owner: Stores the owner's name, how many minutes they have to care for their pet, and their pets.
    Pets: Stores the pet's name, species and its care tasks
    Task: Represents one care activity, like walk or feed. It stores title, duration, priority and if it's done or not.

**b. Design changes**

- Did your design change during implementation?
    Yes.

- If yes, describe at least one change and why you made it.
    I made the Scheduler use the Owner rather than a single Pet. The Owner's get_all_tasks() method lets the scheduler consider tasks for every pet, which is necessary for a household with multiple pets. I also added task frequency and made the scheduler skip completed tasks and tasks that do not fit the owner's available time.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    It considers the owner's available minutes, each task's priority and duration, and whether a task is already completed. It can also filter by pet and detect overlaps between tasks that have scheduled start times.

- How did you decide which constraints mattered most?
    I prioritized high-priority care first, then used shorter duration to order tasks with equal priority. 

**b. Tradeoffs**

- The conflict checker compares each pair of scheduled, incomplete tasks and
  checks their full time intervals, not just whether their start times match.
  This catches partial overlaps, but comparing pairs takes O(n²) time as the
  number of scheduled tasks grows.
- I considered using Python's `itertools.combinations` to produce each pair.
  That is concise and avoids making list slices, but the explicit nested loop
  makes it easier for me to follow how each pair is checked. Pet-care schedules
  are small, so I kept the more direct version; its extra work is reasonable
  for this scenario.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI to turn my brainstormed UML into Python dataclasses, implement scheduling and recurring-task behavior, connect the classes to the Streamlit UI, and write tests and documentation.
- What kinds of prompts or questions were most helpful?
    Specific prompts that named the expected behavior were most helpful, such asasking for a scheduler that gathers tasks from every pet, skips completed tasks, and respects the owner's available time. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    When the AI agent overcomplicated the mmd.
- How did you evaluate or verify what the AI suggested?
    Through getting the AI to test check itself.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
 I tested task completion and adding a task to a pet, collecting tasks from multiple pets, editing task details, sorting by priority/duration and by scheduled time, and filtering by completion status or pet name. I also tested that the scheduler respects the owner's time limit, warns about overlapping scheduled tasks, and creates the next daily or weekly task occurrence when a recurring task is completed.
- Why were these tests important?
    These tests check the core behaviors the app depends on: task state changes, multi-pet scheduling, correct ordering and filtering, and time/conflict handling.
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


**b. Confidence**

- How confident are you that your scheduler works correctly?
    Confidence level: 4
- What edge cases would you test next if you had more time?
    If I had more time, I would test tasks scheduled across midnight, tasks that start exactly when another ends, and schedules with no tasks or zero available minutes.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I'm most satisfied with my usage of my helper AI Agent while completing this project

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would make the Streamlit interface support editing and deleting pets and tasks, and let users set each task's scheduled time with a clearer time picker. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    I learned that clear class responsibilities make it easier to extend a system. AI was most useful when I
    gave it specific requirements and then checked the result with tests and by running the app.
