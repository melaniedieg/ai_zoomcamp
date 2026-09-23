export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
    });
  } catch {
    throw new Error('Cannot reach the backend. Start it on port 8000 and try again.');
  }
  const data = await response.json();
  if (!response.ok) {
    throw new Error(response.status === 409 ? 'This party has already left the waiting list.' :
      response.status === 422 ? 'Enter a name and a party size from 1 to 20.' : data.detail || 'Request failed.');
  }
  return data;
}

export const listParties = () => request('/api/parties');
export const addParty = (name, size) => request('/api/parties', { method: 'POST', body: JSON.stringify({ name, size }) });
export const updateParty = (id, status) => request(`/api/parties/${id}`, { method: 'PATCH', body: JSON.stringify({ status }) });
