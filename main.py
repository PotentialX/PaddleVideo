# copyright (c) 2020 PaddlePaddle Authors. All Rights Reserve.
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
import paddle
import argparse
from paddlevideo.utils import get_config
from paddlevideo.loader.builder import build_dataloader, build_dataset
from paddlevideo.modeling.builder import build_model
from paddlevideo.tasks import train_model
def parse_args():
    parser = argparse.ArgumentParser("PaddleVideo train script")
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        default='configs/example.yaml',
        help='config file path')
    parser.add_argument(
        '-o',
        '--override',
        action='append',
        default=[],
        help='config options to be overridden')
    parser.add_argument(
        '--validate',
        action='store_true',
        help='whether to evaluate the checkpoint during training')
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='use data parallel or not')
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='random seed')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    cfg = get_config(args.config, overrides=args.override)
    # use cfg.model or cfg?
    if args.parallel:
        paddle.distributed.init_parallel_env()

    model = build_model(cfg.MODEL)

    #NOTE: To debug dataloader or wanna inspect your data, please try to print(dataset) here.
    #    for i in dataset[0]:
    #        logger.error(i)

    dataset = [build_dataset((cfg.DATASET.train, cfg.PIPELINE.train))]
    #if args.validate:
    #    dataset.append(build_dataset((cfg.DATASET.valid, cfg.PIPELINE.valid)))
     
    train_model(model,
		dataset, 
		cfg,
                parallel=args.parallel,
                validate=args.validate)


if __name__ == '__main__':
    main()
    #spawn(train, args=(args, ), nprocs=4)