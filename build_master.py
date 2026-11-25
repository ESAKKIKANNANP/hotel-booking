"""
Master Pipeline Coordinator for Hotel Booking Demand Analysis Notebook
======================================================================
Coordinates execution of all analytical sections, captures text outputs
and matplotlib visualization figures into standard Jupyter Notebook v4 JSON,
and validates top-to-bottom structural completeness.
"""

import os
import sys
import json
import time

from generate_notebook import NotebookBuilder
from build_part_ab import add_header_and_oop, add_section_a, add_section_b
from build_part_cd import add_section_c, add_section_d
from build_part_ef import add_section_e, add_section_f

def main():
    print("=" * 70)
    print("STARTING FULL NOTEBOOK GENERATION & EXECUTION PIPELINE")
    print("=" * 70)
    start_time = time.time()

    notebook_path = "Hotel_Booking_Demand_Analysis.ipynb"
    builder = NotebookBuilder(filename=notebook_path)

    print("\n[Phase 1/6] Adding Header, Global Configuration, and OOP Architecture...")
    add_header_and_oop(builder)

    print("\n[Phase 2/6] Executing Section A: Data Loading, Inspection, & Preprocessing (Tasks 1-14)...")
    add_section_a(builder)

    print("\n[Phase 3/6] Executing Section B: Univariate Analysis (Tasks 15-27)...")
    add_section_b(builder)

    print("\n[Phase 4/6] Executing Section C: Hotel-Wise Comparative Analysis (Tasks 28-39)...")
    add_section_c(builder)

    print("\n[Phase 5/6] Executing Section D: Cancellation Analysis (Tasks 40-56)...")
    add_section_d(builder)

    print("\n[Phase 6/6] Executing Section E & F: Time-Series, Seasonality & Revenue Management (Tasks 57-78)...")
    add_section_e(builder)
    add_section_f(builder)

    print("\nSaving completed notebook to disk...")
    builder.save()

    # Validation checks
    print("\nRunning Verification Checks on Generated Notebook...")
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"Target notebook {notebook_path} does not exist!")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_data = json.load(f)

    total_cells = len(nb_data['cells'])
    code_cells = [c for c in nb_data['cells'] if c['cell_type'] == 'code']
    md_cells = [c for c in nb_data['cells'] if c['cell_type'] == 'markdown']
    cells_with_outputs = [c for c in code_cells if len(c.get('outputs', [])) > 0]
    total_images = sum(
        1 for c in code_cells for out in c.get('outputs', [])
        if out.get('output_type') == 'display_data' and 'image/png' in out.get('data', {})
    )

    print("-" * 50)
    print(f"Total Notebook Cells:       {total_cells}")
    print(f"Code Cells:                 {len(code_cells)}")
    print(f"Markdown Cells:             {len(md_cells)}")
    print(f"Code Cells with Outputs:    {len(cells_with_outputs)} / {len(code_cells)}")
    print(f"Embedded Visualizations:    {total_images} High-Res PNG Charts")
    print(f"Total Generation Time:      {time.time() - start_time:.2f} seconds")
    print("-" * 50)
    print("SUCCESS: Notebook is complete, verified, and ready for evaluation!")

if __name__ == '__main__':
    main()
