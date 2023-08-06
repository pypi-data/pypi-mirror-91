# -*- coding: utf-8 -*-
from typeguard import check_type
from typing import TypedDict
from outflow.core.logging import logger

from .base_task import BaseTask
from ..target import Target


class Task(BaseTask):
    def __init__(self, *args, auto_outputs=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.outputs and auto_outputs:
            # run automatic output detection if none were declared
            Target.output("__auto__")(self)

    def __call__(self, *args, **kwargs):
        super().__call__()

        self.resolve_remote_inputs(kwargs)

        return_value = self.run(
            **kwargs, **self.bind_kwargs, **self.parameterized_kwargs
        )

        if return_value is not None:
            # check the type of each output (type being Any if declared with __auto__)
            typed_dict = {}
            for output_target in self.outputs.values():
                typed_dict.update({output_target.name: output_target.type})

            check_type(
                "return_value", return_value, TypedDict("return_value", typed_dict)
            )

        return return_value

    def resolve_remote_inputs(self, task_kwargs):
        """Transform 'ray' ObjectIDs into Python object

        From main actor: get the object in the object store
        If remote: get in the remote object store and transfer by TCP
        """
        try:
            import ray

            for key, val in task_kwargs.items():
                if isinstance(val, ray._raylet.ObjectID):
                    task_kwargs[key] = ray.get(val)
        except ImportError:
            logger.debug(
                "The 'ray' package is not available, usage of remote objects is therefore impossible"
            )


task = Task.as_task
