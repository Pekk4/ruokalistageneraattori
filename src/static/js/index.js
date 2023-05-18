const dateObj = new Date();
let dayOfWeek = dateObj.getDay();
let generatedMeal;

(dayOfWeek - 1) < 0 ? dayOfWeek = 6 : dayOfWeek--;

function generateMeal() {
    const xhttp = new XMLHttpRequest();
    const mealBox = document.getElementById("generated-meal-box");

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const meal = JSON.parse(this.response);

            closeModal();

            generatedMeal = meal;
            const confirmText = "Vaihdetaanko päivän ruokalajiksi "+generatedMeal.meal.toLowerCase()+"?";

            mealBox.innerHTML = meal.meal;
            mealBox.classList.remove("mt-10");
            mealBox.classList.add("mt-24", "mb-10", "hover:bg-white", "hover:cursor-pointer");
            mealBox.onclick = () => { activateAskModal(confirmText, replaceMeal); };
        } else if (this.readyState == 4 && this.status == 500) {
            activateNotifyModal(this.responseText);
        } else {
            activateSpinnerModal();
        }
    }
    xhttp.open("GET", "/generate_meal")
    xhttp.send();
}

function replaceMeal() {
    const xhttp = new XMLHttpRequest();
    const mealForm = new FormData();

    mealForm.append(dayOfWeek, generatedMeal.id);
    mealForm.append("csrf_token", document.getElementById("csrf-token").value);

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 201) {
            activateNotifyModal("Ruokalaji vaihdettu", false);
            setMeal();
        } else if (this.readyState == 4 && this.status == 500) {
            activateNotifyModal(this.responseText);
        } else {
            activateSpinnerModal();
        }
    }
    xhttp.open("POST", "/replace_meal");
    xhttp.send(mealForm);
}

function setMeal() {
    const mealBox = document.getElementById("generated-meal-box");

    mealBox.innerHTML = generatedMeal.meal;
    mealBox.classList.remove("hover:bg-white", "hover:cursor-pointer");
    mealBox.onclick = null;

    document.getElementById("p-meal-day-"+dayOfWeek).innerHTML = generatedMeal.meal;
}
