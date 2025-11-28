export const useCsrf = async () => {
    await $fetch("http://localhost:8000/api/auth/csrf/", {
        method: "GET",
        credentials: "include",
    });
}