"""
Notebook Generation Pipeline for Hotel Booking Demand Analysis
=============================================================
This script constructs and executes the complete, professional-grade
Jupyter Notebook for the Hotel Booking Demand Analysis project,
covering all 78 tasks across Sections A through F.
"""

import sys
import io
import json
import base64
import os
import warnings
from typing import Dict, List, Tuple, Any, Optional

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

class NotebookBuilder:
    """Helper class to build and execute a Jupyter Notebook (.ipynb)."""

    def __init__(self, filename: str = "Hotel_Booking_Demand_Analysis.ipynb"):
        self.filename = filename
        self.cells = []
        self.execution_count = 1
        self.exec_env = {
            'pd': pd,
            'np': np,
            'plt': plt,
            'sns': sns,
            'warnings': warnings
        }

    def add_markdown(self, markdown_text: str):
        """Add a markdown cell to the notebook."""
        # Ensure proper newline termination
        lines = [line + '\n' for line in markdown_text.strip().split('\n')]
        if lines:
            lines[-1] = lines[-1].rstrip('\n')
        self.cells.append({
            'cell_type': 'markdown',
            'metadata': {},
            'source': lines
        })

    def add_code(self, code_text: str, execute: bool = True):
        """Add a code cell, execute it in the internal environment, and capture outputs."""
        lines = [line + '\n' for line in code_text.strip().split('\n')]
        if lines:
            lines[-1] = lines[-1].rstrip('\n')
        
        outputs = []
        if execute:
            old_stdout = sys.stdout
            redirected_output = io.StringIO()
            sys.stdout = redirected_output
            try:
                exec(code_text, self.exec_env)
            except Exception as e:
                import traceback
                print(f"Execution Error: {e}", file=sys.stderr)
                traceback.print_exc()
            finally:
                sys.stdout = old_stdout
            
            # Capture stdout text
            stdout_text = redirected_output.getvalue()
            if stdout_text:
                outputs.append({
                    'output_type': 'stream',
                    'name': 'stdout',
                    'text': stdout_text.splitlines(keepends=True)
                })
            
            # Capture matplotlib figures
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight', dpi=110)
                buf.seek(0)
                img_b64 = base64.b64encode(buf.read()).decode('utf-8')
                plt.close(fig)
                outputs.append({
                    'output_type': 'display_data',
                    'data': {
                        'image/png': img_b64,
                        'text/plain': '<Figure size ...>'
                    },
                    'metadata': {}
                })

        cell = {
            'cell_type': 'code',
            'execution_count': self.execution_count if execute else None,
            'metadata': {},
            'outputs': outputs,
            'source': lines
        }
        self.cells.append(cell)
        if execute:
            self.execution_count += 1

    def save(self):
        """Save the notebook to disk."""
        nb_json = {
            'cells': self.cells,
            'metadata': {
                'kernelspec': {
                    'display_name': 'Python 3 (ipykernel)',
                    'language': 'python',
                    'name': 'python3'
                },
                'language_info': {
                    'name': 'python',
                    'version': '3.12.10',
                    'mimetype': 'text/x-python',
                    'codemirror_mode': {'name': 'ipython', 'version': 3},
                    'pygments_lexer': 'ipython3',
                    'nbconvert_exporter': 'python',
                    'file_extension': '.py'
                }
            },
            'nbformat': 4,
            'nbformat_minor': 5
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(nb_json, f, indent=2, ensure_ascii=False)
        print(f"Successfully generated {self.filename} with {len(self.cells)} cells!")

print("NotebookBuilder module defined successfully.")
