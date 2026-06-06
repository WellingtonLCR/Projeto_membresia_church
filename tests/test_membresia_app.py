import unittest
from datetime import datetime
from unittest.mock import patch

from werkzeug.security import generate_password_hash

from app import app


class MembresiaAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def autenticar(self):
        with self.client.session_transaction() as sess:
            sess["usuario_logado"] = "teste@igreja.org"
            sess["usuario_nome"] = "Usuario Teste"
            sess["usuario_perfil"] = "Administrador"
            sess["usuario_modo"] = "admin"
            sess["usuario_id"] = 1

    def test_rotas_publicas_renderizam(self):
        for rota in [
            "/",
            "/login",
            "/cadastro",
            "/sobre-equipe",
            "/app",
            "/app/eventos",
            "/app/cultos",
            "/app/feed",
            "/app/devocional",
            "/app/oracao",
            "/app/doacoes",
            "/app/cadastro",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 200)

    def test_app_usuario_home_exibe_conteudo_alimentado_pelo_admin(self):
        evento = {
            "id": 10,
            "nome": "Culto Jovem",
            "data_inicio": datetime(2026, 6, 12, 20, 0),
            "local": "Templo principal",
            "banner_path": None,
        }
        aviso = {
            "titulo": "Aviso Admin",
            "categoria": "Comunicado",
            "conteudo": "Conteudo publicado pelo painel administrativo.",
        }
        devocional = {
            "titulo": "Devocional Admin",
            "categoria": "Devocional",
            "conteudo": "Reflexao publicada pela equipe.",
        }

        def config(chave, padrao=""):
            valores = {
                "programacao.domingo": "Domingo as 18h",
                "programacao.quarta": "Quarta as 20h",
                "programacao.celulas": "Durante a semana",
                "doacao.mensagem": "Mensagem de contribuicao configurada no painel.",
            }
            return valores.get(chave, padrao)

        with patch("app.obter_igreja", return_value={"nome": "Igreja Teste", "endereco": "Rua Central"}), \
             patch("app.listar_eventos_publicos", return_value=[evento]), \
             patch("app.listar_mural_publico", side_effect=[[aviso], [devocional]]), \
             patch("app.gerar_metricas_app", return_value={"eventos": 1, "avisos": 1, "devocionais": 1, "testemunhos": 0, "visitantes": 3}), \
             patch("app.gerar_metricas", return_value={}), \
             patch("app.obter_config", side_effect=config):
            resposta = self.client.get("/app")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Culto Jovem".encode(), resposta.data)
        self.assertIn("Aviso Admin".encode(), resposta.data)
        self.assertIn("Devocional Admin".encode(), resposta.data)
        self.assertIn("Domingo".encode(), resposta.data)

    def test_app_usuario_evento_inexistente_redireciona_para_agenda(self):
        resposta = self.client.get("/app/eventos/999999", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app/eventos", resposta.headers["Location"])

    def test_app_usuario_oracao_valida_campos_obrigatorios(self):
        resposta = self.client.post(
            "/app/oracao",
            data={"solicitante_nome": "", "pedido": ""},
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe seu nome e o pedido de".encode(), resposta.data)

    def test_rotas_privadas_exigem_login(self):
        resposta = self.client.get("/membros/listar", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])

    def test_listagens_privadas_renderizam_com_login(self):
        self.autenticar()

        for rota in [
            "/pessoas/painel",
            "/pessoas/aniversarios",
            "/membros/listar",
            "/financeiro/painel",
            "/financeiro/receitas",
            "/financeiro/despesas",
            "/financeiro/cadastros",
            "/financeiro/categorias",
            "/financeiro/centros-custo",
            "/financeiro/contas",
            "/financeiro/formas-recebimento",
            "/financeiro/formas-pagamento",
            "/ministerios/listar",
            "/ministerios/painel",
            "/usuarios/listar",
            "/celulas/listar",
            "/celulas/painel",
            "/eventos/listar",
            "/financeiro/listar",
            "/comunicacao/painel",
            "/comunicacao/listar",
            "/relatorios/listar",
            "/configuracoes/listar",
            "/configuracoes/igreja",
            "/configuracoes/historia",
            "/configuracoes/informacoes",
            "/configuracoes/programacao",
            "/configuracoes/permissoes",
            "/configuracoes/app",
            "/configuracoes/modulos",
            "/familias/listar",
            "/fornecedores/listar",
            "/doacoes/listar",
            "/mural/listar",
            "/intercessao/painel",
            "/intercessao/listar",
            "/intercessao/testemunhos",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 200)

    def test_cadastro_publico_exige_email_e_senha_para_visitante(self):
        resposta = self.client.post(
            "/cadastro",
            data={"nome": "Pessoa Teste"},
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe seu nome, e-mail e senha".encode(), resposta.data)

    def test_cadastro_publico_registra_visitante_no_app(self):
        with patch("app.email_membro_em_uso", return_value=False), \
             patch("app.email_em_uso", return_value=False), \
             patch("app.cadastrar_visitante_app") as cadastrar_visitante:
            resposta = self.client.post(
                "/app/cadastro",
                data={
                    "nome": "Visitante Teste",
                    "email": "visitante@exemplo.com",
                    "telefone": "(14) 99999-9999",
                    "whatsapp": "(14) 99999-9999",
                    "senha": "visitante123",
                    "confirmar_senha": "visitante123",
                    "interesse": "Quero conhecer a igreja",
                    "mensagem": "Participei do culto pelo app.",
                },
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])
        cadastrar_visitante.assert_called_once_with(
            "Visitante Teste",
            "visitante@exemplo.com",
            "(14) 99999-9999",
            "(14) 99999-9999",
            "Quero conhecer a igreja",
            "Participei do culto pelo app.",
            "visitante123",
        )

    def test_inserir_membro_valida_telefone(self):
        self.autenticar()

        resposta = self.client.post(
            "/membros/inserir",
            data={"nome": "Novo Membro", "telefone": "123", "ministerio": "Louvor"},
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe um telefone v".encode(), resposta.data)

    def test_login_admin_redireciona_para_dashboard(self):
        resposta = self.client.post(
            "/login",
            data={"email": "admin@igreja.org", "senha": "admin123"},
            follow_redirects=False,
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/dashboard", resposta.headers["Location"])

    def test_login_visitante_redireciona_para_app(self):
        usuario = {
            "id": 2,
            "nome": "Visitante Teste",
            "email": "visitante@igreja.org",
            "senha_hash": generate_password_hash("visitante123"),
            "status": "Ativo",
            "perfil": "Visitante",
        }
        with patch("app.obter_usuario_por_email", return_value=usuario), patch("app.db_write"):
            resposta = self.client.post(
                "/login",
                data={"email": "visitante@igreja.org", "senha": "visitante123"},
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app", resposta.headers["Location"])

    def test_visitante_logado_nao_acessa_admin(self):
        with self.client.session_transaction() as sess:
            sess["usuario_logado"] = "visitante@igreja.org"
            sess["usuario_nome"] = "Visitante Teste"
            sess["usuario_perfil"] = "Visitante"
            sess["usuario_id"] = 2

        resposta = self.client.get("/dashboard", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app", resposta.headers["Location"])

    def test_app_oracao_registra_reacao_publica(self):
        with patch("app.pedido_oracao_publico_existe", return_value=True), patch("app.db_write") as db_write:
            resposta = self.client.post(
                "/app/oracao/10/reagir",
                data={"tipo": "amem", "autor_nome": "Visitante"},
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app/oracao", resposta.headers["Location"])
        self.assertIn("INSERT INTO pedido_oracao_reacoes", db_write.call_args_list[0].args[0])
        self.assertIn("UPDATE pedidos_oracao", db_write.call_args_list[1].args[0])

    def test_app_oracao_registra_comentario_publico(self):
        with patch("app.pedido_oracao_publico_existe", return_value=True), patch("app.db_write") as db_write:
            resposta = self.client.post(
                "/app/oracao/10/comentar",
                data={"autor_nome": "Visitante", "comentario": "Estamos juntos em oracao."},
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app/oracao", resposta.headers["Location"])
        self.assertIn("INSERT INTO pedido_oracao_comentarios", db_write.call_args.args[0])

    def test_exclusao_logica_nao_aceita_get(self):
        self.autenticar()

        for rota in [
            "/membros/excluir/101",
            "/membros/inativar/101",
            "/ministerios/excluir/201",
            "/usuarios/excluir/1",
            "/familias/excluir/1",
            "/fornecedores/excluir/1",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 405)

    def test_acoes_operacionais_nao_aceitam_get(self):
        self.autenticar()

        for rota in [
            "/mural/publicar/1",
            "/mural/arquivar/1",
            "/intercessao/orar/1",
            "/intercessao/responder/1",
            "/intercessao/arquivar/1",
            "/app/oracao/1/reagir",
            "/app/oracao/1/comentar",
            "/doacoes/receber/1",
            "/doacoes/cancelar/1",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 405)

    def test_inativar_membro_usa_post_com_redirect(self):
        self.autenticar()

        resposta = self.client.post("/membros/inativar/103", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/membros/listar", resposta.headers["Location"])


if __name__ == "__main__":
    unittest.main()
