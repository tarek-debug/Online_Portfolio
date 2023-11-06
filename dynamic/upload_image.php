<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $targetDirectory = "static/img/";
  $imageFileType = strtolower(pathinfo($_FILES["image"]["name"], PATHINFO_EXTENSION));
  $targetFile = $targetDirectory . uniqid() . "." . $imageFileType;
  $uploadOk = 1;

  // Check if image file is a actual image or fake image
  $check = getimagesize($_FILES["image"]["tmp_name"]);
  if ($check !== false) {
    $uploadOk = 1;
  } else {
    $uploadOk = 0;
  }

  // Check if file already exists
  if (file_exists($targetFile)) {
    $uploadOk = 0;
  }

  // Check file size
  if ($_FILES["image"]["size"] > 500000) {
    $uploadOk = 0;
  }

  // Allow certain file formats
  if ($imageFileType != "jpg" && $imageFileType != "jpeg" && $imageFileType != "png" && $imageFileType != "gif") {
    $uploadOk = 0;
  }

  // Move uploaded file to the target directory
  if ($uploadOk == 1) {
    if (move_uploaded_file($_FILES["image"]["tmp_name"], $targetFile)) {
      $imageUrl = $targetFile;
      echo json_encode([
        "imageUrl" => $imageUrl
      ]);
    } else {
      echo "Error uploading the image.";
    }
  } else {
    echo "Invalid image file.";
  }
}
?>
