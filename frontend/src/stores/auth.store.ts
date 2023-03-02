import { defineStore } from "pinia";
import router from "@/router";
import { NavigationFailureType } from "vue-router";

export const userAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    user: {
      username: "",
      bearerToken: "",
      refreshToken: ""
    },
    returnUrl: "",
    error: ""
  }),
  actions: {
    async login(username: string, password: string) {
      let tokens = {
        access: "",
        refresh: "",
        detail: ""
      };
      const authRequestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({username: username, password: password})
      };
      const tokensJson = await fetch("http://188.166.174.54/auth/login/", authRequestOptions);
      if (tokensJson.status == 401) {
        this.error = "We can't find a a user with that username and password"
        localStorage.setItem('error', JSON.stringify({"attempt": [this.error]}))
        await router.go(0);
      }
      tokens = await tokensJson.json();
      if (tokens.access.length > 1) {
        this.user.username = username
        this.user.bearerToken = "Bearer".concat(" ", tokens.access)
        this.user.refreshToken = tokens.refresh
        localStorage.setItem('user', JSON.stringify(this.user))
        localStorage.setItem('error', JSON.stringify({"error": ""}))
        await router.push(this.returnUrl || '/');
      }
    },
    async signup(username: string, email: string, password: string, password2: string) {
      if (password != password2) {
        this.error = "sorry, those passwords do not match"
        localStorage.setItem('error', this.error)
        await router.go(0);
      }
      const authRequestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({username: username, email: email, password: password, password2: password2})
      };
      const signupJson = await fetch("http://188.166.174.54/auth/signup/", authRequestOptions);
      if (signupJson.status.toString()[0] != "2") {
        localStorage.setItem('error', JSON.stringify(await signupJson.json()))
        await router.go(0);
      }
      if (signupJson.status.toString()[0] === "2") {
        return this.login(username, password)
      }
    },
    async logout() {
      this.user = {
        username: "",
        bearerToken: "",
        refreshToken: ""
      };
      localStorage.removeItem('user');
      await router.push('/login')
    }
  },
  persist: true,
})
