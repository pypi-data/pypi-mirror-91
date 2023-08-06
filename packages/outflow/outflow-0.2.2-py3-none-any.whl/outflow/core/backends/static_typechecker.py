# -*- coding: utf-8 -*-
from .backend import Backend as DefaultBackend
from outflow.core.logging import logger
from ..tasks import TaskManager
from ..tasks.task import Task
from ...ray.tasks import MapTask


class TypecheckerError(TypeError):
    pass


class StaticTypecheckerTaskManager(TaskManager):
    def run(self, task: Task, task_inputs):
        for parent_task in task.parents:
            for input_target in task.inputs.values():
                if input_target.name not in parent_task.outputs:
                    raise TypecheckerError(
                        f"Task {task.name} did not get all expected inputs: expected {task.inputs.keys()}, got "
                        f"{parent_task.outputs.keys()}"
                    )
                parent_output_target_type = parent_task.outputs[input_target.name].type
                if input_target.type != parent_output_target_type:
                    raise TypeError(
                        f"Task {task.name} got an inputs with the wrong type: expected target {input_target.name} to "
                        f"be of type {input_target.type}, but is of type {parent_output_target_type}"
                    )

        if isinstance(task, MapTask):
            temp_backend = Backend()
            temp_backend.run(task_list=[task.end])

    def post_process(self, task, task_return_value):
        return {key: None for key in task.outputs.keys()}


class Backend(DefaultBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, *, task_list):
        logger.debug(
            f"Run pipeline with backend '{self}' and with pipeline context '{self.pipeline_context}'"
        )
        task_manager = StaticTypecheckerTaskManager()

        for task in task_list:
            task.workflow.set_context(self.pipeline_context)
            task_manager.compute(task.workflow)

        logger.info("Your workflow looks all right !")
        return [task_manager.results.resolve(task.id) for task in task_list]
