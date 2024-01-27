import pandas as pd
from datetime import datetime


def read_data(file_path):
    """
    Читает данные из файла в формате CSV.

    Parameters:
    - file_path (str): Путь к файлу.

    Returns:
    - pd.DataFrame: Прочитанные данные в виде DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Ошибка чтения данных: {e}")
        return None


def validate_data(data):
    """
    Проводит проверки данных в таблице погашений заемщиков.

    Parameters:
    - data (pd.DataFrame): Данные для проверки.

    Returns:
    - list: Список ошибок.
    """
    errors = []

    data['Payment_Date'] = pd.to_datetime(data['Payment_Date'], errors='coerce')

    current_date = datetime.now().date()
    invalid_dates = data[data['Payment_Date'].dt.date < current_date]
    if not invalid_dates.empty:
        errors.append(f"Обнаружены погашения с датой в прошлом: {invalid_dates['Payment_Date'].tolist()}")

    invalid_amounts = data[data['Amount'] <= 0]
    if not invalid_amounts.empty:
        errors.append(f"Обнаружены платежи с некорректной суммой: {invalid_amounts['Amount'].tolist()}")

    if data.isnull().values.any():
        errors.append("Обнаружены пустые значения в таблице.")

    unique_loan_count = data['Loan_ID'].nunique()
    if unique_loan_count != len(data['Loan_ID']):
        errors.append("Один заемщик не может совершать несколько погашений.")

    return errors


def save_errors_to_csv(errors, output_file='errors.csv'):
    """
    Сохраняет ошибки в файл CSV.

    Parameters:
    - errors (list): Список ошибок.
    - output_file (str): Имя файла для сохранения ошибок.
    """
    error_data = pd.DataFrame({'Error': errors, 'Date': [datetime.now()] * len(errors)})
    error_data.to_csv(output_file, index=False)


if __name__ == "__main__":
    file_path = 'example.csv'

    data = read_data(file_path)

    if data is not None:
        errors = validate_data(data)
        save_errors_to_csv(errors)
