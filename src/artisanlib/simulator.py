#
# ABOUT
# A simple device simulator for Artisan

# LICENSE
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

# AUTHOR
# Marko Luther, 2023


from artisanlib.util import fromFtoCstrict, fromCtoFstrict, RoRfromFtoCstrict, RoRfromCtoFstrict

import numpy
import logging
from typing import Final, Tuple, Dict, List, Any, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    import numpy.typing as npt # pylint: disable=unused-import


_log: Final[logging.Logger] = logging.getLogger(__name__)

class Simulator:
    __slots__ = [ 'profile', 'temp1', 'temp2', 'timex', 'extratemp1', 'extratemp2', 'extratimex',
        'extraDelta1', 'extraDelta2', 'extraNoneTempHint1', 'extraNoneTempHint2',
        'temp1_array', 'temp2_array', 'timex_array', 'extratemp1_array', 'extratemp2_array', 'extratimex_array']

    # mode is the current temperature of Artisan, either "C" or "F"
    def __init__(self, mode:str, profile:Optional[Dict[str, Any]] = None) -> None:

        self.temp1:List[float]
        self.temp2:List[float]
        self.timex:List[float]
        self.extratemp1: List[List[float]]
        self.extratemp2: List[List[float]]
        self.extratimex: List[List[float]]

        self.temp1_array:'npt.NDArray[numpy.double]'
        self.temp2_array:'npt.NDArray[numpy.double]'
        self.timex_array:'npt.NDArray[numpy.double]'
        self.extratemp1_array: List['npt.NDArray[numpy.double]']
        self.extratemp2_array: List['npt.NDArray[numpy.double]']
        self.extratimex_array: List['npt.NDArray[numpy.double]']

        self.profile = profile
        if profile is not None:
            self.temp1 = profile['temp1']
            self.temp2 = profile['temp2']
            self.timex = profile['timex']
        else:
            self.temp1 = []
            self.temp2 = []
            self.timex = []
        if profile is not None and 'extratemp1' in profile and 'extratemp2' in profile and 'extratimex' in profile:
            self.extratemp1 = profile['extratemp1']
            self.extratemp2 = profile['extratemp2']
            self.extratimex = profile['extratimex']
        else:
            self.extratemp1 = []
            self.extratemp2 = []
            self.extratimex = []
        if profile is not None and 'extraDelta1' in profile and 'extraDelta2' in profile:
            self.extraDelta1 = profile['extraDelta1']
            self.extraDelta2 = profile['extraDelta2']
        else:
            self.extraDelta1 = [False]*len(self.extratimex)
            self.extraDelta2 = [False]*len(self.extratimex)
        self.extraNoneTempHint1 = (profile.get('extraNoneTempHint1', []) if profile is not None else [])
        self.extraNoneTempHint2 = (profile.get('extraNoneTempHint2', []) if profile is not None else [])

        # convert temperature unit if needed
        m = profile['mode'] if profile is not None and 'mode' in profile else mode
        if mode == 'C' and m == 'F':
            self.temp1 = [fromFtoCstrict(t) for t in self.temp1]
            self.temp2 = [fromFtoCstrict(t) for t in self.temp2]
            for e in range(len(self.extratimex)):
                if self.extraDelta1[e]:
                    self.extratemp1[e] = [RoRfromFtoCstrict(t) for t in self.extratemp1[e]]
                elif not (len(self.extraNoneTempHint1) > e and self.extraNoneTempHint1[e]):
                    self.extratemp1[e] = [fromFtoCstrict(t) for t in self.extratemp1[e]]
                if self.extraDelta2[e]:
                    self.extratemp2[e] = [RoRfromFtoCstrict(t) for t in self.extratemp2[e]]
                elif not (len(self.extraNoneTempHint2) > e and self.extraNoneTempHint2[e]):
                    self.extratemp2[e] = [fromFtoCstrict(t) for t in self.extratemp2[e]]
        elif mode == 'F' and m == 'C':
            self.temp1 = [fromCtoFstrict(t) for t in self.temp1]
            self.temp2 = [fromCtoFstrict(t) for t in self.temp2]

            for e in range(len(self.extratimex)):
                if self.extraDelta1[e]:
                    self.extratemp1[e] = [RoRfromCtoFstrict(t) for t in self.extratemp1[e]]
                elif not (len(self.extraNoneTempHint1) > e and self.extraNoneTempHint1[e]):
                    self.extratemp1[e] = [fromCtoFstrict(t) for t in self.extratemp1[e]]
                if self.extraDelta2[e]:
                    self.extratemp2[e] = [RoRfromCtoFstrict(t) for t in self.extratemp2[e]]
                elif not (len(self.extraNoneTempHint2) > e and self.extraNoneTempHint2[e]):
                    self.extratemp2[e] = [fromCtoFstrict(t) for t in self.extratemp2[e]]

        self.removeEmptyPrefix()

    def removeEmptyPrefix(self) -> None:
        try:
            # select the first BT index not an error value to start with
            start = [i != -1 for i in self.temp2].index(True)
            self.temp1_array = numpy.array(self.temp1[start:])
            self.temp2_array = numpy.array(self.temp2[start:])
            self.timex_array = numpy.array(self.timex[start:])
            self.extratemp1_array = []
            self.extratemp2_array = []
            self.extratimex_array = []
            for i, _ in enumerate(self.extratimex):
                self.extratemp1_array.append(numpy.array(self.extratemp1[i][start:]))
                self.extratemp2_array.append(numpy.array(self.extratemp2[i][start:]))
                self.extratimex_array.append(numpy.array(self.extratimex[i][start:]))
            # shift timestamps such that they start with 0
            if len(self.timex_array) > 0:
                self.timex_array = self.timex_array - self.timex_array[0]
            # shift timestamps such that they start with 0
            for i, _ in enumerate(self.extratimex_array):
                if len(self.extratimex_array[i]) > 0:
                    self.extratimex_array[i] = self.extratimex_array[i] - self.extratimex_array[i][0]
        except Exception as e: # pylint: disable=broad-except
            _log.exception(e)

    def read(self, tx:float) -> Tuple[float, float]:
        et:float = -1.0
        bt:float = -1.0
        try:
            if tx == 0:
                et = self.temp1_array[0]
                bt = self.temp2_array[0]
            else:
                et = float(numpy.interp(tx,self.timex_array,self.temp1_array))
                bt = float(numpy.interp(tx,self.timex_array,self.temp2_array))
        except Exception: # pylint: disable=broad-except
            pass
        return et,bt

    def readextra(self, i:int, tx:float) -> Tuple[float, float]:
        t1:float = -1
        t2:float = -1
        try:
            if tx == 0:
                t1 = self.extratemp1_array[i][0]
                t2 = self.extratemp2_array[i][0]
            else:
                t1 = float(numpy.interp(tx,self.extratimex_array[i],self.extratemp1_array[i]))
                t2 = float(numpy.interp(tx,self.extratimex_array[i],self.extratemp2_array[i]))
        except Exception: # pylint: disable=broad-except
            pass
        return t2,t1
