<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve form data
    $firstName = $_POST["firstname"];
    $lastName = $_POST["lastname"];
    $subject = $_POST["subject"];

    // You can perform further processing or validation here

    // Send an email with the form data
    $to = "tareksolamy111@example.com"; // Replace with your email address
    $subject = "New Contact Form Submission";
    $message = "First Name: " . $firstName . "\n"
             . "Last Name: " . $lastName . "\n"
             . "Subject: " . $subject;

    if (mail($to, $subject, $message)) {
        // Email sent successfully
        echo "Thank you for your message! We will get back to you soon.";
    } else {
        // Error sending email
        echo "Oops! Something went wrong. Please try again.";
    }
} else {
    // Invalid request method
    echo "Invalid request method. Please submit the form.";
}
?>
