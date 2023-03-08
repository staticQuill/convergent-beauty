/* eslint-disable  @typescript-eslint/no-explicit-any */

<script setup lang="ts">

import {userAuthStore} from "@/stores/auth.store";

import {Field, Form, useForm} from 'vee-validate';

interface formObject {
  username: string,
  password: string
}

interface errorObj {
  setErrors: any,
  username: boolean,
  password: boolean
}

const authStore = userAuthStore();
let errorMsg = JSON.parse(localStorage.getItem("error") || "{}")


const { handleSubmit } = useForm<{ username: string, password: string; }>();

const onSubmit = handleSubmit(values => {{
  const username = values.username;
  const password = values.password;

  return authStore.login(username, password)

}
});

let isSubmitting = false

</script>

<template>
  <main>
    <div>
      <h2>
        Log in
      </h2>
      <div v-if="errorMsg">
        <div v-for="(error, type) in errorMsg" :key="error">
          <p v-if="error">There was an error in your {{type}}: </p>
          <ul>
            <li v-for="err in error" :key="err">{{err}}</li>
          </ul>
          <br>
        </div>
      </div>
      <form @submit="onSubmit">
        <div class="form-group float-box">
          <label>Enter your username</label>
          <Field aria-label="Enter Username" name="username" type="text" class="form-control" />
        </div>
        <div class="form-group float-box">
          <label>Enter your password</label>
          <Field aria-label="Enter Password" name="password" type="password" class="form-control" />
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
