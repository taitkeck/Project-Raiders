import sys
import httpx
from faker import Faker
from decouple import Config, RepositoryEnv

DOTENV_FILE = "./.env"
config = Config(RepositoryEnv(DOTENV_FILE))
API_KEY = config("API_KEY")


def make_products(amount):
    fake = Faker()
    for i in range(amount):
        data = {
            "name": " ".join(fake.words(nb=2, part_of_speech="noun")).title(),
            "description": fake.sentence(nb_words=5),
            "price": float(
                fake.pydecimal(
                    left_digits=fake.pyint(1, 2), right_digits=2, positive=True
                )
            ),
            "quantity": fake.pyint(1, 2),
            "tags": fake.words(nb=fake.pyint(2, 3), part_of_speech="noun"),
        }
        httpx.post(
            "http://localhost:8080/products",
            json=data,
            headers={
                "x-api-key": API_KEY,
            },
        )


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("USAGE: python products.py <amount: int>")
        sys.exit(1)
    amount = int(sys.argv[1])
    if amount <= 0 or amount > 200:
        print("Amount must be in the range [0, 200].")
        sys.exit(2)
    make_products(amount)
