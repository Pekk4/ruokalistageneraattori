let userMeals;
const daysOfWeek = {
    0: "Maanantai",
    1: "Tiistai",
    2: "Keskiviikko",
    3: "Torstai",
    4: "Perjantai",
    5: "Lauantai",
    6: "Sunnuntai",
};

function fetchMeals() {
    const selectElem = document.getElementById("meal-form-select");
    const selectWrapper = document.getElementById("meal-form-select-wrapper");

    if (selectElem.childElementCount < 1) {
        const xhttp = new XMLHttpRequest();

        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                userMeals = new Map(Object.entries(JSON.parse(this.response)));

                buildMealList(selectElem);
                selectElem.classList.remove("hidden");

                selectWrapper.innerHTML = null;
                selectWrapper.appendChild(selectElem);
            } else if (this.readyState == 4 && this.status == 500) {
                activateNotifyModal(this.responseText);
            } else {
                insertSpinner(selectWrapper);
            }
        }
        xhttp.open("GET", "/get_meals");
        xhttp.send();
    }
}

function replaceMeal(form, day, table=null) {
    let mealData;

    if (form !== null) {
        const formData = new FormData(form);
        mealData = formData.get("mealdata").split(":");
    } else {
        mealData = table;
    }

    const dayToLower = daysOfWeek[day].toLowerCase();
    const mealToLower = mealData[1].toLowerCase();
    const confirmStr = "Vaihdetaanko " + dayToLower + "n ruokalajiksi " + mealToLower + "?";

    activateAskModal(confirmStr, deliverItems);

    function deliverItems() {
        closeModal();

        saveMeal(day, mealData);
    }
}

function saveMeal(day, mealData) {
    const xhttp = new XMLHttpRequest();
    const formData = new FormData();

    formData.append(day, mealData[0]);
    formData.append("csrf_token", document.getElementById("csrf_token").value);

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 201) {
            document.getElementById("meal-name-"+day).innerHTML = mealData[1];
            closeEditMeal();
        } else if (this.readyState == 4 && this.status == 500) {
            activateNotifyModal(this.responseText);
        } else {
            insertSpinner(document.getElementById("meal-to-edit"));
        }
    }
    xhttp.open("POST", "/replace_meal");
    xhttp.send(formData);
}

function insertSpinner(element) {
    const spinner = document.getElementById("get-spinner").innerHTML;

    element.innerHTML = spinner;
}

function generateMeal(day) {
    const xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const meal = JSON.parse(this.response);

            replaceMeal(null, day, [meal.id, meal.meal]);
        } else if (this.readyState == 4 && this.status == 500) {
            activateNotifyModal(this.responseText);
        } else {
            insertSpinner(document.getElementById("meal-to-edit"));
        }
    }
    xhttp.open("GET", "/generate_meal");
    xhttp.send();
}

function buildMealList(parentElement) {
    if (parentElement.childElementCount < 1) {
        for (const [key, value] of userMeals) {
            const optionElement = document.createElement("option");

            optionElement.value = key+":"+value;
            optionElement.text = value;

            parentElement.appendChild(optionElement);
        }
    }
}

function editMeal(day) {
    const mealForm = document.getElementById("replace-meal-form");
    const currentMeal = document.getElementById("meal-name-"+day);

    document.getElementById("day-of-meal").innerHTML = daysOfWeek[day];
    document.getElementById("meal-to-edit").innerHTML = currentMeal.innerHTML;

    fetchMeals();

    document.getElementById("current-menu-content").classList.add("hidden");
    document.getElementById("buttons").classList.add("hidden");
    document.getElementById("form-div").classList.remove("hidden");

    document.getElementById("replace-button").onclick = () => {
        replaceMeal(mealForm, day);
    };
    document.getElementById("generate-meal-button").onclick = () => {
        generateMeal(day);
    };
}

function editMenu() {
    const editMenuButton = document.getElementById("start-editing-button");

    for (const div of document.getElementsByClassName("single-meal")) {
        div.classList.remove("border-b", "rounded-bl", "rounded-br", "hover:bg-white");
    }

    document.getElementById("edit-menu-buttons").classList.replace("hidden", "grid");
    document.getElementById("meals-of-week").classList.remove("rounded-b", "border-b");
    document.getElementById("former-menus-wrapper").classList.add("hidden");

    editMenuButton.innerHTML = "Lopeta muokkaus";
    editMenuButton.onclick = () => { closeEditMenu(); };
}

function closeEditMeal() {
    document.getElementById("current-menu-content").classList.remove("hidden");
    document.getElementById("buttons").classList.remove("hidden");
    document.getElementById("form-div").classList.add("hidden");
}

function closeEditMenu() {
    const editMenuButton = document.getElementById("start-editing-button");
    let i = 0;

    for (const div of document.getElementsByClassName("single-meal")) {
        i == 0 || i == 6 ? div.classList.add("rounded-bl", "rounded-br") : null;

        div.classList.add("hover:bg-white");
        i++;
    }

    document.getElementById("edit-menu-buttons").classList.replace("grid", "hidden");
    document.getElementById("meals-of-week").classList.add("border-b", "rounded-b");
    document.getElementById("former-menus-wrapper").classList.remove("hidden");

    editMenuButton.innerHTML = "Muokkaa ruokalistaa";
    editMenuButton.onclick = () => { editMenu(); };
}

function toggleFormerMenus(isOpen = false) {
    if (isOpen === false) {
        document.getElementById("former-menus").classList.add("hidden");
        document.getElementById("former-menus-button").classList.remove("hidden");
    } else {
        document.getElementById("former-menus").classList.remove("hidden");
        document.getElementById("former-menus-button").classList.add("hidden");
    }
}
