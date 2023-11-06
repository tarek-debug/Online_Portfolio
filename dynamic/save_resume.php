<?php
// save_resume.php file

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  if (isset($_POST["resumeData"])) {
    $resumeData = $_POST["resumeData"];

    // Remove the data URI scheme prefix and save the resume to a file
    $base64Prefix = "data:application/pdf;base64,";
    $resumeData = str_replace($base64Prefix, "", $resumeData);
    $decodedResumeData = base64_decode($resumeData);
    $filename = "resume.pdf"; // Choose a desired filename for the saved resume
    file_put_contents($filename, $decodedResumeData);

    // You can perform additional processing or store the resume data in a database if needed

    // Return a success message or any other desired response
    echo "Resume saved successfully.";
  }
}
?>
