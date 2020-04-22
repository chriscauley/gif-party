const schema = {
  type: "object",
  properties: {
    username: { type: 'string', title: 'Username' },
    password: { type: 'string', title: 'Password' },
  }
}


export default {
  login: {
    url: "#/login/",
    post_url: "/api/login/",
    schema: {
      title: "Login To Continue",
      ...schema
    },
  },
  signup: {
    url: "#/signup/",
    post_url: "/api/signup/",
    schema: {
      title: "Signup To Continue",
      ...schema
    },
  },
  logout: {
    url: "#/login/",
    post_url: "/api/logout/",
  }
}