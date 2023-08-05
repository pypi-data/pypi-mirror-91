#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from . import utils


def _can_express_norm(nbits, dtype):
    '''Can express normalized integers?'''
    return nbits <= (1 + np.finfo(dtype).nmant)


def encode_fp_to_uint(x, *, nbits=None):
    '''Encode floating-points to unsigned integers.

    Args:
        x: The type should be `np.float`, or an array in `np.float`.
        nbits: The number of bits to use.

    Returns:
        The resulting unsigned integers.

    Examples:
        >>> fp = np.float32(1.)
        >>> enc = encode_fp_to_uint(fp, nbits=20)

        >>> fp = np.array([0., 0.5, 1.], dtype=np.float32)
        >>> enc = encode_fp_to_uint(fp, nbits=20)

        >>> fp = np.array([[0., 0.5, 1.], [1., 0.5, 0.]], dtype=np.float32)
        >>> enc = encode_fp_to_uint(fp, nbits=20)
    '''
    assert (x.dtype.kind == 'f'), \
        '`dtype` of the argument `x` must be floating point types.'

    dtype = np.dtype('uint' + x.dtype.name[5:])
    max_nbits = dtype.itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (0 < nbits <= max_nbits), '`nbits` value is out of range.'

    return x.view(dtype) >> dtype.type(max_nbits - nbits)


def decode_uint_to_fp(x, *, nbits=None):
    '''Decode unsigned integers to floating-points.

    Args:
        x: The type should be `np.uint`, or an array in `np.uint`.
        nbits: The number of bits to use.

    Returns:
        The resulting floating-points.

    Examples:
        >>> fp = np.float32(1.)
        >>> enc = encode_fp_to_uint(fp, nbits=20)
        >>> dec = decode_uint_to_fp(enc, nbits=20)

        >>> fp = np.array([0., 0.5, 1.], dtype=np.float32)
        >>> enc = encode_fp_to_uint(fp, nbits=20)
        >>> dec = decode_uint_to_fp(enc, nbits=20)

        >>> fp = np.array([[0., 0.5, 1.], [1., 0.5, 0.]], dtype=np.float32)
        >>> enc = encode_fp_to_uint(fp, nbits=20)
        >>> dec = decode_uint_to_fp(enc, nbits=20)
    '''
    assert (x.dtype.kind == 'u'), \
        '`dtype` of the argument `x` must be unsigned integer types.'

    max_nbits = x.itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (0 < nbits <= max_nbits), '`nbits` value is out of range.'

    dtype = np.dtype('float' + x.dtype.name[4:])
    return (x << x.dtype.type(max_nbits - nbits)).view(dtype)


def encode_fp_to_std_unorm(x, *, dtype=np.uint8, nbits=None):
    '''Encode floating-points to unsigned normalized integers.

    Args:
        x: The type should be `np.float`, or an array in `np.float`.
        dtype: The type should be `np.uint`.
        nbits: The number of bits to use.

    Returns:
        The resulting unsigned normalized integers.

    Examples:
        >>> fp = np.float32(1.)
        >>> enc = encode_fp_to_std_unorm(fp, dtype=np.uint16, nbits=16)

        >>> fp = np.array([0., 0.5, 1.], dtype=np.float32)
        >>> enc = encode_fp_to_std_unorm(fp, dtype=np.uint16, nbits=16)

        >>> fp = np.array([[0., 0.5, 1.], [1., 0.5, 0.]], dtype=np.float32)
        >>> enc = encode_fp_to_std_unorm(fp, dtype=np.uint16, nbits=16)
    '''
    assert (x.dtype.kind == 'f'), \
        '`dtype` of the argument `x` must be floating point types.'
    assert (dtype().dtype.kind == 'u'), \
        '`dtype` of the argument `dtype` must be unsigned integer types.'

    max_nbits = dtype().itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (0 < nbits <= max_nbits), '`nbits` value is out of range.'
    assert _can_express_norm(nbits, x.dtype), \
        'Can\'t be expressed with the specified number of bits.'

    max_uint = dtype(np.iinfo(dtype).max) >> dtype(max_nbits - nbits)

    # Avoids memory allocation when the result is an array.
    temp = x * x.dtype.type(max_uint)
    out = temp if isinstance(temp, np.ndarray) else None

    return dtype(utils.rint(temp, out=out))


def decode_std_unorm_to_fp(x, *, dtype=np.float32, nbits=None):
    '''Decode unsigned normalized integers to floating-points.

    Args:
        x: The type should be `np.uint`, or an array in `np.uint`.
        dtype: The type should be `np.float`.
        nbits: The number of bits to use.

    Returns:
        The resulting floating-points.

    Examples:
        >>> fp = np.float32(1.)
        >>> enc = encode_fp_to_std_unorm(fp, dtype=np.uint16, nbits=16)
        >>> dec = decode_std_unorm_to_fp(enc, dtype=np.float32, nbits=16)

        >>> fp = np.array([0., 0.5, 1.], dtype=np.float32)
        >>> enc = encode_fp_to_std_unorm(fp, dtype=np.uint16, nbits=16)
        >>> dec = decode_std_unorm_to_fp(enc, dtype=np.float32, nbits=16)

        >>> fp = np.array([[0., 0.5, 1.], [1., 0.5, 0.]], dtype=np.float32)
        >>> enc = encode_fp_to_std_unorm(fp, dtype=np.uint16, nbits=16)
        >>> dec = decode_std_unorm_to_fp(enc, dtype=np.float32, nbits=16)
    '''
    assert (x.dtype.kind == 'u'), \
        '`dtype` of the argument `x` must be unsigned integer types.'
    assert (dtype().dtype.kind == 'f'), \
        '`dtype` of the argument `dtype` must be floating point types.'

    max_nbits = x.itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (0 < nbits <= max_nbits), '`nbits` value is out of range.'
    assert _can_express_norm(nbits, dtype), \
        'Can\'t be expressed with the specified number of bits.'

    max_uint = x.dtype.type(np.iinfo(x.dtype).max) >> x.dtype.type(max_nbits - nbits)
    # result = dtype(x) / dtype(max_uint)
    result = dtype(x)
    result /= dtype(max_uint)
    return result


def encode_fp_to_std_snorm(x, *, dtype=np.uint8, nbits=None):
    '''Encode floating-points to signed normalized integers.

    Args:
        x: The type should be `np.float`, or an array in `np.float`.
        dtype: The type should be `np.uint`.
        nbits: The number of bits to use.

    Returns:
        The resulting unsigned normalized integers.

    Examples:
        >>> fp = np.float32(-1.)
        >>> enc = encode_fp_to_std_snorm(fp, dtype=np.uint16, nbits=16)

        >>> fp = np.array([-1.0, -0.5, 0., 0.5, 1.], dtype=np.float32)
        >>> enc = encode_fp_to_std_snorm(fp, dtype=np.uint16, nbits=16)

        >>> fp = np.array([[-1.0, -0.5, 0., 0.5, 1.], [1.0, 0.5, 0., -0.5, -1.]], dtype=np.float32)
        >>> enc = encode_fp_to_std_snorm(fp, dtype=np.uint16, nbits=16)
    '''
    assert (x.dtype.kind == 'f'), \
        '`dtype` of the argument `x` must be floating point types.'
    assert (dtype().dtype.kind == 'u'), \
        '`dtype` of the argument `dtype` must be unsigned integer types.'

    max_nbits = dtype().itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (1 < nbits <= max_nbits), '`nbits` value is out of range.'
    assert _can_express_norm(nbits-1, x.dtype), \
        'Can\'t be expressed with the specified number of bits.'

    # (enc << dtype(1)) | np.signbit(x)
    result = encode_fp_to_std_unorm(np.absolute(x), dtype=dtype, nbits=nbits-1)
    result <<= dtype(1)
    result |= np.signbit(x)
    return result


def decode_std_snorm_to_fp(x, *, dtype=np.float32, nbits=None):
    '''Decode signed normalized integers to floating-points.

    Args:
        x: The type should be `np.uint`, or an array in `np.uint`.
        dtype: The type should be `np.float`.
        nbits: The number of bits to use.

    Returns:
        The resulting floating-points.

    Examples:
        >>> fp = np.float32(-1.)
        >>> enc = encode_fp_to_std_snorm(fp, dtype=np.uint16, nbits=16)
        >>> dec = decode_std_snorm_to_fp(enc, dtype=np.float32, nbits=16)

        >>> fp = np.array([-1.0, -0.5, 0., 0.5, 1.], dtype=np.float32)
        >>> enc = encode_fp_to_std_snorm(fp, dtype=np.uint16, nbits=16)
        >>> dec = decode_std_snorm_to_fp(enc, dtype=np.float32, nbits=16)

        >>> fp = np.array([[-1.0, -0.5, 0., 0.5, 1.], [1.0, 0.5, 0., -0.5, -1.]], dtype=np.float32)
        >>> enc = encode_fp_to_std_snorm(fp, dtype=np.uint16, nbits=16)
        >>> dec = decode_std_snorm_to_fp(enc, dtype=np.float32, nbits=16)
    '''
    assert (x.dtype.kind == 'u'), \
        '`dtype` of the argument `x` must be unsigned integer types.'
    assert (dtype().dtype.kind == 'f'), \
        '`dtype` of the argument `dtype` must be floating point types.'

    max_nbits = x.itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (1 < nbits <= max_nbits), '`nbits` value is out of range.'
    assert _can_express_norm(nbits-1, dtype), \
        'Can\'t be expressed with the specified number of bits.'

    # sign = dtype(x & x.dtype.type(0x1)) * dtype(-2.) + dtype(1.)
    sign = dtype(x & x.dtype.type(0x1))
    sign *= dtype(-2.)
    sign += dtype(1.)
    # result = dec * sign
    result = decode_std_unorm_to_fp(x >> x.dtype.type(1), dtype=dtype, nbits=nbits - 1)
    result *= sign
    return result


def encode_fp_to_ogl_snorm(x, *, dtype=np.uint8, nbits=None):
    '''Encode floating-points to signed normalized integers.

    Args:
        x: The type should be `np.float`, or an array in `np.float`.
        dtype: The type should be `np.uint`.
        nbits: The number of bits to use.

    Returns:
        The resulting unsigned normalized integers.
    '''
    assert (x.dtype.kind == 'f'), \
        '`dtype` of the argument `x` must be floating point types.'
    assert (dtype().dtype.kind == 'u'), \
        '`dtype` of the argument `dtype` must be unsigned integer types.'

    max_nbits = dtype().itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (1 < nbits <= max_nbits), '`nbits` value is out of range.'
    assert _can_express_norm(nbits-1, x.dtype), \
        'Can\'t be expressed with the specified number of bits.'

    mask = dtype(np.iinfo(dtype).max) >> dtype(max_nbits - nbits)
    max_uint = dtype((1 << (nbits-1)) - 1)

    # Avoids memory allocation when the result is an array.
    temp = x * x.dtype.type(max_uint)
    out = temp if isinstance(temp, np.ndarray) else None

    # result = dtype(utils.rint(temp, out=out)) & mask
    result = dtype(utils.rint(temp, out=out))
    result &= mask
    return result


def decode_ogl_snorm_to_fp(x, *, dtype=np.float32, nbits=None):
    '''Decode signed normalized integers to floating-points.

    Args:
        x: The type should be `np.uint`, or an array in `np.uint`.
        dtype: The type should be `np.float`.
        nbits: The number of bits to use.

    Returns:
        The resulting floating-points.
    '''
    assert (x.dtype.kind == 'u'), \
        '`dtype` of the argument `x` must be unsigned integer types.'
    assert (dtype().dtype.kind == 'f'), \
        '`dtype` of the argument `dtype` must be floating point types.'

    max_nbits = x.itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (1 < nbits <= max_nbits), '`nbits` value is out of range.'
    assert _can_express_norm(nbits-1, dtype), \
        'Can\'t be expressed with the specified number of bits.'

    # sign = x >> x.dtype.type(nbits-1) * mask
    # uint_x = sign | x
    mask = np.invert(x.dtype.type(np.iinfo(x.dtype).max) >> x.dtype.type(max_nbits - nbits))
    uint_x = x >> x.dtype.type(nbits-1)
    uint_x *= mask
    uint_x |= x

    # Avoids memory allocation when the result is an array.
    # temp = dtype(temp.view(x.dtype.name[1:])) / dtype(max_uint)
    max_uint = x.dtype.type((1 << (nbits-1)) - 1)
    temp = dtype(uint_x.view(x.dtype.name[1:]))
    temp /= dtype(max_uint)
    out = temp if isinstance(temp, np.ndarray) else None

    return np.maximum(temp, dtype(-1.), out=out)


def encode_fp_to_d3d_snorm(x, *, dtype=np.uint8, nbits=None):
    '''Encode floating-points to signed normalized integers.

    Args:
        x: The type should be `np.float`, or an array in `np.float`.
        dtype: The type should be `np.uint`.
        nbits: The number of bits to use.

    Returns:
        The resulting unsigned normalized integers.
    '''
    assert (x.dtype.kind == 'f'), \
        '`dtype` of the argument `x` must be floating point types.'
    assert (dtype().dtype.kind == 'u'), \
        '`dtype` of the argument `dtype` must be unsigned integer types.'

    max_nbits = dtype().itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (1 < nbits <= max_nbits), '`nbits` value is out of range.'
    assert _can_express_norm(nbits-1, x.dtype), \
        'Can\'t be expressed with the specified number of bits.'

    mask = dtype(np.iinfo(dtype).max) >> dtype(max_nbits - nbits)
    max_uint = dtype((1 << (nbits-1)) - 1)

    # Avoids memory allocation when the result is an array.
    temp = x * x.dtype.type(max_uint)
    out = temp if isinstance(temp, np.ndarray) else None

    # result = dtype(utils.rint(temp, out=out)) & mask
    result = dtype(utils.rint(temp, out=out))
    result &= mask
    return result


def decode_d3d_snorm_to_fp(x, *, dtype=np.float32, nbits=None):
    '''Decode signed normalized integers to floating-points.

    Args:
        x: The type should be `np.uint`, or an array in `np.uint`.
        dtype: The type should be `np.float`.
        nbits: The number of bits to use.

    Returns:
        The resulting floating-points.
    '''
    assert (x.dtype.kind == 'u'), \
        '`dtype` of the argument `x` must be unsigned integer types.'
    assert (dtype().dtype.kind == 'f'), \
        '`dtype` of the argument `dtype` must be floating point types.'

    max_nbits = x.itemsize * 8
    if nbits is None:
        nbits = max_nbits
    assert (1 < nbits <= max_nbits), '`nbits` value is out of range.'
    assert _can_express_norm(nbits-1, dtype), \
        'Can\'t be expressed with the specified number of bits.'

    # sign = x >> x.dtype.type(nbits-1) * mask
    # uint_x = sign | x
    mask = np.invert(x.dtype.type(np.iinfo(x.dtype).max) >> x.dtype.type(max_nbits - nbits))
    uint_x = x >> x.dtype.type(nbits-1)
    uint_x *= mask
    uint_x |= x

    # Avoids memory allocation when the result is an array.
    # temp = dtype(temp.view(x.dtype.name[1:])) / dtype(max_uint)
    max_uint = x.dtype.type((1 << (nbits-1)) - 1)
    temp = dtype(uint_x.view(x.dtype.name[1:]))
    temp /= dtype(max_uint)
    out = temp if isinstance(temp, np.ndarray) else None

    return np.maximum(temp, dtype(-1.), out=out)
