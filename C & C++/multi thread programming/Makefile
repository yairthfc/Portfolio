CC=g++
CXX=g++ 
RANLIB=ranlib 
LIBSRC=MapReduceFramework.cpp
LIBHEADER = MapReduceFramework.h MapReduceClient.h
LIBOBJ=$(LIBSRC:.cpp=.o) 
INCS=-I. 
CFLAGS = -Wall -std=c++11 -g $(INCS) 
CXXFLAGS = -Wall -std=c++11 -g $(INCS) 
OSMLIB = libMapReduceFramework.a
TARGETS = $(OSMLIB) 
TAR=tar 
TARFLAGS=-cvf 
TARNAME=ex3.tar
TARSRCS=$(LIBSRC) $(LIBHEADER) Makefile README
all: $(TARGETS)
$(TARGETS): $(LIBOBJ) 
	$(AR) $(ARFLAGS) $@ $^ 
	$(RANLIB) $@ 
clean: 
	$(RM) $(TARGETS) $(OSMLIB) $(OBJ) $(LIBOBJ) *~ *core 
tar: 
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)

