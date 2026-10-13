import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

def calculate_correlations_and_ranks(file_path):
    """
    Calculate correlations and ranks, then write to Excel in YB format
    """
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    
    # Extract the metrics columns
    systems = df['system'].tolist()
    comet_scores = df['comet'].tolist()
    bleu_scores = df['BLEU'].tolist()
    chrf2_scores = df['chrF2'].tolist()
    ter_scores = df['TER'].tolist()
    
    # Calculate Pearson correlations
    r_comet_bleu, _ = pearsonr(comet_scores, bleu_scores)
    r_comet_chrf2, _ = pearsonr(comet_scores, chrf2_scores)
    r_bleu_chrf2, _ = pearsonr(bleu_scores, chrf2_scores)
    
    # Calculate ranks (lower rank = better score, so for TER we need to reverse since lower TER is better)
    comet_ranks = [sorted(comet_scores, reverse=True).index(x) + 1 for x in comet_scores]
    bleu_ranks = [sorted(bleu_scores, reverse=True).index(x) + 1 for x in bleu_scores]
    chrf2_ranks = [sorted(chrf2_scores, reverse=True).index(x) + 1 for x in chrf2_scores]
    ter_ranks = [sorted(ter_scores).index(x) + 1 for x in ter_scores]  # Lower TER is better
    
    # Calculate Spearman correlations (using ranks)
    rho_comet_bleu, _ = spearmanr(comet_ranks, bleu_ranks)
    rho_comet_chrf2, _ = spearmanr(comet_ranks, chrf2_ranks)
    rho_bleu_chrf2, _ = spearmanr(bleu_ranks, chrf2_ranks)
    
    # Create new DataFrame with all the calculated values
    result_df = pd.DataFrame({
        'system': systems,
        'COMET': comet_scores,
        'BLEU': bleu_scores,
        'chrF2': chrf2_scores,
        'TER': ter_scores,
        'r(COMET,BLEU)': [r_comet_bleu] + [''] * (len(systems) - 1),
        'r(COMET,chrF2)': [r_comet_chrf2] + [''] * (len(systems) - 1),
        'r(BLEU,chrF2)': [r_bleu_chrf2] + [''] * (len(systems) - 1),
        'COMET_rank': comet_ranks,
        'BLEU_rank': bleu_ranks,
        'chrF2_rank': chrf2_ranks,
        'TER_rank': ter_ranks,
        'rho(COMET,BLEU)': [rho_comet_bleu] + [''] * (len(systems) - 1),
        'rho(COMET,chrF2)': [rho_comet_chrf2] + [''] * (len(systems) - 1),
        'rho(BLEU,chrF2)': [rho_bleu_chrf2] + [''] * (len(systems) - 1)
    })
    
    return result_df, {
        'r_comet_bleu': r_comet_bleu,
        'r_comet_chrf2': r_comet_chrf2,
        'r_bleu_chrf2': r_bleu_chrf2,
        'rho_comet_bleu': rho_comet_bleu,
        'rho_comet_chrf2': rho_comet_chrf2,
        'rho_bleu_chrf2': rho_bleu_chrf2
    }

def write_to_excel(original_file_path, result_df, correlations):
    """
    Write the results to a new sheet in the original Excel file
    """
    # Load the workbook
    book = openpyxl.load_workbook(original_file_path)
    
    # Create a new sheet or overwrite existing one
    if 'Correlations' in book.sheetnames:
        del book['Correlations']
    sheet = book.create_sheet('Correlations')
    
    # Add title (mimicking YB format)
    sheet['A1'] = 'wh_mateo-eval-corr_2903-3178_ko-en'
    
    # Leave some empty rows
    start_row = 6
    
    # Write headers
    headers = ['', 'COMET', 'BLEU', 'chrF2', 'TER', '', 
               'r(COMET,BLEU)', 'r(COMET,chrF2)', 'r(BLEU,chrF2)', '',
               'COMET_rank', 'BLEU_rank', 'chrF2_rank', 'TER_rank', '',
               'rho(COMET,BLEU)', 'rho(COMET,chrF2)', 'rho(BLEU,chrF2)']
    
    for col, header in enumerate(headers, 1):
        sheet.cell(row=start_row-1, column=col, value=header)
    
    # Write data
    for r_idx, row in enumerate(dataframe_to_rows(result_df, index=False, header=False), start_row):
        for c_idx, value in enumerate(row, 1):
            sheet.cell(row=r_idx, column=c_idx, value=value)
    
    # Save the workbook
    book.save(original_file_path)
    
    print(f"Results successfully written to {original_file_path} in sheet 'Correlations'")

def print_full_results(result_df, correlations):
    """
    Print the complete results including all systems and full correlation analysis
    """
    print(f"\n{'='*100}")
    print("COMPLETE CORRELATION ANALYSIS RESULTS")
    print(f"{'='*100}")
    
    print(f"\nPEARSON CORRELATIONS (r):")
    print(f"r(COMET, BLEU):   {correlations['r_comet_bleu']:.4f}")
    print(f"r(COMET, chrF2):  {correlations['r_comet_chrf2']:.4f}")
    print(f"r(BLEU, chrF2):   {correlations['r_bleu_chrf2']:.4f}")
    
    print(f"\nSPEARMAN CORRELATIONS (ρ):")
    print(f"ρ(COMET, BLEU):   {correlations['rho_comet_bleu']:.4f}")
    print(f"ρ(COMET, chrF2):  {correlations['rho_comet_chrf2']:.4f}")
    print(f"ρ(BLEU, chrF2):   {correlations['rho_bleu_chrf2']:.4f}")
    
    # Interpretation
    print(f"\nCORRELATION STRENGTH INTERPRETATION:")
    correlation_data = {
        'Pearson COMET-BLEU': correlations['r_comet_bleu'],
        'Pearson COMET-chrF2': correlations['r_comet_chrf2'],
        'Pearson BLEU-chrF2': correlations['r_bleu_chrf2'],
        'Spearman COMET-BLEU': correlations['rho_comet_bleu'],
        'Spearman COMET-chrF2': correlations['rho_comet_chrf2'],
        'Spearman BLEU-chrF2': correlations['rho_bleu_chrf2']
    }
    
    for key, value in correlation_data.items():
        strength = "strong" if abs(value) > 0.7 else "moderate" if abs(value) > 0.3 else "weak"
        direction = "positive" if value > 0 else "negative"
        print(f"  {key}: {strength} {direction} correlation ({value:.4f})")
    
    print(f"\n{'='*100}")
    print("COMPLETE SYSTEM RANKINGS AND SCORES")
    print(f"{'='*100}")
    
    # Display all systems with their scores and ranks
    display_df = result_df[['system', 'COMET', 'BLEU', 'chrF2', 'TER', 
                           'COMET_rank', 'BLEU_rank', 'chrF2_rank', 'TER_rank']].copy()
    
    # Sort by COMET rank (best first)
    display_df = display_df.sort_values('COMET_rank')
    
    print(f"\n{'System':<30} {'COMET':<8} {'BLEU':<8} {'chrF2':<8} {'TER':<8} {'COMET_R':<8} {'BLEU_R':<8} {'chrF2_R':<8} {'TER_R':<8}")
    print(f"{'-'*30} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    
    for _, row in display_df.iterrows():
        print(f"{row['system']:<30} {row['COMET']:<8.2f} {row['BLEU']:<8.2f} {row['chrF2']:<8.2f} {row['TER']:<8.2f} "
              f"{row['COMET_rank']:<8} {row['BLEU_rank']:<8} {row['chrF2_rank']:<8} {row['TER_rank']:<8}")
    
    # Print summary statistics
    print(f"\n{'='*100}")
    print("SUMMARY STATISTICS")
    print(f"{'='*100}")
    
    print(f"\nTotal number of systems evaluated: {len(result_df)}")
    print(f"\nScore Ranges:")
    print(f"COMET:  {min(result_df['COMET']):.2f} - {max(result_df['COMET']):.2f}")
    print(f"BLEU:   {min(result_df['BLEU']):.2f} - {max(result_df['BLEU']):.2f}")
    print(f"chrF2:  {min(result_df['chrF2']):.2f} - {max(result_df['chrF2']):.2f}")
    print(f"TER:    {min(result_df['TER']):.2f} - {max(result_df['TER']):.2f}")
    
    # Top performers
    print(f"\nTOP PERFORMERS BY METRIC:")
    top_comet = result_df.loc[result_df['COMET_rank'] == 1, 'system'].iloc[0]
    top_bleu = result_df.loc[result_df['BLEU_rank'] == 1, 'system'].iloc[0]
    top_chrf2 = result_df.loc[result_df['chrF2_rank'] == 1, 'system'].iloc[0]
    top_ter = result_df.loc[result_df['TER_rank'] == 1, 'system'].iloc[0]
    
    print(f"Best COMET:  {top_comet}")
    print(f"Best BLEU:   {top_bleu}")
    print(f"Best chrF2:  {top_chrf2}")
    print(f"Best TER:    {top_ter}")

def main():
    # File path - replace with your actual file path
    file_path = "5_wh_mateo-eval-corr_2903-3178_ko-en.xlsx"
    
    try:
        print("Reading Excel file...")
        # Calculate correlations and ranks
        result_df, correlations = calculate_correlations_and_ranks(file_path)
        
        # Print full results
        print_full_results(result_df, correlations)
        
        # Write to Excel
        write_to_excel(file_path, result_df, correlations)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please check the file path.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please make sure:")
        print("1. The file has the expected structure with columns: 'system', 'comet', 'BLEU', 'chrF2', 'TER'")
        print("2. The file is not open in another program")
        print("3. You have write permissions for the file")

if __name__ == "__main__":
    main()