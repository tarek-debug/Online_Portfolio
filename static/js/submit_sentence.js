function submitSentence() {
    var newSentence = document.getElementById('newSentence').value;
    var formData = new FormData();
    formData.append('sentence', newSentence);
  
    fetch('/add_or_update_sentence', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Refresh the sentences
        fetchSentences();
      }
    });
  }
  