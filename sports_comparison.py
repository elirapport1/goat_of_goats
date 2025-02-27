"""
1) plot gaps between goat and no 2 for each sport. in description include min and max.
2) plot eras of goats answering questions what 10 year span had the most goats
3) create a data visualization of geopgraphical representations
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def load_sport_data(sport_dir):
    """Load normalized index data for a sport if available."""
    # Try different possible CSV filenames
    possible_files = [
        f"{sport_dir}_index_scored.csv",
        f"{sport_dir.replace('mens_', '')}_index_scored.csv",
        f"{sport_dir.replace('womens_', '')}_index_scored.csv"
    ]
    
    for filename in possible_files:
        filepath = os.path.join(sport_dir, filename)
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
    return None

def calculate_goat_gaps():
    """Calculate the gap between the top 2 players for each sport."""
    # Get all sport directories
    sport_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d not in ['env', '__pycache__']]
    
    gaps = []
    for sport_dir in sport_dirs:
        df = load_sport_data(sport_dir)
        if df is not None and 'normalized_index' in df.columns and 'player_name' in df.columns:
            if len(df) >= 2:  # Need at least 2 players
                gap = df.iloc[0]['normalized_index'] - df.iloc[1]['normalized_index']
                goat_name = df.iloc[0]['player_name']
                sport_name = sport_dir.replace('_', ' ').title()
                gaps.append({
                    'sport': sport_name,
                    'gap': gap,
                    'goat': goat_name
                })
    
    return pd.DataFrame(gaps)

def plot_goat_gaps(gaps_df):
    """Create a bar plot of GOAT gaps across sports."""
    # Sort by gap size descending
    gaps_df = gaps_df.sort_values('gap', ascending=True)
    
    # Create the plot
    plt.figure(figsize=(15, 10))
    bars = plt.barh(gaps_df['sport'], gaps_df['gap'])
    
    # Customize the plot
    plt.title('Gap Between GOAT and Second-Best Player Across Sports\n(Normalized Index Score Difference)', 
             pad=20, fontsize=14)
    plt.xlabel('Gap in Normalized Index Score (0-100 scale)')
    
    # Add value labels and GOAT names
    for i, bar in enumerate(bars):
        gap = gaps_df.iloc[i]['gap']
        goat = gaps_df.iloc[i]['goat']
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                f'  {gap:.1f} ({goat})',
                va='center')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('goat_gaps.png', dpi=300, bbox_inches='tight')
    
    # Print summary statistics
    print(f"\nLargest gap: {gaps_df.iloc[-1]['sport']} - {gaps_df.iloc[-1]['gap']:.1f}")
    print(f"Smallest gap: {gaps_df.iloc[0]['sport']} - {gaps_df.iloc[0]['gap']:.1f}")
    print(f"Average gap: {gaps_df['gap'].mean():.1f}")

def main():
    gaps_df = calculate_goat_gaps()
    plot_goat_gaps(gaps_df)

if __name__ == "__main__":
    main()


