$(document).ready(function() {
    var originalContent;
  
    // Function to retrieve the updated content from the server
    function getUpdatedContent() {
      var url = window.location.href; // Get the current URL
      var page = getPageFromURL(url); // Extract the page name from the URL
  
      $.ajax({
        url: "/dynamic/get_" + page + ".php", // Use the page name to construct the URL
        method: 'GET',
        success: function(response) {
          // Update the content in the web page
          $('.editable-container').html(response);
          originalContent = response;
        },
        error: function(xhr, status, error) {
          console.log(error);
        }
      });
    }
  
    // Function to extract the page name from the URL
    function getPageFromURL(url) {
      var parts = url.split('/');
      var page = parts[parts.length - 1].split('.')[0];
      return page;
    }
  
    // Double click event handler
    $('.editable-container').dblclick(function() {
      if (!$(this).hasClass('editing')) {
        originalContent = $(this).html();
        $(this).attr('contenteditable', 'true');
        $(this).addClass('editing');
        createToolbar();
      }
    });
  
  // Button click event handler for saving changes
  $('#save').click(function() {
    var modifiedData = {};
  
    // Check for modified content in each element
    $('.editable-container').each(function() {
      var elementId = $(this).attr('id');
      var originalContent = $(this).data('original-content');
      var modifiedContent = $(this).html().trim();
  
      // Only send modified content to the server
      if (modifiedContent !== originalContent) {
        modifiedData[elementId] = modifiedContent;
      }
    });
  
    // Check if a new photo is uploaded
    var photoFile = $('#photo-upload')[0].files[0];
    if (photoFile) {
      modifiedData['photo'] = photoFile;
    }
  
    // Send modifiedData to the server using AJAX
    $.ajax({
      url: "/edit_about", // Update the URL to match your Flask route
      method: 'POST',
      data: modifiedData,
      processData: false,
      contentType: false,
      success: function(response) {
        // Handle the success response from the server
        console.log(response);
        $('.editable-container').attr('contenteditable', 'false');
        $('.editable-container').removeClass('editing');
        removeToolbar();
  
        // Retrieve the updated content after saving changes
        getUpdatedContent();
      },
      error: function(xhr, status, error) {
        // Handle the error response from the server
        console.log(error);
        $('.editable-container').each(function() {
          var elementId = $(this).attr('id');
          var originalContent = $(this).data('original-content');
          $(this).html(originalContent);
        });
        $('.editable-container').attr('contenteditable', 'false');
        $('.editable-container').removeClass('editing');
        removeToolbar();
      }
    });
  });
  
    // Button click event handler for canceling changes
    $('#cancel').click(function() {
      $('.editable-container').html(originalContent);
      $('.editable-container').attr('contenteditable', 'false');
      $('.editable-container').removeClass('editing');
      removeToolbar();
    });
  
    // Function to create the toolbar
    function createToolbar() {
      if (!$('.editable-container').prev('.text_toolbar').length) {
        var toolbarHTML = `
          <div class="text_toolbar">
            <button class="save-btn">Save changes</button>
            <button class="cancel-btn">Cancel</button>
          </div>
        `;
        $('.editable-container').before(toolbarHTML);
  
  
        // Add click event handler for "Save" button
        $('.save-btn').click(function() {
          saveChanges();
        });
  
        // Add click event handler for "Cancel" button
        $('.cancel-btn').click(function() {
          cancelChanges();
        });
      }
    }
  
  
    
  // Function to save changes
  function saveChanges() {
    // Get the modified content
    var aboutMeTitle = $('#about_me_title').html();
    var aboutTextTitle = $('#about_text_title').html();
    var aboutMeIntro = $('#about_me_intro').html();
    var technicalSkills = $('#technical_skills').html();
    var softwares = $('#softwares').html();
    var softwaresText = $('#softwares_text').html();
    var codingLang = $('#coding_lang').html();
    var codingLangText = $('#coding_lang_text').html();
    var frameworks = $('#frameworks').html();
    var frameworksText = $('#frameworks_text').html();
    var experience = $('#experience').html();
    var experienceTableTitle = $('#experience_table_title').html();
    var count1 = $('#count_1').html();
    var exp1 = $('#exp_1').html();
    var count2 = $('#count_2').html();
    var exp2 = $('#exp_2').html();
    var count3 = $('#count_3').html();
    var exp3 = $('#exp_3').html();
    var aspirations = $('#aspirations').html();
    var asp1 = $('#asp1').html();
    var asp2 = $('#asp2').html();
    var asp3 = $('#asp3').html();
    var asp4 = $('#asp4').html();
    // Create a FormData object and append the data
    var formData = new FormData();
    formData.append('about_me_title', aboutMeTitle);
    formData.append('about_text_title', aboutTextTitle);
    formData.append('about_me_intro', aboutMeIntro);
    formData.append('technical_skills', technicalSkills);
    formData.append('softwares', softwares);
    formData.append('softwares_text', softwaresText);
    formData.append('coding_lang', codingLang);
    formData.append('coding_lang_text', codingLangText);
    formData.append('frameworks', frameworks);
    formData.append('frameworks_text', frameworksText);
    formData.append('experience', experience);
    formData.append('experience_table_title', experienceTableTitle);
    formData.append('count_1', count1);
    formData.append('exp_1', exp1);
    formData.append('count_2', count2);
    formData.append('exp_2', exp2);
    formData.append('count_3', count3);
    formData.append('exp_3', exp3);
    formData.append('aspirations', aspirations);
    formData.append('asp1', asp1);
    formData.append('asp2', asp2);
    formData.append('asp3', asp3);
    formData.append('asp4', asp4);
    // Send the data to the server using AJAX
    $.ajax({
      url: "/edit_about",  // Endpoint that handles the update in Flask
      method: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        // Handle the success response from the server
        console.log(response);
        // Add any necessary UI updates or notifications to indicate successful save
      },
      error: function(xhr, status, error) {
        // Handle the error response from the server
        console.log(error);
        // Handle any error UI updates or notifications
      }
    });
  }
  
    // Function to cancel changes
    function cancelChanges() {
      $('.editable-container').html(originalContent);
      $('.editable-container').attr('contenteditable', 'false');
      $('.editable-container').removeClass('editing');
      removeToolbar();
    }
  
    // Function to remove the toolbar
    function removeToolbar() {
      $('.editable-container').prev('.text_toolbar').remove();
    }
  });
  