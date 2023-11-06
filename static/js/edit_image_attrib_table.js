$(document).ready(function() {
  var originalTableData;

  // Declare nameColumnIndex here
  var nameColumnIndex = 0; // Adjust this to the correct index

  // Capture the original table data
  originalTableData = $('.table-class').html();
  var originalImageData = {}; // To store original image paths

  // Capture the original table data and image paths
  $('#myTable tbody tr').each(function(index) {
    var rowName = $(this).find('td').eq(nameColumnIndex).text().trim();
    var originalImagePath = $(this).find('td.image-cell img').attr('src');
    originalImageData[rowName] = originalImagePath;
  });
  // Add Row button click event
  $('#add-row').click(function() {
    var newRowId = 'row-' + ($('.table-class tbody tr').length + 1);
    var newRowHtml = `
    <tr id="${newRowId}">
      <td contenteditable="true"></td>
      <td contenteditable="true"></td>
      <td contenteditable="true"></td>
      <td contenteditable="true"></td>
      <td class="image-cell">
        <img src="" alt="Image Preview" class="image-preview">
        <input type="file" name="image" class="image-input">
      </td>
      <td>
        <button class="delete-row">Delete</button>
      </td>
    </tr>
  `;
  
    $('.table-class tbody').append(newRowHtml);
  });

  // Delete Row button click event
  $(document).on('click', '.delete-row', function() {
    var row = $(this).closest('tr');
    row.remove();
  });
  
  // Process the updated table data and save it to the server
  $('#save-changes').click(function() {
    var formData = new FormData();
    var tableData = [];
    var originalImagePaths = {};

    // Get the column titles from the table header
    var columnTitles = [];
    $('.table-class thead th').each(function() {
      var title = $(this).text();
      columnTitles.push(title);
    });
  
    $('.table-class tbody tr').each(function(index) {
      var row = {};
      var rowName = $(this).find('td').eq(nameColumnIndex).text().trim();

      $(this).find('td:not(:last-child)').each(function(colIndex) {
        var columnName = columnTitles[colIndex];
        var columnValue = $(this).text();
        row[columnName] = columnValue;
      });
  
      // Attach the image file or original image path
      var imageFile = $(this).find('td.image-cell .image-input')[0].files[0];
      if (imageFile) {
        formData.append('image-' + rowName, imageFile);
      } else {
        originalImagePaths[rowName] = originalImageData[rowName];
      }
  
      tableData.push(row);
    });

    // Attach the originalImagePaths and tableData as a JSON string to FormData
    formData.append('originalImagePaths', JSON.stringify(originalImagePaths));
    formData.append('tableData', JSON.stringify(tableData));

    $.ajax({
      url: '/edit_img_attrib_table',
      method: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        // Handle success here
      },
      error: function(xhr, status, error) {
        alert('An error occurred while saving the changes.');
      }
    });
  });

  // Cancel Changes button click event
  $('#cancel-changes').click(function() {
    // Reset the table state to its original content
    $('.table-class').html(originalTableData);
  });
});
