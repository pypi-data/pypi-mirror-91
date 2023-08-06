# ======================================================================
# Copyright CERFACS (August 2019)
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

from qat.lang.AQASM.routines import QRoutine

from ._interfaces import interfaces


class NamedRoutine(QRoutine, interfaces.NamedRoutine):
    def __init__(self, name: str, arity: int = 0, routop_l=None):
        super().__init__(arity=arity, routop_l=routop_l)
        self.name = name

    @staticmethod
    def from_Routine(rout: QRoutine) -> "NamedRoutine":
        return NamedRoutine(rout.name, rout.arity, rout.op_list)

    @staticmethod
    def from_Routine_and_name(rout: QRoutine, name: str) -> "NamedRoutine":
        return NamedRoutine(name, rout.arity, rout.op_list)

    def ctrl(self) -> "NamedRoutine":
        return NamedRoutine.from_Routine_and_name(super().ctrl(), name="C-" + self.name)

    def dag(self) -> "NamedRoutine":
        return NamedRoutine.from_Routine_and_name(
            super().dag(),
            name=(self.name[2:] if self.name.startswith("D-") else ("D-" + self.name)),
        )

    def trans(self) -> "NamedRoutine":
        return NamedRoutine.from_Routine_and_name(super().trans(), name=self.name)

    def conj(self) -> "NamedRoutine":
        return NamedRoutine.from_Routine_and_name(super().conj(), name=self.name)
