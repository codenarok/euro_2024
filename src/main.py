# src/main.py

import sqlite3
from database import create_connection
from groups import initialize_groups

def record_match(group_name, team1, team2, team1_goals, team2_goals):
    """
    Record the result of a match and update team statistics.

    :param group_name: Name of the group
    :param team1: Name of the first team
    :param team2: Name of the second team
    :param team1_goals: Goals scored by the first team
    :param team2_goals: Goals scored by the second team
    """
    conn = create_connection()
    cur = conn.cursor()
    
    # Insert the match result into the matches table
    cur.execute("INSERT INTO matches (group_name, team1, team2, team1_goals, team2_goals) VALUES (?, ?, ?, ?, ?)",
                (group_name, team1, team2, team1_goals, team2_goals))
    
    # Update statistics for each team
    update_team_stats(cur, group_name, team1, team1_goals, team2_goals)
    update_team_stats(cur, group_name, team2, team2_goals, team1_goals)
    
    conn.commit()
    conn.close()

def update_team_stats(cur, group_name, team, goals_for, goals_against):
    """
    Update the statistics of a team after a match.

    :param cur: SQLite cursor object
    :param group_name: Name of the group
    :param team: Name of the team
    :param goals_for: Goals scored by the team
    :param goals_against: Goals conceded by the team
    """
    points = 0
    if goals_for > goals_against:
        points = 3  # Win
    elif goals_for == goals_against:
        points = 1  # Draw

    # Update the team's points, goal difference, goals scored, and wins
    cur.execute("""
        UPDATE groups
        SET points = points + ?, goal_difference = goal_difference + ?, goals_scored = goals_scored + ?, wins = wins + ?
        WHERE group_name = ? AND team_name = ?
    """, (points, goals_for - goals_against, goals_for, 1 if points == 3 else 0, group_name, team))

def main():
    """
    Main function to initialize groups and handle user input for match results.
    """
    initialize_groups()
    
    while True:
        # Prompt user for match details
        print("\nEnter match result:")
        group_name = input("Group: ")
        team1 = input("Team 1: ")
        team2 = input("Team 2: ")
        team1_goals = int(input(f"{team1} goals: "))
        team2_goals = int(input(f"{team2} goals: "))
        
        # Record the match result
        record_match(group_name, team1, team2, team1_goals, team2_goals)
        
        # Ask if the user wants to enter another match result
        cont = input("Enter another match result? (y/n): ")
        if cont.lower() != 'y':
            break

        TODO: Implement the function to calculate group standings
        def calculate_standings():
            pass

if __name__ == '__main__':
    main()
