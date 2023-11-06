$(document).ready(function() {
    $("#uploadResumeBtn").click(function() {
      $("#resumeInput").click();
    });
  
    $("#resumeInput").change(function() {
      var file = this.files[0];
      var reader = new FileReader();
  
      reader.onload = function(e) {
        $("#resumeLink").attr("href", e.target.result);
        $("#resumeLink").attr("download", file.name); // Set the download attribute with the file name
      };
  
      reader.readAsDataURL(file);
    });
  
    $("#saveChangesBtn").click(function() {
      var resumeData = $("#resumeLink").attr("href");
  
      $.ajax({
        type: "POST",
        url: "/edit_resume",
        data: { resumeData: resumeData },
        success: function(response) {
          // Handle the response if needed
        }
      });
    });
  
    $("#cancelBtn").click(function() {
      $("#resumeLink").attr("href", "/download_resume");
      $("#resumeLink").removeAttr("download"); // Remove the download attribute
    });
  
    $("#resumeLink").click(function(e) {
      e.preventDefault(); // Prevent the default link behavior
  
      window.location.href = "/download_resume";
    });
  });
  