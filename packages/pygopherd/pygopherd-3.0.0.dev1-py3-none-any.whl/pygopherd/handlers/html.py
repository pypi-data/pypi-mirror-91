# pygopherd -- Gopher-based protocol server in Python
# module: Special handling of HTML files
# Copyright (C) 2021 Michael Lazar
# Copyright (C) 2002 John Goerzen
# <jgoerzen@complete.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import html.entities
import html.parser
import mimetypes
import re
import unittest

from pygopherd import testutil
from pygopherd.handlers.base import VFS_Real
from pygopherd.handlers.file import FileHandler


###########################################################################
# HTML File Handler
# Sets the name of a file if it's HTML.
###########################################################################
class HTMLTitleParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.titlestr = ""
        self.readingtitle = 0
        self.gotcompletetitle = 0

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.readingtitle = 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.gotcompletetitle = 1
            self.readingtitle = 0

    def handle_data(self, data):
        if self.readingtitle:
            self.titlestr += data

    def handle_entityref(self, name):
        """Handle things like &amp; or &gt; or &lt;.  If it's not in
        the dictionary, ignore it."""
        if self.readingtitle and name in html.entities.entitydefs:
            self.titlestr += html.entities.entitydefs[name]


class HTMLFileTitleHandler(FileHandler):
    """This class will set the title of a HTML document based on the
    HTML title.  It is a clone of the UMN gsfindhtmltitle function."""

    def canhandlerequest(self):
        if FileHandler.canhandlerequest(self):
            mimetype, encoding = mimetypes.guess_type(self.selector)
            return mimetype == "text/html"
        else:
            return False

    def getentry(self):
        # Start with the entry from the parent.
        entry = FileHandler.getentry(self)
        parser = HTMLTitleParser()

        with self.vfs.open(self.getselector(), "rb") as fp:
            while not parser.gotcompletetitle:
                line = fp.readline()
                if not line:
                    break
                # The PY3 HTML parser doesn't handle surrogateescape
                parser.feed(line.decode(errors="replace"))
            parser.close()

        # OK, we've parsed the file and exited because of either an EOF
        # or a complete title (or error).  Now, figure out what happened.

        if parser.gotcompletetitle:
            # Convert all whitespace sequences to a single space.
            # Removes newlines, tabs, etc.  Good for presentation
            # and for security.
            title = re.sub(r"[\s]+", " ", parser.titlestr)
            entry.setname(title)
        return entry


class TestHTMLHandler(unittest.TestCase):
    def setUp(self) -> None:

        self.config = testutil.getconfig()
        self.vfs = VFS_Real(self.config)
        self.selector = "/testfile.html"
        self.protocol = testutil.gettestingprotocol(self.selector, config=self.config)
        self.stat_result = self.vfs.stat(self.selector)

    def test_pyg_handler(self):
        handler = HTMLFileTitleHandler(
            "/testfile.html", "", self.protocol, self.config, self.stat_result, self.vfs
        )

        self.assertTrue(handler.canhandlerequest())

        entry = handler.getentry()
        self.assertEqual(entry.name, "<Gopher Rocks>")
