from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", available_minutes=50)

    mochi = Pet(name="Mochi", species="dog")
    miso = Pet(name="Miso", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(miso)

    # Add tasks in low-to-high priority order to demonstrate scheduler sorting.
    mochi.add_task(Task("Brush coat", 5, priority="low"))
    miso.add_task(
        Task(
            "Playtime",
            20,
            priority="medium",
            scheduled_time=time(8, 0),
        )
    )
    mochi.add_task(
        Task(
            "Morning walk",
            25,
            priority="high",
            scheduled_time=time(8, 0),
        )
    )
    miso.add_task(Task("Breakfast", 10, priority="high"))
    mochi.tasks[0].mark_complete()

    scheduler = Scheduler(owner)

    print("Tasks sorted by priority, then duration:")
    for task in scheduler.sort_tasks():
        status = "complete" if task.completed else "incomplete"
        print(
            f"- {task.description} ({task.duration_minutes} min, "
            f"{task.priority}, {status})"
        )

    print("\nIncomplete tasks:")
    for task in scheduler.filter_tasks(completed=False):
        print(f"- {task.description}")

    print("\nTasks for Miso:")
    for task in scheduler.filter_tasks(pet_name="Miso"):
        print(f"- {task.description}")

    print("\nSchedule conflict check:")
    conflict_warnings = scheduler.detect_conflicts()
    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No schedule conflicts detected.")

    print("\nToday's Schedule")
    print(f"Owner: {owner.name} | Available time: {owner.available_minutes} minutes")
    plan = scheduler.generate_plan()
    for task in plan:
        pet = next(
            pet for pet in owner.pets if any(existing is task for existing in pet.tasks)
        )
        print(
            f"- {pet.name} ({pet.species}): {task.description} "
            f"({task.duration_minutes} min, {task.priority} priority)"
        )
    if not plan:
        print("No incomplete tasks fit the available time.")


if __name__ == "__main__":
    main()