# CS4348 Project 2

Thread-based bank simulation in Python using the threading module and semaphores.

## Current progress

Implemented so far:
- creates teller threads
- creates customer threads
- opens the bank only after all tellers are ready
- places customers into a shared line
- assigns waiting customers to available tellers
- synchronizes basic teller-customer interaction

## Run

```bash
python bank.py