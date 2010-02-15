#-*- coding: utf-8 -*-

"""
DESCRIPTION:
Adds an "Add Suspended" button to the Add Items dialog.

I personally use this for adding sentences with kanji I haven't
learned yet, but are otherwise easy.

AUTHOR:
Shawn M Moore (sartak@gmail.com)
"""

from ankiqt.ui.addcards import AddCards
from anki.hooks import wrap
from anki.utils import stripHTML
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def reportAddedSuspendedFact(self, fact):
    self.dialog.status.append(
        _("Added %(num)d suspended card(s) for <a href=\"%(id)d\">"
        "%(str)s</a>.") % {
        "num": len(fact.cards),
        "id": fact.id,
        # we're guaranteed that all fields will exist now
        "str": stripHTML(fact[fact.fields[0].name]),
        })

def suspendAddedFact(self, fact):
    self.parent.deck.suspendCards([card.id for card in fact.cards])
    return fact

# this is needs new anki!
def addSuspendedCards(self):
    old_addFact = self.addFact
    old_reportAddedFact = self.reportAddedFact

    suspendAddedFact_closed = lambda fact: suspendAddedFact(self, fact)
    self.addFact = wrap(self.addFact, suspendAddedFact_closed, "after")

    # haha python you crazy..
    self.reportAddedFact = lambda fact: reportAddedSuspendedFact(self, fact)

    self.addCards()

    self.addFact = old_addFact
    self.reportAddedFact = old_reportAddedFact

def addSuspendedButton(self):
    self.addSuspendedButton = QPushButton(_("Add Suspended"))
    self.addSuspendedButton.setAutoDefault(False)
    self.dialog.buttonBox.addButton(self.addSuspendedButton,
                                    QDialogButtonBox.ActionRole)
    self.connect(self.addSuspendedButton, SIGNAL("clicked()"), self.addSuspendedCards)

#Setup our hook
if not __name__ == "__main__":
    AddCards.addButtons = wrap(AddCards.addButtons, addSuspendedButton, "after")
    AddCards.addSuspendedCards = addSuspendedCards

