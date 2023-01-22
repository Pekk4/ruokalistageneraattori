function activateSpinnerModal() {
    document.getElementById("modal-body").classList.remove("hidden");
    document.getElementById("spinner-modal-wrapper").classList.replace("hidden", "grid");
    document.getElementById("notify-modal-wrapper").classList.replace("grid", "hidden");
    document.getElementById("ask-modal-wrapper").classList.replace("grid", "hidden");
}

function activateNotifyModal(modalNote, isWarning = true, buttonFunction = false) {
    const paragraphElem = document.getElementById("notify-modal-text");

    document.getElementById("modal-body").classList.remove("hidden");
    document.getElementById("notify-modal-wrapper").classList.replace("hidden", "grid");
    document.getElementById("spinner-modal-wrapper").classList.replace("grid", "hidden");
    document.getElementById("ask-modal-wrapper").classList.replace("grid", "hidden");
    paragraphElem.innerHTML = modalNote;

    if (isWarning !== true) {
        paragraphElem.classList.replace("text-red-500", "text-black");
    } else {
        paragraphElem.classList.replace("text-black", "text-red-500");
    }

    if (buttonFunction != false) {
        document.getElementById("modal-ok-button").onclick = () => { closeModal(buttonFunction); };
    }
}

function activateAskModal(modalNote, functionWhenYes, functionWhenNo = closeModal) {
    document.getElementById("modal-body").classList.remove("hidden");
    document.getElementById("ask-modal-wrapper").classList.replace("hidden", "grid");
    document.getElementById("notify-modal-wrapper").classList.replace("grid", "hidden");
    document.getElementById("spinner-modal-wrapper").classList.replace("grid", "hidden");

    if (typeof(modalNote) !== "undefined") {
        document.getElementById("ask-modal-text").innerHTML = modalNote;
    }

    document.getElementById("modal-yes-button").onclick = () => { functionWhenYes(); };
    document.getElementById("modal-no-button").onclick = () => { functionWhenNo(); };
}

function closeModal(sideEffectFunction = false) {
    document.getElementById("modal-body").classList.add("hidden");

    if (sideEffectFunction !== false) {
        sideEffectFunction();
    }
}
