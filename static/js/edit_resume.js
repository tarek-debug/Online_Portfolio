$(document).ready(function() {
    $("#uploadResumeBtn").click(function() {
      $("#resumeInput").click();
    });

    $("#resumeInput").change(function() {
      var file = this.files[0];
      var reader = new FileReader();

      reader.onload = function(e) {
        $("#resumeLink").attr("href", e.target.result);
      };

      reader.readAsDataURL(file);
    });

    $("#saveChangesBtn").click(function() {
      var resumeData = $("#resumeLink").attr("href");

      $.ajax({
        type: "POST",
        url: "save_resume.php",
        data: { resumeData: resumeData },
        success: function(response) {
          // Handle the response if needed
        }
      });
    });

    $("#cancelBtn").click(function() {
      $("#resumeLink").attr("href", "resume.pdf"); // Set the default resume file
    });
  });