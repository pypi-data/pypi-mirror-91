#!/usr/bin/env python3

import io
import os

from gv_utils import enums
import numpy as np
import pandas as pd

ENCODING = 'utf8'
CSVSEP = ';'
TEMPCSVSEP = ','

SAMPLES = enums.CsvData.samples
TIMESTAMP = enums.CsvData.timestamp


def dumps_indicators(data):
    csvbuffer = io.BytesIO()
    if isinstance(data, dict):
        timestamp, samples = data[TIMESTAMP], data[SAMPLES]
        metrics = None
        for sampleid, sample in samples.items():
            if metrics is None:
                metrics = list(sample.keys())
                headers = [str(timestamp), ] + metrics
                csvbuffer.write(CSVSEP.join(headers).encode(ENCODING))
            csvbuffer.write(os.linesep.encode(ENCODING))
            values = [str(sampleid), ]
            for metric in metrics:
                value = sample.get(metric, -1)
                if isinstance(value, float):
                    value = round(value)
                values.append(str(value))
            csvbuffer.write(CSVSEP.join(values).encode(ENCODING))
    else:
        data.fillna(-1, inplace=True)
        try:
            data = data.astype('int')
        except:
            pass
        data.to_csv(csvbuffer, sep=CSVSEP)
    csvdata = csvbuffer.getvalue()
    csvbuffer.close()
    return csvdata


def loads_indicators(csvdata):
    dataframe = pd.read_csv(io.BytesIO(csvdata), sep=CSVSEP, index_col=0)
    dataframe.replace(-1, np.NaN, inplace=True)
    dataframe.replace('-1', np.NaN, inplace=True)
    return dataframe


def dumps_zones_travel_time(dictdata, timestamp):
    csvbuffer = io.BytesIO()
    csvbuffer.write(CSVSEP.join([str(timestamp), 'tozonepointeid', 'traveltime', 'path']).encode(ENCODING))
    for fromzpeid, traveltimes in dictdata.items():
        csvbuffer.write(os.linesep.encode(ENCODING))
        for tozpeid, traveltime in traveltimes.items():
            traveltime, path = traveltime
            values = [str(fromzpeid), str(tozpeid)]
            if isinstance(traveltime, float):
                traveltime = round(traveltime)
            values.append(str(traveltime))
            values.append(path)
            csvbuffer.write(CSVSEP.join(values).encode(ENCODING))
    return csvbuffer
