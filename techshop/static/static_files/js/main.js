function funonload() {
    const value = JSON.parse(document.getElementById('rate-data').textContent);
    var percent = value/5*100;
    percent = percent.toFixed(0);
    console.log(percent);
    console.log((Number(value)));
    document.documentElement.style.setProperty('--percent', `${percent}%`);

}
window.onload = funonload;


function myFunction1() {
    var current = document.getElementById('notOrder');
    var archive = document.getElementById('isOrder');
    current.style.display = "block";
    archive.style.display = "none";

}

function myFunction2() {
    var current = document.getElementById("notOrder");
    var archive = document.getElementById("isOrder");
    current.style.display = "none";
    archive.style.display = "block";
}

function clickedForm() {
    var myform = document.getElementById("filter-form-c");
    if (myform.style.display === "none"){
        myform.style.display = "block";
    } else {
        myform.style.display = "none";
    }
}

function clickedForm2() {
    var myform = document.getElementById("filter-form-p");
    if (myform.style.display === "none"){
        myform.style.display = "block";
    } else {
        myform.style.display = "none";
    }
}

