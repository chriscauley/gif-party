const schema = {
  type: 'object',
  properties: {
    username: { type: 'string', title: 'Username' },
    password: { type: 'string', title: 'Password' },
  },
}

const config = {
  login_redirect: '/',
  makeUrl: (target, next = '') =>
    config[target].next_url.replace(':next', encodeURIComponent(next)),
  login: {
    url: '/login/',
    next_url: '/login/:next',
    post_url: '/api/login/',
    schema: {
      title: 'Login To Continue',
      ...schema,
    },
  },
  signup: {
    url: '/signup/',
    next_url: '/signup/:next',
    post_url: '/api/signup/',
    schema: {
      title: 'Signup To Continue',
      ...schema,
    },
  },
  logout: {
    url: '/logout/',
    post_url: '/api/logout/',
  },
}

export default config
