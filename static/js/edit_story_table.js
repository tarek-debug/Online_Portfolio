$(document).ready(function() {
  var originalTableData;

  // Capture the original table data
  originalTableData = $('#myTable').html();

  // Add Row button click event
  $('#add-row').click(function() {
    var newRowHtml = `
      <tr>
        <td contenteditable="true"></td>
        <td contenteditable="true"></td>
        <td contenteditable="true"></td>
        <td contenteditable="true"></td>
        <td>
        <button class="delete-row">Delete</button>
      </td>
      </tr>
    `;
    $('#myTable tbody').append(newRowHtml);
  });

  // Edit Row button click event
  $(document).on('click', '.edit-row', function() {
    var row = $(this).closest('tr');
    row.find('td').attr('contenteditable', 'true');
    row.addClass('editing');
  });

  // Delete Row button click event
  $(document).on('click', '.delete-row', function() {
    var row = $(this).closest('tr');
    row.remove();
  });

  // Process the updated table data and save it to the server
  $('#save-changes').click(function() {
    var tableData = [];

    // Get the column titles from the table header
    var columnTitles = [];
    $('#myTable thead th').each(function() {
      var title = $(this).text();
      columnTitles.push(title);
    });

    $('#myTable tbody tr').each(function() {
      var row = {};

      $(this).find('td:not(:last-child)').each(function(index) {
        var columnName = columnTitles[index];
        var columnValue = $(this).text();
        row[columnName] = columnValue;
      });

      tableData.push(row);
    });

    saveTableData(tableData);
  });

  // Function to save table data to the server
  function saveTableData(tableData) {
    $.ajax({
      url: '/edit_story_writing_table',
      method: 'POST',
      data: JSON.stringify({ tableData: tableData }),
      contentType: 'application/json',
      success: function(response) {
        console.log(response);
        originalTableData = tableData; // Update the original table data
      },
      error: function(xhr, status, error) {
        console.log(error);
        alert('An error occurred while saving the changes.');
      }
    });
  }

  // Cancel Changes button click event
  $('#cancel-changes').click(function() {
    // Reset the table state to its original content
    $('#myTable').html(originalTableData);
  });
});
