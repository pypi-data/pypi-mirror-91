# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
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

"""Configuration definitions for multi-task training."""
from typing import Optional, Tuple

import dataclasses

from official.core import config_definitions as cfg
from official.modeling.hyperparams import base_config


@dataclasses.dataclass
class TaskRoutine(base_config.Config):
  task_name: str = ""
  task_config: cfg.TaskConfig = None
  mixing_steps: int = 1
  eval_steps: Optional[int] = None
  task_weight: Optional[float] = None


@dataclasses.dataclass
class MultiTaskConfig(base_config.Config):
  init_checkpoint: str = ""
  model: base_config.Config = None
  task_routines: Tuple[TaskRoutine, ...] = ()


@dataclasses.dataclass
class MultiEvalExperimentConfig(base_config.Config):
  """An experiment config for single-task training and multi-task evaluation.

  Attributes:
    task: the single-stream training task.
    eval_tasks: individual evaluation tasks.
    trainer: the trainer configuration.
    runtime: the runtime configuration.
  """
  task: cfg.TaskConfig = cfg.TaskConfig()
  eval_tasks: MultiTaskConfig = MultiTaskConfig()
  trainer: cfg.TrainerConfig = cfg.TrainerConfig()
  runtime: cfg.RuntimeConfig = cfg.RuntimeConfig()
