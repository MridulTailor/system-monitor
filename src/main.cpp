#include <iostream>
#include <unistd.h>
#include <csignal>
#include "collectors/cpu_collector.h"
#include "collectors/mem_collector.h"
#include "collectors/net_collector.h"
#include "collectors/db_logger.h"

// ---- Signal Handling ----
volatile sig_atomic_t running = 1;
void handleSignal(int) {
    std::cout << "\nShutting down monitor...\n";
    running = 0;
}

// ---- Main Loop ----
int main() {
    signal(SIGINT, handleSignal);
    signal(SIGTERM, handleSignal);
    sqlite3* db;
    initDB(db);


    std::cout << "System Monitor Started. Press Ctrl+C to stop.\n";
    std::cout << "==========================================\n";

    while (running) {
        double cpu = getCPUUsage();
        auto mem = getMemStats();
        auto net = getNetStats();

        long totalMem = mem["MemTotal"];
        long freeMem  = mem["MemAvailable"];
        long usedMem  = totalMem - freeMem;
        double memPct = (double)usedMem / totalMem * 100.0;

        std::cout << "[CPU]  Usage: " << cpu << "%\n";
        std::cout << "[MEM]  Used: " << usedMem/1024 << " MB / "
                  << totalMem/1024 << " MB (" << memPct << "%)\n";
        std::cout << "[NET]  RX: " << net.rxBytes/1024 << " KB  TX: " 
          << net.txBytes/1024 << " KB\n";
        std::cout << "------------------------------------------\n";
        
        logMetrics(db, cpu, usedMem, totalMem, net.rxBytes, net.txBytes);
        sleep(2);
    }
    sqlite3_close(db);
    return 0;
}
