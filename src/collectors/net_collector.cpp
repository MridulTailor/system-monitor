#include "net_collector.h"
#include <fstream>
#include <string>
#include <sstream>
NetStats getNetStats() {
    std::ifstream file("/proc/net/dev");
    std::string line;
    NetStats total = {0, 0};
    std::getline(file, line); // skip header 1
    std::getline(file, line); // skip header 2
    while (std::getline(file, line)) {
        std::istringstream ss(line);
        std::string iface;
        long rx, tx;
        ss >> iface >> rx;
        for (int i = 0; i < 7; i++) ss >> tx; // skip to tx bytes
        ss >> tx;
        if (iface != "lo:") { // skip loopback
            total.rxBytes += rx;
            total.txBytes += tx;
        }
    }
    return total;
}