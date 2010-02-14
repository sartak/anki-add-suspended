#-*- coding: utf-8 -*-

"""
DESCRIPTION:
Adds checkboxes to each field in the Add Items dialog so that they are
not cleared after clicking add.

I personally use this for adding a few sentences from the same place,
to avoid having to type/paste the same URL or title multiple times.

AUTHOR:
Shawn M Moore (sartak@gmail.com)
"""

from ankiqt.ui.addcards import AddCards
from anki.hooks import wrap
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def addSuspendedButton(self):
    self.addSuspendedButton = QPushButton(_("Add Suspended"))
    self.addSuspendedButton.setAutoDefault(False)
    self.dialog.buttonBox.addButton(self.addSuspendedButton,
                                    QDialogButtonBox.ActionRole)
    self.connect(self.addSuspendedButton, SIGNAL("clicked()"), self.addCards)

#Setup our hook
if not __name__ == "__main__":
    AddCards.addButtons = wrap(AddCards.addButtons, addSuspendedButton, "after")

