# Lint as: python3
# Copyright 2020 The Waymo Open Dataset Authors. All Rights Reserved.
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
# ==============================================================================*/
"""A simple example to generate a file that contains serialized Objects proto."""

from waymo_open_dataset import dataset_pb2
from waymo_open_dataset import label_pb2
from waymo_open_dataset.protos import metrics_pb2


def _create_pd_file_example():
  """Creates a prediction objects file."""
  objects = metrics_pb2.Objects() 

  o = metrics_pb2.Object()
  # 이후에 나오는 3개의 field는 예측을 수행하는 프레임 식별에 사용
  # raw data에서 제공한 값들과 field의 값들을 동일하게 설정할 것 - 그렇지 않을 경우 잘못된 것으로 간주될 수 있음
  o.context_name = ('context_name for the prediction. See Frame::context::name '
                    'in  dataset.proto.')
  # 예측에 대한 timestamp
  invalid_ts = -1
  o.frame_timestamp_micros = invalid_ts
  # 2D 대상의 검출 또는 추적 작업에만 필요한 것
  # 예측 대상을 카메라 이름으로 설정
  o.camera_name = dataset_pb2.CameraName.FRONT

  # box와 score(값)을 매칭
  box = label_pb2.Label.Box()
  box.center_x = 0
  box.center_y = 0
  box.center_z = 0
  box.length = 0
  box.width = 0
  box.height = 0
  box.heading = 0
  o.object.box.CopyFrom(box)
  # 0.0과 1.0 사이의 값이 되어야 함 - 그렇지 않을 경우 필터링을 거쳐 작은 점수로 변환(matrics 연산 속도 높이기 위해 필요)
  o.score = 0.5
  # 추적을 위해 각각의 추적될 sequence에 대해 설정되고, 또한 고유의 값을 가져야만 함
  o.object.id = 'unique object tracking ID'
  # type 올바르게 설정하기
  o.object.type = label_pb2.Label.TYPE_PEDESTRIAN

  objects.objects.append(o)

  # 합리적인 검출 위해서는 프레임 당 box의 수를 제한해야 함(합리적인 값 = 약 400) - box의 수가 많아질 경우 metrics 연산 속도 느려질 수 있음

  # 파일에 객체 작성
  f = open('/tmp/your_preds.bin', 'wb')
  f.write(objects.SerializeToString())
  f.close()


def main():
  _create_pd_file_example()


if __name__ == '__main__':
  main()
