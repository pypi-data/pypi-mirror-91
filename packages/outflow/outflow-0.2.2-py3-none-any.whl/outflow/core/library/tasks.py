# -*- coding: utf-8 -*-
import os
import pathlib
import tempfile
from subprocess import PIPE, STDOUT, Popen
from typing import Dict, Iterable, List, Union

from outflow.core.logging import logger
from outflow.core.target import Target
from outflow.core.tasks.task import Task


class PipelineArgs(Task):
    def __init__(self, *args, **kwargs):
        self.with_context = True
        super().__init__(*args, auto_outputs=False, **kwargs)

    def run(self):
        pipeline_args = {}
        self.outputs = {}

        # update target outputs and returned value using the pipeline args
        for key in vars(self.context.args):
            self.outputs.update({key: Target(name=key)})
            pipeline_args[key] = getattr(self.context.args, key)
        return pipeline_args


@Task.as_task(with_self=False)
def PopenTask(
    command: Union[str, List, pathlib.Path],
    use_system_shell: bool = False,
    env: Dict = {},
):
    """Wrapper task for subprocess.Popen

    With 'use_system_shell=True', if the 'command' argument is:
      - a string, it is executed directly through the system shell.
      - a list, the command element are passed to Popen as follow: Popen(['/bin/sh', '-c', command[0], command[1], ...]) (On a POSIX system)

    Args:
        command (Union[str, List, pathlib.Path]): a list of program arguments, a single string or path-like object
        use_system_shell (bool, optional): specifies whether to use the system shell to execute the command. If True, it is recommended to pass the command as a string rather than as a list. Defaults to False.
        env (Dict, optional): a mapping that defines the environment variables for the command. Defaults to {}.

    """
    current_env = os.environ.copy()
    current_env.update(env)
    process = Popen(command, shell=use_system_shell, env=current_env)
    process.wait()
    return_code = process.returncode
    if return_code:
        msg = f"Command failed with exit code {return_code}"
        raise Exception(msg)


@Task.as_task(with_self=False)
def ExecuteShellScripts(
    shell_scripts: Iterable[str],
    env=None,
    shell: Union[str, None] = None,
    encoding: str = "utf-8",
):
    """Execute a sequence of shell scripts in the same process

    Args:
        shell_scripts (Iterable[str]): sequence of plain text shell scripts
        env (Dict, optional): a mapping that defines the environment variables for the command. Defaults to {}.
        shell (str, optional): the shell used to execute the scripts. Defaults to 'bash'.
        encoding (str, optional): the file encoding. Defaults to 'utf-8'.

    Raises:
        Exception: raise for non-zero return code
    """
    if env is None:
        env = {}
    tmp = tempfile.NamedTemporaryFile(prefix="outflow_", delete=False)

    for script in shell_scripts:
        tmp.write(script.encode(encoding))
        tmp.write("\n".encode(encoding))
    tmp.flush()

    current_env = os.environ.copy()
    current_env.update(env)

    if shell is None:
        use_system_shell = True
        popen_args = tmp.name
    else:
        use_system_shell = False
        popen_args = [shell, tmp.name]

    tmp.close()

    os.chmod(tmp.name, 0o0700)

    with Popen(
        popen_args, stdout=PIPE, stderr=STDOUT, env=current_env, shell=use_system_shell
    ) as process:
        output, error = process.communicate()
        logger.debug(output)
        if error:
            logger.error(error)
        return_code = process.returncode
    os.remove(tmp.name)
    if return_code:
        msg = f"Command failed with exit code {return_code}"
        raise Exception(msg)
