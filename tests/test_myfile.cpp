#include <gtest/gtest.h>
#include "myfile.h"

// Simple tests for add() function
TEST(AddTest, PositiveNumbers) {
    EXPECT_EQ(add(2, 3), 5);
}

TEST(AddTest, NegativeNumbers) {
    EXPECT_EQ(add(-2, -3), -5);
}

TEST(AddTest, MixedSignNumbers) {
    EXPECT_EQ(add(-5, 10), 5);
}

// Tests for divide() function
TEST(DivideTest, NormalDivision) {
    EXPECT_EQ(divide(10, 2), 5);
}

TEST(DivideTest, FractionResult) {
    EXPECT_EQ(divide(5, 2), 2);
}

TEST(DivideTest, DivisionByZero) {
    EXPECT_THROW(divide(5, 0), std::invalid_argument);
}

TEST(DivideTest, LargeNumbers) {
    EXPECT_EQ(divide(1000, 100), 10);
}

// Entry point for tests
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}