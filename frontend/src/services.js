export class APIgatewayService {
  serviceURL = process.env.REACT_APP_APIGATEWAY_API_URL;
  loginURL = this.serviceURL + 'auth/login';
  registerURL = this.serviceURL + 'auth/register';

  async login(body) {
    return await fetch(this.loginURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      // mode: 'cors',
      credentials: 'include',

      body: JSON.stringify(body)
    });
  }

  async register(body) {
    return await fetch(this.registerURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      body: JSON.stringify(body)
    });
  }
}
