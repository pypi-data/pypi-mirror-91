"""Locally Connected Layer and Subsampling layer for 2D input"""
import torch
from torch import Tensor
from torch import nn
import torch.nn.functional as F
from torch.nn.modules.utils import _pair
from torch.nn import init
import math
from typing import Union, Tuple, Optional
from nntoolbox.vision.utils import compute_output_shape
from nntoolbox.vision.components import GlobalAveragePool


__all__ = ['LocallyConnected2D', 'Subsampling2D', 'CondConv2d']


class LocallyConnected2D(nn.Module):
    """
    Works similarly to Conv2d, but does not share weight. Much more memory intensive, and slower
    (due to suboptimal native pytorch implementation) (UNTESTED)

    Example usages:

        Yaniv Taigman et al. "DeepFace: Closing the Gap to Human-Level Performance in Face Verification"
        https://www.cs.toronto.edu/~ranzato/publications/taigman_cvpr14.pdf
    """
    def __init__(
            self, in_channels: int, out_channels: int, in_h: int, in_w: int,
            kernel_size: Union[int, Tuple[int, int]], stride: Union[int, Tuple[int, int]]=1,
            padding: Union[int, Tuple[int, int]]=0, dilation: Union[int, Tuple[int, int]]=1,
            groups: int=1,  bias: bool=True, padding_mode: str='zeros'
    ):
        super(LocallyConnected2D, self).__init__()
        if in_channels % groups != 0:
            raise ValueError('in_channels must be divisible by groups')
        if out_channels % groups != 0:
            raise ValueError('out_channels must be divisible by groups')
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size if isinstance(kernel_size, tuple) else _pair(kernel_size)
        self.stride = stride if isinstance(stride, tuple) else _pair(stride)
        self.padding = padding if isinstance(padding, tuple) else _pair(padding)
        self.dilation = dilation if isinstance(dilation, tuple) else _pair(dilation)
        self.groups = groups
        self.padding_mode = padding_mode
        self.in_h, self.in_w = in_h, in_w

        self.output_h, self.output_w = self.compute_output_shape(in_h, in_w)
        self.weight = nn.Parameter(torch.Tensor(
            out_channels, in_channels // groups,
            self.kernel_size[0], self.kernel_size[1], self.output_h, self.output_w)
        )
        if bias:
            self.bias = nn.Parameter(torch.Tensor(out_channels, self.output_h, self.output_w))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in)
            init.uniform_(self.bias, -bound, bound)

    def compute_output_shape(self, height: int, width: int) -> Tuple[int, int]:
        return (
            compute_output_shape(height, self.padding[0], self.kernel_size[0], self.dilation[0], self.stride[0]),
            compute_output_shape(width, self.padding[1], self.kernel_size[1], self.dilation[1], self.stride[1]),
        )

    def forward(self, input: Tensor) -> Tensor:
        assert input.shape[2] == self.in_h and input.shape[3] == self.in_w

        if self.padding_mode == 'circular':
            expanded_padding = [(self.padding[1] + 1) // 2, self.padding[1] // 2,
                                (self.padding[0] + 1) // 2, self.padding[0] // 2]
            input = F.pad(input, expanded_padding, mode='circular')
            padding = 0
        else:
            padding = self.padding
        input = F.unfold(
            input, kernel_size=self.kernel_size, dilation=self.dilation,
            padding=padding, stride=self.stride
        )
        output = (input.unsqueeze(1) * self.weight.view(
            1, self.out_channels, self.in_channels * self.kernel_size[0] * self.kernel_size[1], -1
        )).sum(2)
        output = output.view(-1, output.shape[1], self.output_h, self.output_w)
        if self.bias is not None:
            output = output + self.bias[None, :]
        return output


class Subsampling2D(nn.AvgPool2d):
    """
    For each feature map of input, subsample one patch at the time, sum the values
    and then perform a linear transformation. Use in LeNet. (UNTESTED)

    References:

        Yann Lecun et al. "Gradient-Based Learning Applied to Document Recognition."
        http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf
    """
    def __init__(
            self, in_channels: int, kernel_size: Union[int, Tuple[int, int]]=2,
            stride: Union[int, Tuple[int, int]]=2, padding: Union[int, Tuple[int, int]]=0, bias: bool=True,
            trainable: bool=True, ceil_mode: bool=False, count_include_pad: bool=True
    ):
        super().__init__(kernel_size, stride, padding, ceil_mode, count_include_pad)
        self.weight = nn.Parameter(torch.ones(in_channels), requires_grad=trainable)
        if bias:
            self.bias = nn.Parameter(torch.zeros(in_channels), requires_grad=trainable)
        else:
            self.register_parameter('bias', None)

    def forward(self, input: Tensor) -> Tensor:
        output = super().forward(input)
        output = output * self.weight[None, :, None, None]
        if self.bias is not None: output = output + self.bias[None, :, None, None]
        return output


class CondConv2d(nn.Conv2d):
    """
    Conditionally Parameterized Convolution Layer.

    References:

        Brandon Yang, Gabriel Bender, Quoc V. Le, Jiquan Ngiam.
        "CondConv: Conditionally Parameterized Convolutions for Efficient Inference."
        https://arxiv.org/abs/1904.04971

        Pytorch implementation of Conv2d
    """

    def __init__(
            self, num_experts: int, in_channels, out_channels, kernel_size, stride=1,
            padding=0, dilation=1, groups=1, bias=True, padding_mode='zeros'
    ):
        super().__init__(in_channels, out_channels, kernel_size, stride, padding, dilation, groups, bias, padding_mode)
        convs = [
            nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation, groups, bias, padding_mode)
            for _ in range(num_experts)
        ]
        self.weight = nn.Parameter(torch.stack([conv.weight for conv in convs], dim=0))
        if bias:
            self.bias = nn.Parameter(torch.stack([conv.bias for conv in convs], dim=0))
        else:
            self.bias = None
        self.routing_weight_fn = nn.Sequential(GlobalAveragePool(), nn.Linear(in_channels, num_experts), nn.Sigmoid())
        self.num_experts = num_experts

    def forward(self, input: Tensor) -> Tensor:
        if self.train and self.num_experts < 4:
            return self.branched_forward(input)
        else:
            return self.efficient_forward(input)

    def branched_forward(self, input: Tensor) -> Tensor:
        if self.padding_mode == 'circular':
            expanded_padding = ((self.padding[1] + 1) // 2, self.padding[1] // 2,
                                (self.padding[0] + 1) // 2, self.padding[0] // 2)

        routing_weights = self.routing_weight_fn(input).transpose(0, 1)
        outputs = []
        for e in range(self.num_experts):
            weight = self.weight[e]
            if self.bias is None:
                bias = self.bias
            else:
                bias = self.bias[e]

            if self.padding_mode == 'circular':
                output = F.conv2d(F.pad(input, expanded_padding, mode='circular'),
                                  weight, bias, self.stride,
                                  (0, 0), self.dilation, self.groups)
            else:
                output = F.conv2d(input, weight, bias, self.stride,
                                  self.padding, self.dilation, self.groups)

            outputs.append(output)

        return (torch.stack(outputs, dim=0) * routing_weights[:, :, None, None, None]).sum(0)

    def efficient_forward(self, input: Tensor) -> Tensor:
        if self.padding_mode == 'circular':
            expanded_padding = ((self.padding[1] + 1) // 2, self.padding[1] // 2,
                                (self.padding[0] + 1) // 2, self.padding[0] // 2)

        routing_weights = self.routing_weight_fn(input)
        outputs = []
        for i in range(len(input)):
            weight = (self.weight * routing_weights[i][:, None, None, None, None]).sum(0)
            if self.bias is None:
                bias = self.bias
            else:
                bias = (self.bias * routing_weights[i][:, None]).sum(0)

            if self.padding_mode == 'circular':
                output = F.conv2d(F.pad(input[i:i + 1], expanded_padding, mode='circular'),
                                  weight, bias, self.stride,
                                  (0, 0), self.dilation, self.groups)
            else:
                output = F.conv2d(input[i:i + 1], weight, bias, self.stride,
                                  self.padding, self.dilation, self.groups)

            outputs.append(output)

        return torch.cat(outputs, dim=0)

