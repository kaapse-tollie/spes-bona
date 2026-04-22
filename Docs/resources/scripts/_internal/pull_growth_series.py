from __future__ import annotations

import json
from pathlib import Path

import requests


SCRIPT_DIR = Path(__file__).resolve().parent
PUBLIC_ROOT = SCRIPT_DIR.parents[1]
OUTPUT = PUBLIC_ROOT / "data/raw/generated_growth_series.py"

WORLD_BANK_URL = "https://api.worldbank.org/v2/country/WLD/indicator/NV.AGR.TOTL.KD?format=json&per_page=200"
WORLD_BANK_TITLE = "World Bank, Agriculture, forestry, and fishing, value added (constant 2015 US$)"
WORLD_BANK_SOURCE_URL = "https://api.worldbank.org/v2/country/WLD/indicator/NV.AGR.TOTL.KD?format=json&per_page=200"

NORA_1930_1932_TITLE = "Statistical Summary of the Mineral Industry 1930-1932"
NORA_1930_1932_URL = "https://nora.nerc.ac.uk/id/eprint/535282/1/SS_1930_1932.pdf"
NORA_1935_1937_TITLE = "Statistical Summary of the Mineral Industry 1935-1937"
NORA_1935_1937_URL = "https://nora.nerc.ac.uk/id/eprint/535283/1/SS_1935_1937.pdf"
NORA_1945_1951_TITLE = "Statistical Summary of the Mineral Industry 1945-1951"
NORA_1945_1951_URL = "https://nora.nerc.ac.uk/id/eprint/535285/1/SS_1945_1951.pdf"
NORA_1950_1955_TITLE = "Statistical Summary of the Mineral Industry 1950-1955"
NORA_1950_1955_URL = "https://nora.nerc.ac.uk/id/eprint/535280/1/SS_1950_1955.pdf"
WMD_2025_TITLE = "World Mining Data 2025"
WMD_2025_URL = "https://www.world-mining-data.info/wmd/downloads/PDF/WMD2025.pdf"
WORLDSTEEL_2025_TITLE = "World Steel in Figures 2025"
WORLDSTEEL_2025_URL = "https://worldsteel.org/wp-content/uploads/World-Steel-in-Figures-2025-1.pdf"


GROWTH_SERIES = {
    "Coal Mine": [
        {"year": 1930, "quantity": 1_390_000_000.0, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Coal table, 1930 world total = 1,390,000,000 long tons, converted to the published annual world series anchor."},
        {"year": 1931, "quantity": 1_240_000_000.0, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Coal table, 1931 world total."},
        {"year": 1932, "quantity": 1_110_000_000.0, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Coal table, 1932 world total."},
        {"year": 1935, "quantity": 1_310_000_000.0, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Coal table, 1935 world total."},
        {"year": 1936, "quantity": 1_420_000_000.0, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Coal table, 1936 world total."},
        {"year": 1937, "quantity": 1_510_000_000.0, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Coal table, 1937 world total."},
        {"year": 1945, "quantity": 1_324_000_000.0, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Coal table, 1945 world total."},
        {"year": 1946, "quantity": 1_445_000_000.0, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Coal table, 1946 world total."},
        {"year": 1947, "quantity": 1_622_000_000.0, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Coal table, 1947 world total."},
        {"year": 1950, "quantity": 1_792_000_000.0, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Coal table, 1950 world total."},
        {"year": 1951, "quantity": 1_900_000_000.0, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Coal table, 1951 world total."},
        {"year": 1952, "quantity": 1_900_000_000.0, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Coal table, 1952 world total."},
        {"year": 1953, "quantity": 1_926_000_000.0, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Coal table, 1953 world total."},
        {"year": 1954, "quantity": 1_941_000_000.0, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Coal table, 1954 world total."},
        {"year": 1955, "quantity": 2_102_000_000.0, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Coal table, 1955 world total."},
        {"year": 2019, "quantity": 7_748_825_405.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Coal Tot table, 2019 world total."},
        {"year": 2020, "quantity": 7_400_520_408.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Coal Tot table, 2020 world total."},
        {"year": 2021, "quantity": 7_786_779_490.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Coal Tot table, 2021 world total."},
        {"year": 2022, "quantity": 8_493_734_052.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Coal Tot table, 2022 world total."},
        {"year": 2023, "quantity": 8_727_852_902.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Coal Tot table, 2023 world total."},
    ],
    "Iron Mine": [
        {"year": 1930, "quantity": 178_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Iron ore table, 1930 world total = 178,000,000 long tons actual weight."},
        {"year": 1931, "quantity": 118_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Iron ore table, 1931 world total."},
        {"year": 1932, "quantity": 75_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Iron ore table, 1932 world total."},
        {"year": 1935, "quantity": 140_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Iron ore table, 1935 world total."},
        {"year": 1936, "quantity": 170_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Iron ore table, 1936 world total."},
        {"year": 1937, "quantity": 214_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Iron ore table, 1937 world total."},
        {"year": 1945, "quantity": 157_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Iron ore table, 1945 world total."},
        {"year": 1946, "quantity": 154_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Iron ore table, 1946 world total."},
        {"year": 1947, "quantity": 187_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Iron ore table, 1947 world total."},
        {"year": 1948, "quantity": 217_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Iron ore table, 1948 world total."},
        {"year": 1949, "quantity": 220_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Iron ore table, 1949 world total."},
        {"year": 1950, "quantity": 244_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Iron ore table, 1950 world total."},
        {"year": 1951, "quantity": 289_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Iron ore table, 1951 world total."},
        {"year": 1952, "quantity": 299_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Iron ore table, 1952 world total."},
        {"year": 1953, "quantity": 336_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Iron ore table, 1953 world total."},
        {"year": 1954, "quantity": 302_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Iron ore table, 1954 world total."},
        {"year": 1955, "quantity": 368_000_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Iron ore table, 1955 world total."},
        {"year": 2023, "quantity": 2_522_000_000.0, "unit": "t output", "source_title": WORLDSTEEL_2025_TITLE, "source_url": WORLDSTEEL_2025_URL, "locator": "Trade in iron ore, actual weight, 2023 world total = 2,522.0 Mt."},
    ],
    "Lead Mine": [
        {"year": 1930, "quantity": 1_640_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Lead table, 1930 world total = 1,640,000 long tons."},
        {"year": 1931, "quantity": 1_340_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Lead table, 1931 world total."},
        {"year": 1932, "quantity": 1_180_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Lead table, 1932 world total."},
        {"year": 1935, "quantity": 1_370_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Lead table, 1935 world total."},
        {"year": 1936, "quantity": 1_490_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Lead table, 1936 world total."},
        {"year": 1937, "quantity": 1_650_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Lead table, 1937 world total."},
        {"year": 1945, "quantity": 1_182_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Lead table, 1945 world total."},
        {"year": 1946, "quantity": 1_156_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Lead table, 1946 world total."},
        {"year": 1947, "quantity": 1_378_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Lead table, 1947 world total."},
        {"year": 1948, "quantity": 1_426_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Lead table, 1948 world total."},
        {"year": 1949, "quantity": 1_541_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Lead table, 1949 world total."},
        {"year": 1950, "quantity": 1_640_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Lead table, 1950 world total."},
        {"year": 1951, "quantity": 1_694_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Lead table, 1951 world total."},
        {"year": 1952, "quantity": 1_830_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Lead table, 1952 world total."},
        {"year": 1953, "quantity": 1_903_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Lead table, 1953 world total."},
        {"year": 1954, "quantity": 2_028_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Lead table, 1954 world total."},
        {"year": 1955, "quantity": 2_091_000.0 * 1.0160469088, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Lead table, 1955 world total."},
        {"year": 2019, "quantity": 4_896_049.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Lead table, 2019 world total."},
        {"year": 2020, "quantity": 4_692_777.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Lead table, 2020 world total."},
        {"year": 2021, "quantity": 4_597_548.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Lead table, 2021 world total."},
        {"year": 2022, "quantity": 4_691_012.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Lead table, 2022 world total."},
        {"year": 2023, "quantity": 4_704_599.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Lead table, 2023 world total."},
    ],
    "Gold Fields": [
        {"year": 1920, "quantity": 16_160_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Gold table retrospective series, 1920 world total = 16,160,000 fine oz."},
        {"year": 1921, "quantity": 15_970_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Gold table retrospective series, 1921 world total."},
        {"year": 1922, "quantity": 15_500_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Gold table retrospective series, 1922 world total."},
        {"year": 1930, "quantity": 20_900_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Gold table, 1930 world total."},
        {"year": 1931, "quantity": 22_400_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Gold table, 1931 world total."},
        {"year": 1932, "quantity": 24_000_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1930_1932_TITLE, "source_url": NORA_1930_1932_URL, "locator": "Gold table, 1932 world total."},
        {"year": 1935, "quantity": 29_600_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Gold table, 1935 world total."},
        {"year": 1936, "quantity": 33_300_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Gold table, 1936 world total."},
        {"year": 1937, "quantity": 34_600_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1935_1937_TITLE, "source_url": NORA_1935_1937_URL, "locator": "Gold table, 1937 world total."},
        {"year": 1945, "quantity": 20_800_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Gold table, 1945 world total."},
        {"year": 1946, "quantity": 21_300_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Gold table, 1946 world total."},
        {"year": 1947, "quantity": 21_800_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Gold table, 1947 world total."},
        {"year": 1948, "quantity": 22_400_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Gold table, 1948 world total."},
        {"year": 1949, "quantity": 23_400_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1945_1951_TITLE, "source_url": NORA_1945_1951_URL, "locator": "Gold table, 1949 world total."},
        {"year": 1950, "quantity": 24_200_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Gold table, 1950 world total."},
        {"year": 1951, "quantity": 23_700_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Gold table, 1951 world total."},
        {"year": 1952, "quantity": 24_300_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Gold table, 1952 world total."},
        {"year": 1953, "quantity": 24_200_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Gold table, 1953 world total."},
        {"year": 1954, "quantity": 25_700_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Gold table, 1954 world total."},
        {"year": 1955, "quantity": 26_900_000.0 * 0.0000311034768, "unit": "t output", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Gold table, 1955 world total."},
        {"year": 2019, "quantity": 3_313.849, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Gold table, 2019 world total = 3,313,849 kg."},
        {"year": 2020, "quantity": 3_202.740, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Gold table, 2020 world total = 3,202,740 kg."},
        {"year": 2021, "quantity": 3_220.656, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Gold table, 2021 world total = 3,220,656 kg."},
        {"year": 2022, "quantity": 3_297.464, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Gold table, 2022 world total = 3,297,464 kg."},
        {"year": 2023, "quantity": 3_266.418, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Gold table, 2023 world total = 3,266,418 kg."},
    ],
    "Sulfur Mine": [
        {"year": 1950, "quantity": 1.0, "unit": "index", "source_title": NORA_1950_1955_TITLE, "source_url": NORA_1950_1955_URL, "locator": "Synthetic 1950 base index used until a fuller annual sulfur reference series is added."},
        {"year": 2019, "quantity": 81_997_309.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Sulfur table, 2019 world total."},
        {"year": 2020, "quantity": 79_339_055.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Sulfur table, 2020 world total."},
        {"year": 2021, "quantity": 78_586_878.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Sulfur table, 2021 world total."},
        {"year": 2022, "quantity": 82_165_519.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Sulfur table, 2022 world total."},
        {"year": 2023, "quantity": 82_745_314.0, "unit": "t output", "source_title": WMD_2025_TITLE, "source_url": WMD_2025_URL, "locator": "Sulfur table, 2023 world total."},
    ],
}


def fetch_world_bank_land_series() -> list[dict[str, object]]:
    response = requests.get(WORLD_BANK_URL, timeout=120)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2:
        raise RuntimeError("Unexpected World Bank payload")
    rows = []
    for entry in payload[1]:
        value = entry.get("value")
        year = entry.get("date")
        if value is None or year is None:
            continue
        rows.append(
            {
                "year": int(year),
                "quantity": float(value),
                "unit": "constant 2015 US$",
                "source_title": WORLD_BANK_TITLE,
                "source_url": WORLD_BANK_SOURCE_URL,
                "locator": f"World aggregate annual value added; year {year}.",
            }
        )
    return sorted(rows, key=lambda row: int(row["year"]))


def main() -> None:
    payload = {
        "GROWTH_SERIES": GROWTH_SERIES,
        "LAND_ECONOMY_SERIES": fetch_world_bank_land_series(),
    }
    OUTPUT.write_text(
        "from __future__ import annotations\n\n"
        f"GROWTH_SERIES = {json.dumps(payload['GROWTH_SERIES'], ensure_ascii=False, indent=4)}\n\n"
        f"LAND_ECONOMY_SERIES = {json.dumps(payload['LAND_ECONOMY_SERIES'], ensure_ascii=False, indent=4)}\n",
        encoding="utf-8",
    )
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
