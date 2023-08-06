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
import inspect
import typing as ty
from collections import deque

from qat.core.gate_set import GateSet, GateSignature
from qat.lang.AQASM.gates import ParamGate, PredefGate, Gate, AbstractGate
from qat.lang.AQASM.routines import QRoutine
from types import ModuleType

from ._interfaces import interfaces

GateType = ty.Union[ParamGate, AbstractGate, QRoutine, PredefGate, Gate]
GateWithName = GateType
LinkingType = ty.Union[AbstractGate, GateSet, ModuleType]
GateCtrlIterable = ty.Iterable[ty.Tuple[GateType, int]]


class RoutineWrapper(interfaces.RoutineWrapper):

    _GATE_TYPES = [ParamGate, AbstractGate, QRoutine, PredefGate, Gate]

    def _iter_from_ParamGate(self, gate: ParamGate, ctrl: int) -> GateCtrlIterable:
        if gate.name in self._linking_set:
            gate.abstract_gate.set_circuit_generator(
                self._linking_set[gate.name].circuit_generator
            )
        yield (
            gate.abstract_gate.circuit_generator(*gate.parameters),
            ctrl + (gate.nb_ctrls or 0),
        )

    def _iter_from_PredefGate(self, gate: PredefGate, ctrl: int) -> GateCtrlIterable:
        # Return an iterable containing the predefined gate only
        yield gate, ctrl

    def _iter_from_QRoutine(self, gate: QRoutine, ctrl: int) -> GateCtrlIterable:
        return (
            (
                op.gate,
                (
                    0
                    if self.use_protected_gates and op.ctrl_prot
                    else ctrl + (gate.nb_ctrls or 0)
                ),
            )
            for op in gate.op_list
        )

    def _iter_from_Gate(self, gate: Gate, ctrl: int) -> GateCtrlIterable:
        yield gate.subgate, ctrl + (gate.nb_ctrls or 0)

    def _iter_from(self, gate: GateType, ctrl: int) -> GateCtrlIterable:
        if not hasattr(self, f"_iter_from_{type(gate).__name__}"):
            raise RuntimeError(
                f"Can't iterate over {type(gate).__name__}. Please implement "
                f"'qprof_myqlm.RoutineWrapper._iter_from_{type(gate).__name__}' to "
                f"avoid this error."
            )
        return getattr(self, f"_iter_from_{type(gate).__name__}")(gate, ctrl)

    def __init__(
        self,
        gate: GateWithName,
        linking_set: ty.Union[ty.Dict[str, LinkingType], ty.List[LinkingType]] = None,
        use_protected_gates: bool = False,
        _number_of_controlled_qubits: int = 0,
    ):
        super().__init__(gate)

        self.use_protected_gates = use_protected_gates
        self._gate = gate
        # If the gate is controlled, first save the actual number of controls.
        self._number_of_controlled_qubits_without_self = _number_of_controlled_qubits
        self._number_of_controlled_qubits = _number_of_controlled_qubits + (
            gate.nb_ctrls or 0
        )

        # Default value
        if linking_set is None:
            linking_set = dict()

        # Get the linking set in the appropriate format
        self._linking_set: ty.Dict[str, GateSignature] = dict()
        if isinstance(linking_set, dict):
            self._linking_set = linking_set
        else:
            for link in linking_set:
                if isinstance(link, AbstractGate) or isinstance(link, GateSet):
                    self._linking_set[link.name] = link
                elif isinstance(link, ModuleType):
                    # Get all the GateSignature instances in the module
                    for name, gate in inspect.getmembers(
                        link, predicate=lambda x: isinstance(x, GateSignature)
                    ):
                        self._linking_set[gate.name] = gate

    def __iter__(self):
        queue = deque()
        queue.extend(
            self._iter_from(self._gate, self._number_of_controlled_qubits_without_self)
        )
        while queue:
            gate, ctrl = queue.popleft()
            if getattr(gate, "name", None) is None:
                # Iterate over the provided gate
                queue.extend(self._iter_from(gate, ctrl))
            else:
                # yield the gate
                yield RoutineWrapper(
                    gate, self._linking_set, self.use_protected_gates, ctrl
                )

    @staticmethod
    def is_base_gate(gate: GateType, linking_set: ty.Dict[str, LinkingType]) -> bool:
        if isinstance(gate, PredefGate):
            return True
        elif isinstance(gate, ParamGate):
            return (
                gate.abstract_gate.circuit_generator is None
                and gate.abstract_gate.name not in linking_set
            )
        return False

    @property
    def is_base(self):
        return RoutineWrapper.is_base_gate(self._gate, self._linking_set)

    @property
    def name(self):
        base_name: str = getattr(self._gate, "name", "")
        if not base_name and hasattr(self._gate, "subgate"):
            base_name = getattr(self._gate.subgate, "name", "")

        if base_name.upper() == "X" and self._number_of_controlled_qubits > 0:
            base_name = "NOT"
        return (
            "C" * self._number_of_controlled_qubits
            + ("D" if self._gate.is_dag else "")
            + base_name
        )

    def __hash__(self):
        if self.is_base:
            return hash(self.name)
        return hash(
            (
                self.name,
                getattr(self, "parameters", tuple()),
                id(getattr(self, "abstract_gate"))
                if hasattr(self, "abstract_gate")
                else 0,
            )
        )

    def __eq__(self, other):
        if self.is_base and other.is_base:
            return self.name == other.name
        self_parameters = getattr(self._gate, "parameters", [])
        other_parameters = getattr(other._gate, "parameters", [])
        self_abstract_gate = getattr(self._gate, "abstract_gate", None)
        other_abstract_gate = getattr(other._gate, "abstract_gate", self_abstract_gate)
        return (
            self._number_of_controlled_qubits == other._number_of_controlled_qubits
            and type(self._gate) == type(other._gate)
            and id(self_abstract_gate) == id(other_abstract_gate)
            and len(self_parameters) == len(other_parameters)
            and all(a == b for a, b in zip(self_parameters, other_parameters))
        )

    @property
    def is_controlled(self):
        return self._number_of_controlled_qubits > 0
