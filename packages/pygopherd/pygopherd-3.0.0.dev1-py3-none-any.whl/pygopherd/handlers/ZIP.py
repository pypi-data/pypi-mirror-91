# pygopherd -- Gopher-based protocol server in Python
# module: ZIP transparent handling
# Copyright (C) 2003-2019 John Goerzen
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
from __future__ import annotations

import codecs
import configparser
import dbm
import io
import marshal
import os.path
import re
import shelve
import stat
import time
import typing
import unittest
import zipfile

from pygopherd.handlers.base import BaseHandler, VFS_Real


class MarshalingShelf(shelve.Shelf):
    def __getitem__(self, key: str):
        return marshal.loads(self.dict[key])

    def __setitem__(self, key: str, value):
        self.dict[key] = marshal.dumps(value)


class DbfilenameShelf(MarshalingShelf):
    def __init__(self, filename: str, flag: typing.Literal["r", "w", "c", "n"] = "c"):
        # We can only pass in a string, see https://bugs.python.org/issue38864
        db = dbm.open(filename, flag)
        super().__init__(db)


def shelveopen(
    filename: str, flag: typing.Literal["r", "w", "c", "n"] = "c"
) -> DbfilenameShelf:
    return DbfilenameShelf(filename, flag)


class VFS_Zip(VFS_Real):
    def __init__(
        self, config: configparser.ConfigParser, chain: VFS_Real, zipfilename: str
    ):
        super().__init__(config, chain)
        self.zipfilename = zipfilename
        self.entrycache = {}
        self.badcache = {}
        self._initzip()

    def __del__(self):
        if hasattr(self, "zipfd"):
            self.zipfd.close()

    def _getcachefilename(self) -> str:
        (dir_, file) = os.path.split(self.zipfilename)
        return os.path.join(dir_, ".cache.pygopherd.zip3." + file)

    def _initcache(self) -> bool:
        """Returns 1 if a cache was found existing; 0 if not."""
        filename = self._getcachefilename()
        if isinstance(self.chain, VFS_Real) and self.chain.iswritable(filename):
            fspath = self.chain.getfspath(filename)
            zipfilemtime = self.chain.stat(self.zipfilename)[stat.ST_MTIME]
            try:
                cachemtime = self.chain.stat(filename)[stat.ST_MTIME]
            except OSError:
                self._createcache(fspath)
                return False

            if zipfilemtime > cachemtime:
                self._createcache(fspath)
                return False

            try:
                self.dircache = shelveopen(fspath, "r")
            except Exception:
                self._createcache(fspath)
                return False

            return True

    def _createcache(self, fspath: str) -> None:
        self.dircache = {}
        self.dbdircache = shelveopen(fspath, "n")

    def _savecache(self) -> None:
        if not hasattr(self, "dbdircache"):
            # createcache was somehow unsuccessful
            return
        for (key, value) in self.dircache.items():
            self.dbdircache[key] = value

    def _initzip(self) -> None:
        self.zipfd = self.chain.open(self.zipfilename, mode="rb")
        self.zip = zipfile.ZipFile(self.zipfd)
        if not self._initcache():
            # For reloading an existing one.  Must be called before _cachedir.
            self._cachedir()
            self._savecache()
            self.dbdircache.close()  # Flush it out

    def _isentryincache(self, fspath: str) -> bool:
        try:
            self._getcacheentry(fspath)
            return True
        except KeyError:
            return False

    def _getcacheentry(self, fspath: str) -> typing.Union[dict, str]:
        return self.dircache[self._getcacheinode(fspath)]

    def _getcacheinode(self, fspath: str) -> str:
        inode = "0"
        if fspath == "":
            return inode

        (dir_, file) = os.path.split(fspath)
        if dir_ in self.entrycache:
            return self.entrycache[dir_][file]
        elif dir_ in self.badcache:
            raise KeyError("Call for %s: directory %s non-existant" % (fspath, dir_))

        workingdir = ""

        for item in fspath.split("/"):
            # right now, directory holds the directory from the *last* iteration.
            directory = self.dircache[inode]
            if type(directory) != dict:
                raise KeyError("Call for %s: couldn't find %s" % (fspath, item))
            self.entrycache[workingdir] = directory

            workingdir = os.path.join(workingdir, item)
            try:
                # Now, inode holds the inode number.
                inode = directory[item]
            except KeyError:
                self.badcache[workingdir] = 1
                raise KeyError("Call for %s: Couldn't find %s" % (fspath, item))
        return inode

    def _cachedir(self) -> None:
        symlinkinodes = []
        nextinode = 1
        self.dircache = {"0": {}}

        for info in self.zip.infolist():
            (dir_, filename) = os.path.split(info.filename)
            if dir_ == "/":
                dir_ = ""

            dirlevel = self.dircache["0"]
            for level in dir_.split("/"):
                if level == "":
                    continue
                if level not in dirlevel:
                    self.dircache[str(nextinode)] = {}
                    dirlevel[level] = str(nextinode)
                    nextinode += 1
                dirlevel = self.dircache[dirlevel[level]]

            if len(filename):
                if self._islinkinfo(info):
                    symlinkinodes.append(
                        {
                            "dirlevel": dirlevel,
                            "filename": filename,
                            "pathname": info.filename,
                            "dest": self._readlinkfspath(info.filename),
                        }
                    )
                else:
                    dirlevel[filename] = str(nextinode)
                    self.dircache[str(nextinode)] = info.filename  # used to be location
                    nextinode += 1

        lastsymlinklen = 0
        while len(symlinkinodes) and len(symlinkinodes) != lastsymlinklen:
            lastsymlinklen = len(symlinkinodes)
            newsymlinkinodes = []
            for item in symlinkinodes:
                if item["dest"][0] == "/":
                    dest = item["dest"][1:]
                else:
                    dest = os.path.join(os.path.dirname(item["pathname"]), item["dest"])
                    dest = os.path.normpath(dest)
                if self._isentryincache(dest):
                    item["dirlevel"][item["filename"]] = self._getcacheinode(dest)
                else:
                    newsymlinkinodes.append(item)
            symlinkinodes = newsymlinkinodes

    def _islinkattr(self, attr) -> bool:
        return stat.S_ISLNK(attr >> 16)

    def _islinkinfo(self, info) -> bool:
        if type(info) == dict:
            return False
        return self._islinkattr(info.external_attr)

    def _readlinkfspath(self, fspath: str) -> str:
        return self.zip.read(fspath).decode(errors="surrogateescape")

    def _readlink(self, selector: str) -> str:
        return self._readlinkfspath(self._getfspathfinal(selector))

    def iswritable(self, selector: str) -> bool:
        return False

    def unlink(self, selector: str):
        raise NotImplementedError("VFS_ZIP cannot unlink files.")

    def _getfspathfinal(self, selector: str) -> str:
        # Strip off the filename part.
        selector = selector[len(self.zipfilename) :]

        if selector.startswith("/"):
            selector = selector[1:]

        if selector.endswith("/"):
            selector = selector[:-1]

        return selector

    def getfspath(self, selector: str) -> str:
        # We can skip the initial part -- it just contains the start of
        # the path.

        return self._getfspathfinal(selector)

    def stat(self, selector: str):
        fspath = self.getfspath(selector)
        try:
            zi = self._getcacheentry(fspath)
        except KeyError:
            raise OSError(
                "Entry %s does not exist in %s" % (selector, self.zipfilename)
            )

        if type(zi) == dict:
            # It's a directory.
            return (
                16877,  # mode
                0,  # inode
                0,  # device
                3,  # links
                0,  # uid
                0,  # gid
                0,  # size
                0,  # access time
                0,  # modification time
                0,
            )  # change time

        zi = self.zip.getinfo(fspath)

        zt = zi.date_time
        modtime = time.mktime(zt + (0, 0, -1))
        return (
            33188,  # mode
            0,  # inode
            0,  # device
            1,  # links
            0,  # uid
            0,  # gid
            zi.file_size,  # size
            modtime,  # access time
            modtime,  # modification time
            modtime,
        )  # change time

    def isdir(self, selector: str) -> bool:
        fspath = self.getfspath(selector)
        try:
            item = self._getcacheentry(fspath)
        except KeyError:
            return False

        return type(item) == dict

    def isfile(self, selector: str) -> bool:
        fspath = self.getfspath(selector)
        try:
            item = self._getcacheentry(fspath)
        except KeyError:
            return False

        return type(item) != dict

    def exists(self, selector: str) -> bool:
        fspath = self.getfspath(selector)
        return self._isentryincache(fspath)

    def open(
        self, selector: str, mode: str = "rb", errors: typing.Optional[str] = None
    ) -> typing.IO:

        assert mode in ("r", "rb")

        fspath = self.getfspath(selector)
        try:
            item = self._getcacheentry(fspath)
        except KeyError:
            raise IOError("Request to open %s, which does not exist" % selector)

        if type(item) == dict:
            raise IOError(
                "Request to open %s, which is a directory (%s)" % (selector, str(item))
            )

        # zip.open() will only return the file object in bytes mode
        fp = self.zip.open(item)
        if mode == "r":
            # Attempted to read in "text mode", so decode the bytestream
            fp = codecs.getreader("utf-8")(fp)

        return fp

    def listdir(self, selector: str) -> typing.List[str]:
        fspath = self.getfspath(selector)
        try:
            retobj = self._getcacheentry(fspath)
        except KeyError:
            raise OSError(
                "listdir on %s (%s) failed: no such file or directory"
                % (selector, fspath)
            )

        if type(retobj) != dict:
            raise OSError(
                "listdir on %s failed: that is a file, not a directory.  Got %s"
                % (selector, str(retobj))
            )

        return list(retobj.keys())


class TestVFS_Zip(unittest.TestCase):
    def setUp(self):
        from configparser import ConfigParser

        self.config = ConfigParser()
        self.config.add_section("pygopherd")
        self.config.set("pygopherd", "root", os.path.abspath("testdata"))
        self.real = VFS_Real(self.config)
        self.z = VFS_Zip(self.config, self.real, "/testdata.zip")
        self.z2 = VFS_Zip(self.config, self.real, "/testdata2.zip")
        self.zs = VFS_Zip(self.config, self.real, "/symlinktest.zip")

    def test_listdir(self):
        m1 = self.z.listdir("/testdata.zip")
        m2 = self.z2.listdir("/testdata2.zip")

        m1.sort()
        m2.sort()

        self.assertIn("pygopherd", m1)
        self.assertEqual(m1, m2)
        self.assertEqual(
            m1,
            [
                ".abstract",
                "README",
                "pygopherd",
                "testarchive.tar",
                "testarchive.tar.gz",
                "testarchive.tgz",
                "testfile.txt",
                "testfile.txt.gz",
                "testfile.txt.gz.abstract",
            ],
        )

        m1 = self.z.listdir("/testdata.zip/pygopherd")
        m2 = self.z2.listdir("/testdata2.zip/pygopherd")

        m1.sort()
        m2.sort()

        self.assertEqual(m1, m2 + ["ziponly"])
        self.assertEqual(m1, ["pipetest.sh", "pipetestdata", "ziponly"])

    def test_iswritable(self):
        self.assertFalse(self.z.iswritable("/testdata.zip"))
        self.assertFalse(self.z.iswritable("/testdata.zip/README"))
        self.assertFalse(self.z.iswritable("/testdata.zip/pygopherd"))

    def test_getfspath(self):
        self.assertEqual(self.z.getfspath("/testdata.zip/foo"), "foo")
        self.assertEqual(self.z.getfspath("/testdata.zip"), "")
        self.assertEqual(self.z.getfspath("/testdata.zip/foo/bar"), "foo/bar")

    def test_stat(self):
        self.assertRaises(OSError, self.z.stat, "/testdata.zip/nonexistant")
        self.assertTrue(stat.S_ISDIR(self.z.stat("/testdata.zip")[0]))
        self.assertTrue(stat.S_ISREG(self.z.stat("/testdata.zip/README")[0]))
        self.assertTrue(stat.S_ISDIR(self.z.stat("/testdata.zip/pygopherd")[0]))
        self.assertTrue(stat.S_ISDIR(self.z2.stat("/testdata2.zip/pygopherd")[0]))
        self.assertTrue(
            stat.S_ISREG(self.z.stat("/testdata.zip/pygopherd/pipetest.sh")[0])
        )
        self.assertTrue(
            stat.S_ISREG(self.z2.stat("/testdata2.zip/pygopherd/pipetest.sh")[0])
        )

    def test_isdir(self):
        self.assertFalse(self.z.isdir("/testdata.zip/README"))
        self.assertFalse(self.z2.isdir("/testdata.zip/README"))
        self.assertTrue(self.z.isdir("/pygopherd"))
        self.assertTrue(self.z.isdir("/testdata.zip/pygopherd"))
        self.assertTrue(self.z2.isdir("/testdata2.zip/pygopherd"))
        self.assertTrue(self.z.isdir("/testdata.zip"))

    def test_isfile(self):
        self.assertTrue(self.z.isfile("/testdata.zip/README"))
        self.assertFalse(self.z.isfile("/testdata.zip"))
        self.assertFalse(self.z.isfile("/testdata.zip/pygopherd"))
        self.assertFalse(self.z2.isfile("/testdata2.zip/pygopherd"))
        self.assertTrue(self.z.isfile("/testdata.zip/.abstract"))

    def test_exists(self):
        self.assertTrue(self.z.exists("/README"))
        self.assertFalse(self.z.exists("/READMEnonexistant"))
        self.assertTrue(self.z.exists("/testdata.zip"))
        self.assertTrue(self.z.exists("/testdata.zip/README"))
        self.assertTrue(self.z.exists("/testdata.zip/pygopherd"))
        self.assertTrue(self.z2.exists("/testdata2.zip/pygopherd"))

    def test_symlinkexists(self):
        self.assertTrue(self.zs.exists("/symlinktest.zip/real.txt"))
        self.assertTrue(self.zs.exists("/symlinktest.zip/linked.txt"))
        self.assertTrue(self.zs.exists("/symlinktest.zip/subdir/linktosubdir2"))

    def test_symlinkgetfspath(self):
        self.assertEqual(self.zs.getfspath("/symlinktest.zip"), "")
        self.assertEqual(self.zs.getfspath("/symlinktest.zip/real.txt"), "real.txt")
        self.assertEqual(self.zs.getfspath("/symlinktest.zip/subdir"), "subdir")
        self.assertEqual(
            self.zs.getfspath("/symlinktest.zip/subdir2/real2.txt"),
            "subdir2/real2.txt",
        )

    def test_symlink_listdir(self):
        m1 = self.zs.listdir("/symlinktest.zip")
        m1.sort()

        self.assertEqual(
            m1, ["linked.txt", "linktosubdir", "real.txt", "subdir", "subdir2"]
        )

        tm2 = [
            "linked2.txt",
            "linkedabs.txt",
            "linkedrel.txt",
            "linktoself",
            "linktosubdir2",
        ]
        m2 = self.zs.listdir("/symlinktest.zip/subdir")
        m2.sort()
        self.assertEqual(m2, tm2)

        m2 = self.zs.listdir("/symlinktest.zip/linktosubdir")
        m2.sort()
        self.assertEqual(m2, tm2)

        self.assertRaises(OSError, self.zs.listdir, "/symlinktest.zip/nonexistant")
        self.assertRaises(OSError, self.zs.listdir, "/symlinktest.zip/real.txt")
        self.assertRaises(
            OSError, self.zs.listdir, "/symlinktest.zip/linktosubdir/linkedrel.txt"
        )

        m2 = self.zs.listdir("/symlinktest.zip/linktosubdir/linktoself/linktoself")

        m2.sort()
        self.assertEqual(m2, tm2)

        m3 = self.zs.listdir("/symlinktest.zip/linktosubdir/linktoself/linktosubdir2")
        self.assertEqual(m3, ["real2.txt"])

    def test_symlink_open(self):
        realtxt = b"Test.\n"
        real2txt = b"asdf\n"

        # Establish basis for tests is correct.
        self.assertEqual(self.zs.open("/symlinktest.zip/real.txt").read(), realtxt)
        self.assertEqual(
            self.zs.open("/symlinktest.zip/subdir2/real2.txt").read(), real2txt
        )

        # Now, run the tests.
        self.assertEqual(
            self.zs.open("/symlinktest.zip/subdir/linked2.txt").read(), real2txt
        )
        self.assertEqual(
            self.zs.open("/symlinktest.zip/linktosubdir/linked2.txt").read(), real2txt
        )
        self.assertEqual(
            self.zs.open("/symlinktest.zip/linktosubdir/linkedabs.txt").read(), realtxt
        )
        self.assertEqual(
            self.zs.open(
                "/symlinktest.zip/linktosubdir/linktoself/linktoself/linktoself/linkedrel.txt"
            ).read(),
            realtxt,
        )
        self.assertEqual(
            self.zs.open("/symlinktest.zip/subdir/linktosubdir2/real2.txt").read(),
            real2txt,
        )

        self.assertRaises(IOError, self.zs.open, "/symlinktest.zip")
        self.assertRaises(IOError, self.zs.open, "/symlinktest.zip/subdir")
        self.assertRaises(IOError, self.zs.open, "/symlinktest.zip/linktosubdir")
        self.assertRaises(IOError, self.zs.open, "/symlinktest.zip/subdir/linktoself")
        self.assertRaises(
            IOError,
            self.zs.open,
            "/symlinktest.zip/linktosubdir/linktoself/linktosubdir2",
        )

    def test_symlink_isdir(self):
        self.assertTrue(self.zs.isdir("/symlinktest.zip/subdir"))
        self.assertTrue(self.zs.isdir("/symlinktest.zip/linktosubdir"))
        self.assertFalse(self.zs.isdir("/symlinktest.zip/linked.txt"))
        self.assertFalse(self.zs.isdir("/symlinktest.zip/real.txt"))

        self.assertTrue(self.zs.isdir("/symlinktest.zip/subdir/linktoself"))
        self.assertTrue(self.zs.isdir("/symlinktest.zip/subdir/linktosubdir2"))
        self.assertTrue(
            self.zs.isdir("/symlinktest.zip/linktosubdir/linktoself/linktosubdir2")
        )
        self.assertFalse(self.zs.isdir("/symlinktest.zip/nonexistant"))
        self.assertFalse(self.zs.isdir("/symlinktest.zip/subdir/linkedrel.txt"))
        self.assertTrue(self.zs.isdir("/symlinktest.zip"))

    def test_symlink_isfile(self):
        self.assertTrue(self.zs.isfile("/symlinktest.zip/real.txt"))
        self.assertFalse(self.zs.isfile("/symlinktest.zip"))
        self.assertFalse(self.zs.isfile("/symlinktest.zip/subdir"))
        self.assertFalse(self.zs.isfile("/symlinktest.zip/linktosubdir"))
        self.assertTrue(self.zs.isfile("/symlinktest.zip/linktosubdir/linkedrel.txt"))
        self.assertTrue(self.zs.isfile("/symlinktest.zip/linktosubdir/linked2.txt"))
        self.assertTrue(
            self.zs.isfile("/symlinktest.zip/subdir/linktoself/linktosubdir2/real2.txt")
        )
        self.assertFalse(
            self.zs.isfile("/symlinktest.zip/subdir/linktoself/linktosubdir2/real.txt")
        )

    def test_open(self):
        self.assertRaises(IOError, self.z.open, "/testdata.zip/pygopherd")
        self.assertRaises(IOError, self.z2.open, "/testdata2.zip/pygopherd")
        self.assertRaises(IOError, self.z2.open, "/testdata.zip/pygopherd")

        self.assertTrue(self.z.open("/testdata.zip/.abstract"))

        self.assertEqual(self.z.open("/testdata.zip/testfile.txt").read(), b"Test\n")
        shouldbe = b"Word1\nWord2\nWord3\n"
        self.assertEqual(
            self.z.open("/testdata.zip/pygopherd/pipetestdata").read(), shouldbe
        )
        self.assertEqual(
            self.z2.open("/testdata2.zip/pygopherd/pipetestdata").read(), shouldbe
        )


class ZIPHandler(BaseHandler):

    handler: BaseHandler

    def canhandlerequest(self):
        """
        We can handle the request if it's a ZIP file, in our pattern, etc.
        """

        if not self.config.getboolean("handlers.ZIP.ZIPHandler", "enabled"):
            return False

        pattern = re.compile(self.config.get("handlers.ZIP.ZIPHandler", "pattern"))

        basename = self.selector
        appendage = None

        while True:

            if pattern.search(basename) and self.vfs.isfile(basename):
                # is_zipfile() accepts filenames as bytes, but the type stub is incorrect
                if zipfile.is_zipfile(self.vfs.getfspath(basename)):  # noqa
                    self.basename = basename
                    self.appendage = appendage
                    return True

            if (
                len(basename) == 0
                or basename == "/"
                or basename == "."
                or basename == "./"
            ):
                return False

            (head, tail) = os.path.split(basename)
            if appendage is not None:
                appendage = os.path.join(tail, appendage)
            else:
                appendage = tail

            basename = head

    def _makehandler(self):
        from pygopherd.handlers import HandlerMultiplexer

        if hasattr(self, "handler"):
            return
        vfs = VFS_Zip(self.config, self.vfs, self.basename)

        self.handler = HandlerMultiplexer.getHandler(
            self.getselector(), self.searchrequest, self.protocol, self.config, vfs=vfs
        )

    def prepare(self):
        self._makehandler()
        self.handler.prepare()

    def isdir(self):
        return self.handler.isdir()

    def getdirlist(self):
        return self.handler.getdirlist()

    def write(self, wfile):
        self.handler.write(wfile)

    def getentry(self):
        self._makehandler()
        return self.handler.getentry()


class TestZipHandler(unittest.TestCase):
    def setUp(self) -> None:
        from pygopherd import testutil

        self.config = testutil.getconfig()
        self.vfs = VFS_Real(self.config)
        self.selector = "/testdata.zip"
        self.protocol = testutil.gettestingprotocol(self.selector, config=self.config)
        self.stat_result = self.vfs.stat(self.selector)

        self.config.set("handlers.ZIP.ZIPHandler", "enabled", "true")

    def test_zip_handler_directory(self):
        handler = ZIPHandler(
            self.selector, "", self.protocol, self.config, self.stat_result, self.vfs
        )
        self.assertTrue(handler.canhandlerequest())

        handler.prepare()
        self.assertTrue(handler.isdir())

        entry = handler.getentry()
        self.assertEqual(entry.selector, "/testdata.zip")
        self.assertEqual(entry.name, "testdata.zip")
        self.assertEqual(entry.mimetype, "application/gopher-menu")

        entries = handler.getdirlist()
        self.assertEqual(len(entries), 7)

        self.assertEqual(entries[0].selector, "/testdata.zip/README")
        self.assertEqual(entries[0].name, "README")
        self.assertEqual(entries[0].mimetype, "text/plain")

    def test_zip_handler_file(self):
        self.selector = "/testdata.zip/README"

        handler = ZIPHandler(
            self.selector, "", self.protocol, self.config, None, self.vfs
        )
        self.assertTrue(handler.canhandlerequest())

        handler.prepare()
        self.assertFalse(handler.isdir())

        entry = handler.getentry()
        self.assertEqual(entry.selector, "/testdata.zip/README")
        self.assertEqual(entry.name, "README")
        self.assertEqual(entry.mimetype, "text/plain")

        wfile = io.BytesIO()
        handler.write(wfile)
        data = wfile.getvalue()
        assert data.startswith(b"This directory contains data for the unit tests.")
