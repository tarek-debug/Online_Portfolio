<?php
// Check if the form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  // Retrieve the email addresses and uploaded images
  $emailAddresses = $_POST['email'];
  $uploadedImages = $_FILES['image'];

  // Perform further processing, such as storing the data in a database or sending emails

  // Example: Store the email addresses in a text file
  $file = 'email_addresses.txt';
  $data = implode(PHP_EOL, $emailAddresses);
  file_put_contents($file, $data);

  // Example: Move uploaded images to a specific directory
  $imageDirectory = 'uploaded_images/';
  foreach ($uploadedImages['tmp_name'] as $key => $tmpName) {
    $imageName = $uploadedImages['name'][$key];
    move_uploaded_file($tmpName, $imageDirectory . $imageName);
  }

  // Provide a response or redirect the user to another page
  echo 'Changes saved successfully!';
}
?>
