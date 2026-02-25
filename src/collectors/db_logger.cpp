#include "db_logger.h"
#include <sqlite3.h>
#include <string>
#include <ctime>

void initDB(sqlite3* &db) {
    sqlite3_open("/app/metrics.db", &db);
    const char* sql = "CREATE TABLE IF NOT EXISTS metrics ("
                      "timestamp INTEGER,"
                      "cpu_pct REAL,"
                      "mem_used_mb INTEGER,"
                      "mem_total_mb INTEGER,"
                      "rx_kb INTEGER,"
                      "tx_kb INTEGER);";
    sqlite3_exec(db, sql, nullptr, nullptr, nullptr);
}

void logMetrics(sqlite3* db, double cpu, long memUsed, long memTotal, long rx, long tx) {
    std::string sql = "INSERT INTO metrics VALUES (" +
        std::to_string(time(nullptr)) + "," +
        std::to_string(cpu) + "," +
        std::to_string(memUsed/1024) + "," +
        std::to_string(memTotal/1024) + "," +
        std::to_string(rx/1024) + "," +
        std::to_string(tx/1024) + ");";
    sqlite3_exec(db, sql.c_str(), nullptr, nullptr, nullptr);
}