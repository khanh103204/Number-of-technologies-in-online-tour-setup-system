
import random
import faker

fake = faker.Faker("vi_VN")

NUM_USERS = 100       # số lượng user
NUM_TOURS = 500       # số lượng tour
NUM_BOOKINGS = 300    # số lượng booking
NUM_PAYMENTS = 300    # số lượng payment

types = ["biển", "leo núi", "cắm trại", "city tour", "quốc tế"]
difficulties = ["easy", "medium", "hard"]
methods = ["VNPay", "Momo", "Visa", "QR"]

# Mở file với encoding UTF-8
with open("travel_data.sql", "w", encoding="utf-8") as f:

    # 1. Users
    f.write("-- USERS\n")
    f.write("INSERT IGNORE INTO users (name, email, password, phone) VALUES\n")
    for i in range(1, NUM_USERS + 1):
        name = fake.name()
        email = f"user{i}@gmail.com"
        password = fake.password(length=8)
        phone = fake.phone_number()
        end = "," if i < NUM_USERS else ";"
        f.write(f"('{name}', '{email}', '{password}', '{phone}'){end}\n")

    # 2. Tours
    f.write("\n-- TOURS\n")
    f.write("INSERT IGNORE INTO tours (name, type, description, price, min_people, max_people, duration_days, difficulty, rating_avg, available) VALUES\n")
    for i in range(1, NUM_TOURS + 1):
        t_type = random.choice(types)
        name = f"Tour {t_type.capitalize()} {i}"
        desc = f"Trải nghiệm {t_type} thú vị số {i}"
        price = random.randint(1000000, 30000000)
        min_people = random.randint(1, 3)
        max_people = random.randint(10, 30)
        duration = random.randint(1, 7)
        difficulty = random.choice(difficulties)
        rating = round(random.uniform(3.5, 5.0), 1)
        available = "TRUE"
        end = "," if i < NUM_TOURS else ";"
        f.write(f"('{name}', '{t_type}', '{desc}', {price}, {min_people}, {max_people}, {duration}, '{difficulty}', {rating}, {available}){end}\n")

    # 3. Bookings
    f.write("\n-- BOOKINGS\n")
    f.write("INSERT IGNORE INTO bookings (user_id, tour_id, number_people, total_price, status) VALUES\n")
    for i in range(1, NUM_BOOKINGS + 1):
        user_id = random.randint(1, NUM_USERS)
        tour_id = random.randint(1, NUM_TOURS)
        number_people = random.randint(1, 10)
        base_price = random.randint(2000000, 10000000)
        total_price = base_price * number_people
        status = random.choice(["paid", "pending", "cancelled"])
        end = "," if i < NUM_BOOKINGS else ";"
        f.write(f"({user_id}, {tour_id}, {number_people}, {total_price}, '{status}'){end}\n")

    # 4. Payments
    f.write("\n-- PAYMENTS\n")
    f.write("INSERT IGNORE INTO payments (booking_id, amount, method, status, paid_at) VALUES\n")
    for i in range(1, NUM_PAYMENTS + 1):
        booking_id = i  # mapping 1-1 với booking
        amount = random.randint(2000000, 20000000)
        method = random.choice(methods)
        status = random.choice(["success", "pending", "failed"])
        paid_at = "NOW()" if status == "success" else "NULL"
        end = "," if i < NUM_PAYMENTS else ";"
        f.write(f"({booking_id}, {amount}, '{method}', '{status}', {paid_at}){end}\n")
