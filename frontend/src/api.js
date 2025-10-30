// Simple backend fetch with proxy fallback
export async function fetchBackend(path, options = {}) {
    // Try relative first (CRA proxy)
    try {
        const res = await fetch(path, options);
        if (res.ok) return res;
    } catch (_) { }

    // Fallback to explicit backend URL
    const backendBase = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
    const url = path.startsWith('http') ? path : `${backendBase}${path.startsWith('/') ? '' : '/'}${path}`;
    return fetch(url, options);
}

export async function fetchBackendJson(path, options = {}) {
    const res = await fetchBackend(path, options);
    const data = await res.json();
    return { res, data };
}



