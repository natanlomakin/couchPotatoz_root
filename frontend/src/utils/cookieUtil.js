import Cookies from "js-cookie";

// Store a cookie
export function setCookie(name, value, options = {}) {
  Cookies.set(name, value, options);
}

// Retrieve a cookie
export function getCookie(name) {
  return Cookies.get(name);
}

// Remove a cookie
export function removeCookie(name) {
  Cookies.remove(name);
}
