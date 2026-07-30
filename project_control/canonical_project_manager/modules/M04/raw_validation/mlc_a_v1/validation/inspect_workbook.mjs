import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath =
  "project_control/canonical_project_manager/architecture/" +
  "Atlas_Architecture_Traceability.xlsx";
const input = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(input);
const locators = [
  ["Surface Map", "A7:O7"],
  ["Target Modules", "A6:Q6"],
  ["Target Modules", "E6"],
  ["Contracts", "A8:E8"],
];

for (const [sheetName, rangeAddress] of locators) {
  const sheet = workbook.worksheets.getItem(sheetName);
  const range = sheet.getRange(rangeAddress);
  console.log(JSON.stringify({
    locator: `${sheetName}!${rangeAddress}`,
    values: range.values,
    formulas: range.formulas,
  }));
}
