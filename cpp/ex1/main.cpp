
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


/*
need to learn chrono, mutex and thread -> the rest is simple enough to guess through logic i think will be similar to last java concurreny project -> call thread lock and run join not sure on the syntax though

*/


std::mutex mtx;
long long global_sum = 0;


void sum_partial(const std::vector<int>& arr, int start, int end) {
    // assign (longlong 64bit      -9.22 x 10^18 to +9.22 x 10^18)
    long long local_sum = 0;
    for (int i = start; i < end; i++) {
        local_sum += arr[i];
    }
    // lock
    std::lock_guard<std::mutex> lock(mtx);
    // add to the global sum 
    global_sum += global_sum
}

int main() {
    // define arr sicxe 
    const int SIZE = 100'000'000;
    // deifne number of threads -> hardware_concurrency will decice 
    const int NUM_THREADS = std::thread::hardware_concurrency();

    std::vector<int> arr(SIZE);
    // https://en.cppreference.com/cpp/algorithm/iota 
    std::iota(arr.begin(), arr.end(), -100);

    // start the timer 
    auto start_time = std::chrono::high_resolution_clock::now()


    // create the thread      
    std::vector<std::thread> threads;
    // partirction the array for each of the threads
    int part = SIZE / NUM_THREADS;

    // THREAD CALLING LOGIC -> call threads to compute there part
    for (int i = 0; i < NUM_THREADS; i++) {
        // call each of the threads ---- need to learn how to do this
        int start = i * chunk;
        int end = (i == NUM_THREADS - 1) ? SIZE : start + chunk;
        threads.emplace_back(sum_partial, std::ref(arr), start, end);
    }

    // what for threads to finnish computaion
    for (&auto t : threads) {
        // join 
        t.join()
    }

    // END TIME 
    auto end_time = std::chrono::high_resolution_clock::now()

    // CALCULAETE DURATION 
    auto dureation = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);

    // OUPTUT
    std::count << "Sum " << global_sum <<  std::endl;  
    std::count << "Time " << duration.count() << " ms"  std::endl;
    std::count << "Threads " << NUM_THREADS << std::endl;

    return 0;
}