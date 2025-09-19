let topic=document.getElementById("topics");
let clicktopic = document.getElementById("clicktopics")
topic.classList.add("d-none");


clicktopic.onclick=function()
{
    topic.classList.remove("d-none");
}


let algo_topic = document.getElementById("algorithmtopics");
let container = document.getElementById("algo-container");

// Initially hide the topics
algo_topic.classList.add("d-none");

// Show on hover of entire container (button + topics)
container.addEventListener("mouseenter", function () {
    algo_topic.classList.remove("d-none");
});

// Hide when mouse leaves the container
container.addEventListener("mouseleave", function () {
    algo_topic.classList.add("d-none");
    greedy_topic.classList.add("d-none");
    dynamic_topic.classList.add("d-none");
});

let greedy_approach=document.getElementById("greedyapproach");
let greedy_topic = document.getElementById("greedytopic");
greedy_topic.classList.add("d-none");

greedy_approach.onclick=function()
{
    greedy_topic.classList.remove("d-none");
}

let dynamic_programming=document.getElementById("dynamicprogramming");
let dynamic_topic = document.getElementById("dynamictopic");
dynamic_topic.classList.add("d-none");

dynamic_programming.onclick=function()
{
    dynamic_topic.classList.remove("d-none");
}


let ds_topic=document.getElementById("DStopics");
let click2=document.getElementById("clickds");
ds_topic.classList.add("d-none");
click2.onclick=function()
{
    ds_topic.classList.remove("d-none");
}
