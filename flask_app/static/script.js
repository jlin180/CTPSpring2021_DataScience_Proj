// const svm_form = document.getElementById("form__svm");
// const random_forest_form = document.getElementById("form__random-forest");
// const nfnet_form = document.getElementById("form__nfnet");
// const analytics_data = document.querySelector(".analytics-data");
// const header_svm = document.querySelector("#header__svm");
// const header_random = document.querySelector("#header__random-forest");
// const header_nfnet = document.querySelector("#header__nfnet");

// $(document).ready(function () {
//     console.log("document loaded");
// });

// $(window).on("load", function () {
//     console.log("window loaded");
// });

const svm_button = document.getElementById("svm_btn");
const random_forest_button = document.getElementById("random-forest_btn");
const nfnet_button = document.getElementById("nfnet_btn");

svm_button.addEventListener("click", getSVMForm, false);
random_forest_button.addEventListener("click", getRandomForestForm, false);
nfnet_button.addEventListener("click", getNFnetForm, false);

function getSVMForm() {
    document.getElementById("form__svm").style.display = "flex";
    document.getElementById("form__random-forest").style.display = "none";
    document.getElementById("form__nfnet").style.display = "none";

    document.getElementById("header__svm").style.display = "flex";
    document.getElementById("header__random-forest").style.display = "none";
    document.getElementById("header__nfnet").style.display = "none";
}

function getRandomForestForm() {
    document.getElementById("form__svm").style.display = "none";
    document.getElementById("form__random-forest").style.display = "flex";
    document.getElementById("form__nfnet").style.display = "none";

    document.getElementById("header__svm").style.display = "none";
    document.getElementById("header__random-forest").style.display = "flex";
    document.getElementById("header__nfnet").style.display = "none";
}

function getNFnetForm() {
    document.getElementById("form__svm").style.display = "none";
    document.getElementById("form__random-forest").style.display = "none";
    document.getElementById("form__nfnet").style.display = "flex";

    document.getElementById("header__svm").style.display = "none";
    document.getElementById("header__random-forest").style.display = "none";
    document.getElementById("header__nfnet").style.display = "flex";
}

const showAnalytics = () => {
    const analytics_data = document.querySelector(".analytics-data");

    const fruitMap = {};

    analytics_data.innerHTML = "<h2>Test Analytics</h2>";
    for (fruit in fruitMap) {
        const newHTMLElement = document.createElement("div");
        newHTMLElement.innerText = `${fruit}: ${fruitMap[fruit]}`;
        analytics_data.insertAdjacentElement("beforeend", newHTMLElement);
    }
};
