from __future__ import annotations

import csv
import importlib.util
import io
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests


SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR.parent
PUBLIC_ROOT = SCRIPTS_DIR.parent
MOD_ROOT = PUBLIC_ROOT.parents[2]
BUILD_PUBLIC = SCRIPT_DIR / "build_resources_workbook.py"
OUTPUT = PUBLIC_ROOT / "data/raw/generated_comparator_data.py"
CACHE_DIR = PUBLIC_ROOT / ".cache"


ABS_WINTER_URL = "https://www.abs.gov.au/statistics/industry/agriculture/australian-agriculture-broadacre-crops/2023-24/AABDC_Winter_Broadacre_202324.xlsx"
ABS_SUGARCANE_URL = "https://www.abs.gov.au/statistics/industry/agriculture/australian-agriculture-broadacre-crops/2023-24/AABDC_Sugarcane_202324.xlsx"
ABS_HORT_URL = "https://www.abs.gov.au/statistics/industry/agriculture/australian-agriculture-horticulture/2023-24/AAHDC_Aust_Horticulture_202324.xlsx"
ABS_CATTLE_URL = "https://www.abs.gov.au/statistics/industry/agriculture/australian-agriculture-livestock/2023-24/AALDC_Cattle%20herd%20series_2005%20to%202024.xlsx"
ABS_SHEEP_URL = "https://www.abs.gov.au/statistics/industry/agriculture/australian-agriculture-livestock/2023-24/AALDC_Sheep%20flock%20series_2005%20to%202022.xlsx"
CHILE_CROPS_URL = "https://bibliotecadigital.odepa.gob.cl/bitstream/handle/20.500.12650/74178/CultivosRegional072025.xls"
CHILE_VINES_URL = "https://bibliotecadigital.odepa.gob.cl/bitstreams/abccac3e-705d-4a8b-a16c-cbe35c9841eb/download"
CHILE_LIVESTOCK_URL = "https://bibliotecadigital.odepa.gob.cl/bitstreams/fd09efd0-c13b-4652-be10-42ddca3650a8/download"
MADRID_LIVESTOCK_URL = "https://www.comunidad.madrid/noticias/2018/01/19/comunidad-redujo-desempleo-agricultura-ganaderia-2017-103"

ARG_ESTIMACIONES_URL = "https://datosestimaciones.magyp.gob.ar/reportes.php?reporte=Estimaciones"
ARG_BOVINOS_URL = "https://sitioanterior.indec.gob.ar/agropecuario/cuadros/c20_tot.xls"
ARG_OVINOS_URL = "https://sitioanterior.indec.gob.ar/agropecuario/cuadros/c22_tot.xls"
ARG_CAPRINOS_URL = "https://sitioanterior.indec.gob.ar/agropecuario/cuadros/c23_tot.xls"

IBGE_AGG_CROPS = 5457
IBGE_AGG_LIVESTOCK = 3939


BRAZIL_UF_CODES = {
    "Bahia": "29",
    "Espírito Santo": "32",
    "Federal District": "53",
    "Goiás": "52",
    "Maranhão": "21",
    "Mato Grosso": "51",
    "Mato Grosso do Sul": "50",
    "Minas Gerais": "31",
    "Paraná": "41",
    "Pernambuco": "26",
    "Rio Grande do Sul": "43",
    "Santa Catarina": "42",
    "São Paulo": "35",
    "Alagoas": "27",
}

ARGENTINA_PROVINCE_NAMES = {
    "Buenos Aires Province": "BUENOS AIRES",
    "Chaco Province": "CHACO",
    "Corrientes": "CORRIENTES",
    "Córdoba Province": "CORDOBA",
    "Entre Ríos": "ENTRE RIOS",
    "Entre Ríos Province": "ENTRE RIOS",
    "Formosa Province": "FORMOSA",
    "Jujuy Province": "JUJUY",
    "La Pampa": "LA PAMPA",
    "La Rioja Province": "LA RIOJA",
    "Mendoza Province": "MENDOZA",
    "Misiones Province": "MISIONES",
    "Salta Province": "SALTA",
}

ARGENTINA_LIVESTOCK_NAMES = {
    "Buenos Aires Province": "Buenos Aires",
    "Chaco Province": "Chaco",
    "Corrientes": "Corrientes",
    "Córdoba Province": "Córdoba",
    "Entre Ríos": "Entre Ríos",
    "Entre Ríos Province": "Entre Ríos",
    "Formosa Province": "Formosa",
    "Jujuy Province": "Jujuy",
    "La Pampa": "La Pampa",
    "La Rioja Province": "La Rioja",
    "Mendoza Province": "Mendoza",
    "Misiones Province": "Misiones",
    "Salta Province": "Salta",
}

CHILE_REGION_NAMES = {
    "04 Coquimbo": "Coquimbo Region",
    "05 Valparaíso": "Valparaíso Region",
    "06 O'Higgins": "O'Higgins Region",
    "07 Maule": "Maule Region",
    "08 Bío Bío": "Biobío Region",
    "08 Biobío": "Biobío Region",
    "16 Ñuble": "Ñuble Region",
}

CHILE_LIVESTOCK_COMPARATORS = {
    "Atacama": "Atacama Region",
    "Atacama ": "Atacama Region",
    "Coquimbo": "Coquimbo Region",
    "Valparaíso": "Valparaíso Region",
    "Valparaíso 1/": "Valparaíso Region",
    "O'Higgins": "O'Higgins Region",
    "Maule": "Maule Region",
    "Ñuble": "Ñuble Region",
    "Biobío": "Biobío Region",
}

RESOURCE_CROP_TERMS = {
    "Wheat Farm": ["trigo"],
    "Maize Farm": ["maiz", "milho"],
    "Millet Farm": ["sorgo", "mijo", "millet"],
    "Sugar Plantation": ["cana-de-açúcar", "cana de azucar", "sugarcane", "caña de azúcar"],
    "Tobacco Plantation": ["fumo", "tabaco", "tobacco"],
    "Banana Plantation": ["banana", "bananas"],
    "Cotton Plantation": ["algodão", "algodon", "cotton"],
    "Vineyard": ["uva", "wine grape", "wine grapes", "grape crush"],
    "Tea Plantation": ["tea", "chá", "cha"],
}

IBGE_CROP_CODES = {
    "Wheat Farm": 40127,
    "Maize Farm": 40122,
    "Sugar Plantation": 40106,
    "Tobacco Plantation": 40113,
    "Banana Plantation": 40136,
    "Cotton Plantation": 40099,
    "Vineyard": 40274,
}

US_STATE_COMPARATORS = {
    "Arizona": "ARIZONA",
    "California": "CALIFORNIA",
    "Colorado": "COLORADO",
    "Florida": "FLORIDA",
    "Georgia": "GEORGIA",
    "Kansas": "KANSAS",
    "Kansas / central Great Plains": "KANSAS",
    "Kentucky": "KENTUCKY",
    "Louisiana": "LOUISIANA",
    "Lower Rio Grande / South Texas": "TEXAS",
    "Nebraska": "NEBRASKA",
    "Nevada": "NEVADA",
    "New Mexico": "NEW MEXICO",
    "North Carolina": "NORTH CAROLINA",
    "North Carolina Piedmont": "NORTH CAROLINA",
    "Oklahoma": "OKLAHOMA",
    "San Luis Valley / southern Rockies": "COLORADO",
    "South Carolina": "SOUTH CAROLINA",
    "South Florida": "FLORIDA",
    "South Texas brush country": "TEXAS",
    "Tennessee": "TENNESSEE",
    "Texas": "TEXAS",
    "Utah": "UTAH",
    "Virginia": "VIRGINIA",
    "Virginia Piedmont": "VIRGINIA",
    "Wyoming": "WYOMING",
}

US_OVERVIEW_RESOURCE_PATTERNS = {
    "Wheat Farm": ("WHEAT", "t output", 0.0272155),
    "Maize Farm": ("CORN, GRAIN", "t output", 0.0254),
    "Millet Farm": ("SORGHUM, GRAIN", "t output", 0.0254),
    "Sugar Plantation": ("SUGARCANE", "t output", 1.0),
    "Tobacco Plantation": ("TOBACCO", "t output", 0.00045359237),
    "Cotton Plantation": ("COTTON", "bales lint cotton", 1.0),
    "Vineyard": ("GRAPES", "t output", 1.0),
}


def load_build_public_module():
    spec = importlib.util.spec_from_file_location("build_public_resources_workbook", BUILD_PUBLIC)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", value).strip().lower()


def cache_path(name: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / name


def fetch_binary(url: str, cache_name: str, post_data: dict[str, str] | None = None) -> bytes:
    path = cache_path(cache_name)
    if path.exists():
        return path.read_bytes()
    if post_data:
        response = requests.post(url, data=post_data, timeout=120)
    else:
        response = requests.get(url, timeout=120)
    response.raise_for_status()
    path.write_bytes(response.content)
    return response.content


def parse_rankings(build_public) -> tuple[list[dict[str, object]], dict[str, list[str]]]:
    rankings = build_public.parse_agricultural_rankings()
    current = build_public.parse_live_state_resources()
    resources_by_sheet: dict[str, list[str]] = {}
    for info in build_public.STATE_INFO:
        enabled = [
            resource
            for _category, resource in build_public.BINARY_RESOURCES
            if current[info["official_name"]].get(resource) == "yes"
        ]
        resources_by_sheet[info["sheet_key"]] = enabled
    return rankings, resources_by_sheet


def make_geography(comparator: str, proxy_state_id: str | None, proxy_name: str | None) -> str:
    lines = [comparator]
    if proxy_state_id:
        lines.append(proxy_state_id)
    if proxy_name:
        lines.append(f"Vanilla name: {proxy_name}")
    return "\n".join(lines)


def build_row(
    *,
    sheet_key: str,
    comparator: str,
    proxy_state_id: str | None,
    proxy_name: str | None,
    resource: str,
    year: int,
    quantity: float,
    unit: str,
    title: str,
    url: str,
    locator: str,
    note: str,
) -> dict[str, object]:
    return {
        "sheet": sheet_key,
        "geography": make_geography(comparator, proxy_state_id, proxy_name),
        "resource": resource,
        "year": year,
        "normalized_quantity": quantity,
        "normalized_unit": unit,
        "source_quantity": f"{quantity}",
        "source_unit": unit,
        "source_title": title,
        "source_url": url,
        "citation_locator": locator,
        "note": note,
    }


def load_abs_frames() -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for url, name in [
        (ABS_WINTER_URL, "abs_winter.xlsx"),
        (ABS_SUGARCANE_URL, "abs_sugar.xlsx"),
        (ABS_HORT_URL, "abs_hort.xlsx"),
        (ABS_CATTLE_URL, "abs_cattle.xlsx"),
        (ABS_SHEEP_URL, "abs_sheep.xlsx"),
    ]:
        path = cache_path(name)
        if not path.exists():
            path.write_bytes(fetch_binary(url, name))
        frames[name] = pd.ExcelFile(path)
    return frames


def abs_series_rows(xlsx: pd.ExcelFile, sheet_name: str, data_item_contains: str) -> list[tuple[str, int, float]]:
    df = pd.read_excel(xlsx, sheet_name=sheet_name, header=4)
    year_cols = [col for col in df.columns if re.search(r"\d", str(col))]
    rows: list[tuple[str, int, float]] = []
    for _, row in df.iterrows():
        region = row.get("Region")
        data_item = row.get("Data item")
        if not isinstance(region, str) or region == "Australia":
            continue
        if not isinstance(data_item, str) or data_item_contains.lower() not in data_item.lower():
            continue
        for col in year_cols:
            value = row[col]
            if pd.isna(value):
                continue
            year_text = str(col)
            year_match = re.search(r"(\d{4})", year_text)
            if not year_match:
                continue
            year = int(year_match.group(1))
            rows.append((region, year, float(value)))
    return rows


def load_abs_data() -> dict[tuple[str, str], dict[str, object]]:
    frames = load_abs_frames()
    result: dict[tuple[str, str], dict[str, object]] = {}

    wheat_rows = abs_series_rows(frames["abs_winter.xlsx"], "Table 1", "Levied production")
    sugar_rows = abs_series_rows(frames["abs_sugar.xlsx"], "Table 1", "Levied production")
    banana_rows = abs_series_rows(frames["abs_hort.xlsx"], "Table 2", "Bananas - Production")
    grape_rows = abs_series_rows(frames["abs_hort.xlsx"], "Table 6", "Wine grape crush")

    def add_max(rows: list[tuple[str, int, float]], resource: str, url: str, title: str, locator_prefix: str, unit: str = "t output") -> None:
        by_region: dict[str, tuple[int, float]] = {}
        for region, year, value in rows:
            if value <= 0:
                continue
            if region not in by_region or value > by_region[region][1]:
                by_region[region] = (year, value * (1000 if "000" in locator_prefix else 1))
        for region, (year, value) in by_region.items():
            locator = f"{locator_prefix}; row {region}; max available year {year}."
            result[(region, resource)] = {
                "year": year,
                "quantity": value,
                "unit": unit,
                "title": title,
                "url": url,
                "locator": locator,
                "note": "ABS official state and territory series; maximum available series value used.",
            }

    add_max(
        wheat_rows,
        "Wheat Farm",
        ABS_WINTER_URL,
        "Australian Agriculture: Broadacre Crops, 2023-24",
        "Table 1, Wheat for grain or seed - Levied production (t)",
    )
    add_max(
        sugar_rows,
        "Sugar Plantation",
        ABS_SUGARCANE_URL,
        "Australian Agriculture: Broadacre Crops, 2023-24",
        "Table 1, Sugarcane for processing - Levied production (t)",
    )
    add_max(
        banana_rows,
        "Banana Plantation",
        ABS_HORT_URL,
        "Australian Agriculture: Horticulture, 2023-24",
        "Table 2, Bananas - Production (t)",
    )
    add_max(
        grape_rows,
        "Vineyard",
        ABS_HORT_URL,
        "Australian Agriculture: Horticulture, 2023-24",
        "Table 6, Wine grape crush (t)",
    )

    cattle_rows = abs_series_rows(frames["abs_cattle.xlsx"], "Table 1", "Beef cattle - Total")
    sheep_rows = abs_series_rows(frames["abs_sheep.xlsx"], "Table 1", "Sheep and lambs - Total")
    cattle_by_region: dict[str, tuple[int, float]] = {}
    sheep_by_region: dict[str, tuple[int, float]] = {}
    for region, year, value in cattle_rows:
        if region not in cattle_by_region or value > cattle_by_region[region][1]:
            cattle_by_region[region] = (year, value)
    for region, year, value in sheep_rows:
        if region not in sheep_by_region or value > sheep_by_region[region][1]:
            sheep_by_region[region] = (year, value)
    for region in sorted(set(cattle_by_region) | set(sheep_by_region)):
        cattle_year, cattle_value = cattle_by_region.get(region, (0, 0.0))
        sheep_year, sheep_value = sheep_by_region.get(region, (0, 0.0))
        total = cattle_value + sheep_value
        if total <= 0:
            continue
        result[(region, "Livestock Ranch")] = {
            "year": max(cattle_year, sheep_year),
            "quantity": total,
            "unit": "head livestock",
            "title": "Australian Agriculture: Livestock, 2023-24",
            "url": ABS_CATTLE_URL,
            "locator": f"Table 1 cattle herd series plus sheep flock series; {region}; cattle max year {cattle_year}, sheep max year {sheep_year}.",
            "note": "Generic livestock proxy built from cattle plus sheep series because Victoria 3 ranching combines large- and small-stock systems.",
        }
    return result


def load_us_overview_tables(state_code: str) -> list[pd.DataFrame]:
    cache_name = f"us_overview_{state_code.lower().replace(' ', '_')}.html"
    html = fetch_binary(
        f"https://www.nass.usda.gov/Quick_Stats/Ag_Overview/stateOverview.php?state={quote(state_code)}&year=2024",
        cache_name,
    ).decode("utf-8", errors="ignore")
    return pd.read_html(io.StringIO(html))


def parse_us_number(value: object) -> float | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).replace(",", "").strip()
    if not text or text.upper() == "NA":
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    return float(match.group(0))


def load_us_state_overview_data() -> dict[tuple[str, str], dict[str, object]]:
    result: dict[tuple[str, str], dict[str, object]] = {}
    table_cache: dict[str, list[pd.DataFrame]] = {}

    def tables_for(code: str) -> list[pd.DataFrame]:
        if code not in table_cache:
            table_cache[code] = load_us_overview_tables(code)
        return table_cache[code]

    for comparator, state_code in US_STATE_COMPARATORS.items():
        try:
            tables = tables_for(state_code)
        except Exception:
            continue
        if len(tables) < 4:
            continue
        livestock = tables[1].copy()
        crops = tables[3].copy()

        livestock_total = 0.0
        livestock_found = False
        livestock_bits: list[str] = []
        for label, unit in [
            ("Cattle, Incl Calves - Inventory", "cattle"),
            ("Sheep, Incl Lambs - Inventory", "sheep"),
        ]:
            mask = livestock.iloc[:, 0].astype(str).str.contains(label, na=False)
            if mask.any():
                value = parse_us_number(livestock.loc[mask].iloc[0, 1])
                if value is not None:
                    livestock_total += value
                    livestock_found = True
                    livestock_bits.append(f"{label} = {int(value):,}")
        if livestock_found:
            result[(comparator, "Livestock Ranch")] = {
                "year": 2024,
                "quantity": livestock_total,
                "unit": "head livestock",
                "title": f"USDA/NASS 2024 State Agriculture Overview for {state_code.title()}",
                "url": f"https://www.nass.usda.gov/Quick_Stats/Ag_Overview/stateOverview.php?state={quote(state_code)}&year=2024",
                "locator": "Livestock inventory table; summed cattle including calves and sheep including lambs.",
                "note": "Generic livestock proxy built from USDA/NASS state inventory rows. " + "; ".join(livestock_bits),
            }

        crop_col = crops.columns[0]
        prod_col = "Production" if "Production" in crops.columns else crops.columns[5]
        for resource, (pattern, unit, multiplier) in US_OVERVIEW_RESOURCE_PATTERNS.items():
            mask = crops[crop_col].astype(str).str.fullmatch(pattern, case=False, na=False)
            if not mask.any():
                continue
            quantity = None
            raw_value = None
            for _, matched_row in crops.loc[mask].iterrows():
                candidate_raw = matched_row[prod_col]
                candidate_quantity = parse_us_number(candidate_raw)
                if candidate_quantity is None or candidate_quantity <= 0:
                    continue
                quantity = candidate_quantity * multiplier
                raw_value = candidate_raw
                break
            if quantity is None:
                continue
            note = "USDA/NASS State Agriculture Overview commodity summary row."
            locator = f"Commodity summary table; row {pattern}; production cell = {raw_value}."
            result[(comparator, resource)] = {
                "year": 2024,
                "quantity": quantity,
                "unit": unit,
                "title": f"USDA/NASS 2024 State Agriculture Overview for {state_code.title()}",
                "url": f"https://www.nass.usda.gov/Quick_Stats/Ag_Overview/stateOverview.php?state={quote(state_code)}&year=2024",
                "locator": locator,
                "note": note,
            }
    return result


def query_ibge(aggregate: int, variable: int, class_id: int, category_ids: list[int], state_codes: list[str]) -> dict[tuple[str, int], float]:
    categories = ",".join(str(item) for item in category_ids)
    states = ",".join(state_codes)
    url = (
        f"https://servicodados.ibge.gov.br/api/v3/agregados/{aggregate}/periodos/all/variaveis/{variable}"
        f"?localidades=N3[{states}]&classificacao={class_id}[{categories}]"
    )
    data = requests.get(url, timeout=120).json()
    result: dict[tuple[str, int], float] = {}
    for variable_block in data:
        for result_block in variable_block["resultados"]:
            category_name = next(iter(result_block["classificacoes"][0]["categoria"].values()))
            for series in result_block["series"]:
                state_name = series["localidade"]["nome"]
                for year_text, value in series["serie"].items():
                    if value in ("...", "-", "X"):
                        continue
                    year = int(year_text)
                    result[(state_name, year, category_name)] = float(value)
    return result


def load_brazil_data() -> dict[tuple[str, str], dict[str, object]]:
    result: dict[tuple[str, str], dict[str, object]] = {}
    state_codes = sorted(set(BRAZIL_UF_CODES.values()))
    crop_series = query_ibge(IBGE_AGG_CROPS, 214, 782, sorted(IBGE_CROP_CODES.values()), state_codes)
    livestock_series = query_ibge(IBGE_AGG_LIVESTOCK, 105, 79, [2670, 2677, 2681], state_codes)

    crop_name_to_resource = {
        "Milho (em grão)": "Maize Farm",
        "Trigo (em grão)": "Wheat Farm",
        "Cana-de-açúcar": "Sugar Plantation",
        "Fumo (em folha)": "Tobacco Plantation",
        "Banana (cacho)": "Banana Plantation",
        "Algodão herbáceo (em caroço)": "Cotton Plantation",
        "Uva": "Vineyard",
    }

    best_crop: dict[tuple[str, str], tuple[int, float]] = {}
    for (state_name, year, crop_name), value in crop_series.items():
        resource = crop_name_to_resource.get(crop_name)
        if not resource or value <= 0:
            continue
        key = (state_name, resource)
        if key not in best_crop or value > best_crop[key][1]:
            best_crop[key] = (year, value)

    for (state_name, resource), (year, value) in best_crop.items():
        result[(state_name, resource)] = {
            "year": year,
            "quantity": value,
            "unit": "t output",
            "title": "IBGE Produção Agrícola Municipal",
            "url": f"https://servicodados.ibge.gov.br/api/v3/agregados/{IBGE_AGG_CROPS}/periodos/all/variaveis/214",
            "locator": f"Aggregate 5457, product resource {resource}, state {state_name}, maximum available annual quantity {year}.",
            "note": "Official IBGE state series; maximum annual production in tons used.",
        }

    livestock_best: dict[str, tuple[int, float]] = {}
    by_state_year: dict[tuple[str, int], float] = {}
    for (state_name, year, species_name), value in livestock_series.items():
        if value <= 0:
            continue
        by_state_year[(state_name, year)] = by_state_year.get((state_name, year), 0.0) + value
    for key, value in by_state_year.items():
        state_name, year = key
        if state_name not in livestock_best or value > livestock_best[state_name][1]:
            livestock_best[state_name] = (year, value)
    for state_name, (year, value) in livestock_best.items():
        result[(state_name, "Livestock Ranch")] = {
            "year": year,
            "quantity": value,
            "unit": "head livestock",
            "title": "IBGE Pesquisa da Pecuária Municipal",
            "url": f"https://servicodados.ibge.gov.br/api/v3/agregados/{IBGE_AGG_LIVESTOCK}/periodos/all/variaveis/105",
            "locator": f"Aggregate 3939, bovino+ovino+caprino summed for state {state_name}, maximum available annual herd total in {year}.",
            "note": "Generic livestock proxy built from bovine, ovine, and caprine herd totals because the land-economy model combines ranching outputs.",
        }
    return result


def load_argentina_crop_data() -> dict[tuple[str, str], dict[str, object]]:
    csv_bytes = fetch_binary(ARG_ESTIMACIONES_URL, "argentina_estimaciones.csv", post_data={"Dataset": "Dataset"})
    by_key: dict[tuple[str, str], tuple[int, float, str]] = {}
    crop_terms = {
        "Wheat Farm": ["trigo"],
        "Maize Farm": ["maiz"],
        "Sugar Plantation": ["cana de azucar"],
        "Tobacco Plantation": ["tabaco"],
        "Cotton Plantation": ["algodon"],
        "Vineyard": ["uva", "vid"],
    }
    usecols = ["Provincia", "Cultivo", "Campana", "Producción (Tn)"]
    for chunk in pd.read_csv(io.BytesIO(csv_bytes), sep=";", encoding="latin1", usecols=usecols, chunksize=200000):
        chunk["Provincia_norm"] = chunk["Provincia"].astype(str).map(normalize_text)
        chunk["Cultivo_norm"] = chunk["Cultivo"].astype(str).map(normalize_text)
        for province_label, province_source in ARGENTINA_PROVINCE_NAMES.items():
            province_norm = normalize_text(province_source)
            subset = chunk[chunk["Provincia_norm"] == province_norm]
            if subset.empty:
                continue
            for resource, terms in crop_terms.items():
                resource_rows = subset[subset["Cultivo_norm"].apply(lambda value: any(term in value for term in terms))]
                if resource_rows.empty:
                    continue
                for _, row in resource_rows.iterrows():
                    try:
                        qty = float(row["Producción (Tn)"])
                    except Exception:
                        continue
                    if qty <= 0:
                        continue
                    campana = str(row["Campana"])
                    years = [int(y) for y in re.findall(r"\d{4}", campana)]
                    year = max(years) if years else 0
                    key = (province_label, resource)
                    if key not in by_key or qty > by_key[key][1]:
                        by_key[key] = (year, qty, str(row["Cultivo"]))
    result: dict[tuple[str, str], dict[str, object]] = {}
    for (province_label, resource), (year, qty, crop_name) in by_key.items():
        result[(province_label, resource)] = {
            "year": year,
            "quantity": qty,
            "unit": "t output",
            "title": "MAGyP Estimaciones Agrícolas dataset",
            "url": ARG_ESTIMACIONES_URL,
            "locator": f"Full dataset download; province {province_label}; crop {crop_name}; maximum reported production campaign ending {year}.",
            "note": "Official MAGyP crop production dataset by province; maximum annual tonnage used.",
        }
    return result


def read_argentina_livestock_table(url: str) -> dict[str, float]:
    data = fetch_binary(url, Path(url).name)
    path = cache_path(Path(url).name)
    if not path.exists():
        path.write_bytes(data)
    df = pd.read_excel(path, header=None)
    result: dict[str, float] = {}
    for idx in range(len(df)):
        province = df.iloc[idx, 0]
        total = df.iloc[idx, 1]
        if isinstance(province, str) and province.strip() and province.strip() != "Provincia":
            if province.strip().startswith("Total del país"):
                continue
            if pd.notna(total):
                try:
                    result[province.strip()] = float(total)
                except Exception:
                    continue
    return result


def load_argentina_livestock_data() -> dict[tuple[str, str], dict[str, object]]:
    bov = read_argentina_livestock_table(ARG_BOVINOS_URL)
    ov = read_argentina_livestock_table(ARG_OVINOS_URL)
    cap = read_argentina_livestock_table(ARG_CAPRINOS_URL)
    result: dict[tuple[str, str], dict[str, object]] = {}
    for comparator, province_name in ARGENTINA_LIVESTOCK_NAMES.items():
        total = bov.get(province_name, 0.0) + ov.get(province_name, 0.0) + cap.get(province_name, 0.0)
        if total <= 0:
            continue
        result[(comparator, "Livestock Ranch")] = {
            "year": 2002,
            "quantity": total,
            "unit": "head livestock",
            "title": "INDEC Censo Nacional Agropecuario 2002",
            "url": ARG_BOVINOS_URL,
            "locator": f"Table c20_tot.xls (bovinos), c22_tot.xls (ovinos), and c23_tot.xls (caprinos); province {province_name}; totals summed.",
            "note": "Generic livestock proxy built from bovine, ovine, and caprine provincial census heads.",
        }
    return result


def load_chile_data() -> dict[tuple[str, str], dict[str, object]]:
    result: dict[tuple[str, str], dict[str, object]] = {}

    crop_data = fetch_binary(CHILE_CROPS_URL, "chile_cultivos_regional.xls")
    crop_df = pd.read_excel(io.BytesIO(crop_data), sheet_name="Serie producción regional", header=3)
    crop_df["Año agrícola"] = crop_df["Año agrícola"].astype(str)
    region_col = "Región"
    crop_map = {
        "Trigo\nTotal": "Wheat Farm",
        "Maíz\nTotal": "Maize Farm",
        "Tabaco": "Tobacco Plantation",
    }
    crop_best: dict[tuple[str, str], tuple[int, float, str]] = {}
    for _, row in crop_df.iterrows():
        region_label = str(row.get(region_col, "")).strip()
        comparator = CHILE_REGION_NAMES.get(region_label)
        if not comparator:
            continue
        years = [int(y) for y in re.findall(r"\d{4}", str(row["Año agrícola"]))]
        if not years:
            continue
        year = max(years)
        for column, resource in crop_map.items():
            value = row.get(column)
            if pd.isna(value):
                continue
            try:
                quantity = float(value)
            except Exception:
                continue
            if quantity <= 0:
                continue
            key = (comparator, resource)
            if key not in crop_best or quantity > crop_best[key][1]:
                crop_best[key] = (year, quantity, column)
    for (comparator, resource), (year, quantity, column) in crop_best.items():
        result[(comparator, resource)] = {
            "year": year,
            "quantity": quantity,
            "unit": "t output",
            "title": "Odepa cultivos anuales regionales, 2025 update",
            "url": CHILE_CROPS_URL,
            "locator": f"Sheet 'Serie producción regional'; region {comparator}; column {column}; maximum annual production in metric tons for season ending {year}.",
            "note": "Official ODEPA regional crop-production series; maximum annual tonnage used.",
        }

    livestock_data = fetch_binary(CHILE_LIVESTOCK_URL, "chile_livestock.xlsx")
    livestock_file = io.BytesIO(livestock_data)
    livestock_sheets = {
        "Bovino": ("Existencia (cabezas)", 2),
        "Ovino": ("Unnamed: 0", 4),
        "Caprino": ("Unnamed: 0", 3),
    }
    combined: dict[tuple[str, int], float] = {}
    for sheet_name, (region_column, header_row) in livestock_sheets.items():
        df = pd.read_excel(livestock_file, sheet_name=sheet_name, header=header_row)
        livestock_file.seek(0)
        first_col = df.columns[0]
        for _, row in df.iterrows():
            region_label = str(row.get(first_col, "")).strip()
            comparator = CHILE_LIVESTOCK_COMPARATORS.get(region_label)
            if not comparator:
                continue
            for col in df.columns[1:]:
                year_match = re.search(r"\d{4}", str(col))
                if not year_match:
                    continue
                value = row.get(col)
                if pd.isna(value):
                    continue
                try:
                    quantity = float(value)
                except Exception:
                    continue
                if quantity <= 0:
                    continue
                year = int(year_match.group(0))
                combined[(comparator, year)] = combined.get((comparator, year), 0.0) + quantity
    by_comparator: dict[str, tuple[int, float]] = {}
    for (comparator, year), quantity in combined.items():
        if comparator not in by_comparator or quantity > by_comparator[comparator][1]:
            by_comparator[comparator] = (year, quantity)
    for comparator, (year, quantity) in by_comparator.items():
        result[(comparator, "Livestock Ranch")] = {
            "year": year,
            "quantity": quantity,
            "unit": "head livestock",
            "title": "Odepa existencias bovinos, ovinos y caprinos",
            "url": CHILE_LIVESTOCK_URL,
            "locator": f"Bovino/Ovino/Caprino sheets; region {comparator}; cattle, sheep, and goats summed; maximum annual herd total in {year}.",
            "note": "Official ODEPA regional herd counts; bovine, ovine, and caprine heads summed for the ranching proxy.",
        }

    return result


def load_madrid_data() -> dict[tuple[str, str], dict[str, object]]:
    html = fetch_binary(MADRID_LIVESTOCK_URL, "madrid_agri_2017.html").decode("utf-8", errors="ignore")
    match = re.search(r"1,83 millones de cabezas de ganado", html)
    if not match:
        return {}
    return {
        ("Community of Madrid", "Livestock Ranch"): {
            "year": 2017,
            "quantity": 1_830_000.0,
            "unit": "head livestock",
            "title": "La Comunidad redujo el desempleo en agricultura y ganadería en 2017 un 10,3 %",
            "url": MADRID_LIVESTOCK_URL,
            "locator": "Body text: '1,83 millones de cabezas de ganado'.",
            "note": "Official Comunidad de Madrid release used as a livestock-stock anchor for the Madrid comparator.",
        }
    }


def proxy_name(build_public, proxy_state_id: str) -> str:
    for info in build_public.STATE_INFO:
        if info["vanilla_proxy_id"] == proxy_state_id:
            return info["vanilla_proxy_name"]
    return proxy_state_id


def main() -> None:
    build_public = load_build_public_module()
    rankings, resources_by_sheet = parse_rankings(build_public)

    source_maps: list[dict[tuple[str, str], dict[str, object]]] = [
        load_abs_data(),
        load_us_state_overview_data(),
        load_brazil_data(),
        load_argentina_crop_data(),
        load_argentina_livestock_data(),
        load_chile_data(),
        load_madrid_data(),
    ]
    merged: dict[tuple[str, str], dict[str, object]] = {}
    for mapping in source_maps:
        merged.update(mapping)

    rows: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()
    for rank_row in rankings:
        sheet_key = rank_row["sheet_key"]
        comparator = rank_row["comparator"]
        resources = resources_by_sheet[sheet_key]
        proxy_state_id = rank_row["proxy_state_id"] or None
        proxy_state_name = proxy_name(build_public, proxy_state_id) if proxy_state_id else None
        for resource in resources:
            source = merged.get((comparator, resource))
            if not source:
                continue
            dedupe_key = (sheet_key, comparator, resource)
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            rows.append(
                build_row(
                    sheet_key=sheet_key,
                    comparator=comparator,
                    proxy_state_id=proxy_state_id,
                    proxy_name=proxy_state_name,
                    resource=resource,
                    year=int(source["year"]),
                    quantity=float(source["quantity"]),
                    unit=str(source["unit"]),
                    title=str(source["title"]),
                    url=str(source["url"]),
                    locator=str(source["locator"]),
                    note=str(source["note"]),
                )
            )

    OUTPUT.write_text(
        "from __future__ import annotations\n\n"
        f"GENERATED_HISTORICAL_ANCHORS = []\n\nGENERATED_MODERN_MAXIMA = {json.dumps(rows, ensure_ascii=False, indent=4)}\n",
        encoding="utf-8",
    )
    print(f'wrote {len(rows)} generated rows to {OUTPUT}')


if __name__ == "__main__":
    main()
