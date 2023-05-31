/**
 * It takes a JWT token and returns the decoded payload.
 * @param token - The JWT token that you want to parse.
 * @returns The token is being parsed and the payload is being returned.
 */
export const parseJwt = (token) => {
    if (!token) {
      return;
    }
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace("-", "+").replace("_", "/");
    return JSON.parse(window.atob(base64));
  };