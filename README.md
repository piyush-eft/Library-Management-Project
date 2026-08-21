# 📚 Library Management System

A simple Library Management System built in Python — available in two versions:

1. **Terminal version** — a menu-driven CLI app using plain `input()`
2. **Web UI version** — the same core logic rebuilt with [Streamlit](https://streamlit.io) for a browser-based interface (This has been written entirely with help of claude Terminal version (main.py) is written solely by me)

Both versions store data locally in a `library.json` file, so your data persists between runs.

---

## Features

- ➕ Add new books (title, author, number of copies)
- 📖 List all books with available/total copy counts
- 🧑 Add new members (name, email)
- 👥 List all members along with their currently borrowed books
- 🔄 Borrow a book (checks availability before lending)
- ↩️ Return a book (updates available copies)

---

## Project Structure

```
library-management-system/
├── main.py           # Terminal (CLI) version
├── app.py            # Streamlit (Web UI) version
├── library.json       # Auto-created data file (books + members)
└── README.md
```

> `library.json` is created automatically on first run if it doesn't already exist. Both versions read and write the same file format, so data is shareable between them.

---

## Requirements

- Python 3.8+
- [Streamlit](https://pypi.org/project/streamlit/) (only needed for the Web UI version)

Install Streamlit:

```bash
pip install streamlit
```

---

## Running the Terminal Version

```bash
python main.py
```

You'll see a menu like this:

```
==================================================
Library Management System
==================================================
1. Add Book
2. List Book
3. Add Member
4. List Member
5. Borrow Book
6. Return Book
0. Exit Portal
--------------------------------------------------
```

Enter the number corresponding to the action you want, and follow the prompts.

---

## Running the Web UI Version

```bash
streamlit run app.py
```

This will open the app in your default browser (usually at `http://localhost:8501`). Use the sidebar to navigate between:

- Add Book
- List Books
- Add Member
- List Members
- Borrow Book
- Return Book

---

## Data Format

Data is stored in `library.json` with this structure:

```json
{
    "books": [
        {
            "Id": "B-XXXXX",
            "Title": "Book Title",
            "Author": "Author Name",
            "Total_copies": 3,
            "Available_copies": 2,
            "Add_on": "2026-08-21 10:00:00"
        }
    ],
    "members": [
        {
            "Id": "M-XXXXX",
            "Name": "Member Name",
            "E-mail": "member@example.com",
            "Borrowed": [
                {
                    "book_id": "B-XXXXX",
                    "Title": "Book Title",
                    "borrow_on": "2026-08-21 10:05:00"
                }
            ]
        }
    ]
}
```

- **Book IDs** are prefixed with `B-` (e.g. `B-7K2QX`)
- **Member IDs** are prefixed with `M-` (e.g. `M-9PLQZ`)
- IDs are randomly generated 5-character alphanumeric strings

---

## Known Limitations

- IDs are generated randomly rather than sequentially, so there's a very small chance of collision (not currently checked for).
- There's no edit/delete functionality for books or members yet.
- There's no search/filter feature — all books and members are listed in full.
- No authentication — anyone running the app has full access to all data.

---

## Possible Future Improvements

- [ ] Add search/filter for books and members
- [ ] Add edit/delete functionality
- [ ] Add due dates and overdue tracking for borrowed books
- [ ] Add basic authentication for members/admin
- [ ] Move from JSON storage to a proper database (SQLite)

---

## Author

Built as a learning project to practice Python fundamentals (file I/O, JSON handling, OOP with classmethods) and later extended into a Streamlit web app to practice UI development.
