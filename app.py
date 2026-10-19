from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.write("Plan pet-care tasks around your available time.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=45)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
if "schedule" not in st.session_state:
    st.session_state.schedule = []

owner: Owner = st.session_state.owner
owner_name = st.text_input("Owner name", value=owner.name)
available_minutes = st.number_input(
    "Available care time (minutes)",
    min_value=0,
    value=owner.available_minutes,
    step=5,
)
if owner_name != owner.name or available_minutes != owner.available_minutes:
    st.session_state.scheduler = None
    st.session_state.schedule = []
owner.name = owner_name
owner.available_minutes = available_minutes

st.divider()
st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name.strip():
        st.error("Enter a name for the pet.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species))
        st.session_state.scheduler = None
        st.session_state.schedule = []
        st.success(f"Added {pet_name.strip()}!")

st.divider()
st.subheader("Schedule a Task")
if not owner.pets:
    st.info("Add a pet before scheduling a task.")
else:
    with st.form("add_task_form"):
        pet_index = st.selectbox(
            "Pet",
            options=range(len(owner.pets)),
            format_func=lambda index: (
                f"{owner.pets[index].name} ({owner.pets[index].species})"
            ),
        )
        task_description = st.text_input("Task description")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        frequency = st.text_input("Frequency", value="daily")
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        has_scheduled_time = st.checkbox("Set a scheduled start time")
        scheduled_time = (
            st.time_input("Start time", value=time(8, 0))
            if has_scheduled_time
            else None
        )
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if not task_description.strip():
            st.error("Enter a description for the task.")
        elif not frequency.strip():
            st.error("Enter how often the task should happen.")
        else:
            task = Task(
                description=task_description.strip(),
                duration_minutes=int(duration),
                frequency=frequency.strip(),
                priority=priority,
                scheduled_time=scheduled_time,
            )
            owner.pets[pet_index].add_task(task)
            st.session_state.scheduler = None
            st.session_state.schedule = []
            st.success(f"Added task for {owner.pets[pet_index].name}.")

st.divider()
st.subheader("Your Pets and Tasks")
if not owner.pets:
    st.info("No pets have been added yet.")
else:
    for pet_index, pet in enumerate(owner.pets):
        st.markdown(f"**{pet.name}** ({pet.species})")
        if pet.tasks:
            st.table(
                [
                    {
                        "Task": task.description,
                        "Duration (minutes)": task.duration_minutes,
                        "Frequency": task.frequency,
                        "Due date": task.due_date.isoformat(),
                        "Start time": (
                            task.scheduled_time.strftime("%H:%M")
                            if task.scheduled_time is not None
                            else "Not scheduled"
                        ),
                        "Priority": task.priority,
                        "Completed": task.completed,
                    }
                    for task in pet.tasks
                ]
            )
        else:
            st.caption("No tasks yet.")
        for task_index, task in enumerate(pet.tasks):
            if not task.completed and st.button(
                f"Mark complete: {task.description}",
                key=f"complete-{pet_index}-{task_index}",
            ):
                next_occurrence = Scheduler(owner).mark_task_complete(task)
                st.session_state.scheduler = None
                st.session_state.schedule = []
                if next_occurrence is not None:
                    st.success(
                        f"Completed {task.description}. Next occurrence is due "
                        f"{next_occurrence.due_date.isoformat()}."
                    )
                else:
                    st.success(f"Completed {task.description}.")

st.divider()
st.subheader("Today's Schedule")
for warning in Scheduler(owner).detect_conflicts():
    st.warning(warning)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    st.session_state.schedule = scheduler.generate_plan()
    st.session_state.scheduler = scheduler

scheduler = st.session_state.scheduler
if scheduler is not None:
    st.write(scheduler.explain_plan())
    for task in st.session_state.schedule:
        pet = next(
            pet for pet in owner.pets if any(existing is task for existing in pet.tasks)
        )
        st.markdown(
            f"- **{pet.name}**: {task.description} "
            f"({task.duration_minutes} min, {task.priority} priority)"
        )
