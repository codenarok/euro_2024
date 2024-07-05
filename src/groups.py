# src/groups.py

from database import create_connection

def initialize_groups():
    #initialize groups IF the groups table is blank. 
    """Insert the initial group and team data into the database."""
    groups = {
        'Group A': ['Germany', 'Scotland', 'Hungary', 'Switzerland'],
        'Group B': ['Spain', 'Croatia', 'Italy', 'Albania'],
        'Group C': ['Slovenia', 'Denmark', 'Serbia', 'England'],
        'Group D': ['Poland', 'Netherlands', 'Austria', 'France'],
        'Group E': ['Belgium', 'Slovakia', 'Romania', 'Ukraine'],
        'Group F': ['Türkiye', 'Georgia', 'Portugal', 'Czechia']
    }

    conn = create_connection()
    cur = conn.cursor()

    for group_name, teams in groups.items():
        for team in teams:
            cur.execute("INSERT OR IGNORE INTO groups (group_name, team_name) VALUES (?, ?)", (group_name, team))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_groups()
