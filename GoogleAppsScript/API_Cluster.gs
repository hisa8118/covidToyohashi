//クラスターデータ用API
function getData() {
  var ss = SpreadsheetApp.openById("YOUR_ID");
  var sheet = ss.getActiveSheet();
  var values = sheet.getDataRange().getValues();
  var csv = values.join('\n');
  return csv; 
}
function doGet() {
  var data = getData();
  return ContentService.createTextOutput(data)
  .setMimeType(ContentService.MimeType.CSV);
}