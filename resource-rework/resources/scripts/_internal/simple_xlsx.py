from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

ET.register_namespace("", MAIN_NS)
ET.register_namespace("r", DOC_REL_NS)


def qn(namespace: str, tag: str) -> str:
    return f"{{{namespace}}}{tag}"


def get_column_letter(column: int) -> str:
    if column < 1:
        raise ValueError("column index must be >= 1")
    chars: list[str] = []
    while column:
        column, remainder = divmod(column - 1, 26)
        chars.append(chr(ord("A") + remainder))
    return "".join(reversed(chars))


def column_index_from_string(label: str) -> int:
    value = 0
    for char in label:
        value = value * 26 + (ord(char.upper()) - ord("A") + 1)
    return value


def coordinate_from_tuple(row: int, column: int) -> str:
    return f"{get_column_letter(column)}{row}"


def coordinate_to_tuple(coordinate: str) -> tuple[int, int]:
    letters = []
    digits = []
    for char in coordinate:
        if char.isalpha():
            letters.append(char)
        elif char.isdigit():
            digits.append(char)
    if not letters or not digits:
        raise ValueError(f"invalid coordinate: {coordinate}")
    return int("".join(digits)), column_index_from_string("".join(letters))


@dataclass
class Font:
    size: int | None = None
    bold: bool = False
    color: str | None = None


@dataclass
class PatternFill:
    fill_type: str | None = None
    fgColor: str | None = None

    def __init__(self, fill_type: str | None = None, fgColor: str | None = None):
        self.fill_type = fill_type
        self.fgColor = fgColor


@dataclass
class Alignment:
    horizontal: str | None = None
    vertical: str | None = None
    wrap_text: bool = False


@dataclass
class ColumnDimension:
    width: float | int | None = None


class ColumnDimensionMap(defaultdict[str, ColumnDimension]):
    def __init__(self) -> None:
        super().__init__(ColumnDimension)


class Cell:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.value: Any = None
        self.font: Font | None = None
        self.fill: PatternFill | None = None
        self.alignment: Alignment | None = None

    @property
    def coordinate(self) -> str:
        return coordinate_from_tuple(self.row, self.column)


class Worksheet:
    def __init__(self, title: str) -> None:
        self.title = title
        self.sheet_state = "visible"
        self.freeze_panes: str | None = None
        self.column_dimensions: ColumnDimensionMap = ColumnDimensionMap()
        self._cells: dict[tuple[int, int], Cell] = {}
        self._merged_ranges: list[tuple[int, int, int, int]] = []

    def cell(self, row: int, column: int, value: Any = None) -> Cell:
        key = (row, column)
        cell = self._cells.get(key)
        if cell is None:
            cell = Cell(row=row, column=column)
            self._cells[key] = cell
        if value is not None:
            cell.value = value
        return cell

    def __getitem__(self, coordinate: str | int):
        if isinstance(coordinate, int):
            return [self.cell(coordinate, col_idx) for col_idx in range(1, self.max_column + 1)]
        row, column = coordinate_to_tuple(coordinate)
        return self.cell(row, column)

    def __setitem__(self, coordinate: str, value: Any) -> None:
        self[coordinate].value = value

    @property
    def max_row(self) -> int:
        return max((row for row, _column in self._cells), default=1)

    @property
    def max_column(self) -> int:
        return max((column for _row, column in self._cells), default=1)

    def iter_rows(self, values_only: bool = False):
        for row_idx in range(1, self.max_row + 1):
            row = [self.cell(row_idx, col_idx) for col_idx in range(1, self.max_column + 1)]
            if values_only:
                yield [cell.value for cell in row]
            else:
                yield row

    def merge_cells(
        self,
        start_row: int,
        start_column: int,
        end_row: int,
        end_column: int,
    ) -> None:
        self._merged_ranges.append((start_row, start_column, end_row, end_column))


class Workbook:
    def __init__(self) -> None:
        self.worksheets: list[Worksheet] = [Worksheet("Sheet")]

    @property
    def active(self) -> Worksheet:
        return self.worksheets[0]

    @property
    def sheetnames(self) -> list[str]:
        return [sheet.title for sheet in self.worksheets]

    def create_sheet(self, title: str) -> Worksheet:
        sheet = Worksheet(title)
        self.worksheets.append(sheet)
        return sheet

    def __getitem__(self, title: str) -> Worksheet:
        for sheet in self.worksheets:
            if sheet.title == title:
                return sheet
        raise KeyError(title)

    def save(self, path: str | Path) -> None:
        save_workbook(self, Path(path))


def minimal_styles_xml() -> bytes:
    root = ET.Element(qn(MAIN_NS, "styleSheet"))
    fonts = ET.SubElement(root, qn(MAIN_NS, "fonts"), count="1")
    font = ET.SubElement(fonts, qn(MAIN_NS, "font"))
    ET.SubElement(font, qn(MAIN_NS, "sz"), val="11")
    ET.SubElement(font, qn(MAIN_NS, "name"), val="Calibri")
    ET.SubElement(font, qn(MAIN_NS, "family"), val="2")
    fills = ET.SubElement(root, qn(MAIN_NS, "fills"), count="2")
    fill_none = ET.SubElement(fills, qn(MAIN_NS, "fill"))
    ET.SubElement(fill_none, qn(MAIN_NS, "patternFill"), patternType="none")
    fill_gray = ET.SubElement(fills, qn(MAIN_NS, "fill"))
    ET.SubElement(fill_gray, qn(MAIN_NS, "patternFill"), patternType="gray125")
    borders = ET.SubElement(root, qn(MAIN_NS, "borders"), count="1")
    border = ET.SubElement(borders, qn(MAIN_NS, "border"))
    ET.SubElement(border, qn(MAIN_NS, "left"))
    ET.SubElement(border, qn(MAIN_NS, "right"))
    ET.SubElement(border, qn(MAIN_NS, "top"))
    ET.SubElement(border, qn(MAIN_NS, "bottom"))
    ET.SubElement(border, qn(MAIN_NS, "diagonal"))
    style_xfs = ET.SubElement(root, qn(MAIN_NS, "cellStyleXfs"), count="1")
    ET.SubElement(style_xfs, qn(MAIN_NS, "xf"), numFmtId="0", fontId="0", fillId="0", borderId="0")
    cell_xfs = ET.SubElement(root, qn(MAIN_NS, "cellXfs"), count="1")
    ET.SubElement(cell_xfs, qn(MAIN_NS, "xf"), numFmtId="0", fontId="0", fillId="0", borderId="0", xfId="0")
    cell_styles = ET.SubElement(root, qn(MAIN_NS, "cellStyles"), count="1")
    ET.SubElement(cell_styles, qn(MAIN_NS, "cellStyle"), name="Normal", xfId="0", builtinId="0")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def workbook_xml(workbook: Workbook) -> bytes:
    root = ET.Element(qn(MAIN_NS, "workbook"))
    book_views = ET.SubElement(root, qn(MAIN_NS, "bookViews"))
    ET.SubElement(book_views, qn(MAIN_NS, "workbookView"), xWindow="0", yWindow="0", windowWidth="24000", windowHeight="12000")
    sheets_el = ET.SubElement(root, qn(MAIN_NS, "sheets"))
    for idx, sheet in enumerate(workbook.worksheets, start=1):
        sheet_el = ET.SubElement(
            sheets_el,
            qn(MAIN_NS, "sheet"),
            name=sheet.title,
            sheetId=str(idx),
        )
        if sheet.sheet_state != "visible":
            sheet_el.set("state", sheet.sheet_state)
        sheet_el.set(qn(DOC_REL_NS, "id"), f"rId{idx}")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def workbook_rels_xml(sheet_count: int) -> bytes:
    root = ET.Element(qn(PKG_REL_NS, "Relationships"))
    for idx in range(1, sheet_count + 1):
        ET.SubElement(
            root,
            qn(PKG_REL_NS, "Relationship"),
            Id=f"rId{idx}",
            Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet",
            Target=f"worksheets/sheet{idx}.xml",
        )
    ET.SubElement(
        root,
        qn(PKG_REL_NS, "Relationship"),
        Id=f"rId{sheet_count + 1}",
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles",
        Target="styles.xml",
    )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def package_rels_xml() -> bytes:
    root = ET.Element(qn(PKG_REL_NS, "Relationships"))
    ET.SubElement(
        root,
        qn(PKG_REL_NS, "Relationship"),
        Id="rId1",
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument",
        Target="xl/workbook.xml",
    )
    ET.SubElement(
        root,
        qn(PKG_REL_NS, "Relationship"),
        Id="rId2",
        Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties",
        Target="docProps/core.xml",
    )
    ET.SubElement(
        root,
        qn(PKG_REL_NS, "Relationship"),
        Id="rId3",
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties",
        Target="docProps/app.xml",
    )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def content_types_xml(sheet_count: int) -> bytes:
    root = ET.Element(qn(CONTENT_TYPES_NS, "Types"))
    ET.SubElement(root, qn(CONTENT_TYPES_NS, "Default"), Extension="rels", ContentType="application/vnd.openxmlformats-package.relationships+xml")
    ET.SubElement(root, qn(CONTENT_TYPES_NS, "Default"), Extension="xml", ContentType="application/xml")
    ET.SubElement(root, qn(CONTENT_TYPES_NS, "Override"), PartName="/xl/workbook.xml", ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml")
    ET.SubElement(root, qn(CONTENT_TYPES_NS, "Override"), PartName="/xl/styles.xml", ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml")
    ET.SubElement(root, qn(CONTENT_TYPES_NS, "Override"), PartName="/docProps/core.xml", ContentType="application/vnd.openxmlformats-package.core-properties+xml")
    ET.SubElement(root, qn(CONTENT_TYPES_NS, "Override"), PartName="/docProps/app.xml", ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml")
    for idx in range(1, sheet_count + 1):
        ET.SubElement(
            root,
            qn(CONTENT_TYPES_NS, "Override"),
            PartName=f"/xl/worksheets/sheet{idx}.xml",
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml",
        )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def core_properties_xml() -> bytes:
    return (
        b'<?xml version="1.0" encoding="UTF-8"?>'
        b'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        b'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        b'xmlns:dcterms="http://purl.org/dc/terms/" '
        b'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        b"<dc:creator>Codex</dc:creator>"
        b"<cp:lastModifiedBy>Codex</cp:lastModifiedBy>"
        b"</cp:coreProperties>"
    )


def app_properties_xml(workbook: Workbook) -> bytes:
    heading_pairs = (
        f"<vt:vector size=\"2\" baseType=\"variant\">"
        f"<vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant>"
        f"<vt:variant><vt:i4>{len(workbook.worksheets)}</vt:i4></vt:variant>"
        f"</vt:vector>"
    )
    titles = "".join(f"<vt:lpstr>{escape_xml(sheet.title)}</vt:lpstr>" for sheet in workbook.worksheets)
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\" "
        "xmlns:vt=\"http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes\">"
        "<Application>Codex</Application>"
        "<HeadingPairs>"
        f"{heading_pairs}"
        "</HeadingPairs>"
        "<TitlesOfParts>"
        f"<vt:vector size=\"{len(workbook.worksheets)}\" baseType=\"lpstr\">{titles}</vt:vector>"
        "</TitlesOfParts>"
        "</Properties>"
    ).encode("utf-8")


def escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def cell_xml(cell: Cell) -> str:
    coord = cell.coordinate
    value = cell.value
    if value is None:
        return ""
    if isinstance(value, bool):
        return f"<c r=\"{coord}\" t=\"b\"><v>{1 if value else 0}</v></c>"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"<c r=\"{coord}\"><v>{value}</v></c>"
    text = escape_xml(str(value))
    return f"<c r=\"{coord}\" t=\"inlineStr\"><is><t xml:space=\"preserve\">{text}</t></is></c>"


def pane_xml(freeze_panes: str | None) -> str:
    if not freeze_panes:
        return ""
    row, column = coordinate_to_tuple(freeze_panes)
    x_split = max(column - 1, 0)
    y_split = max(row - 1, 0)
    attrs = [f'topLeftCell="{freeze_panes}"', 'state="frozen"']
    if x_split:
        attrs.append(f'xSplit="{x_split}"')
    if y_split:
        attrs.append(f'ySplit="{y_split}"')
    if x_split and y_split:
        active_pane = "bottomRight"
    elif y_split:
        active_pane = "bottomLeft"
    elif x_split:
        active_pane = "topRight"
    else:
        active_pane = "topLeft"
    attrs.append(f'activePane="{active_pane}"')
    return f"<pane {' '.join(attrs)}/><selection pane=\"{active_pane}\" activeCell=\"{freeze_panes}\" sqref=\"{freeze_panes}\"/>"


def cols_xml(ws: Worksheet) -> str:
    cols: list[str] = []
    for label, dimension in sorted(ws.column_dimensions.items(), key=lambda item: column_index_from_string(item[0])):
        if dimension.width is None:
            continue
        idx = column_index_from_string(label)
        cols.append(f"<col min=\"{idx}\" max=\"{idx}\" width=\"{dimension.width}\" customWidth=\"1\"/>")
    return f"<cols>{''.join(cols)}</cols>" if cols else ""


def merges_xml(ws: Worksheet) -> str:
    if not ws._merged_ranges:
        return ""
    refs = []
    for start_row, start_column, end_row, end_column in ws._merged_ranges:
        start = coordinate_from_tuple(start_row, start_column)
        end = coordinate_from_tuple(end_row, end_column)
        refs.append(f"<mergeCell ref=\"{start}:{end}\"/>")
    return f"<mergeCells count=\"{len(refs)}\">{''.join(refs)}</mergeCells>"


def worksheet_xml(ws: Worksheet) -> bytes:
    max_row = ws.max_row
    max_col = ws.max_column
    dimension = f"A1:{coordinate_from_tuple(max_row, max_col)}"
    rows_xml: list[str] = []
    for row_idx in range(1, max_row + 1):
        cells_xml = "".join(cell_xml(ws.cell(row_idx, col_idx)) for col_idx in range(1, max_col + 1))
        if not cells_xml:
            continue
        rows_xml.append(f"<row r=\"{row_idx}\">{cells_xml}</row>")
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        f"<worksheet xmlns=\"{MAIN_NS}\" xmlns:r=\"{DOC_REL_NS}\">"
        f"<dimension ref=\"{dimension}\"/>"
        f"<sheetViews><sheetView workbookViewId=\"0\">{pane_xml(ws.freeze_panes)}</sheetView></sheetViews>"
        "<sheetFormatPr defaultRowHeight=\"15\"/>"
        f"{cols_xml(ws)}"
        f"<sheetData>{''.join(rows_xml)}</sheetData>"
        f"{merges_xml(ws)}"
        "</worksheet>"
    ).encode("utf-8")


def save_workbook(workbook: Workbook, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml(len(workbook.worksheets)))
        archive.writestr("_rels/.rels", package_rels_xml())
        archive.writestr("docProps/core.xml", core_properties_xml())
        archive.writestr("docProps/app.xml", app_properties_xml(workbook))
        archive.writestr("xl/workbook.xml", workbook_xml(workbook))
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml(len(workbook.worksheets)))
        archive.writestr("xl/styles.xml", minimal_styles_xml())
        for idx, sheet in enumerate(workbook.worksheets, start=1):
            archive.writestr(f"xl/worksheets/sheet{idx}.xml", worksheet_xml(sheet))


def parse_scalar(raw_value: str) -> Any:
    try:
        if raw_value.isdigit() or (raw_value.startswith("-") and raw_value[1:].isdigit()):
            return int(raw_value)
        return float(raw_value)
    except ValueError:
        return raw_value


def normalize_target(target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    if target.startswith("xl/"):
        return target
    return f"xl/{target}"


def load_workbook(path: str | Path, data_only: bool = False) -> Workbook:
    _ = data_only
    path = Path(path)
    with ZipFile(path) as archive:
        workbook_tree = ET.fromstring(archive.read("xl/workbook.xml"))
        rels_tree = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        target_by_rid = {
            rel.get("Id"): normalize_target(rel.get("Target", ""))
            for rel in rels_tree.findall(qn(PKG_REL_NS, "Relationship"))
        }
        workbook = Workbook()
        workbook.worksheets = []
        for sheet_el in workbook_tree.findall(f".//{qn(MAIN_NS, 'sheet')}"):
            title = sheet_el.get("name", "Sheet")
            rel_id = sheet_el.get(qn(DOC_REL_NS, "id"))
            target = target_by_rid.get(rel_id, "")
            ws = Worksheet(title)
            ws.sheet_state = sheet_el.get("state", "visible")
            if target:
                sheet_tree = ET.fromstring(archive.read(target))
                for cell_el in sheet_tree.findall(f".//{qn(MAIN_NS, 'c')}"):
                    coordinate = cell_el.get("r")
                    if not coordinate:
                        continue
                    row, column = coordinate_to_tuple(coordinate)
                    cell = ws.cell(row, column)
                    cell_type = cell_el.get("t")
                    if cell_type == "inlineStr":
                        text_el = cell_el.find(f".//{qn(MAIN_NS, 't')}")
                        cell.value = text_el.text if text_el is not None else ""
                    elif cell_type == "b":
                        value_el = cell_el.find(qn(MAIN_NS, "v"))
                        cell.value = value_el is not None and value_el.text == "1"
                    else:
                        value_el = cell_el.find(qn(MAIN_NS, "v"))
                        if value_el is not None and value_el.text is not None:
                            cell.value = parse_scalar(value_el.text)
                pane_el = sheet_tree.find(f".//{qn(MAIN_NS, 'pane')}")
                if pane_el is not None and pane_el.get("topLeftCell"):
                    ws.freeze_panes = pane_el.get("topLeftCell")
            workbook.worksheets.append(ws)
    return workbook
