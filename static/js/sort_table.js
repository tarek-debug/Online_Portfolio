// JavaScript code to sort the table alphabetically by column
function sortTable(columnIndex) {
    const table = document.getElementById("myTable");
    const tbody = table.getElementsByTagName("tbody")[0];
    const rows = Array.from(tbody.getElementsByTagName("tr"));
  
    rows.sort((a, b) => {
      const cellA = a.getElementsByTagName("td")[columnIndex].innerText.toLowerCase();
      const cellB = b.getElementsByTagName("td")[columnIndex].innerText.toLowerCase();
      return cellA.localeCompare(cellB);
    });
  
    rows.forEach(row => tbody.appendChild(row));
  }
  
  // Add event listeners to the table headers for sorting
  const headers = document.querySelectorAll("#myTable th");
  headers.forEach((header, index) => {
    header.addEventListener("click", () => {
      sortTable(index);
    });
  });
  