<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $content = $_POST["content"];

  // Process the content and save it to a file or database

  echo json_encode([
    "success" => true,
    "message" => "Changes saved successfully."
  ]);
}
?>
