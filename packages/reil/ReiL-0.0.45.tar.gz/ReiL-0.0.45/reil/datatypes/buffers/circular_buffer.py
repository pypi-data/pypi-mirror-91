# -*- coding: utf-8 -*-
'''
CircularBuffer class
====================

A `Buffer` that overflows!
'''

from typing import Dict, Tuple

from reil.datatypes.buffers import Buffer, T


class CircularBuffer(Buffer[T]):
    '''
    A `Buffer` that overflows.

    Extends `Buffer` class.
    '''
    _buffer_full = False

    def add(self, data: Dict[str, T]) -> None:
        '''
        Add a new item to the buffer.

        Arguments
        ---------
        data:
            A dictionary with the name of buffer queues as keys.

        Notes
        -----
        If the buffer is full, new items will be writen over the oldest one.
        '''
        try:
            super().add(data)
        except IndexError:
            self._buffer_full = True
            self._buffer_index = -1
            super().add(data)

        # the size does not change if buffer is full.
        self._count -= self._buffer_full

    def _pick_old(self, count: int) -> Dict[str, Tuple[T, ...]]:
        '''
        Return the oldest items in the buffer.

        Arguments
        ---------
        count:
            The number of items to return.
        '''
        if self._buffer_full:
            slice_pre = slice(self._buffer_index + 1,
                              self._buffer_index + count + 1)
            slice_post = slice(
                max(0, count - (self._buffer_size - self._buffer_index) + 1))
            return dict((name, tuple(
                buffer[slice_pre] +
                buffer[slice_post]))
                for name, buffer in self._buffer.items())
        else:
            return super()._pick_old(count)

    def _pick_recent(self, count: int) -> Dict[str, Tuple[T, ...]]:
        '''
        Return the most recent items in the buffer.

        Arguments
        ---------
        count:
            The number of items to return.
        '''
        if count - self._buffer_index <= 1 or not self._buffer_full:
            return super()._pick_recent(count)
        else:
            slice_pre = slice(-(count - self._buffer_index - 1), None)
            slice_post = slice(self._buffer_index + 1)
            return dict((name, tuple(
                buffer[slice_pre] +
                buffer[slice_post]))
                for name, buffer in self._buffer.items())

    def _pick_all(self) -> Dict[str, Tuple[T, ...]]:
        '''
        Return all items in the buffer.
        '''
        if self._buffer_full:
            slice_pre = slice(self._buffer_index + 1, None)
            slice_post = slice(self._buffer_index + 1)
            return dict((name, tuple(
                         buffer[slice_pre] +
                         buffer[slice_post]))
                        for name, buffer in self._buffer.items())
        else:
            return super()._pick_all()

    def reset(self) -> None:
        '''
        Reset the buffer.
        '''
        super().reset()
        self._buffer_full = False
