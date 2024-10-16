const baseUrl = 'http://127.0.0.1:8484';

interface IRequestParams {
  [key: string]: any;
}

export const get = async (url: string, params: IRequestParams = {}) => {
  return await useFetch(`${baseUrl}${url}`, { method: 'GET', params });
};

export const post = async <T extends Record<string, any>>(url: string, body: T) => {
  return await useFetch(`${baseUrl}${url}`, { method: 'POST', body });
};

export const put = async <T extends Record<string, any>>(url: string, body: T) => {
  return await useFetch(`${baseUrl}${url}`, { method: 'PUT', body });
};

export const patch = async <T extends Record<string, any>>(url: string, body: T) => {
  return await useFetch(`${baseUrl}${url}`, { method: 'PATCH', body });
};

export const del = async (url: string, params: IRequestParams = {}) => {
  return await useFetch(`${baseUrl}${url}`, { method: 'DELETE', params });
};
