function deleteContact() {
    // Get the type and value from the form
    var type = document.getElementById('type').value;
    var value = document.getElementById('del_value').value;
    console.log(value);

    // Create an object to send as JSON
    var contactData = {
      type: type,
      value: value
    };
    console.log(contactData);
    // Send an AJAX request to the Flask endpoint
    $.ajax({
      url: '/delete_contact',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(contactData),
      success: function(response) {
        alert('Contact deleted successfully');
        // Optionally, you may want to reload the contacts or redirect the user
      },
      error: function(error) {
        console.log(error);
        alert('Error deleting contact');
      }
    });
  }
  