#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
   pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2010-2021 by Christoph Schueler <cpu12.gems.googlemail.com>

   All Rights Reserved

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

   s. FLOSS-EXCEPTION.txt
"""
__author__ = "Christoph Schueler"
__version__ = "0.10.2"


import pkgutil
import sys
from os import path

import pya2l.model as model
from pya2l.logger import Logger
from pya2l.templates import doTemplateFromText


class InvalidA2LDatabase(Exception):
    """"""

    pass


class DB(object):
    """"""

    A2L_TEMPLATE = pkgutil.get_data("pya2l.cgen.templates", "a2l.tmpl")

    logger = Logger(__name__)

    def import_a2l(
        self,
        file_name,
        debug=False,
        in_memory=False,
        remove_existing=False,
        encoding="latin-1",
    ):
        """Import `.a2l` file to `.a2ldb` database.


        Parameters
        ----------
        file_name: str
            Name of the A2L to be imported. If you don't specify an extension ``.a2l`` is added.

        debug: bool
            Additional debugging output.

        in_memory: bool
            Create non-persistent in-memory database.

        remove_existing: bool
            ** DANGER ZONE **: Remove existing database.

        Returns
        -------
        SQLAlchemy session object.

        Raises
        ------
        OSError
            If database already exists.

        Note
        ----
        ``AML`` and ``IF_DATA`` sections are currently not processed.
        """
        from os import unlink

        from pya2l.a2l_listener import A2LListener, cut_a2ml
        from pya2l.parserlib import ParserWrapper

        self.in_memory = in_memory

        parser = ParserWrapper("a2l", "a2lFile", A2LListener, debug=debug)
        self._set_path_components(file_name)
        if not in_memory:
            if remove_existing:
                try:
                    unlink(self._dbfn)
                except Exception:
                    pass
            elif path.exists(self._dbfn):
                raise OSError("file '{}' already exists.".format(self._dbfn))
        data = open(self._a2lfn, encoding=encoding).read()
        data, a2ml = cut_a2ml(data)
        self.db = parser.parseFromString(data, dbname=self._dbfn)
        self.session = self.db.session
        return self.session

    def export_a2l(self, file_name=sys.stdout, encoding="ascii"):
        """"""
        namespace = dict(session=self.db.session, model=model)
        data = doTemplateFromText(
            self.A2L_TEMPLATE, namespace, formatExceptions=False, encoding=encoding
        )
        result = []
        for line in data.splitlines():
            line = line.rstrip()
            if not line:
                continue
            else:
                result.append(line)
        result = "\n".join(result)
        print(result)
        # with io.open("{}.render".format(file_name), "w", encoding = encoding, newline = "\r\n") as outf:
        #    outf.write(res)

    def open_create(self, file_name):
        """Open or create an A2LDB."""
        self.in_memory = False
        self._set_path_components(file_name)
        if not path.exists(self._dbfn):
            return self.import_a2l(self._a2lfn)
        else:
            return self.open_existing(self._dbfn)

    def open_existing(self, file_name):
        """Open an existing `.a2ldb` database.

        Parameters
        ----------
        file_name: str
            Name of your database file, resulting from :meth:`import_a2l`.
            Extension `.a2ldb` not needed.

        Returns
        -------
        SQLAlchemy session object.

        Raises
        ------
        OSError
            If database already exists.
        """
        self.in_memory = False
        self._set_path_components(file_name)
        if not path.exists(self._dbfn):
            raise OSError("file '{}' does not exists.".format(self._dbfn))
        else:
            self.db = model.A2LDatabase(self._dbfn)
            self.session = self.db.session
            res = self.session.query(model.MetaData).first()
            if res:
                return self.session
            else:
                raise InvalidA2LDatabase(
                    "Database seems to be corrupted. No meta-data found."
                )

    def _set_path_components(self, file_name):
        """"""
        self._pth, self._base = path.split(file_name)
        fbase, ext = path.splitext(self._base)
        if self.in_memory:
            self._dbfn = ":memory:"
        else:
            self._dbfn = path.join(self._pth, "{}.a2ldb".format(fbase))
        if not ext or ext.lower() == ".a2l" or ext.lower() == ".a2ldb":
            self._a2lfn = "{}.a2l".format(fbase)
        else:
            self._a2lfn = "{}{}".format(fbase, ext)
        self._a2lfn = path.join(self._pth, self._a2lfn)
