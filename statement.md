# Problem Statement

## Problem
Small hotels and guest houses often track rooms, guests and bills on paper or in scattered notes. This causes double bookings, calculation mistakes in bills, lost guest records and careless handling of sensitive identity numbers such as Aadhaar. Staff need a simple tool that works on any computer without a special setup.

## Project
**Hotel Management System** is a command-line application written in Python. It lets a receptionist see which rooms are free, book a room for a guest, check the guest out with a correct bill, and view who is currently staying. Data is saved to a file so it is not lost when the program closes.

## Scope

**Included**
- A fixed set of six rooms (Single, Double, Deluxe, each with and without breakfast)
- Room availability listing and matching by room type and breakfast option
- Booking with guest details: name, phone, Aadhaar, number of people, number of days
- Input validation (1 to 3 people, 1 to 30 days, 10-digit phone, 12-digit Aadhaar)
- Bill calculation (price per day x days) and printed receipts
- Checkout, which frees the room
- Current guest report
- Saving data to a JSON file, and a log file of actions and errors
- Automated unit tests

**Not included**
- Graphical or web interface
- Booking by calendar date or advance reservations
- Online payments
- Multiple users or logins

## Target Users
- Hotel or guest-house receptionists who need a quick booking tool
- Students learning how a real Python program is organised into modules, tests and documentation

## High-Level Features
1. **Room inventory and availability**: view free rooms and find a match for the guest's choice
2. **Booking and guest management**: validated guest details, Aadhaar masking, room status update
3. **Billing and checkout**: automatic total, receipts at booking and checkout
4. **Guest report**: list of all rooms currently occupied
5. **Persistence and logging**: JSON storage, safe saving, and a log file for troubleshooting
6. **Error handling**: clear messages for wrong input, no crashes on bad numbers, recovery from a damaged data file
