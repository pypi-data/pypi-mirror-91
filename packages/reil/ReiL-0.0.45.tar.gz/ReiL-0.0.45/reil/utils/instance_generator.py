# -*- coding: utf-8 -*-
'''
InstanceGenerator class
=======================

`InstanceGenerator` takes any object derived form `ReilBase` and returns
an iterator.
'''

from __future__ import annotations

import os
import pathlib
from typing import Any, Callable, Generic, Tuple, TypeVar, Union

from reil import reilbase
from reil.datatypes.components import MockStatistic

T = TypeVar('T', bound=reilbase.ReilBase)


class InstanceGenerator(Generic[T], reilbase.ReilBase):
    '''
    Make any ReilBase object an iterable.

    The initializer accepts, among other arguments, an instance of an object to
    iterate, and `instance_counter_stops`, which is a tuple of the instance
    numbers where the instance generator should stop.
    '''

    def __init__(self,
                 object: T,
                 instance_counter_stops: Tuple[int] = (-1,),  # -1: infinite
                 first_instance_number: int = 0,
                 auto_rewind: bool = False,
                 save_instances: bool = False,
                 overwrite_instances: bool = False,
                 use_existing_instances: bool = True,
                 save_path: Union[pathlib.Path, str] = '',
                 filename_pattern: str = '{n:04}',
                 **kwargs: Any):
        '''
        Attributes
        ----------
        object:
            An instance of an object.

        instance_counter_stops:
            A tuple of the instance numbers where the instance
            generator should stop. A value of -1 means infinite.

        first_instance_number:
            The number of the first instance to be generated.

        auto_rewind:
            Whether to rewind after the generator hits the last stop.

        save_instances:
            Whether to save instances of the `object` or not.

        overwrite_instances:
            Whether to overwrite instances of the `object` or not.
            This flag is useful only if `save_instances` is set to `True`.

        use_existing_instances:
            Whether try to load instances before attempting to create them.

        save_path:
            The path where instances should be saved to/ loaded from.

        filename_pattern:
            A string that uses "n" as the instance number, and is
            used for saving and loading instances.
        '''
        super().__init__(**kwargs)

        self._object = object
        self._save_instances = save_instances
        self._use_existing_instances = use_existing_instances
        self._overwrite_instances = overwrite_instances
        self._save_path = save_path
        self._filename_pattern = filename_pattern

        self._auto_rewind = auto_rewind
        self._first_instance_number = first_instance_number
        self._instance_counter_stops = instance_counter_stops
        self._last_stop_index = len(self._instance_counter_stops) - 1

        self.is_finite = -1 not in instance_counter_stops and not auto_rewind
        self.statistic = MockStatistic(self._object)

        self.rewind()

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[int, T]:
        end = self._get_end()

        self._instance_counter += 1

        if self._stop_check(self._instance_counter, end):
            self._instance_counter -= 1
            self._stops_index += 1

            if self._stops_index <= self._last_stop_index:
                self._determine_stop_check()

            self._partially_terminated = True
            raise StopIteration

        else:
            self._partially_terminated = False
            self._generate_new_instance()

        return (self._instance_counter, self._object)

    def _get_end(self):
        try:
            end = self._instance_counter_stops[self._stops_index]
        except IndexError:
            if self._auto_rewind:
                self.rewind()
                end = self._instance_counter_stops[self._stops_index]
            else:
                raise StopIteration
        return end

    def _determine_stop_check(self):
        if self._instance_counter_stops[self._stops_index] == -1:
            self._stop_check: Callable[
                [int, int], bool] = lambda current, end: False
        else:
            self._stop_check: Callable[
                [int, int], bool] = lambda current, end: current >= end

    def _generate_new_instance(self):
        current_instance = self._filename_pattern.format(
                n=self._instance_counter)
        new_instance = True
        if self._use_existing_instances:
            try:
                self._object.load(path=self._save_path,
                                  filename=current_instance)
                new_instance = False
            except FileNotFoundError:
                self._object.reset()
        else:
            self._object.reset()

        self.statistic.set_object(self._object)

        if self._save_instances and new_instance:
            if (not self._overwrite_instances and
                    os.path.isfile(pathlib.Path(
                        self._save_path, f'{current_instance}.pkl'))):
                raise FileExistsError(
                        f'File {current_instance} already exists.')
            else:
                self._object.save(path=self._save_path,
                                  filename=current_instance)

    def rewind(self) -> None:
        '''
        Rewind the iterator object.
        '''
        self._instance_counter = self._first_instance_number - 1
        self._stops_index = 0
        self._partially_terminated = False
        self._determine_stop_check()

    def is_terminated(self, fully: bool = True) -> bool:
        if fully:
            return not self._auto_rewind and (self._stops_index >
                                              self._last_stop_index)
        else:
            return self._partially_terminated

    def __repr__(self) -> str:
        try:
            return (f'{self.__class__.__qualname__} '
                    f'-- {self._instance_counter} --> '
                    f'{self._object.__repr__()}')
        except AttributeError:
            return self.__class__.__qualname__
