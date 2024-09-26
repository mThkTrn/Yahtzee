console.log("Dice.js connected")
class Dice{
    constructor(dice_elements, rolls_remaining_element){
        this.rolls_remaining_element= rolls_remaining_element;
        this.dice_elements= dice_elements;
        this.photo_names=["blank", "one", "two", "three", "four", "five", "six"]
        this.rolls_remaining = 3
        this.dice = [0, 0, 0, 0, 0]
        this.counts = [0, 0, 0, 0, 0, 0]
    }

    getRandomInt(min, max) {
        return Math.floor(Math.random() * ((max+1)-min))+min;
      }
    /**
     * Returns the number of rolls remaining for a turn
     * @return {Number} an integer representing the number of rolls remaining for a turn
    */
    get_rolls_remaining(){
        return parseInt(this.rolls_remaining_element.innerHTML)
    }

    /**
     * Returns an array of integers representing a current view of all five Yahtzee dice_elements
     * <br> A natural mapping is used to pair each integer with a die picture
     * <br> 0 is used to represent a "blank" die picture
     *
     * @return {Array} an array of integers representing dice values of dice pictures
    */
    get_values(){
        return this.dice
    }

    /**
     * Calculates the sum of all dice_elements
     * <br> Returns 0 if the dice are blank
     *
     * @return {Number} an integer representing the sum of all five dice
    */
    get_sum(){
        return this.dice.reduce(function(acc, num){return acc+num}, 0)
    }

    /**
     * Calculates a count of each die face in dice_elements
     * <br> Ex - would return [0, 0, 0, 0, 2, 3] for two fives and three sixes
     *
     * @return {Array} an array of six integers representing counts of the six die faces
    */
    get_counts(){
        this.counts = [0, 0, 0, 0, 0, 0]
        for (dice of this.dice) {
            this.counts[dice-1]++
        }
        return this.counts
    }

    /**
     * Performs all necessary actions to roll and update display of dice_elements
     * Also updates rolls remaining
     * <br> Uses this.set to update dice
    */
    roll(){
        for (let i = 0; i < this.dice.length; i++){
            console.log(this.dice_elements[i].classList)
            if (Array.from(this.dice_elements[i].classList).includes("reserved")){
                this.dice[i] = -1
            }
            else{
                this.dice[i] = this.getRandomInt(1, 6)
            }
        }
        this.rolls_remaining--

        this.set(this.dice, this.rolls_remaining)
    }

    /**
     * Resets all dice_element pictures to blank, and unreserved.
     * Also resets rolls remaining to 3
     * <br> Uses this.#setDice to update dice
    */
    reset(){
        this.rolls_remaining = 3
        this.dice = [0, 0, 0, 0, 0]
        this.set(this.dice, this.rolls_remaining)
        for (let idie of this.dice_elements){
            if (Array.from(idie.classList).includes("reserved")){
                idie.classList.remove("reserved")
            }
        }
    }

    /**
     * Performs all necessary actions to reserve/unreserve a particular die
     * <br> Adds "reserved" as a class label to indicate a die is reserved
     * <br> Removes "reserved" a class label if a die is already reserved
     * <br> Hint: use the classlist.toggle method
     *
     * @param {Object} element the <img> element representing the die to reserve
    */
    reserve(die_element){
        if (this.dice[this.dice_elements.indexOf(die_element)] != 0){
            die_element.classList.toggle("reserved")
        }
    }

    /**
     * A useful testing method to conveniently change dice / rolls remaining
     * <br> A value of 0 indicates that the die should be blank
     * <br> A value of -1 indicates that the die should not be updated
     *
     * @param {Array} new_dice_values an array of five integers, one for each die value
     * @param {Number} new_rolls_remaining an integer representing the new value for rolls remaining
     *
    */
    set(new_dice_values, new_rolls_remaining){

        this.dice = new_dice_values
        this.rolls_remaining = new_rolls_remaining

        for(let i = 0; i < this.dice.length; i++){
            if (this.dice[i] != -1) {
                this.dice_elements[i].src = "img/" + this.photo_names[this.dice[i]]+".svg"
            }
        }
        this.rolls_remaining_element.innerHTML = this.rolls_remaining
    }
}

export default Dice;