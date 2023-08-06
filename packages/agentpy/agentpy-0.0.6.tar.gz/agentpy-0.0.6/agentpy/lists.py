"""
Agentpy Lists Module
Content: Lists for objects, environments, and agents
"""

import random as rd


class AttrList(list):
    """ List of attributes from an :class:`AgentList`.

    Calls are forwarded to each entry and return a list of return values.
    Boolean operators are applied to each entry and return a list of bools.
    Arithmetic operators are applied to each entry and return a new list.
    See :class:`AgentList` for examples.
    """

    def __init__(self, *args, attr=None):
        super().__init__(*args)
        self.attr = attr

    def __repr__(self):
        if self.attr is None:
            return f"AttrList: {list.__repr__(self)}"
        else:
            return f"AttrList of attribute '{self.attr}': " \
                   f"{list.__repr__(self)}"

    def __call__(self, *args, **kwargs):
        return AttrList(
            [func_obj(*args, **kwargs) for func_obj in self],
            attr=self.attr)

    def __eq__(self, other):
        return [obj == other for obj in self]

    def __ne__(self, other):
        return [obj != other for obj in self]

    def __lt__(self, other):
        return [obj < other for obj in self]

    def __le__(self, other):
        return [obj <= other for obj in self]

    def __gt__(self, other):
        return [obj > other for obj in self]

    def __ge__(self, other):
        return [obj >= other for obj in self]

    def __add__(self, v):
        if isinstance(v, AttrList):
            return AttrList([x + y for x, y in zip(self, v)])
        else:
            return AttrList([x + v for x in self])

    def __sub__(self, v):
        if isinstance(v, AttrList):
            return AttrList([x - y for x, y in zip(self, v)])
        else:
            return AttrList([x - v for x in self])

    def __mul__(self, v):
        if isinstance(v, AttrList):
            return AttrList([x * y for x, y in zip(self, v)])
        else:
            return AttrList([x * v for x in self])

    def __truediv__(self, v):
        if isinstance(v, AttrList):
            return AttrList([x / y for x, y in zip(self, v)])
        else:
            return AttrList([x / v for x in self])

    def __iadd__(self, v):
        return self + v

    def __isub__(self, v):
        return self - v

    def __imul__(self, v):
        return self * v

    def __itruediv__(self, v):
        return self / v


class ObjList(list):
    """ List of agentpy objects (models, environments, agents). """

    def __repr__(self):
        s = 's' if len(self) > 1 else ''
        return f"ObjList [{len(self)} object{s}]"

    def __setattr__(self, name, value):
        if isinstance(value, AttrList):
            # Apply each value to each agent
            for obj, v in zip(self, value):
                setattr(obj, name, v)
        else:
            # Apply single value to all agents
            for obj in self:
                setattr(obj, name, value)

    def __getattr__(self, name):
        """ Return callable list of attributes """
        return AttrList([getattr(obj, name) for obj in self], attr=name)

    def __call__(self, selection):
        return self.select(selection)

    def select(self, selection):
        """ Returns a new :class:`AgentList` based on `selection`.

        Attributes:
            selection (list of bool): List with same length as the agent list.
                Positions that return True will be selected.
        """
        return AgentList([a for a, s in zip(self, selection) if s])

    def random(self, n=1):
        """ Returns a new :class:`AgentList`
        with ``n`` random agents (default 1)."""
        return AgentList(rd.sample(self, n))

    def sort(self, var_key, reverse=False):
        """ Sorts the list based on var_key and returns self """
        super().sort(key=lambda x: x[var_key], reverse=reverse)
        return self

    def shuffle(self):
        """ Shuffles the list and returns self """
        rd.shuffle(self)
        return self


class AgentList(ObjList):
    """ List of agents.

    Attribute calls and assignments are applied to all agents
    and return an :class:`AttrList` with attributes of each agent.
    This also works for method calls, which returns a list of return values.
    Arithmetic operators can further be used to manipulate agent attributes,
    and boolean operators can be used to filter list based on agent attributes.

    Examples:

        Let us start by preparing an :class:`AgentList` with three agents::

            >>> model = ap.Model()
            >>> model.add_agents(3)
            >>> agents = model.agents
            >>> agents
            AgentList [3 agents]

        The assignment operator can be used to set a variable for each agent.
        When the variable is called, an :class:`AttrList` is returned::

            >>> agents.x = 1
            >>> agents.x
            AttrList of attribute 'x': [1, 1, 1]

        One can also set different variables for each agent
        by passing another :class:`AttrList`::

            >>> agents.y = ap.AttrList([1, 2, 3])
            >>> agents.y
            AttrList of attribute 'y': [1, 2, 3]

        Arithmetic operators can be used in a similar way.
        If an :class:`AttrList` is passed, different values are used for
        each agent. Otherwise, the same value is used for all agents::

            >>> agents.x = agents.x + agents.y
            >>> agents.x
            AttrList of attribute 'x': [2, 3, 4]

            >>> agents.x *= 2
            >>> agents.x
            AttrList of attribute 'x': [4, 6, 8]

        Boolean operators can be used to select a subset of agents::

            >>> subset = agents(agents.x > 5)
            >>> subset
            AgentList [2 agents]

            >>> subset.x
            AttrList of attribute 'x': [6, 8]
    """

    def __repr__(self):
        return f"AgentList [{len(self)} agent{'s' if len(self) != 1 else ''}]"


class EnvList(ObjList):
    """ List of environments.

    Attribute calls and assignments are applied to all environments
    and return an :class:`AttrList` with attributes of each environment.
    This also works for method calls, which returns a list of return values.
    Arithmetic operators can further be used to manipulate attributes,
    and boolean operators can be used to filter list based on attributes.

    See :class:`AgentList` for examples.
    """

    def __repr__(self):
        s = 's' if len(self) > 1 else ''
        return f"EnvList [{len(self)} environment{s}]"

    def add_agents(self, *args, **kwargs):
        """ Add the same agents to all environments in the list.
        See :func:`Environment.add_agents` for arguments and keywords."""

        if self:
            new_agents = self[0].add_agents(*args, **kwargs)
            if len(self) > 1:
                for env in self[1:]:
                    env.add_agents(new_agents)
