from __future__ import annotations

from skfd.api_v2 import BuildContextV2

from proof_lab.task_runner import build_registered_tasks


def build(ctx: BuildContextV2) -> None:
    build_registered_tasks(ctx)
