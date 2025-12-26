#!/bin/bash
set -euo pipefail

export CC=clang
export CXX=clang++

die() {
    echo "Error: $*" >&2
    exit 1
}

SCRIPT_PATH="$(realpath "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd -P)" || die "Failed to determine project root."

THIRD_PARTY_DIR="$ROOT_DIR/third_party"
HIGHS_DIR="$THIRD_PARTY_DIR/HiGHS"
PREFIX="$HIGHS_DIR/install-trunk"
BUILD_DIR="$HIGHS_DIR/build-trunk"

mkdir -p "$THIRD_PARTY_DIR" || die "Failed to create third_party dir: $THIRD_PARTY_DIR"

if [ ! -d "$HIGHS_DIR" ]; then
    git clone https://github.com/ERGO-Code/HiGHS.git "$HIGHS_DIR"
    if [ $? -ne 0 ]; then
        die "Failed to clone HiGHS."
    fi
fi

cd "$HIGHS_DIR" || die "Failed to cd to: $HIGHS_DIR"
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
    -DCMAKE_C_COMPILER="$CC" \
    -DCMAKE_CXX_COMPILER="$CXX" \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

if [ $? -ne 0 ]; then
    die "Failed to configure HiGHS"
fi

cmake --build . -j$(nproc)

if [ $? -ne 0 ]; then
    die "Failed to build HiGHS"
else
    echo "HiGHS built successfully:"
    $HIGHS_DIR/build-trunk/bin/highs --version
fi

exit 0