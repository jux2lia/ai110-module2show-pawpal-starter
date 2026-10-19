from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str = "daily"
    priority: str = "medium"
    completed: bool = False
    due_date: date = field(default_factory=date.today)
    scheduled_time: time | None = None

    def __post_init__(self) -> None:
        """Validate the task's description, duration, frequency, and priority."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if self.duration_minutes < 1:
            raise ValueError("Task duration must be at least 1 minute.")
        if not self.frequency.strip():
            raise ValueError("Task frequency cannot be empty.")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("Task priority must be low, medium, or high.")

    @property
    def title(self) -> str:
        """Return the task description as its title."""
        return self.description

    def mark_complete(self, completed_on: date | None = None) -> Task | None:
        """Complete this task and create its next occurrence for daily or weekly frequency.

        The next due date is calculated from ``completed_on`` or today's date.
        Returns ``None`` for an already completed or non-recurring task.
        """
        if self.completed:
            return None
        self.completed = True
        interval_days = {"daily": 1, "weekly": 7}.get(
            self.frequency.strip().casefold()
        )
        if interval_days is None:
            return None

        next_due_date = (completed_on or date.today()) + timedelta(days=interval_days)
        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            due_date=next_due_date,
            scheduled_time=self.scheduled_time,
        )


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate that the pet has a name and species."""
        if not self.name.strip():
            raise ValueError("Pet name cannot be empty.")
        if not self.species.strip():
            raise ValueError("Pet species cannot be empty.")

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def mark_task_complete(
        self, task: Task, completed_on: date | None = None
    ) -> Task | None:
        """Complete this pet's task and append its next occurrence when recurring.

        Raises ``ValueError`` if the task does not belong to this pet.
        """
        if not any(existing is task for existing in self.tasks):
            raise ValueError(f"Task {task.description!r} does not belong to {self.name}.")
        next_occurrence = task.mark_complete(completed_on)
        if next_occurrence is not None:
            self.add_task(next_occurrence)
        return next_occurrence

    def edit_task(
        self,
        description: str,
        duration_minutes: int | None = None,
        frequency: str | None = None,
        priority: str | None = None,
    ) -> None:
        """Update the matching task's supplied details."""
        for task in self.tasks:
            if task.description == description:
                if duration_minutes is not None:
                    if duration_minutes < 1:
                        raise ValueError("Task duration must be at least 1 minute.")
                if frequency is not None:
                    if not frequency.strip():
                        raise ValueError("Task frequency cannot be empty.")
                if priority is not None:
                    if priority not in {"low", "medium", "high"}:
                        raise ValueError("Task priority must be low, medium, or high.")
                if duration_minutes is not None:
                    task.duration_minutes = duration_minutes
                if frequency is not None:
                    task.frequency = frequency
                if priority is not None:
                    task.priority = priority
                return
        raise ValueError(f"No task found with description {description!r}.")


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the owner's name and available care time."""
        if not self.name.strip():
            raise ValueError("Owner name cannot be empty.")
        if self.available_minutes < 0:
            raise ValueError("Available minutes cannot be negative.")

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return the tasks belonging to all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    owner: Owner
    _plan: list[Task] = field(default_factory=list, init=False, repr=False)
    _omitted_tasks: list[Task] = field(default_factory=list, init=False, repr=False)
    _has_generated_plan: bool = field(default=False, init=False, repr=False)

    def sort_tasks(self, tasks: list[Task] | None = None) -> list[Task]:
        """Sort tasks by high-to-low priority, then shortest duration.

        Uses all owner tasks when ``tasks`` is omitted and leaves the input list
        unchanged.
        """
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        tasks_to_sort = self.owner.get_all_tasks() if tasks is None else tasks
        return sorted(
            tasks_to_sort,
            key=lambda task: (priority_rank[task.priority], task.duration_minutes),
        )

    def sort_tasks_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Sort scheduled tasks chronologically, placing unscheduled tasks last.

        Uses all owner tasks when ``tasks`` is omitted and leaves the input list
        unchanged.
        """
        tasks_to_sort = self.owner.get_all_tasks() if tasks is None else tasks
        return sorted(
            tasks_to_sort,
            key=lambda task: (
                task.scheduled_time is None,
                task.scheduled_time or time.max,
            ),
        )

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter owner tasks by completion status, pet name, or both.

        Pet names are compared without regard to case. An omitted criterion is
        not used to restrict the result.
        """
        if pet_name is None:
            matching_tasks = self.owner.get_all_tasks()
        else:
            normalized_name = pet_name.strip().casefold()
            matching_tasks = [
                task
                for pet in self.owner.pets
                if pet.name.strip().casefold() == normalized_name
                for task in pet.tasks
            ]
        if completed is not None:
            matching_tasks = [
                task for task in matching_tasks if task.completed is completed
            ]
        return matching_tasks

    def mark_task_complete(
        self, task: Task, completed_on: date | None = None
    ) -> Task | None:
        """Complete an owner's task and add its next occurrence when recurring.

        The scheduler's cached plan is cleared. Raises ``ValueError`` if the task
        does not belong to one of the owner's pets.
        """
        for pet in self.owner.pets:
            if any(existing is task for existing in pet.tasks):
                next_occurrence = pet.mark_task_complete(task, completed_on)
                self._has_generated_plan = False
                self._plan = []
                self._omitted_tasks = []
                return next_occurrence
        raise ValueError(f"Task {task.description!r} does not belong to this owner.")

    def detect_conflicts(self) -> list[str]:
        """Return warnings for overlaps between scheduled, incomplete task intervals.

        Tasks without a start time and completed tasks are ignored; the schedule
        is not changed when conflicts are found.
        """
        scheduled_tasks = [
            (pet, task)
            for pet in self.owner.pets
            for task in pet.tasks
            if task.scheduled_time is not None and not task.completed
        ]
        warnings: list[str] = []
        for index, (first_pet, first_task) in enumerate(scheduled_tasks):
            first_start = (
                first_task.scheduled_time.hour * 60
                + first_task.scheduled_time.minute
            )
            first_end = first_start + first_task.duration_minutes
            for second_pet, second_task in scheduled_tasks[index + 1 :]:
                second_start = (
                    second_task.scheduled_time.hour * 60
                    + second_task.scheduled_time.minute
                )
                second_end = second_start + second_task.duration_minutes
                overlaps = any(
                    first_start < second_end + day_offset
                    and second_start + day_offset < first_end
                    for day_offset in (-1440, 0, 1440)
                )
                if overlaps:
                    first_end_time = (first_end % 1440)
                    second_end_time = (second_end % 1440)
                    warnings.append(
                        f"Warning: {first_task.description} for {first_pet.name} "
                        f"({first_task.scheduled_time:%H:%M}-"
                        f"{first_end_time // 60:02d}:{first_end_time % 60:02d}) "
                        f"overlaps with {second_task.description} for "
                        f"{second_pet.name} ({second_task.scheduled_time:%H:%M}-"
                        f"{second_end_time // 60:02d}:{second_end_time % 60:02d})."
                    )
        return warnings

    def generate_plan(self) -> list[Task]:
        """Prioritize incomplete owner tasks and fit them within available minutes.

        Tasks are considered by priority and duration; tasks that do not fit are
        skipped and recorded for the plan explanation.
        """
        outstanding_tasks = [
            task for task in self.owner.get_all_tasks() if not task.completed
        ]
        ordered_tasks = self.sort_tasks(outstanding_tasks)

        self._plan = []
        self._omitted_tasks = []
        self._has_generated_plan = True
        remaining_minutes = self.owner.available_minutes
        for task in ordered_tasks:
            if task.duration_minutes <= remaining_minutes:
                self._plan.append(task)
                remaining_minutes -= task.duration_minutes
            else:
                self._omitted_tasks.append(task)

        return list(self._plan)

    def explain_plan(self) -> str:
        """Describe the generated plan and any tasks left out."""
        if not self._has_generated_plan:
            return "No schedule has been generated yet."

        lines = [
            f"Daily plan for {self.owner.name} "
            f"({self.owner.available_minutes} minutes available):"
        ]
        if self._plan:
            for task in self._plan:
                lines.append(
                    f"- {task.description} ({task.duration_minutes} min, "
                    f"{task.frequency}, {task.priority} priority)"
                )
        else:
            lines.append("- No incomplete tasks fit the available time.")

        completed_count = sum(
            task.completed for task in self.owner.get_all_tasks()
        )
        if completed_count:
            lines.append(f"- Excluded {completed_count} completed task(s).")
        if self._omitted_tasks:
            omitted = ", ".join(task.description for task in self._omitted_tasks)
            lines.append(f"- Omitted for lack of time: {omitted}.")
        lines.append(
            "Tasks are ordered by priority (high to low), then shorter duration; "
            "tasks that do not fit are skipped."
        )
        return "\n".join(lines)
