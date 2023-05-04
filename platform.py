# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import sys

from platformio.managers.platform import PlatformBase


IS_WINDOWS = sys.platform.startswith("win")

class Tqdfcore_watchosPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        board = variables.get("board")
        board_config = self.board_config(board)
        build_core = variables.get(
            "board_build.core", board_config.get("build.core", "arduino"))
        build_mcu = variables.get("board_build.mcu", board_config.get("build.mcu", ""))

        frameworks = variables.get("pioframework", [])
        if "arduino" in frameworks:
            self.packages["toolchain-gccarmnoneeabi"]["version"] = "~1.90201.0"
            self.packages["framework-cmsis"]["version"] = "~2.50700.0"
            self.packages["framework-cmsis"]["optional"] = False

            self.frameworks["arduino"]["package"] = "framework-tqdfcore-watchos"

        default_protocol = board_config.get("upload.protocol") or ""
        if variables.get("upload_protocol", default_protocol) == "dfu":
            self.packages["tool-dfuutil"]["optional"] = False

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        return board


