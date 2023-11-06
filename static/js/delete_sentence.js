function deleteSentenceFromDatabase() {
    const sentenceToDelete = document.getElementById('sentence').value;
  
    fetch('/delete_sentence', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ sentence: sentenceToDelete }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Sentence deleted successfully');
        // Refresh sentences
        fetchSentences();
      } else {
        alert('Error deleting sentence');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  