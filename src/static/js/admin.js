function confirmResetPassword(userId, userName) {
    activateAskModal(
        `Haluatko varmasti resetoida käyttäjän '${userName}' salasanan?`,
        () => {
            const xhttp = new XMLHttpRequest();

            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    activateNotifyModal(`Käyttäjän '${userName}' salasana resetoitu.`);
                } else {
                    activateSpinnerModal();
                }
            }
            xhttp.open("GET", `/reset_password?id=${userId}`);
            xhttp.send();    
        }
    );
}
