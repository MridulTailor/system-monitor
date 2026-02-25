#pragma once
#include <sqlite3.h>
void initDB(sqlite3* &db);
void logMetrics(sqlite3* db, double cpu, long memUsed, long memTotal, long rx, long tx);