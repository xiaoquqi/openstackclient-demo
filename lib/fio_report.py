# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2015 Huron Technologies <http://www.hihuron.com/>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Module for fio report analysis

# Fio Sample:

read4k-rand: (groupid=0, jobs=8): err= 0: pid=34199: Fri Jul 10 17:43:48 2015
  read : io=70076KB, bw=1151.8KB/s, iops=283, runt= 60843msec
    slat (usec): min=1, max=873941, avg=20130.58, stdev=109667.45
    clat (msec): min=7, max=3217, avg=874.74, stdev=241.20
     lat (msec): min=7, max=3217, avg=894.97, stdev=254.25
    clat percentiles (msec):
     |  1.00th=[  255],  5.00th=[  603], 10.00th=[  676], 20.00th=[  742],
     | 30.00th=[  783], 40.00th=[  840], 50.00th=[  865], 60.00th=[  889],
     | 70.00th=[  922], 80.00th=[  963], 90.00th=[ 1037], 95.00th=[ 1221],
     | 99.00th=[ 1795], 99.50th=[ 1926], 99.90th=[ 2606], 99.95th=[ 2704],
     | 99.99th=[ 3163]
    bw (KB  /s): min=    0, max=  240, per=12.42%, avg=142.99, stdev=29.22
    lat (msec) : 10=0.02%, 20=0.07%, 50=0.07%, 100=0.14%, 250=0.66%
    lat (msec) : 500=1.92%, 750=18.60%, 1000=65.73%, 2000=13.81%, >=2000=0.42%
  cpu          : usr=0.01%, sys=0.02%, ctx=1534, majf=0, minf=260

# Report Return:

    * IOPS(count/s)
    * Bandwidth(MB/s)
    * Clat Avg(ms)
    * Lat Avg(ms)
    * Clat Percentiles

    read4k-rand: 283 874.74 894.97 1.12
"""

import logging
import re

# Fields need to be parsed
FIELDS = ["iops", "clat_avg", "lat_avg", "bandwidth"]

class FioReport(object):
    """Parse fio report"""

    def __init__(self):
        """Initial method for fio report

        To analysis an combined report, you should use split_report
        to split the report first then you will get a dict contains all the result

        To analysis a seperate report, you should use parse_report, and
        pass in a report string
        """
        pass

    def split_report(self, lines):
        """Split fio reports and analysis after seperate

        lines is an list contains all fio reports
        """
        start_line = 0
        end_line = 0
        fio_reports = []
        for index in range(len(lines)):
            if self._is_start(lines[index]):
                start_line = index
                end_line = 0
                logging.debug("Found start line %s" % lines[index])
                logging.debug("Start line index is %s" % start_line)

            if self._is_end(lines[index]):
                end_line = index
                logging.debug("Found end line %s" % lines[index])
                logging.debug("End line index is %s" % end_line)
                parse_lines = lines[start_line:end_line]
                logging.debug("Parsing text: %s" % parse_lines)
                fio_data = self.parse_report("\n".join(parse_lines))
                fio_reports.append(fio_data)

        return fio_reports

    def parse_report(self, report):
        """Parse a single part of report

        report is a str contains a seperate fio report
        """
        fio_data = {
           "name": self._get_name(report),
           "iops": self._get_iops(report),
           "bandwidth": self._get_bandwidth(report),
           "clat_avg": self._get_clat_avg(report),
           "lat_avg": self._get_lat_avg(report),
           "clats": self._get_clat_dist(report)
        }
        return fio_data

    def _is_start(self, line):
        """Return true if report start

        read4k-rand: (groupid=0, jobs=8): err= 0: pid=34199: Fri Jul 10 17:43:48 2015
        """
        if re.match(".*\:\s*\(groupid", line):
            return True

    def _is_end(self, line):
        """Return true if report end

        As we just want to analysis IOPS, Bandwidth and latency
        to avoid report recieved abnormally our line end at any
        postion has submit/complete/issued/latency
        """
        if re.match("\s+submit|complete|issued|latency\s+\:\s+.*", line):
            return True

    def _get_name(self, report):
        """Get test case name

        read4k-rand: (groupid=0, jobs=8): err= 0: pid=34199: Fri Jul 10 17:43:48 2015
        """
        match = re.search("(.*)\:\s*\(groupid", report)
        if match:
            return match.group(1)

    def _get_iops(self, report):
        """Get iops from result

        read : io=70076KB, bw=1151.8KB/s, iops=283, runt= 60843msec
        """
        match = re.search("iops\=(\d+)", report)
        if match:
            return int(match.group(1))

    def _get_bandwidth(self, report):
        """Get bandwidth from result

        write: io=6500.0KB, bw=665533 B/s, iops=162 , runt= 10001msec
        """
        match = re.search("bw\=\s*(\d+\.{0,1}\d*)\s*(\w+)\/s",
                report)
        if match:
            bandwidth = float(match.group(1))
            unit = match.group(2)
            if unit.lower() == 'b':
                bandwidth = round(bandwidth / 1024 / 1024, 2)
            elif "kb" in unit.lower():
                bandwidth = round(bandwidth / 1024, 2)
            elif "gb" in unit.lower():
                bandwidth = round(bandwidth * 1024, 2)

            return bandwidth

    def _get_clat_avg(self, report):
        """Get clat average from result

        clat (msec): min=7, max=3217, avg=874.74, stdev=241.20
        """
        match = re.search(".*clat\s*\((\w+)\).*avg\=\s*(\d+\.{0,1}\d*)",
                report)
        if match:
            unit = match.group(1)
            value = float(match.group(2))
            if unit.lower() == "usec":
                value = value / 1000
            return value

    def _get_lat_avg(self, report):
        """Get lat average from result

        lat (usec): min=219, max=270254, avg=5508.93, stdev=15993.36
        """
        match = re.search("\s*lat\s*\((\w+)\).*avg\=\s*(\d+\.{0,1}\d*)",
                report)
        if match:
            unit = match.group(1)
            value = float(match.group(2))
            if unit.lower() == "usec":
                value = value / 1000
            return value

    def _get_clat_dist(self, report):
        """Get clat distributon

        clat percentiles (usec):
         |  1.00th=[ 2160],  5.00th=[ 2960], 10.00th=[ 3728], 20.00th=[ 5024],
         | 30.00th=[ 6240], 40.00th=[ 7392], 50.00th=[ 8512], 60.00th=[ 9920],
         | 70.00th=[12224], 80.00th=[15424], 90.00th=[18304], 95.00th=[22400],
         | 99.00th=[28032], 99.50th=[31360], 99.90th=[35072], 99.95th=[36608],
         | 99.99th=[41728]
        """
        fio_clats = []

        unit = "msec"
        match = re.search("clat percentiles \((\w+)\)", report)
        if match:
            unit = match.group(1)

        match = re.findall("(\d+\.\d+)th\=\[\s*(\d+)\\s*]", report)
        if match:
            for percent, clat in match:
                if unit == "usec":
                    clat = float(clat) / 1000
                elif unit == "msec" :
                    clat = float(clat)
                else:
                    print "WARNING: Unit %s can not be handled." % unit
                fio_clats.append([percent, clat])
            return fio_clats


class PrintReport(object):
    """Print fio report"""

    def __init__(self, fio_reports):
        """Intialization method

        fio_reports format:
        [
            {"name": "4k-rand-write", ...},
            {"name": "4k-rand-read", ...}
        ]
        """
        self.fio_reports = fio_reports
        self.reports = {}

    def output(self):
        for report in self.fio_reports:
            name = report.get("name")
            if name is None:
                print "WARNING: name is missing, ignore"
                continue
            self._handle_report(name, report)

        self._cal_avg()
        self._gen_report()

    def _handle_report(self, name, report):
        """Merge report"""
        if self.reports.get(name) is None:
            self.reports[name] = report
            self.reports[name]['count'] = 1
        else:
            self._add_values(self.reports[name], report)
            self.reports[name]['count'] += 1

    def _cal_avg(self):
        """Calcuate average"""
        for name in self.reports:
            report = self.reports[name]
            count = report['count']
            for f in FIELDS:
                report[f] = round(report[f] / count, 2)

            for i in range(len(report["clats"])):
                value = report["clats"][i][1]
                report["clats"][i][1] = round(value / count, 2)

    def _gen_report(self):
        """Print report to stdout"""
        print "------------------------------------------"
        print "fio report"
        print "------------------------------------------"
        print "name", " ".join(f for f in FIELDS)
        # print fields
        for name in sorted(self.reports):
            report = self.reports[name]
            #print report
            print name, " ".join(str(report.get(f)) for f in FIELDS)

        print "*******************************************"
        # print clats
        index = 0
        for name in sorted(self.reports):
            report = self.reports[name]
            if index == 0:
                print "clat_percent", " ".join(
                        str(c[0]) for c in report["clats"])
            print name, " ".join(str(c[1]) for c in report["clats"])
            index += 1

    def _add_values(self, pre_report, report):
        """Make sum of all values"""
        for f in FIELDS:
            pre_report[f] += report[f]

        clats = report.get("clats")
        for i in range(len(clats)):
            value = float(clats[i][1])
            pre_report["clats"][i][1] += value
