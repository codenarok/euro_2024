# src/main.py

from database import create_connection
from groups import initialize_groups

def record_match(group_name, team1, team2, team1_goals, team2_goals):
    """Record the match result and update the teams' statistics."""
    conn = create_connection()
    cur = conn.cursor()
    
    # Record the match
    cur.execute("INSERT INTO matches (group_name, team1, team2, team1_goals, team2_goals) VALUES (?, ?, ?, ?, ?)",
                (group_name, team1, team2, team1_goals, team2_goals))
    
    # Update team stats
    update_team_stats(cur, group_name, team1, team1_goals, team2_goals)
    update_team_stats(cur, group_name, team2, team2_goals, team1_goals)
    
    conn.commit()
    conn.close()

def update_team_stats(cur, group_name, team, goals_for, goals_against):
    """Update the team statistics based on the match result."""
    points = 0
    if goals_for > goals_against:
        points = 3
    elif goals_for == goals_against:
        points = 1

    # Fetch current stats
    cur.execute("""
        SELECT points, goal_difference, goals_scored, wins
        FROM groups
        WHERE group_name = ? AND team_name = ?
    """, (group_name, team))
    
    result = cur.fetchone()
    
    if result:
        current_points, current_goal_difference, current_goals_scored, current_wins = result
        
        # Calculate new stats
        new_points = current_points + points
        new_goal_difference = current_goal_difference + (goals_for - goals_against)
        new_goals_scored = current_goals_scored + goals_for
        new_wins = current_wins + (1 if points == 3 else 0)
        
        # Explicitly set new values by adding current values with new values
        cur.execute(f"""
            UPDATE groups
            SET points = {new_points}, goal_difference = {new_goal_difference}, goals_scored = {new_goals_scored}, wins = {new_wins}
            WHERE group_name = '{group_name}' AND team_name = '{team}'
        """)


def main():
    """Main function to initialize groups and enter match results."""
    initialize_groups()
    
    while True:
        print("\nEnter match result:")
        group_name = input("Group: ")
        team1 = input("Team 1: ")
        team2 = input("Team 2: ")
        team1_goals = int(input(f"{team1} goals: "))
        team2_goals = int(input(f"{team2} goals: "))
        
        record_match(group_name, team1, team2, team1_goals, team2_goals)
        
        cont = input("Enter another match result? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == '__main__':
    main()
