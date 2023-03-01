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
        localStorage.setItem('error', this.error)
        await router.go(0);
      }
      tokens = await tokensJson.json();
      if (tokens.access.length > 1) {
        this.user.username = username
        this.user.bearerToken = "Bearer".concat(" ", tokens.access)
        this.user.refreshToken = JSON.stringify(tokens.refresh)
        localStorage.setItem('user', JSON.stringify(this.user))
        localStorage.setItem('error', "")
        await router.push(this.returnUrl || '/');
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
