// GymManager — cliente da API REST (GYM-SRC-006)
// Contrato: documentos/arquitetura/openapi.yaml (GYM-ARQ-003)

const BASE = "/api/v1";
const CHAVE = "gymmanager.sessao";

export class ErroApi extends Error {
  constructor(status, mensagem, campo) {
    super(mensagem);
    this.status = status;
    this.campo = campo;
  }
}

function lerSessao() {
  try {
    return JSON.parse(sessionStorage.getItem(CHAVE)) || null;
  } catch {
    return null;
  }
}

let atual = lerSessao();

export const sessao = {
  get token() {
    return atual?.token || null;
  },
  get usuario() {
    return atual?.usuario || null;
  },
  salvar(dados) {
    atual = { token: dados.token, usuario: dados.usuario, expira_em: dados.expira_em };
    try {
      sessionStorage.setItem(CHAVE, JSON.stringify(atual));
    } catch {
      /* navegação privada: mantém só em memória */
    }
  },
  limpar() {
    atual = null;
    try {
      sessionStorage.removeItem(CHAVE);
    } catch {
      /* ignora */
    }
  },
};

export async function api(metodo, caminho, corpo) {
  const cabecalhos = { Accept: "application/json" };
  if (corpo !== undefined) cabecalhos["Content-Type"] = "application/json";
  if (sessao.token) cabecalhos.Authorization = `Bearer ${sessao.token}`;

  let resposta;
  try {
    resposta = await fetch(BASE + caminho, {
      method: metodo,
      headers: cabecalhos,
      body: corpo !== undefined ? JSON.stringify(corpo) : undefined,
    });
  } catch {
    throw new ErroApi(0, "Não foi possível conectar ao servidor.");
  }

  if (resposta.status === 204) return null;
  let dados = null;
  try {
    dados = await resposta.json();
  } catch {
    /* resposta sem JSON */
  }

  if (!resposta.ok) {
    if (resposta.status === 401 && caminho !== "/auth/login") {
      sessao.limpar();
      window.location.hash = "#/login";
    }
    throw new ErroApi(resposta.status, dados?.erro || "Erro inesperado.", dados?.campo);
  }
  return dados;
}

export const get = (caminho) => api("GET", caminho);
export const post = (caminho, corpo) => api("POST", caminho, corpo ?? {});
export const put = (caminho, corpo) => api("PUT", caminho, corpo);
export const patch = (caminho, corpo) => api("PATCH", caminho, corpo);
export const del = (caminho) => api("DELETE", caminho);

export function consulta(parametros) {
  const busca = new URLSearchParams();
  for (const [chave, valor] of Object.entries(parametros)) {
    if (valor !== undefined && valor !== null && valor !== "") busca.set(chave, valor);
  }
  const texto = busca.toString();
  return texto ? `?${texto}` : "";
}
