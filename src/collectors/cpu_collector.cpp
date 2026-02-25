#include "cpu_collector.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unistd.h>

struct CPUStats {
    long user, nice, system, idle, iowait, irq, softirq;
};

CPUStats readCPUStats() {
    std::ifstream file("/proc/stat");
    std::string line;
    std::getline(file, line);

    CPUStats stats;
    std::string cpu;
    std::istringstream ss(line);
    ss >> cpu >> stats.user >> stats.nice >> stats.system >> stats.idle >> stats.iowait >> stats.irq >> stats.softirq;
    return stats;
}

double getCPUUsage() {
    CPUStats s1 = readCPUStats();
    sleep(1);
    CPUStats s2 = readCPUStats();

    long idle1 = s1.idle + s1.iowait;
    long idle2 = s2.idle + s2.iowait;
    long total1 = s1.user + s1.nice + s1.system + idle1 + s1.irq + s1.softirq;
    long total2 = s2.user + s2.nice + s2.system + idle2 + s2.irq + s2.softirq;

    long totalDiff = total2 - total1;
    long idleDiff = idle2 - idle1;
    return (totalDiff - idleDiff) / totalDiff * 100.0;
}
