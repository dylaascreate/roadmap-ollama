import axios from 'axios';

window.axios = axios;

window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

// IMPORTANT: This allows cookies to be sent back and forth
window.axios.defaults.withCredentials = true; 
window.axios.defaults.withXSRFToken = true;

app.config.globalProperties.$axios = axios