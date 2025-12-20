import axios from 'axios';

// axios.defaults.withCredentials = true

const api = axios.create({
    baseURL: '/api', // Matches your api.php prefix
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
});

// Add a request interceptor to attach the token
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;