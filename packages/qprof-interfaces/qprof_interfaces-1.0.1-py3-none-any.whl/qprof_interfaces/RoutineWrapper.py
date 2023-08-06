# ======================================================================
# Copyright CERFACS (July 2019)
# Contributor: Adrien Suau (adrien.suau@cerfacs.fr)
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

import abc
import typing as ty


class RoutineWrapper(abc.ABC):
    """Wrapper around the framework-specific routine type.

    This class should be subclassed and implemented by each framework. It helps
    providing a unique API for all the frameworks that can then be used by the main
    qprof library to profile the wrapper routine.
    """

    @abc.abstractmethod
    def __init__(self, routine):
        """Initialise the wrapper with the given routine

        :param routine: a framework-specific routine that will be wrapped.
        """
        pass

    @abc.abstractmethod
    def __iter__(self) -> ty.Iterable["RoutineWrapper"]:
        """Magic Python method to make the RoutineWrapper object iterable.

        :return: an iterable over all the subroutines called by the wrapped routine.
            The subroutines should be wrapped by the RoutineWrapper.
        """
        pass

    @property
    def ops(self):
        return list(self)

    @property
    @abc.abstractmethod
    def is_base(self) -> bool:
        """Check if the wrapped routine is a "base" routine.

        Base routines are routines that are considered as primitive, i.e. that do not
        call any subroutine.
        The concept of base routine is essential for qprof as only base routines should
        have an entry in the "gate_times" dictionary provided to the "profile" method
        and base routines are used to stop the recursion into the call-tree.

        :return: True if the wrapped routine is considered as a "base" routine,
            else False.
        """
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Returns the name of the wrapped subroutine."""
        pass

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Computes the hash of the wrapped routine.

        __hash__ and __eq__ methods are used by qprof to cache routines and re-use
        already computed data. This optimisation gives impressive results on some
        circuits and is expected to improve the runtime of qprof on nearly all
        quantum circuits, because routines are most of the time re-used.

        :return: int representing a hash of the wrapper routine.
        """
        pass

    @abc.abstractmethod
    def __eq__(self, other: "RoutineWrapper") -> bool:
        """Equality testing for wrapped routines.

        __hash__ and __eq__ methods are used by qprof to cache routines and re-use
        already computed data. This optimisation gives impressive results on some
        circuits and is expected to improve the runtime of qprof on nearly all
        quantum circuits, because routines are most of the time re-used.

        Two routines should be considered equal if and only if they generate exactly
        the same circuit.

        Comparing the generated circuits might be a costly task, but other methods
        can be used. For example, routines with the same name and the same parameters
        might be considered as equal (may be framework-dependent).

        :param other: instance of RoutineWrapper to test for equality with self.
        :return: True if self and other are equal (i.e. generate the exact same
            quantum circuit) else False.
        """
        pass
