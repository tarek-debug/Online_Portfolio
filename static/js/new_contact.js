function addContact() {
    var contactType = $('#type').val();
    var contactValue = $('#value').val();
    var contactImage = $('#image')[0].files[0];
  
    var formData = new FormData();
    formData.append('type', contactType);
    formData.append('value', contactValue);
    formData.append('image', contactImage);
  
    $.ajax({
      type: 'POST',
      url: '/new_contact',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        if (response.success) {
          alert(response.message);
          $('#contactForm').trigger('reset'); // Reset the form if needed
        } else {
          alert('An error occurred while adding the contact.');
        }
      }
    });
  }
  