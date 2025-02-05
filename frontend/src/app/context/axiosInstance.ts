import axios from 'axios';


// get data base usrl from env file

export const baseURL = process.env.NEXT_PUBLIC_BACKEND_URL  ||'http://127.0.0.1:5000'

const axiosInstance = axios.create({
    baseURL: `${baseURL}/`,
    timeout: 1000000,
    headers: {
    },
});

// Request Interceptor
axiosInstance.interceptors.request.use((config) => {
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Response Interceptor
axiosInstance.interceptors.response.use((response) => {
    // Handle responses
    return response;
}, (error) => {
    // Handle errors
    return Promise.reject(error);
});

export default axiosInstance;