import requests
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction


class AlisaLauncher(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, _, extention):
        url = extention.preferences['url']
        try:
            response = requests.get(url=url)
            json = response.json()
            filtered = filter(lambda el: 'server' in el, json)
            items = []

            for el in list(filtered):
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=f'{el["name"]}',
                    description=f'{el["map"]} : {el["usersCount"]}',
                    on_enter=OpenAction(el['url']))
                )

            return RenderResultListAction(items)
        except ValueError:
            return RenderResultListAction([ExtensionResultItem(
                name=f'Error occured',
                on_enter=HideWindowAction())
            ])


if __name__ == '__main__':
    AlisaLauncher().run()
