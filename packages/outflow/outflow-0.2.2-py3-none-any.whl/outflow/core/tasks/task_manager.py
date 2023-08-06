# -*- coding: utf-8 -*-

from outflow.core.logging import logger
from outflow.core.target import TargetException
from outflow.core.results import Results


class TaskManager:
    """
    Manage task calls and store the result references
    """

    def __init__(self):
        # to avoid reprocessing, store a reference of each task result for each already visited graph node
        self.results = Results()

    def compute(self, workflow):

        workflow.scheduler = self

        # run through each task of the workflow to gather task result references
        try:
            for task in workflow:
                self.add(task)
        except RecursionError:
            raise Exception("There is a cycle in the dependency graph")

    def add(self, task):
        """Store the reference of the task result dict

        Args:
            task ([type]): [description]
        """
        if task.id in self.results:
            # avoid reprocessing already visited graph nodes
            return

        # create a dictionary to store the reference to the task inputs
        task_inputs = {}

        # loop over the task parents to get the task inputs
        for parent in task.parents:
            # ensure the parents result reference is already stored in the promises reference dict
            self.add(parent)

            # and loop over parents
            for output_key in parent.outputs:
                task_inputs[output_key] = self.results.get_item_reference(
                    parent.id, output_key
                )

        # check if the current task have been processed during previous steps
        if task.id in self.results:
            return

        # if not, store the reference of the task result dict
        logger.debug(f"Running task {task.name}")

        task_return_value = self.run(task, task_inputs)
        task_return_value = self.post_process(task, task_return_value)

        self.results._set(task.id, task_return_value)

        # repeat the process with task child
        for child in task.children:
            self.add(child)

    def run(self, task, task_inputs):
        return task(**task_inputs)

    def post_process(self, task, task_return_value):
        post_processed = task_return_value
        if not isinstance(task_return_value, dict):
            if len(task.outputs) > 1:
                raise TargetException(
                    f"Task {task.name} must return a dictionary since it has defined more than one output target"
                )
            elif len(task.outputs) == 1:
                post_processed = {
                    next(iter(task.outputs)): task_return_value
                }  # get first and only item in dictionary task.outputs

        return post_processed
