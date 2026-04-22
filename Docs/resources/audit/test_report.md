# Public Resource Audit Test Report

- Date: 2026-04-22
- Passes: 52
- Fails: 0

## Checks

- **PASS** `public cli entrypoint exists`: Expected /Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py
- **PASS** `new arable raw files exist`: Expected land-class, target-capacity, and comparator-capacity raw files.
- **PASS** `new wood raw files exist`: Expected wood land-class, target-capacity, and comparator-capacity raw files.
- **PASS** `non-arable benchmark registry exists`: Expected non_arable_benchmark_cases.csv to be the authoritative non-land comparator registry.
- **PASS** `readme follows the explanatory paper-style structure`: Missing README terms: 
- **PASS** `overview plus one sheet per SB state`: Visible sheets: ['Overview', 'Cape Colony', 'Northern Cape', 'Eastern Cape', 'West Transvaal', 'Eastern Transvaal', 'Northern Transvaal', 'Transorangia', 'Drakensberg', 'Botswana', 'Lourenço Marques', 'Zambezi', 'Hereroland', 'Namaqualand']
- **PASS** `overview sheet sections`: Missing sections: 
- **PASS** `each state sheet has totals and resource table sections`: Missing sections on: 
- **PASS** `visible sheets are generated output`: Formula cells on visible sheets: 0
- **PASS** `data readmes exist`: Missing docs: 
- **PASS** `data/README classifies the package`: README classification text missing.
- **PASS** `raw data README classifies inputs`: README classification text missing.
- **PASS** `derived data README classifies outputs`: README classification text missing.
- **PASS** `no .DS_Store files remain under Docs/resources`: 
- **PASS** `formula-driving raw files expose validation columns`: Missing validation columns in: 
- **PASS** `target data validation output exists and is populated`: Rows=360
- **PASS** `validation discount and drive-x rules hold`: 
- **PASS** `validation notes ship without placeholder language`: 
- **PASS** `new audit tables exist`: Missing state_regional_advantages.csv or state_review_status.csv
- **PASS** `regional advantages and state review status are populated`: advantages=13, review_status=13
- **PASS** `arable rows are removed from gdp selection output`: Unexpected arable GDP rows: 0
- **PASS** `wood rows are removed from gdp selection output`: Unexpected wood GDP rows: 0
- **PASS** `arable target capacity rows cover all states and land classes`: Rows=78, expected=78
- **PASS** `arable comparator capacity rows are populated`: Rows=672
- **PASS** `wood target capacity rows cover all states and land classes`: Rows=78, expected=78
- **PASS** `wood comparator capacity rows are populated`: Rows=120
- **PASS** `shared arable denominator matches simple mean of state means`: shared=55846.153846153844, expected=55846.153846153844
- **PASS** `all arable rows use the shared land-capacity denominator`: States with non-shared arable denominator: 
- **PASS** `arable rows use direct land-capacity X with no GDP fields or legacy Y/Z`: 
- **PASS** `arable spot-check outcomes are playable and directionally plausible`: 
- **PASS** `arable resource expectations are now a gameplay audit surface`: Missing fields: 
- **PASS** `arable basket/live mismatch reporting still works`: Basket logic failures: 
- **PASS** `overview totals mirror regional_resource_totals.csv`: Mismatches: 
- **PASS** `major tag changes mirror regional_resource_totals.csv`: Mismatches: 
- **PASS** `state sheets mirror vanilla baselines and audited SB updates`: Mismatches: 
- **PASS** `live state file sync remains frozen`: Auto-sync disabled; 0 live mismatches are expected during the audit pass.
- **PASS** `wood uses dedicated effective-forestry denominator path`: Wood path failures: 
- **PASS** `non-arable benchmark registry and gold-mine denominator path are wired`: 
- **PASS** `public target observations no longer expose formula-driving wood estate rows`: Wood rows are absent from target_observations.csv
- **PASS** `target observation output exposes validation and discounted evidence fields`: Missing fields: 
- **PASS** `wood rows use the land-capacity contract with no GDP metadata`: 
- **PASS** `wood restoration allowance never exceeds the 50 percent cap`: Cap failures: 
- **PASS** `wood spot-check outcomes are directionally plausible`: 
- **PASS** `unsupported tropical-rubber carry-over rows are retired`: 
- **PASS** `sentinel provenance scenarios behave as intended`: 
- **PASS** `row audit file exists`: row_audit rows=195, final_caps rows=195
- **PASS** `row audit fields are populated`: Rows missing audit fields: 0
- **PASS** `hard zeros carry explicit audit support or exception status`: Unsupported hard zeros: 0
- **PASS** `regional totals match final caps aggregation`: 0 regional mismatches.
- **PASS** `state delta summary matches final caps aggregation`: 
- **PASS** `state delta exports exist and mirror final caps`: 
- **PASS** `priority rows file exists`: Priority rows: 169

## Current Priority Rows

- `P1` `Botswana / Arable Land`: arable audit/gameplay mismatch
- `P1` `Botswana / Coal Mine`: explicit audit exception
- `P1` `Cape Colony / Gold Fields (discovered)`: explicit audit exception
- `P1` `Cape Colony / Gold Fields (undiscovered)`: explicit audit exception
- `P1` `Cape Colony / Gold Mine`: explicit audit exception
- `P1` `Cape Colony / Iron Mine`: explicit audit exception
- `P1` `Cape Colony / Lead Mine`: explicit audit exception
- `P1` `Cape Colony / Oil (discovered)`: explicit audit exception
- `P1` `Cape Colony / Oil (undiscovered)`: explicit audit exception
- `P1` `Cape Colony / Rubber (discovered)`: explicit audit exception
- `P1` `Cape Colony / Rubber (undiscovered)`: explicit audit exception
- `P1` `Cape Colony / Sulfur Mine`: explicit audit exception
- `P1` `Cape Colony / Whaling`: explicit audit exception
- `P1` `Drakensberg / Arable Land`: arable audit/gameplay mismatch
- `P1` `Drakensberg / Coal Mine`: explicit audit exception
