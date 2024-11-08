class Gamecard{
    
    constructor(category_elements, score_elements, myDice){
        this.category_elements = category_elements;
        this.dice=myDice;
        this.score_elements=score_elements;
        this.scorecard = {}
        console.log(category_elements)
        console.log(score_elements)
    }

    /**
     * Determines whether the scorecard is full/finished
     * A full scorecard is a scorecard where all categores are disabled.
     *
     * @return {Boolean} a Boolean value indicating whether the scorecard is full
     */
    is_finished(){
        for (let category_element of this.category_elements){
            console.log(category_element, category_element.classList)
            if (!category_element.value.trim()){return false} 
        }
        return true
    }

    is_subset_of(big, small){
        for (let x of small){
            if (!big.includes(x)){ return false }
        }
        return true
    }

    /**
     * Validates a score for a particular category
     * Upper categories should be validated by a single generalized procedure
     * Hint: Make use of this.dice.get_sum() and this.dice.get_counts()
     *
     * @param {String} category the category that should be validated
     * @param {Number} value the proposed score for the category
     * 
     * @return {Boolean} a Boolean value indicating whether the score is valid for the category
    */
    is_valid_score(category, value){
      let out = 0
      if(this.dice.dice.every( (x) => x == 0) || value.toString().trim() === "") { return false }

      if (this.dice.photo_names.includes(category)){
        let catnum = this.dice.photo_names.indexOf(category.split("_")[0])
        out = this.dice.get_counts()[catnum-1]*catnum
      }
      else{
            if (category == "three_of_a_kind"){
                let is_three_of_a_kind = false
                for(let i of this.dice.get_counts()){
                    if (i >= 3){ is_three_of_a_kind = true }
                }
                if(is_three_of_a_kind) { out = this.dice.get_sum() }
            }
            if (category == "four_of_a_kind"){
                
                let is_four_of_a_kind = false
                for(let i of this.dice.get_counts()){
                    if (i >= 4){ is_four_of_a_kind = true }
                }
                if(is_four_of_a_kind) { out = this.dice.get_sum() }

            }
            if (category == "small_straight"){
                if(this.is_subset_of(this.dice.dice, [1, 2, 3, 4]) || this.is_subset_of(this.dice.dice, [2, 3, 4, 5]) || this.is_subset_of(this.dice.dice, [3, 4, 5, 6])){
                    out = 30
                }
            }
            if (category == "large_straight"){
                if(this.is_subset_of(this.dice.dice, [1, 2, 3, 4, 5]) || this.is_subset_of(this.dice.dice, [2, 3, 4, 5, 6])){
                    out = 40
                }
            }
            if (category == "yahtzee"){
                let is_yahtzee = true
                for (let i = 0; i < this.dice.dice.length-1; i++){
                    if(this.dice.dice[i+1] != this.dice.dice[i]){is_yahtzee = false} 
                }
                if(is_yahtzee){
                    out = 50
                }
            }
            if (category == "chance"){
                out = this.dice.get_sum()
            }
            if (category == "full_house"){
                if(this.dice.get_counts().includes(3) && this.dice.get_counts().includes(2)){
                    out = 25
                }
            }
        }

        return out == value
        
    }

    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){
        this.update_scores()
        return parseInt(this.score_elements[5].innerHTML)
    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       this.score_elements[0].innerHTML = this.category_elements.slice(0, 6).reduce( function(acc, elem){
        if (elem.value.trim() != "" && elem.value != -1 && elem.disabled){
            return acc + parseInt(elem.value)
        }
        else{
            return acc
        }
       }, 0)

       this.score_elements[1].innerHTML =  null
       if(parseInt(this.score_elements[0].innerHTML) > 63) { this.score_elements[1].innerHTML = 35 }

       this.score_elements[2].innerHTML = parseInt(this.score_elements[0].innerHTML) + parseInt(this.score_elements[1].innerHTML)
       if(!this.score_elements[1].innerHTML.trim()){
        this.score_elements[2].innerHTML = parseInt(this.score_elements[0].innerHTML)
       }

       this.score_elements[3].innerHTML = this.category_elements.slice(6).reduce( function(acc, elem){
        if (elem.value.trim() != "" && elem.value != -1 && elem.disabled){
            return acc + parseInt(elem.value)
        }
        else{
            return acc
        }
       }, 0)

       this.score_elements[4].innerHTML = this.score_elements[2].innerHTML

       this.score_elements[5].innerHTML = parseInt(this.score_elements[3].innerHTML) + parseInt(this.score_elements[4].innerHTML)
    }

    /**
     * Loads a scorecard from a JS object in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @param {Object} gameObject the object version of the scorecard
    */
    load_scorecard(gameObject){
        
        //gameObject = JSON.parse(gameObject)
        
        this.dice.rolls_remaining_element.innerHTML = gameObject["rolls_remaining"]

        // for (let i = 0; i < 5; i++){
        //     this.category_elements[i] = gameObject["upper"][this.dice.photo_names[i+1]]
        // }

        let values = Object.values(gameObject["upper"]).concat(Object.values(gameObject["lower"]))

        for (let i in this.category_elements){
            console.log(this.category_elements[i], values[i])
            this.category_elements[i].value = values[i]
            this.category_elements[i].disabled = true
            if (values[i] == -1) {
                this.category_elements[i].value = ""
                this.category_elements[i].disabled = false
            }
        }



    }

    /**
     * Creates a JS object from the scorecard in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @return {Object} an object version of the scorecard
     *
     */
    to_object(){

        let outdict = {
            "rolls_remaining": parseInt(this.dice.rolls_remaining_element.innerHTML),
            "upper":{
                "one":parseInt(this.category_elements[0].value),
                "two":parseInt(this.category_elements[1].value),
                "three":parseInt(this.category_elements[2].value),
                "four":parseInt(this.category_elements[3].value),
                "five":parseInt(this.category_elements[4].value),
                "six":parseInt(this.category_elements[5].value)
            },
            "lower":{
                "three_of_a_kind":parseInt(this.category_elements[6].value),
                "four_of_a_kind":parseInt(this.category_elements[7].value),
                "full_house":parseInt(this.category_elements[8].value),
                "small_straight":parseInt(this.category_elements[9].value),
                "large_straight":parseInt(this.category_elements[10].value),
                "yahtzee":parseInt(this.category_elements[11].value),
                "chance":parseInt(this.category_elements[12].value)
            }
        }

        for(let i of ["upper", "lower"]){
            for (let j in outdict[i]){
                if (isNaN(outdict[i][j])){
                    
                    console.log("j:" + j)
                    outdict[i][j] = -1}
            }
        }

        for(let i = 0; i < 5;  i++){
            if (!(this.category_elements[i].disabled)){
                outdict["upper"][Object.keys(outdict["upper"])[i]] = -1
            }
        }

        for(let i = 6; i < 12;  i++){
            if (!(this.category_elements[i].disabled)){
                // console.log(Object.keys(outdict["lower"]), [i-6], Object.keys(outdict["lower"])[i-6])
                outdict["lower"][Object.keys(outdict["lower"])[i-6]] = -1
            }
        }

        return outdict
    }
}

export default Gamecard;





