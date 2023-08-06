# -*- coding: utf-8 -*-

###################################################################################################
# (C) 2021 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences, Potsdam, Germany  #
#                                                                                                 #
# This file is part of dastools.                                                                  #
#                                                                                                 #
# dastools is free software: you can redistribute it and/or modify it under the terms of the GNU  #
# General Public License as published by the Free Software Foundation, either version 3 of the    #
# License, or (at your option) any later version.                                                 #
#                                                                                                 #
# dastools is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without   #
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU   #
# General Public License for more details.                                                        #
#                                                                                                 #
# You should have received a copy of the GNU General Public License along with this program. If   #
# not, see https://www.gnu.org/licenses/.                                                         #
###################################################################################################

import logging
import os
from copy import copy
from datetime import timedelta
from obspy import UTCDateTime
from abc import ABCMeta
from abc import abstractmethod


class Archive(metaclass=ABCMeta):
    """Base class for the different structures an archive can have"""

    @abstractmethod
    def __init__(self, root, experiment, strictcheck):
        """Define the root directory where files should be archived and
        whether the archival process should strictly check a coherency in
        the order of the records.

        :param root: Directory where files should be archived
        :type root: str
        :param strictcheck: Flag declaring whether to check that this chunk can be appended in case of existing data
        :type strictcheck: bool
        """
        pass

    @abstractmethod
    def archive(self, trace):
        """Archive mseed

        :param trace: Trace to archive
        :type trace: obspy.Trace
        """
        pass


class StreamBasedHour(Archive):
    """Class to archive miniSEED in 1-hour files per stream

    Output file should not contain GAPS"""

    def __init__(self, root='.', experiment=None, strictcheck=True):
        """Define the root directory where files should be archived and
        whether the archival process should strictly check a coherency in
        the order of the records.

        :param root: Directory where files should be archived
        :type root: str
        :param experiment: Name of the experiment
        :type experiment: str
        :param strictcheck: Flag declaring whether to check that this chunk can be appended in case of existing data
        :type strictcheck: bool
        """
        self.__root = root
        self.__experiment = experiment
        self.__strictcheck = strictcheck
        self.__add2files = set()

    def archive(self, trace):
        """Archive mseed

        :param trace: Trace to archive
        :type trace: obspy.Trace
        """
        logs = logging.getLogger('StreamBasedHour')
        sta = trace.stats.station

        logs.debug('Trace to archive:  %s' % trace)

        # Start of the chunk to archive round to a second!
        auxstart = copy(trace.stats.starttime)
        auxstart.microsecond = 0

        while auxstart < trace.stats.endtime:
            dir2check = os.path.join(self.__root, '%d' % auxstart.year,
                                     self.__experiment)

            auxend = copy(auxstart)
            # Set auxend to the beginning of the next hour
            auxend.minute = 0
            auxend.second = 0
            auxend.microsecond = 0
            auxend = auxend + timedelta(hours=1)

            logs.debug('From %s to %s' % (auxstart, auxend))

            if not os.path.isdir(dir2check):
                os.makedirs(dir2check)

            # Open file for this hour
            filename = '%s.%s.%04d.%02d.%02d.%02d.%02d.%02d.mseed' % (self.__experiment,
                                                                      sta,
                                                                      auxstart.year,
                                                                      auxstart.month,
                                                                      auxstart.day,
                                                                      auxstart.hour,
                                                                      auxstart.minute,
                                                                      auxstart.second)
            # Add only in the case that I have already created this file
            # in this run. Otherwise, create it.
            if filename in self.__add2files:
                mode = 'ab'
            else:
                mode = 'wb'
                self.__add2files.add(filename)

            with open(os.path.join(dir2check, filename), mode) as fout:

                hourtrace = trace.slice(starttime=auxstart,
                                        endtime=auxend,
                                        nearest_sample=False)
                hourtrace.write(fout, format='MSEED', reclen=512)

            # Move to the next day
            auxstart = copy(auxend)


class StreamBased(Archive):
    """Class to archive miniSEED in one file per stream

    GAPS will not be removed from the output file"""

    def __init__(self, root='.', experiment=None, strictcheck=True):
        """Define the root directory where files should be archived and
        whether the archival process should strictly check a coherency in
        the order of the records.

        :param root: Directory where files should be archived
        :type root: str
        :param strictcheck: Flag declaring whether to check that this chunk can be appended in case of existing data
        :type strictcheck: bool
        """
        self.__root = root
        self.__experiment = experiment
        self.__strictcheck = strictcheck
        self.__add2files = set()
        self.__uniquestart = None

    def archive(self, trace):
        """Archive mseed

        :param trace: Trace to archive
        :type trace: obspy.Trace
        """

        if self.__uniquestart is None:
            # Start of the chunk to archive round to a second!
            self.__uniquestart = copy(trace.stats.starttime)
            self.__uniquestart.microsecond = 0

        dir2check = os.path.join(self.__root, '%d' % self.__uniquestart.year,
                                 self.__experiment)

        filename = '%s.%s.%04d.%02d.%02d.%02d.%02d.%02d.mseed' % (self.__experiment,
                                                                  trace.stats.station,
                                                                  self.__uniquestart.year,
                                                                  self.__uniquestart.month,
                                                                  self.__uniquestart.day,
                                                                  self.__uniquestart.hour,
                                                                  self.__uniquestart.minute,
                                                                  self.__uniquestart.second)

        # Add only in the case that I have already created this file
        # in this run. Otherwise, create it.
        if filename in self.__add2files:
            mode = 'ab'
        else:
            mode = 'wb'
            self.__add2files.add(filename)

        # Check that the directory exists
        if not os.path.isdir(dir2check):
            os.makedirs(dir2check)

        with open(os.path.join(dir2check, filename), mode) as fout:
            # TODO How would be the best approach to check that it is OK to append?
            if self.__strictcheck:
                pass
            # Write the output rounded to a full second
            round2second = trace.slice(starttime=self.__uniquestart,
                                       nearest_sample=False)
            round2second.write(fout, format='MSEED', reclen=512)


class SDS(Archive):
    """Class to archive miniSEED in an SDS structure"""
    def __init__(self, root='.', experiment=None, strictcheck=True):
        """Define the root directory of the SDS structure

        The structure is defined as
        <root>/YEAR/NET/STA/CHAN.TYPE/NET.STA.LOC.CHAN.TYPE.YEAR.DAY

        :param root: Root directory of the SDS structure
        :type root: str
        :param strictcheck: Flag to declare if the miniSEED chunk should always be parsed to check proper directory structure
        :type strictcheck: bool
        """
        self.__root = root
        self.__strictcheck = strictcheck
        self.__add2files = set()
        if strictcheck:
            logging.warning('Strict Check was not implemented in SDS class')

    def archive(self, trace):
        """Archive mseed

        :param trace: Trace to archive
        :type trace: obspy.Trace
        """
        logs = logging.getLogger('SDS')
        nslc = '%s.%s.%s.%s' % (trace.stats.network, trace.stats.station,
                                trace.stats.location, trace.stats.channel)
        logs.info('Archiving %s %s %s' % (nslc,
                                          trace.stats.starttime,
                                          trace.stats.endtime))
        # Check the stream code
        try:
            n, s, l, c = nslc.split('.')
        except ValueError:
            if nslc.count('.') != 3:
                raise Exception('Wrong format in NSLC code: %s' % nslc)
            else:
                raise
        except Exception:
            raise

        # Check that the directory exists
        for year in range(trace.stats.starttime.year, trace.stats.endtime.year+1):
            dir2check = os.path.join(self.__root, str(year),
                                     trace.stats.network,
                                     trace.stats.station,
                                     '%s.D' % c)
            if os.path.isdir(dir2check):
                continue
            else:
                os.makedirs(dir2check)

        # Start of the chunk to archive
        auxstart = copy(trace.stats.starttime)
        while auxstart < trace.stats.endtime:
            dir2check = os.path.join(self.__root, str(auxstart.year),
                                     trace.stats.network,
                                     trace.stats.station, '%s.D' % c)
            auxend = UTCDateTime(auxstart.date + timedelta(days=1))
            logs.debug('From %s to %s' % (UTCDateTime(auxstart.date), auxend))

            # Open file for this day
            filename = '%s.D.%d.%03d' % (nslc,
                                         auxstart.year,
                                         auxstart.timetuple().tm_yday)

            # Add only in the case that I have already created this file
            # in this run. Otherwise, create it.
            if filename in self.__add2files:
                mode = 'ab'
            else:
                mode = 'wb'
                self.__add2files.add(filename)

            with open(os.path.join(dir2check, filename), mode) as fout:
                daytrace = trace.slice(starttime=auxstart,
                                       endtime=auxend,
                                       nearest_sample=False)
                daytrace.write(fout, format='MSEED', reclen=512)

            # Move to the next day
            auxstart = copy(auxend)
