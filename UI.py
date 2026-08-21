import json
import random
import string
from datetime import datetime
from pathlib import Path

import streamlit as st

DATABASE = "library.json"


# ----------------------------------------------------------------------
# DATA LAYER (same idea as your original Library class, minus input())
# ----------------------------------------------------------------------

def load_data():
    """Load library.json, or create it with empty structure if missing."""
    path = Path(DATABASE)
    if path.exists():
        content = path.read_text().strip()
        if content:
            return json.loads(content)
    data = {"books": [], "members": []}
    save_data(data)
    return data


def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4, default=str)


def gen_id(prefix="B"):
    random_id = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    return f"{prefix}-{random_id}"


# Streamlit reruns the whole script on every interaction, so we load data
# once into session_state instead of re-reading the file every rerun.
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


def persist():
    save_data(data)


# ----------------------------------------------------------------------
# ACTIONS (bug-fixed versions of your original methods)
# ----------------------------------------------------------------------

def add_book(title, author, copies):
    book = {
        "Id": gen_id("B"),
        "Title": title,
        "Author": author,
        "Total_copies": copies,
        "Available_copies": copies,
        "Add_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    data["books"].append(book)
    persist()
    return book


def add_member(name, email):
    member = {
        "Id": gen_id("M"),
        "Name": name,
        "E-mail": email,
        "Borrowed": [],
    }
    data["members"].append(member)
    persist()
    return member


def find_member(member_id):
    matches = [m for m in data["members"] if m["Id"] == member_id]
    return matches[0] if matches else None


def find_book(book_id):
    matches = [b for b in data["books"] if b["Id"] == book_id]
    return matches[0] if matches else None


def borrow_book(member_id, book_id):
    """Returns (success: bool, message: str)."""
    member = find_member(member_id)
    if member is None:
        return False, "No member found with that ID."

    book = find_book(book_id)
    if book is None:
        return False, "No book found with that ID."

    if book["Available_copies"] <= 0:
        return False, "No available copies of that book right now."

    borrow_entry = {
        "book_id": book["Id"],
        "Title": book["Title"],
        "borrow_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    member["Borrowed"].append(borrow_entry)
    book["Available_copies"] -= 1
    persist()
    return True, f"'{book['Title']}' borrowed successfully by {member['Name']}."


def return_book(member_id, borrow_index):
    """Returns (success: bool, message: str). borrow_index is 0-based."""
    member = find_member(member_id)
    if member is None:
        return False, "No member found with that ID."

    if not member["Borrowed"]:
        return False, "This member has no borrowed books."

    try:
        selected = member["Borrowed"].pop(borrow_index)
    except IndexError:
        return False, "Invalid selection."

    book = find_book(selected["book_id"])
    if book is not None:
        # FIX: original code incremented copies only when the book was
        # NOT found, which is backwards. We increment when it IS found.
        book["Available_copies"] += 1

    persist()
    return True, f"'{selected['Title']}' returned successfully."


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------

st.set_page_config(page_title="Library Management System", page_icon="📚", layout="wide")
st.title("📚 Library Management System")

page = st.sidebar.radio(
    "Menu",
    ["Add Book", "List Books", "Add Member", "List Members", "Borrow Book", "Return Book"],
)

# ---- Add Book ----
if page == "Add Book":
    st.header("Add a New Book")
    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("Title")
        author = st.text_input("Author")
        copies = st.number_input("Number of copies", min_value=1, step=1, value=1)
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if not title.strip() or not author.strip():
                st.error("Title and Author cannot be empty.")
            else:
                book = add_book(title.strip(), author.strip(), int(copies))
                st.success(f"Book added! ID: {book['Id']}")

# ---- List Books ----
elif page == "List Books":
    st.header("All Books")
    if not data["books"]:
        st.info("No books found.")
    else:
        st.dataframe(
            [
                {
                    "ID": b["Id"],
                    "Title": b["Title"],
                    "Author": b["Author"],
                    "Total Copies": b["Total_copies"],
                    "Available": b["Available_copies"],
                    "Added On": b["Add_on"],
                }
                for b in data["books"]
            ],
            use_container_width=True,
            hide_index=True,
        )

# ---- Add Member ----
elif page == "Add Member":
    st.header("Add a New Member")
    with st.form("add_member_form", clear_on_submit=True):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Member")

        if submitted:
            if not name.strip() or not email.strip():
                st.error("Name and Email cannot be empty.")
            else:
                member = add_member(name.strip(), email.strip())
                st.success(f"Member added! ID: {member['Id']}")

# ---- List Members ----
elif page == "List Members":
    st.header("All Members")
    if not data["members"]:
        st.info("No members found.")
    else:
        for m in data["members"]:
            with st.expander(f"{m['Id']} — {m['Name']} ({m['E-mail']})"):
                if not m["Borrowed"]:
                    st.write("No books currently borrowed.")
                else:
                    st.table(
                        [
                            {"Book ID": b["book_id"], "Title": b["Title"], "Borrowed On": b["borrow_on"]}
                            for b in m["Borrowed"]
                        ]
                    )

# ---- Borrow Book ----
elif page == "Borrow Book":
    st.header("Borrow a Book")

    if not data["members"]:
        st.warning("No members exist yet. Add a member first.")
    elif not data["books"]:
        st.warning("No books exist yet. Add a book first.")
    else:
        member_options = {f"{m['Id']} — {m['Name']}": m["Id"] for m in data["members"]}
        book_options = {
            f"{b['Id']} — {b['Title']} ({b['Available_copies']} available)": b["Id"]
            for b in data["books"]
        }

        member_label = st.selectbox("Select Member", list(member_options.keys()))
        book_label = st.selectbox("Select Book", list(book_options.keys()))

        if st.button("Borrow"):
            success, message = borrow_book(member_options[member_label], book_options[book_label])
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

# ---- Return Book ----
elif page == "Return Book":
    st.header("Return a Book")

    if not data["members"]:
        st.warning("No members exist yet.")
    else:
        member_options = {f"{m['Id']} — {m['Name']}": m["Id"] for m in data["members"]}
        member_label = st.selectbox("Select Member", list(member_options.keys()))
        member_id = member_options[member_label]
        member = find_member(member_id)

        if not member["Borrowed"]:
            st.info("This member has no borrowed books.")
        else:
            borrowed_options = {
                f"{b['Title']} ({b['book_id']}) — borrowed {b['borrow_on']}": i
                for i, b in enumerate(member["Borrowed"])
            }
            choice_label = st.selectbox("Select book to return", list(borrowed_options.keys()))

            if st.button("Return"):
                success, message = return_book(member_id, borrowed_options[choice_label])
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)