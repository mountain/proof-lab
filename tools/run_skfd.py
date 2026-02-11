from __future__ import annotations

import importlib
import importlib.metadata
import runpy
import site
import sys
from typing import Any


def _patch_external_build_module_loading() -> None:
    try:
        discover: Any = importlib.import_module("skfd.driver.discover")
    except Exception:
        return

    def load_external_build_module(package_name: str):  # type: ignore[no-untyped-def]
        for candidate in (package_name, package_name.replace("-", "_")):
            try:
                return importlib.import_module(f"{candidate}.build")
            except ImportError:
                pass

        if package_name == "metamath-prelude":
            try:
                return importlib.import_module("prelude.build")
            except ImportError:
                return None

        if package_name == "metamath-logic":
            try:
                return importlib.import_module("logic.build")
            except ImportError:
                return None

        return None

    setattr(discover, "load_external_build_module", load_external_build_module)


def _parse_dist_requires(dist_name: str) -> list[str]:
    deps: list[str] = []
    try:
        dist = importlib.metadata.distribution(dist_name)
    except Exception:
        return deps

    for req in dist.requires or []:
        name = (
            req.split(">", 1)[0]
            .split("<", 1)[0]
            .split("=", 1)[0]
            .split(";", 1)[0]
            .strip()
        )
        if not name or name == "proof-scaffold":
            continue
        deps.append(name)
    return deps


def _patch_runner_external_deps() -> None:
    try:
        runner_mod: Any = importlib.import_module("skfd.driver.runner")
    except Exception:
        return

    DriverRunner = getattr(runner_mod, "DriverRunner", None)
    if DriverRunner is None:
        return

    orig = DriverRunner._resolve_dependency

    def _resolve_dependency(self, name: str):  # type: ignore[no-untyped-def]
        orig(self, name)

        if not hasattr(self, "_external_modules"):
            return

        if name not in getattr(self, "_external_modules", {}):
            return

        if self.deps_graph.get(name):
            return

        deps = _parse_dist_requires(name)
        self.deps_graph[name] = deps
        for dep in deps:
            orig(self, dep)

    DriverRunner._resolve_dependency = _resolve_dependency


def main() -> None:
    site.main()
    _patch_external_build_module_loading()
    _patch_runner_external_deps()
    sys.argv[0] = "skfd"
    runpy.run_module("skfd.cli", run_name="__main__")


if __name__ == "__main__":
    main()
