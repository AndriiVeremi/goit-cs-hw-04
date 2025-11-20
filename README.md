# GoIT Computer Science Homework 04

# Parallel Text File Processing

## Task Description

This program is designed for parallel processing and analysis of text files to search for specific keywords. Two versions of the program are implemented:
1.  **Multi-threaded version** using the `threading` module.
2.  **Multi-processing version** using the `multiprocessing` module.

Both versions distribute the list of files among threads/processes, search for specified keywords in their respective sets of files, and collect the search results. The program measures and outputs the execution time for each version. The result of the work is a dictionary where the key is the search word and the value is a list of file paths where that word was found.

## How to Run the Program

To run the program, follow these steps:

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd goit-cs-hw-04
    ```

2.  **Create test files:**
    The program expects text files to be present in the `text_files` directory. If this directory does not exist or is empty, the program may not find files to process.
    You can create test files using the following commands:
    ```bash
    mkdir text_files
    echo "Сонце гріє, вітер віє
З поля на долину,
Над водою гне з вербою
Червону калину,
На калині одиноке
Гніздечко гойдає.
А де ж дівся соловейко?
Не питай, не знає." > text_files/file_1.txt
    echo "Ще не вмерла Україна, і слава, і воля,
Ще нам, браття молодії, усміхнеться доля.
Згинуть наші вороженьки, як роса на сонці,
Запануєм і ми, браття, у своїй сторонці." > text_files/file_2.txt
    ```
    *Note: Make sure the files contain the keywords you want to search for, otherwise the search results may be empty.*

3.  **Run the main script:**
    ```bash
    python3 main.py
    ```

The program will output the search results for the multi-threaded and multi-processing versions, as well as the execution time for each.

## Example Output

```
--- Запуск багатопотокового пошуку ---
Багатопотоковий пошук зайняв: 0.0012 секунд
Результати (багатопотоковий):
  'доля': ['text_files/file_2.txt']
  'сонці': ['text_files/file_2.txt']
------------------------------

--- Запуск багатопроцесорного пошуку ---
Багатопроцесорний пошук зайняв: 0.0231 секунд.
Результати (багатопроцесорний):
  'доля': ['text_files/file_2.txt']
  'сонці': ['text_files/file_2.txt']
------------------------------
```
*(Example output may vary depending on file content and keywords)*