import pandas as pd
import matplotlib.pyplot as plt

def normalize_indexes(players_df, name_col='player_name', index_col='index'):
    """
    Normalizes player indexes to a 0-100 scale based on the highest rated player.
    
    Args:
        players_df: DataFrame containing player names and their raw index scores
        name_col: Name of the column containing player names
        index_col: Name of the column containing the index scores
        
    Returns:
        DataFrame with original data plus a new column 'normalized_index'
    """
    # Create a copy to avoid modifying the original
    df = players_df.copy()
    
    # Get the maximum index score
    max_index = df[index_col].max()
    
    # Calculate normalized scores (0-100 scale)
    df['normalized_index'] = (df[index_col] / max_index) * 100
    
    # Sort by normalized index descending
    df = df.sort_values('normalized_index', ascending=False).reset_index(drop=True)
    
    return df

def plot_top_10_indexes(players_df, name_col='player_name', index_col='normalized_index', 
                       title='Top 10 Players by Index', save_path=None):
    """
    Creates a 1D line plot of the top 10 players, with 10th player on the left
    and the GOAT (1st player) on the right.
    
    Args:
        players_df: DataFrame containing player names and their normalized index scores
        name_col: Name of the column containing player names
        index_col: Name of the column containing the normalized index scores
        title: Title for the plot
        save_path: If provided, saves the plot to this path
    """
    # Get top 10 players
    top_10 = players_df.head(10).copy()
    # Reverse the order for plotting (10th -> 1st)
    top_10 = top_10.iloc[::-1].reset_index(drop=True)
    
    plt.figure(figsize=(12, 4))
    
    # Get the minimum index for x-axis start
    min_index = top_10[index_col].min()
    
    # Create the 1D line plot
    plt.hlines(y=0, xmin=min_index, xmax=100, color='gray', alpha=0.3)  # Horizontal baseline
    plt.plot(top_10[index_col], [0] * len(top_10), 'o', color='black', markersize=6)
    
    # Add player names as annotations with staggered heights for overlapping names
    for i, row in top_10.iterrows():
        # Calculate vertical offset - higher offset for names on the left side
        if i < 5:  # First half of players (left side)
            y_offset = 15 - (i % 2) * 8  # Alternate between 15 and 7
        else:
            y_offset = 7
        
        plt.annotate(row[name_col], 
                    xy=(row[index_col], 0),
                    xytext=(2, y_offset),  # Shift text slightly right and use calculated y_offset
                    textcoords='offset points',
                    ha='left',  # Align text to the left of the point
                    va='bottom',
                    rotation=45)
    
    plt.title(title)
    plt.xlabel("Normalized Index Score (0-100)")
    plt.yticks([])  # Hide y-axis ticks
    plt.xlim(min_index - 2, 105)  # Start from minimum index with small padding
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

# Example usage:
if __name__ == "__main__":
    # Example data
    data = {
        'player_name': ['Player A', 'Player B', 'Player C'],
        'index': [850, 750, 650]
    }
    df = pd.DataFrame(data)
    
    # Normalize the indexes
    normalized_df = normalize_indexes(df)
    print("Normalized Indexes:")
    print(normalized_df)
    
    # Plot top 10 (in this example, only 3 players)
    plot_top_10_indexes(normalized_df, save_path='normalized_index_plot.png') 