var sentences = [];
var i = 0;
var j = 0;
var txt = "";
var speed = 50;

function fetchSentences() {
  fetch('/get_sentences')
    .then(response => response.json())
    .then(data => {
      sentences = data.sentences;
      txt = sentences[i];
      setTimeout(typeWriter, 2000); // Start typing only after fetching the sentences
    });
}

function typeWriter() {
  if (j < txt.length) {
    document.getElementById("info").innerHTML += txt.charAt(j);
    j++;
    setTimeout(typeWriter, speed);
  } else {
    setTimeout(deleteSentence, 2000);
  }
}

function deleteSentence() {
  if (j > 0) {
    document.getElementById("info").innerHTML = txt.substring(0, j - 1);
    j--;
    setTimeout(deleteSentence, speed);
  } else {
    i++;
    if (i >= sentences.length) {
      i = 0;
    }
    txt = sentences[i];
    setTimeout(typeWriter, 2000);
  }
}

fetchSentences(); // Start the process by fetching the sentences
