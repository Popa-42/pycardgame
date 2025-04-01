# PyCardGame - A base library for creating card games in Python
# Copyright (C) 2025  Popa-42
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

from abc import ABC
from typing import (
    Any,
    overload,
    Generic,
    Iterator,
    List,
    Optional,
    Type,
    TypeVar,
)

from .base import GenericCard, GenericDeck

_RankT = TypeVar("_RankT")
_SuitT = TypeVar("_SuitT")
_CardT = TypeVar("_CardT", bound=GenericCard)  # type: ignore


