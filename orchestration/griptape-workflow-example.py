# from https://docs.griptape.ai/latest/griptape-framework/structures/workflows/
from griptape.tasks import PromptTask
from griptape.structures import Workflow

workflow = Workflow()

def character_task(task_id, character_name) -> PromptTask:
    return PromptTask(
        "Based on the following world description create a character named {{ name }}:\n{{ parent_outputs['world'] }}",
        context={
            "name": character_name
        },
        id=task_id
    )

world_task = PromptTask(
    "Create a fictional world based on the following key words {{ keywords|join(', ') }}",
    context={
        "keywords": ["fantasy", "ocean", "tidal lock"]
    },
    id="world"
)
workflow.add_task(world_task)

story_task = PromptTask(
    "Based on the following description of the world and characters, write a short story:\n{{ parent_outputs['world'] }}\n{{ parent_outputs['scotty'] }}\n{{ parent_outputs['annie'] }}",
    id="story"
)
workflow.add_task(story_task)

character_task_1 = character_task("scotty", "Scotty")
character_task_2 = character_task("annie", "Annie")

# Note the preserve_relationship flag. This ensures that world_task remains a parent of
# story_task so its output can be referenced in the story_task prompt.
workflow.insert_tasks(world_task, [character_task_1, character_task_2], story_task, preserve_relationship=True)

workflow.run()