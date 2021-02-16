//中間CSVデータから最新データをスプレッドシートに追記
//トリガー定期実行
function importCSVFromGoogleDrive() {
  var fSource = DriveApp.getFolderById("YOUR_ID");
  var file = fSource.getFilesByName('dataAll.csv').next();
  var csvData = Utilities.parseCsv(file.getBlob().getDataAsString());
  var sheet = SpreadsheetApp.openById("YOUR_ID");
  var ss = sheet.getActiveSheet();
  csvData.shift();
  var lasVal = sheet.getRange("B2").getValue();
  var d = new Date(2020, 2, 12)
  Logger.log("Check" + lasVal + ":" + csvData[0][1]) 
  if(lasVal != csvData[0][1]){
    Logger.log("Today DATA" + csvData.length + ":" + csvData[0].length)
    var numRows = csvData.length;
    var numColumns = csvData[0].length;
    ss.insertRows(2,numRows);
    ss.getRange(2, 1, numRows, numColumns).setValues(csvData);
  }else{
    Logger.log("No Chage")
  }
  Logger.log("RESULT" + ":" + csvData[0] + ":" + ss.getLastRow())
  //サービスのヘルスチェック
   var toAdr = "YOUR_EMAIL";//送り先アドレス
    var subject = "YOUR_SUBJECT";
    var name = "gas";
    var body = Logger.getLog()
    MailApp.sendEmail({to:toAdr,subject:subject, name:name, body:body});
}