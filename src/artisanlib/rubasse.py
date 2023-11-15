# -*- coding: utf-8 -*-
#
# ABOUT
# RUBASSE CSV Roast Profile importer for Artisan

import os
import csv
import logging
from typing import Final, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from artisanlib.main import ApplicationWindow # pylint: disable=unused-import
    from artisanlib.types import ProfileData # pylint: disable=unused-import

try:
    from PyQt6.QtWidgets import QApplication # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt6.QtCore import QStringDecoder # @UnusedImport @Reimport  @UnresolvedImport
except ImportError:
    from PyQt5.QtWidgets import QApplication # type: ignore # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt5.QtCore import QStringDecoder # type: ignore # @UnusedImport @Reimport  @UnresolvedImport


_log: Final[logging.Logger] = logging.getLogger(__name__)



# returns a dict containing all profile information contained in the given Rubasse CSV file
def extractProfileRubasseCSV(file:str, aw:'ApplicationWindow') -> 'ProfileData':
    res:ProfileData = {} # the interpreted data set
    res['samplinginterval'] = 1.0
    filename:str = os.path.basename(file)
    res['title'] = filename
    beanname:str = os.path.splitext(os.path.basename(file))[0]
    toString = QStringDecoder(QStringDecoder.Encoding.Utf8)
    res['beans'] = beanname

    with open(file, newline='',encoding='utf-8') as csvFile:
        data = csv.reader(csvFile,delimiter=',')
        #read file header
        header_row = next(data)
        header = ['time','BT','Fan','Heater','RoR','Drum','Humidity','ET','Pressure'] + ['DT', 'timeB', 'BTB', 'FanB', 'HeaterB', 'RoRB', 'DrumB', 'HumidityB', 'ETB', 'PressureB', 'DTB']

        fan:Optional[float] = None # holds last processed fan event value
        fan_last:Optional[float] = None # holds the fan event value before the last one
        heater:Optional[float] = None # holds last processed heater event value
        heater_last:Optional[float] = None # holds the heater event value before the last one
        drumV:Optional[float] = None # holds last processed heater event value
        drum_last:Optional[float] = None # holds the heater event value before the last one
        fan_event:bool = False # set to True if a fan event exists
        heater_event:bool = False # set to True if a heater event exists
        drum_event:bool = False

        specialevents:List[int] = []
        specialeventstype:List[int] = []
        specialeventsvalue:List[float] = []
        specialeventsStrings:List[str] = []
        timex:List[float] = []
        temp1:List[float] = []
        temp2:List[float] = []
        extra1:List[float] = []
        extra2:List[float] = []
        extra3:List[float] = []
        extra4:List[float] = []
        extra5:List[float] = []
        extra6:List[float] = []
        timeindex:List[int] = [-1,0,0,0,0,0,0,0] #CHARGE index init set to -1 as 0 could be an actual index used


        humidity_last:float = 0.0
        hum_1:float = 0.0
        hum_2:float = 0.0
        hum_3:float = 0.0
        hum_4:float = 0.0
        hum_5:float = 0.0
        
        i = 0
        for row in data:
            items = list(zip(header, row))
            item = {}
            for (name, value) in items:
                item[name] = value.strip()

            # take i as time in seconds
            timex.append(i)

            et:float = -1.0
            try:
                et = float(item['ET'])
            except Exception: # pylint: disable=broad-except
                pass
            temp1.append(et)

            bt:float = -1.0
            try:
                bt = float(item['BT'])
                # after 2min we mark DRY if not auto adjusted
                if timeindex[1] == 0 and i>60 and (not aw.qmc.phasesbuttonflag) and bt >= aw.qmc.phases[1]:
                    timeindex[1] = max(0,i)
            except Exception: # pylint: disable=broad-except
                pass
            temp2.append(bt)

            heaterV:float = -1.0
            try:
                heaterV = float(item['Heater'])
            except Exception: # pylint: disable=broad-except
                pass
            extra1.append(heaterV)

            fanV:float = -1.0
            try:
                fanV = float(item['Fan'])
            except Exception: # pylint: disable=broad-except
                pass
            extra2.append(fanV)

            humidity:float = -1.0
            try:
                humidity = float(item['Humidity'])
            except Exception: # pylint: disable=broad-except
                pass
            extra3.append(humidity)

            pressure:float = -1.0
            try:
                pressure = float(item['Pressure'])
            except Exception: # pylint: disable=broad-except
                pass
            extra4.append(pressure)

            drum:float = -1.0
            try:
                drum = float(item['Drum'])
            except Exception: # pylint: disable=broad-except
                pass
            extra5.append(drum)

            DT:float = -1.0
            try:
                DT = float(item['DT'])
#                DT = float((humidity - humidity_last) * 10.0 + 150.0)
                DT = float(humidity - humidity_last)
                humidity_last = humidity
                hum_5 = hum_4
                hum_4 = hum_3
                hum_3 = hum_2
                hum_2 = hum_1
                hum_1 = DT 
                DT = ( hum_1 + hum_2 + hum_3 + hum_4 + hum_5) * 10.0 / 5.0 + 150.0
            except Exception: # pylint: disable=broad-except
                pass
            extra6.append(DT)
#            extra6.append(-1)

            if 'Fan' in item:
                try:
                    vf = item['Fan']
                    if vf != '':
                        v = float(vf)
                        if fan is None or v != fan:
                            # fan value changed
                            if fan_last is not None and v == fan_last:
                                # just a fluctuation, we remove the last added fan value again
                                fan_last_idx = next(i for i in reversed(range(len(specialeventstype))) if specialeventstype[i] == 0)
                                del specialeventsvalue[fan_last_idx]
                                del specialevents[fan_last_idx]
                                del specialeventstype[fan_last_idx]
                                del specialeventsStrings[fan_last_idx]
                                fan = fan_last
                                fan_last = None
                            else:
                                fan_last = fan
                                fan = v
                                fan_event = True
                                v = v/10. + 1
                                specialeventsvalue.append(v)
                                specialevents.append(i)
                                specialeventstype.append(0)
                                specialeventsStrings.append(f"{float(item['Fan'])}%")
                        else:
                            fan_last = None
                except Exception as e: # pylint: disable=broad-except
                    _log.exception(e)
            
            if 'Heater' in item:
                try:
                    vh = item['Heater']
                    if vh != '':
                        v = float(vh)
                        if heater is None or v != heater:
                            # heater value changed
                            if heater_last is not None and v == heater_last:
                                # just a fluctuation, we remove the last added heater value again
                                heater_last_idx = next(i for i in reversed(range(len(specialeventstype))) if specialeventstype[i] == 3)
                                del specialeventsvalue[heater_last_idx]
                                del specialevents[heater_last_idx]
                                del specialeventstype[heater_last_idx]
                                del specialeventsStrings[heater_last_idx]
                                heater = heater_last
                                heater_last = None
                            else:
                                heater_last = heater
                                heater = v
                                heater_event = True
                                v = v/10. + 1
                                specialeventsvalue.append(v)
                                specialevents.append(i)
                                specialeventstype.append(3)
                                specialeventsStrings.append(f"{float(item['Heater'])}%")
                        else:
                            heater_last = None
                except Exception as e: # pylint: disable=broad-except
                    _log.exception(e)

            if 'Drum' in item:
                try:
                    vd = item['Drum']
                    if vd != '':
                        v = float(vd)
                        if drumV is None or v != drumV:
                            # drum value changed
                            if drum_last is not None and v == drum_last:
                                # just a fluctuation, we remove the last added heater value again
                                drum_last_idx = next(i for i in reversed(range(len(specialeventstype))) if specialeventstype[i] == 1)
                                del specialeventsvalue[drum_last_idx]
                                del specialevents[drum_last_idx]
                                del specialeventstype[drum_last_idx]
                                del specialeventsStrings[drum_last_idx]
                                drumV = drum_last
                                drum_last = None
                            else:
                                drum_last = drumV
                                drumV = v
                                drum_event = True
                                v = v/10. + 1
                                specialeventsvalue.append(v)
                                specialevents.append(i)
                                specialeventstype.append(1)
                                specialeventsStrings.append(f"{float(item['Drum'])} rpm")
                        else:
                            drum_last = None
                except Exception as e: # pylint: disable=broad-except
                    _log.exception(e)                    
            i = i + 1

    # mark CHARGE
# not sure if index 1 holds the correct data
#    try:
#        start = int(header_row[1])
#        if start != 0:
#            timeindex[0] = max(0,start)
#    except:
#        pass
    if timeindex[0] == -1:
        timeindex[0] = 0
    # mark FCs
    try:
        timeindex[2] = max(0,int(header_row[19]))
    except Exception: # pylint: disable=broad-except
        pass
    # mark SCs
    try:
        if (max(0,int(header_row[21])) < max(0,int(header_row[19]))):
            timeindex[1] = max(0,int(header_row[21]))
        else:
            timeindex[4] = max(0,int(header_row[21]))    
    except Exception: # pylint: disable=broad-except
        pass
# not sure if index 23 holds the correct data
#    # mark DROP
#    try:
#        end = int(header_row[23])
#        if end != 0:
#            timeindex[6] = max(0,min(end,len(timex)-1))
#    except:
#        pass
    if timeindex[6] == 0:
        timeindex[6] = max(0,len(timex)-1)

    res['mode']= 'C'

    res['timex'] = timex
    res['temp1'] = temp1
    res['temp2'] = temp2
    res['timeindex'] = timeindex

    res['extradevices'] = [25,25,25]
    res['extratimex'] = [timex[:],timex[:],timex[:]]
    res['extraname1'] = ['{3}',toString(b'\u6392\u6ebc'),'{1}']
    res['extratemp1'] = [extra1,extra3,extra5]
    res['extramathexpression1'] = ['','','']
    res['extraCurveVisibility1']=[False, True, False]
    res['extradevicecolor1'] = ['black', '#55ff00', '#ffaa00']
    res['extraDelta1'] = [False, False, False]

    res['extraname2'] = ['{0}',toString(b'\u58d3\u5dee'),toString(b'\u0394\u6ebc\u5ea6')]
    res['extratemp2'] = [extra2,extra4,extra6]
    res['extramathexpression2'] = ['','','']
    res['extraCurveVisibility2']=[False, True, True]
    res['extradevicecolor2'] = ['black', '#ff55ff', '#aaaaff']
    res['extraDelta2'] = [False, True, False]

    if len(specialevents) > 0:
        res['specialevents'] = specialevents
        res['specialeventstype'] = specialeventstype
        res['specialeventsvalue'] = specialeventsvalue
        res['specialeventsStrings'] = specialeventsStrings
        if heater_event or fan_event:
            # first set etypes to defaults
            res['etypes'] = [QApplication.translate('ComboBox', 'Air'),
                             toString(b'\u6efe\u7b52'),
                             'Damper',
                             QApplication.translate('ComboBox', 'Burner'),
                             '--']
            # update
            if fan_event:
                res['etypes'][0] = toString(b'\u98a8')
            if heater_event:
                res['etypes'][3] = toString(b'\u706b')

    return res
