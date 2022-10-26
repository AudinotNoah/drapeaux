import asyncio
import json
import websockets
import random
import sqlite3


'''
https://websockets.readthedocs.io/en/stable/intro/tutorial1.html
https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications
'''


async def choix_pays():
    conn = sqlite3.connect('fichiers/nsi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT pays,Gdrapeaux FROM flags")
    r = cursor.fetchall()
    liste = []
    for x in r:
        liste.append((x[0],x[1]))
    num = random.randint(0,253)
    bonne = random.choice(["r1","r2","r3","r4"])
    question = {"action":"jeux_question","valeur":{"r1":"","r2":"","r3":"","r4":"","lien":""}}
    question["valeur"][bonne] = liste[num][0]
    question["valeur"]["lien"] = liste[num][1]
    if question["valeur"]["r1"] == "" : question["valeur"]["r1"] = liste[random.randint(0,254)][0]
    if question["valeur"]["r2"] == "" : question["valeur"]["r2"] = liste[random.randint(0,254)][0]
    if question["valeur"]["r3"] == "" : question["valeur"]["r3"] = liste[random.randint(0,254)][0]
    if question["valeur"]["r4"] == "" : question["valeur"]["r4"] = liste[random.randint(0,254)][0]

    return bonne,question




async def handler(websocket):
    commencer = tour_du_joueur = False
    bonne_reponse = question = action = ""


    while True:
        message = await websocket.recv()
        print(str(message))
        message = json.loads(message)
        action = message["action"]



        if action == "commencer" and commencer == False:
            print('ya1')
            commencer = True
            action = "jeux"
        
        if action == "jeux" and tour_du_joueur == True and commencer == True:
            print('ya2')
            tour_du_joueur = False
            commencer = False
            await websocket.send(json.dumps({"action":"jeux_reponse","valeur":bonne_reponse}))

              
        elif action == "jeux" and tour_du_joueur == False and commencer == True:
            tour_du_joueur = True
            print('ya3')
            bonne_reponse, question = await choix_pays()
            print(bonne_reponse)
            await websocket.send(json.dumps(question))



        



        
        





async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())