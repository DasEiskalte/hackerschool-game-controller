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
        if klasse == 'oben':
            tastatur.lasse_tasten_los([Key.down])
            tastatur.druecke_taste(Key.up, dauer_in_sekunden=1.0, prozent_aktiv=0.8)
        elif klasse == 'unten' :
            tastatur.lasse_tasten_los([Key.up])
            tastatur.druecke_taste(Key.down, dauer_in_sekunden=1.0, prozent_aktiv=0.8)


start_server = websockets.serve(server, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
