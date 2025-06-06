import os

data = 'base.txt'
sep = '|'
sep_2 = ';'

products = []

def product_string(product):
    name = product.get('Название', 'N/A')
    cost = str(product.get('Стоимость', 'N/A'))

    kbju_data = product.get('КБЖУ', {})
    kbju_parts = []
    for key in ['К', 'Б', 'Ж', 'У']:
        if key in kbju_data:
            kbju_parts.append(f"{key}:{kbju_data[key]}")
    kbju_str = sep.join(kbju_parts)

    return f"{name}{sep_2}{cost}{sep_2}{kbju_str}"

def string_product(product_string):
    parts = product_string.split(sep_2)
    if len(parts) != 3:
        return None

    name = parts[0]
    cost_str = parts[1]
    kbju_str = parts[2]

    try:
        cost = float(cost_str)
    except ValueError:
        cost = 'N/A'

    kbju = {}
    if kbju_str:
        kbju_pairs = kbju_str.split(sep)
        for pair in kbju_pairs:
            if ':' in pair:
                key, value_str = pair.split(':', 1)
                try:
                    kbju[key] = int(value_str)
                except ValueError:
                    pass

    return {
        'Название': name,
        'Стоимость': cost,
        'КБЖУ': kbju
    }

def save_data():
    try:
        with open(data, 'w', encoding='utf-8') as f:
            for product in products:
                f.write(product_string(product) + '\n')
        print(f"\nДанные успешно сохранены в '{data}'.")
    except IOError as e:
        print(f"\nОшибка сохранения данных: {e}")

def load_data():
    global products
    if os.path.exists(data):
        temp_collection = []
        try:
            with open(data, 'r', encoding='utf-8') as f:
                for line in f:
                    product = string_product(line.strip())
                    if product:
                        temp_collection.append(product)
            products = temp_collection
            print(f"Данные успешно загружены из '{data}'.")
        except IOError as e:
            print(f"Ошибка загрузки данных: {e}")
            products = []
    else:
        print("Файл данных не найден. Создана новая база данных продуктов.")
        products = []


def search(products, query):
    found_items = []
    norma_query = query.lower().strip()

    for product in products: # Changed products_collection to products
        if 'Название' in product and norma_query in product['Название'].lower():
            found_items.append(product)
            continue
    return found_items

def display(product):
    print("-" * 30)
    print(f"   Название: {product.get('Название', 'N/A')}")
    print(f"   Стоимость: {product.get('Стоимость', 'N/A')}")
    kbju_str = product.get('КБЖУ', {})
    print(f"   КБЖУ: К-{kbju_str.get('К', 'N/A')} Б-{kbju_str.get('Б', 'N/A')} Ж-{kbju_str.get('Ж', 'N/A')} У-{kbju_str.get('У', 'N/A')}")
    print("-" * 30)

def add():
    print("\n--- Добавление нового продукта ---")

    name = input("Введите Название продукта: ").strip()
    if not name:
        print("Название продукта не может быть пустым.")
        return

    for product in products:
        if product.get('Название', '').lower() == name.lower():
            print(f"Продукт с названием '{name}' уже существует.")
            return

    cost_str = input("Введите Стоимость продукта: ").strip()
    try:
        cost = float(cost_str)
        if cost < 0:
            print("Стоимость не может быть отрицательной.")
            return
    except ValueError:
        print("Некорректный формат стоимости. Продукт не добавлен.")
        return

    print("Введите КБЖУ (оставьте пустым, если неизвестно):")
    calories = input("   Калории (К): ").strip()
    proteins = input("   Белки (Б): ").strip()
    fats = input("   Жиры (Ж): ").strip()
    carbs = input("   Углеводы (У): ").strip()

    kbju = {}
    if calories.isdigit(): kbju['К'] = int(calories)
    if proteins.isdigit(): kbju['Б'] = int(proteins)
    if fats.isdigit(): kbju['Ж'] = int(fats)
    if carbs.isdigit(): kbju['У'] = int(carbs)


    new_product = {
        'Название': name,
        'Стоимость': cost,
        'КБЖУ': kbju
    }

    products.append(new_product)
    print(f"Продукт '{name}' успешно добавлен!")
    save_data()

def lists():
    print("\n--- Список продуктов ---")
    if not products:
        print("Список продуктов пуст.")
        return

    for product in products:
        display(product)

def delete():
    print("\n--- Удаление продукта ---")
    name_delete = input("Введите ТОЧНОЕ название продукта для удаления: ").strip()
    if not name_delete:
        print("Название для удаления не может быть пустым.")
        return

    found_index = -1
    for i, product in enumerate(products):
        if product.get('Название', '').lower() == name_delete.lower():
            found_index = i
            break

    if found_index != -1:
        product_delete = products[found_index]
        print(f"Найден продукт для удаления:")
        display(product_delete) # Changed display_product to display
        confirm = input("Вы уверены, что хотите удалить этот продукт? (да/нет): ").strip().lower()
        if confirm == 'да':
            del products[found_index]
            print(f"Продукт '{name_delete}' успешно удален.")
            save_data()
        else:
            print("Удаление отменено.")
    else:
        print(f"Продукт с названием '{name_delete}' не найден.")

def main():
    print("Добро пожаловать в Каталогизатор продуктов!")
    load_data()

    while True:
        print("\n--- ГЛАВНОЕ МЕНЮ ---")
        print("1. Добавить продукт")
        print("2. Список продуктов")
        print("3. Удалить продукт")
        print("4. Выйти из программы")

        choice = input("Выберите действие (1-4): ").strip()

        if choice == '1':
            add()
        elif choice == '2':
            lists()
        elif choice == '3':
            delete()
        elif choice == '4':
            print("Спасибо за использование Каталогизатора продуктов. До свидания!")
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите число от 1 до 4.")
main()