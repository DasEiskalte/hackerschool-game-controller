import asyncio

import websockets
from pynput.keyboard import Key

from game_controller.eingabe.tastatur import tastatur
from game_controller.eingabe.ausgabestop import starte_ausgabestop
from game_controller.klassifikation.klassifikation import hole_klassifikation


print(f'Starte Server')
tastatur.start()
starte_ausgabestop()



async def server(websocket, path):
    while True:
        klassifikation = await hole_klassifikation(websocket)
        klasse = klassifikation.beste_klasse.name
        if tastatur.ist_ausgabe_aktiv:
            print(f"< {klasse}")
        tastatur.druecke_taste(Key.up, dauer_in_sekunden=1.0, prozent_aktiv=0.8)
        if klasse == 'links':
            tastatur.lasse_tasten_los([Key.left, Key.right])
            tastatur.druecke_taste(Key.left, dauer_in_sekunden=1.0, prozent_aktiv=0.8)
        elif klasse == 'rechts':
            tastatur.lasse_tasten_los([Key.left, Key.right])
            tastatur.druecke_taste(Key.right, dauer_in_sekunden=1.0, prozent_aktiv=0.8)
        elif klasse == 'nichts':
            tastatur.lasse_tasten_los([Key.left, Key.right])


start_server = websockets.serve(server, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
