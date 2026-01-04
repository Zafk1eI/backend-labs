from enum import Enum
from abc import ABC, abstractmethod


class PackingType(Enum):
    BAG = "пакет"
    CAN = "банка"
    VACUUM = "вакуумная упаковка"


class CoffeeType(Enum):
    BEAN = "зерно"
    GROUND = "молотый"
    INSTANT = "растворимый"


class OverflowCustomExc(Exception):
    ...


class Coffee(ABC):
    def __init__(
        self,
        name: str,
        quality: int,
        price: float,
        weight: float,
        packing: PackingType,
        coffee_type: CoffeeType,
    ):
        self.name = name
        self.price = price
        self.weight = weight
        self.packing = packing
        self.coffee_type = coffee_type
        self.quality = quality

    def get_price_per_weight(self) -> float:
        return self.price / self.weight if self.weight > 0 else 0

    @abstractmethod
    def get_packing_coefficient(self):
        raise NotImplementedError

    def calculate_volume(self) -> float:
        return self.weight * self.get_packing_coefficient()

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.coffee_type.value}), "
            f"Упаковка: {self.packing.value}, "
            f"Вес: {self.weight} г, "
            f"Цена: {self.price} руб, "
            f"Качество: {self.quality}/5, "
            f"Объем: {self.calculate_volume():.2f} мл, "
            f"Цена/вес: {self.get_price_per_weight():.2f} руб/г"
        )


class BeanCoffee(Coffee):
    BEAN_PACKING_COEFFICIENTS = {
        PackingType.BAG: 1.5,
        PackingType.CAN: 2.2,
        PackingType.VACUUM: 0.9,
    }

    def __init__(
        self, name: str, quality: int, price: float, weight: float, packing: PackingType
    ):
        super().__init__(name, quality, price, weight, packing, CoffeeType.BEAN)

    def get_packing_coefficient(self) -> float:
        return self.BEAN_PACKING_COEFFICIENTS[self.packing]


class InstantCoffee(Coffee):
    INSTANT_PACKING_COEFFICIENTS = {
        PackingType.BAG: 1.2,
        PackingType.CAN: 1.8,
        PackingType.VACUUM: 0.7,
    }

    def __init__(
        self, name: str, quality: int, price: float, weight: float, packing: PackingType
    ):
        super().__init__(name, quality, price, weight, packing, CoffeeType.INSTANT)

    def get_packing_coefficient(self) -> float:
        return self.INSTANT_PACKING_COEFFICIENTS[self.packing]


class GroundCoffee(Coffee):
    GROUND_PACKING_COEFFICIENTS = {
        PackingType.BAG: 1.3,
        PackingType.CAN: 2.0,
        PackingType.VACUUM: 0.8,
    }

    def __init__(
        self, name: str, quality: int, price: float, weight: float, packing: PackingType
    ):
        super().__init__(name, quality, price, weight, packing, CoffeeType.GROUND)

    def get_packing_coefficient(self) -> float:
        return self.GROUND_PACKING_COEFFICIENTS[self.packing]


class CoffeeTruck:
    def __init__(self, max_volume: float, max_cost: float):
        self.max_cost = max_cost
        self.max_volume = max_volume
        self.current_volume = 0
        self.current_cost = 0
        self._product_list: list[Coffee] = []

    def append_coffee(self, coffee: Coffee):
        new_volume = self.current_volume + coffee.calculate_volume()
        new_cost = self.current_cost + coffee.price

        if new_volume > self.max_volume:
            raise OverflowCustomExc("Превышен максимальный объем")
        if new_cost > self.max_cost:
            raise OverflowCustomExc("Превышена максимальная стоимость")

        self.current_volume = new_volume
        self.current_cost = new_cost
        self._product_list.append(coffee)

    def sorting_coffee_list(self):
        self._product_list = sorted(
            self._product_list,
            key=lambda x: x.price / x.calculate_volume(),
        )

    def append_coffee_list(self, coffee: list[Coffee]):
        sorted_coffees = sorted(coffees, key=lambda x: x.price, reverse=True)

        for coffee in sorted_coffees:
            try:
                self.append_coffee(coffee)
                print(f"Успешно добавлено: {coffee.name}")
            except OverflowCustomExc as e:
                print(f"Не удалось добавить {coffee.name}: {e}")

    def search(self, min_quality: int = 0, max_quality: int = 5) -> list[Coffee]:
        result: list[Coffee] = []
        for coffee in self._product_list:
            if min_quality <= coffee.quality <= max_quality:
                result.append(coffee)
        if not result:
            print("Кофе не найден")
        return result

if __name__ == "__main__":
    truck = CoffeeTruck(5000, 10000)

    coffees = [
        BeanCoffee("Arabica Premium", 5, 5000, 1000, PackingType.BAG),
        GroundCoffee("Robusta Classic", 4, 3000, 500, PackingType.VACUUM),
        InstantCoffee("Nescafe Gold", 3, 2000, 250, PackingType.CAN),
        GroundCoffee("Lavazza Qualita", 5, 4000, 750, PackingType.BAG),
        BeanCoffee("Ethiopian Yirg", 5, 6000, 1200, PackingType.VACUUM),
    ]

    optimized_list = truck.append_coffee_list(coffees)
    truck.sorting_coffee_list()
    optimized_list = truck._product_list
    result = truck.search(3, 5)
    for item in result:
        print(item)