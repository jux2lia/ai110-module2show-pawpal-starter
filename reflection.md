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
- How did you decide which constraints mattered most?

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
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
