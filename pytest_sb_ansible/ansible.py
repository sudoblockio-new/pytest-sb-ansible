import os
from typing import Any, Mapping

from ansible_runner import Runner, RunnerConfig


def run_playbook(
    playbook: str,
    *,
    project_dir: str,
    roles_path: str | None = None,
    inventory: str = "localhost,",
    extravars: Mapping[str, Any] | None = None,
    envvars: Mapping[str, str] | None = None,
    artifact_subdir: str = ".artifacts",
) -> None:
    rcfg = RunnerConfig(
        project_dir=project_dir,
        private_data_dir=project_dir,
        roles_path=roles_path or os.path.join(project_dir, "roles"),
        playbook=playbook,
        inventory=inventory,
        artifact_dir=os.path.join(project_dir, artifact_subdir),
        extravars=dict(extravars or {}),
        envvars=dict(envvars or {}),
    )
    rcfg.prepare()
    status, rc = Runner(config=rcfg).run()
    if not (status == "successful" and rc == 0):
        raise RuntimeError(f"play failed: status={status}, rc={rc}")


def run_playbook_on_host(
    hostname: str,
    port: int,
    user: str,
    identityfile: str,
    playbook: str,
    project_dir: str,
):
    ssh_vars = {
        "ansible_connection": "ssh",
        "ansible_host": hostname,
        "ansible_port": port,
        "ansible_user": user,
        "ansible_ssh_private_key_file": identityfile,
        "ansible_ssh_common_args": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null",
        "ansible_python_interpreter": "/usr/bin/python3",
    }

    run_playbook(
        playbook=playbook,
        project_dir=project_dir,
        roles_path=os.path.join(project_dir, "roles"),
        inventory="target,",
        extravars=ssh_vars,
    )
