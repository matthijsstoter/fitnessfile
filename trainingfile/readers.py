from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass, field
from abc import ABC, abstractmethod, abstractproperty
import pathlib
from typing import Any

import pandas as pd
from fitparse import FitFile
import gpxpy
import gpxpy.gpx


class TrainingFileReader(ABC):
    """Abstract base class for all classes responsible for reading the training load file"""
    
    @abstractproperty
    def file_type(self) -> str:
        "Returns the filetype as a str"
    
    @abstractmethod
    def read_file(self) -> pd.DataFrame:
        """Reading the file containing the training load data into a Pandas DataFrame"""
    
    @abstractproperty
    def training_type(self) -> str:
        """Retrieving the training type"""
    
    @abstractproperty
    def start_time(self) -> datetime:
        "Retrieving the training start time"
    
    @abstractmethod
    def duration(self, raw_duration: float) -> float:
        "Computing the training duration"
    

@dataclass
class FitFileReader(TrainingFileReader):

    filepath: pathlib.Path
    file: FitFile = field(init=False)
    _filepath_str: str = field(init=False)


    def __post_init__(self):
        self._filepath_str = str(self.filepath)
        self.file: FitFile = FitFile(self._filepath_str)
    
    @property
    def file_type(self) -> str:
        return self.filepath.suffix
    
    def read_file(self) -> pd.DataFrame:
        try:
            raw_data = defaultdict(list)

            for record in self.file.get_messages():
                if record.mesg_type is None or record.mesg_type.name != 'record':
                    continue

                for record_data in record:
                    raw_data[record_data.name].append(record_data.value)

            # Creating a Pandas DataFrame 'df' using raw_data as the input, timestamp as index
            df = pd.DataFrame(raw_data).set_index('timestamp')
        
        except ValueError:
            # Accounting for faulty files in which not all list are of equal length, due to missing values
            cols = list()
            raw_data = defaultdict(list)

            # Enumerating over the fitfile. fitfile.get_messages retrieves the messages in the fit-file
            for record in self.file.get_messages():

                if record.name == 'record':
                    for record_data in record:
                        if record_data.name not in cols:
                            cols.append(record_data.name)
            
            for record in self.file.get_messages():
                if record.name == 'record':
                    for record_data in record:
                        for col in cols:
                            raw_data[col].append(record.get_value(col))
            
            # Creating a Pandas DataFrame 'df' using raw_data as the input, timestamp as index
            df = pd.DataFrame(raw_data).set_index('timestamp')
            
        # Removing duplicated rows
        return df.loc[~df.index.duplicated(keep='first')]
    
    @property
    def training_type(self) -> str:
        return self._get_info(key="session", value="sport")
    
    @property
    def start_time(self) -> datetime:
        return self._get_info(key="file_id", value="time_created")
    
    def _get_info(self, key: str, value: str) -> Any:
        "Retrieve relevant information from the FitFile, such as start time and training type"
        for record in self.file.get_messages():
            if record.name == key:
                return record.get_value(value) 
    
    def duration(self, raw_duration) -> float:
        return (raw_duration.total_seconds() + 1)/60


@dataclass
class CSVFileReader(TrainingFileReader):
    filepath: pathlib.Path
    _cols: dict[str, str] = field(init=False)
    _filepath_str: str = field(init=False)

    def __post_init__(self):
        self._filepath_str = str(self.filepath)
        self._cols = {'activityType': 'activity_type',
                      'lapNumber': 'lap_number',
                      'lat': 'position_lat',
                      'long': 'position_',
                      'heartRate': 'heart_rate'}
    
    def read_file(self) -> pd.DataFrame:
        df = pd.read_csv(self._filepath_str)
        df.rename(columns=self._cols, inplace=True)
        return df.loc[~df.index.duplicated(keep='first')]
    
    @property
    def file_type(self) -> str:
        return self.filepath.suffix
    
    @property
    def start_time(self) -> datetime:
        date_time = self.filepath.name.split("-", 1)[1] #Remove training type
        date_time = date_time.split(".", 1)[0] #Remove file extension
        date_str, time_str = date_time.split("T", 1)
        
        year, month, day = int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8])
        hour, minute, second = int(time_str[0:2]), int(time_str[2:4]), int(time_str[4:6])
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    
    @property
    def training_type(self) -> str:
        return self.filepath.name.split("-", 1)[0]
    
    def duration(self, raw_duration: float) -> float:
        return raw_duration / 60


# @dataclass
# class GPXReader(TrainingFileReader):
#     file: pathlib.Path


#     def read_file(self) -> pd.DataFrame:
#         # Parsing an existing file:
#         # -------------------------

#         # # gpx_file = file
#         # with open(file) as f:
#         #     # gpx = gpxpy.parse(f)

        

#         gpx = gpxpy.parse(str(self.file))

#         for track in gpx.tracks:
#             for segment in track.segments:
#                 for point in segment.points:
#                     print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

#         for waypoint in gpx.waypoints:
#             print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

#         for route in gpx.routes:
#             print('Route:')
#             for point in route.points:
#                 print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

#         # There are many more utility methods and functions:
#         # You can manipulate/add/remove tracks, segments, points, waypoints and routes and
#         # get the GPX XML file from the resulting object:

#         print('GPX:', gpx.to_xml())

#         # Creating a new file:
#         # --------------------

#         gpx = gpxpy.gpx.GPX()

#         # Create first track in our GPX:
#         gpx_track = gpxpy.gpx.GPXTrack()
#         gpx.tracks.append(gpx_track)

#         # Create first segment in our GPX track:
#         gpx_segment = gpxpy.gpx.GPXTrackSegment()
#         gpx_track.segments.append(gpx_segment)

#         # Create points:
#         gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1234, 5.1234, elevation=1234))
#         gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1235, 5.1235, elevation=1235))
#         gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1236, 5.1236, elevation=1236))

#         # You can add routes and waypoints, too...

#         print('Created GPX:', gpx.to_xml())

#         return None
    
#     @property
#     def file_type(self) -> str:
#         return "gpx"
    
#     @property
#     def start_time(self) -> datetime:
#         pass

#     @property
#     def training_type(self) -> str:
#         pass

#     def duration(self, raw_duration: float) -> float:
#         pass