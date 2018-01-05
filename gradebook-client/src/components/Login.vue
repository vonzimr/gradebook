<template>
  <div id="container" class="l-container">
    <div v-if="!loggedIn">
      <div>
        <input type="text" v-model="user"/>
        <input type="password" v-model="password"/>
        <button @click="login"> Login </button>
        {{ response }}
      </div>
      <div>
        <input placeholder="username" type="text" v-model="user"/>
        <input placeholder="email" type="email" v-model="email"/>
        <input placeholder="password" v-model="password"/>
        <input placeholder="confirm password" type="password" v-model="passwordConfComp"/>
        <button @click="register"> Register </button>
        <div v-if="passwordCompare"> Passwords are the same!</div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  components: {
  },
  data () {
    return {
      user: '',
      email: '',
      password: '',
      passwordConf: false,
      passwordCompare: false,
      response: 'Login!',
      loggedIn: false
    }
  },
  methods: {
    login: function () {
      axios.post(`api/accounts/login`, {
        username: this.user,
        password: this.password
      }).then((response) => {
        console.log(response)
        window.localStorage.setItem('auth_token', response)
        axios.defaults.headers.common['Authorization'] = `Bearer ${response['data']['access_token']}`
        this.response = 'Success!'
        this.loggedIn = true
      }).catch((error) => {
        if (error) {
          console.log(error)
        }
        this.response = 'Bad username/password'
      })
      console.log(this.$jwt.hasToken())
    },
    register: function () {
      axios.post(`/api/accounts/create`, {
        username: this.user,
        email: this.email,
        password: this.password,
        role: 'teacher'
      }).then((response) => {
        console.log(response)
        this.response = 'Success!'
      }).catch((error) => {
        if (error) {
          console.log(error)
        }
        this.response = 'Bad username/password'
      })
    }
  },
  computed: {
    passwordConfComp: {
      set: function (val) {
        this.passwordConf = val
        if (val !== this.password) {
          this.passwordCompare = false
        } else {
          this.passwordCompare = true
        }
      },
      get: function () {
        return this.passwordConf
      }
    }
  },
  mounted: function () {
    // this.loggedIn = this.$jwt.hasToken()
    // console.log(this.$jwt.hasToken());
  }
}
</script>
</style>
