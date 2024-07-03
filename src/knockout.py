# src/knockout.py

from database import create_connection

def get_group_standings():
    """Retrieve the standings for each group."""
    conn = create_connection()
    cur = conn.cursor()

    standings = {}
    groups = cur.execute("SELECT DISTINCT group_name FROM groups").fetchall()
    
    for group in groups:
        group_name = group[0]
        standings[group_name] = cur.execute("""
            SELECT team_name, points, goal_difference, goals_scored, wins
            FROM groups
            WHERE group_name = ?
            ORDER BY points DESC, goal_difference DESC, goals_scored DESC, wins DESC
        """, (group_name,)).fetchall()

    conn.close()
    return standings

def print_standings(standings):
    """Print the standings for each group."""
    for group_name, teams in standings.items():
        print(f"\n{group_name} Standings:")
        for team in teams:
            print(f"{team[0]} - Points: {team[1]}, Goal Difference: {team[2]}, Goals Scored: {team[3]}, Wins: {team[4]}")

def main():
    """Main function to retrieve and print group standings."""
    standings = get_group_standings()
    print_standings(standings)

if __name__ == '__main__':
    main()
