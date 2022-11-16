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

async def sql():
    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(chemin_absolu + '/nsi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT pays,Gdrapeaux FROM flags")
    r = cursor.fetchall()
    return r

async def choix_pays_infini():
    r = await sql()
    choix = random.sample(r,4)
    bonne = random.randint(0,3)
    question = {"action":"jeux_question","valeur":{"r1":choix[0][0],"r2":choix[1][0],"r3":choix[2][0],"r4":choix[3][0],"lien":choix[bonne][1]}}

    return "r"+str(bonne+1),question


async def choix_pays_classique():
    r = await sql()
    liste = []
    for x in r.copy():
        r.remove(x)
        choix = random.sample(r,4)
        r.append(x)
        bonne = random.randint(0,3)
        choix[bonne] = x
        question = {"action":"jeux_question","valeur":{"r1":choix[0][0],"r2":choix[1][0],"r3":choix[2][0],"r4":choix[3][0],"lien":x[1]}}
        liste.append(("r"+str(bonne+1),question))
    random.shuffle(liste)
    return liste






async def handler(websocket, _=""):
    commencer = continuer = tour_du_joueur = False
    bonne_reponse = question = action = mode = ""
    victoire = 0
    n_jouer = 1
    n_pays = len(await sql())

    while True:
        message = await websocket.recv()
        print("Reçu :",str(message))
        message = json.loads(message)
        action = message["action"]

        if action == "commencer" and commencer == False:
            commencer = True
            action = "jeux"
            mode = message["valeur"]
            if mode == "classique" or "classe":
                jeux = await choix_pays_classique()

        if action == "continuer" and continuer == False:
            n_jouer += 1
            if mode == "infini":
                mode = message["valeur"]
            action = "jeux"
                
            if n_pays < n_jouer: #fini
                valeur = str(victoire)+"/"+str(n_pays)
                await envoie(websocket,{"action":"fin","valeur":valeur})
                commencer = False
        
        if action == "jeux" and tour_du_joueur == True and commencer == True:
            tour_du_joueur = False
            continuer = False
            
            if message["valeur"] == bonne_reponse:
                victoire +=1
            await envoie(websocket,{"action":"jeux_reponse","valeur":bonne_reponse})


              
        elif action == "jeux" and tour_du_joueur == False and commencer == True:
            tour_du_joueur = True
            if mode == "infini":
                bonne_reponse, question = await choix_pays_infini()
            elif mode =="classique" or "classe":
                bonne_reponse, question = jeux[0][0],jeux[0][1]
                del jeux[0]

            await envoie(websocket,question)
        print(str(victoire),"/",str(n_jouer))





async def main():
    async with websockets.serve(handler, "", 443):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        #pour les versions en dessous de 3.7
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(main())
