const socket = new WebSocket('ws://localhost:8001');
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

commencer = function() {
    socket.send(JSON.stringify({
        "action": "commencer"
    }));
    num_j = num_j + 1;
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
    commencer();
};

socket.onmessage = function(event) {
    let reponse = JSON.parse(event.data);
    if (reponse['action'] == 'jeux_question') {
        document.getElementById("image").src = reponse['valeur']['lien']
        for (let i = 1; i < 5; i++) {
            document.getElementById("reponse" + i).innerText = reponse['valeur']['r' + i];
        }
    };
    if (reponse['action'] == 'jeux_reponse') {
        if (reponse['valeur'] == repp) {
            num_v = num_v + 1
        }
        for (let i = 1; i < 5; i++) {
            document.getElementById("reponse" + i).style.background = '#FF0000';
        }
        document.getElementById("reponse" + reponse['valeur'].slice(1)).style.background = '#00FF00';
        setTimeout(() => {
            commencer();
        }, 1500);

    }
    //document.getElementById('vf').innerText = num_v + "/" + num_j + "parties gagnées.";


}