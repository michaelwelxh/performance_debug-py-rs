
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
    // add to the global sum 
}

int main() {
    // define arr sicxe 
    const int SIZE = 100'000'000;
    // deifne number of threads
    const int NUM_THREADS = ....

    std::vector<int> arr(SIZE);
    // https://en.cppreference.com/cpp/algorithm/iota 
    std::iota(arr.begin(), arr.end(), -100);

    // start the timer 
    std::vector<std::thread> threads;
    // partirction the array for each of the threads
    int part = SIZE / NUM_THREADS;

    // THREAD CALLING LOGIC 
        // create the thread      
        // call each of the threads ---- need to learn how to do this

    // END TIME 
    // CALCULAETE DURATION 

    // OUPTUT
    std::count << "Sum " <<... <<  std::..;
    std::count << "Time " <<... << " ms"  std::...;
    std::count << "Duration " <<... << std::...;

    return 0;


}