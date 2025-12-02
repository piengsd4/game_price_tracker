export function getCookie(name: string): string {
  const row = document.cookie
    .split("; ")
    .find(c => c.startsWith(name + "="));

  if (!row) return "";

  const value = row.split("=")[1] ?? "";
  return decodeURIComponent(value);
}
