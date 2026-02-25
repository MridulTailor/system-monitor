#include "cpu_collector.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unistd.h>

// Read cumulative CPU usage from cgroup v2
long long readCgroupCPUUsage() {
    std::ifstream file("/sys/fs/cgroup/cpu.stat");
    if (!file.is_open()) {
        std::cerr << "Failed to open /sys/fs/cgroup/cpu.stat, falling back to 0" << std::endl;
        return 0;
    }
    
    std::string line;
    while (std::getline(file, line)) {
        if (line.find("usage_usec") == 0) {
            std::istringstream ss(line);
            std::string key;
            long long value;
            ss >> key >> value;
            return value;
        }
    }
    return 0;
}

double getCPUUsage() {
    long long usage1 = readCgroupCPUUsage();
    sleep(1);
    long long usage2 = readCgroupCPUUsage();
    
    // Delta is in microseconds over 1 second (1,000,000 microseconds)
    long long deltaUsage = usage2 - usage1;
    
    // CPU usage percentage: (microseconds used / microseconds in 1 second) * 100
    // On multi-core systems, this can exceed 100% (e.g., 200% = 2 full cores)
    double cpuPct = (deltaUsage / 1000000.0) * 100.0;
    return cpuPct;
}
