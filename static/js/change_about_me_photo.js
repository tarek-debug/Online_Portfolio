var originalPhotoSrc;

$(document).ready(function() {
  originalPhotoSrc = $("#profile_photo").attr("src");

  $("#changePhotoBtn").click(function() {
    $("#photoInput").click();
    $("#cancelPhotoBtn").show();
  });

  $("#photoInput").change(function() {
    var file = this.files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
      $("#profile_photo").attr("src", e.target.result);
    };

    reader.readAsDataURL(file);
  });

  $("#cancelPhotoBtn").click(function() {
    $("#profile_photo").attr("src", originalPhotoSrc);
    $(this).hide();
  });

  $("#savePhotoBtn").click(function() {
    var photoData = $("#photoInput")[0].files[0];
  
    var formData = new FormData();
    formData.append("profile_photo", photoData);
  
    $.ajax({
      type: "POST",
      url: "/edit_about_me_photo",
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        originalPhotoSrc = response.newPath; // Update the original photo source with the new path
      }
    });
  });
});
