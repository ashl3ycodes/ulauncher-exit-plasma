from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.SmallResultItem import SmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import (
    RenderResultListAction
)
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.utils.image_loader import icon_theme, Gtk
 
def get_icon_path(name, size):
    info = icon_theme.lookup_icon(name, size, Gtk.IconLookupFlags.FORCE_SIZE)
    if info is not None:
        return info.get_filename()

def create_item(name, icon, keyword, description, on_enter):
    return (
        keyword,
        ExtensionResultItem(
            name=name,
            description=description,
            icon=get_icon_path(icon, ExtensionResultItem.ICON_SIZE),
            on_enter=RunScriptAction(on_enter, None),
            #            on_enter=RunScriptAction('xfce4-session-logout --{}'.format(on_enter), None),
        )
    )

class XFCESessionExtension(Extension):
    def __init__(self):
        super(XFCESessionExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


items_cache = [
    create_item('Cerrar Sesión', 'system-log-out', 'logout', 'Cerrar la sesión actual de Plasma.', 'qdbus org.kde.ksmserver /KSMServer logout 0 3 3'),
    create_item('Reiniciar', 'system-reboot', 'reboot', 'Reiniciar el equipo.', 'qdbus org.kde.ksmserver /KSMServer logout 0 1 3'),
    create_item('Apagar', 'system-shutdown', 'shutdown', 'Apagar el equipo.', 'qdbus org.kde.ksmserver /KSMServer logout 0 2 3'),

    # https://askubuntu.com/questions/1792/how-can-i-suspend-hibernate-from-command-line/131022#131022
    # https://www.freedesktop.org/wiki/Software/systemd/logind/
    # https://askubuntu.com/questions/652978/how-to-create-keyboard-shortcut-which-initiates-suspend
    create_item('Suspender', 'system-suspend', 'suspend', 'Poner el equipo en estado de suspensión.', 'dbus-send --system --print-reply --dest="org.freedesktop.login1" /org/freedesktop/login1 org.freedesktop.login1.Manager.Suspend boolean:true'),
    create_item('Hibernar', 'system-suspend-hibernate', 'hibernate', 'Poner el equipo a hibernar.', 'dbus-send --system --print-reply --dest="org.freedesktop.login1" /org/freedesktop/login1 org.freedesktop.login1.Manager.Hibernate boolean:true'),
]


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        term = (event.get_argument() or '').lower()
        items = [i for name, i in items_cache if name.startswith(term)]
        return RenderResultListAction(items)


if __name__ == '__main__':
    XFCESessionExtension().run()
