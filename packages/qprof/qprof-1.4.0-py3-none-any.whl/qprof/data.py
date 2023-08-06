# ======================================================================
# Copyright TOTAL / CERFACS / LIRMM (09/2020)
# Contributor: Adrien Suau (<adrien.suau@cerfacs.fr>
#                           <adrien.suau@lirmm.fr>)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================

import typing as ty


class RoutineCallsData:
    """Represents the base call data.

    This class is "simply" a triplet of ints representing:
        1. A number of calls.
        2. A "self" time.
        3. A "subroutine" time.
    With these 3 numbers, it can represent all the call data we need.

    Attributes:
        number: number of calls
        self_nano_seconds: time spent in the routine, subroutines excluded
        subroutines_nano_seconds: time spent in subroutines
    """

    def __init__(
        self, number: int, self_nano_seconds: int, subroutines_nano_seconds: int
    ):
        self.number = number
        self.self_nano_seconds = self_nano_seconds
        self.subroutines_nano_seconds = subroutines_nano_seconds

    def __iadd__(self, other: "RoutineCallsData") -> "RoutineCallsData":
        self.number += other.number
        self.self_nano_seconds += other.self_nano_seconds
        self.subroutines_nano_seconds += other.subroutines_nano_seconds
        return self

    def __add__(self, other: "RoutineCallsData") -> "RoutineCallsData":
        return RoutineCallsData(
            self.number + other.number,
            self.self_nano_seconds + other.self_nano_seconds,
            self.subroutines_nano_seconds + other.subroutines_nano_seconds,
        )

    def __repr__(self) -> str:
        return self.to_dict().__repr__()

    def to_dict(self) -> ty.Dict[str, int]:
        return self.__dict__


class RoutineData:
    """Represents the call data of a given routine.

    Attributes:
        self_call: data about the routine
        called_by: data about the callers of the routine
        subroutine_calls: data about the routines called by the routine
    """

    def __init__(self):
        self.self_call: RoutineCallsData = RoutineCallsData(0, 0, 0)
        self.called_by: ty.Dict[str, RoutineCallsData] = dict()
        self.subroutine_calls: ty.Dict[str, RoutineCallsData] = dict()

    def add_call(self, call_data: RoutineCallsData):
        self.self_call += call_data

    def add_subroutine_call(self, called_subroutine: str, call_data: RoutineCallsData):
        self.subroutine_calls[called_subroutine] = (
            self.subroutine_calls.setdefault(
                called_subroutine, RoutineCallsData(0, 0, 0)
            )
            + call_data
        )

    def add_called_by(self, caller_routine: str, call_data: RoutineCallsData):
        self.called_by[caller_routine] = (
            self.called_by.setdefault(caller_routine, RoutineCallsData(0, 0, 0))
            + call_data
        )

    def __repr__(self) -> str:
        return self.to_dict().__repr__()

    def to_dict(self) -> ty.Dict:
        return {
            "self_call": self.self_call.to_dict(),
            "called_by": {k: v.to_dict() for k, v in self.called_by.items()},
            "subroutine_calls": {
                k: v.to_dict() for k, v in self.subroutine_calls.items()
            },
        }


class ProgramData:
    """Represents the program data needed to analyse it.

    Attributes:
        max_index: maximum index found in indices
        indices: a dictionary-like structure linking subroutines names with an index.
            The program entry-point (i.e. a "virtual" routine that has a standard
            name and that acts as the entry point of the program) is **not** included in
            this attribute.
        routines_data: a dictionary-like structure linking subroutines name with
            their call data. The program entry-point (i.e. a "virtual" routine that has
            a standard name and that acts as the entry point of the program) **is**
            included in this attribute.
        total_time_nanoseconds: total execution time of the program in nano-seconds
    """

    def __init__(self, total_time_nanoseconds: int, entry_point: str = "<spontaneous>"):
        self.max_index: int = 0
        self.indices: ty.Dict[str, int] = dict()
        self.routines_data: ty.Dict[str, RoutineData] = dict()
        self.total_time_nanoseconds: int = total_time_nanoseconds
        self.entry_point: str = entry_point

    def _add_subroutine_no_index(self, subroutine_name: str) -> None:
        """Add a subroutine to the program, without adding it to the internal index.

        This method should only be used internally. It is used to add the entry point
        routine without messing with the indices stored.

        :param subroutine_name: name of the subroutine to register.
        """
        if subroutine_name in self.routines_data:
            raise RuntimeError(
                f"The subroutine '{subroutine_name}' has already been added."
            )
        self.routines_data[subroutine_name] = RoutineData()

    def add_subroutine(self, subroutine_name: str) -> None:
        """Add a subroutine to the program.

        This method should be called for each new subroutine. Calling any other
        method of the class with a subroutine that has not been added with this
        method will result in an exception.

        :param subroutine_name: name of the subroutine to register.
        """
        self._add_subroutine_no_index(subroutine_name)
        self.max_index = len(self.indices)
        self.indices[subroutine_name] = len(self.indices)

    def add_subroutine_call(
        self,
        caller: str,
        called_routine: str,
        number: int,
        self_nano_seconds: int,
        subroutines_nano_seconds: int,
    ):
        """Add the information about `called_routine` being called by `caller`.

        Whenever a registered subroutine is called by another registered subroutine,
        this method should be called in order to update the stored data.

        :param caller: name of the routine calling `called_routine`.
        :param called_routine: name of the routine called by `caller`.
        :param number: number of times `caller` calls `called_routine`. For example
            if `caller` is called 3 times and calls in turn `called_routine` twice,
            this parameter should be 6 = 3 * 2 = the number of times `called_routine`
            has been called from `caller`.
        :param self_nano_seconds: total self time spent by the `number` calls (time
            spent in subroutines is excluded).
        :param subroutines_nano_seconds: total time spent in subroutines called by
            the `number` calls to `called_routine`.
        """
        call_data: RoutineCallsData = RoutineCallsData(
            number, self_nano_seconds, subroutines_nano_seconds
        )
        self.routines_data[called_routine].add_call(call_data)
        self.routines_data[caller].add_subroutine_call(called_routine, call_data)
        self.routines_data[called_routine].add_called_by(caller, call_data)

    def add_entry_point_call(
        self,
        called_routine: str,
        number: int,
        self_nano_seconds: int,
        subroutines_nano_seconds: int,
    ):
        """Add the information about `called_routine` being called by the entry point

        This method should only be called once for the main routine of the program,
        i.e. the routine that is called when starting the program.

        :param called_routine: name of the routine called by `caller`.
        :param number: number of times `caller` calls `called_routine`. For example
            if `caller` is called 3 times and calls in turn `called_routine` twice,
            this parameter should be 6 = 3 * 2 = the number of times `called_routine`
            has been called from `caller`.
        :param self_nano_seconds: total self time spent by the `number` calls (time
            spent in subroutines is excluded).
        :param subroutines_nano_seconds: total time spent in subroutines called by
            the `number` calls to `called_routine`.
        """
        if self.entry_point not in self.routines_data:
            self._add_subroutine_no_index(self.entry_point)
        if len(self.routines_data[self.entry_point].subroutine_calls) != 0:
            alread_called: str = next(
                iter(self.routines_data[self.entry_point].subroutine_calls.keys())
            )
            raise RuntimeError(
                "The entry-point cannot call more than one subroutine. It already "
                f"called '{alread_called}' and as such cannot call '{called_routine}'."
            )
        self.add_subroutine_call(
            self.entry_point,
            called_routine,
            number,
            self_nano_seconds,
            subroutines_nano_seconds,
        )

    def __repr__(self) -> str:
        return self.to_dict().__repr__()

    def to_dict(self) -> ty.Dict:
        return {
            "max_index": self.max_index,
            "indices": self.indices,
            "routines_data": {k: v.to_dict() for k, v in self.routines_data.items()},
            "total_time_nanoseconds": self.total_time_nanoseconds,
            "entry_point": self.entry_point,
        }
