from datetime import date, time, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_scheduler_collects_tasks_from_every_pet() -> None:
    owner = Owner("Jordan", available_minutes=30)
    dog = Pet("Mochi", "dog", [Task("Walk", 20, priority="high")])
    cat = Pet("Miso", "cat", [Task("Feed", 10, priority="medium")])
    owner.add_pet(dog)
    owner.add_pet(cat)

    plan = Scheduler(owner).generate_plan()

    assert [task.description for task in plan] == ["Walk", "Feed"]
    assert owner.get_all_tasks() == dog.tasks + cat.tasks


def test_scheduler_skips_completed_tasks_and_respects_available_time() -> None:
    owner = Owner(
        "Jordan",
        available_minutes=15,
        pets=[
            Pet(
                "Mochi",
                "dog",
                [
                    Task("Completed walk", 5, completed=True),
                    Task("Long grooming", 20, priority="high"),
                    Task("Feed", 10, priority="medium"),
                    Task("Brush", 5, priority="low"),
                ],
            )
        ],
    )
    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert [task.description for task in plan] == ["Feed", "Brush"]
    explanation = scheduler.explain_plan()
    assert "Completed walk" not in explanation
    assert "Long grooming" in explanation
    assert "Excluded 1 completed task(s)" in explanation


def test_pet_can_edit_task_details() -> None:
    task = Task("Medication", 2, frequency="daily", priority="high")
    pet = Pet("Mochi", "dog", [task])

    pet.edit_task(
        "Medication",
        duration_minutes=3,
        frequency="twice daily",
        priority="medium",
    )

    assert (task.duration_minutes, task.frequency, task.priority) == (
        3,
        "twice daily",
        "medium",
    )


def test_task_requires_positive_duration() -> None:
    with pytest.raises(ValueError, match="at least 1 minute"):
        Task("Walk", 0)


def test_scheduler_sorts_tasks_by_priority_then_duration() -> None:
    owner = Owner(
        "Jordan",
        available_minutes=60,
        pets=[
            Pet(
                "Mochi",
                "dog",
                [
                    Task("Low priority", 5, priority="low"),
                    Task("Long high priority", 20, priority="high"),
                    Task("Short high priority", 10, priority="high"),
                ],
            )
        ],
    )

    sorted_tasks = Scheduler(owner).sort_tasks()

    assert [task.description for task in sorted_tasks] == [
        "Short high priority",
        "Long high priority",
        "Low priority",
    ]


def test_scheduler_sorts_tasks_in_chronological_order() -> None:
    late_task = Task("Evening feed", 10, scheduled_time=time(18, 0))
    early_task = Task("Morning walk", 20, scheduled_time=time(7, 30))
    unscheduled_task = Task("Grooming", 15)
    owner = Owner(
        "Jordan",
        available_minutes=60,
        pets=[Pet("Mochi", "dog", [late_task, unscheduled_task, early_task])],
    )

    sorted_tasks = Scheduler(owner).sort_tasks_by_time()

    assert sorted_tasks == [early_task, late_task, unscheduled_task]


def test_scheduler_filters_by_completion_status_and_pet_name() -> None:
    completed_task = Task("Completed walk", 20, completed=True)
    open_task = Task("Open walk", 15)
    cat_task = Task("Cat playtime", 10)
    owner = Owner(
        "Jordan",
        available_minutes=60,
        pets=[
            Pet("Mochi", "dog", [completed_task, open_task]),
            Pet("Miso", "cat", [cat_task]),
        ],
    )
    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks(completed=True) == [completed_task]
    assert scheduler.filter_tasks(completed=False) == [open_task, cat_task]
    assert scheduler.filter_tasks(pet_name="mIsO") == [cat_task]
    assert scheduler.filter_tasks(completed=False, pet_name="MOCHI") == [open_task]


def test_completing_daily_task_adds_next_occurrence() -> None:
    today = date(2026, 10, 18)
    task = Task("Medication", 2, frequency="daily")
    pet = Pet("Mochi", "dog", [task])

    next_occurrence = pet.mark_task_complete(task, completed_on=today)

    assert task.completed is True
    assert len(pet.tasks) == 2
    assert next_occurrence is pet.tasks[1]
    assert next_occurrence is not task
    assert next_occurrence.completed is False
    assert next_occurrence.due_date == today + timedelta(days=1)


def test_completing_weekly_task_adds_occurrence_one_week_later() -> None:
    today = date(2026, 10, 18)
    task = Task("Nail trim", 15, frequency="weekly")
    owner = Owner("Jordan", 60, [Pet("Mochi", "dog", [task])])

    next_occurrence = Scheduler(owner).mark_task_complete(task, completed_on=today)

    assert next_occurrence is not None
    assert next_occurrence.due_date == today + timedelta(days=7)
    assert owner.pets[0].tasks == [task, next_occurrence]


def test_completing_nonrecurring_task_does_not_create_another() -> None:
    task = Task("One-time vet visit", 30, frequency="once")
    pet = Pet("Mochi", "dog", [task])

    next_occurrence = pet.mark_task_complete(task, completed_on=date(2026, 10, 18))

    assert next_occurrence is None
    assert pet.tasks == [task]
    assert task.completed is True


def test_completing_task_twice_does_not_duplicate_occurrence() -> None:
    task = Task("Walk", 20, frequency="daily")
    pet = Pet("Mochi", "dog", [task])
    pet.mark_task_complete(task, completed_on=date(2026, 10, 18))

    next_occurrence = pet.mark_task_complete(task, completed_on=date(2026, 10, 18))

    assert next_occurrence is None
    assert len(pet.tasks) == 2


def test_scheduler_warns_when_tasks_for_different_pets_overlap() -> None:
    dog = Pet(
        "Mochi",
        "dog",
        [Task("Morning walk", 30, scheduled_time=time(8, 0))],
    )
    cat = Pet(
        "Miso",
        "cat",
        [Task("Breakfast", 15, scheduled_time=time(8, 15))],
    )
    scheduler = Scheduler(Owner("Jordan", 60, [dog, cat]))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Warning:" in warnings[0]
    assert "Morning walk for Mochi" in warnings[0]
    assert "Breakfast for Miso" in warnings[0]
    assert "08:15-08:30" in warnings[0]


def test_scheduler_warns_when_two_tasks_have_the_same_start_time() -> None:
    pet = Pet(
        "Mochi",
        "dog",
        [
            Task("Walk", 30, scheduled_time=time(8, 0)),
            Task("Breakfast", 15, scheduled_time=time(8, 0)),
        ],
    )

    warnings = Scheduler(Owner("Jordan", 60, [pet])).detect_conflicts()

    assert len(warnings) == 1
    assert "Walk for Mochi" in warnings[0]
    assert "Breakfast for Mochi" in warnings[0]


def test_scheduler_does_not_warn_for_nonoverlapping_or_completed_tasks() -> None:
    pet = Pet(
        "Mochi",
        "dog",
        [
            Task("Walk", 30, scheduled_time=time(8, 0)),
            Task("Breakfast", 15, scheduled_time=time(8, 30)),
            Task("Completed grooming", 30, completed=True, scheduled_time=time(8, 0)),
        ],
    )
    scheduler = Scheduler(Owner("Jordan", 60, [pet]))

    assert scheduler.detect_conflicts() == []
