// Shared env vars in all environments
var shared = {
  apiUrl: process.env.API_URL,
  apiToken: process.env.API_TOKEN
};

var environments = {
  development: {
    ENV_VARS: shared
  },
  staging: {
    ENV_VARS: shared
  },
  production: {
    ENV_VARS: shared
  }
};

module.exports = environments;