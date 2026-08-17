
/*!
Write a multi-threaded C++ program using std::thread and std::mutex to
sum a large array in parallel; profile it with perf .
*/

#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>
#include <numeric>

std::mutex mtx;
long long global_sum = 0;


/*
Set up visual studios 

Sum 4999989950000000
Time 2181 ms
Threads 12
*/

void sum_partial(const std::vector<int>& arr, int start, int end) {
    // assign (longlong 64bit      -9.22 x 10^18 to +9.22 x 10^18)
    long long local_sum = 0;
    for (int i = start; i < end; i++) {
        local_sum += arr[i];
    }
    // lock
    std::lock_guard<std::mutex> lock(mtx);
    // add to the global sum 
    global_sum += local_sum;
}

int main() {
    // define arr sicxe 
    const int SIZE = 100'000'000;
    // deifne number of threads -> hardware_concurrency will decice 
    unsigned int NUM_THREADS = std::thread::hardware_concurrency();
    if (NUM_THREADS == 0) NUM_THREADS = 4;

    std::vector<int> arr(SIZE);
    // https://en.cppreference.com/cpp/algorithm/iota 
    std::iota(arr.begin(), arr.end(), 0);

    // start the timer 
    auto start_time = std::chrono::high_resolution_clock::now();


    // create the thread      
    std::vector<std::thread> threads;
    // partirction the array for each of the threads
    int chunk = SIZE / NUM_THREADS;

    // THREAD CALLING LOGIC -> call threads to compute there part
    for (int i = 0; i < NUM_THREADS; i++) {
        // call each of the threads ---- need to learn how to do this
        int start = i * chunk;
        int end = (i == NUM_THREADS - 1) ? SIZE : start + chunk;
        threads.emplace_back(sum_partial, arr, start, end);
    }

    // what for threads to finnish computaion
    for (auto& t : threads) {
        // join 
        t.join();
    }

    // END TIME 
    auto end_time = std::chrono::high_resolution_clock::now();

    // CALCULAETE DURATION 
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);

    // OUPTUT
    std::cout << "Sum " << global_sum <<  std::endl;  
    std::cout << "Time " << duration.count() << " ms" << std::endl;
    std::cout << "Threads " << NUM_THREADS << std::endl;

    return 0;
}