from __future__ import annotations
from typing import TYPE_CHECKING
import inspect

from py_rete.beta import ReteNode
from py_rete.common import V

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any
    from typing import Dict
    from py_rete.network import ReteNetwork


class BindNode(ReteNode):
    """
    A beta network class. This class stores a code snipit, with variables in
    it. It gets all the bindings from the incoming token, updates them with the
    current bindings, binds the result to the target variable (to), then
    activates its children with the updated bindings.
    """

    def __init__(self, children, parent, func, to, rete: ReteNetwork):
        """
        :type children:
        :type parent: BetaNode
        :type to: str
        """
        super().__init__(children=children, parent=parent)
        self.func = func
        self.bind = to
        self._rete_net = rete

    def get_function_result(self, binding: Dict[V, Any]):
        """
        Given a binding that maps variables to values, this instantiates the
        arguments for the function and executes it.
        """
        args = inspect.getfullargspec(self.func)[0]
        args = {arg: self._rete_net if arg == 'net' else
                self._rete_net.facts[binding[V(arg)]] if
                binding[V(arg)] in self._rete_net.facts else
                binding[V(arg)] for arg in args}
        return self.func(**args)

    def left_activation(self, token, wme, binding):
        """
        Copies and updates the bindings with the results of the function
        execution. It then left_activates children with this binding.
        """
        result = self.get_function_result(binding)

        if self.bind in binding:
            if binding[self.bind] != result:
                return
        else:
            binding = binding.copy()
            binding[self.bind] = result

        for child in self.children:
            child.left_activation(token, wme, binding)
