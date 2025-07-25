from backend.database_config import Base, engine, SessionLocal
from backend.models import Fabricante, Vacina, UnidadeSaude, Paciente, Aplicacao
from datetime import date

def initialize_database():
    print("Conectando e criando tabelas...")
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")

    db = SessionLocal() # Usar 'db' para a sessão aqui
    try:
        # Povoamento (seu código existente)
        if db.query(Fabricante).count() == 0:
            print("Povoando Fabricantes...")
            fabricantes = [
                Fabricante(nome="Butantan"), Fabricante(nome="Fiocruz"),
                Fabricante(nome="Pfizer"), Fabricante(nome="Moderna"),
                Fabricante(nome="Janssen"), Fabricante(nome="GSK"),
                Fabricante(nome="Sinovac"), Fabricante(nome="Sanofi"),
                Fabricante(nome="Bharat Biotech"), Fabricante(nome="Sputnik V")
            ]
            db.add_all(fabricantes)
            db.commit()

        # Rebusque fabricantes do banco para garantir que IDs estão corretos
        fabricante_map = {f.nome: f.id for f in db.query(Fabricante).all()}

        if db.query(Vacina).count() == 0:
            print("Povoando Vacinas...")
            vacinas = [
                Vacina(nome="Coronavac", tipo="Vírus inativado", fabricante_id=fabricante_map["Butantan"]),
                Vacina(nome="AstraZeneca", tipo="Vetor viral", fabricante_id=fabricante_map["Fiocruz"]),
                Vacina(nome="Pfizer", tipo="mRNA", fabricante_id=fabricante_map["Pfizer"]),
                Vacina(nome="Moderna", tipo="mRNA", fabricante_id=fabricante_map["Moderna"]),
                Vacina(nome="Janssen", tipo="Vetor viral", fabricante_id=fabricante_map["Janssen"]),
                Vacina(nome="Shingrix", tipo="Subunidade proteica", fabricante_id=fabricante_map["GSK"]),
                Vacina(nome="Sinovac", tipo="Vírus inativado", fabricante_id=fabricante_map["Sinovac"]),
                Vacina(nome="Vaxigrip", tipo="Vírus inativado", fabricante_id=fabricante_map["Sanofi"]),
                Vacina(nome="Covaxin", tipo="Vírus inativado", fabricante_id=fabricante_map["Bharat Biotech"]),
                Vacina(nome="Sputnik", tipo="Vetor viral", fabricante_id=fabricante_map["Sputnik V"])
            ]
            db.add_all(vacinas)
            db.commit()

        if db.query(UnidadeSaude).count() == 0:
            print("Povoando Unidades de Saúde...")
            unidades = [
                UnidadeSaude(nome="Posto Central", endereco="Rua A, 123"),
                UnidadeSaude(nome="UBS Flores", endereco="Av. das Flores, 456"),
                UnidadeSaude(nome="UBS São José", endereco="Rua das Árvores, 10"),
                UnidadeSaude(nome="Centro de Saúde Vila Nova", endereco="Av. Brasil, 1000"),
                UnidadeSaude(nome="UBS Leste", endereco="Rua da Saúde, 200"),
                UnidadeSaude(nome="Posto Esperança", endereco="Travessa da Alegria, 50"),
                UnidadeSaude(nome="UBS Norte", endereco="Rua 7 de Setembro, 77"),
                UnidadeSaude(nome="Posto Aurora", endereco="Av. do Sol, 123"),
                UnidadeSaude(nome="UBS Harmonia", endereco="Rua Harmonia, 333"),
                UnidadeSaude(nome="Centro Médico Popular", endereco="Rua do Povo, 909")
            ]
            db.add_all(unidades)
            db.commit()

        if db.query(Paciente).count() == 0:
            print("Povoando Pacientes...")
            pacientes = [
                Paciente(nome="João da Silva", data_nascimento=date(1990, 5, 20), cpf="12345678800"),
                Paciente(nome="Maria Souza", data_nascimento=date(1985, 8, 15), cpf="98765452100"),
                Paciente(nome="Carlos Lima", data_nascimento=date(1980, 1, 10), cpf="12312012301"),
                Paciente(nome="Ana Paula", data_nascimento=date(1992, 7, 30), cpf="32132132142"),
                Paciente(nome="Fernanda Costa", data_nascimento=date(1975, 3, 12), cpf="45643645603"),
                Paciente(nome="Bruno Rocha", data_nascimento=date(2000, 9, 8), cpf="65465465704"),
                Paciente(nome="Luciana Teixeira", data_nascimento=date(1988, 12, 25), cpf="78978978905"),
                Paciente(nome="Pedro Henrique", data_nascimento=date(1995, 4, 5), cpf="98798791706"),
                Paciente(nome="Juliana Silva", data_nascimento=date(1999, 11, 19), cpf="11122239344"),
                Paciente(nome="Ricardo Souza", data_nascimento=date(1970, 6, 22), cpf="55566677988")
            ]
            db.add_all(pacientes)
            db.commit()

        if db.query(Aplicacao).count() == 0:
            print("Povoando Aplicações...")
            # Rebusque os IDs do banco para garantir que estão corretos
            pacientes_db = db.query(Paciente).all()
            vacinas_db = db.query(Vacina).all()
            unidades_db = db.query(UnidadeSaude).all()

            # Mapeia nomes/CPFs/etc. para IDs para uso nas aplicações
            paciente_map = {p.nome: p.id for p in pacientes_db}
            vacina_map = {v.nome: v.id for v in vacinas_db}
            unidade_map = {u.nome: u.id for u in unidades_db}

            aplicacoes = [
                Aplicacao(paciente_id=paciente_map["João da Silva"], vacina_id=vacina_map["Coronavac"], unidade_id=unidade_map["Posto Central"], data_aplicacao=date(2023, 1, 10)),
                Aplicacao(paciente_id=paciente_map["Maria Souza"], vacina_id=vacina_map["AstraZeneca"], unidade_id=unidade_map["UBS Flores"], data_aplicacao=date(2023, 2, 5)),
                Aplicacao(paciente_id=paciente_map["Carlos Lima"], vacina_id=vacina_map["Pfizer"], unidade_id=unidade_map["UBS São José"], data_aplicacao=date(2023, 3, 1)),
                Aplicacao(paciente_id=paciente_map["Ana Paula"], vacina_id=vacina_map["Moderna"], unidade_id=unidade_map["Centro de Saúde Vila Nova"], data_aplicacao=date(2023, 3, 5)),
                Aplicacao(paciente_id=paciente_map["Fernanda Costa"], vacina_id=vacina_map["Janssen"], unidade_id=unidade_map["UBS Leste"], data_aplicacao=date(2023, 3, 10)),
                Aplicacao(paciente_id=paciente_map["Bruno Rocha"], vacina_id=vacina_map["Shingrix"], unidade_id=unidade_map["Posto Esperança"], data_aplicacao=date(2023, 3, 15)),
                Aplicacao(paciente_id=paciente_map["Luciana Teixeira"], vacina_id=vacina_map["Sinovac"], unidade_id=unidade_map["UBS Norte"], data_aplicacao=date(2023, 3, 20)),
                Aplicacao(paciente_id=paciente_map["Pedro Henrique"], vacina_id=vacina_map["Vaxigrip"], unidade_id=unidade_map["Posto Aurora"], data_aplicacao=date(2023, 3, 25)),
                Aplicacao(paciente_id=paciente_map["Juliana Silva"], vacina_id=vacina_map["Covaxin"], unidade_id=unidade_map["UBS Harmonia"], data_aplicacao=date(2023, 3, 30)),
                Aplicacao(paciente_id=paciente_map["Ricardo Souza"], vacina_id=vacina_map["Sputnik"], unidade_id=unidade_map["Centro Médico Popular"], data_aplicacao=date(2023, 4, 1))
            ]
            db.add_all(aplicacoes)
            db.commit()

    except Exception as e:
        db.rollback()
        print(f"Erro durante o povoamento: {e}")
    finally:
        db.close()

    print("Povoamento concluído (se aplicável).")

if __name__ == "__main__":
    initialize_database()