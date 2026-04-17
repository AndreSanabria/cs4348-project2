# CS4348 Project 2

Thread-based bank simulation in Python using `threading` and semaphores.

## Requirements

- Python 3.8+

## Run

```bash
python bank.py
```

## Implemented Behavior

- Starts 3 teller threads and 50 customer threads.
- Opens the bank only after all tellers report ready.
- Customers choose deposit/withdrawal at random and wait 0-100 ms before arriving.
- Enforces a shared bank door with capacity 2 for entering/leaving.
- Places customers in a shared line and synchronizes teller selection/servicing.
- Requires manager access for withdrawals (1 teller at a time, 5-30 ms interaction).
- Enforces safe access with capacity 2 tellers (10-50 ms transaction work).
- Ensures customers leave tellers only after transaction completion.
- Shuts down tellers after all customers are served and prints final bank-close message.
