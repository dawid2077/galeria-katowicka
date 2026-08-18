{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "fastapi-flutter-backend-env";

  packages = with pkgs; [
    python311
    uv

    # Native dependencies
    openssl
    postgresql
  ];

  shellHook = ''
    echo ""
    echo "🚀 FastAPI development environment"
    echo ""
    echo "Python: $(python --version)"
    echo "uv: $(uv --version)"
    echo ""
    cd backend
    echo "Run:"
    echo "  uv sync"
    echo "  uv run uvicorn main:app --reload"
    echo ""
  '';
}