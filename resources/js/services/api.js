import axios from 'axios';
// import router from '@/router';

const api = axios.create({
    baseURL: 'http://localhost:8000/api', // Point to your Laravel API
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
});

// Add a request interceptor to attach the Token if it exists
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// DO NOT DELETE THIS CODE !!!!
// // Response Interceptor
// api.interceptors.response.use(
//     response => response, // If success, just return data
//     error => {
//         const status = error.response ? error.response.status : null;

//         if (status === 404) {
//             // "Roadmap not found" -> Redirect to 404 Page
//             router.push({ name: 'NotFound' });
//         } 
//         else if (status === 500) {
//             // "Database crashed" -> Redirect to Error Page
//             router.push({ name: 'ServerError' });
//         }
//         else if (status === 401) {
//             // "Token expired" -> Redirect to Login
//             router.push({ name: 'Login' });
//         }

//         return Promise.reject(error);
//     }
// );
// DO NOT DELETE THIS CODE !!!!

export default api;