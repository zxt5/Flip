#!/usr/bin/env bash

SCRIPT_PATH="$(realpath "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd -P)"
PROJECT_BIN_DIR="$ROOT_DIR/bin"
THIRD_PARTY_DIR="$ROOT_DIR/third_party"
source "$SCRIPT_DIR/utils.sh"

info "project root: $ROOT_DIR"
info "third_party:  $THIRD_PARTY_DIR"

SCIP_BUILD_SCRIPT="$SCRIPT_DIR/build_scip_trunk.sh"
CBC_BUILD_SCRIPT="$SCRIPT_DIR/build_cbc_trunk.sh"
HiGHS_BUILD_SCRIPT="$SCRIPT_DIR/build_highs_trunk.sh"

if [ ! -f "$SCIP_BUILD_SCRIPT" ]; then
    warning "SCIP build script not found: $SCIP_BUILD_SCRIPT"
fi

if [ ! -f "$CBC_BUILD_SCRIPT" ]; then
    warning "CBC build script not found: $CBC_BUILD_SCRIPT"
fi

if [ ! -f "$HiGHS_BUILD_SCRIPT" ]; then
    warning "HiGHS build script not found: $HiGHS_BUILD_SCRIPT"
fi

SCIP_PATH="$THIRD_PARTY_DIR/scip/build-trunk/bin/scip"
CBC_PATH="$THIRD_PARTY_DIR/cbc/install-trunk/bin/cbc"
HiGHS_PATH="$THIRD_PARTY_DIR/HiGHS/build-trunk/bin/highs"

if [ ! -f "$SCIP_PATH" ]; then
    info "Building SCIP..."
    "$SCIP_BUILD_SCRIPT" &> /dev/null
    if [ $? -ne 0 ]; then
        error "Failed to build SCIP"
        exit 1
    fi
fi
info "SCIP version:"
$SCIP_PATH --version

if [ ! -f "$CBC_PATH" ]; then
    info "Building CBC..."
    "$CBC_BUILD_SCRIPT"
    if [ $? -ne 0 ]; then
        error "Failed to build CBC"
        exit 1
    fi
fi
info "CBC version:"
$CBC_PATH --version

if [ ! -f "$HiGHS_PATH" ]; then
    info "Building HiGHS..."
    "$HiGHS_BUILD_SCRIPT"
    if [ $? -ne 0 ]; then
        error "Failed to build HiGHS"
        exit 1
    fi
fi
info "HiGHS version:"
$HiGHS_PATH --version

if [ ! -d "$PROJECT_BIN_DIR" ]; then
    mkdir -p "$PROJECT_BIN_DIR"
fi
ln -sf "$SCIP_PATH" "$PROJECT_BIN_DIR/scip"
ln -sf "$CBC_PATH" "$PROJECT_BIN_DIR/cbc"
ln -sf "$HiGHS_PATH" "$PROJECT_BIN_DIR/highs"

ln -sf "$ROOT_DIR/flip/fuzzer.py" "$PROJECT_BIN_DIR/flip"

export PATH="$PROJECT_BIN_DIR:$PATH"
export PYTHONPATH="$ROOT_DIR"

# Note: for commercial solvers, please install by following the instructions from respective official documentations.

info "Setup completed successfully!"

info "Run 'flip' to start the fuzzer."