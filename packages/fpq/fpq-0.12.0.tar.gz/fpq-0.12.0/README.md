[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/Hasenpfote/fpq/blob/master/LICENSE)
[![Build Status](https://travis-ci.com/Hasenpfote/fpq.svg?branch=master)](https://travis-ci.com/Hasenpfote/fpq)
[![PyPI version](https://badge.fury.io/py/fpq.svg)](https://badge.fury.io/py/fpq)
[![Pyversions](https://img.shields.io/pypi/pyversions/fpq.svg?style=flat)](https://img.shields.io/pypi/pyversions/fpq.svg?style=flat)

fpq
===

## About
This package provides modules for manipulating floating point numbers quantization using NumPy.

## Feature
* Supports multidimensional arrays.
* Supports encoding and decoding between 64/32/16-bits floating point numbers and N-bits unsigned normalized integers.
* Supports encoding and decoding between 64/32/16-bits floating point numbers and N-bits signed normalized integers.
* Supports encoding and decoding between 3d-vectors and N-bits unsigned integers.
* Supports encoding and decoding between Quaternions and N-bits unsigned integers.

## Compatibility
fpq works with Python 3.4 or higher.

## Dependencies
* NumPy
* Numba

## Installation
```
pip install fpq
```

## Usage
encoding and decoding between 32-bits floating point numbers and 5-bits unsigned normalized integers.
```python
>>> import numpy as np
>>> from fpq.fp import *
>>> fp = np.array([0., 0.25, 1.], dtype=np.float32)
>>> enc = encode_fp_to_std_unorm(fp, dtype=np.uint8, nbits=5)
>>> enc
array([ 0,  8, 31], dtype=uint8)
>>> dec = decode_std_unorm_to_fp(enc, dtype=np.float32, nbits=5)
>>> dec
array([0.       , 0.2580645, 1.       ], dtype=float32)
```

encoding and decoding between 32-bits floating point numbers and 5-bits signed normalized integers.
```python
>>> import numpy as np
>>> from fpq.fp import *
>>> fp = np.array([-1., -0.25, -0., 0., 0.25, 1.], dtype=np.float32)
>>> enc = encode_fp_to_std_snorm(fp, dtype=np.uint8, nbits=5)
>>> enc
array([31,  9,  1,  0,  8, 30], dtype=uint8)
>>> dec = decode_std_snorm_to_fp(enc, dtype=np.float32, nbits=5)
>>> dec
array([-1.        , -0.26666668, -0.        ,  0.        ,  0.26666668,
        1.        ], dtype=float32)
>>> enc = encode_fp_to_ogl_snorm(fp, dtype=np.uint8, nbits=5)
>>> enc
array([17, 28,  0,  0,  4, 15], dtype=uint8)
>>> dec = decode_ogl_snorm_to_fp(enc, dtype=np.float32, nbits=5)
>>> dec
array([-1.        , -0.26666668,  0.        ,  0.        ,  0.26666668,
        1.        ], dtype=float32)
```

encoding and decoding between 3d-vectors and 64-bits(2:20:20:22) unsigned integers.
```python
>>> import math
>>> import random
>>> import numpy as np
>>> from fpq.vector import *
>>> v = np.array([vec_random(norm=100.) for _ in range(3)], dtype=np.float64)
>>> v
array([[-54.70386501, -22.45578546, -52.18237577],
       [-85.46791152,  -5.69032986,   1.21334561],
       [ 16.02886205,   1.94634654, -30.35219431]])
>>> enc = encode_vec_to_uint(v, dtype=np.uint64, nbits=20)
>>> enc
array([ 1313110064653969262,   306332797892602581, 11373476070061802081],
      dtype=uint64)
>>> dec = decode_uint_to_vec(enc, dtype=np.float64, nbits=20)
>>> dec
array([[-54.69957531, -22.45404536, -52.17828412],
       [-85.4662517 ,  -5.69027392,   1.21334561],
       [ 16.02845595,   1.94632843, -30.3514349 ]])
```

encoding and decoding between Quaternions and 64-bits(2:20:20:20) unsigned integers.
```python
>>> import numpy as np
>>> from fpq.quaternion import *
>>> q = np.array([quat_random() for _ in range(3)], dtype=np.float64)
>>> q
array([[ 0.25679071, -0.15512517,  0.88804262,  0.34838917],
       [ 0.71399177,  0.05729705, -0.69728753, -0.02688697],
       [-0.66527338, -0.62596543, -0.40672262, -0.01246296]])
>>> enc = encode_quat_to_uint(q, dtype=np.uint64)
>>> enc
array([2724532880236077588,   93422189206870975, 1020620101889574962],
      dtype=uint64)
>>> dec = decode_uint_to_quat(enc, dtype=np.float64)
>>> dec
array([[ 0.25679011, -0.15512497,  0.88804308,  0.34838854],
       [ 0.71399243,  0.0572969 , -0.69728688, -0.02688637],
       [ 0.66527395,  0.62596484,  0.40672258,  0.01246335]])
```

[Here](https://github.com/Hasenpfote/fpq/tree/master/example) are a few examples.

## Documentation
For users, docs are now available at https://hasenpfote.github.io/fpq/.

## References and links
[D3D: Data Conversion Rules](https://msdn.microsoft.com/en-us/library/windows/desktop/dd607323(v=vs.85).aspx)
[OGL: Normalized Integer](https://www.khronos.org/opengl/wiki/Normalized_Integer)
[Vulkan: Fixed-Point Data Conversions](http://vulkan-spec-chunked.ahcox.com/ch02s08.html)

## License
This software is released under the MIT License, see LICENSE.
