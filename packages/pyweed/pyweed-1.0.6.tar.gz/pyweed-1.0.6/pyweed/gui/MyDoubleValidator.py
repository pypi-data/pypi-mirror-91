# -*- coding: utf-8 -*-
"""
Custom QDoubleValidator that pays attention to ranges

https://gist.github.com/jirivrany/4473639

:copyright:
    Mazama Science, IRIS
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""

from sys import float_info

from PyQt5.QtGui import QValidator
from PyQt5.QtGui import QDoubleValidator


class MyDoubleValidator(QDoubleValidator):
    '''
    Custom QDoubleValidator that pays attention to ranges

    from https://gist.github.com/jirivrany/4473639

    Note that the Validate API is different for QString v2
    '''

    def __init__(self, bottom=float_info.min,
                 top=float_info.max,
                 decimals=float_info.dig, parent=None):

        super(MyDoubleValidator, self).__init__(bottom, top, decimals, parent)

    def validate(self, input_value, pos):

        if input_value in ('', '.', '-'):
            return QValidator.Intermediate, input_value, pos

        state, value, pos = QDoubleValidator.validate(self, input_value, pos)

        if state != QValidator.Acceptable:
            return QValidator.Invalid, value, pos

        return QValidator.Acceptable, value, pos
