"""
Módulo de Persistência — SQLite
Engetrol Engenharia — Sistema de Orçamentação
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "orcamentos.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS orcamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cliente TEXT DEFAULT '',
        local_obra TEXT DEFAULT '',
        versao INTEGER DEFAULT 1,
        status TEXT DEFAULT 'rascunho',
        dados_json TEXT NOT NULL,
        criado_em TEXT NOT NULL,
        atualizado_em TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS versoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orcamento_id INTEGER NOT NULL,
        versao INTEGER NOT NULL,
        dados_json TEXT NOT NULL,
        criado_em TEXT NOT NULL,
        FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id)
    );
    """)
    conn.commit()
    conn.close()


def salvar_orcamento(state_dict: dict, orcamento_id: int = None) -> int:
    """Salva ou atualiza um orçamento. Retorna o ID."""
    conn = get_conn()
    agora = datetime.now().isoformat()
    dados_json = json.dumps(state_dict, ensure_ascii=False, default=str)

    nome = state_dict.get("nome_obra", "Sem nome")
    cliente = state_dict.get("cliente", "")
    local_obra = state_dict.get("local_obra", "")

    if orcamento_id:
        # Atualizar existente
        row = conn.execute("SELECT versao FROM orcamentos WHERE id = ?", (orcamento_id,)).fetchone()
        nova_versao = (row["versao"] + 1) if row else 1

        # Salvar versão anterior
        if row:
            old = conn.execute("SELECT dados_json FROM orcamentos WHERE id = ?", (orcamento_id,)).fetchone()
            conn.execute(
                "INSERT INTO versoes (orcamento_id, versao, dados_json, criado_em) VALUES (?, ?, ?, ?)",
                (orcamento_id, row["versao"], old["dados_json"], agora),
            )

        conn.execute(
            """UPDATE orcamentos SET nome=?, cliente=?, local_obra=?, versao=?,
               dados_json=?, atualizado_em=? WHERE id=?""",
            (nome, cliente, local_obra, nova_versao, dados_json, agora, orcamento_id),
        )
        conn.commit()
        conn.close()
        return orcamento_id
    else:
        # Novo orçamento
        cur = conn.execute(
            """INSERT INTO orcamentos (nome, cliente, local_obra, versao, status, dados_json, criado_em, atualizado_em)
               VALUES (?, ?, ?, 1, 'rascunho', ?, ?, ?)""",
            (nome, cliente, local_obra, dados_json, agora, agora),
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return new_id


def listar_orcamentos() -> list:
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, nome, cliente, local_obra, versao, status, criado_em, atualizado_em FROM orcamentos ORDER BY atualizado_em DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def carregar_orcamento(orcamento_id: int) -> dict:
    conn = get_conn()
    row = conn.execute("SELECT dados_json FROM orcamentos WHERE id = ?", (orcamento_id,)).fetchone()
    conn.close()
    if row:
        return json.loads(row["dados_json"])
    return {}


def listar_versoes(orcamento_id: int) -> list:
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, versao, criado_em FROM versoes WHERE orcamento_id = ? ORDER BY versao DESC",
        (orcamento_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def carregar_versao(versao_id: int) -> dict:
    conn = get_conn()
    row = conn.execute("SELECT dados_json FROM versoes WHERE id = ?", (versao_id,)).fetchone()
    conn.close()
    if row:
        return json.loads(row["dados_json"])
    return {}


def excluir_orcamento(orcamento_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM versoes WHERE orcamento_id = ?", (orcamento_id,))
    conn.execute("DELETE FROM orcamentos WHERE id = ?", (orcamento_id,))
    conn.commit()
    conn.close()


# Inicializar DB ao importar
init_db()
