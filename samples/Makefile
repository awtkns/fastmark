# A Makefile for using Google Test and building a unit test program against it.
# CPSC 2150 by Gladys Monagan
# January 10, 2021
# based on the Google Test distribution sample Makefiles

# Where to find user code.
USER_DIR = .

VERSION = -std=c++17
CXX = g++

# Flags passed to the preprocessor.
# We have no idea here whether pthreads is available in the system, so disable its use.
# Set Google Test's header directory as a system directory, such that
# the compiler doesn't generate warnings in Google Test headers.
CPPFLAGS = -I$(GTEST_DIR)/include -DGTEST_HAS_PTHREAD=0

# Flags passed to the C++ compiler.
CXXFLAGS = $(CPPFLAGS) -pedantic -Wall -Wextra $(VERSION)

#DEBUG = -g
LFLAGS = $(DEBUG) $(VERSION)

# Where to find gtest_main.cc.
GTEST_MAIN_CC = $(GTEST_DIR)/gtest_main.cc

# All Google Test headers.  Usually you shouldn't change this
# definition.
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h \
                $(GTEST_DIR)/include/gtest/internal/*.h

SRC = lfcts

# a main program that runs with the Google Tests
STUDENT_UNITTEST = lfcts_unittest
SOLUTION_UNITTEST = solution_unittest

# House-keeping build targets.
all : $(STUDENT_UNITTEST) $(SOLUTION_UNITTEST)

# Usually you shouldn't tweak such internal variables, indicated by a
# trailing _.
GTEST_SRCS_ = $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)

# For simplicity and to avoid depending on Google Test's
# implementation details, the dependencies specified below are
# conservative and not optimized.  This is fine as Google Test
# compiles fast and for ordinary users its source rarely changes.
gtest-all.o : $(GTEST_SRCS_)
	$(CXX) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest-all.cc

gtest_main.o : $(GTEST_SRCS_)
	$(CXX) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest_main.cc

$(SRC).o : $(USER_DIR)/$(SRC).cpp $(USER_DIR)/$(SRC).h
	$(CXX) $(CXXFLAGS) -c $(USER_DIR)/$(SRC).cpp

$(STUDENT_UNITTEST).o : $(USER_DIR)/$(STUDENT_UNITTEST).cpp  \
                  $(USER_DIR)/$(SRC).h \
                  $(GTEST_HEADERS)
	$(CXX) $(CXXFLAGS) -c $(USER_DIR)/$(STUDENT_UNITTEST).cpp

$(STUDENT_UNITTEST) : $(SRC).o $(STUDENT_UNITTEST).o gtest-all.o gtest_main.o
	$(CXX) $(LFLAGS) $(CXXFLAGS) $^ -o $@

$(SOLUTION_UNITTEST).o : $(USER_DIR)/$(SOLUTION_UNITTEST).cpp  \
                  $(USER_DIR)/$(SRC).h \
                  $(GTEST_HEADERS)
	$(CXX) $(CXXFLAGS) -c $(USER_DIR)/$(SOLUTION_UNITTEST).cpp

$(SOLUTION_UNITTEST) : $(SRC).o $(SOLUTION_UNITTEST).o gtest-all.o gtest_main.o
	$(CXX) $(LFLAGS) $(CXXFLAGS) $^ -o $@