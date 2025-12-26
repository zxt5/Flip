#!/bin/bash
set -euo pipefail

export CC=clang
export CXX=clang++

die() {
    echo "Error: $*" >&2
    exit 1
}

readonly build_soplex=true

SCRIPT_PATH="$(realpath "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd -P)" || die "Failed to determine project root."

THIRD_PARTY_DIR="$ROOT_DIR/third_party"
SCIP_DIR="$THIRD_PARTY_DIR/scip"
SOPLEX_DIR="$THIRD_PARTY_DIR/soplex"
BUILD_DIR="$SCIP_DIR/build-trunk"

mkdir -p "$THIRD_PARTY_DIR" || die "Failed to create third_party dir: $THIRD_PARTY_DIR"

if [ "$build_soplex" = true ]; then
    if [ ! -d "$SOPLEX_DIR" ]; then
        git clone https://github.com/scipopt/soplex.git "$SOPLEX_DIR"
        if [ $? -ne 0 ]; then
            die "Failed to clone soplex."
        fi
    fi
    cd "$SOPLEX_DIR" || die "Failed to cd to: $SOPLEX_DIR"
    git stash || die "Failed to stash changes."
    git checkout master || die "Failed to checkout master."
    git pull || die "Failed to pull latest changes."
    SOPLEX_BUILD_DIR="$SOPLEX_DIR/build-trunk"
    if [ -d "$SOPLEX_BUILD_DIR" ]; then
        rm -rf "$SOPLEX_BUILD_DIR"
    fi
    mkdir -p "$SOPLEX_BUILD_DIR" || die "Failed to create build dir: $SOPLEX_BUILD_DIR"
    cd "$SOPLEX_BUILD_DIR" || die "Failed to cd to: $SOPLEX_BUILD_DIR"
    cmake .. \
        -DCMAKE_BUILD_TYPE=Debug \
        -DCMAKE_C_COMPILER="$CC" \
        -DCMAKE_CXX_COMPILER="$CXX" \
        -DAUTOBUILD=ON \
        -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
    if [ $? -ne 0 ]; then
        die "Failed to configure soplex"
    fi
    cmake --build . -j$(nproc)
    if [ $? -ne 0 ]; then
        die "Failed to build soplex"
    fi
fi

if [ ! -d "$SCIP_DIR" ]; then
    git clone https://github.com/scipopt/scip.git "$SCIP_DIR"
    if [ $? -ne 0 ]; then
        die "Failed to clone SCIP."
    fi
fi

cd "$SCIP_DIR" || die "Failed to cd to: $SCIP_DIR"
git stash || die "Failed to stash changes."
git checkout master || die "Failed to checkout master."
git pull || die "Failed to pull latest changes."

if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
fi
mkdir -p "$BUILD_DIR" || die "Failed to create build dir: $BUILD_DIR"
cd "$BUILD_DIR" || die "Failed to cd to: $BUILD_DIR"

cmake .. \
    -DCMAKE_BUILD_TYPE=Debug \
    -DAUTOBUILD=ON \
    -DCMAKE_C_COMPILER="$CC" \
    -DCMAKE_CXX_COMPILER="$CXX" \
    -DSOPLEX_DIR="$SOPLEX_DIR/build-trunk" \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

if [ $? -ne 0 ]; then
    die "Failed to configure SCIP"
fi

cmake --build . -j$(nproc)

if [ $? -ne 0 ]; then
    die "Failed to build SCIP"
else
    echo "SCIP built successfully:"
    $SCIP_DIR/build-trunk/bin/scip --version
fi

exit 0