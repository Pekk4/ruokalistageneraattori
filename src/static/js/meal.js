let baseFields;
let preparedData;

window.onload = () => {
    const emptyFields = document.getElementById("empty-tr-to-copy");

    baseFields = emptyFields.cloneNode(true);
    emptyFields.parentElement.removeChild(emptyFields);
}

function addIngredientsFields() {
    const inputBody = document.getElementById("input-table-body");
    const newInputs = baseFields.cloneNode(true);

    newInputs.id = null;
    newInputs.className = null;
    inputBody.append(newInputs);
}

function composeData() {
    const mealForm = document.getElementById("meal-form");
    const formData = new FormData(mealForm);

    let inputStatus = checkInputs(formData);

    if (typeof(preparedData) === "undefined" && inputStatus === true) {
        preparedData = buildJSON(formData);

        return preparedData;
    } else {
        if (inputStatus === true) {
            return preparedData;
        } else {
            return false;
        }
    }
}

function submitMeal(updateMeal = true) {
    const xhttp = new XMLHttpRequest();
    const mealData = composeData();
    const addedText = "Ruokalaji on lisätty kirjastoosi.";
    const updatedText = "Ruokalaji on päivitetty.";
    const askForNew = "Haluatko lisätä uuden ruokalajin?"

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (updateMeal === true) {
                activateAskModal(
                    updatedText + " " + askForNew,
                    () => { location.replace("/meals?new=0"); },
                    () => { location.replace("/meals"); }
                );
            } else {
                activateAskModal(
                    addedText + " " + askForNew,
                    () => { location.replace("/meals?new=0"); },
                    () => { location.replace("/meals"); }
                );
            }
        } else if (this.readyState == 4 && this.status == 422) {
            if (this.responseText.includes("Samanniminen") === true) {
                activateAskModal(this.responseText, submitMeal);
            } else {
                activateNotifyModal(this.responseText);
            }
        } else {
            activateSpinnerModal();
        }
    }

    if (mealData !== false) {
        if (updateMeal === true) {
            xhttp.open("POST", "/add_meal?update=true")
        } else {
            xhttp.open("POST", "/add_meal");
        }

        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader("X-CSRFToken", document.getElementById("csrf_token").value);
        xhttp.send(mealData);
    }
}

function buildJSON(formData) {
    let meal = {};
    let ingredient = {};
    let ingredients = [];
    let index = 0;

    for (const [key, value] of formData.entries()) {
        if (key == "ingredient_name" || key == "qty" || key == "unit") {
            ingredient[key] = value;
            index++;
        } else if (key != "csrf_token") {
            meal[key] = value;
        }
        if (index == 3) {
            ingredients.push(ingredient);
            ingredient = new Object;
            index = 0;
        }
    }

    meal.ingredients = ingredients;

    return JSON.stringify(meal);
}

function checkInputs(formData) {
    const mealName = formData.get("meal_name").replace(/\s+/g, "");
    const ingredientName = formData.get("ingredient_name").replace(/\s+/g, "");

    if (mealName.length == 0 || ingredientName.length == 0) {
        const modalText = "Merkkijono oli tyhjä, anna ruokalajille jokin nimi ja vähintään yksi raaka-aine."

        activateNotifyModal(modalText, true, false);

        return false;
    }

    return true;
}

function addMeal() {
    document.getElementById("meal-form").classList.remove("hidden");
    document.getElementById("main-content").classList.replace("grid", "hidden");

    clearFields();
}

function toggleRecipe(hideInfo = true) {
    const addMealButton = document.getElementById("add-meal-button");

    if (hideInfo === true) {
        document.getElementById("add-meal-info").classList.replace("flex", "hidden");
        document.getElementById("recipe-div").classList.replace("hidden", "flex");
        addMealButton.innerHTML = "Näytä ohjeet";
        addMealButton.onclick = () => { toggleRecipe(false); };
    } else {
        document.getElementById("add-meal-info").classList.replace("hidden", "flex");
        document.getElementById("recipe-div").classList.replace("flex", "hidden");
        addMealButton.innerHTML = "Lisää resepti";
        addMealButton.onclick = () => { toggleRecipe(); };
    }
}

function removeRow(column) {
    const removableRow = column.parentElement;
    const ingredientsTbody = removableRow.parentElement;

    ingredientsTbody.removeChild(removableRow);

    if (ingredientsTbody.children.length == 0) {
        addIngredientsFields();
    }
}

function clearFields() {
    document.getElementById("meal_name").value = null;
    document.getElementById("input-table-body").innerHTML = null;

    addIngredientsFields();
}

function showMeals() {
    document.getElementById("meal-form").classList.add("hidden");
    document.getElementById("main-content").classList.replace( "hidden", "grid");
}

function confirmDeleteMeal() {
    activateAskModal("Haluatko varmasti poistaa ruokalajin?", deleteMeal);
}

function deleteMeal() {
    const xhttp = new XMLHttpRequest();
    const mealForm = document.getElementById("meal-form");
    const formData = new FormData(mealForm);
    const mealName = formData.get("meal_name");
    const mealObj = {}

    mealObj["meal_name"] = mealName;

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            activateNotifyModal(
                "Ruokalaji poistettu.",
                false,
                () => { location.replace("/meals"); }
            );
        } else if (this.readyState == 4 && this.status == 422) {
            activateNotifyModal(this.responseText);
        } else {
            activateSpinnerModal();
        }
    }
    xhttp.open("POST", "/delete_meal");
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.setRequestHeader("X-CSRFToken", document.getElementById("csrf_token").value);
    xhttp.send(JSON.stringify(mealObj));
}