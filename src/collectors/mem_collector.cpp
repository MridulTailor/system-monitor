#include "mem_collector.h"
#include <fstream>
#include <string>
#include <map>
#include <sstream>

std::map<std::string, long> getMemStats() {
    std::ifstream file("/proc/meminfo");
    std::map<std::string, long> memStats;
    std::string line;

    while(std::getline(file, line)) {
        std::istringstream ss(line);
        std::string key;
        long value;
        ss >> key >> value;
        key.pop_back(); //remove the trailing ':'
        memStats[key] = value;
    }
    return memStats;
}