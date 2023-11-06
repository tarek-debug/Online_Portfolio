        // Function to toggle the responsive class for the navigation bar
        function toggleView() {
          var x = document.getElementById("myTopnav");
          if (x.classList.contains("responsive")) {
            x.classList.remove("responsive");
          } else {
            x.classList.add("responsive");
          }
        }
      
        // Function to handle the second click on the toggle view button
        function handleSecondClick() {
          var x = document.getElementById("myTopnav");
          x.classList.remove("responsive");
        }
      
        // Function to check if the navigation bar is currently responsive
        function isResponsive() {
          var x = document.getElementById("myTopnav");
          return x.classList.contains("responsive");
        }
      
        // Function to toggle view and handle second click
        function toggleViewAndHandleSecondClick() {
          toggleView();
          if (isResponsive()) {
            setTimeout(handleSecondClick, 500);
          }
        }