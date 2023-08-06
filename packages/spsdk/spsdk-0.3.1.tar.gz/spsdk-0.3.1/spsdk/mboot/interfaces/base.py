#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2019-2020 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Module for functionality shared accross all MBoot interfaces."""

from abc import ABC
from typing import Any


class Interface(ABC):
    """Base class for all Mboot Interface classes."""

    @property
    def is_opened(self) -> bool:
        """Indicates whether interface is open."""

    @property
    def need_data_split(self) -> bool:
        """Indicates whether device need to split data into smaller chunks."""
        return True

    def __init__(self, reopen: bool = False) -> None:
        """Initialize the Interface object.

        :param reopen: Reopen the interface after reset, defaults to False
        """
        self.reopen = reopen

    def open(self) -> None:
        """Open the interface."""

    def close(self) -> None:
        """Close the interface."""

    def read(self) -> Any:
        """Read data from the device."""

    def write(self, packet: Any) -> None:
        """Write a packet to the device."""

    def info(self) -> str:
        """Return string containing information about the interface."""
