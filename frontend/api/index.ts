// устанавливаем baseUrl в зависимости откуда был выполнен запрос CSR || SSR
const setBaseUrl = () =>
  useRuntimeConfig().public.apiBase || process.env.NUXT_SSR_API_BASE || '';

interface IRequestParams {
  [key: string]: any;
}

export const get = async (url: string, params: IRequestParams = {}) => {
  return await useFetch(`${setBaseUrl()}${url}`, { method: 'GET', params });
};

export const post = async <T extends Record<string, any>>(url: string, body: T) => {
  return await useFetch(`${setBaseUrl()}${url}`, { method: 'POST', body });
};

export const put = async <T extends Record<string, any>>(url: string, body: T) => {
  return await useFetch(`${setBaseUrl()}${url}`, { method: 'PUT', body });
};

export const patch = async <T extends Record<string, any>>(url: string, body: T) => {
  return await useFetch(`${setBaseUrl()}${url}`, { method: 'PATCH', body });
};

export const del = async (url: string, params: IRequestParams = {}) => {
  return await useFetch(`${setBaseUrl()}${url}`, { method: 'DELETE', params });
};
