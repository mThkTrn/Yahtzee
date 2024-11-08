console.log("UI.js connected")
import Dice from './Dice.js';
import Gamecard from './Gamecard.js';

//-------Dice Setup--------//
let roll_button = document.getElementById('roll_button'); 
roll_button.addEventListener('click', roll_dice_handler);

let dice_elements =[];
for (let i = 0; i<5; i++){
    let die = document.getElementById("die_"+i);
    die.addEventListener('dblclick', reserve_die_handler);
    dice_elements.push(die);
}
let rolls_remainging_element = document.getElementById("rolls_remaining");

let dice = new Dice(dice_elements, rolls_remainging_element);
window.dice = dice; //useful for testing to add a reference to global window object
window.dice.set = dice.set.bind(dice);
window.dice.resetGame = dice.resetGame.bind(dice);


//-----Gamecard Setup---------//
let category_elements = Array.from(document.getElementsByClassName("category"));
for (let category of category_elements){
    category.addEventListener('keypress', function(event){
        if (event.key === 'Enter') {
            enter_score_handler(event);
        }
    });
}
let score_elements = Array.from(document.getElementsByClassName("score"));
let gamecard = new Gamecard(category_elements, score_elements, dice);
window.gamecard = gamecard; //useful for testing to add a reference to global window object

let save_gamecard_button = document.getElementById("save_game")
save_gamecard_button.onclick = save_gamecard
let load_gamecard_button = document.getElementById("load_game")
load_gamecard_button.onclick = load_gamecard

function resetGame(){
    window.dice.rolls_remaining = 3
    window.dice.dice = [0, 0, 0, 0, 0]
    window.dice.counts = [0, 0, 0, 0, 0]
    for (let die of window.dice.dice_elements){
        die.classList.remove("reserved")
    }
    window.dice.set([0, 0, 0, 0, 0], 3)
}

//---------Event Handlers-------//
function reserve_die_handler(event){
    console.log("Trying to reserve "+event.target.id);
    dice.reserve(event.target)
}

function roll_dice_handler(){
    // console.log(window.dice, dice)
    if (!window.gamecard.is_finished()){
        if (dice.rolls_remaining > 0){
            window.dice.roll()
            display_feedback("", "");
        }
        else{
            display_feedback("No more rolls left for this turn!", "bad")
        }
    }
    else{
        display_feedback("The gamecard is finished!", "bad")
    }
    // console.log("Dice values:", dice.get_values());
    // console.log("Sum of all dice:", dice.get_sum());
    // console.log("Count of all dice faces:", dice.get_counts());
    // console.log(window.dice, dice)
}

function enter_score_handler(event){
    // console.log("Score entry attempted for: ", event.target.id);
    // console.log("is_valid_score_params", event.target.id.slice(0, -6), event.target.value, gamecard.is_valid_score(event.target.id.slice(0, -6), event.target.value))
    console.log(window.dice)
    if((gamecard.is_valid_score(event.target.id.slice(0, -6), event.target.value) || (parseInt(event.target.value) === 0)) && !dice.dice.every( (x) => x == 0)) {
        window.dice = dice
        event.target.disabled = true
        resetGame()
        display_feedback("You scored!", "good")
        if(window.gamecard.is_finished()){
            display_feedback("You fifnished the game!", "good")
        }
    }
    else {
        event.target.value = ""
        display_feedback("Oops - that score is invalid for this category", "bad")
    }
}

//------Feedback ---------//
var feedback_elem = document.getElementById("feedback")
function display_feedback(message, context){
    console.log(feedback_elem)
    console.log(context, "Feedback: ", message);
    if(context == "good"){
        feedback_elem.classList.add("good")
        feedback_elem.classList.remove("bad")
    }
    else if (context == "bad"){
        feedback_elem.classList.remove("good")
        feedback_elem.classList.add("bad")
    }
    else{
        feedback_elem.classList.remove("good")
        feedback_elem.classList.remove("bad") 
    }
    feedback_elem.innerHTML = message

}

display_feedback("Welcome to Yahtzee!", "good")

function save_gamecard(){
    console.log("saving game")
    // try{
        console.log(window.gamecard)
        let savedict = window.gamecard.to_object()
        localStorage.setItem("yahtzee", JSON.stringify(savedict))
    display_feedback("Saved game successfully", "good")
    // }
    // catch{
    //     display_feedback("Failed to save game", "bad")
    // }
}

function load_gamecard(){
    console.log("loading game")
    if(localStorage.getItem("yahtzee")){
        // try{
            gamecard.load_scorecard(JSON.parse(localStorage.getItem("yahtzee")))
            dice.resetGame()
            display_feedback("Loaded game", "good")
        // }
        // catch{
        //     display_feedback("Failed to load game", "bad")
        // }
    }
    else{
        display_feedback("Could not find saved game", "bad")

    }
}