# Hotel Management System

A command-line hotel management program written in Python. A receptionist can view available rooms, book a room for a guest, check a guest out with a final bill, and see who is currently staying. Data is saved to a JSON file, so records are kept after the program closes.

Built for the **Python Essentials** course (VITyarthi, Build Your Own Project).

## Overview

The program is split into small modules (menu, business logic, validation, storage, billing). Every rule, such as the 3-person limit or the 12-digit Aadhaar check, lives in one place and is covered by unit tests. Only the last 4 digits of an Aadhaar number are ever stored or shown.

## Features

- **Show available rooms** with type, breakfast option and price per day
- **Book a room**: choose room type and breakfast, enter guest details, get a receipt
- **Book several rooms** in a row
- **Checkout**: final bill and the room becomes available again
- **Current guest report**
- **Input validation**: people (1 to 3), days (1 to 30), phone (10 digits), Aadhaar (12 digits), name
- **Aadhaar masking**: shown and stored as `XXXX-XXXX-1234`
- **Data saved to file** (`data/hotel_data.json`) with safe writing
- **Logging** of bookings, checkouts and errors (`logs/hotel.log`)

## Technologies Used

- Python 3.8 or newer (standard library only: `json`, `logging`, `dataclasses`, `pathlib`, `unittest`)
- Git and GitHub for version control
- Graphviz (only to draw the design diagrams for the report)

## Project Structure

```
hotel_management_system/
├── main.py                  # entry point
├── hotel/
│   ├── cli.py               # menus, prompts, printing
│   ├── booking_service.py   # book and checkout logic
│   ├── room_manager.py      # find and list rooms
│   ├── billing.py           # total and receipt text
│   ├── validators.py        # input rules
│   ├── storage.py           # JSON load and save
│   ├── models.py            # Room and Guest classes
│   ├── config.py            # constants and default rooms
│   ├── exceptions.py        # custom errors
│   └── logger_setup.py      # logging setup
├── tests/                   # unit tests
├── docs/diagrams/           # architecture and UML diagrams
├── data/                    # saved data (created automatically)
├── statement.md
├── requirements.txt
└── README.md
```

## Installation and Running

No packages need to be installed. You only need Python.

1. **Check Python** (3.8 or newer):
   ```bash
   python --version
   ```
   On some systems use `python3` instead of `python` in every command below.

2. **Get the project**:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

3. **(Optional) Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   ```

4. **Install dependencies** (there are none, this only confirms setup):
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the program**:
   ```bash
   python main.py
   ```

6. **Use the menu**: type the number of an option and press Enter. Choose `5` to exit.

There is no extra configuration. The folders `data/` and `logs/` are created automatically on first run. Default rooms and limits can be changed in `hotel/config.py`.

## Testing

Run all unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

All 18 tests should pass. They cover validation, billing, booking, checkout, saving to file, recovery from a damaged data file, and confirm that a full Aadhaar number is never written to disk.

## Example Session

```
Enter your choice: 2
Select Room Type
1. Single  2. Double  3. Deluxe
...
======================================
          BOOKING SUCCESSFUL
======================================
Room Number : 104
Room Type   : Double
Breakfast   : With Breakfast
Guest Name  : Rahul Sharma
Phone       : 9876543210
Aadhaar     : XXXX-XXXX-9012
People      : 2
Days        : 3
Price/Day   : ₹3000
--------------------------------------
Total Bill  : ₹9000
======================================
```

Screenshots: add your own terminal screenshots in a `screenshots/` folder and link them here.

## Rooms and Prices

| Room | Type   | Breakfast         | Price per day |
|------|--------|-------------------|---------------|
| 101  | Single | Without Breakfast | ₹1500 |
| 102  | Single | With Breakfast    | ₹1800 |
| 103  | Double | Without Breakfast | ₹2500 |
| 104  | Double | With Breakfast    | ₹3000 |
| 105  | Deluxe | Without Breakfast | ₹4000 |
| 106  | Deluxe | With Breakfast    | ₹4500 |

## Troubleshooting

- **The ₹ sign looks wrong**: use a terminal that supports UTF-8 (Windows Terminal, VS Code terminal).
- **Data looks reset**: if `data/hotel_data.json` is damaged, the program logs the problem and starts with default rooms. Check `logs/hotel.log`.
- **To reset all data**: delete `data/hotel_data.json`.

## Limitations and Future Work

- Bookings have no calendar dates
- Single user, no login
- Possible additions: date-based reservations, guest search, GST in the bill, a web or GUI front end
