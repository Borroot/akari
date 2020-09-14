# -----------------------------------------------------------------------------
# Files and directories
# -----------------------------------------------------------------------------

SRC_DIR       = src
INC_DIR       = inc
OBJ_DIR       = obj

BIN_SRC_FILES = $(wildcard $(SRC_DIR)/*.cpp)
BIN_INC_FILES = $(wildcard $(INC_DIR)/*.h)
BIN_OBJ_FILES = $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(BIN_SRC_FILES))

# -----------------------------------------------------------------------------
# Flags
# -----------------------------------------------------------------------------

EXTRAS        = -Wno-unused-parameter -Wno-unused-variable -Wno-unused-function
CFLAGS        = -Wall -Wextra -Werror -pedantic $(EXTRAS)
IFLAGS        = -I $(INC_DIR)

TARGETS       = akari

# -----------------------------------------------------------------------------
# Build rules
# -----------------------------------------------------------------------------

all: $(TARGETS)

akari: % : $(BIN_OBJ_FILES)
	@echo -e "LINK\t$@"
	@$(CXX) $(CFLAGS) $(IFLAGS) -o $@ $^

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp $(BIN_INC_FILES)
	@echo -e "CXX\t$@"
	@mkdir -p $(OBJ_DIR)
	@$(CXX) $(CFLAGS) $(IFLAGS) -c -o $@ $<

# -----------------------------------------------------------------------------
# Phonies
# -----------------------------------------------------------------------------

clean:
	rm -rf $(OBJ_DIR) $(TARGETS)

re:
	@$(MAKE) -s clean
	@$(MAKE) -s

.PHONY: all clean re
