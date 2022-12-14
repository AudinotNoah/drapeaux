let lien_socket = 'ws://141.145.193.207:443'
const socket = new WebSocket(lien_socket);
let num_v = 0;
let num_j = 0;
let repp = '';

choix = function(rep) {
    socket.send(JSON.stringify({
        "action": "jeux",
        "valeur": rep
    }));
    repp = rep
}

continuer = function() {
    socket.send(JSON.stringify({
        "action": "continuer",
        "valeur":"classique"
    }));
    for (let i = 1; i < 5; i++) {
        document.getElementById("reponse" + i).style.background = '#33ACFF';
    }
}


socket.onopen = function() {
    let t = setInterval(function() {
        socket.send(JSON.stringify({
            "action": "vivant",
            "valeur": ""
        }));
    }, 55000);
    socket.send(JSON.stringify({
        "action": "commencer",
        "valeur":"classique"
    }));
};

socket.onmessage = function(event) {
    let reponse = JSON.parse(event.data);
    if (reponse['action'] == 'fin'){
        document.getElementById("bloc").innerHTML =
        '<div class="container" style="position: absolute;top:0; bottom: 0;left: 0;right: 0;margin: auto;">'+
        '<h1 class="resultat">Votre résultat : '+reponse['valeur']+'</h1>'+
        '<button class="play-button" onclick="window.location.href = '+"'"+"index.html"+"'"+'">Retour au menu</button>'+
        '</div>'
    }
    if (reponse['action'] == 'jeux_question') {
        document.getElementById("image").src = reponse['valeur']['lien']
        for (let i = 1; i < 5; i++) {
            document.getElementById("reponse" + i).innerText = reponse['valeur']['r' + i];
        }
    };
    if (reponse['action'] == 'jeux_reponse') {
        num_j = num_j + 1;
        if (reponse['valeur'] == repp) {
            num_v = num_v + 1
        }
        for (let i = 1; i < 5; i++) {
            document.getElementById("reponse" + i).style.background = '#FF0000';
        }
        document.getElementById("reponse" + reponse['valeur'].slice(1)).style.background = '#00FF00';
        setTimeout(() => {
            continuer();
        }, 1500);

    }
    document.getElementById('vf').innerText = num_v + "/ 221 pays trouvés.\n"+num_v+" ✔️ et " + (num_j-num_v) + " ❌";

}
