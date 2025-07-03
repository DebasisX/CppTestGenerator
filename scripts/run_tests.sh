#!/bin/bash

# Build and run tests
set -e

TEST_FILE=$1
TEST_NAME=$(basename $TEST_FILE .cpp)

# Compile with coverage
g++ -std=c++17 -fprofile-arcs -ftest-coverage -I src/ \
    src/myfile.cpp $TEST_FILE -lgtest -lgtest_main -lpthread -o $TEST_NAME

# Run tests
./$TEST_NAME

# Generate coverage
gcov -r -s src/ $TEST_NAME > coverage.txt