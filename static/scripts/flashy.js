var total;
var countright;

function moveToCard(num){
  if(num >0){
      previous = document.getElementById("card-" + (num - 1) );
      previous.remove();
  }
  if (num<total){
      card = document.getElementById("card-" + num);
      card.style.visibility = 'visible';
  } else {
      resultsBlock = document.getElementById("results-block");
      resultsBlock.style.visibility = 'visible';
      resultsText = document.getElementById("results-text-message");
      resultsText.innerHTML = "That's it! you got " + countRight + " correct out of a total of " + total;
      resultsLink = document.getElementById("results-save-link");
      let href = resultsLink.getAttribute("href");
      resultsLink.setAttribute("href", href + Math.round(countRight*100/total));
  }
}

function go(cardCount){
    total = cardCount;
    countRight = 0;
    hideStart();
    moveToCard(0);
}

function hideStart(){
  gosection = document.getElementById("start-block");
  gosection.style.visibility = 'hidden';
  gosection.remove()
}

function right(num){
    countRight++;
    moveToCard(num + 1);
}

function wrong(num){
    moveToCard(num + 1);
}

function revealAnswer(id, answer) {
  textBlock = document.getElementById("cardtext-" + id);
  textBlock.innerHTML = answer ;
  rightWrongBlock = document.getElementById("rightwrong-" + id);
  rightWrongBlock.style.visibility = 'visible';
  revealButton = document.getElementById("reveal-button");
  revealButton.style.visibility = 'hidden';



}
