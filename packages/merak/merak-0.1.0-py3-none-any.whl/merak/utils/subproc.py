# Copyright 2021 (David) Siu-Kei Muk. All Rights Reserved.
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
# ==============================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import subprocess
import threading


def run(*popenargs, **kwargs):
  logger = logging.getLogger(__name__)

  kwargs["stdout"] = subprocess.PIPE
  kwargs["stderr"] = subprocess.PIPE
  kwargs["text"] = True

  with subprocess.Popen(*popenargs, **kwargs) as process:
    debug_log_piper = LogPiper(logger.debug, process.stdout)
    warning_log_piper = LogPiper(logger.warning, process.stderr)
    debug_log_piper.start()
    warning_log_piper.start()

    retcode = process.wait()

  return subprocess.CompletedProcess(process.args, retcode)


class LogPiper(threading.Thread):
  def __init__(self, log_fn, pipe):
    super(LogPiper, self).__init__()
    self._log_fn = log_fn
    self._pipe = pipe

  def run(self):
    for line in iter(self._pipe.readline, ""):
      self._log_fn(line[:-1])
