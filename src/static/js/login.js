let usernameOk;
let passwordOk;
let usernameFree;

function activateForm(action) {
    const loginBox = document.getElementById("login-box");
    const itemsBox = document.getElementById("items-box");
    const getButton = document.getElementById("login-box-button");
    let widthCounter = 1500;
    let heightCounter = 224;

    getButton.innerHTML = action;
    loginBox.style = "width: "+widthCounter+"px; height: "+heightCounter+"px;";
    itemsBox.style = "display: none;";

    let animationInterval = setInterval(animateResize, 1);

    function animateResize() {
        console.log("perse")
        widthCounter = widthCounter - 20;

        if (heightCounter <= 384) {
            heightCounter = heightCounter + 10;
        }
        if (widthCounter < 384) {
            clearInterval(animationInterval);
            document.getElementById("login-form").style = "";
        } else {
            loginBox.style = "width: "+widthCounter+"px; height: "+heightCounter+"px;";
        }
    }

    if (action == "Rekisteröidy") {
        document.getElementById("login-form").action = "/register"
        addListeners();
    } else {
        usernameFree = usernameOk = passwordOk = true;
        unlockButton(true);
    }
}

function addListeners() {
    const unameField = document.getElementById("username-field");
    const pwordField = document.getElementById("password-field");

    unameField.addEventListener("keyup", event => {
        let inputValue = event.target.value;
        let isValid = validateUsername(inputValue);

        unameField.value = inputValue.replace(/\s+/g, "");

        isValid === true ? askUsernameStatus(inputValue) : null
    });

    unameField.addEventListener("focusout", event => {
        let inputValue = event.target.value;
        let isValid = validateUsername(inputValue);

        isValid === true ? askUsernameStatus(inputValue) : null
    });

    pwordField.addEventListener("keyup", event => {
        let inputValue = event.target.value;

        pwordField.value = inputValue.replace(/\s+/g, "");

        validatePassword(inputValue);
    });
}

function askUsernameStatus(username) {
    const xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            usernameFree = this.responseText;
        }
    }
    xhttp.open("GET", "/check_username?uname="+username)
    xhttp.send();

    checkUsernameStatus();
}

function checkUsernameStatus() {
    document.getElementById("uname-free-notification").style = "display: none";

    setTimeout(() => {
        if (usernameFree == "OK") {
            usernameFree = true
            unlockButton(true);
        } else if (usernameFree == "NOK") {
            usernameFree = false;
            document.getElementById("uname-free-notification").style = "";
        }
    }, 500);
}

function validateUsername(username) {
    let checkString = username.replace(/\s+/g, "");

    if (checkString.length < 5) {
        document.getElementById("username-notification").style = "";

        unlockButton();

        return false;
    } else {
        document.getElementById("username-notification").style = "display: none;";
        usernameOk = true;

        unlockButton(true);

        return true;
    }
}

function validatePassword(password) {
    const specialChars = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
    const numbers = /[0123456789]/;

    if ((password.length < 8) || (!specialChars.test(password)) || (!numbers.test(password))) {
        document.getElementById("password-notification").style = "";

        unlockButton();
    } else {
        document.getElementById("password-notification").style = "display: none;";
        passwordOk = true;

        unlockButton(true);
    }
}

function unlockButton(enable = false) {
    const submitButton = document.getElementById("login-box-button");

    if (enable === true) {
        if ((usernameOk === true) && (passwordOk === true) && (usernameFree === true)) {
            //submitButton.disabled = false;

            submitButton.classList.remove("bg-green-400");
            submitButton.classList.add("hover:bg-green-700");
            submitButton.classList.add("bg-green-600");
        }
    } else {
        //submitButton.disabled = true;

        submitButton.classList.remove("hover:bg-green-700");
        submitButton.classList.remove("bg-green-600");
        submitButton.classList.add("bg-green-400");
    }
}
