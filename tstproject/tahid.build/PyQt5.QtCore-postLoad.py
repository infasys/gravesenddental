from __future__ import absolute_import

from PyQt5.QtCore import QCoreApplication
import os

QCoreApplication.setLibraryPaths(
    [
        os.path.join(
           os.path.dirname(__file__),
           "qt-plugins"
        )
    ]
)

os.environ["QML2_IMPORT_PATH"] = os.path.join(
    os.path.dirname(__file__),
    "qml"
)

