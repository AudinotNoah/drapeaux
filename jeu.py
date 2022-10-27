import asyncio
import json
import websockets
import random
import sqlite3
import os


'''
https://websockets.readthedocs.io/en/stable/intro/tutorial1.html
https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications
'''
async def envoie(websocket,message):
    print("Envoie :",message)
    await websocket.send(json.dumps(message))

async def choix_pays():
    try:
        conn = sqlite3.connect('fichiers/nsi.db')
    except:
        chemin_absolu = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(chemin_absolu + '/fichiers/nsi.db')

    cursor = conn.cursor()
    cursor.execute("SELECT pays,Gdrapeaux FROM flags")
    r = cursor.fetchall()
    choix = random.sample(r,4)
    bonne = random.randint(0,3)
    question = {"action":"jeux_question","valeur":{"r1":choix[0][0],"r2":choix[1][0],"r3":choix[2][0],"r4":choix[3][0],"lien":choix[bonne][1]}}

    return "r"+str(bonne+1),question




async def handler(websocket):
    commencer = tour_du_joueur = False
    bonne_reponse = question = action = ""


    while True:
        message = await websocket.recv()
        print("Reçu :",str(message))
        message = json.loads(message)
        action = message["action"]

        if action == "commencer" and commencer == False:
            commencer = True
            action = "jeux"
        
        if action == "jeux" and tour_du_joueur == True and commencer == True:
            tour_du_joueur = False
            commencer = False
            await envoie(websocket,{"action":"jeux_reponse","valeur":bonne_reponse})

              
        elif action == "jeux" and tour_du_joueur == False and commencer == True:
            tour_du_joueur = True
            bonne_reponse, question = await choix_pays()
            await envoie(websocket,question)





async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
