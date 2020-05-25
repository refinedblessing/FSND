/*
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'refinedblessing-coffee-shop', // the auth0 domain prefix
    audience: 'coffee-dev', // the audience set for the auth0 app
    clientId: 'V0TjMtFe9w51gzgothO9I171YLrVcTlG', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};
