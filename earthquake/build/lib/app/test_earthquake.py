import os
import datetime
import pytest
import h5py
import numpy as np
import matplotlib.pyplot as plt

from earthquake import retrieve_data, plot_map, _UTC


@pytest.fixture(scope="module")
def sample_file_path():
    # Assuming the sample file is named 'roti_01_17.h5' and is in the same directory as the test file
    file_path = os.path.join(os.path.dirname(__file__), "roti_01_17.h5")
    return file_path


@pytest.fixture(scope="module")
def sample_data(sample_file_path):
    times = [
        datetime.datetime(2023, 2, 6, 1, 17),
         datetime.datetime(2023, 2, 6, 1, 32),
         datetime.datetime(2023, 2, 6, 1, 37)
    ]
    times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in times]
    data = retrieve_data(sample_file_path, "ROTI", times)
    _data={'ROTI':data}
    return _data


def test_retrieve_data(sample_file_path):
    # Check if the file exists
    assert os.path.isfile(sample_file_path)

    # Test retrieving data without specific times
    data = retrieve_data(sample_file_path, "ROTI")
    assert isinstance(data, dict)
    assert len(data) > 0

    # Test retrieving data with specific times
    times = [
        datetime.datetime(2023, 2, 6, 1, 17),
         datetime.datetime(2023, 2, 6, 1, 32),
         datetime.datetime(2023, 2, 6, 1, 37)
    ]
    times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in times]
    data = retrieve_data(sample_file_path, "ROTI", times)
    assert isinstance(data, dict)
    assert len(data) == 3
    assert all(time in data.keys() for time in times)


def test_plot_map(sample_file_path, sample_data):
    # Test plotting data without saving the figure
    with pytest.warns(UserWarning):
        plot_map(
            plot_times=list(sample_data["ROTI"].keys())[:3],
            data=sample_data,
            type_d="ROTI",
            lon_limits=(25, 50),
            lat_limits=(25, 50),
            nrows=1,
            ncols=3,
            markers=[],
            sort=False,
            use_alpha=False,
            clims={
                "ROTI": [-0, 0.5, "TECu/min"]
            },
            savefig=""
        )

    # Test plotting data and saving the figure
    savefig_path = os.path.join(os.path.dirname(__file__), "test_figure.png")
    plot_map(
        plot_times=list(sample_data["ROTI"].keys())[:3],
        data=sample_data,
        type_d="ROTI",
        lon_limits=(25, 50),
        lat_limits=(25, 50),
        nrows=1,
        ncols=3,
        markers=[],
        sort=False,
        use_alpha=False,
        clims={
            "ROTI": [-0, 0.5, "TECu/min"]
        },
        savefig=savefig_path
    )
    assert os.path.isfile(savefig_path)
    os.remove(savefig_path)
    
pytest.main()