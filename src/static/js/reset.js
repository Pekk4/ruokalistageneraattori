let passwordOk;

window.onload = () => {
    function setupListener(element) {
        element.addEventListener("keyup", event => {
            let inputValue = event.target.value;
    
            element.value = inputValue.replace(/\s+/g, "");
    
            validatePassword(inputValue);
        });
    }

    setupListener(document.getElementById("password-field"));
    setupListener(document.getElementById("repeat-password-field"));
}

function validatePassword(password) {
    const specialChars = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
    const numbers = /[0123456789]/;

    if ((password.length < 8) || (!specialChars.test(password)) || (!numbers.test(password))) {
        passwordOk = false;

        unlockButton();
    } else {
        passwordOk = true;

        unlockButton(true);
    }
}

function unlockButton(enable = false) {
    const submitButton = document.getElementById("login-box-button");
    const pwordField = document.getElementById("password-field");
    const pwordRepeatField = document.getElementById("repeat-password-field");

    if (enable === true) {
        if ((passwordOk === true) && (pwordField.value === pwordRepeatField.value)) {
            submitButton.disabled = false;
            document.getElementById("matches-notification").style = "display: none;";
            document.getElementById("password-notification").style = "display: none;";

            submitButton.classList.remove("bg-green-400");
            submitButton.classList.add("hover:bg-green-700");
            submitButton.classList.add("bg-green-600");
        }
    } else {
        submitButton.disabled = true;
        document.getElementById("matches-notification").style = null;

        submitButton.classList.remove("hover:bg-green-700");
        submitButton.classList.remove("bg-green-600");
        submitButton.classList.add("bg-green-400");
    }
}
