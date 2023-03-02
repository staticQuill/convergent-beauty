/* eslint-disable  @typescript-eslint/no-explicit-any */

<script setup lang="ts">

import {userAuthStore} from "@/stores/auth.store";

import {Field, Form} from 'vee-validate';

interface formObject {
  username: string,
  email: string,
  password: string,
  password2: string
}

const authStore = userAuthStore();
let errorMsg = {
  password: [],
  email: [],
  username: []
}
errorMsg = JSON.parse(localStorage.getItem("error") || "{}")

function onSubmit(values: formObject) {
  const username = values.username;
  const email = values.email;
  const password = values.password;
  const password2 = values.password2;

  return authStore.signup(username, email, password, password2)

}

let errors = {
  apiError: false,
  username: false,
  password: false
}

let isSubmitting = false

</script>

<template>
  <main>
    <div>
      <h2>
        Create a new account
      </h2>
      <div v-if="errorMsg">
        <div v-for="(error, type) in errorMsg" :key="error">
        <p>There was an error in your {{type}}: </p>
          <ul>
            <li v-for="err in error" :key="err">{{err}}</li>
          </ul>
        <br>
        </div>
      </div>
      <Form @submit="onSubmit">
        <div class="form-group float-box">
          <label>Enter your preferred username</label>
          <Field name="username" type="text" class="form-control" />
        </div>
        <div class="form-group float-box">
          <label>Enter your email address</label>
          <Field name="email" type="email" class="form-control" />
        </div>
        <div class="form-group float-box">
          <label>Choose a password</label>
          <Field name="password" type="password" class="form-control" />
        </div>
        <div class="form-group float-box">
          <label>Enter that password again</label>
          <Field name="password2" type="password" class="form-control" />
        </div>
        <div class="form-group float-box">
          <button class="btn btn-primary" :disabled="isSubmitting">
            <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
            Login
          </button>
        </div>
      </Form>
    </div>
  </main>
</template>
