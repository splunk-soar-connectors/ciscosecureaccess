# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from importlib import import_module

from .core import app

_ACTION_MODULES = (
    "destination_lists",
    "devices",
    "domains",
    "identities",
    "make_request",
    "rules",
    "swg",
    "vpn",
)


def _register_actions() -> None:
    package = __package__ or "src"
    for module_name in _ACTION_MODULES:
        import_module(f".actions.{module_name}", package=package)


_register_actions()


if __name__ == "__main__":
    app.cli()
