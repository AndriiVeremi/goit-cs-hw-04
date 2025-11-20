import os
import time
from threading import Thread, Lock
from multiprocessing import Process, Queue


def search_in_file(file_path, keywords):
    """
    Шукає ключові слова в одному файлі.

    """
    found_keywords = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    if keyword not in found_keywords:
                        found_keywords[keyword] = []
                    found_keywords[keyword].append(file_path)
    except IOError as e:
        print(f"Помилка читання файлу {file_path}: {e}")
    return found_keywords

# Багатопотокова версія 

thread_results = {}

lock = Lock()

def thread_worker(files_chunk, keywords):
    """
    Він обробляє свою частину файлів.

    """
    local_results = {}
    
    for file in files_chunk:
        found = search_in_file(file, keywords)
        for keyword, file_paths in found.items():
            if keyword not in local_results:
                local_results[keyword] = []
            local_results[keyword].extend(file_paths)

    with lock:
        for keyword, file_paths in local_results.items():
            if keyword not in thread_results:
                thread_results[keyword] = []
            thread_results[keyword].extend(file_paths)

def run_threaded_search(all_files, keywords):
    """
    Запускає пошук з використанням потоків.
    """
    start_time = time.time()
    threads = []
    num_threads = 4  
    chunk_size = len(all_files) // num_threads
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(all_files)
        files_chunk = all_files[start:end]       
        thread = Thread(target=thread_worker, args=(files_chunk, keywords))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    execution_time = time.time() - start_time
    print(f"Багатопотоковий пошук зайняв: {execution_time:.4f} секунд")
    return thread_results

# Багатопроцесорна версія 

def process_worker(files_chunk, keywords, output_queue):
    """
    Результати своєї роботи він кладе у чергу.

    """
    process_results = {}
    for file in files_chunk:
        found = search_in_file(file, keywords)
        for keyword, file_paths in found.items():
            if keyword not in process_results:
                process_results[keyword] = []
            process_results[keyword].extend(file_paths)            
    output_queue.put(process_results)

def run_multiprocess_search(all_files, keywords):
    """
    Запускає пошук з використанням процесів.

    """
    start_time = time.time()

    output_queue = Queue()
    processes = []
    num_processes = 4 

    chunk_size = len(all_files) // num_processes
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(all_files)
        files_chunk = all_files[start:end]

        process = Process(target=process_worker, args=(files_chunk, keywords, output_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_results = {}
    while not output_queue.empty():
        result = output_queue.get()
        for keyword, file_paths in result.items():
            if keyword not in final_results:
                final_results[keyword] = []
            final_results[keyword].extend(file_paths)

    execution_time = time.time() - start_time
    print(f"Багатопроцесорний пошук зайняв: {execution_time:.4f} секунд.")
    return final_results


def main():
    file_dir = "text_files"
    if not os.path.isdir(file_dir):
        print(f"Помилка: Директорія '{file_dir}' не знайдена. Завершення роботи.")
        return
    
    files_to_search = [os.path.join(file_dir, f) for f in os.listdir(file_dir) if f.endswith('.txt')]  
    keywords_to_find = ["калина", "доля", "сонці", "небо"]

    print("--- Запуск багатопотокового пошуку ---")
    threaded_res = run_threaded_search(files_to_search, keywords_to_find)
    print("Результати (багатопотоковий):")

    for keyword in sorted(threaded_res.keys()):
        print(f"  '{keyword}': {sorted(threaded_res[keyword])}")
    print("-" * 30)

    print("\n--- Запуск багатопроцесорного пошуку ---")
    multiprocess_res = run_multiprocess_search(files_to_search, keywords_to_find)
    print("Результати (багатопроцесорний):")

    for keyword in sorted(multiprocess_res.keys()):
        print(f"  '{keyword}': {sorted(multiprocess_res[keyword])}")
    print("-" * 30)

if __name__ == "__main__":
    main()