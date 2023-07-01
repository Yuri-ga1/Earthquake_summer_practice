import os
import datetime
import pytest
import h5py
import numpy as np
import matplotlib.pyplot as plt

from earthquake import retrieve_data, plot_map, _UTC



file_path = os.path.join(os.path.dirname(__file__), "roti_01_17.h5")
print(file_path)
times = [
        datetime.datetime(2023, 2, 6, 1, 17),
         datetime.datetime(2023, 2, 6, 1, 32),
         datetime.datetime(2023, 2, 6, 1, 37)
    ]
times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in times]
data = retrieve_data(file_path, "ROTI", times)
_data={"ROTI":data}

plot_map(
            plot_times=times,
            data=_data,
            type_d="ROTI",
            ncols=3,
            lon_limits=(25, 50),
            lat_limits=(25, 50)
        )

