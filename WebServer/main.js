var counter = 0;

function main() {
    console.log("Ready");

    document.querySelector("#decButton").onclick = (event) => {
        counter--;
        updateView();
    }

    document.querySelector("#resetButton").onclick = (event) => {
        counter = 0;
        updateView();
    }

    document.querySelector("#incButton").onclick = (event) => {
        counter++;
        updateView();
    }
}

function updateView() {
    document.querySelector("#counterText").innerHTML = `Count = ${counter}`;
}

main();