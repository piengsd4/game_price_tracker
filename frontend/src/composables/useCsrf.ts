import axios from "axios";

export const useCsrf = async () => {
    await axios.get("http://localhost:8000/api/auth/csrf/", {
        withCredentials: true,
    });
}