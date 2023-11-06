function convertTableToStackedList() {
  var table = document.getElementById("myTable");
  var headers = Array.from(table.querySelectorAll("th")).map(th => th.innerText);
  var rows = Array.from(table.querySelectorAll("tbody tr"));

  // Remove existing stacked list and containers if they exist
  var stackedList = document.getElementById("stackedList");
  if (stackedList) {
    stackedList.parentNode.removeChild(stackedList);
  }

  // Create a new stacked list
  stackedList = document.createElement("ul");
  stackedList.setAttribute("id", "stackedList");

  // Iterate over the rows and create containers and list items
  rows.forEach(row => {
    var listItem = document.createElement("li");

    // Create a container for each list item
    var listItemContainer = document.createElement("div");
    listItemContainer.classList.add("list-item-container");
    listItem.appendChild(listItemContainer);

    // Get the first cell in the row for the title
    var title = row.querySelector("td:first-child").innerText;
    var titleElement = document.createElement("h2");
    titleElement.style.textAlign = "center"; // Center align the title
    titleElement.innerText = title;
    listItemContainer.appendChild(titleElement);

    // Iterate over the remaining cells and create content for each list item
    Array.from(row.querySelectorAll("td:not(:first-child)")).forEach((cell, index) => {
      var header = headers[index]; // Use the original index without offset
      var content = cell.innerText;

      var itemContent = document.createElement("span");
      itemContent.innerHTML = "<strong>" + header + ":</strong> " + content + " <br>"; // Add <br> for new line
      listItemContainer.appendChild(itemContent);
    });

    // Get the image cell in the row
    var imageCell = row.querySelector(".image-cell");

    // If image cell exists, create an image tag and append it to the container
    if (imageCell) {
      var imageTag = document.createElement("img");
      var imageSrc = imageCell.querySelector("img").getAttribute("src");
      imageTag.setAttribute("src", imageSrc);
      imageTag.style.width = "200px"; // Set the width of the image
      imageTag.style.height = "auto"; // Set the height to auto to maintain aspect ratio

      // Create a container for the image and position it at the bottom
      var imageContainer = document.createElement("div");
      imageContainer.classList.add("image-container");
      imageContainer.appendChild(imageTag);

      listItemContainer.appendChild(imageContainer);
    }

    stackedList.appendChild(listItem);
  });

  // Insert the stacked list after the table
  table.parentNode.insertBefore(stackedList, table.nextSibling);
}

function handleResize() {
  var screenWidth = window.innerWidth || document.documentElement.clientWidth;
  var table = document.getElementById("myTable");
  var stackedList = document.getElementById("stackedList");

  if (screenWidth < 600) {
    // Check if table exists and remove it
    if (table) {
      table.style.display = "none";
    }

    // Check if stacked list already exists
    if (!stackedList) {
      convertTableToStackedList();
    }
  } else {
    // Check if table is hidden and show it
    if (table) {
      table.style.display = "";
    }

    // Remove stacked list and containers if they exist
    if (stackedList) {
      stackedList.parentNode.removeChild(stackedList);
    }
  }
}

document.addEventListener("DOMContentLoaded", function() {
  // Call handleResize to check the screen size and convert the table on page load
  handleResize();

  // Add event listener for window resize
  window.addEventListener("resize", handleResize);
});
