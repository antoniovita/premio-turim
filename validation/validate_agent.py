"""Confere a pasta submetida e, opcionalmente, produz/inspeciona o ZIP."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "agent"
FLOORS = {str(number) for number in range(2, 7)}
BLOCKED_SUFFIXES = {".exe", ".dll", ".bat", ".cmd", ".msi", ".scr"}


def fail(message: str) -> None:
    raise ValueError(message)


def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            fail(f"Chave JSON duplicada: {key}")
        result[key] = value
    return result


def agent_files() -> dict[str, Path]:
    files: dict[str, Path] = {}
    for path in AGENT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(AGENT).as_posix()
        if any(part.startswith(".") for part in PurePosixPath(relative).parts):
            fail(f"Arquivo oculto dentro do agente: {relative}")
        if path.suffix.lower() in BLOCKED_SUFFIXES:
            fail(f"Executável bloqueado: {relative}")
        files[relative] = path
    return files


def validate_source() -> dict[str, Path]:
    files = agent_files()
    if "CLAUDE.md" in files:
        fail("Use apenas Claude.md, com a capitalização do starter kit")
    if "Claude.md" not in files or "contrato.json" not in files:
        fail("Claude.md e contrato.json devem estar na raiz do ZIP")
    manifesto = files["Claude.md"].read_text(encoding="utf-8-sig")
    if not manifesto.strip() or len(manifesto) > 3000:
        fail(f"Claude.md vazio ou acima de 3.000 caracteres: {len(manifesto)}")
    if not any(name.startswith("tools/") for name in files):
        fail("A pasta tools/ precisa conter ao menos um arquivo")

    raw = files["contrato.json"].read_text(encoding="utf-8")
    if raw.startswith("\ufeff"):
        fail("contrato.json não pode conter BOM")
    contract = json.loads(raw, object_pairs_hook=no_duplicate_keys)
    if not isinstance(contract, dict) or set(contract) != {"nome", "descricao", "andares"}:
        fail("A raiz do contrato deve conter apenas nome, descricao e andares")
    name, description, floors = contract["nome"], contract["descricao"], contract["andares"]
    if not isinstance(name, str) or not 1 <= len(name) <= 80:
        fail("nome deve ter entre 1 e 80 caracteres")
    if not isinstance(description, str) or len(description) < 40 or "TROQUE ESTE TEXTO" in description:
        fail("descricao deve ser original e ter ao menos 40 caracteres")
    if not isinstance(floors, dict) or set(floors) != FLOORS:
        fail("andares deve conter exatamente as chaves 2 a 6")

    for floor in sorted(FLOORS):
        item = floors[floor]
        if not isinstance(item, dict) or "prompt" not in item or not set(item) <= {"prompt", "saida"}:
            fail(f"Andar {floor}: somente prompt obrigatório e saida opcional")
        name = item["prompt"]
        if not isinstance(name, str) or not name:
            fail(f"Andar {floor}: caminho do prompt inválido")
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or relative.suffix != ".md" or name not in files:
            fail(f"Andar {floor}: prompt ausente ou fora da raiz: {name}")
        content = files[name].read_text(encoding="utf-8-sig")
        if not content.strip() or len(content) > 2500:
            fail(f"Andar {floor}: prompt vazio ou acima de 2.500 caracteres: {len(content)}")
        if "ESCREVA AQUI" in content or "TODO" in content:
            fail(f"Andar {floor}: marcador não preenchido")
        print(f"Andar {floor}: {name}, {len(content)}/2500 caracteres")

    print(f"Manifesto: {len(manifesto)}/3000 caracteres; {len(files)} arquivos no agente")
    return files


def inspect_zip(path: Path, expected: set[str]) -> None:
    with zipfile.ZipFile(path) as archive:
        actual = {entry.filename for entry in archive.infolist() if not entry.is_dir()}
        if len(actual) != sum(not entry.is_dir() for entry in archive.infolist()):
            fail("O ZIP contém nomes de arquivos duplicados")
        if actual != expected:
            fail(f"Conteúdo do ZIP difere da pasta: faltando={sorted(expected-actual)}, extras={sorted(actual-expected)}")
        for name in actual:
            relative = PurePosixPath(name)
            if relative.is_absolute() or ".." in relative.parts or name.startswith("agent/"):
                fail(f"Arquivo fora da raiz esperada no ZIP: {name}")
    print(f"ZIP válido: {path} ({len(actual)} arquivos na raiz correta)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, help="cria o ZIP e confere seu conteúdo")
    parser.add_argument("--zip", type=Path, help="confere um ZIP existente")
    args = parser.parse_args()
    files = validate_source()
    if args.package:
        args.package.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, path in sorted(files.items()):
                archive.write(path, arcname=name)
        inspect_zip(args.package, set(files))
    if args.zip:
        inspect_zip(args.zip, set(files))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        print(f"Falha: {error}", file=sys.stderr)
        raise SystemExit(1)
