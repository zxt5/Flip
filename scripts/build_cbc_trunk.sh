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
CBC_DIR="$THIRD_PARTY_DIR/cbc"
PREFIX="$CBC_DIR/install-trunk"
BUILD_DIR="$CBC_DIR/build-trunk"

mkdir -p "$THIRD_PARTY_DIR" || die "Failed to create third_party dir: $THIRD_PARTY_DIR"

if [ ! -d "$CBC_DIR" ]; then
    mkdir -p "$CBC_DIR" || die "Failed to create cbc dir: $CBC_DIR"
fi

cd "$CBC_DIR" || die "Failed to cd to: $CBC_DIR"

echo "[cbc] root:       $ROOT_DIR"
echo "[cbc] workdir:    $CBC_DIR"
echo "[cbc] prefix:     $PREFIX"
echo "[cbc] build-dir:  $BUILD_DIR"

if [ ! -f "coinbrew" ]; then
    wget -O coinbrew https://raw.githubusercontent.com/coin-or/coinbrew/master/coinbrew
    if [ $? -ne 0 ]; then
        die "Failed to download coinbrew."
    fi
    chmod +x coinbrew
fi

if [ ! -x "coinbrew" ]; then
    die "coinbrew is not executable. Please check file permissions: $CBC_DIR/coinbrew"
fi

./coinbrew fetch Cbc@master

if [ -d "$PREFIX" ]; then
    rm -rf "$PREFIX"
fi

if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
fi

CC=$CC CXX=$CXX \
./coinbrew build Cbc \
    --prefix="$PREFIX" \
    --build-dir="$BUILD_DIR" \
    --reconfigure \
    --tests=none \
    --enable-debug

if [ $? -ne 0 ]; then
    die "Failed to build Cbc"
else
    echo "Cbc built successfully"
    $PREFIX/bin/cbc --version
fi

exit 0