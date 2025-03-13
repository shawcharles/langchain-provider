# -*- coding: utf-8 -*-
#



"""
Status widget for Langchain + OpenAI completions.
"""

# Standard library imports
import logging
import os

# Third party imports
from qtpy.QtCore import QPoint

# Griffin imports
from griffin.api.translations import _
from griffin.api.widgets.status import StatusBarWidget
from griffin.utils.icon_manager import ima
from griffin.api.widgets.menus import GriffinMenu
from griffin.utils.qthelpers import add_actions, create_action

# Local imports
from .config_dialog import LangchainConfigDialog

logger = logging.getLogger(__name__)


class LangchainStatusWidget(StatusBarWidget):
    """Status bar widget for LangChain completions status."""

    BASE_TOOLTIP = _("LangChain completions status")
    DEFAULT_STATUS = _("not reachable")
    ID = "langchain_status"

    def __init__(self, parent, provider):
        self.provider = provider
        self.tooltip = self.BASE_TOOLTIP
        super().__init__(parent)
        self.setVisible(True)
        self.menu = GriffinMenu(self)
        self.sig_clicked.connect(self.show_menu)

    def set_value(self, value):
        """Return Langchain completions state."""
        langchain_enabled = self.provider.get_conf(
            ("enabled_providers", "langchain"), default=True, section="completions"
        )

        if value is not None and "short" in value:
            self.tooltip = value["long"]
            value = value["short"]
        elif value is not None:
            self.setVisible(True)
        elif value is None:
            value = self.DEFAULT_STATUS
            self.tooltip = self.BASE_TOOLTIP
        self.update_tooltip()
        self.setVisible(langchain_enabled)
        value = "Langchain: {0}".format(value)
        super(LangchainStatusWidget, self).set_value(value)

    def get_tooltip(self):
        """Reimplementation to get a dynamic tooltip."""
        return self.tooltip

    def open_provider_preferences(self):
        config_dialog = LangchainConfigDialog(self.provider, parent=self)
        config_dialog.show()

    def show_menu(self):
        """Display a menu when clicking on the widget."""
        menu = self.menu
        menu.clear()
        text = _("Change provider parameters")
        change_action = create_action(
            self,
            text=text,
            triggered=self.open_provider_preferences,
        )
        add_actions(menu, [change_action])
        rect = self.contentsRect()
        os_height = 7 if os.name == "nt" else 12
        pos = self.mapToGlobal(rect.topLeft() + QPoint(-40, -rect.height() - os_height))
        menu.popup(pos)

    def get_icon(self):
        return ima.icon("langchain")
