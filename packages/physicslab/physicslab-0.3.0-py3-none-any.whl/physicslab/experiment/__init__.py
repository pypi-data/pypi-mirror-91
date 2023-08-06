"""
Modules for particular experiments and general functions.
"""


from physicslab.experiment import van_der_pauw
from physicslab.experiment import hall
from physicslab.experiment import magnetism_type


def process(measurements, by_module, **kwargs):
    """ Genereal process function calling appropriate *process* function
    from selected :mod:`experiment` module.

    If you want to use simple list of measurements, wrap :attr:`measurements`
    argument in :func:`enumerate` method.

    :param measurements: List of pairs ``(name, data)``. The latter one
        is passed to appropriate *process* method
    :type measurements: list(tuple)
    :param by_module: Module by which the :attr:`measurements` should be
        processed
    :type by_module: :mod:`experiment` submodule
    :param kwargs: Additional keyword arguments are forwarded to
        :meth:`by_module.process` method
    :return: Collection of results indexed by ``name``
    :rtype: pandas.DataFrame
    """
    import pandas as pd

    output = pd.DataFrame(columns=by_module.PROCESS_COLUMNS)
    for name, data in measurements:
        series = by_module.process(data, **kwargs)
        series.name = name
        output = output.append(series)
    return output
