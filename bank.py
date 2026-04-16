import random
import threading
import time

NUM_TELLERS = 3
NUM_CUSTOMERS = 50

print_lock = threading.Lock()
ready_lock = threading.Lock()
bank_open = threading.Event()

ready_tellers = 0


def log(thread_type, thread_id, message, partner_type=None, partner_id=None):
    with print_lock:
        if partner_type is None or partner_id is None:
            print(f"{thread_type} {thread_id} []: {message}")
        else:
            print(f"{thread_type} {thread_id} [{partner_type} {partner_id}]: {message}")


class Teller(threading.Thread):
    def __init__(self, teller_id):
        super().__init__()
        self.teller_id = teller_id

    def run(self):
        global ready_tellers

        log("Teller", self.teller_id, "ready to serve")

        with ready_lock:
            ready_tellers += 1
            if ready_tellers == NUM_TELLERS:
                bank_open.set()

        log("Teller", self.teller_id, "waiting for a customer")


class Customer(threading.Thread):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id
        self.transaction = random.choice(["deposit", "withdrawal"])

    def run(self):
        log(
            "Customer",
            self.customer_id,
            f"wants to perform a {self.transaction} transaction",
        )

        time.sleep(random.uniform(0, 0.1))

        bank_open.wait()

        log("Customer", self.customer_id, "going to bank.")
        log("Customer", self.customer_id, "entering bank.")
        log("Customer", self.customer_id, "getting in line.")


def main():
    tellers = [Teller(i) for i in range(NUM_TELLERS)]
    customers = [Customer(i) for i in range(NUM_CUSTOMERS)]

    for teller in tellers:
        teller.start()

    for customer in customers:
        customer.start()

    for teller in tellers:
        teller.join()

    for customer in customers:
        customer.join()


if __name__ == "__main__":
    main()