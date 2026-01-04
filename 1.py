from dataclasses import dataclass
from enum import Enum
from random import randint, choice

class Diagnosis(Enum):
    HYPERTENSION = "Артериальная гипертензия"
    DIABETES_TYPE_2 = "Сахарный диабет 2 типа"
    CORONARY_HEART_DISEASE = "Ишемическая болезнь сердца"
    BRONCHIAL_ASTHMA = "Бронхиальная астма"
    GASTRITIS = "Хронический гастрит"
    OSTEOARTHRITIS = "Остеоартроз"
    DEPRESSION = "Депрессивное расстройство"
    HYPOTHYROIDISM = "Гипотиреоз"
    CHRONIC_BRONCHITIS = "Хронический бронхит"
    ANEMIA = "Анемия"

@dataclass(repr=True)
class  Patient:
    id: int
    last_name: str
    first_name: str
    middle_name: str
    address: str
    numbers: str
    id_med_card: int
    diagnosis: Diagnosis

def filter_diagnosis(list_patient: list[Patient], diagnosis: Diagnosis) -> list[Patient]:
    filtered_patient = []
    for patient in list_patient:
        if patient.diagnosis == diagnosis:
            filtered_patient.append(patient)
    
    return filtered_patient
            
def filtered_by_med_card(patients: list[Patient], start_interval: int, end_interval: int) -> list[Patient]:
    filtered_patient_by_med_card = []
    for patient in patients:
        if start_interval < patient.id_med_card < end_interval:
            filtered_patient_by_med_card.append(patient)

    return filtered_patient_by_med_card

def generate_patients() -> list[Patient]:
    last_names = ["Иванов", "Петров", "Смирнов", "Кузнецов", "Попов", "Соколов", "Михайлов", "Федоров", "Морозов", "Волков"]
    first_names = ["Иван", "Петр", "Алексей", "Дмитрий", "Сергей", "Андрей", "Николай", "Михаил", "Виктор", "Александр"]
    middle_names = ["Иванович", "Петрович", "Сергеевич", "Андреевич", "Николаевич", "Михайлович", "Дмитриевич", "Алексеевич", "Викторович", "Федорович"]
    
    patients = []
    for i in range(10):
        patient = Patient(
            id=i+1,
            last_name=last_names[i],
            first_name=first_names[i],
            middle_name=middle_names[i],
            address=f"ул. Центральная, д. {randint(1, 100)}, кв. {randint(1, 50)}",
            numbers=f"+7 ({randint(900, 999)}) {randint(100, 999)}-{randint(10, 99)}-{randint(10, 99)}",
            id_med_card=randint(10000, 99999),
            diagnosis=choice(list(Diagnosis))
        )
        patients.append(patient)

    return patients

def main():
    patients = generate_patients()
    for patient in patients:
        print(patient)
    print("По диагнозу:")
    filtered_by_diagnos_list = filter_diagnosis(patients, diagnosis=Diagnosis.DEPRESSION)
    for patient in filtered_by_diagnos_list:
        print(patient)

    filtered_by_med_card_list = filtered_by_med_card(patients, 10000, 60000)
    print("По картам:")
    for patient in filtered_by_med_card_list:
        print(patient)



if __name__ == "__main__":
    main()