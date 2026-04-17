import queue
import random
import threading
import time

NUM_TELLERS = 3
NUM_CUSTOMERS = 50

print_lock = threading.Lock()
ready_lock = threading.Lock()
bank_open = threading.Event()

ready_tellers = 0

waiting_customers = queue.Queue()
customer_waiting = threading.Semaphore(0)


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

        with ready_lock:
            log("Teller", self.teller_id, "ready to serve")
            ready_tellers += 1
            if ready_tellers == NUM_TELLERS:
                bank_open.set()

        while True:
            log("Teller", self.teller_id, "waiting for a customer")
            customer_waiting.acquire()
            customer = waiting_customers.get()

            if customer is None:
                log("Teller", self.teller_id, "leaving for the day")
                break

            customer.assigned_teller = self
            customer.teller_selected.release()

            customer.introduced_self.acquire()

            log(
                "Teller",
                self.teller_id,
                "serving a customer",
                "Customer",
                customer.customer_id,
            )
            log(
                "Teller",
                self.teller_id,
                "asks for transaction",
                "Customer",
                customer.customer_id,
            )

            customer.transaction_requested.release()
            customer.transaction_sent.acquire()

            log(
                "Teller",
                self.teller_id,
                f"handling {customer.transaction} transaction",
                "Customer",
                customer.customer_id,
            )

            customer.transaction_done.release()

            log(
                "Teller",
                self.teller_id,
                "wait for customer to leave.",
                "Customer",
                customer.customer_id,
            )
            customer.left_teller.acquire()


class Customer(threading.Thread):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id
        self.transaction = random.choice(["deposit", "withdrawal"])
        self.assigned_teller = None

        self.teller_selected = threading.Semaphore(0)
        self.introduced_self = threading.Semaphore(0)
        self.transaction_requested = threading.Semaphore(0)
        self.transaction_sent = threading.Semaphore(0)
        self.transaction_done = threading.Semaphore(0)
        self.left_teller = threading.Semaphore(0)

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

        waiting_customers.put(self)
        customer_waiting.release()

        self.teller_selected.acquire()
        teller = self.assigned_teller

        log("Customer", self.customer_id, "selecting a teller.")
        log(
            "Customer",
            self.customer_id,
            "selects teller",
            "Teller",
            teller.teller_id,
        )
        log(
            "Customer",
            self.customer_id,
            "introduces itself",
            "Teller",
            teller.teller_id,
        )

        self.introduced_self.release()

        self.transaction_requested.acquire()

        log(
            "Customer",
            self.customer_id,
            f"asks for {self.transaction} transaction",
            "Teller",
            teller.teller_id,
        )

        self.transaction_sent.release()
        self.transaction_done.acquire()

        log(
            "Customer",
            self.customer_id,
            "leaves teller",
            "Teller",
            teller.teller_id,
        )
        self.left_teller.release()

        log("Customer", self.customer_id, "goes to door")
        log("Customer", self.customer_id, "leaves the bank")


def main():
    tellers = [Teller(i) for i in range(NUM_TELLERS)]
    customers = [Customer(i) for i in range(NUM_CUSTOMERS)]

    for teller in tellers:
        teller.start()

    for customer in customers:
        customer.start()

    for customer in customers:
        customer.join()

    for _ in range(NUM_TELLERS):
        waiting_customers.put(None)
        customer_waiting.release()

    for teller in tellers:
        teller.join()


if __name__ == "__main__":
    main()