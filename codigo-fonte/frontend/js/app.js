// GymManager — roteamento por hash e menu por perfil (GYM-SRC-006, RF07)

import { post, sessao } from "./api.js";
import { $, erro, esc, iniciais } from "./ui.js";
import {
  telaAlunos, telaExercicios, telaFichas, telaHistorico, telaLogin, telaMinhasFichas,
  telaMontarFicha, telaPainel, telaTreino, telaUsuarios,
} from "./telas.js";

const EQUIPE = ["ADMIN", "INSTRUTOR"];
const TODOS = ["ADMIN", "INSTRUTOR", "ALUNO"];

// Rotas: padrão, tela, perfis permitidos. A verificação definitiva é no backend (RNF02).
const ROTAS = [
  { padrao: /^\/painel$/, tela: telaPainel, perfis: TODOS },                       // TL02
  { padrao: /^\/usuarios$/, tela: telaUsuarios, perfis: ["ADMIN"] },              // TL03
  { padrao: /^\/alunos$/, tela: telaAlunos, perfis: EQUIPE },                     // TL04
  { padrao: /^\/exercicios$/, tela: telaExercicios, perfis: EQUIPE },             // TL05
  { padrao: /^\/fichas$/, tela: telaFichas, perfis: EQUIPE },                     // TL06
  { padrao: /^\/fichas\/nova$/, tela: telaMontarFicha, perfis: EQUIPE },          // TL06
  { padrao: /^\/fichas\/(?<id>\d+)$/, tela: telaMontarFicha, perfis: EQUIPE },    // TL06
  { padrao: /^\/minhas-fichas$/, tela: telaMinhasFichas, perfis: ["ALUNO"] },     // TL07
  { padrao: /^\/treino\/(?<id>\d+)$/, tela: telaTreino, perfis: ["ALUNO"] },      // TL08
  { padrao: /^\/historico$/, tela: telaHistorico, perfis: TODOS },                // TL09
];

const MENU = [
  { href: "#/painel", rotulo: "Painel", icone: "▦", perfis: TODOS },
  { href: "#/usuarios", rotulo: "Usuários", icone: "◎", perfis: ["ADMIN"] },
  { href: "#/alunos", rotulo: "Alunos", icone: "☺", perfis: EQUIPE },
  { href: "#/fichas", rotulo: "Treinos", icone: "☰", perfis: EQUIPE },
  { href: "#/exercicios", rotulo: "Exercícios", icone: "↯", perfis: EQUIPE },
  { href: "#/minhas-fichas", rotulo: "Meu treino", icone: "☰", perfis: ["ALUNO"] },
  { href: "#/historico", rotulo: "Histórico", icone: "↗", perfis: TODOS },
];

const NOME_PERFIL = { ADMIN: "Administrador", INSTRUTOR: "Instrutor", ALUNO: "Aluno" };

function layout(caminho) {
  const u = sessao.usuario;
  const itens = MENU.filter((m) => m.perfis.includes(u.perfil))
    .map((m) => {
      const ativo = caminho.startsWith(m.href.slice(1)) ? "ativo" : "";
      return `<a class="${ativo}" href="${m.href}"><span aria-hidden="true">${m.icone}</span>${m.rotulo}</a>`;
    }).join("");
  return `
    <aside class="lateral" id="lateral">
      <div class="marca"><span class="marca-icone">◆</span> GymManager
        <button class="btn-menu" id="btn-menu" aria-label="Abrir menu" aria-expanded="false">☰</button></div>
      <nav class="menu" id="menu">${itens}</nav>
      <div class="perfil-usuario">
        <span class="avatar avatar-escuro">${esc(iniciais(u.nome))}</span>
        <div><strong>${esc(u.nome)}</strong><small>${NOME_PERFIL[u.perfil]}</small></div>
        <button class="btn-sair" id="btn-sair" title="Sair">Sair</button>
      </div>
    </aside>
    <main class="conteudo" id="conteudo" tabindex="-1"><p class="carregando">Carregando...</p></main>`;
}

async function navegar() {
  const hash = window.location.hash.slice(1) || "/painel";
  const [caminho, busca = ""] = hash.split("?");
  const parametros = new URLSearchParams(busca);
  const app = $("#app");

  if (!sessao.token) {
    app.onclick = null;
    if (caminho !== "/login") { window.location.hash = "#/login"; return; }
    await telaLogin(app);
    return;
  }
  if (caminho === "/login") { window.location.hash = "#/painel"; return; }

  const rota = ROTAS.find((r) => r.padrao.test(caminho));
  if (!rota || !rota.perfis.includes(sessao.usuario.perfil)) { window.location.hash = "#/painel"; return; }

  app.onclick = null;
  app.innerHTML = layout(caminho);
  $("#btn-sair").onclick = sair;
  $("#btn-menu").onclick = () => {
    const aberto = $("#lateral").classList.toggle("aberto");
    $("#btn-menu").setAttribute("aria-expanded", String(aberto));
  };

  const conteudo = $("#conteudo");
  try {
    await rota.tela(conteudo, rota.padrao.exec(caminho).groups || {}, parametros);
  } catch (e) {
    if (e.status !== 401) {
      conteudo.innerHTML = `<div class="cartao"><p class="vazio">Não foi possível carregar a página.</p></div>`;
      erro(e);
    }
  }
  conteudo.focus({ preventScroll: true });
}

async function sair() {
  try { await post("/auth/logout"); } catch { /* sessão já inválida */ }
  sessao.limpar();
  window.location.hash = "#/login";
}

window.addEventListener("hashchange", navegar);
navegar();
