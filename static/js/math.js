var ans
var score = 0

function nextQ() {
    const n1 = Math.floor(Math.random()*5) + 1
    const n2 = Math.floor(Math.random()*5)

    document.getElementById('n1').innerHTML = n1
    document.getElementById('n2').innerHTML = n2
    
    ans = n1 + n2
}

function CheckAns() {
         
    const pred = predictImage()
    // console.log(`ans: ${ans} and prediction: ${pred}`)

    if(ans == pred){
        score++
        alert("Correct! :)")
        // console.log(`correct! Score: ${score}`);
    }else{
        if(score != 0) {score--}
        alert("Wrong! :(")
        // console.log(`Wrong! Score: ${score}`);
    }

    document.getElementById('score').innerHTML = score
}