function addBar(category, value, innerValue) {
    fetch('/add_bar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ Category: category, Value: value, InnerValue: innerValue })
    })
    .then(response => response.json())
    .then(() => loadCircularData()); // Refresh the plot
  }
  
  function editBar(category, value, innerValue) {
    fetch('/edit_bar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ Category: category, Value: value, InnerValue: innerValue })
    })
    .then(response => response.json())
    .then(() => loadCircularData()); // Refresh the plot
  }
  
  function removeBar(category) {
    fetch('/remove_bar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ Category: category })
    })
    .then(response => response.json())
    .then(() => loadCircularData()); // Refresh the plot
  }
  