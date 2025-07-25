import panel as pn
import param
from backend.crud_operations import get_fabricantes, create_fabricante, delete_fabricante, get_vacinas, create_vacina, update_vacina, delete_vacina
from backend.database_config import get_db

pn.extension('tabulator', 'notifications')

class GestaoVacinasFabricantes(pn.viewable.Viewer):
    # --- Parâmetros de Filtragem de Fabricantes ---
    filtro_fabricante_nome = param.String(default="", placeholder="Filtrar por nome do fabricante...")

    # --- Parâmetros para Inclusão de Fabricante ---
    novo_fabricante_nome = param.String(default="", placeholder="Nome do novo fabricante")
    criar_fabricante_btn = pn.widgets.Button(name="Adicionar Fabricante", button_type="primary")
    remover_fabricante_id = param.Integer(default=0, doc="ID do Fabricante para remover")
    remover_fabricante_btn = pn.widgets.Button(name="Remover Fabricante", button_type="danger")

    # --- Parâmetros de Filtragem de Vacinas ---
    filtro_vacina_nome = param.String(default="", placeholder="Filtrar por nome da vacina...")
    filtro_vacina_tipo = param.String(default="", placeholder="Filtrar por tipo...")
    filtro_vacina_fabricante_nome = param.String(default="", placeholder="Filtrar por fabricante...")

    # --- Parâmetros para Inclusão de Vacina ---
    nova_vacina_nome = param.String(default="", placeholder="Nome da nova vacina")
    nova_vacina_tipo = param.String(default="", placeholder="Tipo da nova vacina")
    # Seletor para fabricantes (dropdown)
    vacina_fabricante_select = param.Selector(objects=[])
    criar_vacina_btn = pn.widgets.Button(name="Adicionar Vacina", button_type="primary")

    # --- Parâmetros para Edição/Remoção de Vacina ---
    vacina_id_crud = param.Integer(default=0, doc="ID da Vacina para editar/remover")
    nova_vacina_nome_edit = param.String(default="", placeholder="Novo nome da vacina (opcional)")
    nova_vacina_tipo_edit = param.String(default="", placeholder="Novo tipo da vacina (opcional)")
    vacina_fabricante_edit_select = param.Selector(objects=[])
    editar_vacina_btn = pn.widgets.Button(name="Atualizar Vacina", button_type="warning")
    remover_vacina_btn = pn.widgets.Button(name="Remover Vacina", button_type="danger")


    def __init__(self, **params):
        super().__init__(**params)
        self._update_fabricantes_selectors() # Preenche seletores ao iniciar
        self.criar_fabricante_btn.on_click(self._on_criar_fabricante)
        self.remover_fabricante_btn.on_click(self._on_remover_fabricante)
        self.criar_vacina_btn.on_click(self._on_criar_vacina)
        self.editar_vacina_btn.on_click(self._on_editar_vacina)
        self.remover_vacina_btn.on_click(self._on_remover_vacina)


    def _update_fabricantes_selectors(self):
        db = next(get_db())
        fabricantes = get_fabricantes(db)
        db.close()
        # Mapeia nomes para IDs para os Selectors do Panel
        self._fabricantes_nomes_ids = {f.nome: f.id for f in fabricantes}
        self.param.vacina_fabricante_select.objects = list(self._fabricantes_nomes_ids.keys())
        self.param.vacina_fabricante_edit_select.objects = [''] + list(self._fabricantes_nomes_ids.keys()) # Adiciona opção vazia para edição
        if self._fabricantes_nomes_ids:
            self.vacina_fabricante_select = list(self._fabricantes_nomes_ids.keys())[0]
        else:
            self.vacina_fabricante_select = None
            self.vacina_fabricante_edit_select = '' # Define como vazio se não houver fabricantes

    # --- Métodos de Consulta ---
    @param.depends('filtro_fabricante_nome', watch=True)
    def _get_fabricantes_data(self):
        db = next(get_db())
        fabricantes = get_fabricantes(db, nome=self.filtro_fabricante_nome)
        db.close()
        data = [{'ID': f.id, 'Nome': f.nome} for f in fabricantes]
        return pn.widgets.Tabulator(data, show_index=False, layout='fit_columns', sizing_mode='stretch_width')

    @param.depends('filtro_vacina_nome', 'filtro_vacina_tipo', 'filtro_vacina_fabricante_nome', watch=True)
    def _get_vacinas_data(self):
        db = next(get_db())
        vacinas = get_vacinas(db, nome=self.filtro_vacina_nome, tipo=self.filtro_vacina_tipo, fabricante_nome=self.filtro_vacina_fabricante_nome)
        db.close()
        data = [{'ID': v.id, 'Nome': v.nome, 'Tipo': v.tipo, 'Fabricante': v.fabricante.nome if v.fabricante else 'N/A'} for v in vacinas]
        return pn.widgets.Tabulator(data, show_index=False, layout='fit_columns', sizing_mode='stretch_width')

    # --- Métodos de Ação para Fabricantes ---
    def _on_criar_fabricante(self, event):
        if self.novo_fabricante_nome:
            db = next(get_db())
            try:
                create_fabricante(db, self.novo_fabricante_nome)
                pn.state.notifications.success("Fabricante adicionado com sucesso!")
                self._update_fabricantes_selectors() # Atualiza os seletores
                self.param.trigger('filtro_fabricante_nome') # Atualiza a tabela
            except Exception as e:
                pn.state.notifications.error(f"Erro ao adicionar fabricante: {e}")
            finally:
                db.close()
            self.novo_fabricante_nome = ""
        else:
            pn.state.notifications.warning("O nome do fabricante não pode ser vazio.")

    def _on_remover_fabricante(self, event):
        if self.remover_fabricante_id > 0:
            db = next(get_db())
            try:
                fabricante_removido = delete_fabricante(db, self.remover_fabricante_id)
                if fabricante_removido:
                    pn.state.notifications.success(f"Fabricante '{fabricante_removido.nome}' removido!")
                    self._update_fabricantes_selectors()
                    self.param.trigger('filtro_fabricante_nome')
                else:
                    pn.state.notifications.warning("Fabricante não encontrado.")
            except Exception as e:
                pn.state.notifications.error(f"Erro ao remover fabricante: {e}. Verifique dependências (vacinas).")
            finally:
                db.close()
            self.remover_fabricante_id = 0
        else:
            pn.state.notifications.warning("Forneça um ID de fabricante válido.")

    # --- Métodos de Ação para Vacinas ---
    def _on_criar_vacina(self, event):
        if self.nova_vacina_nome and self.nova_vacina_tipo and self.vacina_fabricante_select:
            fabricante_id = self._fabricantes_nomes_ids.get(self.vacina_fabricante_select)
            if fabricante_id is None:
                pn.state.notifications.error("Selecione um fabricante válido.")
                return

            db = next(get_db())
            try:
                create_vacina(db, self.nova_vacina_nome, self.nova_vacina_tipo, fabricante_id)
                pn.state.notifications.success("Vacina adicionada com sucesso!")
                self.param.trigger('filtro_vacina_nome') # Atualiza a tabela
            except Exception as e:
                pn.state.notifications.error(f"Erro ao adicionar vacina: {e}")
            finally:
                db.close()
            self.nova_vacina_nome = ""
            self.nova_vacina_tipo = ""
            # Manter o fabricante selecionado ou resetar se for o caso
        else:
            pn.state.notifications.warning("Preencha todos os campos da nova vacina.")

    def _on_editar_vacina(self, event):
        if self.vacina_id_crud > 0:
            db = next(get_db())
            try:
                fabricante_id_to_update = None
                if self.vacina_fabricante_edit_select:
                    fabricante_id_to_update = self._fabricantes_nomes_ids.get(self.vacina_fabricante_edit_select)

                vacina_atualizada = update_vacina(db, self.vacina_id_crud,
                                                new_nome=self.nova_vacina_nome_edit if self.nova_vacina_nome_edit else None,
                                                new_tipo=self.nova_vacina_tipo_edit if self.nova_vacina_tipo_edit else None,
                                                new_fabricante_id=fabricante_id_to_update)
                if vacina_atualizada:
                    pn.state.notifications.success(f"Vacina ID {vacina_atualizada.id} atualizada!")
                    self.param.trigger('filtro_vacina_nome')
                else:
                    pn.state.notifications.warning("Vacina não encontrada.")
            except Exception as e:
                pn.state.notifications.error(f"Erro ao atualizar vacina: {e}")
            finally:
                db.close()
            self.vacina_id_crud = 0
            self.nova_vacina_nome_edit = ""
            self.nova_vacina_tipo_edit = ""
            self.vacina_fabricante_edit_select = '' # Resetar seletor
        else:
            pn.state.notifications.warning("Forneça um ID de vacina válido.")

    def _on_remover_vacina(self, event):
        if self.vacina_id_crud > 0:
            db = next(get_db())
            try:
                vacina_removida = delete_vacina(db, self.vacina_id_crud)
                if vacina_removida:
                    pn.state.notifications.success(f"Vacina '{vacina_removida.nome}' removida!")
                    self.param.trigger('filtro_vacina_nome')
                else:
                    pn.state.notifications.warning("Vacina não encontrada.")
            except Exception as e:
                pn.state.notifications.error(f"Erro ao remover vacina: {e}. Verifique dependências (aplicações).")
            finally:
                db.close()
            self.vacina_id_crud = 0
        else:
            pn.state.notifications.warning("Forneça um ID de vacina válido para remoção.")

    # --- Layout da Tela ---
    def __panel__(self):
        fabricantes_pane = pn.Column(
            pn.pane.Markdown("## Gestão de Fabricantes", styles={'font-weight': 'bold'}),
            pn.Row(
                pn.widgets.TextInput.from_param(self.param.filtro_fabricante_nome, name="Filtrar Nome")
            ),
            self._get_fabricantes_data,
            pn.pane.Markdown("### Adicionar/Remover Fabricante"),
            pn.Row(
                pn.widgets.TextInput.from_param(self.param.novo_fabricante_nome),
                self.criar_fabricante_btn
            ),
            pn.Row(
                pn.widgets.IntInput.from_param(self.param.remover_fabricante_id, name="ID Fabricante"),
                self.remover_fabricante_btn
            ),
            sizing_mode='stretch_width'
        )

        vacinas_pane = pn.Column(
            pn.pane.Markdown("## Gestão de Vacinas", styles={'font-weight': 'bold'}),
            pn.Row(
                pn.widgets.TextInput.from_param(self.param.filtro_vacina_nome, name="Filtrar Nome"),
                pn.widgets.TextInput.from_param(self.param.filtro_vacina_tipo, name="Filtrar Tipo"),
                pn.widgets.TextInput.from_param(self.param.filtro_vacina_fabricante_nome, name="Filtrar Fabricante")
            ),
            self._get_vacinas_data,
            pn.pane.Markdown("### Adicionar Nova Vacina"),
            pn.Column( # Usar Column para alinhar verticalmente se houver muitos campos
                pn.Row(
                    pn.widgets.TextInput.from_param(self.param.nova_vacina_nome),
                    pn.widgets.TextInput.from_param(self.param.nova_vacina_tipo)
                ),
                pn.Row(
                    pn.widgets.Select.from_param(self.param.vacina_fabricante_select, name="Fabricante"),
                    self.criar_vacina_btn
                )
            ),
            pn.pane.Markdown("### Editar/Remover Vacina (por ID)"),
            pn.Column(
                pn.widgets.IntInput.from_param(self.param.vacina_id_crud, name="ID da Vacina"),
                pn.Row(
                    pn.widgets.TextInput.from_param(self.param.nova_vacina_nome_edit),
                    pn.widgets.TextInput.from_param(self.param.nova_vacina_tipo_edit)
                ),
                pn.Row(
                    pn.widgets.Select.from_param(self.param.vacina_fabricante_edit_select, name="Novo Fabricante (opcional)"),
                    self.editar_vacina_btn,
                    self.remover_vacina_btn
                )
            ),
            sizing_mode='stretch_width'
        )
        return pn.Column(fabricantes_pane, vacinas_pane, sizing_mode='stretch_width')