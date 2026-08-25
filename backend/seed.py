from db import get_connection, init_db

SAMPLE_PROJECTS = [
    (
        "TaskFlow",
        "A minimal kanban board for solo devs to track side projects without the clutter of full project management tools.",
        "https://github.com/example/taskflow",
        "https://taskflow-demo.vercel.app",
        "Ayesha Khan",
    ),
    (
        "VoiceNotes AI",
        "Turns rambling voice memos into clean, structured notes using speech-to-text plus an LLM summarizer.",
        "https://github.com/example/voicenotes-ai",
        "https://voicenotes-ai.netlify.app",
        "Bilal Ahmed",
    ),
    (
        "CampusEats",
        "A crowd-sourced menu and rating app for canteen food across university campuses in Lahore.",
        "https://github.com/example/campuseats",
        "https://campuseats.up.railway.app",
        "Hina Raza",
    ),
    (
        "GitPulse",
        "Visualizes your GitHub contribution patterns and suggests the best time of day for you to code.",
        "https://github.com/example/gitpulse",
        "https://gitpulse.pages.dev",
        "Usman Tariq",
    ),
    (
        "Roz Ka Kharcha",
        "A dead-simple daily expense tracker in Urdu and English, built for first-time budgeters.",
        "https://github.com/example/roz-ka-kharcha",
        "https://rozkakharcha.vercel.app",
        "Sara Malik",
    ),
    (
        "DevMatch",
        "Swipe-based matching app that pairs hackathon participants with complementary skill sets.",
        "https://github.com/example/devmatch",
        "https://devmatch.onrender.com",
        "Hamza Sheikh",
    ),
]


def seed() -> None:
    init_db()
    conn = get_connection()
    cur = conn.execute("SELECT COUNT(*) AS c FROM projects")
    if cur.fetchone()["c"] > 0:
        print("Projects already exist, skipping seed.")
        conn.close()
        return

    conn.executemany(
        """
        INSERT INTO projects (name, description, github_url, deployed_url, submitter, episode)
        VALUES (?, ?, ?, ?, ?, 'Episode 1')
        """,
        SAMPLE_PROJECTS,
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(SAMPLE_PROJECTS)} sample projects.")


if __name__ == "__main__":
    seed()
