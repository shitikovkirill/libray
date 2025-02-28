{ pkgs ? import <nixpkgs> { }, projectName ? "application" }:
let
  scriptPrefix = "${projectName}-";

  docScript = pkgs.writeShellScriptBin (scriptPrefix + "doc")
    "nix-build docs/ --out-link .docs";
  docRunScript = pkgs.writeShellScriptBin (scriptPrefix + "doc-wotch")
    "python -m http.server 8001 --directory .docs --bind 127.0.0.1";

  coverageRunScript = pkgs.writeShellScriptBin (scriptPrefix + "coverage-wotch")
    "python -m http.server 8002 --directory htmlcov/ --bind 127.0.0.1";

  styleScript = let
    styleNix = "find . -name '*.nix' -not -path '.direnv' -exec nixfmt {} \\;";
    styleOrder = "isort ./${projectName}/";
    stylePython =
      "black ${projectName} --exclude ${projectName}/migrations -l 79";
  in pkgs.writeShellScriptBin (scriptPrefix + "style")
  "${styleOrder} && ${stylePython} && ${styleNix}";

  mypyScript =
    pkgs.writeShellScriptBin (scriptPrefix + "mypy") "mypy ${projectName}";

  lintScript =
    pkgs.writeShellScriptBin (scriptPrefix + "lint") "flake8 ${projectName}";

  preCommitInit = pkgs.writeShellScriptBin (scriptPrefix + "pre-commit-init")
    "pre-commit install";
  preCommitChackAll = pkgs.writeShellScriptBin (scriptPrefix + "pre-commit")
    "pre-commit run --all-files";

  run = pkgs.writeShellScriptBin (scriptPrefix + "run") ''
    python ${projectName}/manage.py runserver
  '';

  runInDebug = pkgs.writeShellScriptBin (scriptPrefix + "run-debug") ''
    python -m debugpy --listen localhost:5678 ${projectName}/manage.py runserver
  '';

  runTests = pkgs.writeShellScriptBin (scriptPrefix + "run-tests") ''
    python -m pytest
  '';

  runTestsInDebug =
    pkgs.writeShellScriptBin (scriptPrefix + "run-tests-debug") ''
      python -m debugpy --listen localhost:5678 --wait-for-client  -m pytest
    '';

  runLab = pkgs.writeShellScriptBin (scriptPrefix + "run-lab") ''
    python ${projectName}/manage.py shell_plus --lab
  '';

  migrationsScript =
    pkgs.writeShellScriptBin (scriptPrefix + "make-migration") ''
      python ${projectName}/manage.py makemigrations
    '';
  migrateScript = pkgs.writeShellScriptBin (scriptPrefix + "migrate") ''
    python ${projectName}/manage.py  migrate
  '';

  translate = pkgs.writeShellScriptBin (scriptPrefix + "translate") ''
    python ${projectName}/manage.py makemessages -a --ignore=venv --traceback && poedit && python -m ${projectName}.manage  compilemessages --ignore=env
  '';

in with pkgs.python311Packages;
with pkgs; [
  # Linting
  pkgs.nixfmt-classic
  isort
  black
  pylint
  pylint-django
  styleScript

  mypy
  mypyScript

  flake8
  lintScript

  # Documantation
  docScript
  docRunScript

  coverageRunScript

  pkgs.pre-commit
  preCommitInit
  preCommitChackAll

  # Develop
  run
  runInDebug
  runTests
  runTestsInDebug
  runLab
  migrationsScript
  migrateScript

  # Translaste
  poedit
  translate
]
