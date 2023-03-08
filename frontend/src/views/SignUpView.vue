/* eslint-disable  @typescript-eslint/no-explicit-any */

<script setup lang="ts">

import {userAuthStore} from "@/stores/auth.store";

import {Field, Form, useForm} from 'vee-validate';

const authStore = userAuthStore();
let errorMsg = {
  password: [],
  email: [],
  username: []
}
errorMsg = JSON.parse(localStorage.getItem("error") || "{}")

const { handleSubmit } = useForm<{ username: string, email: string, password: string, password2: string; }>();

const onSubmit = handleSubmit(values => {{
  const username = values.username;
  const email = values.email;
  const password = values.password;
  const password2 = values.password2;

  return authStore.signup(username, email, password, password2)

}
})

let isSubmitting = false

</script>

<template>
  <main>
    <div>
      <h2>
        Create a new account
      </h2>
      <div v-if="errorMsg">
        <div v-for="(error, type) in errorMsg" :key="type">
        <p>There was an error in your {{type}}: </p>
          <ul>
            <li v-for="err in error" :key="err">{{err}}</li>
          </ul>
        <br>
        </div>
      </div>
      <form @submit="onSubmit">
        <div class="form-group float-box">
          <label>Enter your preferred username</label>
          <Field aria-label="Enter Username" name="username" type="text" class="form-control" />
        </div>
        <div class="form-group float-box">
          <label>Enter your email address</label>
          <Field aria-label="Enter Email" name="email" type="email" class="form-control" />
        </div>
        <div class="form-group float-box">
          <label>Choose a password</label>
          <Field aria-label="Choose Password" name="password" type="password" class="form-control" />
        </div>
        <div class="form-group float-box">
          <label>Enter that password again</label>
          <Field aria-label="Repeat Password" name="password2" type="password" class="form-control" />
        </div>
        <div class="form-group float-box">
          <button class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            Login
          </button>
        </div>
      </form>
    </div>
  </main>
</template>
