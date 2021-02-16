//クラスター管理用CSV
//スプレッドシートが更新されるとCSVを書き出し
//トリガー：スプレッドシート変更時
function createCSV() {
  var ss = SpreadsheetApp.openById("YOUR_ID");
  var sheet = ss.getActiveSheet();
  var values = sheet.getDataRange().getValues();
  // Logger.log(values)
  var csv = values.join('\n');
  Logger.log(csv)
  FILE_ID = "YOUR_ID";
  var file = DriveApp.getFileById(FILE_ID);
  file.setContent(csv)
}