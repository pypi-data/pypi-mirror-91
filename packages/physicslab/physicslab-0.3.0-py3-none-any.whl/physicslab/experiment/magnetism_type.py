"""
Magnetization measurement.


"""


import numpy as np
import pandas as pd

from scipy.optimize import newton as scipy_optimize_newton
from scipy.optimize import curve_fit as scipy_optimize_curve_fit

from physicslab.curves import magnetic_hysteresis_loop
from physicslab.electricity import carrier_concentration, Mobility, Resistance


#: Column names used in :meth:`process` function.
PROCESS_COLUMNS = [
    'magnetic_susceptibility',
    'offset',
    'saturation',
    'remanence',
    'coercivity',
    'ratio_DM_FM',
]


def process(data):
    """ Bundle method.

    Parameter :attr:`data` must include magnetic field and
    magnetization and/or temperature. See :class:`Measurement` for
    details and column names.

    :param data: Measured data
    :type data: pandas.DataFrame
    :return: Derived quantities listed in :data:`PROCESS_COLUMNS`.
    :rtype: pandas.Series
    """
    measurement = Measurement(data)

    magnetic_susceptibility, offset = measurement.diamagnetism(
        from_residual=True)
    saturation, remanence, coercivity = measurement.ferromagnetism(
        from_residual=True)
    ratio_DM_FM = abs(measurement.data['Diamagnetism'].iloc[-1]
                      / measurement.data['Ferromagnetism'].iloc[-1])

    return pd.Series(
        data=(magnetic_susceptibility, offset, saturation, remanence,
              coercivity, ratio_DM_FM),
        index=PROCESS_COLUMNS)


class Measurement():
    """ Magnetization measurement.

    Copy magnetization column, so individual magnetic effects can be
    subtracted. Suffix :data:`RESIDUE_SUFFIX` will be added to names of
    copied columns.

    :param data: Magnetic field, magnetization and temperature data. See
        :class:`Measurement.Columns` for default column names.
    :type data: pandas.DataFrame
    """

    class Columns:
        """ :data:`data` column names. """
        #:
        MAGNETICFIELD = 'B'
        #:
        MAGNETIZATION = 'M'

    #: :data:`data` residue column name suffix.
    RESIDUE_SUFFIX = '_residue'

    def __init__(self, data):
        self.data = data

        column = self.Columns.MAGNETIZATION
        self.data[column + self.RESIDUE_SUFFIX] = self.data[column].copy()

    def diamagnetism(self, from_residual=False,
                     fit_label='Diamagnetism', fit_array=None):
        """ Find diamagnetic component of overall magnetization.

        :param from_residual: Use residual data instead of the original data,
            defaults to False
        :type from_residual: bool, optional
        :param fit_label: Simulated data (fit) will be added to a column
            of this name. :class:`None` to skip, defaults to 'Diamagnetism'
        :type fit_label: str, optional
        :param fit_array: Simulate data in those points. None to use source
            points, defaults to None
        :type fit_array: numpy.ndarray, optional
        :return: Magnetic susceptibility and magnetization offset
        :rtype: tuple
        """
        magnetization_label = self._column_name(
            self.Columns.MAGNETIZATION, from_residual)

        coef = self._lateral_linear_fit(self.data[self.Columns.MAGNETICFIELD],
                                        self.data[magnetization_label])
        offset, magnetic_susceptibility = coef

        # Save fitted curve.
        if fit_label is not None:
            if fit_array is None:
                fit_array = self.data[self.Columns.MAGNETICFIELD]
            self.data[fit_label] = np.polynomial.polynomial.polyval(
                fit_array, coef)

        # Modify magnetization residue.
        self._modify_residue(self.Columns.MAGNETIZATION,
                             original_data_label=magnetization_label,
                             simulated_data=np.polynomial.polynomial.polyval(
                                 self.data[self.Columns.MAGNETICFIELD], coef))

        return magnetic_susceptibility, offset

    @staticmethod
    def _lateral_linear_fit(x, y, percentage=10):
        """ Linear fit bypassing central region (there can be hysteresis loop).

        Separate fit of top and bottom part. Then average.

        :param x: Free variable
        :type x: numpy.ndarray
        :param y: Function value
        :type y: numpy.ndarray
        :param percentage: How far from either side should the fitting go.
            Using value, because center is often measured with higher
            accuracy, defaults to 10
        :type percentage: int, optional
        :return: Array of fitting parameters sorted in ascending order.
        :rtype: numpy.ndarray
        """
        lateral_interval = (max(x) - min(x)) * percentage / 100

        mask = x >= max(x) - lateral_interval
        popt_top = np.polynomial.polynomial.polyfit(x[mask], y[mask], 1)

        mask = x <= min(x) + lateral_interval
        popt_bottom = np.polynomial.polynomial.polyfit(x[mask], y[mask], 1)

        return (popt_bottom + popt_top) / 2

    def ferromagnetism(self, from_residual=False,
                       fit_label='Ferromagnetism', fit_array=None,
                       p0=None):
        """ Find ferromagnetic component of overall magnetization.

        :param from_residual: Use residual data instead of the original data,
            defaults to False
        :type from_residual: bool, optional
        :param fit_label: Simulated data (fit) will be added to a column
            of this name. :class:`None` to skip, defaults to 'Ferromagnetism'
        :type fit_label: str, optional
        :param fit_array: Simulate data in those points. None to use source
            points, defaults to None
        :type fit_array: numpy.ndarray, optional
        :return: Saturation, remanence and coercivity
        :rtype: tuple
        """
        magnetization_label = self._column_name(
            self.Columns.MAGNETIZATION, from_residual)

        if p0 is None:
            p0 = self._ferromagnetism_parameter_guess(magnetization_label)
        popt, pcov = scipy_optimize_curve_fit(
            f=magnetic_hysteresis_loop,
            xdata=self.data[self.Columns.MAGNETICFIELD],
            ydata=self.data[magnetization_label],
            p0=p0
        )
        saturation, remanence, coercivity = popt

        # Save fitted curve.
        if fit_label is not None:
            if fit_array is None:
                fit_array = self.data[self.Columns.MAGNETICFIELD]
            self.data[fit_label] = magnetic_hysteresis_loop(fit_array, *popt)

        # Modify magnetization residue.
        self._modify_residue(self.Columns.MAGNETIZATION,
                             original_data_label=magnetization_label,
                             simulated_data=magnetic_hysteresis_loop(
                                 self.data[self.Columns.MAGNETICFIELD], *popt))

        return saturation, remanence, coercivity

    def _ferromagnetism_parameter_guess(self, magnetization_label):
        """ Try to guess ferromagnetic hysteresis loop parameters.

        :param magnetization_label: Source magnetization column name
        :type magnetization_label: str
        :return: saturation, remanence, coercivity
        :rtype: tuple
        """
        magnetic_field = self.data[self.Columns.MAGNETICFIELD]
        magnetization = self.data[magnetization_label]

        saturation = (max(magnetization) - min(magnetization)) / 2
        remanence = saturation / 2
        coercivity = (max(magnetic_field) - min(magnetic_field)) / 10

        return (abs(saturation), abs(remanence), abs(coercivity))

    def _column_name(self, column, residual):
        """[summary]

        :param column: [description]
        :type column: [type]
        :param residual: [description]
        :type residual: [type]
        :return: [description]
        :rtype: [type]
        """
        if residual:
            column += self.RESIDUE_SUFFIX
        return column

    def _modify_residue(self, column, original_data_label, simulated_data):
        """[summary]

        :param column: [description]
        :type column: [type]
        :param original_data_label: [description]
        :type original_data_label: [type]
        :param simulated_data: [description]
        :type simulated_data: [type]
        """
        residual_data_label = self._column_name(column, True)
        original_data = self.data[original_data_label]

        self.data.loc[:, residual_data_label] = original_data - simulated_data
