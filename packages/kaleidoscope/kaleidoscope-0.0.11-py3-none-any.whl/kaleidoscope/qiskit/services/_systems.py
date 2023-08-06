# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=unexpected-keyword-arg

"""Module for easily getting IBMQ systems"""

import warnings
from kaleidoscope.errors import KaleidoscopeError
from ._account import Account
from .filters.backend import (BackendCollection, NumQubits, HasPulse,
                              QVCompare, IsOperational,
                              MaxCircuits, MaxShots, Reservations)


class KaleidoscopeSystemService():
    """The service class for systems.

    All attributes are dynamically attached to
    this class.

    This class is much simpler than the simulators
    one because there is no processing that needs
    to be done async.

    Allows for filtering backends by the following:

    - `num_qubits` : Filter against an integer number of qubits.

    - `open_pulse` : Boolean filter for open_pulse capability.

    - `quantum_volume` : Filter against an integer number for quantum volume.

    - `operational` : Boolean filter for system operational status.

    - `max_circuits` : Filter against integer number of max circuits.

    - `max_shots` : Filter against integer number of max shots.
    """
    def __init__(self):
        self._all_added_attr = None
        self._default_added_attr = None
        self._default_added_backends = None
        self._default_provider = Account.get_default_provider()
        _system_loader(self)

    def __call__(self, name=None):
        """Return all backends that satisfy the given criteria.

        If no criteria passed then returns all systems.

        Parameters:
            name (str or list): System name(s).

        Returns:
            IBMQBackend: A single backend instance if only one.
            BackendCollection: List of specified backends if more than one.

        Raises:
            KaleidoscopeError: No matching backends.
        """
        if name is not None:
            if not isinstance(name, list):
                out = [back for back in self._default_added_backends if back.name() == name]
                if any(out):
                    return out[0]
                raise KaleidoscopeError('No matching backend name.')
            out = []
            for nm in name:
                out += [back for back in self._default_added_backends if back.name() == nm]
            if any(out):
                return BackendCollection(out)
            raise KaleidoscopeError('No matching backend names.')
        return BackendCollection(self._default_added_backends)

    def __getattr__(self, name):
        if name == 'num_qubits':
            out = NumQubits(self._default_added_backends)
        elif name == 'open_pulse':
            out = HasPulse(self._default_added_backends)
        elif name == 'quantum_volume':
            out = QVCompare(self._default_added_backends)
        elif name == 'operational':
            out = IsOperational(self._default_added_backends)
        elif name == 'max_circuits':
            out = MaxCircuits(self._default_added_backends)
        elif name == 'max_shots':
            out = MaxShots(self._default_added_backends)
        elif name == 'reservations':
            out = Reservations(self._default_added_backends)
        else:
            raise AttributeError("BackendCollection does not have attr '{}'.".format(name))
        return out

    def _refresh(self):
        """Refresh the service in place.
        """
        for key in self._default_added_attr:
            try:
                del self.__dict__[key]
            except AttributeError:
                pass
        self._all_added_attr = []
        self._default_added_attr = []
        self._default_added_backends = []
        self._default_provider = Account.get_default_provider()
        delattr(self, 'ALL')
        _system_loader(self)


class KaleidoscopeSystemDispatcher():
    """Contains all the backend instances
    corresponding to the providers for a given
    system.

    All attributes are dynamically attached to
    this class.

    Allows for filtering backends by the following:

    - `num_qubits` : Filter against an integer number of qubits.

    - `open_pulse` : Boolean filter for open_pulse capability.

    - `quantum_volume` : Filter against an integer number for quantum volume.

    - `operational` : Boolean filter for system operational status.

    - `max_circuits` : Filter against integer number of max circuits.

    - `max_shots` : Filter against integer number of max shots.
    """
    def __call__(self, name=None, hub=None, group=None, project=None):
        """Return all backends that satisfy the given criteria.

        If no criteria passed then returns all systems.

        Parameters:
            name (str or list): System name.
            hub (str or list): Specified hub.
            group (str or list): Specified group.
            project (str or list): Specified project.

        Returns:
            BackendCollection: List of specified backends.

        Raises:
            KaleidoscopeError: No matching backends.
        """
        filtered_backends = self._added_backends
        if name is not None:
            _temp = []
            if not isinstance(name, list):
                name = [name]
            for nm in name:
                _temp += [back for back in self._added_backends
                          if back.name() == nm and back in filtered_backends]
            filtered_backends = _temp

        if hub is not None:
            _temp = []
            if not isinstance(hub, list):
                hub = [hub]
            for hb in hub:
                _temp += [back for back in self._added_backends
                          if back.hub == hb and back in filtered_backends]
            filtered_backends = _temp

        if group is not None:
            _temp = []
            if not isinstance(group, list):
                group = [group]
            for gp in group:
                _temp += [back for back in self._added_backends
                          if back.group == gp and back in filtered_backends]
            filtered_backends = _temp

        if project is not None:
            _temp = []
            if not isinstance(project, list):
                project = [project]
            for pt in project:
                _temp += [back for back in self._added_backends
                          if back.project == pt and back in filtered_backends]
            filtered_backends = _temp

        if not any(filtered_backends):
            raise KaleidoscopeError('No matching systems found.')
        return BackendCollection(filtered_backends)

    def __getattr__(self, name):
        if name == 'num_qubits':
            out = NumQubits(self._added_backends)
        elif name == 'open_pulse':
            out = HasPulse(self._added_backends)
        elif name == 'quantum_volume':
            out = QVCompare(self._added_backends)
        elif name == 'operational':
            out = IsOperational(self._added_backends)
        elif name == 'max_circuits':
            out = MaxCircuits(self._added_backends)
        elif name == 'max_shots':
            out = MaxShots(self._added_backends)
        elif name == 'reservations':
            out = Reservations(self._added_backends)
        else:
            raise AttributeError("BackendCollection does not have attr '{}'.".format(name))
        return out


def _system_loader(service):
    """Attaches system dispatchers to the service
    """
    if not any(Account.providers()):
        try:
            Account.load_account()
        except Exception:  # pylint: disable=broad-except
            pass
    systems = _get_ibmq_systems()
    all_added_attr = []
    default_added_attr = []
    default_added_backends = []
    default_provider = service._default_provider.split('//') if service._default_provider else []

    setattr(service, 'ALL', KaleidoscopeSystemDispatcher())
    setattr(service.ALL, '_added_backends', [])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for name, back_list in systems.items():
            reference = back_list[0]
            num_qubits = reference._configuration.num_qubits
            system_name = "{}𖼯{}Q𖼞".format(name, num_qubits)
            all_dispatcher = KaleidoscopeSystemDispatcher()
            for backend in back_list:
                hub = backend.hub
                group = backend.group
                project = backend.project
                pro_str = "{}_{}_{}".format(hub, group, project)
                pro_str = pro_str.replace('-', 'ー')
                setattr(all_dispatcher, pro_str, backend)
                service.ALL._added_backends.append(backend)
                # is backend in default provider
                if [hub, group, project] == default_provider:
                    setattr(service, system_name, backend)
                    default_added_attr.append(system_name)
                    default_added_backends.append(backend)

            setattr(service.ALL, 'get_'+system_name, all_dispatcher)
            all_added_attr.append(system_name)

    service._all_added_attr = all_added_attr
    service._default_added_attr = default_added_attr
    service._default_added_backends = default_added_backends


def _get_ibmq_systems():
    """Get instances for all IBMQ systems that the user has access to.

    Returns:
        dict: A dict of all IBMQ systems that a user has access to.
    """
    ibmq_backends = {}
    for pro in Account.providers():
        for back in pro.backends():
            if not back.configuration().simulator:
                if ('alt' not in back.name()) \
                        and back.name().startswith('ibmq'):
                    if back.name() not in ibmq_backends:
                        ibmq_backends[back.name()] = [back]
                    else:
                        ibmq_backends[back.name()].append(back)
    return ibmq_backends
