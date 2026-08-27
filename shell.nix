{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "fastap-backend";

  packages = with pkgs; [
    python311
    uv

    #c++ runtime for python wheels
    stdenv.cc.cc.lib
    # Native dependencies
    openssl
    postgresql
  ];

  shellHook = ''
    # Exposes libstdc++.so.6 to Python binary extensions
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
    echo ""
    echo "🚀 FastAPI development environment"
    echo ""
    echo "Python: $(python --version)"
    echo "uv: $(uv --version)"
    echo ""
    cd app
    echo "Run:"
    echo "  uv sync"
    echo "  uv run fastapi dev"
    echo ""
  '';
}