#  Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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

from __future__ import print_function

import unittest
import numpy as np
import sys
sys.path.append("..")
from op_test import OpTest
from op_test_xpu import XPUOpTest
import paddle
import paddle.fluid.core as core

paddle.enable_static()


class XPUBaseTestCase(XPUOpTest):
    def initTestCase(self):
        self.dims = (3, 4)
        self.dtype = 'float32'
        self.axis = 1

    def setUp(self):
        self.initTestCase()
        self.__class__.op_type = 'arg_max'
        self.__class__.use_xpu = True
        np.random.seed(2021)
        self.x = (np.random.random(self.dims)).astype(self.dtype)
        self.inputs = {'X': self.x}
        self.attrs = {'axis': self.axis, 'use_xpu': True}
        if self.op_type == "arg_min":
            self.outputs = {'Out': np.argmin(self.x, axis=self.axis)}
        else:
            self.outputs = {'Out': np.argmax(self.x, axis=self.axis)}

    def test_check_output(self):
        if paddle.is_compiled_with_xpu():
            place = paddle.XPUPlace(0)
            self.check_output_with_place(place)


# test argmax, dtype: float32
class TestArgMaxFloat32Case1(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (3, 4, 5)
        self.dtype = 'float32'
        self.axis = -1


class TestArgMaxFloat32Case2(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (3, 4, 5)
        self.dtype = 'float32'
        self.axis = 0


class TestArgMaxFloat32Case3(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (3, 4, 5)
        self.dtype = 'float32'
        self.axis = 1


class TestArgMaxFloat32Case4(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (3, 4, 5)
        self.dtype = 'float32'
        self.axis = 2


class TestArgMaxFloat32Case5(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (3, 4)
        self.dtype = 'float32'
        self.axis = -1


class TestArgMaxFloat32Case6(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (3, 4)
        self.dtype = 'float32'
        self.axis = 0


class TestArgMaxFloat32Case7(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (3, 4)
        self.dtype = 'float32'
        self.axis = 1


class TestArgMaxFloat32Case8(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (1, )
        self.dtype = 'float32'
        self.axis = 0


class TestArgMaxFloat32Case9(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (2, )
        self.dtype = 'float32'
        self.axis = 0


class TestArgMaxFloat32Case10(XPUBaseTestCase):
    def initTestCase(self):
        self.op_type = 'arg_max'
        self.dims = (3, )
        self.dtype = 'float32'
        self.axis = 0


class TestArgMaxAPI(unittest.TestCase):
    def initTestCase(self):
        self.dims = (3, 4, 5)
        self.dtype = 'float32'
        self.axis = 0

    def setUp(self):
        self.initTestCase()
        self.__class__.use_Xpu = True
        self.place = [paddle.XPUPlace(0)]

    def test_dygraph_api(self):
        def run(place):
            paddle.disable_static(place)
            np.random.seed(2021)
            numpy_input = (np.random.random(self.dims)).astype(self.dtype)
            tensor_input = paddle.to_tensor(numpy_input)
            numpy_output = np.argmax(numpy_input, axis=self.axis)
            paddle_output = paddle.argmax(tensor_input, axis=self.axis)
            self.assertEqual(
                np.allclose(numpy_output, paddle_output.numpy()), True)
            paddle.enable_static()

        for place in self.place:
            run(place)


class TestArgMaxAPI_2(unittest.TestCase):
    def initTestCase(self):
        self.dims = (3, 4, 5)
        self.dtype = 'float32'
        self.axis = 0
        self.keep_dims = True

    def setUp(self):
        self.initTestCase()
        self.__class__.use_xpu = True
        self.place = [paddle.XPUPlace(0)]

    def test_dygraph_api(self):
        def run(place):
            paddle.disable_static(place)
            np.random.seed(2021)
            numpy_input = (np.random.random(self.dims)).astype(self.dtype)
            tensor_input = paddle.to_tensor(numpy_input)
            numpy_output = np.argmax(
                numpy_input, axis=self.axis).reshape(1, 4, 5)
            paddle_output = paddle.argmax(
                tensor_input, axis=self.axis, keepdim=self.keep_dims)
            self.assertEqual(
                np.allclose(numpy_output, paddle_output.numpy()), True)
            self.assertEqual(numpy_output.shape, paddle_output.numpy().shape)
            paddle.enable_static()

        for place in self.place:
            run(place)


if __name__ == '__main__':
    unittest.main()
