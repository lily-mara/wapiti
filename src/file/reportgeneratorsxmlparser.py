#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Report Generators Parser for Wapiti Project
# Wapiti Project (http://wapiti.sourceforge.net)
#
# David del Pozo
# Copyright (C) 2011 Germinus XXI
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from xml.parsers import expat
from report.reportgeneratorinfo import ReportGeneratorInfo

class ReportGeneratorsXMLParser:

    REPORT_GENERATOR = "reportGenerator"
    REPORT_GENERATOR_KEY = "reportTypeKey"
    REPORT_GENERATOR_CLASS_MODULE = "classModule"
    REPORT_GENERATOR_CLASSNAME = "className"

    reportGenerators = []
    repGen = None
    tag = ""

    def __init__(self):
        self._parser = expat.ParserCreate()
        self._parser.StartElementHandler  = self.start_element
        self._parser.EndElementHandler    = self.end_element
        self._parser.CharacterDataHandler = self.char_data

    def parse(self,fileName):
        f = None
        try:
            f = open(fileName)
            content = f.read()
            self.feed(content)
        finally:
            if f!=None:
                f.close()

    def feed(self, data):
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start_element(self, name, attrs):
        if name == self.REPORT_GENERATOR:
            self.repGen = ReportGeneratorInfo()
        elif name == self.REPORT_GENERATOR_KEY:
            self.tag = self.REPORT_GENERATOR_KEY
        elif name == self.REPORT_GENERATOR_CLASSNAME:
            self.tag = self.REPORT_GENERATOR_CLASSNAME
        elif name == self.REPORT_GENERATOR_CLASS_MODULE:
            self.tag = self.REPORT_GENERATOR_CLASS_MODULE

    def end_element(self, name):
        if name == self.REPORT_GENERATOR:
            self.reportGenerators.append(self.repGen)

    def char_data(self, data):
        if self.tag == self.REPORT_GENERATOR_KEY:
            self.repGen.setKey(data)
        elif self.tag == self.REPORT_GENERATOR_CLASSNAME:
            self.repGen.setClassName(data)
        elif self.tag == self.REPORT_GENERATOR_CLASS_MODULE:
            self.repGen.setClassModule(data)
        self.tag = ""

    def getReportGenerators(self):
        return self.reportGenerators

