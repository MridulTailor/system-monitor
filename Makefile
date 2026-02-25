CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
TARGET = monitor
SRCS = src/main.cpp \
       src/collectors/cpu_collector.cpp \
       src/collectors/mem_collector.cpp \
       src/collectors/net_collector.cpp \
	   src/collectors/db_logger.cpp

all:
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET) -lsqlite3

clean:
	rm -f $(TARGET)